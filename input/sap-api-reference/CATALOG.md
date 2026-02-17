# SAP API Reference Catalog

## Overview

- **Total APIs**: 30,201
- **Last Updated**: 2025-12-10 20:16
- **Source**: github.com/SAP/abap-atc-cr-cv-s4hc

### API States

| State | Count | Description |
|-------|-------|-------------|
| released | 25,056 | Officially released and supported |
| classicAPI | 3,734 | Legacy API, plan migration |
| notToBeReleased | 452 | Will not be released publicly |
| deprecated | 431 | Being retired by SAP |
| notToBeReleasedStable | 421 |  |
| noAPI | 107 | Internal, not for external use |

### Object Types

| Type | Count | Description |
|------|-------|-------------|
| DDLS | 7,405 | CDS View |
| TABL | 5,756 | Database Table |
| DTEL | 5,113 | Data Element |
| INTF | 4,349 | Interface |
| CLAS | 2,922 | ABAP Class |
| TTYP | 1,674 | Table Type |
| FUGR | 1,172 | Function Group |
| ENHS | 609 |  |
| SUSO | 482 |  |
| IWSV | 207 |  |
| SIA2 | 125 |  |
| CHKO | 80 |  |
| DOMA | 69 | Domain |
| RONT | 59 |  |
| G4BA | 36 |  |

---

## Business Functions

| Business Function | Total | Deprecated | Classic | Tables | Classes |
|-------------------|-------|------------|---------|--------|---------|
| Cross-Application | 7,354 | 4 | 126 | 3776 | 108 |
| Basis Components | 6,936 | 167 | 2552 | 172 | 2512 |
| Finance | 3,740 | 19 | 113 | 646 | 62 |
| Materials Management | 2,259 | 195 | 9 | 501 | 20 |
| Other (FS) | 1,189 | 0 | 76 | 0 | 7 |
| Sales & Distribution | 1,137 | 9 | 10 | 140 | 5 |
| Other (FIN) | 1,105 | 10 | 61 | 27 | 4 |
| Logistics General | 977 | 6 | 55 | 122 | 9 |
| Production Planning | 707 | 0 | 12 | 30 | 9 |
| Other (EHS) | 628 | 1 | 3 | 223 | 41 |
| Industry Solutions | 418 | 0 | 65 | 0 | 6 |
| Customer Relationship Management | 375 | 3 | 6 | 6 | 2 |
| Transportation Management | 362 | 0 | 0 | 0 | 0 |
| Quality Management | 355 | 0 | 10 | 14 | 9 |
| Other (OPU) | 291 | 0 | 213 | 0 | 50 |
| Plant Maintenance | 286 | 2 | 33 | 4 | 2 |
| Logistics Execution | 229 | 0 | 10 | 20 | 0 |
| Controlling | 218 | 4 | 25 | 21 | 2 |
| Other (CM) | 199 | 1 | 0 | 25 | 1 |
| Other (PPM) | 195 | 4 | 14 | 0 | 0 |
| Real Estate | 193 | 0 | 30 | 0 | 9 |
| Supply Chain Management | 165 | 5 | 26 | 0 | 2 |
| Personnel Administration | 148 | 0 | 145 | 0 | 28 |
| Other (AP) | 147 | 0 | 11 | 0 | 0 |
| Other (SLC) | 104 | 0 | 0 | 0 | 0 |
| Other (PSM) | 84 | 0 | 35 | 1 | 3 |
| Other (SUS) | 71 | 0 | 0 | 7 | 13 |
| Enterprise Controlling | 51 | 0 | 2 | 4 | 0 |
| Other (BNS) | 46 | 0 | 0 | 16 | 0 |
| Other (PY) | 41 | 0 | 40 | 0 | 4 |
| Product Lifecycle Management | 35 | 1 | 0 | 1 | 0 |
| Other (AC) | 33 | 0 | 3 | 0 | 0 |
| Other (MOB) | 25 | 0 | 0 | 0 | 0 |
| Other (PT) | 21 | 0 | 20 | 0 | 3 |
| Project Systems | 17 | 0 | 15 | 0 | 0 |
| Business Warehouse | 17 | 0 | 4 | 0 | 9 |
| Other (XX) | 17 | 0 | 0 | 0 | 0 |
| Other (FT) | 11 | 0 | 0 | 0 | 0 |
| Other (LOD) | 5 | 0 | 1 | 0 | 0 |
| Other (ICM) | 4 | 0 | 4 | 0 | 1 |
| Investment Management | 4 | 0 | 3 | 0 | 0 |
| Other (HAN) | 1 | 0 | 1 | 0 | 1 |
| Other (PE) | 1 | 0 | 1 | 0 | 0 |

---

### Cross-Application

**Total APIs**: 7,354

**Application Components**: CA-, CA-ATP, CA-BFA, CA-BK, CA-CL, CA-CPD, CA-DI, CA-DMS, CA-DT, CA-EPT
  ...and 16 more

**By Type**:
- TABL: 3776
- DTEL: 1982
- TTYP: 620
- DDLS: 439
- INTF: 197

**By State**:
- released: 7155
- classicAPI: 126
- notToBeReleasedStable: 66
- deprecated: 4
- noAPI: 2
- notToBeReleased: 1

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| IF_EDOC_IT_ARCHIVE | INTF | - |
| IF_J3RL_NOTICE_UPLOAD | INTF | - |
| I_JVAJOINTOPERATINGAGRMTDETAIL | DDLS | I_JVAJOINTOPERATINGAGRMTDET_2 |
| I_JVAVENTURECOSTOBJECTDETAILS | DDLS | I_JVAVENTURECOSTOBJECTDETS_2 |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /APE/CL_PROC | CLAS | classicAPI | CA-GTF-APE |
| /BA1/F4_DTE_MDCODE | DTEL | released | CA-FS-MKD |
| /BA1/F4_FX_BAPI | FUGR | classicAPI | CA-FS-MKD |
| /BA1/F4_IR_BAPI | FUGR | classicAPI | CA-FS-MKD |
| /BA1/F4_SEC_BAPI | FUGR | classicAPI | CA-FS-MKD |
| /BA1/F4_VOLA_BAPI | FUGR | classicAPI | CA-FS-MKD |
| /BCV/CL_AUT_AUTHORIZATION | CLAS | classicAPI | CA-EPT-BCV |
| /BOBF/TXC_TEXT_TYPE | DTEL | released | CA-EPT-BRC |
| /BOBF/USER_ID_CH | DTEL | released | CA-EPT-BRC |
| /BOBF/USER_ID_CR | DTEL | released | CA-EPT-BRC |
| /BOFU/ADDRESS_ID | DTEL | released | CA-EPT-BRC |
| /BOFU/FBI_CHANGE_MODE | DTEL | released | CA-EPT-BRC-FBI |
| /BOFU/USER_ID_CHANGED_BY | DTEL | released | CA-EPT-BRC |
| /BOFU/USER_ID_CREATED_BY | DTEL | released | CA-EPT-BRC |
| /CPD/PFP_FG_API_RFC | FUGR | classicAPI | CA-CPD-FP |
| ... | | | (7335 more) |

---

### Basis Components

**Total APIs**: 6,936

**Application Components**: BC-ABA, BC-AI, BC-BMT, BC-BSP, BC-CCM, BC-CI, BC-CP, BC-CST, BC-CTS, BC-CUS
  ...and 18 more

**By Type**:
- INTF: 2655
- CLAS: 2512
- DTEL: 512
- FUGR: 367
- DDLS: 234

**By State**:
- released: 4097
- classicAPI: 2552
- deprecated: 167
- notToBeReleased: 86
- notToBeReleasedStable: 21
- noAPI: 13

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| A4C_CP_SERVICE_TYPE | DTEL | - |
| A4C_CP_SVC_INSTANCE_NAME | DTEL | - |
| A4C_CP_SVC_PROPERTY_NAME | DTEL | - |
| A4C_CP_SVC_PROPERTY_VALUE | DTEL | - |
| BAPIRET1 | TABL | - |
| BAPIRETURN | TABL | - |
| BAPIRETURN1 | TABL | - |
| BAPI_RCODE | DTEL | - |
| BOOLEAN | DTEL | ABAP_BOOLEAN |
| BOOLE_D | DTEL | ABAP_BOOLEAN |
| ... | | (157 more) |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /AIF/CL_BGRFC_CLEANUP_UTIL | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CL_ENABLER_IDOC | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CL_ENABLER_PROXY | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CL_ENABLER_SYNC_LOG | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CL_ENABLER_XML | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CL_NRT_CONFIG_BASE | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CL_NRT_TRANSFER_PROCESS | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CL_NRT_TRANSFER_SIMPLE | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CL_PERS_QUEUE | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CL_TRANSFORM_DATA | CLAS | noAPI | BC-SRV-AIF |
| /AIF/CX_AIF_ENGINE_BASE | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CX_AIF_ENGINE_NOT_FOUND | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CX_ENABLER_BASE | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CX_ERROR_HANDLING_GENERAL | CLAS | classicAPI | BC-SRV-AIF |
| /AIF/CX_INF_DET_BASE | CLAS | classicAPI | BC-SRV-AIF |
| ... | | | (6754 more) |

---

### Finance

**Total APIs**: 3,740

**Application Components**: FI-, FI-AA, FI-AP, FI-AR, FI-BL, FI-CA, FI-CF, FI-FIO, FI-FM, FI-GL
  ...and 6 more

**By Type**:
- DDLS: 1183
- TABL: 646
- DTEL: 617
- INTF: 447
- TTYP: 360

