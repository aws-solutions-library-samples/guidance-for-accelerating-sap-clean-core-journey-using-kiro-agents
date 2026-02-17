# Agent Guide

Complete reference for all SAP Clean Core agents: capabilities, commands, usage patterns, and configuration.

---

## Quick Reference

### Agent Capabilities

| Capability | atc-checker | documenter | unused-code | biz-mapper | accelerator |
|------------|:-----------:|:----------:|:-----------:|:----------:|:-----------:|
| ATC checks | YES | - | - | - | YES |
| Source retrieval | - | YES | YES | - | YES |
| Object search | YES | YES | YES | - | YES |
| File operations | YES | YES | YES | YES | YES |
| Requires SAP | YES | YES | Optional | NO | YES |
| Requires SUSG | - | - | YES | - | - |
| Depends on other agent | - | - | - | atc-checker | - |

### Invocation Commands

| Agent | Command |
|-------|---------|
| sap-atc-checker | `kiro-cli --agent sap-atc-checker` |
| sap-custom-code-documenter | `kiro-cli --agent sap-custom-code-documenter` |
| sap-unused-code-discovery | `kiro-cli --agent sap-unused-code-discovery` |
| business-function-mapper | `kiro-cli --agent business-function-mapper` |
| abap-accelerator | `kiro-cli --agent abap-accelerator` |

**Non-interactive (automation):**
```bash
kiro-cli chat --trust-all-tools --agent <agent-name> --no-interactive "<prompt>"
```

---

## Which Agent Should I Use?

### Decision Tree

```
START
  |
  +-- Need Clean Core compliance assessment?
  |     YES --> sap-atc-checker
  |
  +-- Need code documentation?
  |     YES --> sap-custom-code-documenter
  |
  +-- Have SUSG data and want to find unused code?
  |     YES --> sap-unused-code-discovery
  |
  +-- Have ATC reports and need executive summaries?
  |     YES --> business-function-mapper
  |
  +-- Need ad-hoc tasks or general SAP assistance?
  |     YES --> abap-accelerator
  |
  +-- Unsure?
        --> Start with sap-atc-checker or abap-accelerator
```

### Use Case Examples

| Use Case | Agent | Example Prompt |
|----------|-------|----------------|
| Assess S/4HANA readiness | sap-atc-checker | `"Check package ZLEGACY"` |
| Generate developer docs | sap-custom-code-documenter | `"Document package ZUTILS"` |
| Find dead code | sap-unused-code-discovery | `"Analyze package ZOLD"` |
| Create management report | business-function-mapper | `"Map findings for ZLEGACY"` |
| Quick code lookup | abap-accelerator | `"Show source of ZCL_HELPER"` |
| Custom analysis | abap-accelerator | `"Find all BAPIs used in ZPACKAGE"` |

---

## sap-atc-checker

### Purpose
Runs SAP ATC (ABAP Test Cockpit) checks and classifies objects into Clean Core Levels A-D.

### Key Features
- Bulk package processing with resume capability
- Batch checkpointing every 3 objects
- Automatic Clean Core level classification
- Remediation guidance with documentation and quick fixes

### Clean Core Levels

| Level | ATC Priority | Meaning | Action |
|-------|-------------|---------|--------|
| A | None | Fully compliant with Clean Core | Ready for cloud |
| B | Info only | Uses documented extension points | Acceptable, low upgrade risk |
| C | Warning | Uses internal or undocumented APIs | Conditionally clean, verify before upgrades |
| D | Error | Non-released APIs, modifications, or blocked patterns | Requires remediation |

**Classification Rule:** Worst finding determines level. One Error = Level D.

### Commands

```bash
kiro-cli --agent sap-atc-checker

# Example prompts:
> "Check package ZFLIGHT"
> "Run ATC check on ZCL_MY_CLASS"
> "Check package ZAPI with variant ABAP_CLOUD_DEVELOPMENT"
> "Resume"  # Continue interrupted session
```

### Configuration

