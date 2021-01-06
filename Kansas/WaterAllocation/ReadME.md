# KDADWR  Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Kansas Department of Agriculture's Division of Water Resources (KDADWR)](https://agriculture.ks.gov/divisions-programs/dwr), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- Point of diversion water quantity (qty) and location (wimas) data obtained from the Water Information Management and Analysis System (WIMAS): https://geoportal.kgs.ku.edu/geohydro/wimas/index.cfm?CFID=70602&CFTOKEN=1c898e89c26f094b-815CA8A9-FFF0-E432-AE5700215117F981


Two unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - qty_input.csv
 - wimas_input.csv

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share KDADWR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *KS_Allocation Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the KDADWR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those six code files are as follows...

- 0_PreProcessKansasWaterRightData.ipynb
- 1_KSwr_Methods.py
- 2_KSwr_Variables.py
- 3_KSwr_Organizations.py
- 4_KSwr_WaterSources.py
- 5_KSwr_Sites.py
- 6_KSwr_AllocationsAmounts_facts.py


***
### 0) Code File: 0_PreProcessKansasWaterRightData.ipynb
Purpose: Pre-process the Kansas input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - qty_input.csv
 - wimas_input.csv

#### Outputs:
 - P_KansasMaster.csv

#### Operation and Steps:
- Read the input files (qyt & wimas) and generate temporary input dataframes.
- Merge inputs using custom key, made from **wr_id** and **pdiv_id** fields merged together.
- Format **priority_date** field to %m/%d/%Y format.
- Format **longitude**, **latitude**, and **auth_quant** to float datatype.
- Generate right type field using provided KS terminology code and **right_type** field.
- Generate beneficial use field using provided KS terminology code and **umw_code** field.
- Generate watersource field using provided KS terminology code and **source** field.
- Generate status field using provided KS terminology code and **wrf_status** field.
- Generate basin name field using provided KS terminology code and **basin** field.
- Generate county name field using provided KS terminology code and **county** field.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_KansasMaster.csv*.


***
### 1) Code File: 1_KSwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **KDADWR** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
KDADWR_Water Rights | Surface Ground Water | Modeled


***
### 2) Code File: 2_KSwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **KDADWR** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
KDADWR_Allocation All | 1 | Year | AF


***
### 3) Code File: 3_KSwr_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **KDADWR** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
KDADWR | The Kansas Department of Agriculture, Division of Water Resources | Ginger Pugh | https://agriculture.ks.gov/home


***
### 4) Code File: 4_KSwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_KansasMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **KDADWR** info to the *WaDE WaterSources* specific columns.  See *KS_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = **basin**, see *0_PreProcessKansasWaterRightData.ipynb* for specifics.
    - *WaterSourceNativeID* = **basin**.
    - *WaterSourceTypeCV* = **WatersourceType**, see *0_PreProcessKansasWaterRightData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
KSwr_WS1 | Fresh | Saline River | Unspecified | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_KSwr_Sites.py
Purpose: generate a list of sites information.

#### Inputs:
- P_KansasMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **KDADWR** info to the *WaDE Site* specific columns.  See *KS_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *Latitude* = **latitude**.
    - *Longitude* = **longitude**.
    - *SiteNativeID* = **pdiv_id**.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ------------ | ------------ | ------------
KSwr_S1 | Unspecified | 38.9982 | -97.87295 | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_KSwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_KansasMaster.csv
- methods.csv
- variables.csv
- organizations.csv
- watersources.csv
- sites.csv

#### Outputs:
- waterallocations.csv
- waterallocations_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign **KDADWR** info to the *WaDE Water Allocations* specific columns.  See *KS_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationLegalStatusCV* = **wrf_status**, see *0_PreProcessKansasWaterRightData.ipynb* for specifics.
    - *AllocationNativeID* = **wr_id**.
    - *AllocationPriorityDate* = **priority_date**.
    - *AllocationTypeCV* = **right_type**, see *0_PreProcessKansasWaterRightData.ipynb* for specifics.
    - *AllocationVolume_AF* = **auth_quant**.
    - *BeneficialUseCategory* = **umw_code**, see *0_PreProcessKansasWaterRightData.ipynb* for specifics.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_AF | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
10001 | 394 | Certificated Issued | Irrigation

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- SiteUUID
- AllocationPriorityDate
- BeneficialUseCategory
- AllocationAmount or AllocationMaximum
- DataPublicationDate


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Kansas Department of Natural Resources and Conservation (KDADWR)](https://opendata-mtdnrc.hub.arcgis.com/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

Kansas DNRC Staff
- Ginger Pugh <Ginger.Pugh@ks.gov>