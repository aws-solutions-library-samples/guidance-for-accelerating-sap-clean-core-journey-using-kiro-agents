#!/usr/bin/env python3
"""
SAP Custom Code Documenter - Summary Generator

Generates SUMMARY.md from discovery.json and progress.json data.
This is the standard summary generation script - DO NOT create custom scripts.

Usage:
    python3 generate-summary.py <PACKAGE>

Example:
    python3 generate-summary.py Z_FLIGHT
"""

import json
import os
import re
import sys
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from collections import Counter

# CC_DIR: Clean Core root directory
# Auto-derive from script location if not set (script is in agents/documenter/)
CC_DIR = os.environ.get("CC_DIR") or str(Path(__file__).resolve().parent.parent.parent)
BASE_DIR = CC_DIR  # Alias for compatibility

# Pre-compiled regex patterns (compiled once at module load)
PACKAGE_NAME_PATTERN = re.compile(r'^[A-Z][A-Z0-9_]{0,29}$')


def validate_package_name(name):
    """Validate SAP package name format to prevent path traversal."""
    if not name:
        print("ERROR: Package name is required", file=sys.stderr)
        sys.exit(1)
    if not PACKAGE_NAME_PATTERN.match(name):
        print(f"ERROR: Invalid package name: {name}", file=sys.stderr)
        print("Package name must start with A-Z and contain only A-Z, 0-9, _ (max 30 chars)", file=sys.stderr)
        sys.exit(1)
    return name


