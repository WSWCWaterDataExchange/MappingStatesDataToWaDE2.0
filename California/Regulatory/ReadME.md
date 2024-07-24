# California Department of Water Resources (CDWR) Regulatory Overview Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting regulatory overlay area data, made available by the [California Department of Water Resources (CDWR)](https://water.ca.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Sustainable Groundwater Management Act (SGMA) Basin Prioritization** | SGMA Basin Prioritization of California’s 515 groundwater basins and subbasins. The Department of Water Resources is mandated by California Water Code Section 10933(b) to prioritize each basin based on eight components. | [link](https://data.cnra.ca.gov/dataset/sgma-basin-prioritization) | [link](https://data.cnra.ca.gov/dataset/sgma-basin-prioritization/resource/ffafd27b-5e7e-4db3-b846-e7b3cb5c614c)
**Sustainable Groundwater Management Act (SGMA)** | Shpe file information for Sustainable Groundwater Management Act (SGMA). | [link](https://data.cnra.ca.gov/dataset/sgma-basin-prioritization/resource/ffafd27b-5e7e-4db3-b846-e7b3cb5c614c) | not provided

Unique files were created to be used as input.  Input files used are as follows...
- sgma_2019_basin_prioritization_dashboard_data.csv
- 2019_SGMA_Basins.shp


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- California Department of Water Resources (CDWR) Regulatory Data: [link](https://drive.google.com/drive/folders/1OazP2MAU8ALg-tJ_bBUk6VFFPnVUosvH)


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share the state's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *CAre_RegulatoryInfo Schema Mapping to WaDE.xlsx*. Several WaDE csv input files will be created in order to extract the water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_CAe_PreProcessRegulatoryData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_CAre_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: date.csv, organization.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv, sites.csv, etc.
- **3_CAre_WRSiteRegulatoryID.ipynb**: used to pair regulatory overlay information to water allocation information using an overlay on water allocation site information within the boundaries of the regulation.
- **4_CAre_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_CAe_PreProcessRegulatoryData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- 2019_SGMA_Basins.shp

#### Outputs:
 - Pre_caMain.zip
 - P_Geometry.zip

#### Operation and Steps:
- read in input files, place into temporary dataframes.
- extract values for WaDE specific elements.
- Translate **Region_Office** input out of abbreviation format. "NRO" : "Northern Region Office", "SRO" : "Southern Region Office", "NCRO" : "North Central Region Office", "SCRO" : "South Central Region Office"
- Extract geometry information form shp file.
- Export output dataframe as new csv file, *Pre_caMain.csv* for tabular data and *P_Geometry.csv* for geometry data.


***
## Code File: 2_UTwr_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (date.csv, organizations.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv, sites.csv).

#### Inputs:
- Pre_caMain.zip
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
9/10/2023 | 2023


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
OrganizationUUID | OrganizationContactEmail | OrganizationContactName | OrganizationName | OrganizationPhoneNumber | OrganizationPurview | OrganizationWebsite | State
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
CAre_O1 | Jennifer.Stricklin@water.ca.gov | Jennifer Stricklin | California Department of Water Resources | 303-866-3581 | Department of Water Resources California Water Plan program computes applied, net, and depletion water balances for California. | https://water.ca.gov/ | CA



### 3) Reporting Unit Information
Purpose: generate a list of polygon areas associated with the state agency regulatory overlay area data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *CAre_RegulatoryInfo Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitUUID* = CAre_RU + **Basin_Subbasin_Number** input.
    - *EPSGCodeCV* = 4326.
    - *ReportingUnitName* = **Basin_Subbasin_Name** input.
    - *ReportingUnitNativeID* = **Basin_Subbasin_Number** input.
    - *ReportingUnitProductVersion* = ""
    - *ReportingUnitTypeCV* = "Sustainable Groundwater Management Act Basin"
    - *ReportingUnitUpdateDate* = ""
    - *StateCV* = "CA"
    - *Geometry* = extract from shp file, match **Basin_Subbasin_Number** input -to- **Basin_Subb** from shp input.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | EPSGCodeCV | ReportingUnitName | ReportingUnitNativeID | ReportingUnitProductVersion | ReportingUnitTypeCV | ReportingUnitUpdateDate | StateCV 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------  
CAre_RUca1001 | 4326 | Smith River Plain | ca1-001 | - | Sustainable Groundwater Management Act Basin | - | CA

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV


### 4) Regulatory Overlays Information
Purpose: generate master sheet of regulatory overlay area information to import into WaDE 2.0.

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Regulatory Overlays* specific columns.
- Assign state agency data info to the *WaDE Water Regulatory Overlays* specific columns.  See *CAre_RegulatoryInfo Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = "CAre_RO" + **Basin_Subbasin_Number** input.
    - *OversightAgency* = **Region_Office** input, see above 1_CAe_PreProcessRegulatoryData.ipynb for specifics.
    - *RegulatoryDescription* = "Each basin’s priority (e.g., high, medium, low, or very low) determines which provisions of California Statewide Groundwater Elevation Monitoring (CASGEM) and the Sustainable Groundwater Management Act (SGMA) apply.  SGMA requires medium- and high-priority basins to develop groundwater sustainability agencies (GSAs), develop groundwater sustainability plans (GSPs) and manage groundwater for long-term sustainability."
    - *RegulatoryName* = **Basin_Subbasin_Name** input.
    - *RegulatoryOverlayNativeID* = **Basin_Subbasin_Number** input.
    - *RegulatoryStatusCV* = "Final"
    - *RegulatoryStatue* = **Priority** input.
    - *RegulatoryStatuteLink* = "https://water.ca.gov/Programs/Groundwater-Management/Basin-Prioritization"
    - *StatutoryEffectiveDate* = "01/01/2019"
    - *RegulatoryOverlayTypeCV* = "Sustainable Groundwater Management Act Basin"
    - *WaterSourceTypeCV* = "Groundwater"
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID| OversightAgency | RegulatoryDescription | RegulatoryName | RegulatoryOverlayNativeID | RegulatoryStatusCV | RegulatoryStatute | RegulatoryStatuteLink | StatutoryEffectiveDate | StatutoryEndDate | RegulatoryOverlayTypeCV | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
CAre_RO4005 | Southern Region Office | Each basins priority (e.g., high, medium, low, or very low) determines which provisions of California Statewide Groundwater Elevation Monitoring (CASGEM) and the Sustainable Groundwater Management Act (SGMA) apply.  SGMA requires medium- and high-priority basins to develop groundwater sustainability agencies (GSAs), develop groundwater sustainability plans (GSPs) and manage groundwater for long-term sustainability. | Acton Valley | 4-005 | Final | Very Low | https://water.ca.gov/Programs/Groundwater-Management/Basin-Prioritization | 1/1/2019 | - | Sustainable Groundwater Management Act Basin | Groundwater


Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryoverlays_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water regulatory overlays include the following...
- RegulatoryOverlayUUID
- OversightAgency
- RegulatoryDescription
- RegulatoryName
- RegulatoryStatusCV
- StatutoryEffectiveDate


### 5) Regulatory Reporting Units Information 
Purpose: generate master sheet of regulatory overlay area information and how it algins with reporting unit area information.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Regulatory Reportingunits* specific columns.
- Assign state agency data info to the *WaDE Regulatory Reportingunits* specific columns.  See *CAre_RegulatoryInfo Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *DataPublicationDate* = use date of file creation
    - *OrganizationUUID* = pull from organization.csv
    - *RegulatoryOverlayUUID* = pull form regulatoryoverlay.csv
    - *ReportingUnitUUID* = pull from reportingunit.csv
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
DataPublicationDate | OrganizationUUID | RegulatoryOverlayUUID | ReportingUnitUUID 
---------- | ---------- | ------------ | ------------ 
9/10/2023 | CAre_O1 | CAre_RO1001 | CAre_RUca1001

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryreportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the regulatory reportingunits include the following...
- DataPublicationDate
- OrganizationUUID
- RegulatoryOverlayUUID
- ReportingUnitUUID


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [California Department of Water Resources (CDWR)](https://water.ca.gov/).

WSWC Staff
- Ryan James (Data Analysis) <rjames@wswc.utah.gov>

California Department of Water Resources (CDWR) Staff
- Jennifer Stricklin <Jennifer.Stricklin@water.ca.gov>
