#!/usr/bin/env python3
"""
Business Function Mapper - Object Processor

Processes ATC reports and maps referenced APIs to business functions.
This is the standard processing script - DO NOT create custom scripts.

Usage:
    python3 process-objects.py <PACKAGE>

Example:
    python3 process-objects.py Z_CL_SRIO_DEV
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

# Pre-compiled regex patterns for API extraction (compiled once at module load)
PACKAGE_NAME_PATTERN = re.compile(r'^[A-Z][A-Z0-9_]{0,29}$')

API_PATTERNS = [
    # Classes (CL_*, CX_*, IF_*)
    re.compile(r'\b(CL_[A-Z][A-Z0-9_]+)\b', re.IGNORECASE),
    re.compile(r'\b(CX_[A-Z][A-Z0-9_]+)\b', re.IGNORECASE),
    re.compile(r'\b(IF_[A-Z][A-Z0-9_]+)\b', re.IGNORECASE),
    # Tables from SELECT statements
    re.compile(r'(?:FROM|INTO|TABLE)\s+([A-Z][A-Z0-9_]{2,30})\b', re.IGNORECASE),
    # Function modules
    re.compile(r"CALL\s+FUNCTION\s+'([A-Z][A-Z0-9_]+)'", re.IGNORECASE),
    # BAPIs
    re.compile(r'\b(BAPI_[A-Z0-9_]+)\b', re.IGNORECASE),
    # CDS views
    re.compile(r'\b(I_[A-Z][A-Z0-9_]+)\b', re.IGNORECASE),
    re.compile(r'\b(C_[A-Z][A-Z0-9_]+)\b', re.IGNORECASE),
    # Explicit "Usage of internal API" messages
    re.compile(r'Usage of internal API:\s*([A-Z][A-Z0-9_]+)', re.IGNORECASE),
    # Reading from DDIC tables
    re.compile(r'Reading from DDIC.*?:\s*([A-Z][A-Z0-9_]+)', re.IGNORECASE),
]

# Common false positives to filter out
FALSE_POSITIVES = frozenset({'FROM', 'INTO', 'TABLE', 'SELECT', 'WHERE', 'AND', 'OR', 'NOT'})


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


def load_json(path):
    """Load JSON file with error handling, return empty dict if not found or invalid."""
    try:
        if not path.exists():
            print(f"WARNING: File not found: {path}", file=sys.stderr)
            return {}
        with open(path, encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                print(f"WARNING: Empty file: {path}", file=sys.stderr)
                return {}
            return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {path}: {e}", file=sys.stderr)
        return {}
    except UnicodeDecodeError as e:
        print(f"ERROR: Encoding error in {path}: {e}", file=sys.stderr)
        return {}


def save_json(path, data):
    """Save JSON file atomically with pretty formatting.

    Uses temp file + atomic rename to prevent corruption on crash.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write to temp file in same directory (same filesystem for atomic rename)
    fd, temp_path = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        os.replace(temp_path, path)  # Atomic rename
    except Exception:
        # Clean up temp file on failure
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def extract_apis_from_atc(content):
    """Extract API references from ATC report content.

    Uses pre-compiled regex patterns for performance.
    """
    found_apis = set()

    # Use pre-compiled patterns (defined at module level)
    for pattern in API_PATTERNS:
        matches = pattern.findall(content)
        found_apis.update(m.upper() for m in matches)

    # Filter out common false positives (using pre-defined frozenset)
    found_apis -= FALSE_POSITIVES

    return found_apis


def lookup_api(api_name, sap_apis, custom_mappings):
    """Look up API in custom mappings first, then SAP reference."""

    # Priority 1: Custom mappings
    if api_name in custom_mappings:
        mapping = custom_mappings[api_name]
        return {
            "name": api_name,
            "businessFunction": mapping.get("businessFunction", "Custom"),
            "applicationComponent": mapping.get("applicationComponent", ""),
            "state": mapping.get("state", "custom"),
            "successor": None,
            "source": "custom"
        }

    # Priority 2: SAP reference data
    if api_name in sap_apis:
        api_info = sap_apis[api_name]
        successors = api_info.get("successors", [])
        return {
            "name": api_name,
            "businessFunction": api_info.get("businessFunction", "Unknown"),
            "applicationComponent": api_info.get("applicationComponent", ""),
            "state": api_info.get("state", "unknown"),
            "successor": successors[0].get("name") if successors else None,
            "source": "sap"
        }

    # Priority 3: Uncategorized
    return {
        "name": api_name,
        "businessFunction": "Uncategorized",
        "applicationComponent": "",
        "state": "unknown",
        "successor": None,
        "source": "none"
    }


