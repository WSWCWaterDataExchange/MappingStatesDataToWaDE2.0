# Nevada Division of Water Resources (NVDWR) Overlay Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting overlay area data, made available by the [Nevada Division of Water Resources (NVDWR)](http://water.nv.gov/index.aspx), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Basins_State_Engineer_Admin_Boundaries"** | Shapefile of NV tate Engineer Administrative Basin Boundaries. | [Link]("https://data-ndwr.hub.arcgis.com/datasets/NDWR::basins-state-engineer-admin-boundaries/about) | Not Provided
**CHAPTER 534 - UNDERGROUND WATER AND WELLS** | HTML of underground water and well laws for NV. | Not Provided | [Link](https://www.leg.state.nv.us/NRS/NRS-534.html#NRS534Sec037) |

Unique files were created to be used as input.  Input files used are as follows...
- Basins_State_Engineer_Admin_Boundaries.zip, zipped shapefile


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Nevada Division of Water Resources (NVDWR) Overlay Data: [Link](https://drive.google.com/drive/folders/1QK72hc8Xu9vo6TYBRMAzuVugPEo7lVEN?usp=drive_link)


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share the state's overlay data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NVov_Overlay Schema Mapping to WaDE.xlsx*. Several WaDE csv input files will be created in order to extract the overlay data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_NVov_PreProcessRegulatoryData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_NVov_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: date.csv, organization.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv, etc.
- **3_NVov_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_NVov_PreProcessRegulatoryData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- Basins_State_Engineer_Admin_Boundaries.zip

#### Outputs:
 - Pov_Main.zip
 - P_Geometry.zip

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
- Export output dataframe as new csv file (P_nvRegMaster.csv & P_Geometry.csv respectively).
- Export output dataframe as new csv file, *Pov_Main.csv* for tabular data and *P_Geometry.csv* for geometry data.


***
## Code File: 2_NVov_CreateWaDEInputFiles.ipynb
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
|    | Date     |   Year |
|---:|:---------|-------:|
|  0 | 8/7/2023 |   2023 |


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
|    | OrganizationUUID   | OrganizationContactEmail   | OrganizationContactName   | OrganizationName                   | OrganizationPhoneNumber   | OrganizationPurview                 | OrganizationWebsite            | State   |
|---:|:-------------------|:---------------------------|:--------------------------|:-----------------------------------|:--------------------------|:------------------------------------|:-------------------------------|:--------|
|  0 | NVov_O1            | bmcmenamy@water.nv.gov     | Brian McMenamy            | Nevada Division of Water Resources | 775-684-2800              | Manager of Nevada's water resources | http://water.nv.gov/index.aspx | NV      |


### 3) Reporting Unit Information
Purpose: generate a list of polygon areas associated with the state agency overlay area data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *NVov_Overlay Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitUUID* = "NVov_RU" + counter
    - *EPSGCodeCV* = 4326.
    - *ReportingUnitName* = **BasinName** input.
    - *ReportingUnitNativeID* = **BasinID** input.
    - *ReportingUnitProductVersion* = ""
    - *ReportingUnitTypeCV* = "Groundwater Basin Designations"
    - *ReportingUnitUpdateDate* = ""
    - *StateCV* = "NV"
    - *Geometry* = from geometry
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | ReportingUnitUUID   |   EPSGCodeCV | ReportingUnitName       | ReportingUnitNativeID   | ReportingUnitProductVersion   | ReportingUnitTypeCV            | ReportingUnitUpdateDate   | StateCV   |
|---:|:--------------------|-------------:|:------------------------|:------------------------|:------------------------------|:-------------------------------|:--------------------------|:----------|
|  1 | NVov_RUnv002        |         4326 | Continental Lake Valley | nv002                   |                               | Groundwater Basin Designations |                           | NV        |

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
- Assign state agency data info to the *WaDE Water Overlays* specific columns.  See *NVov_Overlay Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = "NVov_RO" + counter
    - *OversightAgency* = "Office of the Nevada State Engineer"
    - *RegulatoryDescription* = Use **Designatio** input to help designated provided text.
    - *RegulatoryName* = **BasinName** input.
    - *RegulatoryOverlayNativeID* = **BasinID** input.
    - *RegulatoryStatusCV* = **Designatio** input.
    - *RegulatoryStatue* = ""
    - *RegulatoryStatuteLink* = "https://www.leg.state.nv.us/NRS/NRS-534.html#NRS534Sec037"
    - *StatutoryEffectiveDate* = "07/01/1981"
    - *RegulatoryOverlayTypeCV* = "Groundwater Basin Designations"
    - *WaterSourceTypeCV* = "Groundwater"
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | RegulatoryOverlayUUID   | OversightAgency                     | RegulatoryDescription                                                | RegulatoryName       | RegulatoryOverlayNativeID   | RegulatoryStatusCV   | RegulatoryStatute   | RegulatoryStatuteLink                                     | StatutoryEffectiveDate   | StatutoryEndDate   | RegulatoryOverlayTypeCV        | WaterSourceTypeCV   |
|---:|:------------------------|:------------------------------------|:---------------------------------------------------------------------|:---------------------|:----------------------------|:---------------------|:--------------------|:----------------------------------------------------------|:-------------------------|:-------------------|:-------------------------------|:--------------------|
|  1 | NVov_ROnv142            | Office of the Nevada State Engineer | State Engineer's order(s) do not define any administrative controls. | Alkali Spring Valley | nv142                       | DESIGNATED           |                     | https://www.leg.state.nv.us/NRS/NRS-534.html#NRS534Sec037 | 1981-07-01               |                    | Groundwater Basin Designations | Groundwater         |

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
- Assign state agency data info to the *WaDE OverlayReportingunits* specific columns.  See *NVov_Overlay Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *DataPublicationDate* = use date of file creation
    - *OrganizationUUID* = pull from organization.csv
    - *RegulatoryOverlayUUID* = pull form regulatoryoverlay.csv
    - *ReportingUnitUUID* = pull from reportingunit.csv
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | DataPublicationDate   | OrganizationUUID   | RegulatoryOverlayUUID   | ReportingUnitUUID   |
|---:|:----------------------|:-------------------|:------------------------|:--------------------|
|  1 | 2025-02-03            | NVov_O1            | NVov_ROnv204            | NVov_RUnv204        |

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
**Basins_State_Engineer_Admin_Boundaries"** | 256


Dataset | Num of Identified Reporting Units | Num of Identified Overlays
---------- | ---------- | ------------
**Compiled WaDE Data** | 256 | 256


Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
... nothing removed | - | -


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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nevada Division of Water Resources (NVDWR)](http://water.nv.gov/index.aspx).

WSWC Staff
- Ryan James (Data Analysis) <rjames@wswc.utah.gov>

Nevada Division of Water Resources (NVDWR) Staff
- Brian McMenamy <bmcmenamy@water.nv.gov>
- Levi Kryder (Chief, Hydrology Section) <lkryder@water.nv.gov>
