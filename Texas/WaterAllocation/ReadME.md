# TCEQ Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Texas Commission on Environmental Quality (TCEQ)](https://www.tceq.texas.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- Point of diversion (POD) water rights data were made available via the [Texas Water Rights Viewer](https://tceq.maps.arcgis.com/home/webmap/viewer.html?webmap=796b001513b9407a9818897b4dc1ec4d), and downloaded with [ArcGIS Pro](https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview).  

Input files used are as follows...

 - WaterRightPoint.csv
 

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share TCEQ's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *[TX_Allocation Schema Mapping to WaDE_QA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Texas/WaterAllocation/TX_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx)*.  Six executable code files were used to extract the TCEQ's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those six code files are as follows...

- 0_PreProcessTexasAllocationData.ipynb
- 1_TXwr_Methods.py
- 2_TXwr_Variables.py
- 3_TXwr_Organizations.py
- 4_TXwr_WaterSources.py
- 5_TXwr_Sites.py
- 6_TXwr_AllocationsAmounts_facts.py


***
### 0) Code File: 0_PreProcessTexasAllocationData.ipynb
Purpose: Pre-process the state agency's input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- WaterRightPoint.csv

#### Outputs:
 - P_TexasWRP.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframe.
- Repair string data.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_TexasWRP.csv*.


***
### 1) Code File: 1_TXwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **TCEQ** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
TCEQ_Water Rights | Surface Ground | Estimated


***
### 2) Code File: 2_TXwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **TCEQ** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
TCEQ_Allocation All | 1 | Year | CFS


***
### 3) Code File: 3_TXwr_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **TCEQ** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
TCEQ | Texas Commission on Environmental Quality | John-Cody Stalsby | https://www.tceq.texas.gov/


***
### 4) Code File: 4_TXwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_TexasWRP.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **TCEQ** info to the *WaDE WaterSources* specific columns.  See *[TX_Allocation Schema Mapping to WaDE_QA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Texas/WaterAllocation/TX_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx)* for specific details.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
TXwr_WS1 | Fresh | Unspecified | Unspecified | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_TXwr_Sites.py
Purpose: generate a list of sites information.

#### Inputs:
- P_TexasWRP.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **TCEQ** info to the *WaDE Site* specific columns.  See *[TX_Allocation Schema Mapping to WaDE_QA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Texas/WaterAllocation/TX_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx)* for specific details.  Items of note are as follows...
    - *Latitude* = **LAT_DD**, will need to convert from EPSG:4269 -to- EPSG:4326. 
    - *Longitude* = **LONG_DD**, will need to convert from EPSG:4269 -to- EPSG:4326.
    - *SiteNativeID* = **TCEQ_ID**.
    - *SiteTypeCV* = **TYPE**.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ------------ | ------------ | ------------
TXwr_S1 | Unspecified | 29.651976 | -96.275803 | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_TXwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_TexasWRP.csv
- WaterRightOwner.csv
- WaterUse.csv
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
- Assign **TCEQ** info to the *WaDE Water Allocations* specific columns.  See *[TX_Allocation Schema Mapping to WaDE_QA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Texas/WaterAllocation/TX_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx)* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationNativeID* = **WR_ID**.
    - *AllocationOwner* = **owners**.
    - *BeneficialUseCategory* = **Uses**.   
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
C1000 | - | ACTIVE | -

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Texas Commission on Environmental Quality (TCEQ)](https://www.tceq.texas.gov/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

TCEQ Staff
- Kathy Alexander <kathy.alexander@tceq.texas.gov>
- John Cody <john-cody.stalsby@tceq.texas.gov>
