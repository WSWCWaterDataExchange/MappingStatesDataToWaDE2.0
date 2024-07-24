# UDWRE Aggregated Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting aggregated water budget data made available by the [Utah Division of Water Resources (UDWRE)](https://water.utah.gov/), for inclusion into the Water Data Exchange (WaDE) project.   WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Source Data Utilized
 All data retrieved from the provided arcgis service provided by UT (https://services.arcgis.com/ZzrwjTRez6FJiOq4/arcgis/rest/services/Water_Budget_WaDE_Compatible_Table/FeatureServer)
 - [Water_Budget_WaDE_Compatible_Table.xlsx] timeseries water use for Utah.
 - UT_Subarea.shp shapefile geometry data used for custom location information for the timeseries water use data.
 - UT_HUC8.shp shapefile geometry data used for HUC8 location information for the timeseries water use data.
 - UT_Counties.shp shapefile geometry data used for county location information for the timeseries water use data.

  ## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Utah Aggregated Water Budget Data: https://drive.google.com/drive/folders/1-9uX9PHE_hHbqfR3DEWPDuVurJLlyJm1?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share UDWRE's aggregated water budget data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *UT_Aggregated Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the UDWRE's aggregated water budget data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(AggregatedAmounts_facts)* is dependent on the previous files.  Those six code files are as follows...

- 0_UTAggregatedDataPreprocess.ipynb
- 1_UTag_Methods.py
- 2_UTag_Variables.py
- 3_UTag_Organizations.py
- 4_UTag_WaterSources.py
- 5_UTag_ReportingUnits.py
- 6_UTag_AggregatedAmounts_facts.py


***
### 0) Code File: 0_UTAggregatedDataPreprocess.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - Water_Budget_WaDE_Compatible_Table.xlsx
 - UT_Subarea.shp
 - UT_HUC8.shp
 - UT_Counties.shp

#### Outputs:
 - P_utAggMaster.csv
 - P_utGeometry.csv

#### Operation and Steps:
- Read water use input file and generate temporary input dataframe.
- Create WaDE specific *VariableSpecificCV* field using **UT_VariableCV**, **BeneficialUseCategory**, & **WaterSourceID** input fields.
- Generate WaDE specific field *WaterSourceNativeID* from **WaterSourceID** field.  Used to identify unique watersources of water.
- Read in shapefile data and generate temporary input dataframes for each file.
- Concatenate each shapefile dataframe into one long dataframe.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv files, *P_utAggMaster.csv* & *P_caGeometry.csv*.


***
### 1) Code File: 1_UTag_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign state agency data  info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
UTag_M1 | Surface Ground Water | Estimate


***
### 2) Code File: 2_UTag_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign state agency data info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
    - WaDE *VariableSpecificCV* = see *0_UTAggregatedDataPreprocess.ipynb* for specifics.
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV | VariableCV | VariableSpecificCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------
UTag_V1 | 1 | Annual | AFY | Consumptive Use | Consumptive Use_Annual_Agriculture_Surface and Groundwater


***
### 3) Code File: 3_UTag_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign state agency data info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName  | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
UTag_O1 | Utah Division of Water Resources | Craig Miller| https://water.utah.gov/


***
### 4) Code File: 4_UTag_WaterSources.py
Purpose: generate a list of water sources specific to an aggregated water budget data area.

#### Inputs:
- P_utAggMaster.csv

#### Outputs:
- watersources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency data info to the *WaDE WaterSources* specific columns.  See *UT_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceNativeID* = *in_WaterSourceNativeID*, see *0_UTAggregatedDataPreprocess.ipynb* for specifics.
    - *WaterSourceTypeCV* = **WaterSourceID**.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* field.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
UTag_WS1 | Fresh | Unspecified | WaDEUT_WS1 | Fresh_SW_GW

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_UTag_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency specific area on aggregated water budget data.

#### Inputs:
- P_utAggMaster.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *UT_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = **ReportingUnitName**.
    - *ReportingUnitNativeID* = **ReportingUnitNativeID**.
    - *ReportingUnitTypeCV* = **ReportingUnitTypeCV**.
    - *Geometry* = WKT created **geometry**, see *0_UTAggregatedDataPreprocess.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | ReportingUnitName | ReportingUnitNativeID | ReportingUnitTypeCV 
---------- | ---------- | ------------ | ------------ 
UTag_RU1 | Beaver | 49001 | County

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV


***
### 6) Code File: 6_UTag_AggregatedAmounts_facts.py
Purpose: generate master sheet of state agency specified area aggregated water budget information to import into WaDE 2.0.

#### Inputs:
- P_utAggMaster.csv
- variables.csv
- watersources.csv
- sites.csv

#### Outputs:
- aggregatedamounts.csv
- aggregatedamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *UT_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *ReportingUnitUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **Amount**.
    - *BeneficialUseCategory* = **BeneficialUseCategory**.
    - *ReportYearCV* = **ReportYearCV**.
    - *TimeframeEnd* = **TimeframeEnd**.
    - *TimeframeStart* = **TimeframeStart**.
- Perform error check on output dataframe.
- Export output dataframe *aggregatedamounts.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | ReportingUnitUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | -----------
UTag_M1 | UTag_O1 | UTag_RU1 | UTag_V1 | UTag_WS1 | 80061.753287 | Agriculture | 2005

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- ReportingUnitUUID
- Amount


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Utah Division of Water Resources (UDWRE)](https://water.utah.gov/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>

UDWRE DNRC Staff
- Craig Miller <craigmiller@utah.gov>
