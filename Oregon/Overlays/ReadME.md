# Oregon Water Resources Department Overlay Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting overlay area data, made available by the [Oregon Water Resources Department ](https://www.oregon.gov/owrd/pages/index.aspx), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Administrative Basins (AB)** | Administrative basins for water rights. | [link](https://www.oregon.gov/OWRD/access_Data/Pages/Data.aspx) | [link](https://www.oregon.gov/owrd/programs/administrativebasins/Pages/default.aspx#b1)
**Groundwater Restricted Areas (GRA)** | Areas specific for existing water rights by preventing excessive groundwater declines, restoring aquifer stability, and preserving aquifers with limited storage capacity for designated high public value uses.  | [link]( https://geohub.oregon.gov/datasets/oregon-geo::groundwater-restricted-areas/about) | [link](https://www.arcgis.com/sharing/rest/content/items/94c6ec9b19de4ce6b7e05596d368971b/info/metadata/metadata.xml?format=default&output=html)

Unique files were created to be used as input.  Input files used are as follows...
- oregon-water-resources-department-owrd-administrative-basins.zip, a zipped shp file of basin geometry
- GW_Restricted_Areas.zip, zipped shp file of groundwater restricted area geometry.


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Oregon Water Resources Department  Overlay Data: [link](https://drive.google.com/drive/folders/1NvrOsTUNrl2xtVhh3uvTnQCCDarGQYVM?usp=drive_link)


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share the state's overlay data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *ORov_Overlay Info Schema Mapping to WaDE.xlsx*. Several WaDE csv input files will be created in order to extract the overlay data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_ORov_PreProcessRegulatoryData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_ORov_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: date.csv, organization.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv, etc.
- **3_ORov_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_ORov_PreProcessRegulatoryData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- oregon-water-resources-department-owrd-administrative-basins.zip, a zipped shp file of basin geometry

#### Outputs:
 - Pov_Main.zip
 - P_Geometry.zip

#### Operation and Steps:
- Read in shp file as temporary dataframe.
- Extract key WaDE elements.
- Check data types and for errors.
- Export output dataframe as new csv file, *Pov_Main.csv* for tabular data and *P_Geometry.csv* for geometry data.


***
## Code File: 2_ORov_CreateWaDEInputFiles.ipynb
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
|  0 | 10/29/2024 |   2024 |


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
|    | OrganizationUUID   | OrganizationContactEmail   | OrganizationContactName   | OrganizationName                  | OrganizationPhoneNumber   | OrganizationPurview                                                                                                                                                | OrganizationWebsite                                     | State   |
|---:|:-------------------|:---------------------------|:--------------------------|:----------------------------------|:--------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------|:--------|
|  0 | ORov_O1            | wrd_dl_Director@oregon.gov | Tom Byler                 | Oregon Water Resources Department | 503-986-0900              | Water right surface Points of Diversion (POD) and groundwater Points of Appropriation (POA) locations in the state of Oregon are collectively referred to as PODs. | https://www.oregon.gov/OWRD/access_Data/Pages/Data.aspx | OR      |


### 3) Reporting Unit Information
Purpose: generate a list of polygon areas associated with the state agency overlay area data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *ORov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitUUID* = "ORov_RU" + ReportingUnitNativeID
    - *EPSGCodeCV* = "4326".
    - *ReportingUnitName* = **BASIN_NAME** for AB, **gwra_area_** for GRA inputs.
    - *ReportingUnitNativeID* = **BASIN_NUM** input.
    - *ReportingUnitProductVersion* = "9.6" for AB.
    - *ReportingUnitTypeCV* = "Administrative Basins" for AB, "Groundwater Restricted Areas" for GRA.
    - *ReportingUnitUpdateDate* = "9/22/2021" or AB, "07/23/2023" for GRA.
    - *StateCV* = "OR"
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | ReportingUnitUUID   |   EPSGCodeCV | ReportingUnitName   | ReportingUnitNativeID   |   ReportingUnitProductVersion | ReportingUnitTypeCV   | ReportingUnitUpdateDate   | StateCV   |
|---:|:--------------------|-------------:|:--------------------|:------------------------|------------------------------:|:----------------------|:--------------------------|:----------|
|  1 | ORov_RUor10         |         4326 | Malheur             | or10                    |                           9.6 | Administrative Basins | 9/22/2021                 | OR        |

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
- Assign state agency data info to the *WaDE Water Overlays* specific columns.  See *ORov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = "ORov_RO" + RegulatoryOverlayNativeID
    - *OversightAgency* = "Oregon Water Resources Department"
    - *RegulatoryDescription* = See 1_ORov_PreProcessRegulatoryData for specifics.
    - *RegulatoryName* = **BASIN_NAME** input for AB, **gwra_area_** for GRA.
    - *RegulatoryOverlayNativeID* = **BASIN_NUM** input.
    - *RegulatoryStatusCV* = "Active" for AB, **gwra_statu** input for GRA.
    - *RegulatoryStatue* = ""
    - *RegulatoryStatuteLink* = "https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision=3207" or AB, **source_lin** input for GRA.
    - *StatutoryEffectiveDate* = "10/7/1993" for AB, **effective_** input for GRA.
    - *RegulatoryOverlayTypeCV* = "Administrative Basins" for AB, "Groundwater Restricted Areas" for GRA.
    - *WaterSourceTypeCV* = "Surface and Groundwater" for AB, "Groundwater" for GRA.
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | RegulatoryOverlayUUID   | OversightAgency                   | RegulatoryDescription                                                                                                                                    | RegulatoryName       | RegulatoryOverlayNativeID   | RegulatoryStatusCV   | RegulatoryStatute   | RegulatoryStatuteLink                                                                 | StatutoryEffectiveDate   | StatutoryEndDate   | RegulatoryOverlayTypeCV   | WaterSourceTypeCV       |
|---:|:------------------------|:----------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------|:----------------------------|:---------------------|:--------------------|:--------------------------------------------------------------------------------------|:-------------------------|:-------------------|:--------------------------|:------------------------|
|  1 | ORov_ROor13             | Oregon Water Resources Department | Administrative rules which establish water management policies and objectives and which govern the appropriation and use of the surface and ground water | Goose & Summer Lakes | or13                        | Active               |                     | https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision=3207 | 1993-10-07               |                    | Administrative Basins     | Surface and Groundwater |

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
- Assign state agency data info to the *WaDE OverlayReportingunits* specific columns.  See *ORov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *DataPublicationDate* = use date of file creation
    - *OrganizationUUID* = pull from organization.csv
    - *RegulatoryOverlayUUID* = pull form regulatoryoverlay.csv
    - *ReportingUnitUUID* = pull from reportingunit.csv
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | DataPublicationDate   | OrganizationUUID   | RegulatoryOverlayUUID   | ReportingUnitUUID   |
|---:|:----------------------|:-------------------|:------------------------|:--------------------|
|  1 | 2024-10-26            | ORov_O1            | ORov_ROor8              | ORov_RUor8          |

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
**Administrative Basins (AB)** | 19
**Groundwater Restricted Areas (GRA)** | 29



Dataset | Num of Identified Reporting Unit Areas | Num of Identified Overlays
---------- | ---------- | ------------
**Compiled WaDE Data** | 47 | 47


Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
Nothing removed| - | -


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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Oregon Water Resources Department ](https://www.oregon.gov/owrd/pages/index.aspx).

WSWC Staff
- Ryan James (Data Analysis) <rjames@wswc.utah.gov>

Oregon Water Resources Department  Staff
- Tom Byler <wrd_dl_Director@oregon.gov>
