#!/usr/bin/env python3
"""
Business Function Mapper - Report Generator

Generates the final CLEAN_CORE_ASSESSMENT report from progress.json and template.
This is the standard report generation script - DO NOT create custom scripts.

Usage:
    python3 generate-report.py <PACKAGE>

Example:
    python3 generate-report.py Z_CL_SRIO_DEV
"""

import json
import os
import re
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

# CC_DIR: Clean Core root directory
# Auto-derive from script location if not set (script is in agents/business-function-mapper/)
CC_DIR = os.environ.get("CC_DIR") or str(Path(__file__).resolve().parent.parent.parent)
BASE_DIR = CC_DIR  # Alias for compatibility


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
    if not re.match(r'^[$A-Z][A-Z0-9_]{0,29}$', name):
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


def generate_executive_overview(progress):
    """Generate executive overview paragraph."""
    total = progress.get("totalObjects", 0)
    findings = progress.get("objectsWithFindings", 0)
    level_dist = progress.get("levelDistribution", {})

    level_d = level_dist.get("D", {}).get("count", 0)
    level_c = level_dist.get("C", {}).get("count", 0)
    level_a = level_dist.get("A", {}).get("count", 0)
    level_b = level_dist.get("B", {}).get("count", 0)

    cloud_ready = level_a + level_b
    needs_work = level_c + level_d
    
    # Use findings as total if totalObjects is 0 (edge case)
    if total == 0:
        total = findings

    bf_count = len(progress.get("businessFunctions", {}))
    deprecated_count = len(progress.get("deprecatedApis", []))

    overview = f"This assessment analyzed **{total} custom ABAP objects** in package {progress.get('package', 'N/A')}. "

    if findings > 0 and total > 0:
        overview += f"Of these, **{findings} objects** ({round(findings*100/total)}%) have findings that require attention.\n\n"
    elif findings > 0:
        overview += f"**{findings} objects** have findings that require attention.\n\n"
    else:
        overview += "All objects are cloud ready with no findings requiring attention.\n\n"

    if level_d > 0:
        overview += f"**{level_d} objects require immediate action** (Level D) due to severe violations such as modifications or use of non-recommended APIs. "

    if level_c > 0:
        overview += f"**{level_c} objects need modernization planning** (Level C) to address usage of internal SAP objects.\n\n"

    if cloud_ready > 0 and total > 0:
        overview += f"**{cloud_ready} objects ({round(cloud_ready*100/total)}%) are already cloud ready** (Level A/B)."

    if bf_count > 0:
        overview += f" The findings impact **{bf_count} business areas**"
        if deprecated_count > 0:
            overview += f" with **{deprecated_count} APIs needing updates**"
        overview += "."

    return overview


def generate_level_distribution_table(progress):
    """Generate Clean Core Level Distribution table."""
    level_dist = progress.get("levelDistribution", {})

    status_map = {
        "A": "Ready for cloud",
        "B": "Acceptable",
        "C": "Plan migration",
        "D": "Requires action"
    }

    lines = ["| Level | Count | Percentage | Status |", "|-------|-------|------------|--------|"]

    for level in ["A", "B", "C", "D"]:
        data = level_dist.get(level, {"count": 0, "percentage": "0%"})
        count = data.get("count", 0)
        pct = data.get("percentage", "0%")
        status = status_map.get(level, "")
        lines.append(f"| {level} | {count} | {pct} | {status} |")

    return "\n".join(lines)


def generate_business_area_table(progress):
    """Generate Impact by Business Area table.

    Each object is counted only once, assigned to its primary business area.
    Objects with only uncategorized APIs go to "Uncategorized".
    Objects with categorized APIs go to their business area (not Uncategorized).
    """
    bf = progress.get("businessFunctions", {})
    objects = progress.get("objects", [])

    # Determine priority based on object levels
    def get_priority(obj_names):
        for obj in objects:
            if obj.get("name") in obj_names and obj.get("level") == "D":
                return "HIGH"
        return "MEDIUM"

    # Collect all objects that have a categorized business area (not Uncategorized)
    categorized_objects = set()
    for bf_name, bf_data in bf.items():
        if bf_name != "Uncategorized":
            categorized_objects.update(bf_data.get("objects", []))

    # Build table rows - exclude Uncategorized from main loop
    lines = ["| Business Area | Objects | Priority |", "|---------------|---------|----------|"]

    sorted_bf = sorted(
        [(k, v) for k, v in bf.items() if k != "Uncategorized"],
        key=lambda x: len(x[1].get("objects", [])),
        reverse=True
    )

    for bf_name, bf_data in sorted_bf:
        bf_objects = set(bf_data.get("objects", []))
        obj_count = len(bf_objects)
        priority = get_priority(bf_objects)
        lines.append(f"| {bf_name} | {obj_count} | {priority} |")

    # Uncategorized = objects that ONLY have uncategorized APIs (not in any other business area)
    uncategorized_bf = bf.get("Uncategorized", {})
    all_uncategorized = set(uncategorized_bf.get("objects", []))
    # Only count objects that are NOT in any categorized business area
    pure_uncategorized = all_uncategorized - categorized_objects

    if pure_uncategorized:
        priority = get_priority(pure_uncategorized)
        # Use HIGH if any Level D, else REVIEW for uncategorized
        if priority != "HIGH":
            priority = "REVIEW"
        lines.append(f"| Uncategorized | {len(pure_uncategorized)} | {priority} |")

    return "\n".join(lines)


