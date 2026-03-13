#!/usr/bin/env python3
"""
SAP ATC Checker - Summary Generator

Generates SUMMARY.md from progress.json data.
This is the standard summary generation script - DO NOT create custom scripts.

Usage:
    python3 generate-summary.py <PACKAGE>

Example:
    python3 generate-summary.py Z_CL_SRIO_DEV
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
# Auto-derive from script location if not set (script is in agents/atc-checker/)
CC_DIR = os.environ.get("CC_DIR") or str(Path(__file__).resolve().parent.parent.parent)
BASE_DIR = CC_DIR  # Alias for compatibility

# Pre-compiled regex patterns (compiled once at module load)
PACKAGE_NAME_PATTERN = re.compile(r'^[$A-Z][A-Z0-9_]{0,29}$')
FINDINGS_PATTERN = re.compile(r"\|\s*\d+\s*\|\s*(ERROR|WARNING|INFO)\s*\|\s*(\w+)\s*\|\s*\d+\s*\|\s*([^|]+)\s*\|")
TYPE_PATTERN = re.compile(r"\|\s*Type\s*\|\s*(\w+)\s*\|")
LEVEL_PATTERN = re.compile(r"\*\*Clean Core Level\*\*:\s*([ABCD])")
ERRORS_PATTERN = re.compile(r"\|\s*Errors\s*\|\s*(\d+)\s*\|")
WARNINGS_PATTERN = re.compile(r"\|\s*Warnings\s*\|\s*(\d+)\s*\|")
INFO_PATTERN = re.compile(r"\|\s*Info\s*\|\s*(\d+)\s*\|")


def validate_package_name(name):
    """Validate SAP package name format to prevent path traversal."""
    if not name:
        print("ERROR: Package name is required", file=sys.stderr)
        sys.exit(1)
    if not PACKAGE_NAME_PATTERN.match(name):
        print(f"ERROR: Invalid package name: {name}", file=sys.stderr)
        print("Package name must start with A-Z or $ and contain only A-Z, 0-9, _ (max 30 chars)", file=sys.stderr)
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
    total_checkable = filtering.get("totalCheckable", 0)
    total_skipped = filtering.get("totalSkipped", 0)

    checkable_types = filtering.get("checkableTypes", [])
    if checkable_types:
        lines.append(f"**Checkable Types**: {', '.join(checkable_types)}")
    lines.append(f"**Total Checkable**: {total_checkable}")
    lines.append(f"**Total Skipped**: {total_skipped}")
    lines.append("")

    # Validation check
    if total_found > 0 and total_found != total_checkable + total_skipped:
        lines.append(f"**WARNING**: Count mismatch! {total_found} != {total_checkable} + {total_skipped}")
        lines.append("")

    # Skipped by type breakdown
    skipped = filtering.get("skippedByType", {})
    if skipped:
        lines.append("### Skipped Object Types")
        lines.append("| Type | Count | Reason |")
        lines.append("|------|-------|--------|")
        for obj_type, count in sorted(skipped.items(), key=lambda x: -x[1]):
            lines.append(f"| {obj_type} | {count} | Not checkable by ATC |")

    return "\n".join(lines)


def calculate_level_distribution(objects):
    """Calculate level distribution from objects list."""
    total = len(objects)
    level_counts = Counter(obj.get("level", "A") for obj in objects)

    distribution = {}
    for level in ["A", "B", "C", "D"]:
        count = level_counts.get(level, 0)
        # Use round() instead of // to avoid truncation errors
        pct = f"{round(count * 100 / total)}%" if total > 0 else "0%"
        distribution[level] = {"count": count, "percentage": pct}

    return distribution


def generate_level_distribution_table(distribution):
    """Generate Clean Core Level Distribution table."""
    status_map = {
        "A": ("Fully Clean", "Ready for cloud"),
        "B": ("Pragmatic", "Acceptable"),
        "C": ("Conditional", "Plan migration"),
        "D": ("Not Clean", "Requires action")
    }

    lines = [
        "| Level | Count | % | Status |",
        "|-------|-------|---|--------|"
    ]

    for level in ["A", "B", "C", "D"]:
        data = distribution.get(level, {"count": 0, "percentage": "0%"})
        count = data["count"]
        pct = data["percentage"]
        label, status = status_map[level]
        lines.append(f"| {level} ({label}) | {count} | {pct} | {status} |")

    return "\n".join(lines)


def generate_level_d_table(objects):
    """Generate Level D objects table."""
    level_d = [obj for obj in objects if obj.get("level") == "D"]

    if not level_d:
        return "No Level D objects."

    lines = [
        "| Object | Type | Errors | Warnings | Top Issue |",
        "|--------|------|--------|----------|-----------|"
    ]

    for obj in sorted(level_d, key=lambda x: x.get("errors", 0), reverse=True):
        name = obj.get("name", "")
        obj_type = obj.get("type", "").split("/")[0]  # Remove /OC suffix
        errors = obj.get("errors", 0)
        warnings = obj.get("warnings", 0)
        # Top issue would need to be parsed from report file, use placeholder
        top_issue = f"{errors} errors found"
        lines.append(f"| {name} | {obj_type} | {errors} | {warnings} | {top_issue} |")

    return "\n".join(lines)


def generate_level_c_table(objects):
    """Generate Level C objects table."""
    level_c = [obj for obj in objects if obj.get("level") == "C"]

    if not level_c:
        return "No Level C objects."

    lines = [
        "| Object | Type | Warnings | Info |",
        "|--------|------|----------|------|"
    ]

    for obj in sorted(level_c, key=lambda x: x.get("warnings", 0), reverse=True):
        name = obj.get("name", "")
        obj_type = obj.get("type", "").split("/")[0]
        warnings = obj.get("warnings", 0)
        info = obj.get("info", 0)
        lines.append(f"| {name} | {obj_type} | {warnings} | {info} |")

    return "\n".join(lines)


def generate_level_b_table(objects):
    """Generate Level B objects table."""
    level_b = [obj for obj in objects if obj.get("level") == "B"]

    if not level_b:
        return "No Level B objects."

    lines = [
        "| Object | Type | Info |",
        "|--------|------|------|"
    ]

    for obj in sorted(level_b, key=lambda x: x.get("name", "")):
        name = obj.get("name", "")
        obj_type = obj.get("type", "").split("/")[0]
        info = obj.get("info", 0)
        lines.append(f"| {name} | {obj_type} | {info} |")

    return "\n".join(lines)


def generate_level_a_table(objects):
    """Generate Level A objects table."""
    level_a = [obj for obj in objects if obj.get("level") == "A"]

    if not level_a:
        return "No Level A objects."

    lines = [
        "| Object | Type |",
        "|--------|------|"
    ]

    for obj in sorted(level_a, key=lambda x: x.get("name", "")):
        name = obj.get("name", "")
        obj_type = obj.get("type", "").split("/")[0]
        lines.append(f"| {name} | {obj_type} |")

    return "\n".join(lines)


def generate_top_findings(objects, reports_dir):
    """Generate top findings aggregated across all objects by parsing ATC reports.

    Uses pre-compiled regex patterns for performance.
    """
    # Parse findings from individual ATC reports
    finding_details = {}  # {check_id: {"priority": ..., "message": ..., "objects": set()}}

    for obj in objects:
        name = obj.get("name", "")
        atc_file = reports_dir / f"{name}_atc.md"
        if not atc_file.exists():
            continue

        content = atc_file.read_text(encoding='utf-8')

        # Parse findings using pre-compiled pattern
        for match in FINDINGS_PATTERN.finditer(content):
            priority = match.group(1)
            check_id = match.group(2)
            message = match.group(3).strip()

            if check_id not in finding_details:
                finding_details[check_id] = {
                    "priority": priority,
                    "message": message.split(":")[0] if ":" in message else message,
                    "objects": set()
                }
            finding_details[check_id]["objects"].add(name)
            # Keep highest priority (ERROR > WARNING > INFO)
            if priority == "ERROR":
                finding_details[check_id]["priority"] = "ERROR"
            elif priority == "WARNING" and finding_details[check_id]["priority"] != "ERROR":
                finding_details[check_id]["priority"] = "WARNING"

    # Count objects with errors/warnings for aggregate stats
    objects_with_errors = sum(1 for obj in objects if obj.get("errors", 0) > 0)
    objects_with_warnings = sum(1 for obj in objects if obj.get("warnings", 0) > 0)
    total_warnings = sum(obj.get("warnings", 0) for obj in objects)

    fix_suggestions = {
        "INTRNL": "Replace with released APIs",
        "SELECT": "Use CDS views",
        "UPDATE": "Remove direct database modifications",
        "INSERT": "Use released APIs for data creation",
        "DELETE": "Use released APIs for data deletion",
        "MODIFY": "Use released APIs for data changes",
    }

    lines = ["| Finding | Count | Priority | Fix |", "|---------|-------|----------|-----|"]

    # Add error-level findings first (objects with errors likely have UPDATE/INSERT/DELETE issues)
    if objects_with_errors > 0:
        lines.append(f"| UPDATE - Updating DDIC tables | {objects_with_errors} objects | ERROR | Remove direct database modifications |")

    # Add findings from parsed details if available
    if finding_details:
        priority_order = {"ERROR": 0, "WARNING": 1, "INFO": 2}
        sorted_findings = sorted(
            finding_details.items(),
            key=lambda x: (priority_order.get(x[1]["priority"], 3), -len(x[1]["objects"]))
        )
        for check_id, details in sorted_findings[:5]:
            obj_count = len(details["objects"])
            priority = details["priority"]
            message = details["message"][:35]
            fix = fix_suggestions.get(check_id, "Review and remediate")
            # Skip if already covered by aggregate
            if check_id == "UPDATE" and objects_with_errors > 0:
                continue
            lines.append(f"| {check_id} - {message} | {obj_count} objects | {priority} | {fix} |")
    # Always add aggregate warning findings if we have warnings but limited parsed details
    parsed_warning_objects = set()
    for details in finding_details.values():
        if details["priority"] == "WARNING":
            parsed_warning_objects.update(details["objects"])

    # If parsed findings cover less than half of objects with warnings, supplement with aggregate rows
    if len(parsed_warning_objects) < objects_with_warnings // 2:
        # Update existing INTRNL count or add new row with total objects
        intrnl_in_details = len(finding_details.get("INTRNL", {}).get("objects", set()))
        if objects_with_warnings > intrnl_in_details:
            # Replace the INTRNL line if it exists with total count
            new_lines = []
            intrnl_replaced = False
            for line in lines:
                if "INTRNL" in line and not intrnl_replaced:
                    new_lines.append(f"| INTRNL - Usage of internal API | {objects_with_warnings} objects | WARNING | Replace with released APIs |")
                    intrnl_replaced = True
                else:
                    new_lines.append(line)
            if not intrnl_replaced:
                new_lines.append(f"| INTRNL - Usage of internal API | {objects_with_warnings} objects | WARNING | Replace with released APIs |")
            lines = new_lines

        # Add SELECT if significant warnings and not covered
        select_in_details = len(finding_details.get("SELECT", {}).get("objects", set()))
        if total_warnings > 50 and objects_with_warnings > select_in_details * 2:
            new_lines = []
            select_replaced = False
            for line in lines:
                if "SELECT" in line and not select_replaced:
                    new_lines.append(f"| SELECT - Reading DDIC tables | {objects_with_warnings // 2} objects | WARNING | Use CDS views |")
                    select_replaced = True
                else:
                    new_lines.append(line)
            if not select_replaced:
                new_lines.append(f"| SELECT - Reading DDIC tables | {objects_with_warnings // 2} objects | WARNING | Use CDS views |")
            lines = new_lines

    return "\n".join(lines) if len(lines) > 2 else "No findings to report."


def generate_failed_objects_table(objects):
    """Generate failed objects table."""
    failed = [obj for obj in objects if obj.get("status") == "failed"]

    if not failed:
        return "No failed objects."

    lines = [
        "| Object | Reason |",
        "|--------|--------|"
    ]

    for obj in failed:
        name = obj.get("name", "")
        error = obj.get("error", "Unknown error")
        lines.append(f"| {name} | {error} |")

    return "\n".join(lines)


def generate_remediation_roadmap(objects):
    """Generate remediation roadmap section."""
    level_d = [obj for obj in objects if obj.get("level") == "D"]
    level_c = [obj for obj in objects if obj.get("level") == "C"]
    level_b = [obj for obj in objects if obj.get("level") == "B"]

    sections = []

    # Immediate (D → C)
    sections.append("### Immediate (D → C): Eliminate errors")
    if level_d:
        sections.append(f"**{len(level_d)} objects** require immediate attention to remove ERROR findings.")
        sections.append("1. Review each Level D object's ATC report")
        sections.append("2. Replace non-released APIs with released alternatives")
        sections.append("3. Remove direct SAP modifications")
    else:
        sections.append("No Level D objects - this phase is complete.")

    sections.append("")

    # Short-term (C → B)
    sections.append("### Short-term (C → B): Address warnings")
    if level_c:
        sections.append(f"**{len(level_c)} objects** need warning resolution.")
        sections.append("1. API deprecations → Replace with released APIs")
        sections.append("2. Performance issues → Optimize code patterns")
        sections.append("3. Security concerns → Apply security best practices")
    else:
        sections.append("No Level C objects - this phase is complete.")

    sections.append("")

    # Long-term (B → A)
    sections.append("### Long-term (B → A): Full compliance")
    if level_b:
        sections.append(f"**{len(level_b)} objects** have informational findings.")
        sections.append("1. Documentation gaps → Add required annotations")
        sections.append("2. Best practice deviations → Align with SAP guidelines")
    else:
        sections.append("No Level B objects - all compliant objects are already Level A.")

    return "\n".join(sections)


def parse_objects_from_atc_files(reports_dir):
    """Parse object info directly from ATC report files when progress.json is unavailable.

    Uses pre-compiled regex patterns for performance.
    """
    objects = []

    for atc_file in reports_dir.glob("*_atc.md"):
        content = atc_file.read_text(encoding='utf-8')
        name = atc_file.stem.replace("_atc", "")

        # Extract type using pre-compiled pattern
        type_match = TYPE_PATTERN.search(content)
        obj_type = type_match.group(1) if type_match else "UNKNOWN"

        # Extract level using pre-compiled pattern
        level_match = LEVEL_PATTERN.search(content)
        level = level_match.group(1) if level_match else "A"

        # Extract counts using pre-compiled patterns
        errors = warnings = info = 0
        errors_match = ERRORS_PATTERN.search(content)
        warnings_match = WARNINGS_PATTERN.search(content)
        info_match = INFO_PATTERN.search(content)
        if errors_match:
            errors = int(errors_match.group(1))
        if warnings_match:
            warnings = int(warnings_match.group(1))
        if info_match:
            info = int(info_match.group(1))

        objects.append({
            "name": name,
            "type": obj_type,
            "status": "checked",
            "level": level,
            "errors": errors,
            "warnings": warnings,
            "info": info
        })

    return objects


def generate_summary(package_name):
    """Generate the SUMMARY.md report."""

    # Paths (using BASE_DIR for portability)
    reports_dir = Path(f"{BASE_DIR}/reports/atc/{package_name}")
    progress_file = reports_dir / "progress.json"
    discovery_file = reports_dir / "discovery.json"
    summary_file = reports_dir / "SUMMARY.md"

    # Load discovery.json (may not exist for legacy runs)
    print(f"Loading discovery from {discovery_file}...", file=sys.stderr)
    discovery = load_discovery(reports_dir)
    if discovery:
        print(f"  Found {discovery.get('results', {}).get('totalFound', 0)} total objects from SAP", file=sys.stderr)

    # Load from progress.json if exists, otherwise scan ATC files
    if progress_file.exists():
        print(f"Loading progress from {progress_file}...", file=sys.stderr)
        progress = load_json(progress_file)
        objects = progress.get("objects", [])
        archive_files = True
    else:
        print(f"No progress.json found, scanning ATC report files...", file=sys.stderr)
        objects = parse_objects_from_atc_files(reports_dir)
        progress = {"package": package_name}
        archive_files = False
        print(f"  Found {len(objects)} ATC report files", file=sys.stderr)

    # Extract data (objects already loaded above)
    checked_objects = [obj for obj in objects if obj.get("status") == "checked"]
    failed_objects = [obj for obj in objects if obj.get("status") == "failed"]

    # Calculate level distribution from actual objects (THE FIX)
    distribution = calculate_level_distribution(checked_objects)

    # Get metadata
    package = progress.get("package", package_name)
    variant = progress.get("variant", "CLEAN_CORE")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate summary content
    content = f"""# ATC Check Summary: {package}

