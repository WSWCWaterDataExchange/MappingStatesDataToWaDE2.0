# NVDWR Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Nevada Division of Water Resources (NVDWR)](http://water.nv.gov/index.aspx), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- **Point of diversion (POD)** data was obtained from a [NVDWR arcgis server](https://arcgis.shpo.nv.gov/arcgis/rest/services/Water_Resources_Public_Data/WaterRights_POD_POU/FeatureServer).
- **Place of Use (POU)** data was obtained from a [NVDWR arcgis server](https://arcgis.shpo.nv.gov/arcgis/rest/services/Water_Resources_Public_Data/WaterRights_POD_POU/FeatureServer).
- **Permit** data related to water rights was obtained from a [NVDWR arcgis server](https://arcgis.shpo.nv.gov/arcgis/rest/services/Water_Resources_Public_Data/WaterRights_POD_POU/FeatureServer).

Three unique files were created as input.  Input files used are as follows...
 - POD AllApps_2_input.csv
 - PoU AllApps_3_input.cs
 - Permit_Owners_5temp.csv

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NVDWR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NV_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *NV_POU_Allocation Schema Mapping to WaDE_QA.xlsx*.  Seven executable code files were used to extract the NVDWR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (preprocess) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining six code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those seven code files are as follows...

- 0_PreProcessNevadaAllocationData.ipynb
- 1_NVwr_Methods.py
- 2_NVwr_Variables.py
- 3_NVwr_Organizations.py
- 4_NVwr_WaterSources.py
- 5_NVwr_Sites.py
- 6_NVwr_AllocationsAmounts_facts.py
- 7_NVwr_PODSiteToPOUSiteRelationships.py


***
### 0) Code File: 0_PreProcessNevadaAllocationData.ipynb
Purpose: preprocess the Montana input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - POD AllApps_2_input.csv
 - PoU AllApps_3_input.csv
 - Permit_Owners_5temp.csv

#### Outputs:
 - P_MastersNV.csv

#### Operation and Steps:
- Read in the input files.  Create temporary POD and POU dataframes.  POD and POU data share similar fields.
- For POD AllApps_2_input.csv, set WaDE field *PODorPOUSite* = POD.
- For PoU AllApps_3_input.csv, set WaDE field *PODorPOUSite* = POU.
- Concatenate temporary POD & POU dataframes together into single long output dataframe.
- Left-merge Permit_Owners_5temp.csv via **app** field to long concatenated dataframe..  Drop duplicates.
- Generate WaDE specific field *WaterSourceTypeC* from NVDWR **source** field (see preprocess code for specific dictionary used).
- Generate WaDE specific field *SiteName* from NVDWR **site_name** field (see preprocess code for specific dictionary used).
- Generate WaDE specific field *SiteTypeCV* from NVDWR **source** field (see preprocess code for specific dictionary used).
- Generate WaDE specific field *SiteNativeID* from WaDE *Latitude*, *Longitude*, *SiteTypeCV* & *SiteName* fields.  Used to identify unique sites.
- Generate WaDE specific field *WaterSourceNativeID* from WaDE *WaterSourceName* & *WaterSourceTypeCV* fields.  Used to identify unique sources of water.
- Format **prior_dt** field to %m/%d/%Y format.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_MastersNV.csv*.


***
### 1) Code File: 1_NVwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **NVDWR** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
NVDWR_Diversion Tracking | Surface Ground | Estimated


***
### 2) Code File: 2_NVwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **NVDWR** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
NVDWR_Allocation | 1 | Year | CFS


***
### 3) Code File: 3_MTwr_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **NVDWR** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
NVDWR | Nevada Division of Water Resources | Brian McMenamy | http://water.nv.gov/index.aspx


***
### 4) Code File: 4_NVwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_MastersNV.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **NVDWR** info to the *WaDE WaterSources* specific columns.  See *NV_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *NV_POU_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = generated list of sources from **SOURCE_TYPE**, see *0_PreProcessNevadaAllocationData.ipynb* for specifics.
    - *WaterSourceNativeID* = see *0_PreProcessNevadaAllocationData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NVwr_WS1 | Unspecified | Unspecified | WaDENV_WS1 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_NVwr_Sites.py
Purpose: generate a list of sites information.

#### Inputs:
- P_MastersNV.csv
- watersources.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **NVDWR** info to the *WaDE Site* specific columns.  See *NV_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *NV_POU_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - *County* = **county_x**.
    - *Latitude* = **x**.
    - *Longitude* = **y**.
    - *SiteName* = *in_SiteName*, see *0_PreProcessNevadaAllocationData.ipynb* for specifics.
    - *SiteNativeID* = *in_SiteNativeID*, see *0_PreProcessNevadaAllocationData.ipynb* for specifics.
    - *SiteTypeCV* = *in_SiteTypeCV*, see *0_PreProcessNevadaAllocationData.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
NVwr_S1 | NVwr_WS1 | Digitized | 41.9883349988497 | -118.527228999731 | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_NVwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_MastersNV.csv
- methods.csv
- variables.csv
- organizations.csv
- sites.csv

#### Outputs:
- waterallocations.csv
- waterallocations_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign **NVDWR** info to the *WaDE Water Allocations* specific columns.  See *NV_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *NV_POU_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* = **duty_balance**.
    - *AllocationLegalStatusCV* = **app_status**.
    - *AllocationNativeID* = **app**.
    - *AllocationOwner* = **owner_name**.
    - *AllocationPriorityDate* = **prior_dt**.
    - *BeneficialUseCategory* = **mou**.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
1 | 0 | Canceled | Power

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- SiteUUID
- AllocationPriorityDate
- BeneficialUseCategory
- AllocationAmount or AllocationMaximum
- DataPublicationDate


***
### 7) Code File: 7_NVwr_PODSiteToPOUSiteRelationships.py
Purpose: generate linking element between POD and POU sites that share the same water right.
Note: podsitetopousiterelationships.csv output only needed if both POD and POU data is present, otherwise produces empty file.

#### Inputs:
- sites.csv
- waterallocations.csv

#### Outputs:
- podsitetopousiterelationships.csv

#### Operation and Steps:
- Read the sites.csv & waterallocations.csv input files.
- Create three temporary dataframes: one for waterallocations, & two for site info that will store POD and POU data separately.
- For the temporary POD dataframe...
    - Read in site.csv data from sites.csv with a *PODSiteUUID* field = POD only.
    - Create *PODSiteUUID* field = *SiteUUID*.
- For the temporary POU dataframe
    - Read in site.csv data from sites.csv with a *PODSiteUUID* field = POU only.
    - Create *POUSiteUUID* field = *SiteUUID*.
- For the temporary waterallocations dataframe, explode *SiteUUID* field to create unique rows.
- Left-merge POD & POU dataframes to the waterallocations dataframe via *SiteUUID* field.
- Consolidate waterallocations dataframe by grouping entries by *AllocationNativeID* filed.
- Explode the consolidated waterallocations dataframe again using the *PODSiteUUID* field, and again for the *POUSiteUUID* field to create unique rows.
- Perform error check on waterallocations dataframe (check for NaN values)
- If waterallocations is not empty, export output dataframe *podsitetopousiterelationships.csv*.


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nevada Division of Water Resources (NVDWR)]( http://water.nv.gov/index.aspx).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

Nevada DNR Staff
- Brian McMenamy (IT Professional) <bmcmenamy@water.nv.gov>
- Levi Kryder (Chief Hydrology Section) <lkryder@water.nv.gov>
- Caitlan Jellema (Water Use Specialist) <cjellema@water.nv.gov>
- Stephanie Snider (GIS Analyst)
