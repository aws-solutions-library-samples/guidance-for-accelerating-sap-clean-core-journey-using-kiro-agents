#!/usr/bin/env python3
"""
Business Function Mapper - Progress Initializer

Parses ATC SUMMARY.md and creates progress.json with all Level C/D objects.
This is the standard initialization script - DO NOT create custom scripts.

Usage:
    python3 init-progress.py <PACKAGE>

Example:
    python3 init-progress.py Z_CL_SRIO_DEV
"""

import json
import os
import re
import sys
import tempfile
from pathlib import Path
from datetime import datetime

# CC_DIR: Clean Core root directory
# Auto-derive from script location if not set (script is in agents/business-function-mapper/)
CC_DIR = os.environ.get("CC_DIR") or str(Path(__file__).resolve().parent.parent.parent)
BASE_DIR = CC_DIR  # Alias for compatibility

# Pre-compiled regex patterns (compiled once at module load)
PACKAGE_NAME_PATTERN = re.compile(r'^[A-Z][A-Z0-9_]{0,29}$')
TABLE_ROW_PATTERN = re.compile(r"\|\s*([A-Z][A-Z0-9_]+)\s*\|\s*(\w+)\s*\|")
TYPE_PATTERN = re.compile(r"\|\s*Type\s*\|\s*(\w+)\s*\|")
LEVEL_PATTERN = re.compile(r"\*\*Clean Core Level\*\*:\s*([ABCD])")
LEVEL_DIST_PATTERN = re.compile(r"Clean Core Level Distribution.*?\n(.*?)(?=\n##|\n---|\Z)", re.DOTALL | re.IGNORECASE)
LEVEL_ROW_PATTERN = re.compile(r"\|\s*([A-D])(?:\s*\([^)]*\))?\s*\|\s*(\d+)\s*\|\s*([\d.]+%?)\s*\|")
SYSTEM_PATTERN = re.compile(r"\|\s*System\s*\|\s*([^|]+)\s*\|")
VARIANT_PATTERN = re.compile(r"\|\s*Variant\s*\|\s*([^|]+)\s*\|")
TOTAL_PATTERN = re.compile(r"\|\s*Total(?:\s+Objects)?\s*\|\s*(\d+)\s*\|")


def validate_package_name(name):
    """Validate SAP package name format to prevent path traversal.

    SAP package names must:
    - Start with a letter (A-Z)
    - Contain only uppercase letters, digits, and underscores
    - Be 1-30 characters long
    """
    if not name:
        print("ERROR: Package name is required", file=sys.stderr)
        sys.exit(1)
    if not PACKAGE_NAME_PATTERN.match(name):
        print(f"ERROR: Invalid package name: {name}", file=sys.stderr)
        print("Package name must start with A-Z and contain only A-Z, 0-9, _ (max 30 chars)", file=sys.stderr)
        sys.exit(1)
    return name


def parse_summary_table(content, section_header):
    """Extract objects from a markdown table section.

    Uses pre-compiled regex patterns for performance.
    """
    objects = []

    # Find the section (this pattern is dynamic so compile it once per call)
    pattern = re.compile(rf"###\s*{re.escape(section_header)}.*?\n(.*?)(?=\n###|\n---|\Z)", re.DOTALL | re.IGNORECASE)
    match = pattern.search(content)

    if not match:
        return objects

    section_content = match.group(1)

    # Parse table rows using pre-compiled pattern
    for row_match in TABLE_ROW_PATTERN.finditer(section_content):
        name = row_match.group(1).strip()
        obj_type = row_match.group(2).strip()
        if name and not name.startswith("Object") and not name.startswith("-"):
            objects.append({"name": name, "type": obj_type})

    return objects


def parse_objects_from_atc_files(atc_dir):
    """Parse object info directly from individual ATC report files.

    This is more reliable than parsing SUMMARY.md tables which may have missing rows.
    Uses pre-compiled regex patterns for performance.
    """
    objects_by_level = {"A": [], "B": [], "C": [], "D": []}

    for atc_file in atc_dir.glob("*_atc.md"):
        content = atc_file.read_text(encoding='utf-8')

        # Extract object name from filename (remove _atc.md suffix)
        name = atc_file.stem.replace("_atc", "")

        # Extract type from header table using pre-compiled pattern
        type_match = TYPE_PATTERN.search(content)
        obj_type = type_match.group(1) if type_match else "UNKNOWN"

        # Extract level using pre-compiled pattern
        level_match = LEVEL_PATTERN.search(content)
        level = level_match.group(1) if level_match else "A"

        objects_by_level[level].append({"name": name, "type": obj_type, "level": level})

    return objects_by_level


def parse_level_distribution(content):
    """Extract Clean Core Level Distribution from SUMMARY.md.

    Uses pre-compiled regex patterns for performance.
    """
    distribution = {}

    # Find the distribution table using pre-compiled pattern
    match = LEVEL_DIST_PATTERN.search(content)

    if not match:
        return distribution

    table_content = match.group(1)

    # Parse rows using pre-compiled pattern
    for row_match in LEVEL_ROW_PATTERN.finditer(table_content):
        level = row_match.group(1)
        count = int(row_match.group(2))
        percentage = row_match.group(3)
        distribution[level] = {"count": count, "percentage": percentage}

    return distribution