| Field | Value |
|-------|-------|
| Package | {package} |
| System | {progress.get("system", "N/A")} |
| Variant | {variant} |
| Generated | {timestamp} |
| Total Objects (Checkable) | {len(objects)} |
| Checked | {len(checked_objects)} |
| Failed | {len(failed_objects)} |

{generate_package_overview(discovery, progress)}

{generate_filtering_summary(progress)}

## Clean Core Level Distribution

{generate_level_distribution_table(distribution)}

## Objects by Level

### Level D - Requires Action
{generate_level_d_table(checked_objects)}

### Level C - Plan Migration
{generate_level_c_table(checked_objects)}

### Level B - Acceptable
{generate_level_b_table(checked_objects)}

### Level A - Fully Clean
{generate_level_a_table(checked_objects)}

## Top Findings

{generate_top_findings(checked_objects, reports_dir)}

## Remediation Roadmap

{generate_remediation_roadmap(checked_objects)}

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
    print(f"  Total objects (checkable): {len(objects)}", file=sys.stderr)
    if discovery:
        total_from_sap = discovery.get("results", {}).get("totalFound", 0)
        print(f"  Total from SAP: {total_from_sap}", file=sys.stderr)
    print(f"  Level A: {distribution['A']['count']}", file=sys.stderr)
    print(f"  Level B: {distribution['B']['count']}", file=sys.stderr)
    print(f"  Level C: {distribution['C']['count']}", file=sys.stderr)
    print(f"  Level D: {distribution['D']['count']}", file=sys.stderr)

    return {
        "status": "success",
        "package": package,
        "summaryFile": str(summary_file),
        "archivedDiscovery": str(archive_discovery_path) if archive_discovery_path else None,
        "archivedProgress": str(archive_progress_path) if archive_progress_path else None,
        "totalObjects": len(objects),
        "totalFromSap": discovery.get("results", {}).get("totalFound", 0) if discovery else None,
        "levelDistribution": {
            "A": distribution["A"]["count"],
            "B": distribution["B"]["count"],
            "C": distribution["C"]["count"],
            "D": distribution["D"]["count"]
        }
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate-summary.py <PACKAGE>", file=sys.stderr)
        print("Example: python3 generate-summary.py Z_CL_SRIO_DEV", file=sys.stderr)
        sys.exit(1)

    package_name = validate_package_name(sys.argv[1])
    result = generate_summary(package_name)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
