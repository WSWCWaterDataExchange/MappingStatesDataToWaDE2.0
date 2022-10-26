# ADWR Aggregated Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting aggregated water budget data made available by the [Arizona Department of Water Resources (ADWR)](https://new.azwater.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Source Data Utilized
The following data was used for aggregated water budget...

- **AMA Demand Supply from DW**, and was obtained from the ADWR website at:  http://www.azwater.gov/querycenter/query.aspx?qrysessionid=8CF17C8B1CB88E14E0534C64850A39FA
- **AMA shape files**, and was obtained from the ADWR website at: https://new.azwater.gov/gis.
- **AMA WaterSourceType Dictionary.xlsx**, which contains a water source type dictionary, and was obtained from meeting / email correspondence with ADWR.

Two unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - AMA Demand Supply from DW_use as input.xlsx
 - AMA_and_INA.shp
 - AMA WaterSourceType Dictionary.xlsx

 ## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Arizona Aggregated Water Budget Data: https://drive.google.com/drive/folders/1aGpDOmXBYEsOJkwWgJzpA4JOP3wvO_Cp?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share ADWR's aggregated water budget data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *AZ_Aggregated Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the ADWR's aggregated water budget data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(AggregatedAmounts_facts)* is dependent on the previous files.  Those six code files are as follows...

- 0_AZAggregatedDataPreprocess.ipynb
- 1_AZagg_Methods.py
- 2_AZagg_Variables.py
- 3_AZagg_Organizations.py
- 4_AZagg_WaterSources.py
- 5_AZagg_ReportingUnits.py
- 6_AZagg_AggregatedAmounts_facts.py


***
### 0) Code File: 0_AZAggregatedDataPreprocess.ipynb
Purpose: Pre-process the Arizona input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - AMA Demand Supply from DW_use as input.xlsx
 - AMA_and_INA.shp
 - AMA WaterSourceType Dictionary.xlsx (added manually into python dictionary)

#### Outputs:
 - P_AZagg.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.
- Create inputWaterSourceTypeCV from provided AMA WaterSourceType Dictionary.xlss file.
- Dropped unnecessary columns for WaDE input, **PARENT WATER TYPE OR SECTOR** & **BUDGET ELEMENT**.
- Dropped and only kept rows who's **CATEGORY** value was either *Supply* or *Demand*.
- Aggregated data based on **AMA**,**YEAR**, **SECTOR**, **CATEGORY**, & **inputWaterSourceTypeCV** to quantity an annual year value for **QUANTITY**.
- Generated WKT from AMA_and_INA.shp file to create *Geometry* WaDE input.
- Export output dataframe as new csv file, *P_AZagg.csv*.


***
### 1) Code File: - 1_AZagg_Methods.py
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
AMA_Aggregated Models | Surface Ground Water | Modeled


***
### 2) Code File: 2_AZagg_Variables.py
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
AZ_Demand | 1 | Year | AFY


***
### 3) Code File: 3_AZagg_Organizations.py
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
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
ADWR_AMA | Arizona Department of Water Resources | Lisa Williams | http://gisdata-azwater.opendata.arcgis.com/


***
### 4) Code File: 4_AZagg_WaterSources.py
Purpose: generate a list of water sources specific to an aggregated water budget data area.

#### Inputs:
- P_AZagg.csv

#### Outputs:
- WaterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency data info to the *WaDE WaterSources* specific columns.  See *AZ_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = generated list of sources provided by the ADWR, see AMA WaterSourceType Dictionary.xlsx and *0_AZAggregatedDataPreprocess.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* field.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
AZag_WS3 | Fresh | Unspecified | Unspecified | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_AZagg_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency specific area on aggregated water budget data.

#### Inputs:
- P_AZagg.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *AZ_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = **AMA**.
    - *Geometry* = WKT created **Geometry**, see *0_AZAggregatedDataPreprocess.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName* field.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | ReportingUnitName | ReportingUnitTypeCV 
---------- | ---------- | ------------ 
AZag_RU1 | PHOENIX AMA | Active Management Area

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV


***
### 6) Code File: 6_AZagg_AggregatedAmounts_facts.py
Purpose: generate master sheet of state agency specified area aggregated water budget information to import into WaDE 2.0.

#### Inputs:
- P_AZagg.csv
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
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *AZ_Aggregated Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **QUANTITY**.
    - *BeneficialUseCategory* = **SECTOR**.
    - *ReportYearCV* = **YEAR**.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | ReportingUnitUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | -----------
AZ_AMAModels | ADWR_AMA | AZag_RU1 | AZ_Demand | AZag_WS1 | 1265635 | Agricultural | 1985

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- ReportingUnitUUID
- Amount


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Arizona Department of Water Resources (ADWR)](https://new.azwater.gov/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

ADWR Staff
-
-