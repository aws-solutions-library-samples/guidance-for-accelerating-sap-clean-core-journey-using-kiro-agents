# Enhancement Guide

Ideas for extending, customizing, and integrating the SAP Clean Core agents.

---

## What the Platform Does Today

Five AI agents automate SAP Clean Core compliance assessment, documentation, unused code detection, and executive reporting, all driven from `kiro-cli`.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          SAP Clean Core Platform                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌──────────────┐     ┌──────────────────┐     ┌─────────────────────────┐     │
│  │ SAP System   │────▶│ sap-atc-checker  │────▶│ business-function-mapper│     │
│  │ (via MCP)    │     │                  │     │                         │     │
│  └──────────────┘     └──────────────────┘     └─────────────────────────┘     │
│         │                    │                            │                     │
│         │                    ▼                            ▼                     │
│         │             /reports/atc/          /reports/executive/                │
│         │                                                                        │
│         │             ┌──────────────────┐                                      │
│         ├────────────▶│ sap-custom-code- │                                      │
│         │             │ documenter       │                                      │
│         │             └──────────────────┘                                      │
│         │                    │                                                   │
│         │                    ▼                                                   │
│         │             /reports/docs/                                            │
│         │                                                                        │
│  ┌──────────────┐     ┌──────────────────┐                                      │
│  │ SUSG XML     │────▶│ sap-unused-code- │                                      │
│  │ (Runtime)    │     │ discovery        │                                      │
│  └──────────────┘     └──────────────────┘                                      │
│         │                    │                                                   │
│         │                    ▼                                                   │
│         │             /reports/unused/                                          │
│         │                                                                        │
│         │             ┌──────────────────┐                                      │
│         └────────────▶│ abap-accelerator │  (General purpose - all tools)      │
│                       └──────────────────┘                                      │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Infrastructure all agents share:**

- Three-phase workflow: initialize, batch process, complete
- `progress.json` state management with checkpoints every 3 objects
- Docker MCP server for SAP connectivity (`mcp/mcp-launcher.sh`)
- SAP API reference data -- 30,201 APIs in `input/sap-api-reference/api-parsed.json`
- SUSG runtime statistics parsing (`agents/unused-code/parse-susg.py`)

---

## Workflow Orchestration

Today you run agents manually in sequence (README section 6). These enhancements automate that pipeline.

### Unified Assessment Orchestrator

Chain all agents into a single command: unused-code, documenter, atc-checker, then business-function-mapper.

