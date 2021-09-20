# CDWR Reguloatory Overview Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting regulatory overlay area data, made available by the [California Department of Water Resources (CDWR)](https://water.ca.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Data Utilized
The following data was used for regulatory overlay area data...
- **Sustainable Groundwater Management Act (SGMA) Basin Prioritization**.  Data and information to classify California’s 515 groundwater basins into one of four categories (high, medium, low, or very low).  Data acquired incldues both 1) tabular summary informatoin and 2) shapefile boundary information.  https://data.cnra.ca.gov/dataset/sgma-basin-prioritization


The folllowing unique files were created to be used as input.  Input files used are as follows...
- *sgma_2019_basin_prioritization_dashboard_data.xlsx*.  Contains SGMA tabular data
- *2019_SGMA_Basins.shp*  Contains shapefile boundary information for SGMA areas.


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CDWR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *CA_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx*.  Seven executable code files were used to extract the CDWR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last two code file _(RegulatoryReportingUnits_fact & RegulatoryOverlayBridge_sites_fact)_ is depended on the previous files.  Those Six code files are as follows...

- 0_CARegulatorySourceDataPreprocess.ipynb
- 1_CAre_Date.py
- 2_CAre_Organizations.py
- 3_CAre_ReportingUnits.py
- 4_CAre_RegulatoryOverlay.py
- 5_CAre_RegulatoryReportingUnits_fact.py
- 6_CAre_RegulatoryOverlayBridge_sites_fact.py



***
### 0) Code File: 0_CARegulatorySourceDataPreprocess.ipynb
Purpose: Pre-process the state agency input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- sgma_2019_basin_prioritization_dashboard_data.xlsx.
- 2019_SGMA_Basins.shp

#### Outputs:
 - P_caRegMaster.csv
 - P_caRegGeometry.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframe.
- For SGMA tabular data...
    - Covert abbrevaited **Region_Office** to full name: Northern Region Office, Southern Region Office, North Central Region Office, & South Central Region Office
    - Export **Basin_Subbasin_Number**, **Basin_Subbasin_Name**, **Priority**, & **Region_Office** fields to export dataframe.
- For SGMA shapefile data...
    - Export **Basin_Subb**, **Basin_Su_1**, & **geometry** fields to export dataframe.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file (P_caRegMaster.csv & P_caRegGeometry.csv respectively).



***
### 1) Code File: 1_CAre_Date.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- date.csv
- date_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Date* specific columns.
- Assign **CDWR** info to the *WaDE Date* specific columns (this was hardcoded by hand for simplicity).
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
Date | Year 
---------- | ---------- 
8/26/2021 | 2021



***
### 2) Code File: 2_CAre_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **CDWR** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
CDWR | California Department of Water Resources | Jennifer Stricklin | https://water.ca.gov



***
### 3) Code File: 3_CAre_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency regulatory overlay area data.

#### Inputs:
- P_caRegMaster.csv.csv
- P_caRegGeometry.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *CA_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = **Basin_Subbasin_Name**
    - *ReportingUnitNativeID* =**Basin_Subbasin_Number**
    - *ReportingUnitTypeCV* = "Sustainable Groundwater Management Act Basin"
    - *Geometry* = **geometry** from P_caRegGeometry.csv file.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | ReportingUnitName | ReportingUnitTypeCV 
---------- | ---------- | ------------ 
CAre_RU1 | Smith River Plain |Sustainable Groundwater Management Act Basin

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV



***
### 4) Code File: 4_CAre_RegulatoryOverlay.py
Purpose: generate master sheet of regulatory overlay area information to import into WaDE 2.0.

#### Inputs:
- P_caRegMaster.csv.csv.csv