| Option | Default | Description |
|--------|---------|-------------|
| variant | CLEAN_CORE | ATC check variant (must exist in SAP) |
| includeDocumentation | true | Include remediation guidance |
| includeQuickFixes | true | Include fix suggestions |

### Output

```
reports/atc/{PACKAGE}/
├── {OBJECT_NAME}_atc.md       # Per-object ATC findings
├── SUMMARY.md                 # Package summary with level distribution
└── {timestamp}-progress.json  # Archived processing state
```

### CLEAN_CORE Variant Requirement

> **CRITICAL**: The CLEAN_CORE variant MUST exist in your SAP system.

To verify:
1. Transaction `ATC` in SAP GUI
2. Select "Manage Check Variants"
3. Search for `CLEAN_CORE`

If not found, contact SAP Basis or create via ATC administration.

---

## sap-custom-code-documenter

### Purpose
Generates comprehensive documentation for custom ABAP objects (Z/Y prefix), targeting both developers and business analysts.

### Key Features
- Dual-audience documentation (technical + business)
- Bulk package processing with resume capability
- Support for multiple object types

### Supported Object Types

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

### Commands

```bash
kiro-cli --agent sap-custom-code-documenter

> "Document package ZFLIGHT"
> "Document class ZCL_MY_CLASS"
> "Resume"
```

### Output

```
reports/docs/{PACKAGE}/
├── {OBJECT_NAME}.md    # Per-object documentation
└── SUMMARY.md          # Package catalog
```

### Documentation Structure

Each object documentation includes:

**For Developers:**
- Main functionality overview
- Key methods/functions
- Dependencies and called objects
- Design patterns used
- ABAP style (Classic/Modern/Mixed)

**For Business Analysts:**
- Business process supported
- Problem solved
- Target users
- Business value

---

## sap-unused-code-discovery

### Purpose
Identifies unused Z*/Y* custom code using SUSG runtime statistics and reference analysis.

### Prerequisites

**SUSG Data Required:** Export runtime statistics from SAP transaction `SUSG`.

```
input/
├── PROG0001.xml       # Object master catalog
├── DATA0001.xml       # Execution statistics
├── RDATA0001.xml      # Call relationships
├── SUB0001.xml        # Trigger contexts
└── ADMIN0001.xml      # Metadata (optional)
```

### Analysis Modes

| Mode | SAP Connection | Use Case |
|------|---------------|----------|
| Offline | Not needed | Single object analysis from SUSG only |
| Online | Required | Package analysis with source search |

### Classification Levels

| Classification | Confidence | Meaning | Action |
|----------------|------------|---------|--------|
| UNUSED | HIGH | No executions, no callers | Safe to delete |
| LIKELY_UNUSED | MEDIUM | No evidence of use | Verify before deletion |
| USED | HIGH | Has runtime executions or callers | Keep |
| INDETERMINATE | LOW | Cannot determine | Manual review |

### Commands

```bash
kiro-cli --agent sap-unused-code-discovery

> "Check if ZCL_MY_CLASS is unused"  # Offline mode
> "Analyze package ZFLIGHT for unused code"  # Online mode
> "Resume"
```

### Output

```
reports/unused/{PACKAGE}/
├── {OBJECT_NAME}_unused.md  # Per-object analysis
├── SUMMARY.md               # Cleanup summary with metrics
└── VISUALIZATION.md         # Mermaid dependency graph
```

### Limitations

- Custom code only (Z*/Y* objects)
- Cannot detect dynamic calls (`CALL METHOD (variable)`)
- Cannot detect cross-system RFC calls
- May miss configuration-only usage

---

## business-function-mapper

### Purpose
Enriches ATC reports with business function context, generating executive summaries grouped by SAP application component.

### Prerequisites

> **Must run sap-atc-checker first.** This agent reads existing ATC reports.

```bash
# Step 1: Generate ATC reports
kiro-cli --agent sap-atc-checker
> "Check package ZLEGACY"

# Step 2: Generate executive summary
kiro-cli --agent business-function-mapper
> "Map findings for ZLEGACY"
```

