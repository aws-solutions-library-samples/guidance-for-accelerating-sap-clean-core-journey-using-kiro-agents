# SAP API Reference Data

This directory contains SAP API reference data used by the Business Function Mapper agent to classify custom ABAP objects by business area.

## Directory Contents

| File | Source | Purpose |
|------|--------|---------|
| `objectReleaseInfoLatest.json` | SAP GitHub | Deprecated APIs with successors |
| `objectClassifications_SAP.json` | SAP GitHub | API classifications by application component |
| `objectClassifications_3TierModel.json` | SAP GitHub | 3-tier model classifications |
| `objectReleaseInfo_BTPLatest.json` | SAP GitHub | BTP-specific release info |
| `objectClassifications.json` | SAP GitHub | Base classifications |
| `api-parsed.json` | **Generated** | Combined lookup index (30,201 APIs) |
| `custom-mappings.json` | **User-created** | Custom API mappings (optional) |
| `CATALOG.md` | **Generated** | Human-readable API catalog |

## Updating SAP Reference Data

SAP updates these files quarterly. To get the latest data:

```bash
cd input/sap-api-reference

# Download latest from SAP GitHub
curl -L -o objectReleaseInfoLatest.json \
  https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfoLatest.json

curl -L -o objectClassifications_SAP.json \
  https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectClassifications_SAP.json

curl -L -o objectClassifications_3TierModel.json \
  https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectClassifications_3TierModel.json

curl -L -o objectReleaseInfo_BTPLatest.json \
  https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_BTPLatest.json

curl -L -o objectClassifications.json \
  https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectClassifications.json

# Re-parse to update api-parsed.json
python3 agents/business-function-mapper/parse-api-refs.py \
  input/sap-api-reference \
  input/sap-api-reference/api-parsed.json

# Regenerate catalog
python3 agents/business-function-mapper/generate-catalog.py
```

## Adding Custom Mappings

To add custom API-to-business-function mappings, edit `custom-mappings.json`:

```json
{
  "customMappings": {
    "ZCUSTOM_TABLE": {
      "businessFunction": "Finance (FI)",
      "applicationComponent": "FI-GL",
      "state": "custom",
      "notes": "Custom GL extension table"
    },
    "ZCL_MY_CLASS": {
      "businessFunction": "Sales & Distribution (SD)",
      "applicationComponent": "SD-SLS",
      "state": "custom",
      "notes": "Custom sales processing class"
    }
  }
}
```

Custom mappings take priority over SAP reference data.

## Business Function Reference

| Prefix | Business Function |
|--------|-------------------|
| FI | Finance |
| CO | Controlling |
| SD | Sales & Distribution |
| MM | Materials Management |
| PP | Production Planning |
| PM | Plant Maintenance |
| QM | Quality Management |
| PS | Project Systems |
| HR/HCM | Human Capital Management |
| BC | Basis Components |
| CA | Cross-Application |
| LO | Logistics General |
| LE | Logistics Execution |
| TR | Treasury |
| RE | Real Estate |

## Source Repository

SAP maintains the official API reference data at:
https://github.com/SAP/abap-atc-cr-cv-s4hc

## See Also

- `CATALOG.md` - Human-readable catalog of all available APIs
- `agents/business-function-mapper/instructions.md` - Agent workflow documentation
