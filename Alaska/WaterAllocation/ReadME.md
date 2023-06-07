# Useful Resources
The Status of Alaska Water Export Laws and Water Transfers 
https://www.adfg.alaska.gov/static/lands/planning_management/pdfs/WaterExport.pdf


# AKDNR Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Alaska Department of Natural Resources (AKDNR)](https://dnr.alaska.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- Water Use surface and groundwater data files were made available at the [Alaska Water Use Data System](https://dnr.alaska.gov/akwuds/).
- Priority date data was shared by Jim Vohden (retired now) at Alaska DNR on Feb 16, 2018.  Contact AKDNR for more info.

Two unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - water_data_usage_input
 - Jim Vohden Notes_input

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share AKDNR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *AK_Allocation Schema Mapping to WaDE_QA*.  Six executable code files were used to extract the AKDNR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those six code files are as follows...

- 0_PreProcessAlaskaAllocationData.ipynb
- 1_AKwr_Methods.py
- 2_AKwr_Variables.py
- 3_AKwr_Organizations.py
- 4_AKwr_WaterSources.py
- 5_AKwr_Sites.py
- 6_AKwr_AllocationsAmounts_facts.py


***
### 0) Code File: 0_PreProcessAlaskaAllocationData.ipynb
Purpose: Pre-process the Alaska input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - water_data_usage_input
 - Jim Vohden Notes_input

#### Outputs:
 - P_AlaskaMaster.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes for water data.  Join tables via the **FILE_NUMBER** field.
- Perform the following additional actions on the data...
    - Drop the following fields to eliminate duplicate entries and preserve water right information: **RPT_YEAR**, **RPT_MONTH**, **WATER_SOURCE_USAGE_ID**, **ENTERED_TIME**, **QUANTITY**, **QTY_UNIT**, & **DAILY_PEAK_QTY**.
    - *AllocationPriorityDate* = **PriorityDate**.  Format **PriorityDate** field to %m/%d/%Y format.
    - *WaterSourceTypeCV* == Groundwater.
    - *WaterSourceName* == Unspecified.
    - *Latitude* & *Longitude*= **INTAKE_LOCATION**, needs to be split, ensure float datatype.
    - *AllocationFlow_AF* = **TOTAL_PERMIT_QTY**, convert from gallons -to- AF, ensure float datatype.
    - Generate WaDE specific field *SiteNativeID* from latitude, longitude, SiteType and SiteName fields.  Used to identify unique PODs.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_AlaskaMaster.csv*.


***
### 1) Code File: 1_AKwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **AKDNR** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
AKDNR_Water Use | Surface Ground Water | Metered


***
### 2) Code File: 2_AKwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **AKDNR** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
AKDRN_Water Allocation | 1 | Year | AFY


***
### 3) Code File: 3_AKwr_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **AKDNR** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
AKDNR | Alaska Department of Natural Resources | asdf | asdf


***
### 4) Code File: 4_AKwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_AlaskaMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **AKDNR** info to the *WaDE WaterSources* specific columns.  See *AK_Allocation Schema Mapping to WaDE_QA* for specific details.  Items of note are as follows...
    - *WaterSourceName* = **WITHDRAWAL_WATER_BODY_NAME**, Unspecified if not given.
    - *WaterSourceNativeID* = **WATER_SOURCE_ID**, Unspecified if not given.
    - *WaterSourceTypeCV* = **WATER_SOURCE_TYPE**, Unspecified if not given.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
AKwr_WS1 | Fresh | Well 13 | 1422 | well

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_AKwr_Sites.py
Purpose: generate a list of sites information.

#### Inputs:
- P_AlaskaMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **AKDNR** info to the *WaDE Site* specific columns.  See *AK_Allocation Schema Mapping to WaDE_QA* for specific details.  Items of note are as follows...
    - *HUC8* = **'HYDROLOGIC_UNIT_CODE**.
    - *Latitude* = *wswc_lat*, see *0_PreProcessAlaskaAllocationData.ipynb* for specifics.
    - *Longitude* = *wswc_long*, see *0_PreProcessAlaskaAllocationData.ipynb* for specifics.
    - *SiteName* = **INTAKE_NAME**, Unspecified if not given.
    - *SiteNativeID* = *wswc_SiteNativeID*, see *0_PreProcessAlaskaAllocationData.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ------------ | ------------ | ------------
AKwr_S1 | Unspecified | 61.1632126746014 | -149.818544983864 | Well 13

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_AKwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_AlaskaMaster.csv
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
- Assign **AKDNR** info to the *WaDE Water Allocations* specific columns.  See *AK_Allocation Schema Mapping to WaDE_QA* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationLegalStatusCV = **FILE_TYPE**
    - *AllocationNativeID* = **FILE_NUMBER**.
    - *AllocationOwner* =  **CUSTOMER_NAME**.
    - *AllocationPriorityDate* = **PriorityDate**.
    - *AllocationFlow_AF* = *wswc_QTY*, see *0_PreProcessAlaskaAllocationData.ipynb* for specifics.
    - *BeneficialUseCategory* = **STATE_USE**.   
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_AF | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
1145 | 186.6908073 | ADL | Water Supply

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Alaska Department of Natural Resources (AKDNR)](https://dnr.alaska.gov/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

Alaska DNR Staff
- asdf