def load_json(path):
    """Load JSON file with error handling."""
    try:
        if not path.exists():
            print(f"WARNING: File not found: {path}", file=sys.stderr)
            return None
        with open(path, encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                print(f"WARNING: Empty file: {path}", file=sys.stderr)
                return None
            return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {path}: {e}", file=sys.stderr)
        return None
    except UnicodeDecodeError as e:
        print(f"ERROR: Encoding error in {path}: {e}", file=sys.stderr)
        return None


def load_discovery(package_dir):
    """Load discovery.json for package overview."""
    discovery_path = package_dir / "discovery.json"
    return load_json(discovery_path)


def generate_package_overview(discovery, progress):
    """Generate Package Overview section from discovery.json."""
    lines = ["## Package Overview", ""]

    if discovery:
        sap_system = discovery.get("sapSystem", {})
        lines.append(f"**SAP System**: {sap_system.get('sid', 'N/A')} (Client {sap_system.get('client', 'N/A')})")
        lines.append(f"**Search Timestamp**: {discovery.get('timestamp', 'N/A')}")

        results = discovery.get("results", {})
        total_found = results.get("totalFound", 0)
        lines.append(f"**Total Objects Found**: {total_found}")
        lines.append("")
        lines.append("### Objects by Type (from SAP)")
        lines.append("| Type | Count |")
        lines.append("|------|-------|")

        by_type = results.get("byType", {})
        for obj_type, count in sorted(by_type.items(), key=lambda x: -x[1]):
            lines.append(f"| {obj_type} | {count} |")
    else:
        lines.append("*Discovery data not available*")

    return "\n".join(lines)


def generate_filtering_summary(progress):
    """Generate Filtering Summary section from progress.json."""
    filtering = progress.get("filtering", {})
    lines = ["## Filtering Summary", ""]

    discovery_ref = progress.get("discovery", {})
    total_found = discovery_ref.get("totalFound", 0)
    total_documentable = filtering.get("totalDocumentable", 0)
    total_skipped = filtering.get("totalSkipped", 0)

    documentable_types = filtering.get("documentableTypes", [])
    if documentable_types:
        lines.append(f"**Documentable Types**: {', '.join(documentable_types)}")
    lines.append(f"**Total Documentable**: {total_documentable}")
    lines.append(f"**Total Skipped**: {total_skipped}")
    lines.append("")

    # Validation check
    if total_found > 0 and total_found != total_documentable + total_skipped:
        lines.append(f"**WARNING**: Count mismatch! {total_found} != {total_documentable} + {total_skipped}")
        lines.append("")

    # Skipped by type breakdown
    skipped = filtering.get("skippedByType", {})
    if skipped:
        lines.append("### Skipped Object Types")
        lines.append("| Type | Count | Reason |")
        lines.append("|------|-------|--------|")
        for obj_type, count in sorted(skipped.items(), key=lambda x: -x[1]):
            lines.append(f"| {obj_type} | {count} | Not documentable (no source) |")

    return "\n".join(lines)


def calculate_type_distribution(objects):
    """Calculate object type distribution from objects list."""
    total = len(objects)
    type_counts = Counter()

    for obj in objects:
        obj_type = obj.get("type", "UNKNOWN").split("/")[0]  # Get base type
        type_counts[obj_type] += 1

    distribution = {}
    for obj_type, count in type_counts.items():
        pct = f"{round(count * 100 / total)}%" if total > 0 else "0%"
        distribution[obj_type] = {"count": count, "percentage": pct}

    return distribution


def generate_type_distribution_table(distribution):
    """Generate Object Type Distribution table."""
    type_labels = {
        "CLAS": "Classes (CLAS)",
        "PROG": "Programs (PROG)",
        "INTF": "Interfaces (INTF)",
        "FUGR": "Function Groups (FUGR)",
        "DDLS": "CDS Views (DDLS)",
        "DCLS": "Access Controls (DCLS)",
        "DDLX": "Metadata Extensions (DDLX)",
        "BDEF": "Behavior Definitions (BDEF)",
        "SRVD": "Service Definitions (SRVD)",
    }

    lines = [
        "| Type | Count | % |",
        "|------|-------|---|"
    ]

    # Sort by count descending
    sorted_types = sorted(distribution.items(), key=lambda x: -x[1]["count"])

    for obj_type, data in sorted_types:
        label = type_labels.get(obj_type, obj_type)
        count = data["count"]
        pct = data["percentage"]
        lines.append(f"| {label} | {count} | {pct} |")

    return "\n".join(lines)


def generate_documented_table(objects):
    """Generate documented objects table."""
    documented = [obj for obj in objects if obj.get("status") == "documented"]

    if not documented:
        return "No documented objects."

    lines = [
        "| Object | Type | Doc |",
        "|--------|------|-----|"
    ]

    for obj in sorted(documented, key=lambda x: x.get("name", "")):
        name = obj.get("name", "")
        obj_type = obj.get("type", "").split("/")[0]  # Remove suffix
        report_file = obj.get("reportFile", f"{name}.md")
        lines.append(f"| {name} | {obj_type} | [View](./{report_file}) |")

    return "\n".join(lines)


def generate_failed_objects_table(objects):
    """Generate failed objects table."""
    failed = [obj for obj in objects if obj.get("status") == "failed"]

    if not failed:
        return "No failed objects."

    lines = [
        "| Object | Type | Reason |",
        "|--------|------|--------|"
    ]

    for obj in failed:
        name = obj.get("name", "")
        obj_type = obj.get("type", "").split("/")[0]
        error = obj.get("error", "Unknown error")
        lines.append(f"| {name} | {obj_type} | {error} |")

    return "\n".join(lines)


def parse_objects_from_doc_files(reports_dir):
    """Parse object info directly from documentation files when progress.json is unavailable."""
    objects = []

    for doc_file in reports_dir.glob("*.md"):
        if doc_file.name == "SUMMARY.md":
            continue

        name = doc_file.stem

        # Try to extract type from file content
        content = doc_file.read_text(encoding='utf-8')
        obj_type = "UNKNOWN"

        # Look for type in the metadata table
        type_match = re.search(r"\|\s*Type\s*\|\s*([^|]+)\s*\|", content)
        if type_match:
            type_text = type_match.group(1).strip()
            # Map common type descriptions back to codes
            type_map = {
                "Class": "CLAS",
                "Program": "PROG",
                "Interface": "INTF",
                "Function Group": "FUGR",
                "CDS View": "DDLS",
                "Access Control": "DCLS",
                "Metadata Extension": "DDLX",
                "Behavior Definition": "BDEF",
                "Service Definition": "SRVD",
            }
            for label, code in type_map.items():
                if label.lower() in type_text.lower():
                    obj_type = code
                    break

        objects.append({
            "name": name,
            "type": obj_type,
            "status": "documented",
            "reportFile": doc_file.name
        })

    return objects


def generate_summary(package_name):
    """Generate the SUMMARY.md report."""

    # Paths
    reports_dir = Path(f"{BASE_DIR}/reports/docs/{package_name}")
    progress_file = reports_dir / "progress.json"
    discovery_file = reports_dir / "discovery.json"
    summary_file = reports_dir / "SUMMARY.md"

    # Load discovery.json (may not exist for legacy runs)
    print(f"Loading discovery from {discovery_file}...", file=sys.stderr)
    discovery = load_discovery(reports_dir)
    if discovery:
        print(f"  Found {discovery.get('results', {}).get('totalFound', 0)} total objects from SAP", file=sys.stderr)

    # Load from progress.json if exists, otherwise scan doc files
    if progress_file.exists():
        print(f"Loading progress from {progress_file}...", file=sys.stderr)
        progress = load_json(progress_file)
        objects = progress.get("objects", [])
        archive_files = True
    else:
        print(f"No progress.json found, scanning documentation files...", file=sys.stderr)
        objects = parse_objects_from_doc_files(reports_dir)
        progress = {"package": package_name}
        archive_files = False
        print(f"  Found {len(objects)} documentation files", file=sys.stderr)

    # Extract data
    documented_objects = [obj for obj in objects if obj.get("status") == "documented"]
    failed_objects = [obj for obj in objects if obj.get("status") == "failed"]

    # Calculate type distribution from documented objects
    distribution = calculate_type_distribution(documented_objects)

    # Get metadata
    package = progress.get("package", package_name)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate summary content
    content = f"""# Documentation Catalog: {package}

| Field | Value |
|-------|-------|
| Package | {package} |
| Generated | {timestamp} |
| Total Objects (Documentable) | {len(objects)} |
| Documented | {len(documented_objects)} |
| Failed | {len(failed_objects)} |

{generate_package_overview(discovery, progress)}

{generate_filtering_summary(progress)}

## By Object Type

{generate_type_distribution_table(distribution)}

## Object Inventory

{generate_documented_table(objects)}

## Failed Objects

{generate_failed_objects_table(objects)}
"""

    # Write summary atomically
    fd, temp_path = tempfile.mkstemp(dir=reports_dir, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        os.replace(temp_path, summary_file)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise
    print(f"  Summary: {summary_file}", file=sys.stderr)

    # Archive both files (only if we loaded from progress.json)
    archive_discovery_path = None
    archive_progress_path = None
    if archive_files:
        # Use same timestamp for both files
        archive_timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")

        # Archive discovery.json if it exists
        if discovery_file.exists():
            archive_name = f"{archive_timestamp}-discovery.json"
            archive_discovery_path = reports_dir / archive_name
            shutil.copy(discovery_file, archive_discovery_path)
            discovery_file.unlink()
            print(f"  Archived discovery to: {archive_name}", file=sys.stderr)

        # Archive progress.json
        if progress_file.exists():
            archive_name = f"{archive_timestamp}-progress.json"
            archive_progress_path = reports_dir / archive_name
            shutil.copy(progress_file, archive_progress_path)
            progress_file.unlink()
            print(f"  Archived progress to: {archive_name}", file=sys.stderr)

    # Summary stats
    print(f"\nSummary generated successfully!", file=sys.stderr)
    print(f"  Package: {package}", file=sys.stderr)
    print(f"  Total objects (documentable): {len(objects)}", file=sys.stderr)
    if discovery:
        total_from_sap = discovery.get("results", {}).get("totalFound", 0)
        print(f"  Total from SAP: {total_from_sap}", file=sys.stderr)
    print(f"  Documented: {len(documented_objects)}", file=sys.stderr)
    print(f"  Failed: {len(failed_objects)}", file=sys.stderr)

    return {
        "status": "success",
        "package": package,
        "summaryFile": str(summary_file),
        "archivedDiscovery": str(archive_discovery_path) if archive_discovery_path else None,
        "archivedProgress": str(archive_progress_path) if archive_progress_path else None,
        "totalObjects": len(objects),
        "totalFromSap": discovery.get("results", {}).get("totalFound", 0) if discovery else None,
        "documented": len(documented_objects),
        "failed": len(failed_objects),
        "typeDistribution": {k: v["count"] for k, v in distribution.items()}
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate-summary.py <PACKAGE>", file=sys.stderr)
        print("Example: python3 generate-summary.py Z_FLIGHT", file=sys.stderr)
        sys.exit(1)

    package_name = validate_package_name(sys.argv[1])
    result = generate_summary(package_name)
    print(json.dumps(result))


if __name__ == "__main__":
    main()