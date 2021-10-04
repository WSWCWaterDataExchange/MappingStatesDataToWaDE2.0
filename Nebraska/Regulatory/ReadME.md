# NARD Reguloatory Overview Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting regulatory overlay area data, made available by the [Nebraska Association of Resources Districts (NARD)](https://www.nrdnet.org/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Data Utilized
The following data was used for regulatory overlay area data...
- **Natural Resrouce Distsrict (NRD) Boundaries**.  River based districts for enviormental and groundwater regulation. https://www.nebraskamap.gov/datasets/natural-resource-district-nrd-boundaries/explore


The folllowing unique files were created to be used as input.  Input files used are as follows...
- *BND_NaturalResourceDistricts_DNR_input.csv*.  Contains tabular regulatory data for natural resource districts.
- *BND_NaturalResourceDistricts_DNR.shp*.  Shapefile of geometry of regulatory data for natural resource districts.


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NARD's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NE_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx*.  Seven executable code files were used to extract the NARD's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last two code file _(RegulatoryReportingUnits_fact & RegulatoryOverlayBridge_sites_fact)_ is depended on the previous files.  Those Six code files are as follows...

- 0_NERegulatorySourceDataPreprocess.ipynb
- 1_NEre_Date.py
- 2_NEre_Organizations.py
- 3_NEre_ReportingUnits.py
- 4_NEre_RegulatoryOverlay.py
- 5_NEre_RegulatoryReportingUnits_fact.py
- 6_NEre_RegulatoryOverlayBridge_sites_fact.py



***
### 0) Code File: 0_NERegulatorySourceDataPreprocess.ipynb
Purpose: Pre-process the state agency input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- BND_NaturalResourceDistricts_DNR_input.csv
- BND_NaturalResourceDistricts_DNR.shp

#### Outputs:
 - P_neRegMaster.csv
 - P_neRegGeometry.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframe.
- For Tabular Data...
    - Check datatype of **NRD_Name_A** and **NRD_Num**.
    - Create WaDE specific *RegulatoryStatuteLink* using url info found here: https://www.nrdnet.org/
- For shapefile data...
    - Export **OBJECTID**, **NRD_Name**, & **geometry** fields to export dataframe.
- Inspect output dataframes for additional errors / datatypes.
- Export output dataframe as new csv file, *P_neRegMaster.csv* & *P_neRegGeometry.csv*.



***
### 1) Code File: 1_NEre_Date.py
Purpose: generate legend of granular date used on data collection.

#### Inputs:
- None

#### Outputs:
- date.csv
- date_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Date* specific columns.
- Assign **NARD** info to the *WaDE Date* specific columns (this was hardcoded by hand for simplicity).
- Perform error check on output dataframe.
- Export output dataframe *date.csv*.

#### Sample Output (WARNING: not all fields shown):
Date | Year 
---------- | ---------- 
8/24/2021 | 2021



***
### 2) Code File: 2_NEre_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **NARD** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
NARD | Nebraska Association of Resources Districts | Office | https://www.nrdnet.org/



***
### 3) Code File: 3_NEre_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency regulatory overlay area data.

#### Inputs:
- P_neRegMaster.csv
- P_neRegGeometry.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *NE_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = **NRD_Name_A**
    - *ReportingUnitNativeID* =**NRD_Num**
    - *ReportingUnitTypeCV* = "Natural Resources Districts"
    - *Geometry* = exract from *P_neRegGeometry.csv* file using **OBJECTID** field.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | ReportingUnitName | ReportingUnitTypeCV 
---------- | ---------- | ------------ 
NEre_RU1 | Central Platte | Natural Resources Districts

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV



***
### 4) Code File: 4_NEre_RegulatoryOverlay.py
Purpose: generate master sheet of regulatory overlay area information to import into WaDE 2.0.

#### Inputs:
- P_neRegMaster.csv.csv

#### Outputs:
- regulatoryoverlays.csv
- regulatoryoverlays_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Regulatory Overlays* specific columns.
- Assign state agency data info to the *WaDE Water Regulatory Overlays* specific columns.  See *NE_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *OversightAgency* = **NRD_Name_A** + "NRD"
    - *RegulatoryDescription* = "Natural Resources Districts were created to solve flood control, soil erosion, irrigation run-off, and groundwater quantity and quality issues. Nebraska's NRDs are involved in a wide variety of projects and programs to conserve and protect the state's natural resources. NRDs are charged under state law with 12 areas of responsibility including flood control, soil erosion, groundwater management and many others."
    - *RegulatoryName* = **'NRD_Name_A**
    - *RegulatoryOverlayNativeID* = **NRD_Num**
    - *RegulatoryStatusCV* = "Active"
    - *RegulatoryStatute* = "Unspecified"
    - *RegulatoryStatuteLink* = *in_RegulatoryStatuteLink*, see pre-processing in *0_NERegulatorySourceDataPreprocess.ipynb* for details.
    - *StatutoryEffectiveDate* = "01/01/1972"
    - *RegulatoryOverlayTypeCV* = "Natural Resources Districts"
    - *WaterSourceTypeCV* = "Groundwater"
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID | OversightAgency | RegulatoryName | RegulatoryStatusCV | StatutoryEffectiveDate
---------- | ---------- | ------------ | ------------ | ------------
NEre_RO1 | Central Platte NRD | Central Platte | Active | 01/01/1972 

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryoverlays_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water regulatory overlays include the following...
- RegulatoryOverlayUUID
- OversightAgency
- RegulatoryDescription
- RegulatoryName
- RegulatoryStatusCV
- StatutoryEffectiveDate



***
### 5) Code File: 5_NEre_RegulatoryReportingUnits_fact.py
Purpose: generate master sheet of regulatory overlay area information and how it algins with reporting unit area information.

#### Inputs:
- P_neRegMaster.csv
- reportingunits.csv
- regulatoryoverlays.csv

#### Outputs:
- regulatoryreportingunits.csv
- regulatoryreportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Regulatory Reportingunits* specific columns.
- Assign state agency data info to the *WaDE Regulatory Reportingunits* specific columns.  See *NE_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - OrganizationUUID = "NARD"
    - *RegulatoryOverlayUUID* = extract from regulatoryoverlays.csv.  Match via in_RegulatoryName, see *0_NERegulatorySourceDataPreprocess.ipynb.ipynb* for specifics.
    - *ReportingUnitUUID* = extract from reportingunits.csv.  Match via in_ReportingUnitName, see *0_NERegulatorySourceDataPreprocess.ipynb.ipynb* for specifics. 
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
DataPublicationDate | OrganizationUUID | RegulatoryOverlayUUID | ReportingUnitUUID 
---------- | ---------- | ------------ | ------------ 
8/12/2021 | NARD | NEre_RO1 | NEre_RU1

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
NEre_RO3 | NEwr_S1

and 

#### Sample Output (WARNING: not all fields shown):
SiteUUID | RegulatoryOverlayUUID | WaterSourceUUID | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
NEwr_S1 | NEre_RO3  | NEwr_WS1 | 40.01104072 | -97.5223804 | Unspecified



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nebraska Association of Resources Districts (NARD)](https://www.nrdnet.org/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

NARD Staff
- asfd