#### Outputs:
- regulatoryoverlays.csv
- regulatoryoverlays_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Regulatory Overlays* specific columns.
- Assign state agency data info to the *WaDE Water Regulatory Overlays* specific columns.  See *CA_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *OversightAgency* = in_OversightAgency, see *0_CARegulatorySourceDataPreprocess.ipynb* for specifics.
    - *RegulatoryDescription* = "Each basin’s priority (high, medium, low, or very low) determines which provisions of California Statewide Groundwater Elevation Monitoring (CASGEM) and the Sustainable Groundwater Management Act (SGMA) apply.  SGMA requires medium- and high-priority basins to develop groundwater sustainability agencies (GSAs), develop groundwater sustainability plans (GSPs) and manage groundwater for long-term sustainability."
    - *RegulatoryName* = **Basin_Subbasin_Name**
    - *RegulatoryOverlayNativeID* = **Basin_Subbasin_Number**
    - *RegulatoryStatusCV* = "Final"
    - *RegulatoryStatuteLink* = "https://water.ca.gov/Programs/Groundwater-Management/Basin-Prioritization"
    - *StatutoryEffectiveDate* = "01/01/2019"
    - *RegulatoryOverlayTypeCV* = "Sustainable Groundwater Management Act Basin"
    - *WaterSourceTypeCV* = "Groundwater"
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID | OversightAgency | RegulatoryName | RegulatoryStatusCV | StatutoryEffectiveDate
---------- | ---------- | ------------ | ------------ | ------------
CAre_RO1 | North Region Office | Smith River Plain | Final | 01/01/2019

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryoverlays_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water regulatory overlays include the following...
- RegulatoryOverlayUUID
- OversightAgency
- RegulatoryDescription
- RegulatoryName
- RegulatoryStatusCV
- StatutoryEffectiveDate



***
### 5) Code File: 5_CAre_RegulatoryReportingUnits_fact.py
Purpose: generate master sheet of regulatory overlay area information and how it algins with reporting unit area information.

#### Inputs:
- P_caRegMaster.csv.csv
- reportingunits.csv
- regulatoryoverlays.csv

#### Outputs:
- regulatoryreportingunits.csv
- regulatoryreportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Regulatory Reportingunits* specific columns.
- Assign state agency data info to the *WaDE Regulatory Reportingunits* specific columns.  See *CA_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - OrganizationUUID = "CDWR"
    - *RegulatoryOverlayUUID* = extract from regulatoryoverlays.csv.  Match via in_RegulatoryName, see *0_CARegulatorySourceDataPreprocess.ipynb.ipynb* for specifics.
    - *ReportingUnitUUID* = extract from reportingunits.csv.  Match via in_ReportingUnitName, see *0_CARegulatorySourceDataPreprocess.ipynb.ipynb* for specifics. 
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
DataPublicationDate | OrganizationUUID | RegulatoryOverlayUUID | ReportingUnitUUID 
---------- | ---------- | ------------ | ------------ 
8/26/2021 | CDWR | CAre_RO1 | CAre_RU1

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryreportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the regulatory reportingunits include the following...
- DataPublicationDate
- OrganizationUUID
- RegulatoryOverlayUUID
- ReportingUnitUUID



***
### 6) Code File: 6_CAre_RegulatoryOverlayBridge_sites_fact.py
Purpose: generate master sheet of regulatory overlay area information and how it algins with reporting unit area information.

#### Inputs:
- regulatoryoverlays.csv
- sites.csv (from water rights data)
- CA_Sites_RegulatoryOverlay_Bridge_input.csv (generated via spatial joining water right sites to regulatory reporting units.)

#### Outputs:
- regulatoryreportingunits.csv
- regulatoryreportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *df_regToSite*.
- Populate output dataframe with *WaDE Regulatory Overlay Bridge to Site* specific columns.
- Assign state agency data info to the *WaDE Regulatory Reportingunits* specific columns.  See *CA_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = extract from regulatoryoverlays.csv.  Match via in_RegulatoryNativeID.
    - *SiteUUID* = extract from CA_Sites_RegulatoryOverlay_Bridge_input.csv.  Match via in_ReportingUnitNativeID.
- Update *RegulatoryOverlayUUID* field in water right *sites.csv* field using the newly completed *WaDE Regulatory Overlay Bridge to Site* table.
- Export updated sites dataframe as *sites_withReg.csv* to perserve source info / allow error check on updated sites table.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID | SiteUUID 
---------- | ---------- 
CAre_RO1 | CAwr_S11717

and 

#### Sample Output (WARNING: not all fields shown):
SiteUUID | RegulatoryOverlayUUID | WaterSourceUUID | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
CAwr_S11717 | CAre_RO1  | CAwr_WS247 | 41.82726506 | -124.10358562 | Unspecified



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [California Department of Water Resources (CDWR)](https://water.ca.gov/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

CDWR Staff
- asfd