### No SAP Connection Required
This agent processes local files only - no MCP server needed.

### Business Function Mapping

| Component Prefix | Business Function |
|------------------|-------------------|
| FI | Finance |
| CO | Controlling |
| SD | Sales & Distribution |
| MM | Materials Management |
| PP | Production Planning |
| BC | Basis Components |
| HR/HCM | Human Capital Management |
| CA | Cross-Application |

### Output

```
reports/executive/{PACKAGE}/
├── CLEAN_CORE_ASSESSMENT.md    # Executive report (Markdown)
└── CLEAN_CORE_ASSESSMENT.html  # Executive report (styled HTML)
```

---

## abap-accelerator

### Purpose
Full-featured SAP ABAP assistant with unrestricted access to all MCP tools.

### When to Use

| Use Case | Example |
|----------|---------|
| Ad-hoc lookups | `"Show source of ZCL_ORDER"` |
| Custom analysis | `"Find all BAPIs in package ZSALES"` |
| Multi-step tasks | `"Check syntax and activate ZCL_NEW"` |
| Development help | `"Help me write a class for IDoc processing"` |

### Full Tool Access

Unlike specialized agents, abap-accelerator has access to ALL MCP tools:
- Search: `search_object`, `get_objects`
- Retrieve: `get_source`, `get_test_classes`
- Analyze: `run_atc_check`, `check_syntax`, `get_migration_analysis`
- Modify: `create_object`, `update_source`, `activate_object`
- Test: `run_unit_tests`
- File operations: read, write, glob, grep, bash

### Commands

```bash
kiro-cli --agent abap-accelerator

> "Find all classes in ZFLIGHT"
> "Get source code for ZCL_MY_CLASS"
> "Run ATC check on ZPROGRAM"
> "Help me write a new report"
```

> **Note:** This agent can modify SAP system objects. Use with appropriate caution.

---

## Common Operations

### Resuming Interrupted Sessions

All batch-processing agents support automatic resume:

```bash
# Just restart the agent and say Resume
kiro-cli --agent sap-atc-checker
> "Resume"

# Or repeat your original prompt - agent detects progress.json
> "Check package ZFLIGHT"
```

### Checking Progress

Progress is tracked in `reports/{type}/{PACKAGE}/progress.json`:
```json
{
  "package": "ZFLIGHT",
  "totalObjects": 42,
  "analyzed": 15,
  "failed": 0,
  "objects": [...]
}
```

### Background Execution

```bash
kiro-cli chat --trust-all-tools --agent sap-atc-checker --no-interactive "Check package ZBIG" &
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Connection failed | SAP unreachable | Check `mcp/sap.env`, verify network |
| Object not found | Wrong name/type | Use search first to verify |
| ATC variant not found | Missing variant | Verify CLEAN_CORE exists in SAP |
| Missing SUSG data | No XML files | Export from SAP transaction SUSG |
| Context overflow | Large package | Agent auto-saves; say "Resume" |
| Permission denied | Docker access | `chmod 644 secrets/sap_password` |

### Recovery Commands

```bash
# Verify setup
./check-setup.sh --verbose

# Test SAP connection
./check-setup.sh --test-connection

# Reset progress (start fresh)
rm reports/atc/ZPACKAGE/progress.json
```

---

## Advanced Usage

### Custom ATC Variants

```bash
> "Check package ZFLIGHT with variant ABAP_CLOUD_DEVELOPMENT"
```

### Processing Specific Object Types

```bash
> "Check only classes in package ZFLIGHT"
> "Document only CDS views in package ZRAP"
```

### Combining Agents (Full Pipeline)

```bash
# 1. ATC Compliance
kiro-cli --agent sap-atc-checker
> "Check package ZLEGACY"
> /exit

# 2. Executive Summary
kiro-cli --agent business-function-mapper
> "Map findings for ZLEGACY"
> /exit

# 3. Documentation
kiro-cli --agent sap-custom-code-documenter
> "Document package ZLEGACY"
```
