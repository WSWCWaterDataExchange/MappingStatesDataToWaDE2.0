# Kansas Department of Agriculture,Division of Water Resources (KDADWR) Overlay Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting overlay area data, made available by the [Kansas Department of Agriculture,Division of Water Resources (KDADWR)](https://www.agriculture.ks.gov/home), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Groundwater Management Distrcits (GMD)** | Established under the authority of the Kansas Groundwater Management District Act, there are five GMD's in Kansas. Kansas Groundwater Management District Act (K.S.A. 82a-1020 through 82a-1040) This set includes the GMD No. 2 boundary expansion effective July 7, 2017. | [link](https://hub.kansasgis.org/datasets/15a4f274956c4a129457bd33dac8ca3b_0/explore?location=38.207107%2C-98.150095%2C7.95) | [link](https://hub.kansasgis.org/datasets/KSDOT::groundwater-management-districts-gmd/about)

Unique files were created to be used as input.  Input files used are as follows...
- Groundwater_Management_Districts_GMD.zip, shp file of district geometry


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Kansas Department of Agriculture,Division of Water Resources (KDADWR) Overlay Data: [link](https://drive.google.com/drive/folders/10PU1oOmUItBdEAVNsc36hNvbbq8lZNB2?usp=drive_link)


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share the state's overlay data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *KSov_Overlay Info Schema Mapping to WaDE.xlsx*. Several WaDE csv input files will be created in order to extract the overlay data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_KSov_PreProcessRegulatoryData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_KSov_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: date.csv, organization.csv, reportingunits.csv, regulatoryoverlays.csv, regulatoryreportingunits.csv, etc.
- **3_KSov_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_KSov_PreProcessRegulatoryData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- Groundwater_Management_Districts_GMD.zip

#### Outputs:
 - Pov_Main.zip
 - P_Geometry.zip

#### Operation and Steps:
- Read in shp file as temporary dataframe.
- Extract key WaDE elements.
- Check data types and for errors.
- Export output dataframe as new csv file, *Pov_Main.csv* for tabular data and *P_Geometry.csv* for geometry data.


***
## Code File: 2_KSov_CreateWaDEInputFiles.ipynb
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
|  0 | 11/7/2024 |   2024 |


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
|    | OrganizationUUID   | OrganizationContactEmail   | OrganizationContactName   | OrganizationName                                                  | OrganizationPhoneNumber   | OrganizationPurview                                                                                                                        | OrganizationWebsite             | State   |
|---:|:-------------------|:---------------------------|:--------------------------|:------------------------------------------------------------------|:--------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------|:--------|
|  0 | KSov_O1            | Ginger.Pugh@ks.gov         | Ginger Pugh               | The Kansas Department of Agriculture, Division of Water Resources | 785-564-6677              | The Division of Water Resources within the Kansas Department of Agriculture governs the use and allocation of the state's water resources. | https://agriculture.ks.gov/home | KS      |


### 3) Reporting Unit Information
Purpose: generate a list of polygon areas associated with the state agency overlay area data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *KSov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitUUID* = "KSov_RU" + ReportingUnitNativeID
    - *EPSGCodeCV* = 4326.
    - *ReportingUnitName* = **Name** input.
    - *ReportingUnitNativeID* = **GMD_ID** input.
    - *ReportingUnitProductVersion* = ""
    - *ReportingUnitTypeCV* = "Groundwater Management Districts"
    - *ReportingUnitUpdateDate* = ""
    - *StateCV* = "KS"
    - *Geometry* = **geometry** input.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | ReportingUnitUUID   |   EPSGCodeCV | ReportingUnitName   | ReportingUnitNativeID   | ReportingUnitProductVersion   | ReportingUnitTypeCV              | ReportingUnitUpdateDate   | StateCV   |
|---:|:--------------------|-------------:|:--------------------|:------------------------|:------------------------------|:---------------------------------|:--------------------------|:----------|
|  1 | KSov_RUksGMD2       |         4326 | Equus Beds GMD #2   | ksGMD2                  |                               | Groundwater Management Districts |                           | KS        |

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
- Assign state agency data info to the *WaDE Water Overlays* specific columns.  See *KSov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *RegulatoryOverlayUUID* = "KSov_RO" + RegulatoryOverlayNativeID
    - *OversightAgency* = **Name** input.
    - *RegulatoryDescription* = "In Kansas, local units of government, called groundwater management districts, provide water-use administration, planning, and information. Five groundwater management districts were created in the 1970s in the western and central parts of the state. The primary use of ground water in these areas is irrigation, although several districts also face issues of municipal supply. The districts are governed by local boards and have been instrumental in providing information and identifying research and regulatory needs within their boundaries."
    - *RegulatoryName* = **Name** input.
    - *RegulatoryOverlayNativeID* = **GMD_ID** input.
    - *RegulatoryStatusCV* = "Final"
    - *RegulatoryStatue* = ""
    - *RegulatoryStatuteLink* = "'https://www.kgs.ku.edu/Hydro/gmd.html"
    - *StatutoryEffectiveDate* = "09/25/2015"
    - *RegulatoryOverlayTypeCV* = "Groundwater Management Districts"
    - *WaterSourceTypeCV* = "Groundwater"
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID| OversightAgency | RegulatoryDescription | RegulatoryName | RegulatoryOverlayNativeID | RegulatoryStatusCV | RegulatoryStatute | RegulatoryStatuteLink | StatutoryEffectiveDate | StatutoryEndDate | RegulatoryOverlayTypeCV | WaterSourceTypeCV
|    | RegulatoryOverlayUUID   | OversightAgency   | RegulatoryDescription                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | RegulatoryName    | RegulatoryOverlayNativeID   | RegulatoryStatusCV   | RegulatoryStatute   | RegulatoryStatuteLink                 | StatutoryEffectiveDate   | StatutoryEndDate   | RegulatoryOverlayTypeCV          | WaterSourceTypeCV   |
|---:|:------------------------|:------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------|:----------------------------|:---------------------|:--------------------|:--------------------------------------|:-------------------------|:-------------------|:---------------------------------|:--------------------|
|  1 | KSov_ROksGMD2           | Equus Beds GMD #2 | In Kansas, local units of government, called groundwater management districts, provide water-use administration, planning, and information. Five groundwater management districts were created in the 1970s in the western and central parts of the state. The primary use of ground water in these areas is irrigation, although several districts also face issues of municipal supply. The districts are governed by local boards and have been instrumental in providing information and identifying research and regulatory needs within their boundaries. | Equus Beds GMD #2 | ksGMD2                      | Final                |                     | https://www.kgs.ku.edu/Hydro/gmd.html | 2015-09-25               |                    | Groundwater Management Districts | Groundwater         |

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
- Assign state agency data info to the *WaDE OverlayReportingunits* specific columns.  See *KSov_Overlay Info Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *DataPublicationDate* = use date of file creation
    - *OrganizationUUID* = pull from organization.csv
    - *RegulatoryOverlayUUID* = pull form regulatoryoverlay.csv
    - *ReportingUnitUUID* = pull from reportingunit.csv
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | DataPublicationDate   | OrganizationUUID   | RegulatoryOverlayUUID   | ReportingUnitUUID   |
|---:|:----------------------|:-------------------|:------------------------|:--------------------|
|  1 | 2024-11-07            | KSov_O1            | KSov_ROksGMD1           | KSov_RUksGMD1       |

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
**Groundwater Management Distrcits (GMD)** | 5


Dataset | Num of Identified Reporting Units | Num of Identified Overlays
---------- | ---------- | ------------
***Compiled WaDE Data** | 5 | 5


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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Kansas Department of Agriculture,Division of Water Resources (KDADWR)](https://www.agriculture.ks.gov/home).

WSWC Staff
- Ryan James (Data Analysis) <rjames@wswc.utah.gov>

Kansas Department of Agriculture,Division of Water Resources (KDADWR) Staff
- Ginger Pugh <Ginger.Pugh@ks.gov>