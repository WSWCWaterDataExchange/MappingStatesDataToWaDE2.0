# DRBC Aggregated Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting aggregated water budget data made available by the [Delaware River Basin Commission (DRBC)](https://www.nj.gov/drbc/), for inclusion into the Water Data Exchange (WaDE) project.   WaDE enables states to share data with each other and the public in a more streamlined and consistent way.  WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**2060report_data-release_v2110.xlsx** | Timeseries report information for withdrawal and consumptive areas. Only historic surface water and groundwater data was extracted for WaDE use (e.g., A-1, A-6, A-9, A-11, A-14, A-17, A-22). | See *Download the Dataset (xlsx 10 MB)* option, [link](https://www.nj.gov/drbc/programs/supply/use-demand-projections2060.html) | See *Table.Index* tab within downloaded file.
**drb147.shp** | Geometry and location information saved within a shapefile. Joined to timeseries report information. | See *Download GIS files of 147 watersheds in the DRB (sub-basins) (zip 3 MB)* option, [link](https://www.nj.gov/drbc/programs/supply/use-demand-projections2060.html) | not provided


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Delaware River Basin Commission Aggregated Time Series Data: https://drive.google.com/drive/folders/1AXFKpxzbo_GLnvjGIKMTqVRoHrFc2jhL?usp=sharing

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share DRBC's aggregated water budget data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *DRBCag_Aggregated Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_DRBCag_PreProcessAggregatedData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_DRBCag_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, reportingunits.csv, aggregatedamounts.csv
- **3_DRBCag_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 2_DRBCag_CreateWaDEInputFiles.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - 2060report_data-release_v2110.xlsx
 - drb147.shp

#### Outputs:
 - Pag_drbcMain.zip, main input of timeseries data
 - P_Geometry.zip, geometry values for reporting unit areas

#### Operation and Steps:
- Read in the timeseries and shapefile input files.  For timeseries info extract out tabs for groundwater and surface water info only (e.g., A-1, A-6, A-9, A-11, A-14, A-17, A-22).  Left-join shapefile info to timeseries info via **BASIN_ID** input value.
- Convert **WD_MGD** & **CU_MGD** inputs from a million gallons per day (MGD) to a acre-feet per year (AFY) value.
- Split input timeseries info into Withdrawal & Consumptive counter parts.
- Translate **DESIGNATION** input from abbreviated from to *Groundwater* or *Surface Water* values.
- Generate WaDE specific field *WaterSourceNativeID* from WaDE *WaterSourceTypeCV* field.  Used to identify unique sources of water.
- Inspect output dataframe for additional errors / datatypes.
- Export main timeseries output dataframe as new csv file, *Pag_drbcMain.zip*.
- Export related shapefile geometry information, *P_Geometry.zip*.



***
## Code File: 2_DRBCag_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (methods.csv, variables.csv, organizations.csv, watersources.csv, reportingunits.csv, aggregatedamounts.csv).

#### Inputs:
- Pag_drbcMain.zip
- P_Geometry.zip

#### Outputs:
- methods.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- variables.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- organizations.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- watersources.csv
- reportingunits.csv
- aggregatedamounts.csv


## 1) Method Information
Purpose: generate legend of granular methods used on data collection.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign state info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
DRBCag_M1 | Surface Water & Groundwater | Legal Processes


## 2) Variables Information
Purpose: generate legend of granular variables specific to each state.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign agency info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
DRBCwr_V1 | 1 | Year | CFS


## 3) Organization Information
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign agency info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
DRBCag_O1 | Delaware River Basin Commission | Michael Thompson (Water Resource Engineer) | https://www.nj.gov/drbc/


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency data info to the *WaDE WaterSources* specific columns.  See *WAwr_Allocation Schema Mapping_WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = **DESIGNATION** input value..
    - *WaterSourceNativeID* = make custom wade ID as temp fix.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID| WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
DRBCag_WSwadeID1 | Fresh | WaDE Blank | wadeID1 | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


### 5) Code File: 5_NMag_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency specific area on aggregated water budget data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *DRBCag_Aggregated Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *Geometry* = WKT created **Geometry** input value, extracted from shapefile.
    - *ReportingUnitName* = **STREAMS** input value.
    - *ReportingUnitNativeID* = **BASIN_ID** input value.
    - *ReportingUnitTypeCV* = *Subbasin*
    - *StateCV* = *DE* for abbreviated "Delaware River Basin Commission".
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | ReportingUnitName | ReportingUnitNativeID | ReportingUnitTypeCV | State
---------- | ---------- | ------------  | ------------ | ------------ 
DRBCag_RUDB001 | Upper West Br Delaware River | ReportingUnitNativeID | Subbasin | DE

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV


### 6) Code File: 6_NMag_AggregatedAmounts_facts.py
Purpose: generate master sheet of state agency specified area aggregated water budget information to import into WaDE 2.0.

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *DRBCag_Aggregated Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *ReportingUnitUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **WD_MGD** & **CU_MGD** inputs for withdrawal and consumptive values respectively.  Convert from a million gallons per day (MGD) to a acre-feet per year (AFY) value.
    - *BeneficialUseCategory* = **CATEGORY** input value.
    - *ReportYearCV* = **YEAR** input value.
- Perform error check on output dataframe.
- Export output dataframe *aggregatedamounts.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | ReportingUnitUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | -----------
DRBCag_M1 | DRBCag_O1 | DRBCag_RU1 | DRBCag_V1 | DRBCag_WS1 | 46.4169285136986 | Public Supply | 1990

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *aggregatedamounts_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- ReportingUnitUUID
- Amount

***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Delaware River Basin Commission (DRBC)](https://www.nj.gov/drbc/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

DRBC Staff
- Michael Thompson (Water Resource Engineer) <Michael.Thompson@drbc.gov>