# Accelerate your SAP Clean Core journey with Kiro Agents

AI-powered agents for SAP custom code analysis: Clean Core compliance, documentation generation, unused code discovery, and executive reporting.

## Table of Contents

1. [Why clean core?](#1-why-clean-core)
2. [Architecture](#2-architecture)
3. [Prerequisites](#3-prerequisites)
4. [Setup](#4-setup)
5. [Quick start](#5-quick-start)
6. [Troubleshooting](#6-troubleshooting)
7. [Security configuration guide](#7-security-configuration-guide)
8. [Documentation & references](#8-documentation--references)

---

## 1. Why clean core?

SAP Clean Core is about decoupling custom extensions from SAP standard code through ABAP Cloud and reliable development technologies. The goal is upgrade stability -- keeping your S/4HANA system maintainable and cloud-ready as SAP evolves. Custom code that depends on internal SAP objects creates upgrade risk; Clean Core governance quantifies and reduces that risk.

The [Clean Core Extensibility whitepaper](https://www.sap.com/documents/2024/09/20aece06-d87e-0010-bca6-c68f7e60039b.html) defines four compliance levels:

| Level | ATC Result | What it means | Action |
|-------|-----------|---------------|--------|
| **A** | No findings | Fully compliant with Clean Core | Cloud-ready, no action needed |
| **B** | Info only | Uses documented extension points | Acceptable, low upgrade risk |
| **C** | Warnings | Uses internal or undocumented APIs | Conditionally clean, verify before upgrades |
| **D** | Errors | Non-released APIs, modifications, or blocked patterns | Requires remediation |

These agents automate the assessment. The `sap-atc-checker` runs ATC checks against your custom code and classifies every Z* object into Levels A-D. From there, `business-function-mapper` generates executive summaries, `sap-custom-code-documenter` produces developer and business documentation, and `sap-unused-code-discovery` identifies dead code you can remove before starting remediation.

---

## 2. Architecture

Kiro CLI agents connect to SAP through a Python-based MCP server running locally.

```
┌─────────────────────────────┐      ┌──────────────┐          ┌────────────┐
│      Kiro CLI Agents        │      │  MCP Server  │          │ SAP System │
│                             │ HTTP │   (Python)   │ ADT API  │            │
│  Instructions   Scripts     │◄────►│    ABAP      │◄────────►│  S/4HANA   │
│   (Text)       (Python)     │      │ Accelerator  │          │            │
└─────────────────────────────┘      └──────────────┘          └────────────┘
```

1. **Kiro CLI agents**: Five specialized agents run locally within a security boundary. Each agent has text-based instructions and optional Python scripts for local processing (report generation, data parsing).

2. **MCP server**: The [SAP ABAP Accelerator](https://github.com/aws-solutions-library-samples/guidance-for-deploying-sap-abap-accelerator-for-amazon-q-developer) runs as a local Python HTTP server on port 8001, providing SAP connectivity to Kiro CLI agents via the Model Context Protocol.

3. **SAP system**: Target SAP ECC or S/4HANA system where ABAP code resides.

---

## 3. Prerequisites

These agents connect to SAP through the [SAP ABAP Accelerator](https://github.com/aws-solutions-library-samples/guidance-for-deploying-sap-abap-accelerator-for-amazon-q-developer) MCP server. Verify the following before setup.

### 3.1 System requirements

| Requirement | Verification | Install |
|-------------|--------------|---------|
| Python 3.11+ | `python3 --version` | Your package manager |
| Kiro-CLI | `kiro-cli --version` | [Kiro CLI](https://kiro.dev/docs/cli/) |

**AI model:** All agents are configured to use `claude-opus-4.5`. You can change this by editing the `"model"` field in each agent config file under `.kiro/agents/*.json`. See [Kiro CLI docs](https://kiro.dev/docs/cli/) for supported model values.

### 3.2 SAP system requirements

Verify these in SAP:

| Requirement | What/How to verify |
|-------------|---------------|
| S/4HANA 2023 or 2025 (Central System) | System information & [Note Analyzer (SAP-NOTE-3627152-CENTRAL.xml)](https://me.sap.com/notes/3627152) |
| Checked system (e.g., ECC) | [Note Analyzer (SAP-NOTE-3627152-CHECKED.xml)](https://me.sap.com/notes/3627152) |
| CLEAN_CORE variant exists | Transaction `ATC` > Manage Check Variants > Search for `CLEAN_CORE` or similar |
| ADT services enabled | `curl https://<host>/sap/bc/adt/discovery` returns XML |
| User has ATC authorization | Authorization objects: `S_ATC_*`, `S_DEVELOP` |
| Custom code exists (Z*) | Transaction `SE80` > Your package |

**If CLEAN_CORE variant does not exist:** The variant may be named differently in your system (e.g., `CLEAN_CORE_LOCAL`, `Z_CLEAN_CORE`). Check with your ATC administrator for the correct variant name. If no Clean Core variant exists at all, create one via transaction `ATC` > Manage Check Variants. Without it, ATC checks use system defaults and will not assess Clean Core compliance. See [SAP Note 3565942](https://me.sap.com/notes/3565942) for details.

Alternatively, Clean Core checks support a Central ATC configuration where one check system serves multiple SAP systems. See [Remote Code Analysis in ATC](https://community.sap.com/t5/technology-blog-posts-by-sap/remote-code-analysis-in-atc-one-central-check-system-for-multiple-systems/ba-p/13307811) for setup details and pre-requisites.

---

## 4. Setup

Steps to configure the SAP connection and verify everything works.

### 4.1 Clone and install MCP server

```bash
git clone https://github.com/aws-solutions-library-samples/guidance-for-accelerating-sap-clean-core-journey-using-kiro-agents clean-core
cd clean-core
cp mcp/sap.env.example mcp/sap.env

# Clone and set up MCP server
git clone https://github.com/aws-solutions-library-samples/guidance-for-deploying-sap-abap-accelerator-for-amazon-q-developer aws-abap-accelerator-http
cd aws-abap-accelerator-http
python3.11 -m venv venv              # Create isolated Python environment
venv/bin/pip install -r requirements.txt  # Install MCP server dependencies
cd ..  # Return to clean-core directory
```

### 4.2 Configure SAP connection

Edit `mcp/sap.env` with your SAP connection details:
```
SAP_SID=A4H
SAP_DESCRIPTION=Dev System
SAP_HOST=sap.example.com:8000
SAP_CLIENT=001
SAP_USERNAME=youruser
SAP_LANGUAGE=EN
SAP_SECURE=true
```

### 4.3 Set SAP password

Add your SAP password to `secrets/sap_password` (the file must contain only the password, no trailing newline):

```bash
echo -n "yourpassword" > secrets/sap_password
chmod 600 secrets/sap_password
```

### 4.4 Verify setup

```bash
./check-setup.sh
```

All checks should pass. If any fail, see [Troubleshooting](#6-troubleshooting).

**Options:**
```bash
./check-setup.sh --quiet            # Silent mode, exit code only
./check-setup.sh --json             # JSON output
./check-setup.sh --verbose          # Extra detail

# To test SAP connectivity, start the MCP server first:
./mcp/mcp-launcher.sh &
./check-setup.sh --test-connection
```

---

## 5. Quick start

Run agents interactively or in scripted mode.

### 5.1 Start the MCP server

Before running any agent, start the MCP server in a separate terminal:

```bash
./mcp/mcp-launcher.sh
```

The server runs on `http://localhost:8001/mcp`. Keep it running while using agents.

### 5.2 Run an agent (interactive)

Start any agent with `kiro-cli --agent <name>` and type your prompt:

| Agent | Command | Example prompt | Requires |
|-------|---------|----------------|----------|
| **sap-atc-checker** | `kiro-cli --agent sap-atc-checker` | `"Check package ZFLIGHT"` | - |
| **sap-custom-code-documenter** | `kiro-cli --agent sap-custom-code-documenter` | `"Document package ZFLIGHT"` | - |
| **sap-unused-code-discovery** | `kiro-cli --agent sap-unused-code-discovery` | `"Analyze package ZFLIGHT"` | SUSG data in `input/` |
| **business-function-mapper** | `kiro-cli --agent business-function-mapper` | `"Map findings for ZFLIGHT"` | sap-atc-checker output |
| **abap-accelerator** | `kiro-cli --agent abap-accelerator` | `"Search for Z* classes"` | - |

> **Recommended order:** Run `sap-atc-checker` first. Its output in `reports/atc/` is required by `business-function-mapper` and useful context for other agents. For `sap-unused-code-discovery`, export SUSG data from SAP first -- SAP recommends collecting usage data for 6-18 months before export to improve accuracy (see [Usage Data Collection](https://help.sap.com/docs/ABAP_PLATFORM_NEW/ba879a6e2ea04d9bb94c7ccd7cdac446/ca200f7002394c809d90873e19e5ac84.html)).

### 5.3 Non-interactive mode

For automation and scripting, pass the prompt directly:

```bash
kiro-cli chat --trust-all-tools --agent sap-atc-checker --no-interactive "Check package ZFLIGHT"
```

Append `&` to run in the background:

```bash
kiro-cli chat --trust-all-tools --agent sap-atc-checker --no-interactive "Check package ZFLIGHT" &
```

**Resume interrupted sessions:** Run the same command again. Agents auto-detect `progress.json` and continue where they left off.

### 5.4 Output

Agents write reports to the `reports/` directory, organized by type and package:

| Agent | Output location |
|-------|-----------------|
| sap-atc-checker | `reports/atc/<PACKAGE>/` |
| sap-custom-code-documenter | `reports/docs/<PACKAGE>/` |
| sap-unused-code-discovery | `reports/unused/<PACKAGE>/` |
| business-function-mapper | `reports/executive/<PACKAGE>/` |

Each directory contains individual object reports and a `SUMMARY.md` with an overview.

### 5.5 Working with results

- **Identify non-compliance patterns**: Look across reports for recurring findings -- the same internal API used in multiple objects, common Level D violations, or groups of objects that need the same fix. Fixing by pattern is faster than going object by object.
- **Use reports as a knowledge base**: Feed generated reports into a Gen AI assistant to query your findings -- "which objects depend on CL_GUI_ALV_GRID?", "what are the most common Level D findings?", "draft a remediation plan for these objects."

---

## 6. Troubleshooting

Common issues and how to resolve them.

| Problem | Solution |
|---------|----------|
| MCP server not running | Start with `./mcp/mcp-launcher.sh` in a separate terminal |
| Connection refused on port 8001 | MCP server not started or crashed -- check terminal output |
| Permission denied | `chmod 600 secrets/sap_password` and `chmod 600 mcp/sap.env` |
| SAP connection fails | Check `mcp/sap.env` values and network |
| Agent not found | Run from `clean-core` directory |
| Context overflow | Restart agent, say "Resume" |
| ATC variant error | Verify a Clean Core variant exists in SAP (see [section 3.2](#32-sap-system-requirements)) |

**Debug SAP connection:**
```bash
# Start MCP server first
./mcp/mcp-launcher.sh &

# Then test connection
./check-setup.sh --test-connection
curl -v https://<SAP_HOST>/sap/bc/adt/discovery    # use http:// if SAP_SECURE=false
```

---

## 7. Security configuration guide

Recommended actions to secure your environment before running agents.

### 7.1 Enforce TLS for SAP connections

Set `SAP_SECURE=true` in `mcp/sap.env` to encrypt all traffic between the MCP server and SAP. Without TLS, SAP credentials and source code transit the network in cleartext.

### 7.2 Secure SAP credentials

- Set file permissions: `chmod 600 mcp/sap.env` and `chmod 600 secrets/sap_password`
- Use a SAP developer account with the appropriate access -- avoid sharing credentials
- Verify credentials are git-ignored: `git ls-files --error-unmatch mcp/sap.env` should return an error
- Rotate SAP passwords according to your organization's policy

### 7.3 Assign SAP authorizations (least privilege)

- Read-only agents (atc-checker, documenter, unused-code) need only display access -- do not grant change or create permissions
- The abap-accelerator agent requires full development access -- restrict to trusted users only
- Limit authorization scope to only the packages agents need to access

### 7.4 Enable Kiro audit logging

- Enable Kiro prompt logging and Kiro user activity report in your AWS account
- Review logs periodically for unexpected access patterns

### 7.5 Secure generated reports

- Reports in `reports/` may contain SAP source code and internal API details
- Restrict access to the `reports/` directory to authorized users
- Do not commit reports to public repositories

### 7.6 Limit SAP connections per client IP

- Run only a few agents in parallel to avoid exhausting SAP work processes or dialog sessions
- Configure the SAP Web Dispatcher or ICM to limit connections per client IP -- see [Limit Connections per Client IP](https://help.sap.com/docs/ABAP_PLATFORM_BW4HANA/683d6a1797a34730a6e005d1e8de6f22/fa9ad653a77949c79dd8cbea83d5cb8f.html) for an example using `icm/client_ip_connection_limit`

### 7.7 Download API reference data directly from SAP

- Download API classification files in `input/` from the official [SAP/abap-atc-cr-cv-s4hc](https://github.com/SAP/abap-atc-cr-cv-s4hc) GitHub repository
- Verify file integrity after download -- tampered reference data can produce incorrect compliance assessments

---

## 8. Documentation & references

Detailed guides and external references.

### 8.1 Documentation

- [Agent Guide](docs/agent-guide.md) - Detailed agent capabilities, commands, and usage
- [Enhancement Guide](docs/enhancement-guide.md) - Ideas for extending and customizing agents
- [Security Model](docs/SECURITY.md) - Agent permissions and credential handling

### 8.2 References

- [ABAP Extensibility Guide - Clean Core (August 2025)](https://community.sap.com/t5/technology-blog-posts-by-sap/abap-extensibility-guide-clean-core-for-sap-s-4hana-cloud-august-2025/ba-p/14175399)
- [ATC Cloud Readiness Check Variants for S/4HANA Cloud](https://github.com/SAP/abap-atc-cr-cv-s4hc) - API classification data used by ATC checks
- [Clean Core Extensibility Whitepaper](https://www.sap.com/documents/2024/09/20aece06-d87e-0010-bca6-c68f7e60039b.html)
- [Usage Data Collection](https://help.sap.com/docs/ABAP_PLATFORM_NEW/ba879a6e2ea04d9bb94c7ccd7cdac446/ca200f7002394c809d90873e19e5ac84.html)


## Notices
Customers are responsible for making their own independent assessment of the information in this Guidance. This Guidance: (a) is for informational purposes only, (b) represents AWS current product offerings and practices, which are subject to change without notice, and (c) does not create any commitments or assurances from AWS and its affiliates, suppliers or licensors. AWS products or services are provided “as is” without warranties, representations, or conditions of any kind, whether express or implied. AWS responsibilities and liabilities to its customers are controlled by AWS agreements, and this Guidance is not part of, nor does it modify, any agreement between AWS and its customers.
