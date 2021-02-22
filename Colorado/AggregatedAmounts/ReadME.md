# CODWR Aggregated Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting aggregated water budget data made available by the [Colorado Division of Water Resources (CODWR)](https://dwr.colorado.gov/about-us/contact-us/denver-office), for inclusion into the Water Data Exchange (WaDE) project.   WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Data Utilized
The following data was used for aggregated water budget...

- **DWR__Surface_Water_Supply_Index_Component_by_HUC** xlsc file contained surface water aggregated water budget data and info and was obtained from the provided [DWR Surface Water Supply Index Component by HUC data site](https://data.colorado.gov/Water/DWR-Surface-Water-Supply-Index-Component-by-HUC/xbs6-xrne/data).
- **CO_HUC8.shp** files were used to extract geometry and create shape files, and were on hand from WaDE 1.0 data original data files.
   

From the above mentioned inputs, 1 unique file was used as input to the Python codes that prepare WaDE 2.0 input files.  Input files used are as follows...
 - DWR__Surface_Water_Supply_Index_Component_by_HUC_input.xlsx

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CODWR's aggregated water budget data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *CO_Aggregated Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the CODWR's aggregated water budget data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(AggregatedAmounts_facts)* is dependent on the previous files.  Those six code files are as follows...

- 0_CO Aggregated Data Preprocess.ipynb
- 1_COagg_Methods.py
- 2_COagg_Variables.py
- 3_COagg_Organizations.py
- 4_COagg_WaterSources.py
- 5_COagg_ReportingUnits.py
- 6_COagg_AggregatedAmounts_facts.py


***
### 0) Code File: 0_CO Aggregated Data Preprocess.ipynb
Purpose: Pre-process the Arizona input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
- DWR__Surface_Water_Supply_Index_Component_by_HUC_input.xlsx
- CO_HUC8.shp

#### Outputs:
 - P_COagg_ru.csv

#### Operation and Steps:
- Read the input file and generate temporary input dataframe.
- Create WadE specific *TimeframeStart* and *TimeframeEnd* by concatenating **Report Year** with **Report Month**, make assumption that start day is a *1* and end day is a *28*.
- For simplicity, drop columns not needed for WaDE input at this time: **Basin**, '**Component NEP**, & **Report Month**.
- Generated WKT from *CO_HUC8.shp* file to create *geometry* WaDE input.
- Inspect dataframes for errors.
- Export output dataframe as new csv files, *P_COagg_ru.csv*.


***
### 1) Code File: 1_COagg_Methods.py
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
CO_SWSIModels | Surface Water | Modeled


***
### 2) Code File: 2_COagg_Variables.py
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
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
CO_Supply_1 | 1 | Year | AFY


***
### 3) Code File: 3_COagg_Organizations.py
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
CODWR | Colorado Division of Water Resources | https://dwr.colorado.gov/about-us/contact-us/denver-office


***
### 4) Code File: 4_COagg_WaterSources.py
Purpose: generate a list of water sources specific to an aggregated water budget data area.

#### Inputs:
- P_COagg_ru.csv

#### Outputs:
- WaterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency data info to the *WaDE WaterSources* specific columns.  See *CO_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = **Component Name**.
    - *WaterSourceNativeID* = **Component ID**.
    - *WaterSourceTypeCV* = Surface Water.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by specific *WaterSourceNativeID* field.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
COag_WS1 | Fresh | ANTERO RESERVOIR | 06016010 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_COagg_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency specific area on aggregated water budget data.

#### Inputs:
- P_COagg_ru.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *CO_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = **HUC8 Name**.
    - *ReportingUnitNativeID* = **HUC8**.
    - *ReportingUnitTypeCV* = *HUC8*.
    - *Geometry* = WKT created **geometry**, see *0_CO Aggregated Data Preprocess.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | ReportingUnitName | ReportingUnitNativeID | ReportingUnitTypeCV 
---------- | ---------- | ------------ | ------------ 
COag_RU1 | South Platte Headwater | 10190001 | South Platte Headwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV


***
### 6) Code File: 6_COagg_AggregatedAmounts_facts.py
Purpose: generate master sheet of state agency specified area aggregated water budget information to import into WaDE 2.0.

#### Inputs:
- P_COagg_ru.csv
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
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *CO_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **Component Volume**.
    - *ReportYearCV* = **Report Year**.
    - *TimeframeStart* = **Report Year** with **Report Month**, see *0_CO Aggregated Data Preprocess.ipynb* for specifics.
    - *TimeframeEnd* = **Report Year** with **Report Month**, see *0_CO Aggregated Data Preprocess.ipynb* for specifics.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | ReportingUnitUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | -----------
CO_SWSIModels | CODWR | COag_RU1 | CO_Supply_1| COag_WS1 | 19300 | Unspecified | 2010

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- ReportingUnitUUID
- Amount


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Colorado Division of Water Resources (CODWR)](https://dwr.colorado.gov/about-us/contact-us/denver-office).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

CODWR Staff
- Doug Stenzel <doug.stenzel@state.co.us>