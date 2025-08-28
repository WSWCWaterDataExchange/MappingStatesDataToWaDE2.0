# Nebraska Natural Resources Districts Overlay Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting overlay area data, made available by the [Nebraska Natural Resources Districts](https://www.nrdnet.org/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Natural Resource District (NRD) Boundaries** | description of data | [link](https://www.nebraskamap.gov/datasets/4ba353be6a794e379f90391e54ab6a42_0/explore?location=41.350562%2C-99.634750%2C6.47) | [link](https://www.nebraskamap.gov/datasets/nebraska::natural-resource-district-nrd-boundaries-1/about)

Unique files were created to be used as input.  Input files used are as follows...
- Natural_Resource_District_NRD_Boundaries_20250129.shp

## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Nebraska Natural Resources Districts Overlay Data: [link](https://drive.google.com/drive/folders/1PxFVgsiCNj4nrwOj_DhRQUojDJfQa2hq?usp=drive_link)


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share the state's overlay data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NEov_Overlay Info Schema Mapping to WaDE.xlsx*. Several WaDE csv input files will be created in order to extract the overlay data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_NEov_PreProcessOverlayData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_NEov_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: date.csv, organization.csv, reportingunits.csv, overlays.csv, overlayreportingunits.csv, etc.
- **3_NEov_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_XXov_PreProcessOverlayData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- Natural_Resource_District_NRD_Boundaries_20250129.shp

#### Outputs:
 - Pov_Main.zip
 - P_Geometry.zip

#### Operation and Steps:
- read in shp file input, place into temporary dataFrame.
- Use provided dictionary to attach additional status web link information based on **OBJECTID** UD input of shp file (see file for specifics).
- Translate state specific inputs for WaDE specific entries.
- Review dataFrame for errors.
- Extract geometry information from shp file.
- Export output dataframe as new csv file, *Pov_Main.csv* for tabular data and *P_Geometry.csv* for geometry data.


***
## Code File: 2_NEov_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (date.csv, organizations.csv, reportingunits.csv, overlays.csv, overlayreportingunits.csv.

#### Inputs:
- Pov_Main.zip
- P_Geometry.zip

#### Outputs:
- date.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- organizations.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- reportingunits.csv
- overlays.csv 
- overlayreportingunits.csv



## 1) Date Information
Purpose: generate legend of granular date used on data collection.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Date* specific columns.
- Assign agency info to the *WaDE Date* specific columns (this was hardcoded by hand for simplicity).
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | Date     |   Year |
|---:|:---------|-------:|
|  0 | 1/9/2025 |   2025 |


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
|    | OrganizationUUID   | OrganizationContactEmail   | OrganizationContactName   | OrganizationName                            | OrganizationPhoneNumber   | OrganizationPurview                                                                                                                                                                                                                                    | OrganizationWebsite     | State   |
|---:|:-------------------|:---------------------------|:--------------------------|:--------------------------------------------|:--------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------|:--------|
|  0 | NEov_O1            | nard@nrdnet.org            | Office                    | Nebraska Association of Resources Districts | 402-471-7670              | The Nebraska Association of Resources Districts (NARD) is the trade association for Nebraska's 23 Natural Resources Districts. NARD has five full-time employees, and is governed by a 23-member board made up of directors from individual districts. | https://www.nrdnet.org/ | NE      |


### 3) Reporting Unit Information
Purpose: generate a list of polygon areas associated with the state agency overlay area data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *NEov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitUUID* = "NEov_RE" + **NRD_Num** input.
    - *EPSGCodeCV* = 4326.
    - *ReportingUnitName* = **NRD_Name_A** input.
    - *ReportingUnitNativeID* = **NRD_Num** input.
    - *ReportingUnitProductVersion* = ""
    - *ReportingUnitTypeCV* = "Natural Resources Districts"
    - *ReportingUnitUpdateDate* = ""
    - *StateCV* = "NE"
    - *Geometry* = extract from shp file, pair via **NRD_Num** input.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | ReportingUnitUUID   |   EPSGCodeCV | ReportingUnitName    | ReportingUnitNativeID   | ReportingUnitProductVersion   | ReportingUnitTypeCV         | ReportingUnitUpdateDate   | StateCV   |