**By State**:
- released: 3511
- classicAPI: 113
- notToBeReleased: 58
- notToBeReleasedStable: 33
- deprecated: 19
- noAPI: 6

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| CL_CN_TXI_PROC_BADI_UTIL | CLAS | - |
| CL_CN_TXI_PROC_NOTI_UTIL | CLAS | - |
| FIWTAR_BASE_AMOUNT | ENHS | - |
| FIWTJP_MYNUMBER | ENHS | FIWTJP_VALIDATEMYNUMBER |
| IF_BADI_J_1IG_SUBCON | INTF | IF_BADI_CE_J_1IG_SUBCON |
| I_CADOCUMENTBPITEMLOGICAL | DDLS | I_CADOCUMENTBPITEM |
| I_CADOCUMENTBPITEMPHYSICAL | DDLS | I_CADOCUMENTBPITEM |
| I_CADOCUMENTBPREPETITIONITEM | DDLS | I_CADOCUMENTBPITEM |
| I_CADOCUMENTHEADER | DDLS | I_CADOCUMENT |
| I_CAINVCGCHARGEANDDISCOUNT | DDLS | I_CONACCTPRTNINVCGCHRGANDDISC |
| ... | | (9 more) |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /ATL/BADI_FILL_BNKA_ENH | ENHS | released | FI-LOC-FI-IL |
| /ATL/BADI_PCN874_CONF_NUM_ENH | ENHS | released | FI-LOC-FI-IL |
| /ATL/BADI_PCN874_CONF_NUM_EXPL | CLAS | released | FI-LOC-FI-IL |
| /ATL/BADI_PCN874_FINPO_ENH | ENHS | released | FI-LOC-FI-IL |
| /ATL/BADI_PCN874_GENERAL_ENH | ENHS | released | FI-LOC-FI-IL |
| /ATL/BADI_PCN874_INV_ENH | ENHS | released | FI-LOC-FI-IL |
| /ATL/BADI_UNIFILES_ENH | ENHS | released | FI-LOC-FI-IL |
| /ATL/BADI_WHT_REPORT_ENH | ENHS | released | FI-LOC-FI-IL |
| /ATL/BADI_WHT_RET_INV_ENH | ENHS | released | FI-LOC-FI-IL |
| /ATL/BLART_RANGE | TABL | released | FI-LOC-FI-IL |
| /ATL/BLART_RANGE_T | TTYP | released | FI-LOC-FI-IL |
| /ATL/BLDAT_RANGE | TABL | released | FI-LOC-FI-IL |
| /ATL/BLDAT_RANGE_T | TTYP | released | FI-LOC-FI-IL |
| /ATL/BRSCH_RANGE | TABL | released | FI-LOC-FI-IL |
| /ATL/BUDAT_RANGE | TABL | released | FI-LOC-FI-IL |
| ... | | | (3706 more) |

---

### Materials Management

**Total APIs**: 2,259

**Application Components**: MM-, MM-IM, MM-IV, MM-PUR, MM-SRV

**By Type**:
- DDLS: 769
- TABL: 501
- DTEL: 353
- TTYP: 204
- INTF: 178

**By State**:
- released: 1900
- deprecated: 195
- notToBeReleasedStable: 88
- notToBeReleased: 66
- classicAPI: 9
- noAPI: 1

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| CL_EX_INFOREC_SEND_CHANGES | CLAS | - |
| CL_MEOUT_BAPI_CUST_INBOUND_EXE | CLAS | - |
| CL_MEOUT_BAPI_CUST_OUTBOUND_EX | CLAS | - |
| CL_MEOUT_BAPI_DET_GROSS_COUT | CLAS | - |
| CL_MEOUT_BAPI_HANDLE_EXT_RF | CLAS | - |
| CL_MEOUT_BAPI_MAP2E_DATA | CLAS | - |
| CL_MEOUT_BAPI_MAP2E_EXT_OUT | CLAS | - |
| CL_MEOUT_BAPI_MAP2I_DATA | CLAS | - |
| CL_MEOUT_BAPI_MAP2I_EXT_IN | CLAS | - |
| CL_ME_CHK_SRC_DURING_SEARCH | CLAS | - |
| ... | | (185 more) |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 2012 | FUGR | notToBeReleased | MM-PUR-PO-2CL |
| 2013 | FUGR | notToBeReleased | MM-PUR-OA-2CL |
| 2014 | FUGR | notToBeReleased | MM-PUR-OA-2CL |
| 2105 | FUGR | notToBeReleased | MM-PUR-REQ-2CL |
| ABSKZ_EXT | DTEL | released | MM-PUR-PO-ES-2CL |
| ANFNR | DTEL | released | MM-PUR-2CL |
| ANFPS | DTEL | released | MM-PUR-2CL |
| API_PLANT_2_G4BA | SCO2 | released | MM-IM-GF-2CL |
| APPL_MRM_FORM_ERS_EXTERNAL | ENHS | released | MM-IV-LIV-2CL |
| ARKUEN | DTEL | released | MM-IV-LIV-2CL |
| BAPICUREXT_EXT | DTEL | released | MM-PUR-PO-ES-2CL |
| BAPIUPDATE_EXT | DTEL | released | MM-PUR-PO-ES-2CL |
| BASB | FUGR | classicAPI | MM-SRV |
| BBEIN_EXT | DTEL | released | MM-PUR-PO-ES-2CL |
| BBERD_EXT | DTEL | released | MM-PUR-PO-ES-2CL |
| ... | | | (2049 more) |

---

### Other (FS)

**Total APIs**: 1,189

**Application Components**: FS-, FS-BP, FS-CD, FS-CM, FS-CML, FS-CMS, FS-PM

**By Type**:
- DTEL: 1032
- DDLS: 62
- INTF: 45
- FUGR: 40
- CLAS: 7

**By State**:
- released: 1097
- classicAPI: 76
- noAPI: 16

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /GSINS/TR_IF_TRANSFORM | INTF | classicAPI | FS-CM-LC |
| /PM0/ABB_REMOTE_BP | FUGR | classicAPI | FS-PM |
| /PM0/ABN_REMOTE | FUGR | classicAPI | FS-PM |
| /PM0/ABP_MULTI_CONTRACT | FUGR | classicAPI | FS-PM |
| /PM0/ABQ_BAPI_MIGRATION | FUGR | classicAPI | FS-PM |
| /PM0/ABT_BW_EXTRACT | FUGR | classicAPI | FS-PM |
| /PM0/ABT_DATA_REPL | FUGR | classicAPI | FS-PM |
| /PM0/ABU_IBC_XML_EXP | FUGR | classicAPI | FS-PM |
| /PM0/AB_AUDIT | FUGR | classicAPI | FS-PM |
| /PM0/ALQ_BAPI_MIGRATION | FUGR | classicAPI | FS-PM |
| /PM0/AOIL_SVC_LOAN_CALC | FUGR | classicAPI | FS-PM |
| /PM0/CL_3FT_PROPERTY_LIST | CLAS | classicAPI | FS-PM |
| /PM0/CL_3FT_REGISTRY | CLAS | classicAPI | FS-PM |
| /PM0/CL_3F_BPU_CTRL | CLAS | classicAPI | FS-PM |
| /PM0/CL_3F_DA_STATE_ENG | CLAS | classicAPI | FS-PM |
| ... | | | (1174 more) |

---

### Sales & Distribution

**Total APIs**: 1,137

**Application Components**: SD-ANA, SD-BF, SD-BIL, SD-CAS, SD-CRF, SD-MD, SD-SLS

**By Type**:
- DDLS: 766
- TABL: 140
- INTF: 76
- DTEL: 71
- TTYP: 28

**By State**:
- released: 1016
- notToBeReleased: 95
- classicAPI: 10
- deprecated: 9
- notToBeReleasedStable: 7

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| C_BILLGDOCITMPRCGELMNTBSCDEX | DDLS | C_BILLGDOCITMPRCGELMNTBSCDEX_1 |
| C_BILLINGDOCUMENTITEMBASICDEX | DDLS | C_BILLINGDOCITEMBASICDEX_1 |
| C_SALESDOCITMPRCGELMNTDEX | DDLS | C_SALESDOCITMPRCGELMNTDEX_1 |
| C_SALESDOCUMENTITEMDEX | DDLS | C_SALESDOCUMENTITEMDEX_1 |
| C_SALESDOCUMENTSCHEDLINEDEX | DDLS | C_SALESDOCUMENTSCHEDLINEDEX_1 |
| I_PRODAVAILABILITYCHECKGROUP | DDLS | I_ATPCHECKINGGROUP |
| I_PRODAVAILABILITYCHECKGROUPT | DDLS | I_ATPCHECKINGGROUPTEXT |
| I_STOCKTYPE | DDLS | I_STOCKTYPE_2 |
| I_STOCKTYPETEXT | DDLS | I_STOCKTYPETEXT_2 |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 1037 | FUGR | classicAPI | SD-CAS-SA |
| 2030 | FUGR | classicAPI | SD-SLS-GF |
| 2031 | FUGR | classicAPI | SD-SLS-GF |
| 2032 | FUGR | notToBeReleased | SD-SLS-GF-2CL |
| 3033 | FUGR | classicAPI | SD-MD-AM-CMI |
| AUART | SIA2 | released | SD-SLS-2CL |
| CL_PRCG_DOC_ITM_REQUIREMENT | CLAS | released | SD-BF-PR-2CL |
| CL_PRC_RESULT_FACTORY | CLAS | notToBeReleased | SD-BF-PR-2CL |
| CL_SD_DOCFLOW_UTIL | CLAS | notToBeReleased | SD-CRF-DF-2CL |
| CL_SD_DOCUMENT_FLOW_RT | CLAS | notToBeReleased | SD-CRF-DF-2CL |
| CONDITIONTYPE | DTEL | released | SD-ANA-2CL |
| CREDITMEMOREQUEST | RONT | released | SD-SLS-CMR-2CL |
| CUSTOMERRETURN | RONT | released | SD-SLS-RE-2CL |
| CX_PRICING_FORMULA | CLAS | released | SD-BF-PR-2CL |
| C_BILLGDOCITMPRCGELMNTBSCDEX_1 | DDLS | released | SD-BIL-2CL |
| ... | | | (1113 more) |

---

### Other (FIN)

**Total APIs**: 1,105

**Application Components**: FIN-CS, FIN-FB, FIN-FIO, FIN-FSCM, FIN-IE

**By Type**:
- DDLS: 844
- IWSV: 52
- FUGR: 47
- DTEL: 32
- SUSO: 29

