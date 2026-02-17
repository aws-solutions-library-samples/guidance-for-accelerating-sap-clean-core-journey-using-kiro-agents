# Input Directory

Runtime data files for SAP Unused Code Discovery skill.

## Location

This directory is at the project root: `/clean-core-automation/input/`

When running the skill from `/clean-core-automation/skills/SAP-Unused-Code-Discovery/`:
```bash
node --import tsxrun-unused-code-check.ts ZCL_TEST --runtime-data=../../input/SUSG.zip
```

## Supported Formats

Place your SCMON/SUSG runtime data files here:

- XML files: `scmon_export.xml` (SAP native format - recommended)
- CSV files: `scmon_export.csv`
- JSON files: `runtime_stats.json`
- ZIP files: `SUSG.zip` (will be auto-extracted to this directory)

Supported formats:
- .xml (SAP native SCMON/SUSG exports)
- .csv
- .json
- .zip (containing XML, CSV, or JSON files)

ZIP files are automatically extracted to this same directory.