def parse_metadata(content):
    """Extract metadata from SUMMARY.md.

    Uses pre-compiled regex patterns for performance.
    """
    metadata = {
        "sourceSystem": "",
        "variant": "",
        "totalObjects": 0
    }

    # Source system using pre-compiled pattern
    system_match = SYSTEM_PATTERN.search(content)
    if system_match:
        metadata["sourceSystem"] = system_match.group(1).strip()

    # Variant using pre-compiled pattern
    variant_match = VARIANT_PATTERN.search(content)
    if variant_match:
        metadata["variant"] = variant_match.group(1).strip()

    # Total objects using pre-compiled pattern
    total_match = TOTAL_PATTERN.search(content)
    if total_match:
        metadata["totalObjects"] = int(total_match.group(1))

    return metadata


def init_progress(package_name):
    """Initialize progress.json from ATC SUMMARY.md."""

    # Paths (using BASE_DIR for portability)
    atc_dir = Path(f"{BASE_DIR}/reports/atc/{package_name}")
    summary_file = atc_dir / "SUMMARY.md"
    output_dir = Path(f"{BASE_DIR}/reports/executive/{package_name}")
    progress_file = output_dir / "progress.json"

    # Check if ATC reports exist
    if not summary_file.exists():
        print(f"ERROR: SUMMARY.md not found at {summary_file}", file=sys.stderr)
        print("Run sap-atc-checker first.", file=sys.stderr)
        return {"status": "error", "message": "SUMMARY.md not found"}

    # Check if progress already exists
    if progress_file.exists():
        print(f"WARNING: progress.json already exists at {progress_file}", file=sys.stderr)
        print("Reading existing progress...", file=sys.stderr)
        try:
            with open(progress_file, encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    print(f"WARNING: progress.json is empty, will reinitialize", file=sys.stderr)
                else:
                    existing = json.loads(content)
                    return {
                        "status": "exists",
                        "processed": existing.get("processed", 0),
                        "total": len(existing.get("objects", [])),
                        "progressFile": str(progress_file)
                    }
        except json.JSONDecodeError as e:
            print(f"WARNING: Invalid JSON in progress.json ({e}), will reinitialize", file=sys.stderr)
        except UnicodeDecodeError as e:
            print(f"WARNING: Encoding error in progress.json ({e}), will reinitialize", file=sys.stderr)

    # Read SUMMARY.md for metadata
    print(f"Reading {summary_file}...", file=sys.stderr)
    content = summary_file.read_text(encoding='utf-8')

    # Parse metadata from SUMMARY.md
    metadata = parse_metadata(content)
    level_distribution = parse_level_distribution(content)

    # Parse objects directly from ATC report files (more reliable than SUMMARY.md tables)
    print(f"Scanning ATC report files in {atc_dir}...", file=sys.stderr)
    objects_by_level = parse_objects_from_atc_files(atc_dir)

    level_d_objects = objects_by_level["D"]
    level_c_objects = objects_by_level["C"]

    # Set status to pending for processing
    for obj in level_d_objects + level_c_objects:
        obj["status"] = "pending"

    # Combine Level C and D objects (objects with findings)
    all_objects = level_d_objects + level_c_objects

    # Verify counts match Level Distribution (warn if mismatch)
    expected_c = level_distribution.get("C", {}).get("count", 0)
    expected_d = level_distribution.get("D", {}).get("count", 0)
    if len(level_c_objects) != expected_c:
        print(f"  WARNING: Found {len(level_c_objects)} Level C objects, expected {expected_c}", file=sys.stderr)
    if len(level_d_objects) != expected_d:
        print(f"  WARNING: Found {len(level_d_objects)} Level D objects, expected {expected_d}", file=sys.stderr)

    # Build progress structure
    progress = {
        "package": package_name,
        "started": datetime.utcnow().isoformat() + "Z",
        "lastUpdated": datetime.utcnow().isoformat() + "Z",
        "atcReportSource": str(atc_dir),
        "apiReferenceLoaded": False,
        "sourceSystem": metadata["sourceSystem"],
        "variant": metadata["variant"],
        "totalObjects": metadata["totalObjects"],
        "objectsWithFindings": len(all_objects),
        "levelDistribution": level_distribution,
        "processed": 0,
        "businessFunctions": {},
        "deprecatedApis": [],
        "uncategorizedApis": [],
        "objects": all_objects
    }

    # Create output directory and save atomically
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write to temp file + atomic rename to prevent corruption
    fd, temp_path = tempfile.mkstemp(dir=output_dir, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2)
        os.replace(temp_path, progress_file)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise

    # Summary
    print(f"\nProgress initialized: {progress_file}", file=sys.stderr)
    print(f"  Package: {package_name}", file=sys.stderr)
    print(f"  Total objects: {metadata['totalObjects']}", file=sys.stderr)
    print(f"  Level D objects: {len(level_d_objects)}", file=sys.stderr)
    print(f"  Level C objects: {len(level_c_objects)}", file=sys.stderr)
    print(f"  Objects to process: {len(all_objects)}", file=sys.stderr)

    return {
        "status": "success",
        "package": package_name,
        "totalObjects": metadata["totalObjects"],
        "levelD": len(level_d_objects),
        "levelC": len(level_c_objects),
        "objectsToProcess": len(all_objects),
        "progressFile": str(progress_file)
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 init-progress.py <PACKAGE>", file=sys.stderr)
        print("Example: python3 init-progress.py Z_CL_SRIO_DEV", file=sys.stderr)
        sys.exit(1)

    package_name = validate_package_name(sys.argv[1])
    result = init_progress(package_name)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
