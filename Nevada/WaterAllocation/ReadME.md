work in progress

# WSDE Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Nevada Division of Water Resources (NDWR)](http://water.nv.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- **Permit_Owners_5temp.csv**, from the [NDWR Feature Service Site](https://arcgis.shpo.nv.gov/arcgis/rest/services/Water_Resources_Public_Data/WaterRights_POD_POU/FeatureServer).
- **POD AllApps_2.csv**, from the [NDWR Feature Service Site](https://arcgis.shpo.nv.gov/arcgis/rest/services/Water_Resources_Public_Data/WaterRights_POD_POU/FeatureServer).


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NDWR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NV_Allocation Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the NDWR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those six code files are as follows...

- 0_PreProcessNevadaAllocationData.ipynb
- 1_NV_WR_Methods.py
- 2_NV_WR_Variables.py
- 3_NV_WR_Organizations.py
- 4_NV_WR_WaterSources.py
- 5_NV_WR_Sites.py
- 6_NV_WR_AllocationAmounts_fact.py


***
### 0) Code File: 0_PreProcessNevadaAllocationData.ipynb
Purpose: Pre-process the Nevada input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - Permit_Owners_5temp.csv
 - POD AllApps_2.csv

#### Outputs:
 - P_MastersNV.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.
- Sort and merge columns in the Permit_Owners_5temp.csv input by the **app** field.
- Left POD AllApps_2.csv -to- the now sorted Permit_Owners_5temp.csv via **app** field.  Generate single output dataframe *df*.
- Format **prior_dt** field to %m/%d/%Y format.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_MastersNV.csv*.


***
### 1) Code File: 1_NV_WR_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **WSDE** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
NVDWR_Diversion Tracking | Surface Ground | Estimated


***
### 2) Code File: 2_NV_WR_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **WSDE** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
NVDWR_Allocation All | 1 | Year | CFS


***
### 3) Code File: 3_NV_WR_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **WSDE** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
NVDWR | Nevada Division of Water Resources | Brian McMenamy | http://water.nv.gov/index.aspx


***
### 4) Code File: 4_NV_WR_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_MastersNV.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency data info to the *WaDE WaterSources* specific columns.  See *NV_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = **source**, see *0_PreProcessNevadaAllocationData.ipynb* for details.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------
NV_1 | Unspecified | Unspecified | Unspecified | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_NV_WR_Sites.py
Purpose: generate a list of sites where water is diverted (also known as Points Of Diversion, PODs).

#### Inputs:
- P_MastersNV.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to the *WaDE Site* specific columns.  See *NV_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *County* = **county_x**, see *0_PreProcessNevadaAllocationData.ipynb* for details.
    - *Latitude* = **y**.
    - *Longitude* = **x**.
    - *SiteName* = **site_name**, Unknown if blank.
    - *SiteTypeCV* = **source**, see *0_PreProcessNevadaAllocationData.ipynb* for details.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude*, and *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NV_1 | Unknown| 41.9883349988497 | -118.527228999731 | stream

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_NV_WR_AllocationAmounts_fact.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_MastersNV.csv
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
- Assign state agency info to the *WaDE Water Allocations* specific columns.  See *NV_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* = **ProGrant**, 0 if blank.
    - *AllocationLegalStatusCV* = **RightStatus**, Unspecified if blank.
    - *AllocationNativeID* = **ApplicationNumber**.
    - *AllocationPriorityDate* = **PriorityDate**.
    - *BeneficialUseCategory* = **BeneficialUseCategory**.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
Unspecified | 746.67 | Denied | Irrigation

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nevada Division of Water Resources (NDWR)](http://water.nv.gov/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

WSDE Staff
- asdf