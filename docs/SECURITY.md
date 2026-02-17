# Security Model

The SAP Clean Core Platform implements a **restricted access model** where specialized agents have limited tool access based on their specific purpose, following the principle of least privilege.

---

## Overview

- **4 specialized agents** with restricted MCP tool access (3 tools each max)
- **1 unrestricted agent** (abap-accelerator) with full access to all tools
- Credentials stored locally, never committed to git
- Batch processing with local state management

---

## Agent Access Matrix

### MCP Tool Access

| MCP Tool | atc-checker | documenter | unused-code | biz-mapper | accelerator |
|----------|:-----------:|:----------:|:-----------:|:----------:|:-----------:|
| `connection_status` | YES | YES | YES | - | YES |
| `search_object` | YES | YES | YES | - | YES |
| `run_atc_check` | YES | - | - | - | YES |
| `get_source` | - | YES | YES | - | YES |
| `get_objects` | - | - | - | - | YES |
| `create_object` | - | - | - | - | YES |
| `update_source` | - | - | - | - | YES |
| `check_syntax` | - | - | - | - | YES |
| `activate_object` | - | - | - | - | YES |
| `run_unit_tests` | - | - | - | - | YES |

### System Tool Access

| Tool | atc-checker | documenter | unused-code | biz-mapper | accelerator |
|------|:-----------:|:----------:|:-----------:|:----------:|:-----------:|
| read | YES | YES | YES | YES | YES |
| write | YES | YES | YES | YES | YES |
| shell | YES | YES | YES | YES | YES |
| glob | - | - | - | - | YES |
| grep | - | - | - | - | YES |
| bash | - | - | - | - | YES |
| web | - | - | - | - | YES |

---

## Security Implications

### Restricted Agents (4 agents)

**sap-atc-checker, sap-custom-code-documenter, sap-unused-code-discovery, business-function-mapper**

- Limited to 3 MCP tools maximum per agent
- **Cannot** create, modify, or activate SAP objects
- **Cannot** run unit tests
- **Cannot** access web resources
- Safe for compliance and documentation workflows
- Suitable for read-only analysis tasks

### Unrestricted Agent (1 agent)

**abap-accelerator**

- Full access to all MCP tools via `@sap-abap-accelerator/*`
- **Can** create, modify, and activate SAP objects
- **Can** run unit tests with coverage
- **Can** access web resources and execute shell commands
- Use with caution - appropriate for trusted users and development tasks

---

## Credential Security

### File Locations

| File | Purpose | Recommended Permissions |
|------|---------|------------------------|
| `mcp/sap.env` | SAP connection settings | 600 (owner read/write only) |
| `secrets/sap_password` | SAP password | 644 (Docker needs read access) |

### Git Security

The following are in `.gitignore` and should **NEVER** be committed:

```
mcp/sap.env
secrets/sap_password
secrets/*
```

Verify nothing is tracked:
```bash
git ls-files --error-unmatch mcp/sap.env 2>&1 | grep -q "error" && echo "Safe"
git ls-files --error-unmatch secrets/sap_password 2>&1 | grep -q "error" && echo "Safe"
```

---

## Batch Processing Security

### Checkpointing Model

All batch-processing agents use a checkpoint model:
- Progress saved every 3 objects (BATCH_SIZE)
- State stored in local `progress.json`
- Automatic recovery after context overflow or crash
- No sensitive data in progress files

### Data Residency

| Data Type | Storage Location | Transmitted To |
|-----------|------------------|----------------|
| SAP credentials | Local files only | SAP system via MCP |
| Source code | Fetched to local | Never transmitted out |
| ATC results | Local files | Never transmitted out |
| Generated reports | Local files | Never transmitted out |
| Progress state | Local JSON | Never transmitted |

---

## Recommendations

### For Compliance Workflows

Use specialized agents (`sap-atc-checker`, `sap-custom-code-documenter`, etc.) which have restricted access and cannot modify SAP systems.

### For Development Tasks

Use `abap-accelerator` with caution. This agent can:
- Create new ABAP objects
- Modify existing source code
- Activate objects
- Run unit tests

Consider restricting access to users with appropriate SAP development authorizations.

### For Automation

When using `--trust-all-tools`:
- Only use with agents you trust
- Consider running in isolated environments
- Review generated reports before acting on recommendations
- Monitor SAP security audit logs

### For Multi-User Environments

- Each user should have their own `secrets/sap_password`
- Consider using SAP technical user accounts with appropriate authorizations
- Implement SAP-side authorization controls (S_ATC_*, S_DEVELOP)
- Review SAP security audit logs for automated access patterns

---

## SAP Authorization Requirements

### Base Requirements (All SAP-Connected Agents)

All agents that connect to SAP require:
- **S_RFC** - Remote Function Call authorization for ADT connectivity
- Network access to SAP host on configured port

### Per-Agent Requirements

| Agent | SAP Operations | Required Authorizations |
|-------|----------------|------------------------|
| sap-atc-checker | Run ATC checks, search objects | S_DEVELOP (display), ATC execution rights |
| sap-custom-code-documenter | Read source code, search objects | S_DEVELOP (display) |
| sap-unused-code-discovery | Search objects, read source (optional) | S_DEVELOP (display) - only for online mode |
| business-function-mapper | None - reads local files only | None |
| abap-accelerator | Full development operations | S_DEVELOP (full), S_TADIR, S_TCODE |

### Authorization Details

**S_DEVELOP** - Main development authorization object controlling:
- ACTVT 02 (Change) - Modify source code
- ACTVT 03 (Display) - Read source code
- OBJTYPE - Object types (PROG, CLAS, FUNC, etc.)
- DEVCLASS - Package restrictions

**ATC Execution** - Running ATC checks typically requires:
- S_DEVELOP with display access to objects being checked
- ATC variant execution rights (may be controlled by custom authorization objects in your system)

**Note:** Exact authorization objects may vary by SAP release and system configuration. Consult your SAP Basis team for system-specific requirements.

---

## SAP Connection Throttling

Running multiple agents concurrently — particularly in scripted or background mode — can generate many simultaneous ADT/RFC connections through the MCP server, potentially exhausting SAP work process limits or dialog sessions.

- Run only a few agents in parallel against the same SAP system
- Configure connection limits per client IP on whichever component accepts client connections — SAP Web Dispatcher, ICM, an AWS load balancer, or another reverse proxy. For SAP Web Dispatcher, see the [`icm/client_ip_connection_limit`](https://help.sap.com/docs/ABAP_PLATFORM_BW4HANA/683d6a1797a34730a6e005d1e8de6f22/fa9ad653a77949c79dd8cbea83d5cb8f.html) parameter as an example
- Monitor connection usage in SAP Web Dispatcher Administration UI under **Menu > Core System > Client IP Top Consumer**

---

## Reporting Security Issues

If you discover a security vulnerability, please report it via GitHub Issues with the `security` label, or contact the repository maintainers directly.