**By State**:
- released: 959
- classicAPI: 61
- notToBeReleasedStable: 60
- notToBeReleased: 14
- deprecated: 10
- noAPI: 1

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| I_CASHFLOWACTUALITEM | DDLS | - |
| I_CNSLDTNPOSTINGLEVELT | DDLS | I_CNSLDTNPOSTINGLEVELTEXT_2 |
| I_FINTRANSFLOWPOSTGBLKGRSN | DDLS | I_FINTRANSFLOWFIXINGBLKGRSN |
| I_FINTRANSFLOWPOSTGBLKGRSNTEXT | DDLS | I_FINTRANSFLOWFIXBLKGRSNTXT |
| I_FINTRANSFLOWPOSTGSTATUS | DDLS | I_FINTRANSFLOWFIXINGSTATUS |
| I_FINTRANSFLOWPOSTGSTATUSTEXT | DDLS | I_FINTRANSFLOWFIXSTATUSTEXT |
| I_VOLATILITYNAME | DDLS | I_IMPLIEDVOLATILITYIDENTIFIER |
| I_VOLATILITYNAMETEXT | DDLS | I_IMPLIEDVOLATILITYIDENTIFIERT |
| I_VOLATILITYPROFILE | DDLS | I_VOLATILITYPROFILE_2 |
| NPVTYPE | SIA2 | F_T_NPV |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /DCO/DAGRP | SUSO | released | FIN-FSCM-DM-2CL |
| /DCO/DSPUT | SUSO | released | FIN-FSCM-DM-2CL |
| /DCO/DSPVD | SUSO | released | FIN-FSCM-DM-2CL |
| /DCO/I_ACCOUNTINGDOCUMENTTP | DDLS | released | FIN-FSCM-COL-2CL |
| /DCO/I_CUSTOMER | DDLS | released | FIN-FSCM-COL-2CL |
| /DCO/I_CUSTOMERCOMPANY | DDLS | released | FIN-FSCM-COL-2CL |
| /DCO/I_DISPUTERESUBMISSIONTP | DDLS | released | FIN-FSCM-DM-2CL |
| /DCO/I_DISPUTETP | DDLS | released | FIN-FSCM-DM-2CL |
| /DCO/I_DSPUTACCTGDOCUMENTTP | DDLS | released | FIN-FSCM-DM-2CL |
| /DCO/I_DSPUTRELTDACCTGDOCTP | DDLS | released | FIN-FSCM-DM-2CL |
| /DCO/I_RBLPYBLTRANSACITEMTP | DDLS | released | FIN-FSCM-COL-2CL |
| /DCO/RECIT | SUSO | released | FIN-FSCM-COL-2CL |
| /PF1/DB_ACCT | TABL | notToBeReleased | FIN-FSCM-PF-IHB-2CL |
| /PF1/DB_ACCT_D | TABL | notToBeReleased | FIN-FSCM-PF-IHB-2CL |
| /PF1/DB_ACCT_LIM | TABL | notToBeReleased | FIN-FSCM-PF-IHB-2CL |
| ... | | | (1080 more) |

---

### Logistics General

**Total APIs**: 977

**Application Components**: LO-AB, LO-AGR, LO-ARM, LO-BM, LO-GT, LO-HU, LO-INT, LO-MD, LO-RFM, LO-SPM
  ...and 3 more

**By Type**:
- DDLS: 523
- TABL: 122
- FUGR: 80
- TTYP: 57
- INTF: 56

**By State**:
- released: 837
- notToBeReleased: 56
- classicAPI: 55
- notToBeReleasedStable: 20
- deprecated: 6
- noAPI: 3

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| I_BILLOFMATERIALHEADERDEX | DDLS | - |
| I_BILLOFMATERIALITEMDEX | DDLS | - |
| I_BILLOFMATERIALITEMDEX_2 | DDLS | I_BILLOFMATERIALITEMDEX_3 |
| I_MATERIALBOMLINKDEX | DDLS | I_MATERIALBOMLINKDEX_2 |
| I_SALESORDERBOMLINKDEX | DDLS | I_SALESORDERBOMLINKDEX_2 |
| I_SERIALNUMBERMATERIALDOCUMENT | DDLS | I_SERIALNUMBERMATERIALDOC_2 |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /ACCGO/CAS_APPL_API | FUGR | classicAPI | LO-AGR-APP |
| /ACCGO/CCAK_TC_API | FUGR | classicAPI | LO-AGR-CC |
| /ACCGO/OIJ_NOM_API | FUGR | classicAPI | LO-AGR-LDC |
| /ACCGO/UIS_API | FUGR | classicAPI | LO-AGR-LDC |
| /SPE/DELIVERY_INTERFACES | FUGR | classicAPI | LO-SPM-X |
| /SPE/IF_TOOLS | FUGR | classicAPI | LO-SPM-X |
| 1001 | FUGR | notToBeReleased | LO-MD-MM-2CL |
| 1001DIA | FUGR | notToBeReleased | LO-MD-MM-2CL |
| 1001MASSUEB | FUGR | notToBeReleased | LO-MD-MM-2CL |
| 1001UEB | FUGR | notToBeReleased | LO-MD-MM-2CL |
| 1008 | FUGR | classicAPI | LO-MD-BP-VM |
| 1069 | FUGR | classicAPI | LO-RFM-MD-SIT |
| 1070 | FUGR | classicAPI | LO-RFM-MD-LST |
| 1071 | FUGR | classicAPI | LO-RFM-OBS |
| 1171 | FUGR | classicAPI | LO-RFM-MD-PCT-IN |
| ... | | | (956 more) |

---

### Production Planning

**Total APIs**: 707

**Application Components**: PP-BD, PP-CFS, PP-CRP, PP-ES, PP-FIO, PP-KAB, PP-MES, PP-MP, PP-MRP, PP-PDC
  ...and 6 more

**By Type**:
- DDLS: 533
- INTF: 34
- TABL: 30
- FUGR: 25
- ENHS: 21

**By State**:
- released: 641
- notToBeReleased: 32
- notToBeReleasedStable: 21
- classicAPI: 12
- noAPI: 1

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 0001_BAPI | FUGR | notToBeReleased | PP-SFC-2CL |
| 2004 | FUGR | notToBeReleased | PP-PLO-2CL |
| 2005_BAPI | FUGR | notToBeReleased | PP-SFC-2CL |
| 2016 | FUGR | notToBeReleased | PP-SFC-EXE-CON-2CL |
| 2116 | FUGR | notToBeReleased | PP-SFC-EXE-CON-2CL |
| 2142 | FUGR | classicAPI | PP-REM-ADE |
| 3027 | FUGR | notToBeReleased | PP-MP-DEM-2CL |
| AFKO | TABL | notToBeReleased | PP-SFC-2CL |
| AFPO | TABL | notToBeReleased | PP-SFC-2CL |
| AFRU | TABL | notToBeReleased | PP-SFC-EXE-CON-2CL |
| AFVC | TABL | notToBeReleased | PP-SFC-2CL |
| AFVU | TABL | notToBeReleased | PP-SFC-2CL |
| AFVU_INCL_EEW_PS | TABL | released | PP-SFC-2CL |
| AFVV | TABL | notToBeReleased | PP-SFC-2CL |
| ARBPL_WERKS | SIA2 | released | PP-MRP-2CL |
| ... | | | (692 more) |

---

### Other (EHS)

**Total APIs**: 628

**Application Components**: EHS-DGP, EHS-SAF, EHS-SUS

**By Type**:
- TABL: 223
- TTYP: 142
- DTEL: 101
- INTF: 47
- CLAS: 41

**By State**:
- released: 611
- notToBeReleasedStable: 7
- noAPI: 4
- classicAPI: 3
- notToBeReleased: 2
- deprecated: 1

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| ES_EHHSS_INV_LEAD_DETERM | ENHS | - |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 1077 | FUGR | classicAPI | EHS-SAF |
| 1078 | FUGR | classicAPI | EHS-DGP |
| 1091 | FUGR | classicAPI | EHS-SAF |
| BAPI_EHENVS_ADC_IMPORT | TABL | released | EHS-SUS-EM |
| BAPI_EHENVT_ADC_IMPORT | TTYP | released | EHS-SUS-EM |
| CHEMICALCOMPLIANCEINFO | RONT | released | EHS-SUS-FND-PC |
| CL_BADI_EHDGM_MIXED_LOAD_BASE | CLAS | released | EHS-SUS-DG |
| CL_EHDGM_API_EXT_FACTORY | CLAS | released | EHS-SUS-DG |
| CL_EHDGM_API_EXT_INJECTOR | CLAS | released | EHS-SUS-DG |
| CL_EHDGM_DATA_PRVDR_BASIC_CLFN | CLAS | released | EHS-SUS-DG |
| CL_EHFND_ABAP_TESTDOUBLE_MNGR | CLAS | released | EHS-SUS-FND |
| CL_EHFND_DATA_PRVDR_AC | CLAS | released | EHS-SUS-FND-PC |
| CL_EHFND_DATA_PRVDR_ARM | CLAS | released | EHS-SUS-FND-PC |
| CL_EHFND_DATA_PRVDR_CBI | CLAS | released | EHS-SUS-FND-PC |
| CL_EHFND_DATA_PRVDR_CCI_ID | CLAS | released | EHS-SUS-FND-PC |
| ... | | | (612 more) |

---

### Industry Solutions

**Total APIs**: 418

**Application Components**: IS-A, IS-B, IS-DFS, IS-EC, IS-HER, IS-MP, IS-OIL, IS-PS, IS-T, IS-U

**By Type**:
- INTF: 164
- ENHS: 159
- FUGR: 86
- CLAS: 6
- DDLS: 1

**By State**:
- released: 332
- classicAPI: 65
- noAPI: 21

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /ISDFPS/ALE_TEST | FUGR | classicAPI | IS-DFS |
| /ISDFPS/BAPI_NSN | FUGR | classicAPI | IS-DFS-MM |
| /ISDFPS/BAPI_NSN_GC | FUGR | classicAPI | IS-DFS-MM |
| /ISDFPS/CRUPS | FUGR | noAPI | IS-DFS-PDR |
| /ISDFPS/CS_COMMAND | FUGR | classicAPI | IS-DFS-MM |
| /ISDFPS/DGUPS | FUGR | noAPI | IS-DFS-PDR |
| /ISDFPS/GOODS_RECEIPT | FUGR | classicAPI | IS-DFS-MM |
| /ISDFPS/LSYS | FUGR | classicAPI | IS-DFS-BIT-DIS |
| /ISDFPS/PORD | FUGR | classicAPI | IS-DFS-MM |
| /ISDFPS/PREQ | FUGR | classicAPI | IS-DFS-MM |
| /ISDFPS/REQ_MASTER_DATA | FUGR | noAPI | IS-DFS-BIT |
| /ISDFPS/WM_LES | FUGR | classicAPI | IS-DFS-MM |
| /PRA/ACCT_DOC_CHANGE | ENHS | released | IS-OIL-PRA |
| /PRA/ACCT_DOC_MASS_UPLOAD | ENHS | released | IS-OIL-PRA |
| /PRA/ACCT_DOC_SUMMARY | ENHS | released | IS-OIL-PRA |
| ... | | | (403 more) |

---

### Customer Relationship Management

**Total APIs**: 375

**Application Components**: CRM-BF, CRM-BTX, CRM-IU, CRM-S4

**By Type**:
- DDLS: 292
- DTEL: 48
- SUSO: 11
- TABL: 6
- FUGR: 5