```
┌─────────────────────────────────────────────────────────────────┐
│                  Unified Assessment Workflow                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: Package name                                             │
│                                                                  │
│  Step 1: Unused Code Discovery                                   │
│          └─ Identify candidates for deletion                     │
│          └─ Output: unused-candidates.json                       │
│                                                                  │
│  Step 2: Documentation (skip UNUSED objects)                     │
│          └─ Generate docs for USED objects only                  │
│          └─ Output: docs/*.md                                    │
│                                                                  │
│  Step 3: ATC Check (skip UNUSED objects)                         │
│          └─ Classify remaining objects by Clean Core level       │
│          └─ Output: atc/*.md                                     │
│                                                                  │
│  Step 4: Generate Unified Report                                 │
│          └─ Combine all findings                                 │
│          └─ Output: CLEAN_CORE_ASSESSMENT.md                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**What it builds on:**
- Non-interactive mode already supports automation: `kiro-cli chat --trust-all-tools --agent <name> --no-interactive "<prompt>"`
- Each agent has deterministic output paths (`reports/atc/{PKG}/`, `reports/docs/{PKG}/`, etc.)
- `business-function-mapper` already demonstrates agent chaining -- it reads from `reports/atc/` and needs no MCP connection

**Getting started:**
- Simplest approach: a shell script calling `kiro-cli chat --trust-all-tools --agent <name> --no-interactive` for each agent in sequence
- More advanced: create a new agent config at `.kiro/agents/orchestrator.json` following the pattern of `business-function-mapper.json` (no MCP needed)
- Key file to study: `agents/business-function-mapper/instructions.md` Phase 1, which checks for prerequisites from another agent

### Shared Context Between Agents

A JSON context file that accumulates findings across agent runs so downstream agents can use upstream results.

Today each agent writes isolated outputs. The business-function-mapper demonstrates a basic form of this (it reads ATC reports), but there is no formal shared state between unused-code and atc-checker.

```json
{
  "package": "ZFINANCE",
  "workflow": "full-assessment",
  "phases": {
    "unused": { "status": "complete", "candidates": 15 },
    "docs": { "status": "in_progress", "completed": 42 },
    "atc": { "status": "pending" }
  },
  "objectFilter": ["ZCL_UNUSED_1", "ZCL_UNUSED_2"]
}
```

**Getting started:**
- Create a `reports/{PKG}/context.json` that the orchestrator writes and all agents read
- Model the schema after `progress.json` but add cross-agent sections
- Each agent's `instructions.md` would add a "Load shared context" step to Phase 1

### Consolidated Assessment Report

A single unified report combining findings from all agents into one executive view. Today outputs are spread across four directories.

**What it builds on:**
- `business-function-mapper` already generates a unified executive report (`CLEAN_CORE_ASSESSMENT.md` and `.html`) using `agents/business-function-mapper/report-template.md`
- The `md-to-html.py` script already handles markdown-to-HTML conversion

**Getting started:**
- Extend the existing `report-template.md` with new sections for unused code summary and documentation coverage
- Or create a new template in an orchestrator agent directory
- Use the `generate-report.py` pattern (template + JSON data = filled report) from `agents/business-function-mapper/`

---

## New Agent Ideas

To create a new agent you need three things: a `.json` config in `.kiro/agents/`, an `instructions.md` in `agents/<name>/`, and optional Python utilities. See [Building Your Own Agent](#building-your-own-agent) below for the full recipe.

### Dependency Mapper

Visualize call graphs, detect orphans, find circular dependencies, and assess the blast radius of changes.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Dependency Mapper                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Inputs:                                                         │
│  - SUSG RDATA (runtime call relationships)                       │
│  - Static source analysis (PERFORM, CALL METHOD, etc.)           │
│  - CDS associations                                              │
│  - RAP behavior definitions                                      │
│                                                                  │
│  Outputs:                                                        │
│  - Full dependency graph (Mermaid + JSON)                        │
│  - Orphan detection (objects with no inbound calls)              │
│  - Circular dependency detection                                 │
│  - Impact analysis ("what breaks if I delete X?")                │
│  - Cluster identification (tightly coupled object groups)        │
│                                                                  │
│  Use Cases:                                                      │
│  - "Show me everything that calls ZCL_PAYMENT_PROCESSOR"         │
│  - "What's the blast radius if I change ZIF_CUSTOMER?"           │
│  - "Find all circular dependencies in package ZFINANCE"          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**What it builds on:**
- SUSG RDATA files already contain caller/called relationships (parsed by `agents/unused-code/parse-susg.py`)
- The unused-code agent already generates Mermaid dependency graphs in `VISUALIZATION.md`
- MCP tools `aws_abap_cb_get_source` and `aws_abap_cb_search_object` can supplement runtime data with static analysis

**Getting started:**
- Copy the `unused-code` agent directory structure as a template
- Reuse `parse-susg.py` output (`input/susg-parsed.json`) for runtime call relationships
- Add static source analysis by calling `aws_abap_cb_get_source` and scanning for `CALL METHOD`, `PERFORM`, `CALL FUNCTION` patterns
- Output Mermaid graph syntax following the pattern in the unused-code `VISUALIZATION.md` generation

### API Migration Assistant

Map each deprecated/internal API usage to its released successor, generate migration code snippets, and estimate effort.

The ATC checker identifies Level C/D findings but does not tell you how to fix them. This agent closes that gap with actionable migration paths.

```
┌─────────────────────────────────────────────────────────────────┐
│                  API Migration Assistant                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Inputs:                                                         │
│  - ATC findings (deprecated API usage)                           │
│  - Source code                                                   │
│  - SAP API release notes / documentation                         │
│                                                                  │
│  Capabilities:                                                   │
│  - Map deprecated API → released replacement                     │
│  - Generate migration code snippets                              │
│  - Estimate migration effort per object                          │
│  - Prioritize by usage frequency                                 │
│                                                                  │
│  Example Output:                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Finding: CALL FUNCTION 'BAPI_MATERIAL_GET_DETAIL'       │    │
│  │ Status: Not released for cloud                          │    │
│  │ Replacement: CDS View I_PRODUCT                         │    │
│  │ Migration Pattern:                                      │    │
│  │   SELECT * FROM i_product WHERE product = @lv_matnr     │    │
│  │ Effort: Low (direct replacement available)              │    │
│  │ Occurrences: 12 (across 5 objects)                      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**What it builds on:**
- SAP API reference data already contains deprecated-to-successor mappings in `input/sap-api-reference/api-parsed.json`
- `business-function-mapper` already extracts API names from ATC reports using regex (`agents/business-function-mapper/process-objects.py`, the `API_PATTERNS` list)
- MCP tool `aws_abap_cb_get_migration_analysis` already provides migration analysis data from SAP

