#!/usr/bin/env python3
"""
SUSG XML Parser for Unused Code Discovery
Parses SAP SUSG runtime data and outputs a compact JSON for agent consumption.

Usage:
    python parse-susg.py input/ input/susg-parsed.json

Output JSON structure:
{
    "metadata": { "sysId": "A4H", "dateFrom": "2025-10-23", "dateTo": "2025-10-28", "daysAvailable": 6 },
    "objects": {
        "ZCL_EXAMPLE": { "progId": 123, "type": "CLAS", "executions": 1500, "lastUsed": "2025-10-28", "callers": [...], "called": [...] }
    },
    "customObjectNames": ["ZCL_EXAMPLE", ...]
}
"""

import sys
import os
import json
import re
import tempfile
# nosemgrep: use-defused-xml - SUSG files are user-exported from SAP, not untrusted input
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict


# Pre-compiled regex pattern for package name validation
PACKAGE_NAME_PATTERN = re.compile(r'^[A-Z][A-Z0-9_]{0,29}$')


def get_element_text(elem, tag_name):
    """Safely extract text from a child element.

    Returns stripped text or None if element doesn't exist or has no text.
    """
    child = elem.find(tag_name)
    if child is not None and child.text:
        return child.text.strip()
    return None


def get_element_int(elem, tag_name, default=0):
    """Safely extract integer from a child element."""
    text = get_element_text(elem, tag_name)
    if text:
        try:
            return int(text)
        except ValueError:
            return default
    return default