**By State**:
- released: 358
- classicAPI: 6
- notToBeReleasedStable: 6
- deprecated: 3
- noAPI: 2

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| I_BSORDITMSUBSCRPNPARAMETERTP | DDLS | I_BSORDITMSUBSCRPNPARAMTP_2 |
| I_SRVCORDFUPMAINTORDTP | DDLS | - |
| I_SRVCORDITMFUPMAINTORDTP | DDLS | - |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| ABART | DTEL | released | CRM-BTX-BF-ATP-2CL |
| ABNUM | DTEL | released | CRM-BTX-BF-ATP-2CL |
| AUSCHUFAK | DTEL | released | CRM-BTX-BF-ATP-2CL |
| BEDAE | DTEL | released | CRM-BTX-BF-ATP-2CL |
| BMENG | DTEL | released | CRM-BTX-BF-ATP-2CL |
| BOLNR | DTEL | released | CRM-BTX-BF-ATP-2CL |
| CL_CRMS4_SOM_PROD_SPEC_API | CLAS | classicAPI | CRM-S4-SOM |
| CL_CRMS4_SOM_PROD_SPEC_FACTORY | CLAS | classicAPI | CRM-S4-SOM |
| CO_APLZL | DTEL | released | CRM-BTX-BF-ATP-2CL |
| CRMS4S_1O_BADI_MESSAGE | TABL | released | CRM-S4-BTX-2CL |
| CRMS4S_ANA_EXT_BTX | TABL | released | CRM-S4-ANA-CDS-2CL |
| CRMS4S_SERV_H_BADI | TABL | released | CRM-S4-BTX-2CL |
| CRMS4S_SERV_H_INCL_EEW_PS | TABL | released | CRM-S4-BTX-2CL |
| CRMS4S_SERV_I_BADI | TABL | released | CRM-S4-BTX-2CL |
| CRMS4S_SERV_I_INCL_EEW_PS | TABL | released | CRM-S4-BTX-2CL |
| ... | | | (357 more) |

---

### Transportation Management

**Total APIs**: 362

**Application Components**: TM-2CL, TM-BF, TM-CF, TM-FRA, TM-FRM, TM-FRS, TM-MD, TM-PLN

**By Type**:
- DDLS: 202
- DTEL: 142
- INTF: 10
- SUSO: 5
- SIA2: 2

**By State**:
- released: 338
- notToBeReleasedStable: 24

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /SCMB/LOCB | SUSO | released | TM-MD-TN-LOC-2CL |
| /SCMTMS/BASE_BTD_ITEM_TCO | DTEL | released | TM-CF-2CL |
| /SCMTMS/BTD_DATE | DTEL | released | TM-CF-2CL |
| /SCMTMS/BTD_ID | DTEL | released | TM-CF-2CL |
| /SCMTMS/BTD_ISSUINGPARTY_NAME | DTEL | released | TM-CF-2CL |
| /SCMTMS/BTD_ITEM_ID | DTEL | released | TM-CF-2CL |
| /SCMTMS/BTD_ITEM_TYPECODE | DTEL | released | TM-CF-2CL |
| /SCMTMS/BTD_TYPE_CODE | DTEL | released | TM-CF-2CL |
| /SCMTMS/COMMODITY_CODE | DTEL | released | TM-CF-2CL |
| /SCMTMS/CONT_SHIPPER_OWN | DTEL | released | TM-CF-2CL |
| /SCMTMS/DLV_GOODS_MOVEM_STATUS | DTEL | released | TM-CF-2CL |
| /SCMTMS/EIKTO_K | DTEL | released | TM-FRM-2CL |
| /SCMTMS/EQUIP_GROUP | DTEL | released | TM-CF-2CL |
| /SCMTMS/EQUIP_TYPE | DTEL | released | TM-CF-2CL |
| /SCMTMS/ES_TRANSP_ORDER_EXTEND | ENHS | released | TM-FRM-2CL |
| ... | | | (347 more) |

---

### Quality Management

**Total APIs**: 355

**Application Components**: QM-2CL, QM-CA, QM-ES, QM-IM, QM-PT, QM-QC, QM-QN

**By Type**:
- DDLS: 221
- SUSO: 28
- INTF: 25
- DTEL: 19
- FUGR: 14

**By State**:
- released: 337
- classicAPI: 10
- notToBeReleased: 8

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 1006 | FUGR | classicAPI | QM-QN |
| 2045 | FUGR | notToBeReleased | QM-IM-2CL |
| 2078 | FUGR | notToBeReleased | QM-QN-2CL |
| ARC_QM_DEFECT | ENHS | released | QM-QN-DEF-2CL |
| CL_QASDR_EX_PLAN_TO_INSPECTION | CLAS | released | QM-PT-BD-2CL |
| CL_QC_EX_CERT_RES_ORIGIN | CLAS | released | QM-CA-MD-2CL |
| CL_QC_EX_CERT_SKIP_STRATEGY | CLAS | released | QM-CA-MD-2CL |
| CL_QC_EX_CERT_SPEC_ORIGIN | CLAS | released | QM-CA-MD-2CL |
| CL_QC_EX_CERT_TEXT_ORIGIN | CLAS | released | QM-CA-MD-2CL |
| CL_QQM_EX_NOTIF_DEFLT_VAL_CLD | CLAS | released | QM-QN-2CL |
| CL_QQM_EX_NOTIF_EVENT_POST_CLD | CLAS | released | QM-QN-2CL |
| CL_QQM_EX_NOTIF_EVENT_SAVE_CLD | CLAS | released | QM-QN-2CL |
| CL_QQM_NOTIF_ACTIONBOX_FOA | CLAS | released | QM-QN-2CL |
| CPCC_BUS1191 | FUGR | classicAPI | QM-PT-IP |
| CPCC_ES | FUGR | classicAPI | QM-ES |
| ... | | | (340 more) |

---

### Other (OPU)

**Total APIs**: 291

**Application Components**: OPU-BSC, OPU-BSE, OPU-FND, OPU-GW, OPU-XBE

**By Type**:
- INTF: 237
- CLAS: 50
- DTEL: 4

**By State**:
- classicAPI: 213
- released: 78

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /IWBEP/CL_COS_LOGGER | CLAS | classicAPI | OPU-GW-V4 |
| /IWBEP/CL_CP_FACTORY_REMOTE | CLAS | released | OPU-GW-CP |
| /IWBEP/CL_CP_FACTORY_UNIT_TST | CLAS | released | OPU-GW-CP |
| /IWBEP/CL_MGW_ABS_DATA | CLAS | classicAPI | OPU-BSE-SDE |
| /IWBEP/CL_MGW_ABS_MODEL | CLAS | classicAPI | OPU-BSE-SDE |
| /IWBEP/CL_MGW_BOP_COMMON | CLAS | classicAPI | OPU-BSE-SDE |
| /IWBEP/CL_MGW_BOP_COMMON_RFC | CLAS | classicAPI | OPU-BSE-SDE |
| /IWBEP/CL_MGW_BOP_DO | CLAS | classicAPI | OPU-BSE-SDE |
| /IWBEP/CL_MGW_DATA_UTIL | CLAS | classicAPI | OPU-BSE-SDE |
| /IWBEP/CL_MGW_GSR_EDP_RO_BASE | CLAS | classicAPI | OPU-BSE-SDE |
| /IWBEP/CL_MGW_PUSH_ABS_DATA | CLAS | classicAPI | OPU-BSE-TLS |
| /IWBEP/CL_MGW_PUSH_ABS_MODEL | CLAS | classicAPI | OPU-BSE-TLS |
| /IWBEP/CL_SB_GEN_DPC_RT_UTIL | CLAS | classicAPI | OPU-BSE-SB |
| /IWBEP/CL_SB_GEN_READ_AFTR_CRT | CLAS | classicAPI | OPU-BSE-SB |
| /IWBEP/CL_SB_SHLP_DATA_FACTORY | CLAS | classicAPI | OPU-BSE-SB |
| ... | | | (276 more) |

---

### Plant Maintenance

**Total APIs**: 286

**Application Components**: PM-, PM-2CL, PM-EQM, PM-PRM, PM-WOC

**By Type**:
- DDLS: 225
- SUSO: 24
- FUGR: 14
- DTEL: 8
- INTF: 6

**By State**:
- released: 238
- classicAPI: 33
- notToBeReleasedStable: 11
- deprecated: 2
- notToBeReleased: 2

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| I_EAM_OM | SUSO | I_EAM_MJPB |
| I_MAINTORDEROPCOMPONENTTP | DDLS | I_MAINTORDEROPCOMPONENTTP_2 |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 2128 | FUGR | classicAPI | PM-WOC-JC |
| AFIH_INCL_EEW_PS | TABL | released | PM-WOC-MO-2CL |
| AFIH_INCL_EEW_X | TABL | released | PM-WOC-MO-2CL |
| CL_EAM_PR_ITEM_RELEASE_WF_COND | CLAS | released | PM-WOC-MO-PUR-2CL |
| C_EQUIPMENTCLFNCHARCVALUEDEX | DDLS | released | PM-EQM-EQ-2CL |
| C_FUNCNLLOCCLFNCHARCVALUEDEX | DDLS | released | PM-EQM-EQ-2CL |
| D_EQUIPCRTEMASSMATLSRLNMBRP | DDLS | notToBeReleasedStable | PM-EQM-EQ-2CL |
| D_EQUIPCRTEMASSMATLSRLNMBRR | DDLS | notToBeReleasedStable | PM-EQM-EQ-2CL |
| D_EQUIPMENTINSTALLATIONP | DDLS | released | PM-EQM-EQ-2CL |
| D_EQUI_STR_FUNCIMPORTP | DDLS | released | PM-EQM-EQ-2CL |
| D_MAINTORDASSIGNNOTIFICATIONP | DDLS | released | PM-WOC-MO-2CL |
| D_MAINTORDCONFIRMATIONCANCELP | DDLS | released | PM-WOC-JC-2CL |
| D_MAINTORDERSTATUSCLOSEDP | DDLS | released | PM-WOC-MO-2CL |
| D_MAINTORDERSTSDONOTEXECUTEP | DDLS | released | PM-WOC-MO-2CL |
| D_MAINTORDMAINWORKCOMPLETEP | DDLS | released | PM-WOC-MO-2CL |
| ... | | | (269 more) |

---

### Logistics Execution

**Total APIs**: 229

**Application Components**: LE-DSD, LE-IDW, LE-JIT, LE-SHP, LE-TRA, LE-WM

**By Type**:
- DDLS: 163
- TABL: 20
- INTF: 16
- FUGR: 10
- DTEL: 8

