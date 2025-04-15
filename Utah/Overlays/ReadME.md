# Utah Department of Natural Resources Overlay Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting overlay area data, made available by the [Utah Department of Natural Resources](https://naturalresources.utah.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Utah Water Right Areas** | Water Right Areas Service, where administrative boundaries based primarily on surface drainage areas.  | [link](https://opendata.gis.utah.gov/datasets/utahDNR::utah-water-right-areas/about) | Not Provided
**Groundwater Policy Management** | Areas throughout Utah to promote wise use of the ground-water, protect existing water rights, and address water quality issues and over-appropriation of ground water. | Emailed through personal correspondence with state | [link](https://www.waterrights.utah.gov/groundwater/)
**BasinsClosedToNewAppropriations** | Water Right areas / basins closed to new appropriations. | Emailed through personal correspondence with state | Not Provided
**AreasOpenToLimitedAppropriation** | Water Right Areas with limited new appropriations. | Emailed through personal correspondence with state | Not Provided

Unique files were created to be used as input.  Input files used are as follows...
- WaterRightAreasServiceView.zip (zipped shp & dbf files)
- ground_water_policy.zip (zipped shp & dbf files)
- BasinsClosedToNewAppropriations (zipped shp & dbf files)
- AreasOpenToLimitedAppropriation.zip (zipped shp & dbf files)


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Utah Department of Natural Resources Overlay Data: [link](https://drive.google.com/drive/folders/1zXz1qOKe2I20L_Oov5gIBxGeDyuz4Ynk?usp=drive_link)


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share the state's overlay data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *UTov_Overlay Info Schema Mapping to WaDE.xlsx*. Several WaDE csv input files will be created in order to extract the overlay data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_UTov_PreProcessRegulatoryData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_UTov_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: date.csv, organization.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv, etc.
- **3_UTov_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_UTov_PreProcessRegulatoryData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- WaterRightAreasServiceView.zip (zipped shp & dbf files)
- ground_water_policy.zip (zipped shp & dbf files)
- BasinsClosedToNewAppropriations (zipped shp & dbf files)
- AreasOpenToLimitedAppropriation.zip (zipped shp & dbf files)

#### Outputs:
 - Pov_Main.zip
 - P_Geometry.zip

#### Operation and Steps:
- Read in each data source and store into temporary dataframes.
- Extract key WadE information needed from each source, combine into single output dataframe outdf.
- Clean & inspect the data (remove special characters, round float values, remove white space between strings).
- Extract geometry values from temporary dataframes, save as P_Geometry df.
- Export output dataframe as new csv file, *Pov_Main.csv* for tabular data and *P_Geometry.csv* for geometry data


***
## Code File: 2_UTov_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (date.csv, organizations.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv.

#### Inputs:
- Pov_Main.zip
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
|    | Date       |   Year |
|---:|:-----------|-------:|
|  0 | 12/10/2023 |   2023 |


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
|    | OrganizationUUID   | OrganizationContactEmail   | OrganizationContactName                                   | OrganizationName              | OrganizationPhoneNumber   | OrganizationPurview                                                                                                                                                                                                    | OrganizationWebsite     | State   |
|---:|:-------------------|:---------------------------|:----------------------------------------------------------|:------------------------------|:--------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------|:--------|
|  0 | UTre_O1            | jreese@utah.gov            | Jim Reese (Assistant State Engineer - Technical Services) | Utah Division of Water Rights | 801-538-7280              | The Utah Division of Water Rights (DWRi) is an agency of Utah State Government within the Department of Natural Resources that administers the appropriation and distribution of the State's valuable water resources. | https://water.utah.gov/ | UT      |


### 3) Reporting Unit Information
Purpose: generate a list of polygon areas associated with the state agency overlay area data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *UTov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitUUID* = create unique it based on **AREA_CODE** input.
    - *EPSGCodeCV* = "4326".
    - *ReportingUnitName* = "WaDE Blank" (not provided)
    - *ReportingUnitNativeID* = **AREA_CODE** input.
    - *ReportingUnitProductVersion* = "" (not provided)
    - *ReportingUnitTypeCV* = "Water Right Areas", "Areas Open to Limited Appropriation", "Basins Closed to New Appropriations"
    - *ReportingUnitUpdateDate* = "5/31/2022"
    - *StateCV* = "UT"
    - *Geometry* = **geometry** input, converted to WGS 1984 coordinate.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | ReportingUnitUUID   |   EPSGCodeCV | ReportingUnitName   | ReportingUnitNativeID   | ReportingUnitProductVersion   | ReportingUnitTypeCV   | ReportingUnitUpdateDate   | StateCV   |
|---:|:--------------------|-------------:|:--------------------|:------------------------|:------------------------------|:----------------------|:--------------------------|:----------|
|  1 | UTov_RUut_05        |         4326 | WaDE Blank          | ut_05                   |                               | WaDE Blank            | 5/31/2022                 | UT        |

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
- Assign state agency data info to the *WaDE Water Overlays* specific columns.  See *UTov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = create unique it based on **AREA_CODE** input.
    - *OversightAgency* = **Office** input.
    - *RegulatoryDescription* = unique to each input file, see UTov_Overlay Info Schema Mapping to WaDE.xlsx for specifics.
    - *RegulatoryName* = '"WaDE Blank" (not provided)
    - *RegulatoryOverlayNativeID* = **AREA_CODE** input.
    - *RegulatoryStatusCV* = "Active"
    - *RegulatoryStatue* = (not provided)
    - *RegulatoryStatuteLink* = **Link** input.
    - *StatutoryEffectiveDate* = "12/10/2023" (not provided, filler value)
    - *RegulatoryOverlayTypeCV* = "Water Right Areas", "Areas Open to Limited Appropriation", "Basins Closed to New Appropriations"
    - *WaterSourceTypeCV* = "Surface Water and Groundwater"
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | RegulatoryOverlayUUID   | OversightAgency                      | RegulatoryDescription                                                                                                                                                                                                   | RegulatoryName   | RegulatoryOverlayNativeID   | RegulatoryStatusCV   | RegulatoryStatute   | RegulatoryStatuteLink                                            | StatutoryEffectiveDate   | StatutoryEndDate   | RegulatoryOverlayTypeCV   | WaterSourceTypeCV             |
|---:|:------------------------|:-------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|:----------------------------|:---------------------|:--------------------|:-----------------------------------------------------------------|:-------------------------|:-------------------|:--------------------------|:------------------------------|
|  1 | UTov_ROutr1_05          | Southeastern Regional Office (PRICE) | Water Right Areas are administrative boundaries based primarily on surface drainage areas. Different water right areas can have different appropriation policies and can be administered by different regional offices. | WaDE Blank       | utr1_05                     | Active               |                     | http://www.waterrights.utah.gov/wrinfo/policy/wrareas/area05.asp | 2023-12-10               |                    | Water Right Areas         | Surface Water and Groundwater |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryoverlays_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water overlays include the following...
- RegulatoryOverlayUUID
- OversightAgency
- RegulatoryDescription
- RegulatoryName
- RegulatoryStatusCV
- StatutoryEffectiveDate


### 5) Overlay Reporting Units Information
Purpose: generate master sheet of overlay area information and how it algins with reporting unit area information.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE OverlayReportingunits* specific columns.
- Assign state agency data info to the *WaDE OverlayReportingunits* specific columns.  See *UTov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *DataPublicationDate* = use date of file creation
    - *OrganizationUUID* = pull from organization.csv
    - *RegulatoryOverlayUUID* = pull form regulatoryoverlay.csv
    - *ReportingUnitUUID* = pull from reportingunit.csv
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | DataPublicationDate   | OrganizationUUID   | RegulatoryOverlayUUID   | ReportingUnitUUID   |
|---:|:----------------------|:-------------------|:------------------------|:--------------------|
|  1 | 2025-04-15            | UTov_O1            | UTov_ROutr1_81          | UTov_RUut_81        |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryreportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- DataPublicationDate
- OrganizationUUID
- RegulatoryOverlayUUID
- ReportingUnitUUID


***
## Source Data & WaDE Complied Data Assessment
The following info is from a data assessment evaluation of the completed data...

Dataset | Num of Source Entries (rows) 
---------- | ----------
**Utah Water Right Areas** | 51
**Groundwater Policy Management** | 60
**BasinsClosedToNewAppropriations** | 5
**AreasOpenToLimitedAppropriation** | 7


Dataset | Num of Identified Reporting Units | Num of Identified Overlays
---------- | ---------- | ------------
**Compiled WaDE Data** | 77 | 120


Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
...nothing removed. | - | -


**Figure 1:** Distribution of Reporting Unit Name within reportingunits.csv
![](figures/ReportingUnitName.png)

**Figure 2:** Distribution of Reporting Unit Type within reportingunits.csv
![](figures/ReportingUnitTypeCV.png)

**Figure 3:** Distribution of Oversight Agency within the regulatoryoverlays.csv
![](figures/OversightAgency.png)

**Figure 4:** Distribution of Overlay Type within the regulatoryoverlays.csv
![](figures/RegulatoryOverlayTypeCV.png)

**Figure 5:** Map of Overlay Areas (i.e., Reporting Unit)
![](figures/ReportingUnitMap.png)



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Utah Department of Natural Resources](https://naturalresources.utah.gov/).

WSWC Staff
- Ryan James (Data Analysis) <rjames@wswc.utah.gov>

Utah Department of Natural Resources Staff
- Not Provided