# NEDNR Aggregated Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting aggregated water budget data made available by the [Nebraska Department of Natural Resources (NEDNR)](https://dnr.nebraska.gov/contact)), for inclusion into the Water Data Exchange (WaDE) project.   WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Source Data Utilized
The following data was used for aggregated water budget...

- **INSIGHT_FinalBasinData_20151102** csv file containing basin wide aggregated water supply and demand data and info and were obtained from the provided [Insight](https://nednr.nebraska.gov/insight/about.html) services.  Data used was for the years 1988-2012.
- **INSIGHT_FinalSubBasinData_20151102** csv file containing subbasin wide aggregated water supply and demand data and info and were obtained from the provided [Insight](https://nednr.nebraska.gov/insight/about.html) services.  Data used was for the years 1988-2012.
- **Insight Shape Files** for both basin and subbasin aggregated water supply and demand ares, obtain from obtained from the provided [Insight](https://nednr.nebraska.gov/insight/about.html) services.

From the above mentioned services, 2 unique files were used as input to the Python codes that prepare WaDE 2.0 input files.  Input files used are as follows...
 - INSIGHT_FinalBasinData_20151102_input.csv
 - INSIGHT_FinalSubBasinData_20151102_input.csv

 ## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Nebraska Aggregated Time Series Data: https://drive.google.com/drive/folders/1Me_kk6HmZ4t4eU67j2ISXOnGbk_SQzGY?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NEDNR's aggregated water budget data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NE_Aggregated Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the NEDNR's aggregated water budget data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(AggregatedAmounts_facts)* is dependent on the previous files.  Those six code files are as follows...

- 0_NEAggregatedDataPreprocess.ipynb
- 1_NEag_Methods.py
- 2_NEag_Variables.py
- 3_NEag_Organizations.py
- 4_NEag_WaterSources.py
- 5_NEag_ReportingUnits.py
- 6_NEag_AggregatedAmounts_facts.py


***
### 0) Code File: 0_NEAggregatedDataPreprocess.ipynb
Purpose: Pre-process the Arizona input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - INSIGHT_FinalBasinData_20151102_input.csv
 - INSIGHT_FinalSubBasinData_20151102_input.csv
 - InsightShapeFiless.shp


#### Outputs:
 - P_neAgMaster.csv
 - P_neAgGeometry.csv

#### Operation and Steps:
- Read the basin, subbasin, and shape file input files and generate output dataframes for each.
- For basin data...
    - Want to split the data into 7 different times frames based on water source (see WaterSourceTypeCV), variable (see VariableSpecificCV), and beneficial use (see BeneficialUseCategory) type.
    - *VariableSpecificCV* = "Depletion_Annual_Total_Surface Water", "Depletion_Annual_Total_Groundwater", "Consumptive Use_Annual_Total_Groundwater", "Consumptive Use_Annual_Irrigation_Groundwater", "Consumptive Use_Annual_Municipal_Groundwater", "Consumptive Use_Annual_Industrial_Groundwater", "Demand_Annual_Total_Surface Water"
    - *WaterSourceTypeCV* = "Groundwater" or *Surface Water* depending on *VariableSpecificCV*.
    - *ReportingUnitName* = **Basin**
    - *ReportingUnitNativeID* = **BasinID**
    - *ReportingUnitTypeCV* = "Basin"
    - *ReportYearCV* = **Year**
    - *BeneficialUseCategory* = "Total", "Irrigation", "Industrial", & "Municipal" depending on *VariableSpecificCV*.
    - *Amount* = **SWDTotal_Annual**, **GWDP_Annual**, **GWCTotal_Annual**, **GWCIrrigation_Annual**, **GWCMunicipal_Annual**, **GWCIndustrial_Annual**, **SWDemandTotal_Annual** depending on *VariableSpecificCV*.
    - Concatenate each temp dataframe into one long basin out dataframe, *df_BasinOUT*.
- For subbasin data...
    - Want to split the data into 7 different times frames based on water source (see WaterSourceTypeCV), variable (see VariableSpecificCV), and beneficial use (see BeneficialUseCategory) type.
        - *VariableSpecificCV* = "Depletion_Annual_Total_Surface Water", "Depletion_Annual_Total_Groundwater", "Consumptive Use_Annual_Total_Groundwater", "Consumptive Use_Annual_Irrigation_Groundwater", "Consumptive Use_Annual_Municipal_Groundwater", "Consumptive Use_Annual_Industrial_Groundwater", "Demand_Annual_Total_Surface Water"
    - *WaterSourceTypeCV* = "Groundwater" or *Surface Water* depending on *VariableSpecificCV*.
    - *ReportingUnitName* = **Basin**
    - *ReportingUnitNativeID* = **BasinID**
    - *ReportingUnitTypeCV* = "Subbasin"
    - *ReportYearCV* = **Year**
    - *BeneficialUseCategory* = "Total", "Irrigation", "Industrial", & "Municipal" depending on *VariableSpecificCV*.
    - *Amount* = **SWDTotal_Annual**, **GWDP_Annual**, **GWCTotal_Annual**, **GWCIrrigation_Annual**, **GWCMunicipal_Annual**, **GWCIndustrial_Annual**, **SWDemandTotal_Annual** depending on *VariableSpecificCV*.
    - Concatenate each temp dataframe into one long basin out dataframe, *df_SubbasinOUT*.
- Concatenate *df_BasinOUT* & *df_SubbasinOUT* together to create one long output dataframe, *df_out*.
- Generate WaDE specific field *WaterSourceTypeCV* fields.  Used to identify unique sources of water.
- For Shapefile data...
    - Split into 2 different temp dataframes for specific for basin and subbasin types.
    - *ReportingUnitName* = **Basin** & **Subbasin**
    - *ReportingUnitNativeID* = **BID** & **SubID**
    - *ReportingUnitTypeCV* = "Basin" or "Subbasin"
    - *Geomerty* = **geometry**
    - Concatenate each basin and subbasin shapefile dataframe into one long out dataframe, *df_shape_out*.
- Perform error check on output dataframes.
- Export output dataframes *P_neAgMaster.csv* & *P_neAgGeometry.csv*.



***
### 1) Code File: 1_NEag_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign state agency data info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
NEag_M1 | Surface Ground Water | Modeled



***
### 2) Code File: 2_NEag_Variables.py
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
NEag_V1 | 1 | Annual | AFY | Depletion | Depletion_Annual_Total_Surface Water



***
### 3) Code File: 3_NEag_Organizations.py
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
NEag_O1 | Nebraska Department of Natural Resources | https://dnr.nebraska.gov/contact



***
### 4) Code File: 4_NEag_WaterSources.py
Purpose: generate a list of water sources specific to an aggregated water budget data area.

#### Inputs:
- P_neAgMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency data info to the *WaDE WaterSources* specific columns.  See *NE_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = "Groundwater" or "Surface Water" (see *0_NEAggregatedDataPreprocess.ipynb* for specifics).
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* field.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *waterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NEag_WS1 | Fresh | Unspecified | WaDENE_WS1 | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_NEag_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency specific area on aggregated water budget data.

#### Inputs:
- P_neAgMaster.csv
- P_neAgGeometry.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *NE_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *Geometry* = WKT created **Geometry** (see *0_NEAggregatedDataPreprocess.ipynb* for specifics).
    - *ReportingUnitName* = in_ReportingUnitName (see *0_NEAggregatedDataPreprocess.ipynb* for specifics).
    - *ReportingUnitNativeID* = in_ReportingUnitNativeID (see *0_NEAggregatedDataPreprocess.ipynb* for specifics).
    - *ReportingUnitTypeCV* = in_ReportingUnitTypeCV (see *0_NEAggregatedDataPreprocess.ipynb* for specifics).
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | ReportingUnitName | ReportingUnitTypeCV 
---------- | ---------- | ------------ 
NEag_RU1 | BIG BLUE | Basin

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV



***
### 6) Code File: 6_NEag_AggregatedAmounts_facts.py
Purpose: generate master sheet of state agency specified area aggregated water budget information to import into WaDE 2.0.

#### Inputs:
- P_neAgMaster.csv
- methods.csv
- variables.csv
- organizations.csv
- watersources.csv
- reportingunits.csv

#### Outputs:
- aggregatedamounts.csv
- aggregatedamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *NE_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *ReportingUnitUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = in_Amount (see *0_NEAggregatedDataPreprocess.ipynb* for specifics).
    - *BeneficialUseCategory* = "Combined"
    - *ReportYearCV* = in_ReportYearCV (see *0_NEAggregatedDataPreprocess.ipynb* for specifics).
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | ReportingUnitUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | -----------
NEag_M1 | NEag_O1 | NEag_RU1 | NEag_V1 | NEag_WS1 | 195533 | Total | 1988

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *aggregatedamounts_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- ReportingUnitUUID
- Amount


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nebraska Department of Natural Resources (NEDNR)](https://dnr.nebraska.gov/contact)).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>

NEDNR Staff
- Jennifer Schellpeper <jennifer.schellpeper@nebraska.gov>