# Texas Commission on Environmental Quality Overlay Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting overlay area data, made available by the [Texas Commission on Environmental Quality](https://gis-tceq.opendata.arcgis.com/datasets/TCEQ::groundwater-conservation-districts/explore), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Groundwater Conservation Districts** | description of data | [link](https://gis-tceq.opendata.arcgis.com/datasets/TCEQ::groundwater-conservation-districts/explore) | Not Provided

Unique files were created to be used as input.  Input files used are as follows...
- Groundwater_Conservation_Districts.csv.shp, "Shapefile"


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Texas Commission on Environmental Quality Overlay Data:[link]()


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share the state's overlay data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *TXov_Overlay Info Schema Mapping to WaDE.xlsx*. Several WaDE csv input files will be created in order to extract the overlay data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_TXov_PreProcessRegulatoryData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_TXov_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: date.csv, organization.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv, etc.
- **3_TXov_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_TXov_PreProcessRegulatoryData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- "{name of data file}.data file type"

#### Outputs:
 - Pov_Main.zip
 - P_Geometry.zip

#### Operation and Steps:
- Export output dataframe as new csv file, *Pwr_xxMain.csv* for tabular data and *P_Geometry.csv* for geometry data.


***
## Code File: 2_TXov_CreateWaDEInputFiles.ipynb
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
|    | Date      |   Year |
|---:|:----------|-------:|
|  0 | 2/20/2025 |   2025 |


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
|    | OrganizationUUID   | OrganizationContactEmail       | OrganizationContactName   | OrganizationName                          | OrganizationPhoneNumber   | OrganizationPurview              | OrganizationWebsite         | State   |
|---:|:-------------------|:-------------------------------|:--------------------------|:------------------------------------------|:--------------------------|:---------------------------------|:----------------------------|:--------|
|  0 | TXov_O1            | kathy.alexander@tceq.texas.gov | Kathy Alexander           | Texas Commission on Environmental Quality | 512-239-1000              | Water conservation, and planning | https://www.tceq.texas.gov/ | TX      |


### 3) Reporting Unit Information
Purpose: generate a list of polygon areas associated with the state agency overlay area data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *TXov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitUUID* = "TXov_RU + OBJECTID"
    - *EPSGCodeCV* = 4326.
    - *ReportingUnitName* = **SHORTNAM** input.
    - *ReportingUnitNativeID* = **OBJECTID** input.
    - *ReportingUnitProductVersion* = ""
    - *ReportingUnitTypeCV* = "Groundwater Conservation Districts"
    - *ReportingUnitUpdateDate* = "5/2/2022"
    - *StateCV* = "TX"
    - *Geometry* = **geometry** input.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | ReportingUnitUUID   |   EPSGCodeCV | ReportingUnitName   | ReportingUnitNativeID   | ReportingUnitProductVersion   | ReportingUnitTypeCV                | ReportingUnitUpdateDate   | StateCV   |
|---:|:--------------------|-------------:|:--------------------|:------------------------|:------------------------------|:-----------------------------------|:--------------------------|:----------|
|  1 | TXov_RUtx13762      |         4326 | Crockett County GCD | tx13762                 |                               | Groundwater Conservation Districts | 2/5/2022                  | TX        |
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
- Assign state agency data info to the *WaDE Water Overlays* specific columns.  See *TXov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = "TXov_RO" + counter or native id value.
    - *OversightAgency* = "Texas Commission on Environmental Quality"
    - *RegulatoryDescription* = "A district created under Texas Constitution, Article III, Section 52 or Article XVI, Section 59 that has the authority to regulate the spacing of water wells, the production from water wells, or both."
    - *RegulatoryName* = **SHORTNAM** input.
    - *RegulatoryOverlayNativeID* = **OBJECTID** input.
    - *RegulatoryStatusCV* = "Active"
    - *RegulatoryStatue* = **ENABLACT** input.
    - *RegulatoryStatuteLink* = **ORIGIN_DES** input.
    - *StatutoryEffectiveDate* = **EST_DATE** input.
    - *RegulatoryOverlayTypeCV* = "Groundwater Conservation District"
    - *WaterSourceTypeCV* = "Groundwater"
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | RegulatoryOverlayUUID   | OversightAgency                           | RegulatoryDescription                                                                                                                                                                                    | RegulatoryName   |   RegulatoryOverlayNativeID | RegulatoryStatusCV   | RegulatoryStatute   | RegulatoryStatuteLink                                                   | StatutoryEffectiveDate   | StatutoryEndDate   | RegulatoryOverlayTypeCV            | WaterSourceTypeCV   |
|---:|:------------------------|:------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|----------------------------:|:---------------------|:--------------------|:------------------------------------------------------------------------|:-------------------------|:-------------------|:-----------------------------------|:--------------------|
|  1 | TXov_RO13767            | Texas Commission on Environmental Quality | A district created under Texas Constitution, Article III, Section 52 or Article XVI, Section 59 that has the authority to regulate the spacing of water wells, the production from water wells, or both. | Bee GCD          |                       13767 | Active               | SB 16               | http://www.legis.state.tx.us/BillLookup/Text.aspx?LegSess=75R&Bill=SB16 | 2001-01-20               |                    | Groundwater Conservation Districts | Groundwater         |

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
- Assign state agency data info to the *WaDE OverlayReportingunits* specific columns.  See *TXov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *DataPublicationDate* = use date of file creation
    - *OrganizationUUID* = pull from organization.csv
    - *RegulatoryOverlayUUID* = pull form regulatoryoverlay.csv
    - *ReportingUnitUUID* = pull from reportingunit.csv
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | DataPublicationDate   | OrganizationUUID   | RegulatoryOverlayUUID   | ReportingUnitUUID   |
|---:|:----------------------|:-------------------|:------------------------|:--------------------|
|  1 | 2025-02-20            | TXov_O1            | TXov_RO13762            | TXov_RUtx13762      |

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
**"{name of data}"** | "fill value here"


Dataset | Num of Identified Reporting Units | Num of Identified Overlays
---------- | ---------- | ------------
**Compiled WaDE Data** | "fill value here" | "fill value here"


Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
Incomplete or bad entry for Latitude | 1 | Removed from WaDE


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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Texas Commission on Environmental Quality](https://gis-tceq.opendata.arcgis.com/datasets/TCEQ::groundwater-conservation-districts/explore).

WSWC Staff
- Ryan James (Data Analysis) <rjames@wswc.utah.gov>

Texas Commission on Environmental Quality Staff
- "{name of staff member that is our point of contact for this data}" <"{point of contacts email"}>
