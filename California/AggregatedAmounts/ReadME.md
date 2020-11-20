# CDWR Aggregated Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting aggregated water budget data made available by the [California Department of Water Resources (CDWR)](https://data.ca.gov/dataset/water-plan-water-balance-data), for inclusion into the Water Data Exchange (WaDE) project.   WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Data Utilized
The following data was used for aggregated water budget...

- **CA-DWR-WaterBalance-Level2-DP-1000-year-DAUCO** csv files contained aggregated water budget data and info and were obtained from the provided [CDWR Water Plan Balance Data site](https://data.cnra.ca.gov/dataset/water-plan-water-balance-data).  Data used was for the years 2011-2016.  DAUCO files were used as they provided the most information.
- **Water_Plan_Planning_Areas-shp** files were used to extract geometry, create shape files, and were obtained from the [DWR Atlas](https://atlas-dwr.opendata.arcgis.com/datasets/a911dd793cae48f1a3662e08f4811382_0?geometry=-152.647%2C31.071%2C-85.894%2C43.276).
- **Hydrologic_Regions-shp** files were used to extract geometry, create shape files, and were obtained from the [DWR Atlas](https://atlas-dwr.opendata.arcgis.com/datasets/2a572a181e094020bdaeb5203162de15_0).
- **DAUCO-shp** files were used to extract geometry, create shape files, and were provided with previous WaDE 1.0 correspondence in the past between the CDWR and the WSWC.  DAUCO is more granular than the actual county shape (see below Figure 1).
   
![alt text](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/California/AggregatedAmounts/RawInputData/Images/DAUCOvsCounty.png)
**Figure 1:** Detailed Analysis Units by County (DAUCO) by CA vs County


From the above mentioned [CDWR ft site:](ftp://mae2.sdsc.edu/published/), 5 unique files were used as input to the Python codes that prepare WaDE 2.0 input files.  Input files used are as follows...
 - CA-DWR-WaterBalance-Level2-DP-1000-2011-DAUCO_input.csv
 - CA-DWR-WaterBalance-Level2-DP-1000-2012-DAUCO_input.csv
 - CA-DWR-WaterBalance-Level2-DP-1000-2013-DAUCO_input.csv
 - CA-DWR-WaterBalance-Level2-DP-1000-2014-DAUCO_input.csv
 - CA-DWR-WaterBalance-Level2-DP-1000-2015-DAUCO_input.csv
 - CA-DWR-WaterBalance-Level2-DP-1000-2016-DAUCO_input.csv

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CDWR's aggregated water budget data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *CA_Aggregated Schema Mapping to WaDE_QAR.xlsx*.  Six executable code files were used to extract the CDWR's aggregated water budget data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(AggregatedAmounts_facts)* is dependent on the previous files.  Those six code files are as follows...

- 0_CAAggregatedDataPreprocess.ipynb
- 1_CAagg_Methods.py
- 2_CAagg_Variables.py
- 3_CAagg_Organizations.py
- 4_CAagg_WaterSources.py
- 5_CAagg_ReportingUnits.py
- 6_CAagg_AggregatedAmounts_facts.py


***
### 0) Code File: 0_CAAggregatedDataPreprocess.ipynb
Purpose: Pre-process the Arizona input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - CA-DWR-WaterBalance-Level2-DP-1000-2011-DAUCO_input.csv
 - CA-DWR-WaterBalance-Level2-DP-1000-2012-DAUCO_input.csv
 - CA-DWR-WaterBalance-Level2-DP-1000-2013-DAUCO_input.csv
 - CA-DWR-WaterBalance-Level2-DP-1000-2014-DAUCO_input.csv
 - CA-DWR-WaterBalance-Level2-DP-1000-2015-DAUCO_input.csv
 - CA-DWR-WaterBalance-Level2-DP-1000-2016-DAUCO_input.csv
 - Water_Plan_Planning_Areas.shp
 - Hydrologic_Regions.shp
 - WaDECADAU.shp


#### Outputs:
 - P_caAggMaster.csv
 - P_caGeometry.csv

#### Operation and Steps:
- Read the DAUCO csv input files and generate temporary input dataframes, then concatenate together to form one large dataframe.
- For **Planing Area** reporting unit type, group by **PA**, **Year**, & **CategoryA**, and sum the **KAcreFt**.  Input into PA temporary dataframe.
- For **Hydrologic Region** reporting unit type, group by **HR_NAME**, **HR_CODE**, **Year**, & **CategoryA**, and sum the **KAcreFt**.  Input into HR temporary dataframe.
- For **Detailed Analysis Units by County** reporting unit type, group by **DAU**, **DAU_NAME**, **Year**, & **CategoryA**, and sum the **KAcreFt**.  Input into DAUCO temporary dataframe.
- Concatenate temporary, PA, HR, and DAUCO dataframes together.
- Inspect dataframes for errors.
- Generated WKT from AMA_and_INA.shp file to create *Geometry* WaDE input.
- Export output dataframe as new csv files, *P_caAggMaster.csv* & *P_caGeometry.csv*.


***
### 1) Code File: - 1_CAagg_Methods.py
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
CDWR_Water Use | Unspecified | Water Use


***
### 2) Code File: 2_CAagg_Variables.py
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
CA_Consumptive Use | 1 | Year | AFY


***
### 3) Code File: 3_CAagg_Organizations.py
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
CDWR | California Department of Water Resources |https://water.ca.gov/


***
### 4) Code File: 4_CAagg_WaterSources.py
Purpose: generate a list of water sources specific to an aggregated water budget data area.

#### Inputs:
- P_caAggMaster.csv

#### Outputs:
- WaterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency data info to the *WaDE WaterSources* specific columns.  See *CA_Aggregated Schema Mapping to WaDE_QAR.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = Groundwater, Surface Water.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* field.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
CAag_WS1 | Fresh | Unspecified | Unspecified | Groundwater, Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_CAagg_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency specific area on aggregated water budget data.

#### Inputs:
- P_caAggMaster.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *CA_Aggregated Schema Mapping to WaDE_QAR.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = inReportingUnitName, see *0_CAAggregatedDataPreprocess.ipynb* for specifics.
    - *ReportingUnitNativeID* = inReportingUnitNativeID, see *0_CAAggregatedDataPreprocess.ipynb* for specifics.
    - *ReportingUnitTypeCV* = inReportingUnitTypeCV, see *0_CAAggregatedDataPreprocess.ipynb* for specifics.
    - *Geometry* = WKT created **Geometry**, see *0_CAAggregatedDataPreprocess.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | ReportingUnitName | ReportingUnitTypeCV 
---------- | ---------- | ------------ 
CAag_RU1| 101 | Planning Area

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV


***
### 6) Code File: 6_CAagg_AggregatedAmounts_facts.py
Purpose: generate master sheet of state agency specified area aggregated water budget information to import into WaDE 2.0.

#### Inputs:
- P_caAggMaster.csv
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
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *CA_Aggregated Schema Mapping to WaDE_QAR.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = inAmount, see *0_CAAggregatedDataPreprocess.ipynb* for specifics.
    - *BeneficialUseCategory* = inBenUse, see *0_CAAggregatedDataPreprocess.ipynb* for specifics.
    - *ReportYearCV* = inYear, see *0_CAAggregatedDataPreprocess.ipynb* for specifics.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | ReportingUnitUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | -----------
CDWR_Water Use | CDWR | CAag_RU1 | CA_Consumptive Use | CAag_WS1 | 3389.59999999999 | Agricultural | 2011

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- ReportingUnitUUID
- Amount


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [California Department of Water Resources (CDWR)](https://data.ca.gov/dataset/water-plan-water-balance-data).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

CDWR Staff
- Gary Darling <Gary.Darling@water.ca.gov>
- Jennifer Stricklin <Jennifer.Stricklin@water.ca.gov>

San Diego Supercomputer Center
- John Helly <hellyj@ucsd.edu>