# NDWR Aggregated Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting aggregated water budget data made available by the [Nevada Division of Water Resources (NDWR)](http://water.nv.gov/), for inclusion into the Water Data Exchange (WaDE) project.   WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Data Utilized
The following data was used for aggregated water budget...

- **StateInv_2015_BasinPumpage.csv** & **StateInv_2017_BasinPumpage.csv** files that contained aggregated water pumpage budget data and info for basins in both 2015 and 2017, and were obtained from [NDWR GIS Data site](http://water.nv.gov/gisdata.aspx).
- **StateInv_2015_CountyPumpage.csv** & **StateInv_2017_CountyPumpage.csv** csv files that contained aggregated water pumppage budget data and info for counties in both 2015 and 2017, and were obtained from [NDWR GIS Data site](http://water.nv.gov/gisdata.aspx).
 - **NVBasinShapefile.shp** & **NVCountyShapefile.shp** shape files, obtained from the provided [NDWR GIS Data site](http://water.nv.gov/gisdata.aspx).
   
## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NDWR's aggregated water pumpage data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NV_Aggregated Schema Mapping to WaDE_QAR.xlsx*.  Six executable code files were used to extract the NDWR's aggregated water budget data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(AggregatedAmounts_facts)* is dependent on the previous files.  Those six code files are as follows...

- 0_NVAggregatedDataPreprocess.ipynb
- 1_NVag_Methods.py
- 2_NVag_Variables.py
- 3_NVag_Organizations.py
- 4_NVag_WaterSources.py
- 5_NVag_ReportingUnits.py
- 6_NVag_AggregatedAmounts_facts.py


***
### 0) Code File: 0_NVAggregatedDataPreprocess.ipynb
Purpose: Pre-process the state's input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - StateInv_2015_BasinPumpage.csv
 - StateInv_2017_BasinPumpage.csv
 - StateInv_2015_CountyPumpage.csv
 - StateInv_2017_CountyPumpage.csv
 - NVBasinShapefile.shp
 - NVCountyShapefile.shp


#### Outputs:
 - P_nvAggMaster.csv
 - P_nvGeometry.csv

#### Operation and Steps:
- Read the csv input files and generate temporary input dataframes, then concatenate together to form two larger basin and county dataframes.
- Perform the following actions to each dataframe:
    - Add *Year* value and include 2015 and 2017 respectively.
    - Add *ReportingUnitTypeCV* value and include Basin or County respectively.
    - *ReportingUnitName* = **BasinName** & **County**, respectively.
    - *ReportingUnitNativeID* = **BasinID** for basin data, create custom WaDE ID for county data.
    - Based on independent beneficial use columns from source data, transpose data by beneficial use and water amount values, fit to *Year*, *ReportingUnitTypeCV*, *ReportingUnitName* and *ReportingUnitNativeID* columns.
- Concatenate temporary basin and county dataframes together for single output dataframe.
- Create WaDE specific *TimeframeStart* & *TimeframeEnd* values by combining *01/01* & *12/31* with *Year* value, respectively.
- Generated WKT from provided NVBasinShapefile.shp & NVCountyShapefile.shp shapefiles to create *geometry* WaDE input.
- Export output dataframe as new csv files, *P_nvAggMaster.csv* & *P_nvGeometry.csv*.


***
### 1) Code File: - 1_NVag_Methods.py
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
NVDWR_Water Use | Unspecified | Water Use


***
### 2) Code File: 2_NVag_Variables.py
Purpose: generate legend of granular variables used on data collection specific to the state.

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
NVDWR_Withdrawal | 1 | Year | AFY


***
### 3) Code File: 3_NVag_Organizations.py
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
NVDWR | Nevada Division of Water Resources | http://water.nv.gov/index.aspx


***
### 4) Code File: 4_NVag_WaterSources.py
Purpose: generate a list of water sources specific to an aggregated water budget data area.

#### Inputs:
- P_nvAggMaster.csv

#### Outputs:
- WaterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency data info to the *WaDE WaterSources* specific columns.  See *NV_Aggregated Schema Mapping to WaDE_QAR.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = Unspecified.
    - *WaterSourceNativeID* = Unspecified.
    - *WaterSourceTypeCV* = Groundwater.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* field.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NVag_WS1 | Fresh | Unspecified | Unspecified | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_NVag_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency specific area on aggregated water budget data.

#### Inputs:
- P_nvAggMaster.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *NV_Aggregated Schema Mapping to WaDE_QAR.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = in_ReportingUnitName, see *0_NVAggregatedDataPreprocess.ipynb* for specifics.
    - *ReportingUnitNativeID* = in_ReportingUnitNativeID, see *0_NVAggregatedDataPreprocess.ipynb* for specifics.
    - *ReportingUnitTypeCV* = in_ReportingUnitType, see *0_NVAggregatedDataPreprocess.ipynb* for specifics.
    - *Geometry* = WKT created **geometry**, see *0_NVAggregatedDataPreprocess.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | ReportingUnitName | ReportingUnitTypeCV 
---------- | ---------- | ------------ 
NVag_RU1 | Long Valley | Basin

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV


***
### 6) Code File: 6_NVag_AggregatedAmounts_facts.py
Purpose: generate master sheet of state agency specified area aggregated water budget information to import into WaDE 2.0.

#### Inputs:
- P_nvAggMaster.csv
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
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *NV_Aggregated Schema Mapping to WaDE_QAR.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = inAmount, see *0_NVAggregatedDataPreprocess.ipynb* for specifics.
    - *BeneficialUseCategory* = inBenUse, see *0_NVAggregatedDataPreprocess.ipynb* for specifics.
    - *ReportYearCV* = inYear, see *0_NVAggregatedDataPreprocess.ipynb* for specifics.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | ReportingUnitUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | -----------
NVDWR_Water Use | NVDWR | NVag_RU1 | NVDWR_Withdrawal | NVag_WS1 | 0 | Commercial | 2015

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- ReportingUnitUUID
- Amount


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nevada Division of Water Resources (NDWR)](http://water.nv.gov/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

NDWR Staff
- Brian McMenamy (IT Professional) <bmcmenamy@water.nv.gov>
- Levi Kryder (Chief Hydrology Section) <lkryder@water.nv.gov>
- Caitlan Jellema (Water Use Specialist) <cjellema@water.nv.gov>
- Stephanie Snider (GIS Analyst)