**By State**:
- released: 206
- notToBeReleased: 12
- classicAPI: 10
- notToBeReleasedStable: 1

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /DSD/HH_UL_BAPI | FUGR | classicAPI | LE-DSD-DC-DU |
| /DSD/VC_BAPI_VL | FUGR | classicAPI | LE-DSD-VC |
| /DSD/VC_BAPI_VP | FUGR | classicAPI | LE-DSD-VC |
| C_JITPRODNCONFPROFILEVH | DDLS | released | LE-JIT-S2C |
| DELIVERY_HEAD | TABL | released | LE-SHP-EXT-2CL |
| DEL_DOC_PROCESSING_MODE | DTEL | released | LE-SHP-EXT-2CL |
| D_CUSTRETCRTDLVITMFRMSLSDOCP | DDLS | released | LE-SHP-API-2CL |
| D_CUSTRETDLVCRTEDLVFRMSLSDOCP | DDLS | released | LE-SHP-API-2CL |
| D_CUSTRETDLVCRTEFRMSLSDOCITEMP | DDLS | released | LE-SHP-API-2CL |
| D_INBDELIVCRTEDELIVFRMPURGDOCP | DDLS | released | LE-SHP-API-2CL |
| D_INBDELIVCRTEFRMPURGDOCITEMP | DDLS | released | LE-SHP-API-2CL |
| D_OUTBDELIVCRTDLVITMFRMSLSDOCP | DDLS | released | LE-SHP-API-2CL |
| D_OUTBDELIVCRTEDELIVFRMSLSDOCP | DDLS | released | LE-SHP-API-2CL |
| D_OUTBDELIVCRTEFRMSLSDOCITEMP | DDLS | released | LE-SHP-API-2CL |
| D_OUTBDELIVDELIVBLOCKCHANGED | DDLS | released | LE-SHP-GF-2CL |
| ... | | | (214 more) |

---

### Controlling

**Total APIs**: 218

**Application Components**: CO-, CO-FIO, CO-OM, CO-PA, CO-PC

**By Type**:
- DDLS: 86
- FUGR: 33
- TABL: 21
- IWSV: 20
- DTEL: 15

**By State**:
- released: 149
- classicAPI: 25
- notToBeReleasedStable: 22
- notToBeReleased: 16
- deprecated: 4
- noAPI: 2

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| I_MFGORDERACTLPLANTGTCOST | DDLS | I_MFGORDERACTLPLANTGTLDGRCOST |
| I_MFGORDERWIPVARIANCE | DDLS | I_MFGORDEREVTBSDWIPVARIANCE |
| I_PRODNORDERPLANNINGCATEGORY | DDLS | - |
| I_SERVICECOSTRATE | DDLS | I_SERVICECOSTRATE_2 |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 0004 | FUGR | notToBeReleased | CO-OM-2CL |
| 0004CORE | FUGR | notToBeReleased | CO-OM-2CL |
| 0012 | FUGR | notToBeReleased | CO-OM-2CL |
| 0COG | FUGR | classicAPI | CO-OM-OPA |
| 1030 | FUGR | classicAPI | CO-OM |
| 1031 | FUGR | classicAPI | CO-OM |
| 1036 | FUGR | classicAPI | CO-OM-ABC |
| 1079 | FUGR | classicAPI | CO-PC-OBJ |
| 1137 | FUGR | classicAPI | CO-OM-ABC |
| 1138 | FUGR | classicAPI | CO-OM |
| 1139 | FUGR | noAPI | CO-OM-CCA |
| 2044 | FUGR | notToBeReleased | CO-PC-PCP-2CL |
| 2075 | FUGR | noAPI | CO-OM-OPA |
| 2076 | FUGR | classicAPI | CO-PC-OBJ-PER |
| 2137 | FUGR | classicAPI | CO-OM-ABC |
| ... | | | (199 more) |

---

### Other (CM)

**Total APIs**: 199

**Application Components**: CM-CAT, CM-CTX, CM-DOC, CM-GF, CM-INT, CM-LT, CM-TSK

**By Type**:
- DDLS: 97
- INTF: 33
- TABL: 25
- DTEL: 13
- SUSO: 11

**By State**:
- released: 198
- deprecated: 1

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| IF_LCM_LT_WF_CUSTOM_STEP | INTF | IF_LCM_LT_WF_CUSTOM_STEP_2 |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| CL_LCM_LT_WF_CUSTOM_STEP_2 | CLAS | released | CM-LT-2CL |
| COMP_CODE | SIA2 | released | CM-INT-2CL |
| CTX_PROF | SIA2 | released | CM-INT-2CL |
| D_LEGALDOCUPDATEPAPERTYPEP | DDLS | released | CM-DOC-2CL |
| D_LGLCNTNTMDOCLINKOBJKEYCRTEP | DDLS | released | CM-INT-2CL |
| D_LGLCNTNTMDOCLINKOBJKEYCRTER | DDLS | released | CM-INT-2CL |
| D_LGLDOCCREATEFILEFROMVRTLDOCP | DDLS | released | CM-DOC-2CL |
| D_LGLDOCCREATEVRTLDOCP | DDLS | released | CM-DOC-2CL |
| D_LGLDOCCRTELGLDOCWITHFILEP | DDLS | released | CM-DOC-2CL |
| D_LGLDOCUPLDFILEONVRTLDOCP | DDLS | released | CM-DOC-2CL |
| D_LGLTRANSCANCELTSKGRPP | DDLS | released | CM-LT-2CL |
| D_LGLTRANSRESTARTLGLTRANSPHSEP | DDLS | released | CM-LT-2CL |
| D_LGLTRANSSTRTLGLTRANSPHSEP | DDLS | released | CM-LT-2CL |
| D_LGLTRANSTRGGRLGLTRANSTSKGRPP | DDLS | released | CM-LT-2CL |
| IF_LCM_BOINT_DISBLE_LT_REOPEN | INTF | released | CM-LT-2CL |
| ... | | | (183 more) |

---

### Other (PPM)

**Total APIs**: 195

**Application Components**: PPM-PRO, PPM-SCL

**By Type**:
- DDLS: 150
- FUGR: 17
- SUSO: 13
- RONT: 6
- IWSV: 4

**By State**:
- released: 169
- classicAPI: 14
- notToBeReleasedStable: 5
- deprecated: 4
- noAPI: 3

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| C_PROJ_KOK | SUSO | /S4PPM/PR1 |
| C_PROJ_PRC | SUSO | /S4PPM/PR1 |
| C_PRPS_KOK | SUSO | /S4PPM/PR1 |
| C_PRPS_PRC | SUSO | /S4PPM/PR1 |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /S4PPM/ORG | SUSO | released | PPM-SCL-STR |
| /S4PPM/PR1 | SUSO | released | PPM-SCL-STR |
| /S4PPM/PRJ | SUSO | released | PPM-SCL-STR |
| C_DEMAND | SUSO | released | PPM-SCL-DMN |
| C_PRJBLGEL | SUSO | released | PPM-SCL-BIL |
| C_PRJBLGRQ | SUSO | released | PPM-SCL-BIL |
| C_PRPS_KST | SUSO | released | PPM-SCL-STR |
| DPR_BUS2164 | FUGR | classicAPI | PPM-PRO-EXT-API |
| DPR_BUS2165 | FUGR | noAPI | PPM-PRO-EXT-API |
| DPR_BUS2166 | FUGR | noAPI | PPM-PRO-EXT-API |
| DPR_BUS2167 | FUGR | classicAPI | PPM-PRO-EXT-API |
| DPR_BUS2168 | FUGR | classicAPI | PPM-PRO-EXT-API |
| DPR_BUS2169 | FUGR | classicAPI | PPM-PRO-EXT-API |
| DPR_BUS2170 | FUGR | classicAPI | PPM-PRO-EXT-API |
| DPR_BUS2171 | FUGR | classicAPI | PPM-PRO-EXT-API |
| ... | | | (176 more) |

---

### Real Estate

**Total APIs**: 193

**Application Components**: RE-, RE-FX, RE-RT

**By Type**:
- DDLS: 139
- FUGR: 30
- CLAS: 9
- RONT: 6
- SUSO: 4

**By State**:
- released: 154
- classicAPI: 30
- noAPI: 9

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| BUKRS_BERGRP | SIA2 | released | RE-FX-2CL |
| BUKRS_IOSGTYPE | SIA2 | released | RE-FX-2CL |
| BUKRS_SMVART | SIA2 | released | RE-FX-2CL |
| CF_REBD_BUILDING | CLAS | noAPI | RE-FX-BD |
| CF_REBD_BUSINESS_ENTITY | CLAS | noAPI | RE-FX-BD |
| CF_REBD_RENTAL_OBJECT | CLAS | noAPI | RE-FX-BD |
| CF_RECN_CONTRACT | CLAS | noAPI | RE-FX-CN |
| CF_RESC_SETTL_UNIT | CLAS | noAPI | RE-FX-SC |
| CL_REBD_ARCH_OBJECT | CLAS | noAPI | RE-FX-BD |
| CL_REBD_RENTAL_OBJECT | CLAS | noAPI | RE-FX-BD |
| CL_RECN_CONTRACT | CLAS | noAPI | RE-FX-CN |
| CL_REEXC_COMPANY_CODE | CLAS | noAPI | RE-FX |
| C_REARCHITECTUREOBJECTDEX | DDLS | released | RE-FX-BD-2CL |
| C_REARCHTROBJADDRESSDEX | DDLS | released | RE-FX-BD-2CL |
| C_REARCHTROBJHIERNDERLTNDEX | DDLS | released | RE-FX-BD-2CL |
| ... | | | (178 more) |

---

### Supply Chain Management

**Total APIs**: 165

**Application Components**: SCM-APO, SCM-BAS, SCM-EWM

**By Type**:
- DDLS: 63
- DTEL: 33
- FUGR: 32
- SUSO: 15
- INTF: 14