def process_package(package_name):
    """Process all objects in a package."""

    # Paths (using BASE_DIR for portability)
    progress_file = Path(f"{BASE_DIR}/reports/executive/{package_name}/progress.json")
    atc_dir = Path(f"{BASE_DIR}/reports/atc/{package_name}")
    api_ref_file = Path(f"{BASE_DIR}/input/sap-api-reference/api-parsed.json")
    custom_mappings_file = Path(f"{BASE_DIR}/input/sap-api-reference/custom-mappings.json")

    # Check prerequisites
    if not atc_dir.exists():
        print(f"ERROR: ATC reports not found at {atc_dir}", file=sys.stderr)
        print("Run sap-atc-checker first.", file=sys.stderr)
        return {"status": "error", "message": "ATC reports not found"}

    if not progress_file.exists():
        print(f"ERROR: Progress file not found at {progress_file}", file=sys.stderr)
        print("Initialize progress.json first.", file=sys.stderr)
        return {"status": "error", "message": "Progress file not found"}

    # Load data
    print(f"Loading progress from {progress_file}...", file=sys.stderr)
    progress = load_json(progress_file)

    print(f"Loading SAP API reference ({api_ref_file})...", file=sys.stderr)
    api_data = load_json(api_ref_file)
    sap_apis = api_data.get("apis", {})
    print(f"  Loaded {len(sap_apis):,} APIs", file=sys.stderr)

    print(f"Loading custom mappings ({custom_mappings_file})...", file=sys.stderr)
    custom_data = load_json(custom_mappings_file)
    custom_mappings = custom_data.get("customMappings", {})
    print(f"  Loaded {len(custom_mappings)} custom mappings", file=sys.stderr)

    # Initialize tracking structures if not present
    if "businessFunctions" not in progress:
        progress["businessFunctions"] = {}
    if "deprecatedApis" not in progress:
        progress["deprecatedApis"] = []
    if "uncategorizedApis" not in progress:
        progress["uncategorizedApis"] = []

    # Build lookup dicts for O(1) access instead of O(n) list scans
    deprecated_by_name = {d["name"]: d for d in progress["deprecatedApis"]}
    uncategorized_by_name = {u["name"]: u for u in progress["uncategorizedApis"]}

    # Process each pending object
    pending_objects = [obj for obj in progress.get("objects", []) if obj.get("status") == "pending"]
    total = len(progress.get("objects", []))

    print(f"\nProcessing {len(pending_objects)} pending objects...", file=sys.stderr)

    for obj in pending_objects:
        name = obj["name"]
        level = obj.get("level", "C")

        # Read ATC report
        atc_file = atc_dir / f"{name}_atc.md"
        if not atc_file.exists():
            # No ATC file - add to Uncategorized if it has findings (Level C/D)
            if level in ["C", "D"]:
                bf = "Uncategorized"
                if bf not in progress["businessFunctions"]:
                    progress["businessFunctions"][bf] = {
                        "objects": [],
                        "findings": 0,
                        "deprecatedApis": []
                    }
                if name not in progress["businessFunctions"][bf]["objects"]:
                    progress["businessFunctions"][bf]["objects"].append(name)
                progress["businessFunctions"][bf]["findings"] += 1
            print(f"  [{progress['processed']+1}/{total}] {name}: No ATC file (added to Uncategorized)", file=sys.stderr)
            obj["status"] = "processed"
            obj["referencedApis"] = []
            progress["processed"] += 1
            continue

        content = atc_file.read_text(encoding='utf-8')

        # Extract API references
        found_apis = extract_apis_from_atc(content)

        # Lookup each API
        referenced_apis = []
        for api_name in found_apis:
            api_info = lookup_api(api_name, sap_apis, custom_mappings)

            # Skip if it's a Z/Y custom object (shouldn't be in findings)
            if api_name.startswith(('Z', 'Y')) and api_info["source"] == "none":
                continue

            referenced_apis.append(api_info)

            bf = api_info["businessFunction"]
            state = api_info["state"]

            # Aggregate by business function
            if bf not in progress["businessFunctions"]:
                progress["businessFunctions"][bf] = {
                    "objects": [],
                    "findings": 0,
                    "deprecatedApis": []
                }

            if name not in progress["businessFunctions"][bf]["objects"]:
                progress["businessFunctions"][bf]["objects"].append(name)

            progress["businessFunctions"][bf]["findings"] += 1

            # Track deprecated/classic APIs
            if state in ["deprecated", "classicAPI", "noAPI", "notToBeReleased"]:
                if api_name not in progress["businessFunctions"][bf]["deprecatedApis"]:
                    progress["businessFunctions"][bf]["deprecatedApis"].append(api_name)

                # Add to global deprecated list (O(1) dict lookup instead of O(n) list scan)
                existing = deprecated_by_name.get(api_name)
                if existing:
                    if name not in existing["usedBy"]:
                        existing["usedBy"].append(name)
                else:
                    new_entry = {
                        "name": api_name,
                        "type": sap_apis.get(api_name, {}).get("type", ""),
                        "applicationComponent": api_info["applicationComponent"],
                        "businessFunction": bf,
                        "successor": api_info["successor"],
                        "usedBy": [name]
                    }
                    progress["deprecatedApis"].append(new_entry)
                    deprecated_by_name[api_name] = new_entry  # Keep dict in sync

            # Track uncategorized APIs (O(1) dict lookup instead of O(n) list scan)
            if bf == "Uncategorized":
                existing = uncategorized_by_name.get(api_name)
                if existing:
                    if name not in existing["usedBy"]:
                        existing["usedBy"].append(name)
                else:
                    new_entry = {
                        "name": api_name,
                        "usedBy": [name]
                    }
                    progress["uncategorizedApis"].append(new_entry)
                    uncategorized_by_name[api_name] = new_entry  # Keep dict in sync

        # Update object status
        obj["status"] = "processed"
        obj["referencedApis"] = referenced_apis
        progress["processed"] += 1

        api_count = len(referenced_apis)
        uncategorized_count = sum(1 for a in referenced_apis if a["businessFunction"] == "Uncategorized")

        # If object has findings (Level C/D) but no APIs extracted, add to Uncategorized
        # This ensures all objects with findings appear in the business area table
        if api_count == 0 and level in ["C", "D"]:
            bf = "Uncategorized"
            if bf not in progress["businessFunctions"]:
                progress["businessFunctions"][bf] = {
                    "objects": [],
                    "findings": 0,
                    "deprecatedApis": []
                }
            if name not in progress["businessFunctions"][bf]["objects"]:
                progress["businessFunctions"][bf]["objects"].append(name)
            # Count 1 finding per object (we know it has findings but can't parse details)
            progress["businessFunctions"][bf]["findings"] += 1

        status_msg = f"[{progress['processed']}/{total}] {name}: {api_count} APIs"
        if uncategorized_count > 0:
            status_msg += f" ({uncategorized_count} uncategorized)"
        elif api_count == 0 and level in ["C", "D"]:
            status_msg += " (added to Uncategorized - no APIs parsed)"
        print(status_msg, file=sys.stderr)

    # Update timestamp
    progress["lastUpdated"] = datetime.utcnow().isoformat() + "Z"

    # Save progress
    save_json(progress_file, progress)

    # Summary
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"Processing complete!", file=sys.stderr)
    print(f"  Objects processed: {progress['processed']}/{total}", file=sys.stderr)
    print(f"  Business functions: {len(progress['businessFunctions'])}", file=sys.stderr)
    print(f"  Deprecated APIs: {len(progress['deprecatedApis'])}", file=sys.stderr)
    print(f"  Uncategorized APIs: {len(progress['uncategorizedApis'])}", file=sys.stderr)

    # Return summary as JSON for agent
    return {
        "status": "success",
        "processed": progress["processed"],
        "total": total,
        "businessFunctions": len(progress["businessFunctions"]),
        "deprecatedApis": len(progress["deprecatedApis"]),
        "uncategorizedApis": len(progress["uncategorizedApis"]),
        "progressFile": str(progress_file)
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 process-objects.py <PACKAGE>", file=sys.stderr)
        print("Example: python3 process-objects.py Z_CL_SRIO_DEV", file=sys.stderr)
        sys.exit(1)

    package_name = validate_package_name(sys.argv[1])
    result = process_package(package_name)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
