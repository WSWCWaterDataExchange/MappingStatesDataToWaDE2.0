# NDSWC Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [North Dakota State Water Commission (NDSWC)](https://www.swc.nd.gov/theswc/water_appropriations.html), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- Point of diversion (POD) data was obtained from NDSWC Maps and GIS Data Hub at: https://mapservice.swc.nd.gov/.  Downloaded “Water permits” layer displayed by “Use type”. Open the shapefile in QGIS and export layer to csv file: Permits.csv, which was used as the primary input for data.

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NDSWC's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *ND_Allocation Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the NDSWC's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(AllocationAmounts_facts)* is depended on the previous files.  Those six code files are as follows...

- 0_PreProcessNorthDakotaAllocationData.ipynb
- 1_NDwr_Methods.py
- 2_NDwr_Variables.py
- 3_NDwr_Organizations.pys
- 4_NDwr_WaterSources.py
- 5_NDwr_Sites.py
- 6_NDwr_AllocationsAmounts_facts.py


***
### 0) Code File: 0_PreProcessNorthDakotaAllocationData.ipynb
Purpose: Pre-process the state agency input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - Permits.csv

#### Outputs:
 - P_NorthDakotaMaster.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.
- Generate WaDE specific field *WaterSourceTypeC* from NDSWC **SOURCE_TYPE** field (see pre-process code for specific dictionary used).
- Format **priority_d**, **date_issue**, &  **date_cance** field to %m/%d/%Y format.
- Format **source_nam**, **source**, **permit_hol** to title text format.
- Remove excess white space in **source_nam**, **source**, **permit_hol**, **county**, **aquifer**, **pod**, **status**, **use_type**, & **permit_num**.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_NorthDakotaMaster.csv*.


***
### 1) Code File: 1_NDwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **NDSWC** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
NDSWC_Water Rights | Surface Ground | Adjudicated


***
### 2) Code File: 2_NDwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **NDSWC** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
NDSWC_Allocation All | 1 | Year | CFS


***
### 3) Code File: 3_NDwr_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **NDSWC** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
NDSWC | North Dakota State Water Commission | Chris Bader | https://swc.nd.gov/theswc/water_appropriations.html


***
### 4) Code File: 4_NDwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_NorthDakotaMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **NDSWC** info to the *WaDE WaterSources* specific columns.  See *ND_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = **source**, Unknown if not given.
    - *WaterSourceTypeCV* = generated list of sources from **SOURCE_TYPE**, see *0_PreProcessNorthDakotaAllocationData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NDwr_WS1 | Fresh | Unknown | Unspecified | Ground Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_NDwr_Sites.py
Purpose: generate a list of sites information.

#### Inputs:
- P_NorthDakotaMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **NDSWC** info to the *WaDE Site* specific columns.  See *ND_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *County* = **county**.
    - *Latitude* = **latitude**.
    - *Longitude* = **longitude**.
    - *SiteName* = **aquifer**, Unspecified if not given.
    - *SiteNativeID* = **pod**.
    - *SiteTypeCV* = **source**, Unknown if not given.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NDwr_S1 | Unspecified | 46.1113 | -99.78988 | Ground Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_NDwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_NorthDakotaMaster.csv
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
- Assign **NDSWC** info to the *WaDE Water Allocations* specific columns.  See *ND_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationApplicationDate* = **date_issue**.
    0 *AllocationExpirationDate* = **date_cance**.
    - *AllocationFlow_CFS* = **req_rate**.
    - *AllocationLegalStatusCV* = **status**.
    - *AllocationNativeID* = **permit_num**.
    - *AllocationOwner* = **permit_hol**.
    - *AllocationPriorityDate* = **priority_d**.
    - *AllocationTimeframeEnd* = **period_end**.
    - *AllocationTimeframeStart* = **period_sta**.
    - *AllocationVolume_AF* = **req_acft**.
    - *BeneficialUseCategory* = **use_type**.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
1000 | 314.1 | Perfected | Industrial

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [North Dakota State Water Commission (NDSWC)](https://www.swc.nd.gov/theswc/water_appropriations.html).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

NDSWC Staff
- Chris Bader <cbader@nd.gov>