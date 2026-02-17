# SAP Custom Code Documenter

Generates documentation for SAP ABAP custom objects (Z/Y prefix) for both developers and business analysts.

## Quick Start

```bash
cd /clean-core
kiro-cli --agent sap-custom-code-documenter

> "Document package ZFLIGHT"
> "Document class ZCL_MY_CLASS"
```

## Features

- **Bulk processing** - Document entire packages
- **Resume capability** - Survives context overflow via progress.json
- **File System Reconciliation** - No duplicate work on resume
- **Batch checkpoints** - Progress saved every 3 objects
- **Multiple object types** - Classes, programs, CDS views, RAP objects
- **Dual audience** - Technical (developers) + business (analysts) sections

## Configuration

| Setting | Value |
|---------|-------|
| Model | Claude Opus 4.5 |
| BATCH_SIZE | 3 (checkpoint frequency) |
| State File | progress.json |

## Supported Object Types

| Type | Description |
|------|-------------|
| CLAS | Classes |
| PROG | Programs |
| INTF | Interfaces |
| FUGR | Function Groups |
| DDLS | CDS Views |
| DCLS | Access Control |
| DDLX | Metadata Extensions |
| BDEF | Behavior Definitions (RAP) |
| SRVD | Service Definitions (RAP) |

## Workflow

```
Phase 1: Initialization
├── Check for existing progress.json
│   ├── If exists: Resume Validation (5 integrity checks)
│   └── File System Reconciliation (sync .md files with progress.json)
├── Verify SAP connection
├── Search Z*/Y* objects → Create discovery.json
├── Filter to documentable types
├── Create progress.json
└── Phase 1 Gate: Verify all prerequisites

Phase 2: Processing (Batch Mode)
├── BATCH_SIZE = 3 (checkpoint every 3 objects)
├── For each object: Get source → Document → Save .md → Track in batch
├── Every 3 objects: Update progress.json
└── Output: [{N}/{TOTAL}] {NAME}: documented

Phase 3: Completion
├── Generate SUMMARY.md (via Python script)
└── Archive discovery.json + progress.json
```

## Output

```
reports/docs/{PACKAGE}/
├── {OBJECT_NAME}.md           # Per-object documentation
├── SUMMARY.md                 # Package catalog
├── {timestamp}-discovery.json # Archived SAP search results
└── {timestamp}-progress.json  # Archived processing state
```

## Crash Recovery

**File System Reconciliation**: On resume, the agent checks which .md files exist on disk but are marked "pending" in progress.json. These are automatically reconciled, preventing duplicate documentation work.

**Example**: If context overflows after documenting 15 objects but only 12 were checkpointed, reconciliation will recover the 3 missing entries from the existing .md files.

## Files

| File | Purpose |
|------|---------|
| `instructions.md` | Agent prompt (comprehensive) |
| `generate-summary.py` | Generate SUMMARY.md from progress.json |
| `README.md` | User guide (this file) |

## Scope

Documentation only. Does NOT:
- Run ATC checks
- Assess Clean Core compliance
- Check API release status

For compliance, use `sap-atc-checker`.

## Troubleshooting

**Connection failed**: Check SAP system, Docker (`docker ps`), sap.env config

**No objects found**: Verify package name (UPPERCASE), ensure Z*/Y* objects exist

**Resume issues**: Delete progress.json to start fresh, or check for corrupt JSON
