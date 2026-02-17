#!/usr/bin/env python3
"""
SAP API Reference Parser for Business Function Mapper
Parses SAP API reference JSON files and outputs a combined lookup structure.

Usage:
    python parse-api-refs.py <input_dir> <output_json>

Input files (from https://github.com/SAP/abap-atc-cr-cv-s4hc):
    - objectReleaseInfoLatest.json
    - objectClassifications_SAP.json

Output JSON structure:
{
    "metadata": { "source": "...", "parsedAt": "..." },
    "apis": {
        "API_NAME": {
            "type": "CLAS|TABL|FUNC|...",
            "applicationComponent": "FI-GL-GL",
            "businessFunction": "Finance (FI)",
            "state": "deprecated|classicAPI|noAPI",
            "successors": [{"name": "...", "type": "..."}]
        }
    },
    "componentToFunction": { "FI": "Finance", ... },
    "stats": { "totalApis": N, "deprecated": N, "withSuccessors": N }
}
"""

import sys
import os
import json
import tempfile
from pathlib import Path
from datetime import datetime


# SAP Application Component prefix to Business Function mapping
COMPONENT_TO_FUNCTION = {
    "FI": "Finance",
    "CO": "Controlling",
    "SD": "Sales & Distribution",
    "MM": "Materials Management",
    "PP": "Production Planning",
    "PM": "Plant Maintenance",
    "QM": "Quality Management",
    "PS": "Project Systems",
    "HR": "Human Capital Management",
    "HCM": "Human Capital Management",
    "PA": "Personnel Administration",
    "BC": "Basis Components",
    "CA": "Cross-Application",
    "EP": "Enterprise Portal",
    "SRM": "Supplier Relationship Management",
    "CRM": "Customer Relationship Management",
    "SCM": "Supply Chain Management",
    "BW": "Business Warehouse",
    "BI": "Business Intelligence",
    "GRC": "Governance Risk Compliance",
    "PLM": "Product Lifecycle Management",
    "EWM": "Extended Warehouse Management",
    "TM": "Transportation Management",
    "RE": "Real Estate",
    "TR": "Treasury",
    "IM": "Investment Management",
    "EC": "Enterprise Controlling",
    "IS": "Industry Solutions",
    "LO": "Logistics General",
    "LE": "Logistics Execution",
    "CS": "Customer Service",
    "SM": "Service Management",
    "WF": "Workflow",
    "BPM": "Business Process Management",
}


def get_business_function(app_component):
    """Extract business function from application component."""
    if not app_component:
        return "Unknown"

    # Get the first part before the dash (e.g., "FI-GL-GL" -> "FI")
    prefix = app_component.split("-")[0].upper()

    return COMPONENT_TO_FUNCTION.get(prefix, f"Other ({prefix})")


def parse_release_info(file_path):
    """Parse objectReleaseInfoLatest.json for deprecated APIs with successors."""
    if not file_path.exists():
        print(f"  Warning: {file_path} not found", file=sys.stderr)
        return {}

    try:
        content = file_path.read_text(encoding='utf-8')
        if not content.strip():
            print(f"  Warning: {file_path} is empty", file=sys.stderr)
            return {}
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"  ERROR: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        return {}
    except UnicodeDecodeError as e:
        print(f"  ERROR: Encoding error in {file_path}: {e}", file=sys.stderr)
        return {}

    apis = {}

    # Handle various JSON formats
    if isinstance(data, list):
        items = data
    elif 'objectReleaseInfo' in data:
        items = data['objectReleaseInfo']
    elif 'objects' in data:
        items = data['objects']
    elif 'items' in data:
        items = data['items']
    else:
        items = []

    for item in items:
        name = item.get('tadirObjName') or item.get('objectKey')
        if not name:
            continue

        obj_type = item.get('tadirObject') or item.get('objectType')
        app_component = item.get('applicationComponent', '')
        state = item.get('state', '')

        # Parse successors
        successors = []
        if 'successors' in item and item['successors']:
            for succ in item['successors']:
                succ_name = succ.get('tadirObjName') or succ.get('objectKey') or succ.get('name')
                succ_type = succ.get('tadirObject') or succ.get('objectType') or succ.get('type')
                if succ_name:
                    successors.append({
                        "name": succ_name,
                        "type": succ_type
                    })

        apis[name] = {
            "type": obj_type,
            "applicationComponent": app_component,
            "businessFunction": get_business_function(app_component),
            "state": state,
            "successorClassification": item.get('successorClassification', ''),
            "successors": successors,
            "softwareComponent": item.get('softwareComponent', '')
        }

    return apis


