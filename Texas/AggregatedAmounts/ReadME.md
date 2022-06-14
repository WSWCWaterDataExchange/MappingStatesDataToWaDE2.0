# TWDB Aggregated Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting aggregated water budget data made available by the [Texas Water Development Board (TWDB) ](http://www.twdb.texas.gov/index.asp), for inclusion into the Water Data Exchange (WaDE) project.   WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Source Data Utilized
The following data was used for aggregated water budget...

- **2000-2016 Historical Water Use Estimates** csv files contained aggregated water budget data and info and were obtained from the provided [TWDB Historical Water Use Estimates](http://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp).  Each year is separated out into two different area types: Basin and County.  Information for each area type can be found in the **SumFinal_BasinReport.xlsx** and **SumFinal_CountyReport.xlsx** per year respectively.
- Texas County and Basin shapefiles data retrieved from personal correspondence via email from between the TWDB and the WSWC.

## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Texas Aggregated Time Series Data: https://drive.google.com/drive/folders/103lh1q-bRVS-_vncKSiVSxNieKByEDkL?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share TWDB's aggregated water budget data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *[TX_Aggregated Schema Mapping to WaDE_QA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Texas/AggregatedAmounts/TX_Aggregated%20Schema%20Mapping%20to%20WaDE_QA.xlsx)*.  Six executable code files were used to extract the TWDB's aggregated water budget data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(AggregatedAmounts_facts)* is dependent on the previous files.  Those six code files are as follows...

- 0_TXAggregatedDataPreprocess.ipynb
- 1_TXagg_Methods.py
- 2_TXagg_Variables.py
- 3_TXagg_Organizations.py
- 4_TXagg_WaterSources.py
- 5_TXagg_ReportingUnits.py
- 6_TXagg_AggregatedAmounts_facts.py


***
### 0) Code File: 0_TXAggregatedDataPreprocess.ipynb
Purpose: Pre-process the Arizona input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - SumFinal_BasinReport.xlsx, for 2000-2016
 - SumFinal_CountyReport.xlsx, for 2000-2016
 - County and Basin shapefiles.

#### Outputs:
 - P_txAggMaster.csv
 - P_TXGeometry.csv

#### Operation and Steps:
- Read the Basin.csv input files for 2000-2016, concatenate into a single basin dataframe.
- Basin data needs to be restructured with beneficial use per water amounts by year.
    - Preserve **Year**, **Basin**, and **Population** columns.
    - Include *TX_BenUse* column, based on column names.
    - Concatenate each *TX_BenUse* column entry with it's respective Texas **SumFinal_BasinReport.xlsx** column field.
    - *ReportingUnitType* = Basin.
- Read in County.csv input files for 2000-2016, concatenate into a single basin dataframe.
- County data needs to be restructured with beneficial use per water amounts by year.
    - Preserve **Year**, **Basin**, and **Population** columns.
    - Include *TX_BenUse* column, based on column names.
    - Concatenate each *TX_BenUse* column entry with it's respective Texas **SumFinal_CountyReport.xlsx** column field.
    - *ReportingUnitType* = County.
- Concatenate Basin and County dataframes into single dataframe.
- Assign *WaterSourceType* based on respective Texas beneficial use.
- Assign *TimeframeStart* & *TimeframeEnd* using **Year**, and making assumptions that start month and day is 01/01, and end is 12/31.
- Repair string errors in beneficial use columns.
- Generate WaDE specific field *WaterSourceNativeID* from *WaterSourceType* fields.  Used to identify unique sources of water.
- Generate WaDE specific field *ReportingUnitNativeID* from area name and area type fields.  Used to identify unique reporting units.
- Generated WKT from the County and Basin shapefiles, used to to create *geometry* WaDE input.
- Export output dataframe as new csv files, *P_txAggMaster.csv* & *P_TXGeometry.csv*.


***
### 1) Code File: 1_TXagg_Methods.py
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
TXag_M1 | Unspecified | Water Use


***
### 2) Code File: 2_TXagg_Variables.py
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
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV | VariableCV | VariableSpecificCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------
TXag_V1 | 1 | Cumulative | AFY | Consumptive Use | Consumptive Use_Annual_Irrigation_Groundwater


***
### 3) Code File: 3_TXagg_Organizations.py
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
OrganizationUUID | OrganizationName  | OrganizationWebsite
---------- | ---------- | ------------
TXag_O1 | Texas Water Development Board | http://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp


***
### 4) Code File: 4_TXagg_WaterSources.py
Purpose: generate a list of water sources specific to an aggregated water budget data area.

#### Inputs:
- P_txAggMaster.csv

#### Outputs:
- watersources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency data info to the *WaDE WaterSources* specific columns.  See *[TX_Aggregated Schema Mapping to WaDE_QA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Texas/AggregatedAmounts/TX_Aggregated%20Schema%20Mapping%20to%20WaDE_QA.xlsx)* for specific details.  Items of note are as follows...
    - *WaterSourceNativeID* = custom WaDE specific ID of *in_WaterSourceNativeID*, see *0_TXAggregatedDataPreprocess.ipynb* for specifics.
    - *WaterSourceTypeCV* = *in_WaterSourceType*, see *0_TXAggregatedDataPreprocess.ipynb* for specifics. Based on provided Texas beneficial use columns.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* field.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
TXag_WS1 | Fresh | Unspecified | WaDETX_WS1 | Reuse

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_TXagg_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency specific area on aggregated water budget data.

#### Inputs:
- P_txAggMaster.csv
- P_TXGeometry.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *[TX_Aggregated Schema Mapping to WaDE_QA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Texas/AggregatedAmounts/TX_Aggregated%20Schema%20Mapping%20to%20WaDE_QA.xlsx)* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = respective **Basin** and **County** fields.
    - *ReportingUnitNativeID* = custom WaDE specific ID of *in_ReportingUnitNativeID*, see *0_TXAggregatedDataPreprocess.ipynb* for specifics.
    - *ReportingUnitTypeCV* = Basin or County respectively.
    - *geometry* = WKT created **geometry**, see *0_TXAggregatedDataPreprocess.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | ReportingUnitName | ReportingUnitTypeCV | StateCV
---------- | ---------- | ------------ | ------------
TXag_RU1 | BRAZOS | Basin | TX

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV


***
### 6) Code File: 6_TXagg_AggregatedAmounts_facts.py
Purpose: generate master sheet of state agency specified area aggregated water budget information to import into WaDE 2.0.

#### Inputs:
- P_txAggMaster.csv
- methods.csv
- variables.csv
- organizations.csv
- watersources.csv
- sites.csv

#### Outputs:
- aggregatedamounts.csv
- aggregatedamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *[TX_Aggregated Schema Mapping to WaDE_QA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Texas/AggregatedAmounts/TX_Aggregated%20Schema%20Mapping%20to%20WaDE_QA.xlsx)* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *ReportingUnitUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = *in_Amount*, see *0_TXAggregatedDataPreprocess.ipynb* for specifics.
    - *BeneficialUseCategory* = *TX_BenUse*, see *0_TXAggregatedDataPreprocess.ipynb* for specifics.
    - *PopulationServed* = **Population**.
    - *ReportYearCV* = **Year**.
    - *TimeframeEnd* = *inTimeframeEnd*, see *0_TXAggregatedDataPreprocess.ipynb* for specifics.  Utilizes **Year**.
    - *TimeframeStart* = *inTimeframeStart*, see *0_TXAggregatedDataPreprocess.ipynb* for specifics.  Utilizes **Year**.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | ReportingUnitUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | -----------
TXag_M1 | TXag_O1 | TXag_RU1 | TXag_V1 | TXag_WS1 | 15820 | Irrigation | 2015

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- ReportingUnitUUID
- Amount


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Texas Water Development Board (TWDB) ](http://www.twdb.texas.gov/index.asp).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

TWDB Staff
- Bill Billingsley <bill.billingsley@twdb.texas.gov>