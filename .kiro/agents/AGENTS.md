# AGENTS.md - SAP Clean Core Platform

A guide for AI coding agents working with the SAP Clean Core Platform.

See [README.md](README.md) for human-focused documentation and quick start guides.

---

## Project Overview

The **SAP Clean Core Platform** is a multi-agent system for SAP ABAP analysis, built on Kiro-CLI with MCP server integration. It helps organizations assess and remediate custom ABAP code for SAP S/4HANA Cloud readiness.

### Platform Configuration

| Setting | Value |
|---------|-------|
| AI Model | Claude Opus 4.5 |
| BATCH_SIZE | 3 (checkpoint frequency) |
| State File | progress.json |

---

## Agent Inventory

| Agent | Purpose | Key MCP Tools | Output Location | Depends On |
|-------|---------|---------------|-----------------|------------|
| **sap-atc-checker** | ATC compliance, Clean Core Levels A-D | `run_atc_check`, `search_object` | `/reports/atc/` | - |
| **sap-custom-code-documenter** | Dual-audience documentation | `get_source`, `search_object` | `/reports/docs/` | - |
| **sap-unused-code-discovery** | SUSG-based unused code analysis | `search_object` (optional) | `/reports/unused/` | SUSG XML data |
| **business-function-mapper** | Map findings to business areas | None (file-based) | `/reports/executive/` | **sap-atc-checker** |
| **abap-accelerator** | General-purpose ABAP assistant | All MCP tools | Context-dependent | - |

---

## Agent Dependencies

```
┌─────────────────┐     ┌─────────────────────────┐
│ sap-atc-checker │────▶│ business-function-mapper│
│                 │     │ (REQUIRES ATC output)   │
└─────────────────┘     └─────────────────────────┘

Independent (no agent dependencies):
- sap-atc-checker
- sap-custom-code-documenter
- sap-unused-code-discovery (requires SUSG data files, not another agent)
- abap-accelerator
```

**Important**: Run `sap-atc-checker` BEFORE `business-function-mapper`. The mapper reads ATC reports from `/reports/atc/{PACKAGE}/`.

---

## Critical Files & Directories

### Configuration
| File | Purpose |
|------|---------|
| `mcp/sap.env` | SAP connection settings (host, client, user) |
| `secrets/sap_password` | SAP password (chmod 600) |
| `.kiro/agents/*.json` | Agent configurations |

### Input Data
| Location | Purpose |
|----------|---------|
| `input/PROG0001.xml`, `DATA*.xml`, `RDATA*.xml` | SUSG XML export (for unused-code) |
| `input/susg-parsed.json` | Parsed SUSG data (generated) |
| `input/sap-api-reference/api-parsed.json` | SAP API reference mappings |
| `input/sap-api-reference/custom-mappings.json` | User-defined API overrides |

### Output
| Location | Purpose |
|----------|---------|
| `reports/atc/{PACKAGE}/` | ATC compliance reports |
| `reports/docs/{PACKAGE}/` | Object documentation |
| `reports/unused/{PACKAGE}/` | Unused code analysis |
| `reports/executive/{PACKAGE}/` | Executive summaries |

### State (Progress Tracking)
| Location | Purpose |
|----------|---------|
| `reports/{type}/{PACKAGE}/progress.json` | Current processing state |

---

## Agent Instructions

Each agent has detailed instructions in `agents/{name}/instructions.md` including:
- Workflow phases and steps
- Output templates and formats
- State management (progress.json schema)
- Content quality rules

**Always follow the agent-specific `instructions.md` for detailed guidance.**

---

## Python Scripts Reference

| Script | Location | Purpose |
|--------|----------|---------|
| `parse-susg.py` | `agents/unused-code/` | Parse SUSG XML → `susg-parsed.json` |
| `parse-api-refs.py` | `agents/business-function-mapper/` | Parse SAP API reference from GitHub |
| `init-progress.py` | `agents/business-function-mapper/` | Create progress.json from ATC SUMMARY |
| `process-objects.py` | `agents/business-function-mapper/` | Extract APIs, map to business functions |
| `generate-report.py` | `agents/business-function-mapper/` | Generate CLEAN_CORE_ASSESSMENT from template |
| `generate-catalog.py` | `agents/business-function-mapper/` | Generate CATALOG.md from api-parsed.json |
| `generate-summary.py` | `agents/atc-checker/` | Generate SUMMARY.md from progress.json |
| `md-to-html.py` | `agents/business-function-mapper/` | Convert markdown to styled HTML |

**Templates**:
| Template | Location | Purpose |
|----------|----------|---------|
| `report-template.md` | `agents/business-function-mapper/` | Template for CLEAN_CORE_ASSESSMENT.md |

---

## Data Flow

```
SAP System (MCP)                    SUSG XML Export
      │                                   │
      │ aws_abap_cb_*                     │ parse-susg.py
      ▼                                   ▼
┌─────────────────────────────────────────────────────┐
│                   INPUT LAYER                        │
│  /input/sap-api-reference/api-parsed.json           │
│  /input/susg-parsed.json                            │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                   AGENT LAYER                        │
│  atc-checker → /reports/atc/                        │
│  documenter → /reports/docs/                        │
│  unused-code → /reports/unused/                     │
│  business-function-mapper → /reports/executive/     │
│       ↑ reads /reports/atc/ (dependency)            │
└─────────────────────────────────────────────────────┘
```

---

## Common Object Types

