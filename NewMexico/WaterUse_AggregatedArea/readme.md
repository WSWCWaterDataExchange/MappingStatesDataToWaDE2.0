# NMOSE Aggregated Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting aggregated water budget data made available by the [New Mexico Office of the State Engineer (NMOSE)](https://www.ose.state.nm.us/), for inclusion into the Water Data Exchange (WaDE) project.   WaDE enables states to share data with each other and the public in a more streamlined and consistent way.  WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Data Utilized
The following data was used for aggregated water budget...

- [**County Water Use Data**](https://www.ose.state.nm.us/WUC/wuc_waterUseData.php) with a summary of county wide aggregated water groundwater and surface water withdrawal data by beneficial use in increments of 5 years () (1990, 1995, 2000, 2005, 2010, 2015).  Input files provided by personal contact.  Please contact NMOSE for data.

From the above mentioned services unique files were used as input to the Python codes that prepare WaDE 2.0 input files.  Input files used are as follows...
 - Summary of withdrawals by county 90-15_input.xlsx, a summary of the withdrawal data by county
 - CountyShape.shp, shapefile data for the counties

 ## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- New Mexico Aggregated Time Series Data: https://drive.google.com/drive/folders/1QFlWNcGvQESFSPuw_nrdUp_AnYs1Rhry?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NMOSE's aggregated water budget data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NM_Aggregated Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the NMOSE's aggregated water budget data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(AggregatedAmounts_facts)* is dependent on the previous files.  Those six code files are as follows...

- 0_NMAggregatedDataPreprocess.ipynb
- 1_NMag_Methods.py
- 2_NMag_Variables.py
- 3_NMag_Organizations.py
- 4_NMag_WaterSources.py
- 5_NMag_ReportingUnits.py
- 6_NMag_AggregatedAmounts_facts.py


***
### 0) Code File: 0_NMAggregatedDataPreprocess.ipynb
Purpose: Pre-process the Arizona input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - Summary of withdrawals by county 90-15_input.xlsx
 - CountyShape.shp


#### Outputs:
 - P_nmAgMaster.csv
 - P_nmAgGeometry.csv

#### Operation and Steps:
- Read in summary of withdrawal data generate temporary dataframe.
- There are 9 beneficial uses and 2 different water source types = 18 different time series of interest.
    - Want to split the data into 18 different times frames based on water source (see WaterSourceTypeCV), and beneficial use (see BeneficialUseCategory) type.
    - *VariableSpecificCV* = "Withdrawal_Annual_Commercial_Groundwater", "Withdrawal_Annual_Domestic_Groundwater", "Withdrawal_Annual_Industrial_Groundwater", "Withdrawal_Annual_Irrigated Agriculture_Groundwater", "Withdrawal_Annual_Livestock_Groundwater", "Withdrawal_Annual_Mining_Groundwater", "Withdrawal_Annual_Power_Groundwater", "Withdrawal_Annual_Public Supply_Groundwater", "Withdrawal_Annual_Reservoir Evaporation_Groundwater", "Withdrawal_Annual_Commercial_Surface Water", "Withdrawal_Annual_Domestic_Surface Water", "Withdrawal_Annual_Industrial_Surface Water", "Withdrawal_Annual_Irrigated Agriculture_Surface Water", "Withdrawal_Annual_Livestock_Surface Water", "Withdrawal_Annual_Mining_Surface Water", "Withdrawal_Annual_Power_Surface Water", "Withdrawal_Annual_Public Supply_Surface Water", "Withdrawal_Annual_Reservoir Evaporation_Surface Water"
    - *WaterSourceTypeCV* = "Groundwater" or *Surface Water* depending on *VariableSpecificCV*.
    - *ReportingUnitName* = **COUNTY**
    - *ReportingUnitNativeID* = **CN**
    - *ReportingUnitTypeCV* = "County"
    - *ReportYearCV* = **ReportYearCV**
    - *BeneficialUseCategory* = **CAT**, depending on *VariableSpecificCV*.
    - *Amount* = **WGW** for groundwater, & **WSW** for surface water values.
- Concatenate all temporary dataframes into single ouput, *dfout*.
- Generate WaDE specific fields *TimeFrameStart*  = "01/01" + **ReportYearCV** & *TimeFrameEnd* = "12/31" + **ReportYearCV**
- Generate WaDE specific field *WaterSourceNativeID* fields.  Used to identify unique sources of water.
- For Shapefile data...
    - Split into 2 different temp dataframes for specific for basin and subbasin types.
    - *ReportingUnitName* = **County** & **Subbasin**"
    - *Geomerty* = **geometry**
- Perform error check on output dataframes.
- Export output dataframes *P_nmAgMaster.csv* & *P_nmAgGeometry.csv*.



***
### 1) Code File: 1_NMag_Methods.py
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
NMag_M1 | Surface Ground Water | Water Use



***
### 2) Code File: 2_NMag_Variables.py
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
NMag_V1 | 1 | Annual | AFY | Withdrawal | Withdrawal_Annual_Commercial_Groundwater



***
### 3) Code File: 3_NMag_Organizations.py
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
NMag_O1 | New Mexico Office of the State Engineer | https://www.ose.state.nm.us/



***
### 4) Code File: 4_NMag_WaterSources.py
Purpose: generate a list of water sources specific to an aggregated water budget data area.

#### Inputs:
- P_nmAgMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency data info to the *WaDE WaterSources* specific columns.  See *NM_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = "Groundwater" or "Surface Water" (see *0_NMAggregatedDataPreprocess.ipynb* for specifics).
    - *WaterSourceNativeID* = in_WaterSourceNativeID (see *0_NMAggregatedDataPreprocess.ipynb* for specifics).
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* field.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *waterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NMag_WS1 | Fresh | Unspecified | WaDENM_WS1 | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_NMag_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency specific area on aggregated water budget data.

#### Inputs:
- P_nmAgMaster.csv
- P_nmAgGeometry.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *NM_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *Geometry* = WKT created **Geometry** (see *0_NMAggregatedDataPreprocess.ipynb* for specifics).
    - *ReportingUnitName* = in_ReportingUnitName (see *0_NMAggregatedDataPreprocess.ipynb* for specifics).
    - *ReportingUnitNativeID* = in_ReportingUnitNativeID (see *0_NMAggregatedDataPreprocess.ipynb* for specifics).
    - *ReportingUnitTypeCV* = in_ReportingUnitTypeCV (see *0_NMAggregatedDataPreprocess.ipynb* for specifics).
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | ReportingUnitName | ReportingUnitTypeCV 
---------- | ---------- | ------------ 
NMag_RU1 | Bernalillo | County

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV



***
### 6) Code File: 6_NMag_AggregatedAmounts_facts.py
Purpose: generate master sheet of state agency specified area aggregated water budget information to import into WaDE 2.0.

#### Inputs:
- P_nmAgMaster.csv
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
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *NM_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *ReportingUnitUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = in_Amount (see *0_NMAggregatedDataPreprocess.ipynb* for specifics).
    - *BeneficialUseCategory* = in_BeneficialUseCategory(see *0_NMAggregatedDataPreprocess.ipynb* for specifics).
    - *ReportYearCV* = in_ReportYearCV (see *0_NMAggregatedDataPreprocess.ipynb* for specifics).
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | ReportingUnitUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | -----------
NMag_M1 | NMag_O1 | NMag_RU1 | NMag_V1 | NMag_WS1 | 3711.30004882813 | Commercial (self-supplied) | 1990

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *aggregatedamounts_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- ReportingUnitUUID
- Amount


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [New Mexico Office of the State Engineer (NMOSE)](https://www.ose.state.nm.us/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>

NMOSE Staff
- Julie Valdez <julie.valdez@state.nm.us >