**By State**:
- released: 126
- classicAPI: 26
- noAPI: 7
- deprecated: 5
- notToBeReleasedStable: 1

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| I_EWM_DELIVERYCATEGORY | DDLS | I_EWM_DELIVERYCATEGORY_2 |
| I_EWM_DELIVERYTYPE | DDLS | I_EWM_DELIVERYTYPE_2 |
| I_EWM_DELIVERYTYPETEXT | DDLS | I_EWM_DELIVERYTYPETEXT_2 |
| I_EWM_INBOUNDDELIVERYTYPE | DDLS | I_EWM_INBOUNDDELIVERYTYPE_2 |
| I_EWM_OUTBOUNDDELIVORDERTYPE | DDLS | I_EWM_OUTBOUNDDELIVORDERTYPE_2 |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /INCMD/BAPISERVICES | FUGR | classicAPI | SCM-BAS-MD-INC |
| /SAPAPO/CBM_DX | FUGR | classicAPI | SCM-BAS-MD-BM |
| /SCWM/CHG | SUSO | released | SCM-EWM-AUT-2CL |
| /SCWM/CL_EI_POD_VALIDATE_ACT | CLAS | released | SCM-EWM-WC-2CL |
| /SCWM/CL_POD_FILTER_ITEM | CLAS | released | SCM-EWM-WC-2CL |
| /SCWM/DLV | SUSO | released | SCM-EWM-DLP-2CL |
| /SCWM/DLV2 | SUSO | released | SCM-EWM-DLP-2CL |
| /SCWM/ES4_CORE_PTS | ENHS | released | SCM-EWM-WOP-2CL |
| /SCWM/ES4_CORE_RMS | ENHS | released | SCM-EWM-WOP-2CL |
| /SCWM/ES4_OM_EXTEND | ENHS | released | SCM-EWM-PRN-2CL |
| /SCWM/ES_PACK_OUTBDLV | ENHS | released | SCM-EWM-WC-2CL |
| /SCWM/HU | SUSO | released | SCM-EWM-AUT-2CL |
| /SCWM/IF_CORE_CLOUD_TYPES | INTF | released | SCM-EWM-WOP-2CL |
| /SCWM/IF_EX4_CORE_PTS_FILT_EMP | INTF | released | SCM-EWM-WOP-2CL |
| /SCWM/IF_EX4_CORE_PTS_FILT_NFB | INTF | released | SCM-EWM-WOP-2CL |
| ... | | | (145 more) |

---

### Personnel Administration

**Total APIs**: 148

**Application Components**: PA-AS, PA-BN, PA-CP, PA-EC, PA-ESS, PA-FIO, PA-IS, PA-MA, PA-OS, PA-PA
  ...and 3 more

**By Type**:
- FUGR: 85
- INTF: 35
- CLAS: 28

**By State**:
- classicAPI: 145
- noAPI: 3

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 0PBAPI0105 | FUGR | classicAPI | PA-PA |
| 1065 | FUGR | classicAPI | PA-PA |
| APPL | FUGR | classicAPI | PA-RC |
| APPLICATION | FUGR | classicAPI | PA-RC |
| BPAY | FUGR | classicAPI | PA-PA |
| CL_HCMFAB_EMPLOYEE_API | CLAS | classicAPI | PA-FIO |
| CL_HCP_GLOBAL_CONSTANTS | CLAS | classicAPI | PA-CP |
| CL_HRASR00_DATA_CONTAINER | CLAS | classicAPI | PA-AS |
| CL_HRCE_MASTERSWITCHES | CLAS | classicAPI | PA-PA-XX |
| CL_HRECM00_CONST | CLAS | classicAPI | PA-EC-AD |
| CL_HRESS_AS_CATS | CLAS | classicAPI | PA-ESS-XX-WDA |
| CL_HRESS_CATS_WDA_UTILS | CLAS | classicAPI | PA-ESS-XX-WDA |
| CL_HRESS_EMPLOYEE_SERVICES | CLAS | classicAPI | PA-ESS-XX-WDA |
| CL_HRESS_FPM_MSG_SERVICES | CLAS | classicAPI | PA-ESS-XX-WDA |
| CL_HRPAD00AUTH_CHECK_STD | CLAS | classicAPI | PA-PA |
| ... | | | (133 more) |

---

### Other (AP)

**Total APIs**: 147

**Application Components**: AP-CFG, AP-LIM, AP-MD, AP-PPE

**By Type**:
- DDLS: 84
- DTEL: 44
- FUGR: 11
- SUSO: 5
- SIA2: 2

**By State**:
- released: 133
- classicAPI: 11
- notToBeReleasedStable: 2
- noAPI: 1

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| ADFULLNAME | DTEL | released | AP-MD-BP |
| BEGRU_BUPA_GRP | SIA2 | released | AP-MD-BP |
| BPTAXTYPE | DTEL | released | AP-MD-BP |
| BPTAXTYPETXT | DTEL | released | AP-MD-BP |
| BUBA_3 | FUGR | classicAPI | AP-MD-BP |
| BUBA_4 | FUGR | classicAPI | AP-MD-BP |
| BUBA_5 | FUGR | classicAPI | AP-MD-BP |
| BUBA_6 | FUGR | classicAPI | AP-MD-BP |
| BUPA_HOURS_BAPI | FUGR | classicAPI | AP-MD-BP |
| BUPA_TFW_BAPI | FUGR | classicAPI | AP-MD-BP |
| BUS_EI_OBJECT_TASK | DTEL | released | AP-MD-BF-SYN-2CL |
| BU_AKTYP | DTEL | released | AP-MD-BP |
| BU_BOOLEAN | DTEL | released | AP-MD-BP-UI |
| BU_DESCRIP | DTEL | released | AP-MD-BP |
| BU_FCODE | DTEL | released | AP-MD-BP |
| ... | | | (132 more) |

---

### Other (SLC)

**Total APIs**: 104

**Application Components**: SLC-, SLC-ACT, SLC-CAT, SLC-EVL, SLC-SUP

**By Type**:
- DDLS: 102
- DTEL: 1
- SUSO: 1

**By State**:
- released: 104

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /SRMSMC/BO | SUSO | released | SLC |
| /SRMSMC/LANGUAGE_PARAMETER | DTEL | released | SLC |
| I_INACTIVESTATUS | DDLS | released | SLC-SUP |
| I_INACTIVESTATUSTEXT | DDLS | released | SLC-SUP |
| I_PURCHASINGCATEGORYVALUEHELP | DDLS | released | SLC-CAT-2CL |
| I_PURGCATAPI01 | DDLS | released | SLC-CAT-2CL |
| I_PURGCATDESCRIPTIONAPI01 | DDLS | released | SLC-CAT-2CL |
| I_PURGCATMATERIALGROUPAPI01 | DDLS | released | SLC-CAT-2CL |
| I_PURGCATMEMBERAPI01 | DDLS | released | SLC-CAT-2CL |
| I_PURGCATPARTYAPI01 | DDLS | released | SLC-CAT-2CL |
| I_PURGCATPLANSPENDAPI01 | DDLS | released | SLC-CAT-2CL |
| I_PURGCATPURCHASERRESPAPI01 | DDLS | released | SLC-CAT-2CL |
| I_PURGCATSUPPLIERAPI01 | DDLS | released | SLC-CAT-2CL |
| I_PURGCATTRANSLATIONSTSAPI01 | DDLS | released | SLC-CAT-2CL |
| I_SLCCONSISTENCYSTATUS | DDLS | released | SLC-SUP |
| ... | | | (89 more) |

---

### Other (PSM)

**Total APIs**: 84

**Application Components**: PSM-, PSM-FM, PSM-GM

**By Type**:
- DDLS: 69
- FUGR: 7
- CLAS: 3
- DTEL: 1
- INTF: 1

**By State**:
- released: 43
- classicAPI: 35
- notToBeReleasedStable: 6

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /SAPF15/F15 | FUGR | classicAPI | PSM-FM |
| 0035 | FUGR | classicAPI | PSM-GM-GTE |
| 0036 | FUGR | classicAPI | PSM-GM-GTE |
| 0038 | FUGR | classicAPI | PSM-FM-MD |
| 0050 | FUGR | classicAPI | PSM-FM |
| 0051 | FUGR | classicAPI | PSM-FM |
| CL_BUBAS_APPL_LOG | CLAS | classicAPI | PSM-FM-BCS |
| CL_BUBAS_APPL_LOG_CTX | CLAS | classicAPI | PSM-FM-BCS |
| CL_PSM_CORE_SWITCH_CHECK | CLAS | classicAPI | PSM-FM |
| ESH_S_BDGTPER | DDLS | notToBeReleasedStable | PSM-FM-MD |
| ESH_S_FAREA | DDLS | notToBeReleasedStable | PSM-FM-MD |
| ESH_S_FUND | DDLS | notToBeReleasedStable | PSM-FM-MD |
| ESH_S_GRANT | DDLS | notToBeReleasedStable | PSM-GM-GTE-MD |
| ESH_S_SPONSOR_CL | DDLS | notToBeReleasedStable | PSM-GM-GTE-MD |
| ESH_S_SPONSOR_PR | DDLS | notToBeReleasedStable | PSM-GM-GTE-MD |
| ... | | | (69 more) |

---

### Other (SUS)

**Total APIs**: 71

**Application Components**: SUS-INT, SUS-PFM

**By Type**:
- DDLS: 32
- CLAS: 13
- DTEL: 9
- TABL: 7
- TTYP: 4

**By State**:
- released: 69
- notToBeReleasedStable: 2

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| CE_SUFND_GHG_CATEGORY | CLAS | released | SUS-INT |
| CE_SUFND_GHG_DTAQLTYCHARC | CLAS | released | SUS-INT |
| CE_SUFND_GHG_ENERGY_CLASSFCTN | CLAS | released | SUS-INT |
| CE_SUFND_GHG_ENERGY_MIX | CLAS | released | SUS-INT |
| CE_SUFND_GHG_ENGYSRCGTYPE | CLAS | released | SUS-INT |
| CE_SUFND_GHG_SCOPE | CLAS | released | SUS-INT |
| CE_SUFND_GHG_SCP2_CALC_METH | CLAS | released | SUS-INT |
| CE_SUFND_GHG_SCP2_CONTR_INSTR | CLAS | released | SUS-INT |
| CE_SUFND_SUST_MODEOFTRANSPORT | CLAS | released | SUS-INT |
| CL_SUPFM_TDFP_CALC_API | CLAS | released | SUS-PFM-INT |
| CL_SUPFM_TDFP_CALC_API_FACTORY | CLAS | released | SUS-PFM-INT |
| CX_SUPFM_TDFP_CALC_API | CLAS | released | SUS-PFM-INT |
| CX_SUPFM_TDFP_CALC_API_FACTORY | CLAS | released | SUS-PFM-INT |
| IF_SUPFM_TDFP_CALC_API | INTF | released | SUS-PFM-INT |
| IF_SUPFM_TDFP_CALC_API_FACTORY | INTF | released | SUS-PFM-INT |
| ... | | | (56 more) |

---

### Enterprise Controlling

**Total APIs**: 51

