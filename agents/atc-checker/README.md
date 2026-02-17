# SAP ATC Checker

Runs ATC (ABAP Test Cockpit) checks and classifies objects by Clean Core compliance level.

## Quick Start

```bash
cd /clean-core
kiro-cli --agent sap-atc-checker

> "Check package Z_FLIGHT"
> "Run ATC check on ZCL_MY_CLASS"
> "Check package ZAPI with variant ABAP_CLOUD_DEVELOPMENT"
```

## Features

- **Bulk processing** - Check entire packages
- **Resume capability** - Survives context overflow via progress.json
- **File System Reconciliation** - No duplicate work on resume
- **Batch checkpoints** - Progress saved every 3 objects
- **Clean Core classification** - Levels A/B/C/D based on findings
- **Remediation guidance** - Documentation and quick fixes included

## Configuration

| Setting | Value |
|---------|-------|
| Model | Claude Opus 4.5 |
| BATCH_SIZE | 3 (checkpoint frequency) |
| Default Variant | CLEAN_CORE |
| State File | progress.json |

## CRITICAL: ATC Parameters

**EVERY ATC check MUST include:**
```
includeDocumentation: true   ← MANDATORY
includeQuickFixes: true      ← MANDATORY
variant: "CLEAN_CORE"        ← MANDATORY (or user-specified)
```

## Clean Core Levels

| Level | ATC Priority | Status | Action |
|-------|--------------|--------|--------|
| A | None | Fully compliant with Clean Core | Ready for cloud |
| B | Info | Uses documented extension points | Acceptable, low upgrade risk |
| C | Warning | Uses internal or undocumented APIs | Conditionally clean, verify before upgrades |
| D | Error | Non-released APIs, modifications, or blocked patterns | Requires remediation |

**Rule**: Worst finding determines level. One Error = Level D.

## Supported Object Types

| Type | Description |
|------|-------------|
| CLAS | Classes |
| PROG | Programs |
| INTF | Interfaces |
| FUGR | Function Groups |
| DDLS | CDS Views |
| FUNC | Function Modules |
| BDEF | Behavior Definitions (RAP) |

**Skipped**: TABL, DOMA, DTEL, VIEW, STOB, DEVC, etc.

## Workflow

```
Phase 1: Initialization
├── Check for existing progress.json
│   ├── If exists: Resume Validation (5 integrity checks)
│   └── File System Reconciliation (sync _atc.md files with progress.json)
├── Verify SAP connection
├── Search Z*/Y* objects → Create discovery.json
├── Filter to checkable types
├── Create progress.json
└── Phase 1 Gate: Verify all prerequisites

Phase 2: Processing (Batch Mode)
├── BATCH_SIZE = 3 (checkpoint every 3 objects)
├── For each object: Run ATC → Classify → Save report → Track in batch
├── Every 3 objects: Update progress.json
└── Output: [{N}/{TOTAL}] {NAME}: Level {X} ({E}E/{W}W/{I}I)

Phase 3: Completion
├── Generate SUMMARY.md (via Python script)
└── Archive discovery.json + progress.json
```

## Output

```
reports/atc/{PACKAGE}/
├── {OBJECT_NAME}_atc.md       # Per-object findings + remediation
├── SUMMARY.md                 # Level distribution + roadmap
├── {timestamp}-discovery.json # Archived SAP search results
└── {timestamp}-progress.json  # Archived processing state
```

## Crash Recovery

**File System Reconciliation**: On resume, the agent checks which _atc.md files exist on disk but are marked "pending" in progress.json. These are automatically reconciled, preventing duplicate ATC checks.

**Example**: If context overflows after checking 15 objects but only 12 were checkpointed, reconciliation will recover the 3 missing entries from the existing _atc.md files.

## Default Variant

`CLEAN_CORE` - Override with: "Check with variant ABAP_CLOUD_DEVELOPMENT"

## Files

| File | Purpose |
|------|---------|
| `instructions.md` | Agent prompt (comprehensive) |
| `generate-summary.py` | Generate SUMMARY.md from progress.json |
| `README.md` | User guide (this file) |

## Troubleshooting

**Connection failed**: Check SAP system, Docker (`docker ps`), sap.env config

**ATC check failed**: Verify object exists, user has ATC authorization, variant exists

**Missing documentation in reports**: Ensure `includeDocumentation: true` is being passed

**Resume issues**: Delete progress.json to start fresh, or check for corrupt JSON