| Type | Description | MCP Type |
|------|-------------|----------|
| `CLAS` | Class | `CLAS` |
| `CLAS/OC` | Class (with includes) | Use `CLAS` for `get_source` |
| `PROG` | Program | `PROG` |
| `PROG/P` | Executable Program | Use `PROG` for `get_source` |
| `PROG/I` | Include Program | Use `PROG` for `get_source` |
| `INTF` | Interface | `INTF` |
| `FUGR` | Function Group | `FUGR` |
| `DDLS` | CDS View | `DDLS` |
| `DDLS/DF` | CDS View Definition | Use `DDLS` for `get_source` |
| `DCLS` | Access Control | `DCLS` |
| `DDLX` | CDS Metadata Extension | `DDLX` |
| `BDEF` | Behavior Definition | `BDEF` |
| `SRVD` | Service Definition | `SRVD` |
| `SRVB` | Service Binding | `SRVB` |

**Important**: When calling `aws_abap_cb_get_source`, use the base type (e.g., `CLAS` not `CLAS/OC`).

### MCP Tool Call Examples

#### CRITICAL: ATC Check Parameters

**EVERY `aws_abap_cb_run_atc_check` call MUST include:**
```
includeDocumentation: true   ← MANDATORY - never false
includeQuickFixes: true      ← MANDATORY - never false
variant: "CLEAN_CORE"        ← MANDATORY - never omit
```

✅ **Correct** - ATC check with ALL mandatory parameters:
```
aws_abap_cb_run_atc_check(
  objectName: "ZCL_EXAMPLE",
  objectType: "CLAS/OC",
  variant: "CLEAN_CORE",
  includeDocumentation: true,
  includeQuickFixes: true
)
```

❌ **Incorrect** - Missing mandatory parameters:
```
aws_abap_cb_run_atc_check(
  objectName: "ZCL_EXAMPLE",
  objectType: "CLAS/OC",
  variant: "CLEAN_CORE",
  includeDocumentation: false,  ← WRONG! Must be true
  includeQuickFixes: false      ← WRONG! Must be true
)
```
_Reports will lack documentation and quick fix guidance_

❌ **Incorrect** - Missing variant parameter:
```
aws_abap_cb_run_atc_check(
  objectName: "ZCL_EXAMPLE",
  objectType: "CLAS/OC"
)
```
_SAP will use system default variant, not CLEAN_CORE_

✅ **Correct** - get_source with base type:
```
aws_abap_cb_get_source(objectName: "ZCL_EXAMPLE", objectType: "CLAS")
```

❌ **Incorrect** - get_source with compound type:
```
aws_abap_cb_get_source(objectName: "ZCL_EXAMPLE", objectType: "CLAS/OC")
```
_Compound types are not supported by get_source_

---

## Workflow Pattern

All batch-processing agents (atc-checker, documenter, unused-code) follow this pattern:

```
Phase 1: Initialization
├── Check for existing progress.json
│   ├── If exists: Resume Validation (5 integrity checks)
│   └── File System Reconciliation (sync files with progress.json)
├── Verify SAP connection
├── Search Z*/Y* objects → Create discovery.json
├── Filter to supported types
├── Create progress.json
└── Phase 1 Gate: Verify all prerequisites

Phase 2: Processing (Batch Mode)
├── BATCH_SIZE = 3 (checkpoint every 3 objects)
├── For each object: process → save file → track in batch
├── Every 3 objects: checkpoint progress.json
└── Output: [{N}/{TOTAL}] {NAME}: {result}

Phase 3: Completion
├── Generate SUMMARY.md (via Python script)
└── Archive discovery.json + progress.json → {TIMESTAMP}-*.json
```

### File System Reconciliation

On resume, the agent syncs actual files on disk with progress.json:
- Files exist but marked "pending" → Update to completed
- Prevents duplicate processing after context overflow

### Resume Validation (5 Checks)

1. JSON parses successfully
2. No duplicate object entries
3. Counts match (documented + failed + pending = total)
4. Package name matches user request
5. All pending objects have valid names

---

## Best Practices

### ATC Checks
1. **ALWAYS set `includeDocumentation: true`** - MANDATORY for remediation guidance
2. **ALWAYS set `includeQuickFixes: true`** - MANDATORY for fix suggestions
3. **ALWAYS specify `variant`** when running ATC checks (default: `CLEAN_CORE`)

### MCP Tool Usage
4. **Use `search_object`** instead of `get_objects` for better filtering
5. **Use base object types** for `get_source` calls (e.g., `CLAS` not `CLAS/OC`)
6. **Check syntax before activation** using `check_syntax`

### Processing
7. **Checkpoint every 3 objects** - Update progress.json every BATCH_SIZE objects
8. **Handle errors gracefully** - retry transient failures, log permanent failures
9. **Never skip reconciliation** - Always sync files with progress.json on resume

---

## Error Handling

| Error | Solution |
|-------|----------|
| Connection failed | Check `sap.env`, run `connection_status` first |
| Object not found | Verify name/type with `search_object` |
| Syntax errors | Use `check_syntax` before activation |
| ATC timeout | Reduce scope (single object vs package) |
| Missing SUSG data | Export from SAP transaction SUSG |
| Context overflow | Restart agent and ask to "resume"; reconciliation syncs files |
| Missing doc in ATC reports | Ensure `includeDocumentation: true` was used |

---

## Related Documentation

| File | Purpose |
|------|---------|
| [README.md](README.md) | Project overview and setup |
| [docs/agent-guide.md](docs/agent-guide.md) | Agent capabilities and commands |
| [docs/SECURITY.md](docs/SECURITY.md) | Security model and permissions |
| `agents/*/README.md` | Per-agent user guides |
| `agents/*/instructions.md` | Agent prompts (comprehensive) |

---

*SAP Clean Core Platform v1.2 - Claude Opus 4.5*