**Getting started:**
- Create agent config based on `sap-atc-checker.json` (needs MCP for source retrieval)
- Add `aws_abap_cb_get_migration_analysis` to the `allowedTools` list
- Reuse `API_PATTERNS` regex from `agents/business-function-mapper/process-objects.py`
- Read ATC reports from `reports/atc/{PKG}/` (same prerequisite as business-function-mapper)

### Transport Analyzer

Analyze change frequency, author attribution, change coupling detection, and change velocity trends.

Frequently changed objects carry more risk during Clean Core migration. Objects that always change together should be migrated together.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Transport Analyzer                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Inputs:                                                         │
│  - Transport request data (via RFC or table access)              │
│  - Object version history                                        │
│                                                                  │
│  Capabilities:                                                   │
│  - Change frequency analysis ("hot" vs "cold" objects)           │
│  - Author/team attribution                                       │
│  - Change coupling detection (objects changed together)          │
│  - Timeline visualization                                        │
│  - Risk assessment (frequently changed = higher risk)            │
│                                                                  │
│  Use Cases:                                                      │
│  - "Which objects changed most in the last 6 months?"            │
│  - "Who owns package ZFINANCE?"                                  │
│  - "Show me objects that always change together"                 │
│  - "What's the change velocity trend for this package?"          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Getting started:**
- This agent would need access to transport-related SAP data, potentially via direct table reads or new MCP capabilities
- Model after the `unused-code` agent which also processes metadata rather than running ATC checks
- Use the same `progress.json` checkpoint pattern

### Code Quality Analyzer

Measure cyclomatic complexity, method length, class cohesion, coupling, duplication, and naming conventions. Goes beyond ATC compliance to code maintainability.

Objects that are both Level D and high-complexity should be prioritized for rewrite rather than migration.

