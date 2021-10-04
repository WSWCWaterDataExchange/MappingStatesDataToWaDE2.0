# NVDWR Reguloatory Overview Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting regulatory overlay area data, made available by the [Nevada Division of Water Resources (NVDWR)](http://water.nv.gov/index.aspx), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Data Utilized
The following data was used for regulatory overlay area data...
- **State Engineers Groundwater Basin Designations (compressed zipped shapefile)**.  Special provision for designated groundwater basins (https://home-NVDWR.opendata.arcgis.com/maps/NVDWR::surface-water-standards/about)

The folllowing unique files were created to be used as input.  Input files used are as follows...
- *SE_GroundwaterBasins_DesigOrders_input.csv*.  Contains NVDWR tabular data
- *SE_GroundwaterBasins_DesigOrders.shp.*  Contains shapefile boundary information for the NVDWR areas.


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NVDWR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NV_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx*.  Seven executable code files were used to extract the NVDWR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last two code file _(RegulatoryReportingUnits_fact & RegulatoryOverlayBridge_sites_fact)_ is depended on the previous files.  Those Six code files are as follows...

- 0_NVRegulatorySourceDataPreprocess.ipynb
- 1_NVre_Date.py
- 2_NVre_Organizations.py
- 3_NVre_ReportingUnits.py
- 4_NVre_RegulatoryOverlay.py
- 5_NVre_RegulatoryReportingUnits_fact.py
- 6_NVre_RegulatoryOverlayBridge_sites_fact.py



***
### 0) Code File: 0_NVRegulatorySourceDataPreprocess.ipynb
Purpose: Pre-process the state agency input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- SE_GroundwaterBasins_DesigOrders_input.csv 
- SE_GroundwaterBasins_DesigOrders.shp

#### Outputs:
 - P_nvRegMaster.csv
 - P_nvRegGeometry.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframe.
- For NVDWR tabular data...
    - Update **BasinName** to include "Designated" if the provided basin cataogrized as a designated basin, helps prevent duplicate entries with non-designated basins with the same name.
    - Create *in_RegulatoryStatusCV* using **Designated** field as either "Designated" or "Not Designated" entries.
    - Create *in_RegulatoryDescription* using **DesigStatu** field and entries found here [link](https://www.nyecountywaterdistrict.net/161/Designated-Basins-in-Nye-County).
- For NVDWR shapefile data...
    - Use index as **OID_** field.
    - Export **OID_**, **BasinName**, & **geometry** fields to export dataframe.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file (P_nvRegMaster.csv & P_nvRegGeometry.csv respectively).



***
### 1) Code File: 1_NVre_Date.py
Purpose: generate legend of granular date used on data collection.

#### Inputs:
- None

#### Outputs:
- date.csv
- date_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Date* specific columns.
- Assign **NVDWR** info to the *WaDE Date* specific columns (this was hardcoded by hand for simplicity).
- Perform error check on output dataframe.
- Export output dataframe *date.csv*.

#### Sample Output (WARNING: not all fields shown):
Date | Year 
---------- | ---------- 
07/01/1981 | 1981



***
### 2) Code File: 2_NVre_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **NVDWR** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
NVDWR | Nevada Division of Water Resources | Brian McMenamy | http://water.nv.gov/index.aspx



***
### 3) Code File: 3_NVre_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency regulatory overlay area data.

#### Inputs:
- P_nvRegMaster.csv.csv
- P_nvRegGeometry.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *NV_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = **BasinName**
    - *ReportingUnitNativeID* =**OID_**
    - *ReportingUnitTypeCV* = "Groundwater Basin Designations"
    - *Geometry* = **geometry** from P_nvRegGeometry.csv file.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | ReportingUnitName | ReportingUnitTypeCV 
---------- | ---------- | ------------ 
NVre_RU1 | Long Valley | Groundwater Basin Designations

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV



***
### 4) Code File: 4_NVre_RegulatoryOverlay.py
Purpose: generate master sheet of regulatory overlay area information to import into WaDE 2.0.

#### Inputs:
- P_nvRegMaster.csv.csv.csv

#### Outputs:
- regulatoryoverlays.csv
- regulatoryoverlays_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Regulatory Overlays* specific columns.
- Assign state agency data info to the *WaDE Water Regulatory Overlays* specific columns.  See *NV_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *OversightAgency* = "Office of the Nevada State Engineer"
    - *RegulatoryDescription* = *in_RegulatoryDescription*, see *0_NVRegulatorySourceDataPreprocess.ipynb* for specifics.
    - *RegulatoryName* = **BasinName**
    - *RegulatoryOverlayNativeID* = **OID_**
    - *RegulatoryStatusCV* = *in_RegulatoryStatusCV*, see *0_NVRegulatorySourceDataPreprocess.ipynb* for specifics.
    - *RegulatoryStatute* = "NRS 534.120"
    - *StatutoryEffectiveDate* = "07/01/1981"
    - *RegulatoryOverlayTypeCV* = "Groundwater Basin Designations"
    - *WaterSourceTypeCV* = "groundwater"
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID | OversightAgency | RegulatoryName | RegulatoryStatusCV | StatutoryEffectiveDate
---------- | ---------- | ------------ | ------------ | ------------
NVre_RO5 | Office of the Nevada State Engineer | Pine Forest Valley | Designated | 07/01/1981

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryoverlays_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water regulatory overlays include the following...
- RegulatoryOverlayUUID
- OversightAgency
- RegulatoryDescription
- RegulatoryName
- RegulatoryStatusCV
- StatutoryEffectiveDate



***
### 5) Code File: 5_NVre_RegulatoryReportingUnits_fact.py
Purpose: generate master sheet of regulatory overlay area information and how it algins with reporting unit area information.

#### Inputs:
- P_nvRegMaster.csv.csv
- reportingunits.csv
- regulatoryoverlays.csv

#### Outputs:
- regulatoryreportingunits.csv
- regulatoryreportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Regulatory Reportingunits* specific columns.
- Assign state agency data info to the *WaDE Regulatory Reportingunits* specific columns.  See *NV_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - OrganizationUUID = "NVDWR"
    - *RegulatoryOverlayUUID* = extract from regulatoryoverlays.csv.  Match via RegulatoryOverlayNativeID, see *0_NVRegulatorySourceDataPreprocess.ipynb.ipynb* for specifics.
    - *ReportingUnitUUID* = extract from reportingunits.csv.  Match via ReportingUniNativeID, see *0_NVRegulatorySourceDataPreprocess.ipynb.ipynb* for specifics. 
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
DataPublicationDate | OrganizationUUID | RegulatoryOverlayUUID | ReportingUnitUUID 
---------- | ---------- | ------------ | ------------ 
07/01/1981 | NVDWR | NVre_RO5 | NVre_RU5

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryreportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the regulatory reportingunits include the following...
- DataPublicationDate
- OrganizationUUID
- RegulatoryOverlayUUID
- ReportingUnitUUID



***
### 6) Code File: 6_NVre_RegulatoryOverlayBridge_sites_fact.py
Purpose: generate master sheet of regulatory overlay area information and how it algins with reporting unit area information.

#### Inputs:
- regulatoryoverlays.csv
- sites.csv (from water rights data)
- OK_Sites_RegulatoryOverlay_Bridge_input.csv (generated via spatial joining water right sites to regulatory reporting units.)

#### Outputs:
- regulatoryreportingunits.csv
- regulatoryreportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *df_regToSite*.
- Populate output dataframe with *WaDE Regulatory Overlay Bridge to Site* specific columns.
- Assign state agency data info to the *WaDE Regulatory Reportingunits* specific columns.  See *NV_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = extract from regulatoryoverlays.csv.  Match via RegulatoryNativeID.
    - *SiteUUID* = extract from OK_Sites_RegulatoryOverlay_Bridge_input.csv.  Match via ReportingUnitNativeID.
- Update *RegulatoryOverlayUUID* field in water right *sites.csv* field using the newly completed *WaDE Regulatory Overlay Bridge to Site* table.
- Export updated sites dataframe as *sites_withReg.csv* to perserve source info / allow error check on updated sites table.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID | SiteUUID 
---------- | ---------- 
NVwr_S12 | NVre_RU5

and 

#### Sample Output (WARNING: not all fields shown):
SiteUUID | RegulatoryOverlayUUID | WaterSourceUUID | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
NVwr_S12 | NVre_RU5 | NVwr_WS1 | 41.786945 | -118.607224 | Unspecified



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nevada Division of Water Resources (NVDWR)](http://water.nv.gov/index.aspx).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

NVDWR Staff
- Brian McMenamy <bmcmenamy@water.nv.gov>
