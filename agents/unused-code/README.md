# SAP Unused Code Discovery Agent

Identifies unused custom Z*/Y* code in SAP systems using SUSG runtime statistics and reference analysis.

## Configuration

| Setting | Value |
|---------|-------|
| Model | Claude Opus 4.5 |
| BATCH_SIZE | 3 (checkpoint frequency) |
| State File | progress.json |

## Quick Start

```bash
kiro-cli --agent sap-unused-code-discovery

> "Check if ZCL_MY_CLASS is unused"        # Offline mode (SUSG only)
> "Analyze package ZFLIGHT for unused code"   # Online mode (SUSG + SAP)
```

## Analysis Modes

| Mode | Data Source | SAP Connection | Use Case |
|------|-------------|----------------|----------|
| **Offline** | SUSG XML only | Not needed | Single object analysis |
| **Online** | SUSG + Live SAP | Required | Package analysis, source search |

### Offline Mode
- Uses only SUSG XML files from `input/`
- No MCP server or SAP credentials needed
- Best for checking specific objects by name

### Online Mode
- Uses SUSG data + connects to live SAP
- Finds all Z/Y objects in a package
- Can search source code for static references
- Requires MCP server and SAP credentials

## Prerequisites

### 1. SUSG Runtime Data (Required for both modes)
Export SUSG data from SAP - see below.

### 2. SAP Connection (Online mode only)
Configured via `mcp/sap.env` (same as other agents).
Only needed for package analysis or source code reference search.

### 3. SUSG Data Setup
Export SUSG data from SAP and place in `input/`:

**Option A: ZIP file (Recommended)**
```
input/
└── SUSG.zip    # Agent will auto-extract
```

**Option B: Extracted XML files**
```
input/
├── ADMIN0001.xml    # Metadata (optional)
├── PROG0001.xml     # Object master (required)
├── DATA0001.xml     # Execution stats (required)
├── DATA0002.xml     # More execution stats
├── RDATA0001.xml    # Call relationships (required)
└── SUB0001.xml      # Trigger contexts (required)
```

**To export from SAP:**
1. Transaction: `SUSG` (Usage Statistics)
2. Execute statistics collection
3. Export to ZIP
4. Copy `SUSG.zip` to `input/`
5. Agent will auto-extract on first run

## Classification Levels

| Classification | Confidence | Meaning | Action |
|----------------|------------|---------|--------|
| **UNUSED** | HIGH | No executions, no callers | Safe to delete |
| **LIKELY_UNUSED** | MEDIUM | No evidence of use, but cannot fully verify | Verify before deletion |
| **USED** | HIGH | Has runtime executions or callers | Keep - actively used |
| **INDETERMINATE** | LOW | Cannot determine | Manual review in SE80 |

## Output

Reports generated to `reports/unused/{PACKAGE}/`:

```
reports/unused/ZFLIGHT/
├── ZCL_OBJECT1_unused.md    # Per-object analysis
├── ZCL_OBJECT2_unused.md
├── SUMMARY.md               # Package overview
├── VISUALIZATION.md         # Mermaid dependency graph
└── progress.json            # Resume tracking
```

### SUMMARY.md
- Classification distribution
- Deletion candidates list
- Cleanup potential metrics
- Statistics by object type

### VISUALIZATION.md
- Mermaid dependency graph
- Color-coded by classification
- Unused chains detection
- Isolated objects list

## Features

### Progress Tracking
Large packages can be processed across multiple sessions. The agent automatically:
- Creates `progress.json` on start
- Updates after each object
- Resumes from where it left off

### Unused Chains Detection
Identifies groups of objects that only reference each other:
```
ZCL_A --> ZCL_B --> ZCL_C --> ZCL_A (circular, all unused)
```
These can be safely deleted together.

## Example Output

```
[1/32] ZCL_ORDER_PROCESSOR: USED (HIGH) - 1508 executions, 3 callers
[2/32] ZCL_OLD_REPORT: UNUSED (HIGH) - 0 executions, 0 callers
[3/32] ZCL_TEST_HELPER: LIKELY_UNUSED (MEDIUM) - 0 executions, 0 callers
...
Complete! Found: 5 UNUSED, 3 LIKELY_UNUSED, 22 USED, 2 INDETERMINATE
Cleanup potential: 8 objects (25%)
```

## Limitations

- **Custom code only**: Only analyzes Z*/Y* objects
- **Runtime data required**: Best results need SUSG export
- **Dynamic calls**: Cannot detect `CALL METHOD (variable)` or `CALL FUNCTION variable`
- **Cross-system**: Cannot detect RFC calls from other systems
- **Configuration**: May miss objects used only in IMG configuration

## Workflow

```
Phase 1: Initialization
├── Check for existing progress.json
│   ├── If exists: Resume Validation (5 integrity checks)
│   └── File System Reconciliation (sync .md files with progress.json)
├── Load SUSG XML data (build lookup maps)
├── Verify SAP connection
├── Search Z*/Y* objects
├── Create progress.json
└── Phase 1 Gate: Verify all prerequisites

Phase 2: Processing (Batch Mode)
├── BATCH_SIZE = 3 (checkpoint every 3 objects)
├── For each object: Analyze → Classify → Save report → Track in batch
├── Every 3 objects: Update progress.json
└── Output: [{N}/{TOTAL}] {NAME}: {classification}

Phase 3: Completion
├── Generate VISUALIZATION.md (Mermaid graphs)
├── Generate SUMMARY.md
├── Archive progress.json
└── Output: "Complete! Cleanup potential: X objects (Y%)"
```

## Crash Recovery

**File System Reconciliation**: On resume, the agent checks which `_unused.md` files exist on disk but are marked "pending" in progress.json. These are automatically reconciled, preventing duplicate analysis.

**Example**: If context overflows after analyzing 15 objects but only 12 were checkpointed, reconciliation will recover the 3 missing entries from the existing `_unused.md` files.

## Related Agents

| Agent | Purpose |
|-------|---------|
| `sap-atc-checker` | Clean Core compliance checks |
| `sap-custom-code-documenter` | Generate documentation |
| `sap-unused-code-discovery` | Find unused code (this agent) |

## Technology

| Component | Technology |
|-----------|------------|
| Agent Framework | Kiro-CLI |
| AI Model | Claude Opus 4.5 |
| SAP Connectivity | MCP Server (Docker) |
| Runtime Data | SUSG XML Export |