def parse_classifications(file_path):
    """Parse objectClassifications_SAP.json for additional API metadata."""
    if not file_path.exists():
        print(f"  Warning: {file_path} not found", file=sys.stderr)
        return {}

    try:
        content = file_path.read_text(encoding='utf-8')
        if not content.strip():
            print(f"  Warning: {file_path} is empty", file=sys.stderr)
            return {}
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"  ERROR: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        return {}
    except UnicodeDecodeError as e:
        print(f"  ERROR: Encoding error in {file_path}: {e}", file=sys.stderr)
        return {}

    apis = {}

    # Handle format with objectClassifications array
    items = data.get('objectClassifications', data if isinstance(data, list) else [])

    for item in items:
        name = item.get('tadirObjName') or item.get('objectKey')
        if not name:
            continue

        obj_type = item.get('tadirObject') or item.get('objectType')
        app_component = item.get('applicationComponent', '')
        state = item.get('state', '')

        apis[name] = {
            "type": obj_type,
            "applicationComponent": app_component,
            "businessFunction": get_business_function(app_component),
            "state": state,
            "softwareComponent": item.get('softwareComponent', ''),
            "successors": []
        }

    return apis


def main():
    if len(sys.argv) < 3:
        print("Usage: python parse-api-refs.py <input_dir> <output_json>", file=sys.stderr)
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_dir.exists():
        print(f"ERROR: Input directory {input_dir} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Parsing SAP API reference data from {input_dir}...", file=sys.stderr)

    # Parse release info (has successor information)
    release_file = input_dir / 'objectReleaseInfoLatest.json'
    print(f"  Parsing {release_file.name}...", file=sys.stderr)
    release_apis = parse_release_info(release_file)
    print(f"    Found {len(release_apis)} APIs with release info", file=sys.stderr)

    # Parse classifications (additional metadata)
    class_file = input_dir / 'objectClassifications_SAP.json'
    print(f"  Parsing {class_file.name}...", file=sys.stderr)
    class_apis = parse_classifications(class_file)
    print(f"    Found {len(class_apis)} APIs with classifications", file=sys.stderr)

    # Merge: release info takes precedence (has successors)
    all_apis = {}
    all_apis.update(class_apis)
    all_apis.update(release_apis)  # Overwrites with richer data

    # Calculate statistics
    deprecated_count = sum(1 for api in all_apis.values() if api.get('state') == 'deprecated')
    with_successors = sum(1 for api in all_apis.values() if api.get('successors'))

    # Build output
    output = {
        "metadata": {
            "source": "github.com/SAP/abap-atc-cr-cv-s4hc",
            "parsedAt": datetime.now().isoformat(),
            "releaseInfoFile": release_file.name if release_file.exists() else None,
            "classificationsFile": class_file.name if class_file.exists() else None
        },
        "apis": all_apis,
        "componentToFunction": COMPONENT_TO_FUNCTION,
        "stats": {
            "totalApis": len(all_apis),
            "deprecated": deprecated_count,
            "withSuccessors": with_successors,
            "classicApi": sum(1 for api in all_apis.values() if api.get('state') == 'classicAPI'),
            "noApi": sum(1 for api in all_apis.values() if api.get('state') == 'noAPI')
        }
    }

    # Write output atomically
    output_file.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(output, indent=2)
    fd, temp_path = tempfile.mkstemp(dir=output_file.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        os.replace(temp_path, output_file)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise

    print(f"\nOutput written to {output_file}", file=sys.stderr)
    print(f"  Total APIs: {len(all_apis)}", file=sys.stderr)
    print(f"  Deprecated: {deprecated_count}", file=sys.stderr)
    print(f"  With successors: {with_successors}", file=sys.stderr)

    # Output JSON for caller
    print(json.dumps({
        "status": "success",
        "totalApis": len(all_apis),
        "deprecated": deprecated_count,
        "withSuccessors": with_successors,
        "outputFile": str(output_file)
    }))


if __name__ == "__main__":
    main()