**Application Components**: EC-CS, EC-PCA

**By Type**:
- DDLS: 12
- FUGR: 10
- DTEL: 10
- SUSO: 9
- TABL: 4

**By State**:
- released: 39
- noAPI: 8
- classicAPI: 2
- notToBeReleased: 2

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 0015 | FUGR | classicAPI | EC-PCA-TL-ALE |
| 1024 | FUGR | noAPI | EC-CS |
| 1025 | FUGR | noAPI | EC-CS |
| 1026 | FUGR | noAPI | EC-CS |
| 1027 | FUGR | noAPI | EC-CS |
| 1120 | FUGR | noAPI | EC-CS |
| 1121 | FUGR | noAPI | EC-CS |
| 1122 | FUGR | noAPI | EC-CS |
| 2073 | FUGR | noAPI | EC-PCA-TL-ALE |
| CEPC | TABL | notToBeReleased | EC-PCA-MD-2CL |
| CEPCT | TABL | notToBeReleased | EC-PCA-MD-2CL |
| D_PRFTCTRCHANGEVALIDITYPERIODP | DDLS | released | EC-PCA-MD-2CL |
| E_CS_BUNIT | SUSO | released | EC-CS |
| E_CS_CACTT | SUSO | released | EC-CS |
| E_CS_CONGR | SUSO | released | EC-CS |
| ... | | | (36 more) |

---

### Other (BNS)

**Total APIs**: 46

**Application Components**: BNS-ARI, BNS-CON

**By Type**:
- TABL: 16
- INTF: 13
- DTEL: 8
- TTYP: 5
- ENHS: 2

**By State**:
- released: 46

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| BUSINESSNETWORKSTATUSUPDATENOTIF_IN_WEBI | SCO2 | released | BNS-ARI-CI-S4-MM |
| CTE_BOOLEAN | DTEL | released | BNS-CON-SE-S4 |
| CTE_CONDITION_TYPE | DTEL | released | BNS-CON-SE-S4 |
| CTE_DATE | DTEL | released | BNS-CON-SE-S4 |
| CTE_FIN_POST_ITEM_TYPE | DTEL | released | BNS-CON-SE-S4-FIN |
| CTE_FND_POST_EXPENSE_TYPE | DTEL | released | BNS-CON-SE-S4 |
| CTE_OTYPE | DTEL | released | BNS-CON-SE-S4 |
| CTE_SYSTEM_KEY_NUMBER | DTEL | released | BNS-CON-SE-S4 |
| CTE_S_CB_COST_OBJECT | TABL | released | BNS-CON-SE-S4-FIN |
| CTE_S_CB_COST_OBJECT_CHANGES | TABL | released | BNS-CON-SE-S4-FIN |
| CTE_S_FIN_POST_CB_DOCUMENT | TABL | released | BNS-CON-SE-S4-FIN |
| CTE_S_FIN_POST_CB_DOC_ENTRY | TABL | released | BNS-CON-SE-S4-FIN |
| CTE_S_FIN_POST_CB_DOC_JOURNAL | TABL | released | BNS-CON-SE-S4-FIN |
| CTE_S_FIN_POST_CB_DOC_TAX | TABL | released | BNS-CON-SE-S4-FIN |
| CTE_S_FP_CB_ADDITIONAL_DATA | TABL | released | BNS-CON-SE-S4-FIN |
| ... | | | (31 more) |

---

### Other (PY)

**Total APIs**: 41

**Application Components**: PY-BR, PY-CA, PY-CZ, PY-DE, PY-ES, PY-FR, PY-LOC, PY-NPO, PY-PT, PY-SK
  ...and 3 more

**By Type**:
- FUGR: 23
- INTF: 14
- CLAS: 4

**By State**:
- classicAPI: 40
- noAPI: 1

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 0PDA1 | FUGR | classicAPI | PY-DE-NT-NI |
| 3SK2 | FUGR | classicAPI | PY-SK |
| 3SK5 | FUGR | classicAPI | PY-SK |
| 3T02 | FUGR | classicAPI | PY-CZ |
| 3T04 | FUGR | classicAPI | PY-CZ |
| 7004 | FUGR | classicAPI | PY-XX |
| 7023 | FUGR | classicAPI | PY-XX |
| CL_HRPY_DATE | CLAS | classicAPI | PY-XX |
| CL_HR_CD_MANAGER | CLAS | classicAPI | PY-XX |
| CL_HR_MOLGA | CLAS | classicAPI | PY-XX |
| CX_PYD_FND | CLAS | classicAPI | PY-XX-PYP |
| EVAL | FUGR | classicAPI | PY-CA |
| H99_WAGECOMPONENTEXT | FUGR | classicAPI | PY-XX-TL |
| HRDK | FUGR | classicAPI | PY-DE-PS |
| HRDP | FUGR | classicAPI | PY-DE-PS |
| ... | | | (26 more) |

---

### Product Lifecycle Management

**Total APIs**: 35

**Application Components**: PLM-CR, PLM-INT, PLM-WUI

**By Type**:
- DDLS: 29
- FDT0: 2
- ENHS: 1
- INTF: 1
- SMTG: 1

**By State**:
- released: 33
- deprecated: 1
- notToBeReleasedStable: 1

**Deprecated APIs** (sample):

| Name | Type | Successor |
|------|------|-----------|
| /PLMI/CR_PR_CONFIG | FDT0 | /PLMI/CR_PR_CONFIG2 |

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /PLMC/ES_DV | ENHS | released | PLM-INT-TC-2CL |
| /PLMC/IF_DV_SET_SAP_KEY | INTF | released | PLM-INT-TC-2CL |
| /PLMI/CR_PR_CONFIG2 | FDT0 | released | PLM-CR-2CL |
| /PLMI/CR_WF_NOTIF_FOR_APPROVAL | SMTG | released | PLM-CR-2CL |
| /PLMI/S_I_CR_HDR_EXT | TABL | released | PLM-CR-2CL |
| C_CHANGEMSTROBJMGMTRECORDDEX | DDLS | released | PLM-WUI-OBJ-ECN-2CL |
| C_CHANGERECDMAILTMPLFORAPPRVL | DDLS | released | PLM-CR-2CL |
| C_CHANGERECORDBOMITEMDEX | DDLS | released | PLM-CR-2CL |
| C_CHANGERECORDDESCDEX | DDLS | released | PLM-CR-2CL |
| C_CHANGERECORDDEX | DDLS | released | PLM-CR-2CL |
| C_CHANGERECORDDEX_2 | DDLS | released | PLM-CR-2CL |
| C_CHANGERECORDDOCITEMDEX | DDLS | released | PLM-CR-2CL |
| C_CHANGERECORDEMAILTEMPLATE | DDLS | released | PLM-CR-2CL |
| C_CHANGERECORDHIERARCHYDEX | DDLS | released | PLM-CR-2CL |
| C_CHANGERECORDITEMDEX_2 | DDLS | released | PLM-CR-2CL |
| ... | | | (19 more) |

---

### Other (AC)

**Total APIs**: 33

**Application Components**: AC-COB, AC-INT

**By Type**:
- DDLS: 27
- FUGR: 4
- INTF: 1
- SUSO: 1

**By State**:
- released: 28
- classicAPI: 3
- notToBeReleased: 2

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| ACC4 | FUGR | notToBeReleased | AC-INT-2CL |
| ACC6 | FUGR | classicAPI | AC-INT |
| ACC9 | FUGR | notToBeReleased | AC-INT-2CL |
| D_GLADJMTITEMPOSTJOURNALENTRYP | DDLS | released | AC-INT-2CL |
| D_GLADJMTPOSTJOURNALENTRYP | DDLS | released | AC-INT-2CL |
| D_GLADJMTREVERSEJOURNALENTRYP | DDLS | released | AC-INT-2CL |
| D_JOURNALENTRYCHANGEAPARITEMP | DDLS | released | AC-INT-2CL |
| D_JOURNALENTRYCHANGEGLITEMP | DDLS | released | AC-INT-2CL |
| D_JOURNALENTRYCHANGEPARAMETER | DDLS | released | AC-INT-2CL |
| D_JOURNALENTRYCREATED | DDLS | released | AC-INT-2CL |
| D_JOURNALENTRYPOSTAPITEMP | DDLS | released | AC-INT-2CL |
| D_JOURNALENTRYPOSTARITEMP | DDLS | released | AC-INT-2CL |
| D_JOURNALENTRYPOSTCOPAP | DDLS | released | AC-INT-2CL |
| D_JOURNALENTRYPOSTCPDP | DDLS | released | AC-INT-2CL |
| D_JOURNALENTRYPOSTCURRENCYAMTP | DDLS | released | AC-INT-2CL |
| ... | | | (18 more) |

---

### Other (MOB)

**Total APIs**: 25

**Application Components**: MOB-APP

**By Type**:
- G4BA: 9
- DTEL: 7
- IWSV: 5
- SUSO: 2
- DDLS: 1

**By State**:
- notToBeReleasedStable: 14
- released: 11

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /MERP/SDF_CDS_FORMREG | DDLS | released | MOB-APP-MAO-ERP |
| /MERP/SDF_EVENT_EMAIL_SAMPLE | SMTG | released | MOB-APP-MAO-ERP |
| /MFND/CORE_OMDO_ID_DTE | DTEL | released | MOB-APP-MAO-FND |
| /MFND/CORE_OMDO_OPERATION_DTE | DTEL | released | MOB-APP-MAO-FND |
| /MFND/CORE_TECH_ENTITY_TYP_DTE | DTEL | released | MOB-APP-MAO-FND |
| /SMFND/CORE_NO_VALID_ROLE_DTE | DTEL | released | MOB-APP-MAO-FND |
| /SMFND/IBQ_TRANS_REQ_TYP_DTE | DTEL | released | MOB-APP-MAO-FND |
| /SMFND/SYNC_OBJECT_KEY_DTE | DTEL | released | MOB-APP-MAO-FND |
| /SMFND/SYNC_OBJECT_TYPE_DTE | DTEL | released | MOB-APP-MAO-FND |
| M_MAIF_ADM | SUSO | released | MOB-APP-MAO-ERP |
| M_MAIF_CFG | SUSO | released | MOB-APP-MAO-ERP |
| UI_MAIFDYNAMICFORM | G4BA | notToBeReleasedStable | MOB-APP-MAO-ERP |
| UI_MAINTMBLAPPLCOMMSESSION | G4BA | notToBeReleasedStable | MOB-APP-MAO-ERP |
| UI_MAINTMBLAPPLDEFAULTVALUESET | G4BA | notToBeReleasedStable | MOB-APP-MAO-ERP |
| UI_MAINTMBLAPPLDTASTOREMONITOR | G4BA | notToBeReleasedStable | MOB-APP-MAO-ERP |
| ... | | | (10 more) |