def parse_xml_file(file_path, tag_name):
    """Parse XML file and yield elements matching tag_name.

    Uses ElementTree for robust XML parsing instead of fragile regex.
    Handles namespaces, CDATA, and edge cases that regex cannot.
    """
    if not file_path.exists():
        return

    try:
        # nosemgrep: use-defused-xml-parse
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Find all matching elements (handles nested structures)
        for elem in root.iter(tag_name):
            yield elem

    except ET.ParseError as e:
        print(f"WARNING: XML parse error in {file_path}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"WARNING: Error reading {file_path}: {e}", file=sys.stderr)


def parse_admin(input_dir):
    """Parse ADMIN0001.xml for metadata using ElementTree."""
    admin_file = input_dir / 'ADMIN0001.xml'

    default_meta = {"sysId": "UNKNOWN", "dateFrom": "", "dateTo": "", "daysAvailable": 0}

    for elem in parse_xml_file(admin_file, 'SUSG_API_S_ADMIN'):
        return {
            "sysId": get_element_text(elem, 'SYSID') or "UNKNOWN",
            "dateFrom": get_element_text(elem, 'DATE_FROM') or "",
            "dateTo": get_element_text(elem, 'DATE_TO') or "",
            "daysAvailable": get_element_int(elem, 'DAYS_AVAILABLE', 0)
        }

    return default_meta


def parse_prog(input_dir):
    """Parse PROG0001.xml for object catalog using ElementTree."""
    prog_file = input_dir / 'PROG0001.xml'
    if not prog_file.exists():
        print(f"ERROR: {prog_file} not found", file=sys.stderr)
        sys.exit(1)

    # Build maps: progId -> object info, objName -> progId
    prog_map = {}  # progId -> {name, type}
    name_to_prog = {}  # objName -> progId

    for elem in parse_xml_file(prog_file, 'SUSG_API_S_PROG'):
        prog_id = get_element_int(elem, 'PROGID', 0)
        obj_name = get_element_text(elem, 'OBJ_NAME')
        obj_type = get_element_text(elem, 'OBJ_TYPE')

        if prog_id and obj_name:
            prog_map[prog_id] = {"name": obj_name, "type": obj_type}
            name_to_prog[obj_name] = prog_id

    return prog_map, name_to_prog


def parse_sub(input_dir):
    """Parse SUB0001.xml for trigger mapping using ElementTree."""
    sub_file = input_dir / 'SUB0001.xml'
    if not sub_file.exists():
        return {}

    # Build map: subId -> progId
    sub_map = {}
    for elem in parse_xml_file(sub_file, 'SUSG_API_S_SUB'):
        sub_id = get_element_int(elem, 'SUBID', 0)
        prog_id = get_element_int(elem, 'PROGID', 0)
        if sub_id:
            # Use PROGID if available, otherwise SUBID often equals PROGID
            sub_map[sub_id] = prog_id if prog_id else sub_id

    return sub_map


def parse_data(input_dir, prog_map):
    """Parse DATA*.xml files for execution statistics using ElementTree."""
    execution_map = defaultdict(lambda: {"counter": 0, "lastUsed": None})

    for data_file in sorted(input_dir.glob('DATA*.xml')):
        for elem in parse_xml_file(data_file, 'SUSG_API_S_DATA'):
            sub_id = get_element_int(elem, 'SUBID', 0)
            counter = get_element_int(elem, 'COUNTER', 0)
            last_used = get_element_text(elem, 'LAST_USED')

            if sub_id and counter:
                prog_id = sub_id  # SUBID maps to PROGID
                if prog_id in prog_map:
                    execution_map[prog_id]["counter"] += counter
                    if last_used:
                        current = execution_map[prog_id]["lastUsed"]
                        if current is None or last_used > current:
                            execution_map[prog_id]["lastUsed"] = last_used

    return dict(execution_map)


def parse_rdata(input_dir, prog_map):
    """Parse RDATA*.xml files for call relationships using ElementTree."""
    callers = defaultdict(list)  # progId -> list of callers
    called = defaultdict(list)   # progId -> list of called

    for rdata_file in sorted(input_dir.glob('RDATA*.xml')):
        for elem in parse_xml_file(rdata_file, 'SUSG_API_S_RDATA'):
            sub_id1 = get_element_int(elem, 'SUBID1', 0)  # caller
            sub_id2 = get_element_int(elem, 'SUBID2', 0)  # called
            counter = get_element_int(elem, 'COUNTER', 0)
            last_used = get_element_text(elem, 'LAST_USED')

            if sub_id1 and sub_id2:
                caller_id = sub_id1
                called_id = sub_id2

                # Add caller info to called object
                if called_id in prog_map and caller_id in prog_map:
                    callers[called_id].append({
                        "name": prog_map[caller_id]["name"],
                        "type": prog_map[caller_id]["type"],
                        "count": counter,
                        "lastUsed": last_used
                    })
                    called[caller_id].append({
                        "name": prog_map[called_id]["name"],
                        "type": prog_map[called_id]["type"],
                        "count": counter
                    })

    return dict(callers), dict(called)


def is_custom_object(name):
    """Check if object is a custom Z* or Y* object."""
    return name.startswith('Z') or name.startswith('Y')


def save_json_atomic(path, data):
    """Save JSON file atomically using temp file + rename."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fd, temp_path = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        os.replace(temp_path, path)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def main():
    if len(sys.argv) < 3:
        print("Usage: python parse-susg.py <input_dir> <output_json>", file=sys.stderr)
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_dir.exists():
        print(f"ERROR: Input directory {input_dir} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Parsing SUSG data from {input_dir}...", file=sys.stderr)

    # Parse all files using ElementTree
    metadata = parse_admin(input_dir)
    print(f"  Metadata: {metadata['sysId']} ({metadata['dateFrom']} to {metadata['dateTo']})", file=sys.stderr)

    prog_map, name_to_prog = parse_prog(input_dir)
    print(f"  Programs: {len(prog_map)} objects", file=sys.stderr)

    execution_map = parse_data(input_dir, prog_map)
    print(f"  Executions: {len(execution_map)} objects with runtime data", file=sys.stderr)

    callers, called = parse_rdata(input_dir, prog_map)
    print(f"  Relationships: {len(callers)} objects have callers", file=sys.stderr)

    # Build output structure
    objects = {}
    custom_names = []

    for prog_id, info in prog_map.items():
        obj_name = info["name"]
        obj_type = info["type"]

        # Only include Z*/Y* custom objects
        if is_custom_object(obj_name):
            exec_info = execution_map.get(prog_id, {"counter": 0, "lastUsed": None})
            obj_callers = callers.get(prog_id, [])
            obj_called = called.get(prog_id, [])

            objects[obj_name] = {
                "progId": prog_id,
                "type": obj_type,
                "executions": exec_info["counter"],
                "lastUsed": exec_info["lastUsed"],
                "callerCount": len(obj_callers),
                "callers": obj_callers[:10],  # Limit to top 10 callers
                "calledCount": len(obj_called),
                "called": obj_called[:10]     # Limit to top 10 called
            }
            custom_names.append(obj_name)

    print(f"  Custom objects: {len(custom_names)} Z*/Y* objects found", file=sys.stderr)

    # Write output atomically
    output = {
        "metadata": metadata,
        "objects": objects,
        "customObjectNames": sorted(custom_names)
    }

    save_json_atomic(output_file, output)
    print(f"Output written to {output_file}", file=sys.stderr)
    print(json.dumps({"status": "success", "customObjects": len(custom_names), "outputFile": str(output_file)}))


if __name__ == "__main__":
    main()
