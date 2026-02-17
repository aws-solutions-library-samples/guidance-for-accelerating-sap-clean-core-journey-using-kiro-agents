# Business Function Mapper Agent

Enriches ATC compliance reports with business function context by cross-referencing SAP API reference data. Generates executive summaries grouped by business function with API migration roadmaps.

## Configuration

| Setting | Value |
|---------|-------|
| Model | Claude Opus 4.5 |
| State File | progress.json |

## Purpose

Transform technical ATC findings into business-focused reports:
- **Map** referenced APIs to SAP application components (FI-GL, SD-SLS, BC-ABA)
- **Identify** deprecated APIs and their successors
- **Generate** executive summaries grouped by business function
- **Create** migration roadmaps with replacement recommendations

## Prerequisites

1. **Existing ATC reports** - Run `sap-atc-checker` first
2. **No SAP connection required** - This agent reads existing reports

## Usage

### Via Kiro CLI

```bash
cd /clean-core
kiro-cli --agent business-function-mapper
```

Then:
```
> "Map business functions for package ZFLIGHT"
```

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Business Function Mapper                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: Initialization                                         │
│  ├── Check for progress.json (resume support)                   │
│  ├── Verify ATC reports exist                                    │
│  ├── Download/load SAP API reference data                        │
│  └── Create progress.json                                        │
│                                                                  │
│  Phase 2: Processing                                             │
│  └── For each object with Level C/D:                            │
│      ├── Read ATC report for findings                           │
│      ├── Extract referenced APIs                                 │
│      ├── Lookup applicationComponent + successors               │
│      └── Aggregate by business function                          │
│                                                                  │
│  Phase 3: Completion                                             │
│  ├── Generate EXECUTIVE_SUMMARY.md                              │
│  ├── Generate BUSINESS_FUNCTION_REPORT.md                       │
│  ├── Generate MIGRATION_ROADMAP.md                              │
│  └── Archive progress.json                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Output Files

| File | Description |
|------|-------------|
| `CLEAN_CORE_ASSESSMENT.md` | Consolidated assessment report (markdown) |
| `CLEAN_CORE_ASSESSMENT.html` | Consolidated assessment report (HTML with styling) |

Location: `reports/executive/{PACKAGE}/`

### HTML Report Features
- Professional styling with AWS/SAP color scheme
- Mermaid chart rendering support
- Print-friendly CSS
- Mobile responsive design
- Color-coded Clean Core levels (A/B/C/D)

## SAP API Reference Data

The agent uses official SAP API reference data from:
- Source: https://github.com/SAP/abap-atc-cr-cv-s4hc
- Files: `objectReleaseInfoLatest.json`, `objectClassifications_SAP.json`
- Location: `input/sap-api-reference/`

The agent automatically downloads this data on first run.

## Business Function Mapping

APIs are mapped to business functions based on their `applicationComponent`:

| Prefix | Business Function |
|--------|-------------------|
| FI | Finance |
| CO | Controlling |
| SD | Sales & Distribution |
| MM | Materials Management |
| PP | Production Planning |
| BC | Basis Components |
| CA | Cross-Application |
| HR/HCM | Human Capital Management |

## Example Output

### Executive Summary (excerpt)

```markdown
## Findings by Business Area

| Business Area | Objects | Deprecated APIs | Risk Level |
|---------------|---------|-----------------|------------|
| Basis (BC)    | 3       | 5               | Medium     |
| Finance (FI)  | 2       | 3               | High       |
```

### Migration Roadmap (excerpt)

```markdown
## Priority 1: Quick Wins

| Deprecated | Successor | Objects Using |
|------------|-----------|---------------|
| TDEVC      | I_CUSTABAPPACKAGE | ZS4_VERSION_CHECK |
```

## Files

```
agents/business-function-mapper/
├── README.md              # This file
├── instructions.md        # Agent workflow instructions
├── report-template.md     # Report template (edit to customize output)
├── parse-api-refs.py      # SAP reference data parser
└── md-to-html.py          # Markdown to HTML converter
```

## Related Agents

| Agent | Purpose | Run Order |
|-------|---------|-----------|
| `sap-atc-checker` | Generate ATC compliance reports | 1st (required) |
| `sap-custom-code-documenter` | Generate documentation | Optional |
| `business-function-mapper` | Map to business functions | 2nd |

## Troubleshooting

### "No ATC reports found"
Run `sap-atc-checker` first:
```bash
kiro-cli --agent sap-atc-checker
> Check package ZFLIGHT
```

### "Could not download SAP reference data"
Manually download:
```bash
curl -L -o input/sap-api-reference/objectReleaseInfoLatest.json \
  https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfoLatest.json
```

### Resume after interruption

Simply re-run the agent - it will detect and resume from progress.json:
```
> "Resume business function mapping"
```