|---:|:--------------------|-------------:|:---------------------|:------------------------|:------------------------------|:----------------------------|:--------------------------|:----------|
|  1 | NEov_RUne10         |         4326 | PAPIO-MISSOURI RIVER | ne10                    |                               | Natural Resources Districts |                           | NE        |

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
- Assign state agency data info to the *WaDE Water Overlays* specific columns.  See *NEov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *OverlayUUID* = "NEov_RO" + **NRD_Num** input.
    - *OversightAgency* = **NRD_Name_A** input.
    - *OverlayDescription* = "Natural Resources Districts were created to solve flood control, soil erosion, irrigation run-off, and groundwater quantity and quality issues. Nebraska's NRDs are involved in a wide variety of projects and programs to conserve and protect the state's natural resources. NRDs are charged under state law with 12 areas of responsibility including flood control, soil erosion, groundwater management and many others."
    - *OverlayName* = **NRD_Name_A** input.
    - *OverlayNativeID* = **NRD_Num**.
    - *OverlayStatusCV* = "Active"
    - *Statue* = ""
    - *StatuteLink* = see 1_NEov_PreProcessOverlayData.ipynb for specifics on creation.
    - *StatutoryEffectiveDate* = "01/01/1972"
    - *OverlayTypeCV* = "Natural Resources Districts"
    - *WaterSourceTypeCV* = "Groundwater"
- Perform error check on output dataframe.
- Export output dataframe *overlays.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | OverlayUUID   | OversightAgency   | OverlayDescription                                                                                                                                                                                                                                                                                                                                                                                                          | OverlayName   |   OverlayNativeID | OverlayStatusCV   | Statute   | StatuteLink       | StatutoryEffectiveDate   | StatutoryEndDate   | OverlayTypeCV     | WaterSourceTypeCV   |
|---:|:------------------------|:------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|----------------------------:|:---------------------|:--------------------|:----------------------------|:-------------------------|:-------------------|:----------------------------|:--------------------|
|  1 | NEov_RO8                | LEWIS & CLARKNRD  | Natural Resources Districts were created to solve flood control, soil erosion, irrigation run-off, and groundwater quantity and quality issues. Nebraska's NRDs are involved in a wide variety of projects and programs to conserve and protect the state's natural resources. NRDs are charged under state law with 12 areas of responsibility including flood control, soil erosion, groundwater management and many others. | LEWIS & CLARK    |                           8 | Active               |                     | https://lcnrd.nebraska.gov/ | 1972-01-01               |                    | Natural Resources Districts | Groundwater         |


Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *overlays_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water overlays include the following...
- OverlayUUID 
- OversightAgency
- OverlayDescription
- OverlayName
- OverlayStatusCV
- StatutoryEffectiveDate


### 5) Overlay Reporting Units Information
Purpose: generate master sheet of overlay area information and how it algins with reporting unit area information.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE OverlayReportingunits* specific columns.
- Assign state agency data info to the *WaDE OverlayReportingunits* specific columns.  See *NEov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *DataPublicationDate* = use date of file creation
    - *OrganizationUUID* = pull from organization.csv
    - *OverlayUUID* = pull form overlay.csv
    - *ReportingUnitUUID* = pull from reportingunit.csv
- Perform error check on output dataframe.
- Export output dataframe *overlayreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | DataPublicationDate   | OrganizationUUID   | OverlayUUID   | ReportingUnitUUID   |
|---:|:----------------------|:-------------------|:------------------------|:--------------------|
|  1 | 2025-01-29            | NEov_O1            | NEov_RO24               | NEov_RUne24         |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *overlayreportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- DataPublicationDate
- OrganizationUUID
- OverlayUUID 
- ReportingUnitUUID


***
## Source Data & WaDE Complied Data Assessment
The following info is from a data assessment evaluation of the completed data...

Dataset | Num of Source Entries (rows) 
---------- | ----------
**Natural Resource District (NRD) Boundaries** | 23


Dataset | Num of Identified Reporting Units | Num of Identified Overlays
---------- | ---------- | ------------
**Compiled WaDE Data** | 23 | 23


Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
...nothing removed | - | -


**Figure 1:** Distribution of Reporting Unit Name within reportingunits.csv
![](figures/ReportingUnitName.png)

**Figure 2:** Distribution of Reporting Unit Type within reportingunits.csv
![](figures/ReportingUnitTypeCV.png)

**Figure 3:** Distribution of Oversight Agency within the overlays.csv
![](figures/OversightAgency.png)

**Figure 4:** Distribution of Overlay Type within the overlays.csv
![](figures/OverlayTypeCV.png)

**Figure 5:** Map of Overlay Areas (i.e., Reporting Unit)
![](figures/ReportingUnitMap.png)



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nebraska Natural Resources Districts](https://www.nrdnet.org/).

WSWC Staff
- Ryan James (Data Analysis) <rjames@wswc.utah.gov>

Nebraska Natural Resources Districts Staff
- not provided