```
┌─────────────────────────────────────────────────────────────────┐
│                   Code Quality Analyzer                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Metrics:                                                        │
│  - Cyclomatic complexity                                         │
│  - Method length distribution                                    │
│  - Class cohesion                                                │
│  - Coupling metrics                                              │
│  - Code duplication detection                                    │
│  - Naming convention compliance                                  │
│  - Comment/documentation ratio                                   │
│                                                                  │
│  Outputs:                                                        │
│  - Quality score per object (A-F grade)                          │
│  - Refactoring candidates                                        │
│  - Technical debt estimation                                     │
│  - Trend analysis over time                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Getting started:**
- Create agent config with `get_source` and `search_object` MCP tools (same as documenter -- see `.kiro/agents/sap-custom-code-documenter.json`)
- Build Python utility scripts for metrics calculation (follow the `generate-summary.py` pattern)
- Output a quality scorecard per object, similar to the per-object reports in `reports/atc/{PKG}/{NAME}_atc.md`

---

## Report Enhancements

These extend existing agent outputs without creating new agents. They modify or augment summary generation and template rendering.

### Effort Estimation for Remediation

Assign effort tiers (low/medium/high) to each Level C/D finding based on whether a successor API exists and whether the replacement is a direct swap or an architectural change.

**What it builds on:**
- `api-parsed.json` contains successor information that indicates migration complexity
- `report-template.md` already has a "Next Steps" section
- `process-objects.py` already does API lookup

**Getting started:**
- Extend `agents/business-function-mapper/process-objects.py` to assign effort tiers based on successor availability
- Add an `{{EFFORT_ESTIMATION_TABLE}}` placeholder to `report-template.md`
- Update `generate-report.py` to fill the new placeholder

### Historical Trend Tracking

Track Clean Core level distribution over time. Each completed assessment already archives `progress.json` with a timestamp prefix (`{TIMESTAMP}-progress.json`), so the data is already there.

**Getting started:**
- Create a Python utility that reads all `{timestamp}-progress.json` files in a package directory and produces a trend JSON
- Add a trend section to the executive report template
- No workflow changes needed -- the archived files are generated by design

### Risk-Based Remediation Prioritization

Combine Clean Core level, usage frequency, caller count, and business function into a risk score that prioritizes remediation order.

**What it builds on:**
- ATC level data from `reports/atc/{PKG}/`
- Usage data from `input/susg-parsed.json` (executions, callerCount)
- Business function categorization from `reports/executive/{PKG}/`

**Getting started:**
- Create a standalone Python script that reads from all three report directories
- Formula: `risk = level_weight * usage_frequency * caller_count`
- Output a prioritized remediation queue as markdown

---

## Integration Opportunities

### CI/CD Pipeline Integration

Run agents automatically on schedule or triggered by transport creation.

Non-interactive mode already supports this: `kiro-cli chat --trust-all-tools --agent <name> --no-interactive "<prompt>"`. Wrap the command in a GitHub Actions workflow or Jenkins pipeline. Parse the generated `SUMMARY.md` to extract level counts and fail the pipeline if Level D exceeds a threshold.

### Issue Tracker Generation

Automatically create GitHub or GitLab issues from Level C/D findings. The ATC reports at `reports/atc/{PKG}/{NAME}_atc.md` contain structured finding data. A Python script could read `progress.json` and use `gh issue create` to generate one issue per Level D object, with labels based on Clean Core level and business function.

### Web Dashboard

An HTML/JS viewer for browsing all reports with filtering, sorting, and interactive dependency graphs. The `business-function-mapper` already generates HTML via `agents/business-function-mapper/md-to-html.py`. Start with a static site generator that reads the `reports/` directory and add client-side filtering.

### Multi-System Comparison

Run the same assessment against DEV, QA, and PROD systems and compare results. Use environment-specific config files (`mcp/sap-dev.env`, `mcp/sap-qa.env`) and environment-specific output directories (`reports/atc/{PKG}-DEV/`, `reports/atc/{PKG}-PROD/`). A comparison script would diff level distributions across systems.

### Incremental Processing

Only re-analyze objects that changed since the last assessment run. Archived `{timestamp}-progress.json` files already record which objects were analyzed and when. On re-run, compare the new object list from SAP search against the archived progress and only add new or modified objects to the pending list.

---

## Building Your Own Agent

### Step 1: Create the agent config

Create `.kiro/agents/<name>.json`. Use `business-function-mapper.json` as a template if no MCP needed, or `sap-atc-checker.json` if SAP connectivity is required.

```json
{
  "name": "<agent-name>",
  "description": "<one-line description>",
  "prompt": "file://../../agents/<agent-name>/instructions.md",
  "mcpServers": {},
  "tools": ["read", "write", "shell", "todo", "introspect", "knowledge"],
  "allowedTools": ["read", "write", "shell", "todo", "introspect", "knowledge"],
  "resources": ["file://AGENTS.md"],
  "hooks": {},
  "toolsSettings": {},
  "model": "claude-opus-4.5"
}
```

Add MCP tools to `mcpServers`, `tools`, and `allowedTools` if the agent needs SAP access.

### Step 2: Write the instructions

Create `agents/<name>/instructions.md` following the three-phase structure in any existing agent:

- Agent Configuration section (model, state file, resume capability)
- Quick Reference (MCP tools used, scripts, constants)
- Boundaries (Always Do / Never Do)
- Workflow (Phase 1: Initialization, Phase 2: Processing, Phase 3: Completion)
- Templates for output files
- Error handling table
- Resume capability section

### Step 3: Create Python utilities

Follow the patterns in existing scripts:

- `agents/atc-checker/generate-summary.py` -- summary generation from progress.json
- `agents/business-function-mapper/process-objects.py` -- batch processing with regex extraction
- `agents/unused-code/parse-susg.py` -- input data parsing

### Step 4: Create output directory

Follow the convention: `reports/<type>/{PKG}/`

---

## Design Principles

Patterns extracted from the existing agents. Follow these when extending the platform.

1. **Three-phase workflow.** Every batch agent follows init, process, complete. This keeps agents resumable and predictable.

2. **progress.json is the source of truth.** All state lives in one JSON file per run. No database, no external services. Checkpoint every BATCH_SIZE (3) objects.

3. **File system reconciliation on resume.** After a crash or context overflow, reconcile actual files on disk with progress.json before resuming. If a file exists but progress says "pending", mark it completed.

4. **Least privilege tool access.** Specialized agents get only the MCP tools they need. Only the accelerator gets full access. See `docs/SECURITY.md`.

5. **Reports go to disk immediately.** Write each object's report file before updating progress.json. If the checkpoint fails, the file still exists and reconciliation catches it.

6. **Python scripts for deterministic operations.** Summary generation, data parsing, and report rendering use Python scripts, not LLM generation. The LLM calls the scripts.

7. **Consistent output structure.** Reports follow `reports/<type>/{PKG}/{NAME}_<suffix>.md` naming. Summaries are always `SUMMARY.md`.
