# Montana Department of Natural Resources Overlay Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting overlay area data, made available by the [Montana Department of Natural Resources]("https://opendata-mtdnrc.hub.arcgis.com/datasets/MTDNRC::conservation-districts/explore?location=47.204471%2C-109.325843%2C6.61"), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Source Data Utilized
The following data was used for overlays...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Groundwater Conservation Districts** | description of data | [link]("https://opendata-mtdnrc.hub.arcgis.com/datasets/MTDNRC::conservation-districts/explore?location=47.204471%2C-109.325843%2C6.61") | Not Provided

Input files used are as follows...
- Groundwater_Conservation_Districts.shp


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Montana Overlay Data: [link](https://drive.google.com/drive/folders/1HWY-AZZYO7zJfQoRnVPYy6N_pYJOyqGJ?usp=drive_link)


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share overlay data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *MTov_Overlay Info Schema Mapping to WaDE.xlsx*. Several WaDE csv input files will be created in order to extract the overlay data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_MTov_PreProcessRegulatoryData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_MTov_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: date.csv, organization.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv, etc.
- **3_MTov_WRSiteRegulatoryID.ipynb**: used to pair overlay information to water allocation information using an overlay on water allocation site information within the boundaries of the regulation.
- **4_MTov_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_MTov_PreProcessRegulatoryData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- "Conservation_Districts.shp"

#### Outputs:
 - Pre_mtMain.zip
 - P_Geometry.zip

#### Operation and Steps:
- Read in shapefile info.
- Extract native ID, type, geometry fields.
- Export output dataframe as new csv file, *Pre_mtMain.zip* for tabular data and *P_Geometry.csv* for geometry data.


***
## Code File: 2_MTov_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv).

#### Inputs:
- Pre_mtMain.zip
- P_Geometry.zip

#### Outputs:
- date.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- organizations.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- reportingunits.csv
- regulatoryoverlays.csv 
- regulatoryreportingunits.csv



## 1) Date Information
Purpose: generate legend of granular date used on data collection.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Date* specific columns.
- Assign agency info to the *WaDE Date* specific columns (this was hardcoded by hand for simplicity).
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
Date | Year 
---------- | ---------- 
8/2/2023 | 2023


## 2) Organization Information
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign agency info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite | State
---------- | ---------- | ------------ | ------------ | ------------
MTov_O1 | Montana Department of Natural Resources | Mark Bostram | https://dnrc.mt.gov/ | MT 


### 3) Reporting Unit Information
Purpose: generate a list of polygon areas associated with the state agency overlay area data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *MTov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitUUID* = MTov + **OBJECTID** input.
    - *EPSGCodeCV* = 4326.
    - *ReportingUnitName* = **MACD_NAME** input.
    - *ReportingUnitNativeID* = **OBJECTID** input.
    - *ReportingUnitProductVersion* = ""
    - *ReportingUnitTypeCV* = "Conservation Districts"
    - *ReportingUnitUpdateDate* = "9/21/2021"
    - *StateCV* = "MT"
    - *Geometry* = "geometry" input.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | EPSGCodeCV | ReportingUnitName | ReportingUnitNativeID | ReportingUnitProductVersion | ReportingUnitTypeCV | ReportingUnitUpdateDate | StateCV 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------   
MTov_RUMTov1 | 4326 | Northeast | MTov1 | - | Conservation Districts | 9/21/2021 | MT 

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV


### 4) Overlays Information
Purpose: generate master sheet of overlay area information to import into WaDE 2.0.

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Overlays* specific columns.
- Assign state agency data info to the *WaDE Water Overlays* specific columns.  See *MTov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = "MTov_0" + **OBJECTID** input.
    - *OversightAgency* = "Montana Department of Natural Resources"
    - *RegulatoryDescription* = "Help citizens conserve their soil, water, and other renewable natural resources."
    - *RegulatoryName* = **MACD_NAME** input.
    - *RegulatoryOverlayNativeID* = **OBJECTID**
    - *RegulatoryStatusCV* = "Active"
    - *RegulatoryStatue* = ""
    - *RegulatoryStatuteLink* = ""
    - *StatutoryEffectiveDate* = **ORG_DATE** input.
    - *RegulatoryOverlayTypeCV* = "Conservation District".
    - *WaterSourceTypeCV* = "Surface Water".
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID| OversightAgency | RegulatoryDescription | RegulatoryName | RegulatoryOverlayNativeID | RegulatoryStatusCV | RegulatoryStatute | RegulatoryStatuteLink | StatutoryEffectiveDate | StatutoryEndDate | RegulatoryOverlayTypeCV | WaterSourceTypeCV | WaDEUUID
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
MTov_RO10 | Montana Department of Natural Resources | Help citizens conserve their soil, water, and other renewable natural resources. | North Central | 10 | Active | - | - | 12/27/1947 | - | Conservation District | Surface Water 

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryoverlays_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water overlays include the following...
- RegulatoryOverlayUUID
- OversightAgency
- RegulatoryDescription
- RegulatoryName
- RegulatoryStatusCV
- StatutoryEffectiveDate


### 5) Reporting Units Information 
Purpose: generate master sheet of overlay area information and how it algins with reporting unit area information.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Reportingunits* specific columns.
- Assign state agency data info to the *WaDE Reportingunits* specific columns.  See *MTov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    -*DataPublicationDate* = ""
    - *OrganizationUUID* = ""
    - *RegulatoryOverlayUUID* = ""
    - *ReportingUnitUUID* = ""
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
DataPublicationDate | OrganizationUUID | RegulatoryOverlayUUID | ReportingUnitUUID 
---------- | ---------- | ------------ | ------------ 
8/7/2023 | MTov_01 | MTov_RO1 | MTov_RUMTov1


Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryreportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- DataPublicationDate
- OrganizationUUID
- RegulatoryOverlayUUID
- ReportingUnitUUID


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Montana Department of Natural Resources]("https://opendata-mtdnrc.hub.arcgis.com/datasets/MTDNRC::conservation-districts/explore?location=47.204471%2C-109.325843%2C6.61").

WSWC Staff
- Ryan James (Data Analysis) <rjames@wswc.utah.gov>