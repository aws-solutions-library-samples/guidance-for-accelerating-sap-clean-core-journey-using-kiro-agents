#!/usr/bin/env python3
"""
SAP API Reference Catalog Generator

Generates a human-readable CATALOG.md from api-parsed.json.

Usage:
    python3 generate-catalog.py [--output /path/to/CATALOG.md]

Default output: input/sap-api-reference/CATALOG.md
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# CC_DIR: Clean Core root directory
# Auto-derive from script location if not set (script is in agents/business-function-mapper/)
CC_DIR = os.environ.get("CC_DIR") or str(Path(__file__).resolve().parent.parent.parent)

# Default paths (relative to CC_DIR)
DEFAULT_API_FILE = Path(CC_DIR) / "input/sap-api-reference/api-parsed.json"
DEFAULT_CUSTOM_FILE = Path(CC_DIR) / "input/sap-api-reference/custom-mappings.json"
DEFAULT_OUTPUT = Path(CC_DIR) / "input/sap-api-reference/CATALOG.md"


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


def generate_catalog(api_file=DEFAULT_API_FILE, custom_file=DEFAULT_CUSTOM_FILE, output_file=DEFAULT_OUTPUT):
    """Generate CATALOG.md from API reference data."""

    # Load data
    print(f"Loading API data from {api_file}...", file=sys.stderr)
    data = load_json(api_file)
    apis = data.get("apis", {})
    stats = data.get("stats", {})

    print(f"Loading custom mappings from {custom_file}...", file=sys.stderr)
    custom_data = load_json(custom_file)
    custom_mappings = custom_data.get("customMappings", {})

    # Merge custom mappings (they override SAP data)
    for name, mapping in custom_mappings.items():
        apis[name] = {
            "type": mapping.get("type", "CUSTOM"),
            "applicationComponent": mapping.get("applicationComponent", ""),
            "businessFunction": mapping.get("businessFunction", "Custom"),
            "state": mapping.get("state", "custom"),
            "softwareComponent": mapping.get("softwareComponent", ""),
            "successors": []
        }

    # Aggregate by business function
    by_business_function = defaultdict(lambda: {
        "apis": [],
        "by_type": defaultdict(int),
        "by_state": defaultdict(int),
        "app_components": set()
    })

    # Aggregate by type
    by_type = defaultdict(int)

    # Aggregate by state
    by_state = defaultdict(int)

    for name, info in apis.items():
        bf = info.get("businessFunction", "Unknown")
        obj_type = info.get("type", "UNKNOWN")
        state = info.get("state", "unknown")
        app_comp = info.get("applicationComponent", "")

        by_business_function[bf]["apis"].append((name, info))
        by_business_function[bf]["by_type"][obj_type] += 1
        by_business_function[bf]["by_state"][state] += 1
        if app_comp:
            # Extract first two parts of app component (e.g., "FI-GL" from "FI-GL-ACC")
            parts = app_comp.split("-")
            if len(parts) >= 2:
                by_business_function[bf]["app_components"].add(parts[0] + "-" + parts[1])
            else:
                by_business_function[bf]["app_components"].add(app_comp)

        by_type[obj_type] += 1
        by_state[state] += 1

    # Generate markdown
    lines = []

    # Header
    lines.append("# SAP API Reference Catalog")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(f"- **Total APIs**: {len(apis):,}")
    lines.append(f"- **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"- **Source**: github.com/SAP/abap-atc-cr-cv-s4hc")
    if custom_mappings:
        lines.append(f"- **Custom Mappings**: {len(custom_mappings)}")
    lines.append("")

    # Summary by state
    lines.append("### API States")
    lines.append("")
    lines.append("| State | Count | Description |")
    lines.append("|-------|-------|-------------|")
    state_descriptions = {
        "deprecated": "Being retired by SAP",
        "classicAPI": "Legacy API, plan migration",
        "noAPI": "Internal, not for external use",
        "notToBeReleased": "Will not be released publicly",
        "released": "Officially released and supported",
        "custom": "User-defined mapping"
    }
    for state, count in sorted(by_state.items(), key=lambda x: -x[1]):
        desc = state_descriptions.get(state, "")
        lines.append(f"| {state} | {count:,} | {desc} |")
    lines.append("")

    # Summary by type
    lines.append("### Object Types")
    lines.append("")
    lines.append("| Type | Count | Description |")
    lines.append("|------|-------|-------------|")
    type_descriptions = {
        "CLAS": "ABAP Class",
        "INTF": "Interface",
        "TABL": "Database Table",
        "DDLS": "CDS View",
        "DTEL": "Data Element",
        "DOMA": "Domain",
        "FUGR": "Function Group",
        "FUNC": "Function Module",
        "TTYP": "Table Type",
        "SHLP": "Search Help",
        "PROG": "Program",
        "BDEF": "Behavior Definition",
        "CUSTOM": "User-defined"
    }
    for obj_type, count in sorted(by_type.items(), key=lambda x: -x[1])[:15]:
        desc = type_descriptions.get(obj_type, "")
        lines.append(f"| {obj_type} | {count:,} | {desc} |")
    lines.append("")

    # Business Functions
    lines.append("---")
    lines.append("")
    lines.append("## Business Functions")
    lines.append("")

    # Summary table
    lines.append("| Business Function | Total | Deprecated | Classic | Tables | Classes |")
    lines.append("|-------------------|-------|------------|---------|--------|---------|")
    for bf in sorted(by_business_function.keys(), key=lambda x: -len(by_business_function[x]["apis"])):
        info = by_business_function[bf]
        total = len(info["apis"])
        deprecated = info["by_state"].get("deprecated", 0)
        classic = info["by_state"].get("classicAPI", 0)
        tables = info["by_type"].get("TABL", 0)
        classes = info["by_type"].get("CLAS", 0)
        lines.append(f"| {bf} | {total:,} | {deprecated} | {classic} | {tables} | {classes} |")
    lines.append("")

    # Detailed sections for each business function
    for bf in sorted(by_business_function.keys(), key=lambda x: -len(by_business_function[x]["apis"])):
        info = by_business_function[bf]
        total = len(info["apis"])

        lines.append("---")
        lines.append("")
        lines.append(f"### {bf}")
        lines.append("")
        lines.append(f"**Total APIs**: {total:,}")
        lines.append("")

        # Application components
        if info["app_components"]:
            comps = sorted(info["app_components"])[:10]
            lines.append(f"**Application Components**: {', '.join(comps)}")
            if len(info["app_components"]) > 10:
                lines.append(f"  ...and {len(info['app_components']) - 10} more")
            lines.append("")

        # Type breakdown
        lines.append("**By Type**:")
        for obj_type, count in sorted(info["by_type"].items(), key=lambda x: -x[1])[:5]:
            lines.append(f"- {obj_type}: {count}")
        lines.append("")

        # State breakdown
        lines.append("**By State**:")
        for state, count in sorted(info["by_state"].items(), key=lambda x: -x[1]):
            lines.append(f"- {state}: {count}")
        lines.append("")

        # Sample APIs (deprecated ones first, then others)
        deprecated_apis = [(n, i) for n, i in info["apis"] if i.get("state") == "deprecated"]
        other_apis = [(n, i) for n, i in info["apis"] if i.get("state") != "deprecated"]

        if deprecated_apis:
            lines.append("**Deprecated APIs** (sample):")
            lines.append("")
            lines.append("| Name | Type | Successor |")
            lines.append("|------|------|-----------|")
            for name, api_info in sorted(deprecated_apis, key=lambda x: x[0])[:10]:
                obj_type = api_info.get("type", "")
                successors = api_info.get("successors", [])
                successor = successors[0].get("name", "") if successors else "-"
                lines.append(f"| {name} | {obj_type} | {successor} |")
            if len(deprecated_apis) > 10:
                lines.append(f"| ... | | ({len(deprecated_apis) - 10} more) |")
            lines.append("")

        # Sample other APIs
        lines.append("**Sample APIs**:")
        lines.append("")
        lines.append("| Name | Type | State | App Component |")
        lines.append("|------|------|-------|---------------|")
        for name, api_info in sorted(other_apis, key=lambda x: x[0])[:15]:
            obj_type = api_info.get("type", "")
            state = api_info.get("state", "")
            app_comp = api_info.get("applicationComponent", "")
            lines.append(f"| {name} | {obj_type} | {state} | {app_comp} |")
        if len(other_apis) > 15:
            lines.append(f"| ... | | | ({len(other_apis) - 15} more) |")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("## Updating This Catalog")
    lines.append("")
    lines.append("To regenerate this catalog after updating SAP reference data:")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 agents/business-function-mapper/generate-catalog.py")
    lines.append("```")
    lines.append("")
    lines.append("To add custom mappings, edit `input/sap-api-reference/custom-mappings.json`")
    lines.append("")
    lines.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    # Write output atomically
    output_file.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(lines)
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

    print(f"\nCatalog generated: {output_file}", file=sys.stderr)
    print(f"  Total APIs: {len(apis):,}", file=sys.stderr)
    print(f"  Business Functions: {len(by_business_function)}", file=sys.stderr)
    print(f"  Custom Mappings: {len(custom_mappings)}", file=sys.stderr)

    return {
        "status": "success",
        "totalApis": len(apis),
        "businessFunctions": len(by_business_function),
        "customMappings": len(custom_mappings),
        "outputFile": str(output_file)
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate SAP API Reference Catalog")
    parser.add_argument("--api-file", type=Path, default=DEFAULT_API_FILE,
                        help="Path to api-parsed.json")
    parser.add_argument("--custom-file", type=Path, default=DEFAULT_CUSTOM_FILE,
                        help="Path to custom-mappings.json")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT,
                        help="Output path for CATALOG.md")

    args = parser.parse_args()

    result = generate_catalog(args.api_file, args.custom_file, args.output)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