def generate_top_findings_table(progress):
    """Generate Top Findings table from ATC SUMMARY.md."""
    atc_source = progress.get("atcReportSource", "")
    summary_file = Path(atc_source) / "SUMMARY.md"

    if not summary_file.exists():
        return "| Issue | Affected Objects | Severity | Recommended Action |\n|-------|------------------|----------|-------------------|\n| No data available | - | - | - |"

    content = summary_file.read_text(encoding='utf-8')

    # Find Top Findings table
    pattern = r"Top Findings.*?\n(.*?)(?=\n##|\n---|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

    if not match:
        return "| Issue | Affected Objects | Severity | Recommended Action |\n|-------|------------------|----------|-------------------|\n| No data available | - | - | - |"

    # Return the table as-is (it's already formatted)
    table_content = match.group(1).strip()

    # If the table doesn't have the expected format, create a simple one
    if "|" not in table_content:
        return "| Issue | Affected Objects | Severity | Recommended Action |\n|-------|------------------|----------|-------------------|\n| See ATC reports | - | - | Review individual reports |"

    return table_content


def fill_template(template_content, progress):
    """Fill template placeholders with values."""
    now = datetime.now()

    replacements = {
        "{{PACKAGE_NAME}}": progress.get("package", ""),
        "{{ASSESSMENT_DATE}}": now.strftime("%Y-%m-%d"),
        "{{DATE_TIME}}": now.strftime("%Y-%m-%d %H:%M"),
        "{{SOURCE_SYSTEM}}": progress.get("sourceSystem", "N/A"),
        "{{ATC_VARIANT}}": progress.get("variant", "N/A"),
        "{{TOTAL_OBJECTS}}": str(progress.get("totalObjects", 0)),
        "{{OBJECTS_WITH_FINDINGS}}": str(progress.get("objectsWithFindings", 0)),
        "{{EXECUTIVE_OVERVIEW}}": generate_executive_overview(progress),
        "{{CLEAN_CORE_LEVEL_DISTRIBUTION}}": generate_level_distribution_table(progress),
        "{{FINDINGS_BY_BUSINESS_AREA_TABLE}}": generate_business_area_table(progress),
        "{{TOP_FINDINGS_TABLE}}": generate_top_findings_table(progress),
        "{{LEVEL_D_COUNT}}": str(progress.get("levelDistribution", {}).get("D", {}).get("count", 0))
    }

    result = template_content
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)

    return result


def generate_report(package_name):
    """Generate the final assessment report."""

    # Paths (using BASE_DIR for portability)
    progress_file = Path(f"{BASE_DIR}/reports/executive/{package_name}/progress.json")
    template_file = Path(f"{BASE_DIR}/agents/business-function-mapper/report-template.md")
    output_dir = Path(f"{BASE_DIR}/reports/executive/{package_name}")
    md_output = output_dir / "CLEAN_CORE_ASSESSMENT.md"
    html_output = output_dir / "CLEAN_CORE_ASSESSMENT.html"

    # Check prerequisites
    if not progress_file.exists():
        print(f"ERROR: progress.json not found at {progress_file}", file=sys.stderr)
        print("Run init-progress.py and process-objects.py first.", file=sys.stderr)
        return {"status": "error", "message": "progress.json not found"}

    if not template_file.exists():
        print(f"ERROR: Template not found at {template_file}", file=sys.stderr)
        return {"status": "error", "message": "Template not found"}

    # Load data
    print(f"Loading progress from {progress_file}...", file=sys.stderr)
    progress = load_json(progress_file)

    print(f"Loading template from {template_file}...", file=sys.stderr)
    template_content = template_file.read_text(encoding='utf-8')

    # Generate report
    print("Generating report...", file=sys.stderr)
    report_content = fill_template(template_content, progress)

    # Write markdown atomically
    fd, temp_path = tempfile.mkstemp(dir=output_dir, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(report_content)
        os.replace(temp_path, md_output)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise
    print(f"  Markdown: {md_output}", file=sys.stderr)

    # Generate HTML
    html_converter = Path(f"{BASE_DIR}/agents/business-function-mapper/md-to-html.py")
    if html_converter.exists():
        try:
            html_result = subprocess.run(  # nosemgrep: dangerous-subprocess-use-audit, dangerous-subprocess-use-tainted-env-args
                [sys.executable, str(html_converter), str(md_output), str(html_output)],  # nosemgrep: dangerous-subprocess-use-tainted-env-args
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout to prevent hangs
            )
            if html_result.returncode == 0:
                print(f"  HTML: {html_output}", file=sys.stderr)
            else:
                print(f"  WARNING: HTML generation failed: {html_result.stderr}", file=sys.stderr)
        except subprocess.TimeoutExpired:
            print("  ERROR: HTML generation timed out after 60 seconds", file=sys.stderr)
    else:
        print("  WARNING: md-to-html.py not found, skipping HTML generation", file=sys.stderr)

    # Archive progress
    archive_name = datetime.now().strftime("%Y-%m-%d-%H%M%S") + "-progress.json"
    archive_path = output_dir / archive_name
    shutil.copy(progress_file, archive_path)
    progress_file.unlink()
    print(f"  Archived progress to: {archive_name}", file=sys.stderr)

    # Summary
    print(f"\nReport generated successfully!", file=sys.stderr)
    print(f"  Package: {package_name}", file=sys.stderr)
    print(f"  Total Objects: {progress.get('totalObjects', 0)}", file=sys.stderr)
    print(f"  Business Areas: {len(progress.get('businessFunctions', {}))}", file=sys.stderr)

    return {
        "status": "success",
        "package": package_name,
        "markdownReport": str(md_output),
        "htmlReport": str(html_output) if html_output.exists() else None,
        "archivedProgress": str(archive_path)
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate-report.py <PACKAGE>", file=sys.stderr)
        print("Example: python3 generate-report.py Z_CL_SRIO_DEV", file=sys.stderr)
        sys.exit(1)

    package_name = validate_package_name(sys.argv[1])
    result = generate_report(package_name)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