---

### Other (PT)

**Total APIs**: 21

**Application Components**: PT-, PT-RC

**By Type**:
- FUGR: 12
- INTF: 6
- CLAS: 3

**By State**:
- classicAPI: 20
- noAPI: 1

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| ABSE | FUGR | noAPI | PT |
| CL_PT_ARQ_CONST | CLAS | classicAPI | PT |
| CL_PT_REQ_CONST | CLAS | classicAPI | PT |
| CL_PT_TMW_TDM_CONST | CLAS | classicAPI | PT |
| HRIL | FUGR | classicAPI | PT-RC-IW |
| HRTIM00ABSATTEXT | FUGR | classicAPI | PT |
| HRTIM00ALP | FUGR | classicAPI | PT |
| HRTIM00BAPIABSATT | FUGR | classicAPI | PT |
| HRTIM00BAPIPTWS | FUGR | classicAPI | PT |
| HRTIM00BUS7013 | FUGR | classicAPI | PT |
| HRTIM00REMINFO | FUGR | classicAPI | PT |
| HRTIM00SUBSTITUTION | FUGR | classicAPI | PT |
| IF_PT_GUI_TMW_TDE_NM_CONSTS | INTF | classicAPI | PT-RC |
| IF_PT_REQ_APPLICATION | INTF | classicAPI | PT |
| IF_PT_REQ_A_WF | INTF | classicAPI | PT |
| ... | | | (6 more) |

---

### Project Systems

**Total APIs**: 17

**Application Components**: PS-CLM, PS-PRG, PS-ST

**By Type**:
- FUGR: 15
- SUSO: 2

**By State**:
- classicAPI: 15
- released: 2

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 2001 | FUGR | classicAPI | PS-ST-OPR |
| 2002 | FUGR | classicAPI | PS-ST-OPR |
| 2054 | FUGR | classicAPI | PS-ST-OPR |
| CJ2001 | FUGR | classicAPI | PS-ST-INT |
| CJ2054 | FUGR | classicAPI | PS-ST-INT |
| CLAIMWF | FUGR | classicAPI | PS-CLM |
| CN2002 | FUGR | classicAPI | PS-ST-INT |
| CN2002_ACT | FUGR | classicAPI | PS-ST-INT |
| CNIF_CONF | FUGR | classicAPI | PS-ST-INT |
| CNIF_MAT | FUGR | classicAPI | PS-ST-INT |
| CNIF_STATUS_2001 | FUGR | classicAPI | PS-ST-OPR |
| CNIF_STATUS_2002 | FUGR | classicAPI | PS-ST-OPR |
| CNIF_STATUS_2054 | FUGR | classicAPI | PS-ST-OPR |
| C_AFKO_ACT | SUSO | released | PS-ST-OPR-NET |
| C_AFKO_DIS | SUSO | released | PS-ST-OPR-NET |
| ... | | | (2 more) |

---

### Business Warehouse

**Total APIs**: 17

**Application Components**: BW-, BW-BEX, BW-RUI, BW-WHM

**By Type**:
- CLAS: 9
- FUGR: 4
- INTF: 3
- CHKO: 1

**By State**:
- released: 12
- classicAPI: 4
- noAPI: 1

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| CI_CDS_ANALYTICS | CHKO | released | BW-BEX-OT-ODP |
| CL_LBA_ABS_QUERY | CLAS | released | BW-BEX-OT-BICS-EQ |
| CL_LBA_CDS_QUERY | CLAS | released | BW-BEX-OT-BICS-EQ |
| CL_LBA_CDS_QUERY_2STRUC | CLAS | released | BW-BEX-OT-BICS-EQ |
| CL_LBA_CDS_QUERY_4TESTING | CLAS | released | BW-BEX-OT-BICS-EQ |
| CL_LBA_STD_QUERY | CLAS | released | BW-BEX-OT-BICS-EQ |
| CL_LBA_STD_QUERY_2STRUC | CLAS | released | BW-BEX-OT-BICS-EQ |
| CX_LBA_QUERY | CLAS | released | BW-BEX-OT-BICS-EQ |
| CX_RS_NOT_FOUND | CLAS | released | BW |
| CX_RS_VCUBE_READ_ERROR | CLAS | released | BW-BEX-OT |
| IF_FPM_RUIBB_BICS_GRID_CONFIG | INTF | classicAPI | BW-RUI-FPM |
| IF_RSRTS_CDS_READ | INTF | released | BW-BEX-OT-ODP |
| IF_RSRTS_CDS_VARIABLE_CHECK | INTF | released | BW-BEX-OT-ODP |
| RSAB | FUGR | classicAPI | BW-WHM |
| RSBAPI_IOBJ | FUGR | classicAPI | BW-WHM-DBA |
| ... | | | (2 more) |

---

### Other (XX)

**Total APIs**: 17

**Application Components**: XX-INT

**By Type**:
- DDLS: 16
- IWSV: 1

**By State**:
- released: 16
- notToBeReleasedStable: 1

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| DD_CR_APIREP | DDLS | released | XX-INT-TOOLS |
| DD_CR_API_CDSVIEWS | DDLS | released | XX-INT-TOOLS |
| DD_CR_API_CILTSATTR | DDLS | released | XX-INT-TOOLS |
| DD_CR_API_DELSIRIUS | DDLS | released | XX-INT-TOOLS |
| DD_CR_API_DEPENDENCIES | DDLS | released | XX-INT-TOOLS |
| DD_CR_API_EXEMPTION | DDLS | released | XX-INT-TOOLS |
| DD_CR_API_FIORI | DDLS | released | XX-INT-TOOLS |
| DD_CR_API_INCTR | DDLS | released | XX-INT-TOOLS |
| DD_CR_CDS_VIEWS | DDLS | released | XX-INT-TOOLS |
| DD_CR_CILTS_ATTR | DDLS | released | XX-INT-TOOLS |
| DD_CR_DELIVERY_ID_SIRIUS | DDLS | released | XX-INT-TOOLS |
| DD_CR_DU_WO_INCR | DDLS | released | XX-INT-TOOLS |
| DD_CR_EXEMPTIONS | DDLS | released | XX-INT-TOOLS |
| DD_CR_FIORI | DDLS | released | XX-INT-TOOLS |
| DD_CR_INCR_DEPENDENCIES | DDLS | released | XX-INT-TOOLS |
| ... | | | (2 more) |

---

### Other (FT)

**Total APIs**: 11

**Application Components**: FT-ITR

**By Type**:
- DDLS: 8
- IWSV: 2
- DTEL: 1

**By State**:
- released: 9
- notToBeReleasedStable: 2

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| C_COMMODITYCODEFORKEYDATE | DDLS | released | FT-ITR-CLS |
| C_CONTROLCLASSFORKEYDATE | DDLS | released | FT-ITR-CLS |
| C_CSTMSTRIFNMBRFORKEYDATE | DDLS | released | FT-ITR-CLS |
| C_PRODCOMMODITYCODEFORKEYDATE | DDLS | released | FT-ITR-CLS |
| C_PRODCSTMSTRIFNMBRFORKEYDATE | DDLS | released | FT-ITR-CLS |
| C_PRODLGLCTRLCLFNFORKEYDATE | DDLS | released | FT-ITR-CLS |
| C_TRDCMPLNCDOCITMLICASSGMT | DDLS | released | FT-ITR-TRC |
| I_TRDCLASSFCTNNMBRTEXT | DDLS | released | FT-ITR-CLS |
| SLL_PROD_CMDTYCD_CLASSIFY          0001 | IWSV | notToBeReleasedStable | FT-ITR-CLS |
| SLL_PROD_CMDTYCD_RECLASSIFY        0001 | IWSV | notToBeReleasedStable | FT-ITR-CLS |
| SLL_VALIDON | DTEL | released | FT-ITR-TRC |

---

### Other (LOD)

**Total APIs**: 5

**Application Components**: LOD-ET, LOD-FSN

**By Type**:
- DTEL: 3
- FUGR: 1
- SIA2: 1

**By State**:
- released: 4
- classicAPI: 1

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| /BSNAGT/FILE | FUGR | classicAPI | LOD-FSN-AGT |
| BUKRS_PRCTR_KSTAR | SIA2 | released | LOD-FSN-AGT |
| TDE_BD_MEANSOFTRANSP | DTEL | released | LOD-ET-INT |
| TDE_BD_MEANSOFTRANSPORTID | DTEL | released | LOD-ET-INT |
| TDE_BD_MEANSOFTRANSPTYPE | DTEL | released | LOD-ET-INT |

---

### Other (ICM)

**Total APIs**: 4

**Application Components**: ICM-

**By Type**:
- FUGR: 3
- CLAS: 1

**By State**:
- classicAPI: 4

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| CACS_EXT_CC | FUGR | classicAPI | ICM |
| CACS_PS_CUST_RFC | FUGR | classicAPI | ICM |
| CACS_PS_MD_IF_RFC | FUGR | classicAPI | ICM |
| CL_CACS_APPLICATION | CLAS | classicAPI | ICM |

---

### Investment Management

**Total APIs**: 4

**Application Components**: IM-FA

**By Type**:
- FUGR: 4

**By State**:
- classicAPI: 3
- noAPI: 1

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| 1057 | FUGR | noAPI | IM-FA-IP |
| 1157 | FUGR | classicAPI | IM-FA-IP |
| 1158 | FUGR | classicAPI | IM-FA-IP |
| AIA_BAPI | FUGR | classicAPI | IM-FA-IA |

---

### Other (HAN)

**Total APIs**: 1

**Application Components**: HAN-DB

**By Type**:
- CLAS: 1

**By State**:
- classicAPI: 1

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| CL_SHDB_SELTAB | CLAS | classicAPI | HAN-DB |

---

### Other (PE)

**Total APIs**: 1

**Application Components**: PE-

**By Type**:
- FUGR: 1

**By State**:
- classicAPI: 1

**Sample APIs**:

| Name | Type | State | App Component |
|------|------|-------|---------------|
| RHVI | FUGR | classicAPI | PE |

---

## Updating This Catalog

To regenerate this catalog after updating SAP reference data:

```bash
python3 agents/business-function-mapper/generate-catalog.py
```

To add custom mappings, edit `input/sap-api-reference/custom-mappings.json`

*Generated on 2025-12-10 20:16:36*