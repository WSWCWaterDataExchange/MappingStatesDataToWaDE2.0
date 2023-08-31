# Idaho Department of Water Resources (IDWR) Regulatory Overview Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting regulatory overlay area data, made available by the [Idaho Department of Water Resources (IDWR)](https://idwr.idaho.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Rathdrum Comprehensive Aquifer Management Plan** | Rathdrum Comprehensive Aquifer Management Area based on the boundary of the Spokane Valley-Rathdrum Prairie Aquifer within Idaho. | [link](https://data-idwr.hub.arcgis.com/datasets/rathdrum-comprehensive-aquifer-management-plan/explore?location=47.653070%2C-116.087083%2C7.73) | [link](https://idwr.idaho.gov/iwrb/water-planning/camps/)
**Treasure Valley Comprehensive Aquifer Management Plan** | To delineate the TVHP study area boundary. | [link](https://data-idwr.hub.arcgis.com/datasets/IDWR::treasure-valley-comprehensive-aquifer-management-plan/explore?location=43.138851%2C-115.877224%2C7.65) | [link](https://idwr.idaho.gov/iwrb/water-planning/camps/)
**Eastern Snake Comprehensive Aquifer Management Plan** | The Eastern Snake Comprehensive Aquifer Management Plan boundary is equivalent to Area of Common Ground Water Supply (ACGWS). The ACGWS is defined in Section 37.03.11 administrative rules. | [link](https://data-idwr.hub.arcgis.com/datasets/eastern-snake-comprehensive-aquifer-management-plan/explore?location=43.322127%2C-114.298158%2C6.00) | [link](https://idwr.idaho.gov/iwrb/water-planning/camps/)

Unique files were created to be used as input.  Input files used are as follows...
- Rathdrum_Comprehensive_Aquifer_Management_Plan.shp
- Treasure_Valley_Comprehensive_Aquifer_Management_Plan.shp
- Eastern_Snake_Comprehensive_Aquifer_Management_Plan.shp


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Idaho Department of Water Resources (IDWR) Regulatory Data: https://drive.google.com/drive/folders/12-5MRIg-a-ovWx-NV24VirEI1iC8L1K8


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NMOSE's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *IDre_RegulatoryInfo Schema Mapping to WaDE.xlsx*. Several WaDE csv input files will be created in order to extract the water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_IDre_PreProcessRegulatoryData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_IDre_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: date.csv, organization.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv, sites.csv, etc.
- **3_IDre_WRSiteRegulatoryID.ipynb**: used to pair regulatory overlay information to water allocation information using an overlay on water allocation site information within the boundaries of the regulation.
- **4_IDwr_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_IDre_PreProcessRegulatoryData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- Rathdrum_Comprehensive_Aquifer_Management_Plan.shp
- Treasure_Valley_Comprehensive_Aquifer_Management_Plan.shp
- Eastern_Snake_Comprehensive_Aquifer_Management_Plan.shp

#### Outputs:
 - Pre_idMain.zip
 - P_Geometry.zip

#### Operation and Steps:
- Read in input data per shapefile, store in temp dataframes per input.
- Add information unique to each shapefile to the dataframe.
- Combine individual dataframes into single output dataframe.
- Review data for errors, check data data types.
- Extract geometry value from shp file, store in separate file *P_Geometry.zip*.
- Export output dataframe as new csv file, *Pre_idMain.csv* for tabular data and *P_Geometry.csv* for geometry data.


***
## Code File: 2_UTwr_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (date.csv, organizations.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv, sites.csv).

#### Inputs:
- Pre_idMain.zip
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
05/10/2023 | 2023


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
IDre_O1 | Idaho Department of Water Resources | Linda Davis | https://idwr.idaho.gov/ | ID 


### 3) Reporting Unit Information
Purpose: generate a list of polygon areas associated with the state agency regulatory overlay area data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *IDre_RegulatoryInfo Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitUUID* = "IDre_RU" + counter
    - *EPSGCodeCV* = 4326.
    - *ReportingUnitName* = "Eastern Snake", "Rathdrum Prairie", & "Treasure Valley" per input.
    - *ReportingUnitNativeID* = ""
    - *ReportingUnitProductVersion* = ""
    - *ReportingUnitTypeCV* = "Comprehensive Aquifer Management Plan"
    - *ReportingUnitUpdateDate* = ""
    - *StateCV* = "ID"
    - *Geometry* = extract geometry from shp file.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | EPSGCodeCV | ReportingUnitName | ReportingUnitNativeID | ReportingUnitProductVersion | ReportingUnitTypeCV | ReportingUnitUpdateDate | StateCV | Geometry 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------  
IDre_RUwade1 | 4326 | Eastern Snake | wade1	 | - | Comprehensive Aquifer Management Plan | - | ID | - | 


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
- Assign state agency data info to the *WaDE Water Regulatory Overlays* specific columns.  See *IDre_RegulatoryInfo Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = "IDre_RO" + counter
    - *OversightAgency* = "Idaho Department of Water Resources"
    - *RegulatoryDescription* = ""
    - *RegulatoryName* = "Eastern Snake", "Rathdrum Prairie", & "Treasure Valley" per input.
    - *RegulatoryOverlayNativeID* = ""
    - *RegulatoryStatusCV* = "Active"
    - *RegulatoryStatue* = ""
    - *RegulatoryStatuteLink* = "https://idwr.idaho.gov/iwrb/water-planning/camps/espa/", "https://idwr.idaho.gov/IWRB/water-planning/CAMPs/rathdrum-prairie/", "https://idwr.idaho.gov/iwrb/water-planning/camps/treasure-valley/"
    - *StatutoryEffectiveDate* = "01/01/2009"
    - *RegulatoryOverlayTypeCV* = "Comprehensive Aquifer Management Plan"
    - *WaterSourceTypeCV* = ""
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID| OversightAgency | RegulatoryDescription | RegulatoryName | RegulatoryOverlayNativeID | RegulatoryStatusCV | RegulatoryStatute | RegulatoryStatuteLink | StatutoryEffectiveDate | StatutoryEndDate | RegulatoryOverlayTypeCV | WaterSourceTypeCV 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ 
IDre_ROwade1 | Idaho Department of Water Resources | Eastern Snake CAMP | wade1 | - | Active | - | https://idwr.idaho.gov/iwrb/water-planning/camps/espa/ | 1/1/2009 | - | Comprehensive Aquifer Management Plan | Groundwater


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
- Assign state agency data info to the *WaDE Regulatory Reportingunits* specific columns.  See *IDre_RegulatoryInfo Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
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
5/17/2023 | IDre_O1 | IDre_ROwade1 | IDre_RUwade1


Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryreportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the regulatory reportingunits include the following...
- DataPublicationDate
- OrganizationUUID
- RegulatoryOverlayUUID
- ReportingUnitUUID


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Idaho Department of Water Resources (IDWR)](https://idwr.idaho.gov/).

WSWC Staff
- Adel Abdallah (Project Manager) <adelabdallah@wswc.utah.gov>
- Ryan James (Data Analysis) <rjames@wswc.utah.gov>

IDWR Staff
- Linda Davis <linda.davis@idwr.idaho.gov>
