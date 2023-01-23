# SDDENR Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [South Dakota Department of Environment and Natural Resources (SDDENR)](https://denr.sd.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

- Point of diversion (POD) surface and groundwater data files were made temporary available to the WSWC staff by the SDDENR via email correspondence and shared through Google Drive.  Links no longer available, contact SDDENR for further instructions.

Two unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - waterights_input

## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- South Dakota Allocation Data: https://drive.google.com/drive/folders/1AQH7axW_PjUZKd7JQqOiBuE3fMBG3Q7a?usp=sharing

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share SDDENR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *WY_Allocation Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the SDDENR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those six code files are as follows...

- 0_PreProcessSouthDakotaAllocationData.ipynb
- 1_SDwr_Methods.py
- 2_SDwr_Variables.py
- 3_SDwr_Organizations.py
- 4_SDwr_WaterSources.py
- 5_SDwr_Sites.py
- 6_SDwr_AllocationsAmounts_facts.py


***
### 0) Code File: 0_PreProcessSouthDakotaAllocationData.ipynb
Purpose: Pre-process the South Dakota input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - waterights_input

#### Outputs:
 - P_SouthDakotaMaster.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes for groundwater and surface water data.  Goal will be to create two separate clean tables and concatenate to single output table.
- Perform the following additional actions on the groundwater data...
    - *AllocationPriorityDate* = **PRIORDATE**.  Format **PRIORDATE** field to %m/%d/%Y format.
    - *AllocationOwner* =  **FIRST_NAME**, and **LAST_NAME** fields, see pre-process code for specifics.
    - *BeneficialUseCategory* = **USE_TYPE1**, **USE_TYPE2**, **USE_TYPE4** and **USE_TYPE5**, ensure string datatype.  Concatenate together. Use provided SDDENR terminology code and use field, see see pre-process code for specifics.
    - *SiteTypeCV* = **SOURCE**, ensure string datatype.  Use provided SDDENR terminology code and use field, see see pre-process code for specifics.
    - *AllocationTypeCV* = **STATUS**, ensure string datatype.  Use provided SDDENR terminology code and use field, see see pre-process code for specifics.
- Generate WaDE specific field *SiteNativeID* from latitude, longitude, SiteType and SiteName fields.  Used to identify unique PODs.
- Generate WaDE specific field *WaterSourceNativeID* from Watersource Name field.  Used to identify unique sources of water.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_SouthDakotaMaster.csv*.


***
### 1) Code File: 1_SDwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **SDDENR** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
SDwr_M1| Surface Ground Water | Water Use


***
### 2) Code File: 2_SDwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **SDDENR** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
SDwr_V1 | 1 | Year | CFS


***
### 3) Code File: 3_SDwr_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **SDDENR** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
SDwr_O1 | South Dakota Water Development Office | Ron Duvall | https://denr.sd.gov/


***
### 4) Code File: 4_SDwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_SouthDakotaMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **SDDENR** info to the *WaDE WaterSources* specific columns.  See *WY_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = *in_WaterSourceName*, Unspecified if not given, see *0_PreProcessSouthDakotaAllocationData.ipynb* for specifics.
    - *WaterSourceNativeID* = *in_WaterSourceNativeID*, see *0_PreProcessSouthDakotaAllocationData.ipynb* for specifics.
    - *WaterSourceTypeCV* = Unspecified.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
SDwr_WS1 | Fresh | JR | WaDEWY_WS1 | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_SDwr_Sites.py
Purpose: generate a list of sites information.

#### Inputs:
- P_SouthDakotaMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **SDDENR** info to the *WaDE Site* specific columns.  See *WY_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *HUC8* = **HYDROUNIT1**.
    - *Latitude* = **LATITUDE**.
    - *Longitude* = **LONGITUDE**.
    - *SiteName* = **FacilityName**, Unspecified if not given.
    - *SiteNativeID* = **DIVERSION1**, see *0_PreProcessSouthDakotaAllocationData.ipynb* for specifics.
    - *SiteTypeCV* = **Facility_type**, see *0_PreProcessSouthDakotaAllocationData.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ------------ | ------------ | ------------
SDwr_S1 | Unspecified | 43.71384 | -97.6078 | WOLF CREEK

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_SDwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_SouthDakotaMaster.csv
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
- Assign **SDDENR** info to the *WaDE Water Allocations* specific columns.  See *WY_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationLegalStatusCV* = **STATUS**
    - *AllocationFlow_CFS* = **LIC_CFS**.
    - *AllocationLegalStatusCV* = *input_Status*, see *0_PreProcessSouthDakotaAllocationData.ipynb* for specifics.
    - *AllocationNativeID* = **PERMIT_NO**.
    - *AllocationOwner* =  *WaDEOwner*, see *0_PreProcessSouthDakotaAllocationData.ipynb* for specifics.
    - *AllocationPriorityDate* = **PRIORDATE**.
    - *AllocationTypeCV* = "Unspecified.
    - *BeneficialUseCategory* = *input_Benuse*, see *0_PreProcessSouthDakotaAllocationData.ipynb* for specifics.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
010-1 | 0 | Cancelled | Irrigation

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [South Dakota Department of Environment and Natural Resources (SDDENR)](https://denr.sd.gov/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

SDDENR Staff
- Ron Duvall <Ron.Duvall@state.sd.us>
