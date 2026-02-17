# ABAP Accelerator Agent

Full-featured SAP ABAP development assistant with unrestricted tool access.

## Configuration

| Setting | Value |
|---------|-------|
| Model | Claude Opus 4.5 |

## Quick Start

```bash
kiro-cli --agent abap-accelerator

> "Find all classes in ZFLIGHT"
> "Get source code for ZCL_MY_CLASS"
> "Run ATC check on ZPROGRAM"
> "Help me write a new report"
```

## Why Use This Agent?

| Feature | Specialized Agents | ABAP Accelerator |
|---------|-------------------|------------------|
| Tool Access | Limited to task | All tools |
| Approval Prompts | Some required | None |
| Flexibility | Task-specific | Unrestricted |
| Use Case | Focused workflows | Ad-hoc tasks |

## Available Tools

### SAP MCP Tools
| Tool | Description |
|------|-------------|
| `connection_status` | Check SAP connection |
| `run_atc_check` | Execute ATC checks |
| `search_object` | Find ABAP objects |
| `get_objects` | List package objects |
| `get_source` | Retrieve source code |

### File & System
| Tool | Description |
|------|-------------|
| `read` | Read files |
| `write` | Create/edit files |
| `bash` | Shell commands |
| `glob` | File patterns |
| `grep` | Content search |
| `web` | Fetch URLs |

## Example Use Cases

### 1. Quick Lookups
```
"What objects are in package ZFLIGHT?"
"Show me the source of ZCL_ORDER_PROCESSOR"
"Search for classes containing 'ORDER'"
```

### 2. Code Analysis
```
"Run ATC check on ZCL_MY_CLASS"
"Find all usages of BAPI_SALESORDER_CREATEFROMDAT2"
"Check this code for Clean Core compliance"
```

### 3. Development Help
```
"Help me write a class to process IDocs"
"How do I implement IF_HTTP_EXTENSION?"
"Convert this classic ABAP to modern syntax"
```

### 4. Documentation
```
"Document this function module"
"Create a README for this package"
"Generate a class diagram for ZPACKAGE"
```

### 5. Ad-hoc Tasks
```
"Parse this XML file and extract data"
"Create a script to process SUSG exports"
"Help me debug this ABAP error"
```

## Comparison with Other Agents

| Agent | Purpose | Restrictions |
|-------|---------|--------------|
| `sap-atc-checker` | ATC compliance | ATC tools only |
| `sap-custom-code-documenter` | Documentation | Doc tools only |
| `sap-unused-code-discovery` | Find unused code | SUSG analysis |
| **`abap-accelerator`** | **Everything** | **None** |

## When to Use

**Use ABAP Accelerator when:**
- Task doesn't fit a specialized agent
- You need multiple capabilities combined
- Ad-hoc or exploratory work
- Custom automation scripts
- Complex multi-step operations

**Use specialized agents when:**
- Focused on specific workflow (ATC, docs, unused)
- Want guided step-by-step process
- Processing large packages (progress tracking)

## Prerequisites

Same as other agents:
1. SAP connection configured in `mcp/sap.env`
2. MCP server running (auto-started by agent)

## Output

Reports and files can be saved anywhere, but recommended locations:
- `reports/` - Analysis reports
- `output/` - Generated artifacts
