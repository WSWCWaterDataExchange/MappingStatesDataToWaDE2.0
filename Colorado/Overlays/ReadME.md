# Colorado Division of Water Resources (CDWR) Overlay Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting overlay area data, made available by the [Colorado Division of Water Resources (CDWR)](https://dwr.colorado.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Division Boundaries** | The Colorado Division of Water Resources Division Offices are located in the seven major river basins throughout the state.  Division Offices employ Water Commissioners to ensure that the water rights priority system is followed, enforcing the decrees and water laws of the State of Colorado.  | [link](https://cdss.colorado.gov/gis-data/gis-data-by-category) | [link](https://dwr.colorado.gov/division-offices)
**Designated Groundwater Basins** | Designated Groundwater Basins (Designated Basins) are areas in the eastern plains of Colorado with very little surface water where users rely primarily on groundwater as their source of water supply.  Designated groundwater rights are administered separately from water rights outside of the Designated Basins. | [link](https://cdss.colorado.gov/gis-data/gis-data-by-category) | [link](https://dwr.colorado.gov/services/well-permitting/designated-basins)

Unique files were created to be used as input.  Input files used are as follows...
- Division_Boundaries.zip, zipped shp file of division boundary geometry.
- Designated_Basins.zip, zipped shp file of designated groundwater basin geometry data.


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Colorado Division of Water Resources (CDWR) Overlay Data:[link](https://drive.google.com/drive/folders/1MQ6a1Kl2-9D8fxSdIAh76hLt4h86xckU?usp=drive_link)


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share the state's overlay data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *COov_Overlay Info Schema Mapping to WaDE.xlsx*. Several WaDE csv input files will be created in order to extract the overlay data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_COov_PreProcessRegulatoryData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_COov_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: date.csv, organization.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv, etc.
- **3_COov_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_COov_PreProcessRegulatoryData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- Division_Boundaries.zip
- Designated_Basins.zip

#### Outputs:
 - Pov_Main.zip
 - P_Geometry.zip

#### Operation and Steps:
- Read in input data, store in temporary DataFrames.
- Extract out key WaDE information.
- Check for data types errors and NA data.
- Export output dataframe as new csv file, *Pov_Main.csv* for tabular data and *P_Geometry.csv* for geometry data.


***
## Code File: 2_COov_CreateWaDEInputFiles.ipynb
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
|  0 | 8/4/2023 |   2023 |


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
|    | OrganizationUUID   | OrganizationName                     | OrganizationPurview   | OrganizationWebsite       | OrganizationPhoneNumber   | OrganizationContactName   | OrganizationContactEmail   | State   |
|---:|:-------------------|:-------------------------------------|:----------------------|:--------------------------|:--------------------------|:--------------------------|:---------------------------|:--------|
|  0 | COov_O1            | Colorado Division of Water Resources | Water Management      | https://dwr.colorado.gov/ | (303) 866-3581            | Doug Stenzel              | Doug.Stenzel@state.co.us   | CO      |


### 3) Reporting Unit Information
Purpose: generate a list of polygon areas associated with the state agency overlay area data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *COov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitUUID* = "COov_RU" + ReportingUnitNativeID
    - *EPSGCodeCV* = 4326.
    - *ReportingUnitName* = **BASIN** & **DB_NAME** inputs respectively.
    - *ReportingUnitNativeID* = "wab" + **DIV** & "dgb" + **DB** inputs respectively.
    - *ReportingUnitProductVersion* = ""
    - *ReportingUnitTypeCV* = "Colorado Water Administration Division" & "Colorado Designated Groundwater Basins".
    - *ReportingUnitUpdateDate* = ""
    - *StateCV* = "CO"
    - *Geometry* = **geometry** inputs.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | ReportingUnitUUID   |   EPSGCodeCV | ReportingUnitName   | ReportingUnitNativeID   | ReportingUnitProductVersion   | ReportingUnitTypeCV                    | ReportingUnitUpdateDate   | StateCV   | WaDEUUID   |
|---:|:--------------------|-------------:|:--------------------|:------------------------|:------------------------------|:---------------------------------------|:--------------------------|:----------|:-----------|
|  1 | COov_RUdgb2         |         4326 | Kiowa Bijou         | dgb2                    |                               | Colorado Designated Groundwater Basins |                           | CO        | dgb5       |

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
- Assign state agency data info to the *WaDE Water Overlays* specific columns.  See *COov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = "COov_RO" + RegulatoryOverlayNativeID
    - *OversightAgency* = "Colorado Division of Water Resources"
    - *RegulatoryDescription* = see 1_COov_PreProcessRegulatoryData.ipynb or COov_Overlay Info Schema Mapping to WaDE.xlsx for specifics.
    - *RegulatoryName* = **BASIN** & **DB_NAME** inputs respectively.
    - *RegulatoryOverlayNativeID* =  **DIV** & **DB** inputs respectively.
    - *RegulatoryStatusCV* = "Active"
    - *RegulatoryStatue* = ""
    - *RegulatoryStatuteLink* = see 1_COov_PreProcessRegulatoryData.ipynb or COov_Overlay Info Schema Mapping to WaDE.xlsx for specifics.
    - *StatutoryEffectiveDate* = "11/18/2024" for temp value for Division_Boundaries, **FORMATION_** input for Designated_Basins.
    - *RegulatoryOverlayTypeCV* = "Colorado Water Administration Division" & "Colorado Designated Groundwater Basins".
    - *WaterSourceTypeCV* = "Surface Water and Groundwater" for Division_Boundaries, "Groundwater" for Designated_Basins
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | RegulatoryOverlayUUID   | OversightAgency                      | RegulatoryDescription                                                                                                                                                                                                                                                                                                  | RegulatoryName   |   RegulatoryOverlayNativeID | RegulatoryStatusCV   | RegulatoryStatute   | RegulatoryStatuteLink                                               | StatutoryEffectiveDate   | StatutoryEndDate   | RegulatoryOverlayTypeCV                | WaterSourceTypeCV   | WaDEUUID   |
|---:|:------------------------|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|----------------------------:|:---------------------|:--------------------|:--------------------------------------------------------------------|:-------------------------|:-------------------|:---------------------------------------|:--------------------|:-----------|
|  1 | COov_RO6_1              | Colorado Division of Water Resources | Designated Groundwater Basins (Designated Basins) are areas in the eastern plains of Colorado with very little surface water where users rely primarily on groundwater as their source of water supply.  Designated groundwater rights are administered separately from water rights outside of the Designated Basins. | Camp Creek       |                           6 | Active               |                     | https://dwr.colorado.gov/services/well-permitting/designated-basins | 1968-05-13               |                    | Colorado Designated Groundwater Basins | Groundwater         | dgb4       |

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
- Assign state agency data info to the *WaDE OverlayReportingunits* specific columns.  See *COov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *DataPublicationDate* = use date of file creation
    - *OrganizationUUID* = pull from organization.csv
    - *RegulatoryOverlayUUID* = pull form regulatoryoverlay.csv
    - *ReportingUnitUUID* = pull from reportingunit.csv
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | DataPublicationDate   | OrganizationUUID   | RegulatoryOverlayUUID   | ReportingUnitUUID   |
|---:|:----------------------|:-------------------|:------------------------|:--------------------|
|  1 | 2024-11-18            | COov_O1            | COov_RO2_2              | COov_RUwab2         |

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
**Division_Boundaries.zip** | 7
**Designated_Basins.zip** | 8


Dataset | Num of Identified Reporting Units | Num of Identified Overlays
---------- | ---------- | ------------
**Compiled WaDE Data** | 15 | 15


Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
...nothing removed | - | -


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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Colorado Division of Water Resources (CDWR)](https://dwr.colorado.gov/).

WSWC Staff
- Ryan James (Data Analysis) <rjames@wswc.utah.gov>

Colorado Division of Water Resources (CDWR) Staff
- Doug Stenzel <https://dwr.colorado.gov/>
