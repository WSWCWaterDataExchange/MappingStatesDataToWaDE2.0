# OWRB Reguloatory Overview Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting regulatory overlay area data, made available by the [Oklahoma Water Resources Board (OWRB)](https://www.owrb.ok.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Data Utilized
The following data was used for regulatory overlay area data...
- **Surface Water Standards Details**.  Special Provision Watersheds (https://home-owrb.opendata.arcgis.com/maps/OWRB::surface-water-standards/about)

The folllowing unique files were created to be used as input.  Input files used are as follows...
- *Surface Water Standards Details_input.csv*.  Contains OWRB tabular data
- *Surface Water Standards.shp*  Contains shapefile boundary information for the OWRB areas.


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share OWRB's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *OK_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx*.  Seven executable code files were used to extract the OWRB's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last two code file _(RegulatoryReportingUnits_fact & RegulatoryOverlayBridge_sites_fact)_ is depended on the previous files.  Those Six code files are as follows...

- 0_OKRegulatorySourceDataPreprocess.ipynb
- 1_OKre_Date.py
- 2_OKre_Organizations.py
- 3_OKre_ReportingUnits.py
- 4_OKre_RegulatoryOverlay.py
- 5_OKre_RegulatoryReportingUnits_fact.py
- 6_OKre_RegulatoryOverlayBridge_sites_fact.py



***
### 0) Code File: 0_OKRegulatorySourceDataPreprocess.ipynb
Purpose: Pre-process the state agency input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- Surface Water Standards Details_input.csv
- Surface Water Standards.shp

#### Outputs:
 - P_okRegMaster.csv
 - P_okRegGeometry.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframe.
- For OWRB tabular data...
    - Create *in_OversightAgency* = WQ Management Segmen + **WQMSEG**.
- For OWRB shapefile data...
    - Export **OBJECTID**, **NAME**, & **geometry** fields to export dataframe.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file (P_okRegMaster.csv & P_okRegGeometry.csv respectively).



***
### 1) Code File: 1_OKre_Date.py
Purpose: generate legend of granular date used on data collection.

#### Inputs:
- None

#### Outputs:
- date.csv
- date_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Date* specific columns.
- Assign **OWRB** info to the *WaDE Date* specific columns (this was hardcoded by hand for simplicity).
- Perform error check on output dataframe.
- Export output dataframe *date.csv*.

#### Sample Output (WARNING: not all fields shown):
Date | Year 
---------- | ---------- 
09/22/2021 | 2021



***
### 2) Code File: 2_OKre_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **OWRB** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
OWRB | Oklahoma Water Resources Board | David Hamilton | https://www.owrb.ok.gov/



***
### 3) Code File: 3_OKre_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency regulatory overlay area data.

#### Inputs:
- P_okRegMaster.csv.csv
- P_okRegGeometry.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *OK_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = **NAME**
    - *ReportingUnitNativeID* =**OBJECTID**
    - *ReportingUnitTypeCV* = "Special Provision Watersheds"
    - *Geometry* = **geometry** from P_okRegGeometry.csv file.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

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
### 4) Code File: 4_OKre_RegulatoryOverlay.py
Purpose: generate master sheet of regulatory overlay area information to import into WaDE 2.0.

#### Inputs:
- P_okRegMaster.csv.csv.csv

#### Outputs:
- regulatoryoverlays.csv
- regulatoryoverlays_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Regulatory Overlays* specific columns.
- Assign state agency data info to the *WaDE Water Regulatory Overlays* specific columns.  See *OK_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *OversightAgency* = in_OversightAgency, see *0_OKRegulatorySourceDataPreprocess.ipynb* for specifics.
    - *RegulatoryDescription* = **TYPE_DEF**.
    - *RegulatoryName* = **TYPE_DEF**
    - *RegulatoryOverlayNativeID* = **TYPE**
    - *RegulatoryStatusCV* = "Final"
    - *RegulatoryStatute* = **TYPE_DEF**
    - *StatutoryEffectiveDate* = "09/20/2021"
    - *RegulatoryOverlayTypeCV* = "Special Provision Watersheds"
    - *WaterSourceTypeCV* = "Surface Water"
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID | OversightAgency | RegulatoryName | RegulatoryStatusCV | StatutoryEffectiveDate
---------- | ---------- | ------------ | ------------ | ------------
OKre_RO1 | WQ Management Segmen 121700 | Outstanding Resource Waters | Final | 9/20/2020

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryoverlays_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water regulatory overlays include the following...
- RegulatoryOverlayUUID
- OversightAgency
- RegulatoryDescription
- RegulatoryName
- RegulatoryStatusCV
- StatutoryEffectiveDate



***
### 5) Code File: 5_OKre_RegulatoryReportingUnits_fact.py
Purpose: generate master sheet of regulatory overlay area information and how it algins with reporting unit area information.

#### Inputs:
- P_okRegMaster.csv.csv
- reportingunits.csv
- regulatoryoverlays.csv

#### Outputs:
- regulatoryreportingunits.csv
- regulatoryreportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Regulatory Reportingunits* specific columns.
- Assign state agency data info to the *WaDE Regulatory Reportingunits* specific columns.  See *OK_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - OrganizationUUID = "OWRB"
    - *RegulatoryOverlayUUID* = extract from regulatoryoverlays.csv.  Match via in_RegulatoryName, see *0_OKRegulatorySourceDataPreprocess.ipynb.ipynb* for specifics.
    - *ReportingUnitUUID* = extract from reportingunits.csv.  Match via in_ReportingUnitName, see *0_OKRegulatorySourceDataPreprocess.ipynb.ipynb* for specifics. 
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
DataPublicationDate | OrganizationUUID | RegulatoryOverlayUUID | ReportingUnitUUID 
---------- | ---------- | ------------ | ------------ 
9/20/2020 | OWRB | OKre_RO1 | OKre_RU1

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryreportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the regulatory reportingunits include the following...
- DataPublicationDate
- OrganizationUUID
- RegulatoryOverlayUUID
- ReportingUnitUUID



***
### 6) Code File: 6_OKre_RegulatoryOverlayBridge_sites_fact.py
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
- Assign state agency data info to the *WaDE Regulatory Reportingunits* specific columns.  See *OK_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = extract from regulatoryoverlays.csv.  Match via in_RegulatoryNativeID.
    - *SiteUUID* = extract from OK_Sites_RegulatoryOverlay_Bridge_input.csv.  Match via in_ReportingUnitNativeID.
- Update *RegulatoryOverlayUUID* field in water right *sites.csv* field using the newly completed *WaDE Regulatory Overlay Bridge to Site* table.
- Export updated sites dataframe as *sites_withReg.csv* to perserve source info / allow error check on updated sites table.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID | SiteUUID 
---------- | ---------- 
OKwr_S45 | OKre_RO2

and 

#### Sample Output (WARNING: not all fields shown):
SiteUUID | RegulatoryOverlayUUID | WaterSourceUUID | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
OKre_RO2 | OKwr_S45 | OKwr_WS90 | 36.57746246 | -102.19821153 | Unspecified



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Oklahoma Water Resources Board (OWRB)](https://www.owrb.ok.gov/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

OWRB Staff
- David Hamilton <david.hamilton@owrb.ok.gov>
