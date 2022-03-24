# WWDO Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Wyoming Water Development Office (WWDO)](https://wwdc.state.wy.us/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- Point of diversion (POD) surface and groundwater data files were made temporary available to the WSWC staff by the WWDO via email correspondence and shared through Google Drive.  Links no longer available, contact WWDO for further instructions.
- Place of Use (POU) data files were made temporary available to the WSWC staff by the WWDO via email correspondence and shared through Google Drive.  Links no longer available, contact WWDO for further instructions.

Two unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - POD_SW_DepthI_FC.csv
 - POD_GW_DepthI_FC.csv
 - POU.csv

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share WWDO's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *WY_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *WY_POU_Allocation Schema Mapping to WaDE_QA.xlsx* files.  Seven executable code files were used to extract the WWDO's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining six code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those Seven code files are as follows...

- 0_PreProcessWyomingAllocationData.ipynb
- 1_WYwr_Methods.py
- 2_WYwr_Variables.py
- 3_WYwr_Organizations.py
- 4_WYwr_WaterSources.py
- 5_WYwr_Sites.py
- 6_WYwr_AllocationsAmounts_facts.py
- 7_WYwr_PODSiteToPOUSiteRelationships.py


***
### 0) Code File: 0_PreProcessWyomingAllocationData.ipynb
Purpose: Pre-process the Wyoming input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- POD_SW_DepthI_FC.csv
- POD_GW_DepthI_FC.csv
- POU.csv

#### Outputs:
 - P_WyomingMaster.csv

#### Operation and Steps:
- Read in the input files.  Goal will be to create separate POD and POU centric dataframes, then join together for single long output dataframe.
- For POD data...
    - Perform the following additional actions on the groundwater data...
        - *WaterSourceTypeCV* == Groundwater.
        - *WaterSourceName* == Unspecified.
        - *Latitude* = **Latitude_Double**, ensure float datatype.
        - *Longitude* = **Longitude_Double**, ensure float datatype.
        - *SiteName* = **FacilityName**, ensure string datatype.
        - *SiteTypeCV* = **Facility_type**, ensure string datatype.
        - *AllocationFlow_CFS* = **Total_Flow_CFS___Appropriation_GPM_**, ensure float datatype.
        - *AllocationNativeID* = **WR_Number**, ensure string datatype.
        - *AllocationOwner* =  **Company**, **FirstName**, and **LastName** fields, see pre-process code for specifics.
        - *AllocationPriorityDate* = **PriorityDate**.  Format **PriorityDate** field to %m/%d/%Y format.
        - *AllocationTypeCV* = **SummaryWRStatus**, ensure string datatype.
        - *BeneficialUseCategory* = **Uses**, ensure string datatype.  Use provided WWDO terminology code and **Uses** field, see see pre-process code for specifics.  In addition, include all records that have a "Z" in the **Survey_Type_Survey_Number_Survey_Suffix** for "Wild and Scenic River" benefical uses.
    - Perform the following additional actions on the surface water data...
        - *WaterSourceTypeCV* == Surface Water.
        - *WaterSourceName* == **Stream_Source**, ensure string datatype.
        - *Latitude* = **Latitude_Double**, ensure float datatype.
        - *Longitude* = **Longitude_Double**, ensure float datatype.
        - *SiteName* = **FacilityName**, ensure string datatype.
        - *SiteTypeCV* = **Facility_type**, ensure string datatype.
        - *AllocationFlow_CFS* = **Total_Flow_CFS___Appropriation_GPM_**, ensure float datatype.
        - *AllocationNativeID* = **WR_Number**, ensure string datatype.
        - *AllocationOwner* =  **Company**, **FirstName**, and **LastName** fields, see pre-process code for specifics.
        - *AllocationPriorityDate* = **PriorityDate**.  Format **PriorityDate** field to %m/%d/%Y format.
        - *AllocationTypeCV* = **SummaryWRStatus**, ensure string datatype.
        - *BeneficialUseCategory* = **Uses**, ensure string datatype.  Use provided WWDO terminology code and **Uses** field, see see pre-process code for specifics.    In addition, include all records that have a "Z" in the **Survey_Type_Survey_Number_Survey_Suffix** for "Wild and Scenic River" benefical uses.
    - Concatenate groundwater and surface water dataframes together to create single long output table.
    - Create WaDE POD centric temporary dataframe.  Extract POD relevant data (see preprocessing code).
- For POU data...
    - *AllocationPriorityDate* = **PriorityDate**.  Format **PriorityDate** field to %m/%d/%Y format.
    - *BeneficialUseCategory* = **Uses**, ensure string datatype.  Use provided WWDO terminology code and **Uses** field, see see pre-process code for specifics.  In addition, include all records that have a "Z" in the **Survey** for "Wild and Scenic River" benefical uses.
    - Create WaDE POU centric temporary dataframe.  Extract POU relevant data (see preprocessing code).
- Concatenate temporary POD & POU dataframes together into single long output dataframe.
- Generate WaDE specific field *SiteNativeID* from *Latitude*, *Longitude*, *SiteType* and *SiteName* fields.  Used to identify unique sites.
- Generate WaDE specific field *WaterSourceNativeID* from *WaterSourceName* & *WaterSourceTypeCV* fields.  Used to identify unique sources of water.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_WyomingMaster.csv*.


***
### 1) Code File: 1_WYwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **WWDO** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
WYwr_M1 | Surface Ground Water | Adjudicated


***
### 2) Code File: 2_WYwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **WWDO** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
WYwr_V1 | 1 | Year | CFS


***
### 3) Code File: 3_WYwr_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **WWDO** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
WYwr_O1 | Wyoming Water Development Office | Mabel Jones | https://wwdc.state.wy.us/


***
### 4) Code File: 4_WYwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_WyomingMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **WWDO** info to the *WaDE WaterSources* specific columns.  See *WY_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *WY_POU_Allocation Schema Mapping to WaDE_QA.xlsx* files for specific details.  Items of note are as follows...
    - *WaterSourceName* = *in_WaterSourceName*, Unspecified if not given, see *0_PreProcessWyomingAllocationData.ipynb* for specifics.
    - *WaterSourceNativeID* = *in_WaterSourceNativeID*, see *0_PreProcessWyomingAllocationData.ipynb* for specifics.
    - *WaterSourceTypeCV* = *in_WaterSourceTypeCV*, see *0_PreProcessWyomingAllocationData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
WYwr_WS2 | Fresh | Buffalo Creek | WaDEWY_WS2 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_WYwr_Sites.py
Purpose: generate a list of sites information.

#### Inputs:
- P_WyomingMaster.csv
- watersources.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **WWDO** info to the *WaDE Site* specific columns.  See *WY_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *WY_POU_Allocation Schema Mapping to WaDE_QA.xlsx* files for specific details.  Items of note are as follows...
    - *Latitude* = **Latitude_Double**.
    - *Longitude* = **Longitude_Double**.
    - *SiteName* = **FacilityName**, Unspecified if not given.
    - *SiteNativeID* = *in_SiteNativeID*, see *0_PreProcessWyomingAllocationData.ipynb* for specifics.
    - *SiteTypeCV* = **Facility_type**, Unspecified if not given.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
WYwr_S1 | WYwr_WS1 | Unspecified | 42.9129 | -104.46127 | O W WELL #1

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_WYwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_WyomingMaster.csv
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
- Assign **WWDO** info to the *WaDE Water Allocations* specific columns.  See *WY_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *WY_POU_Allocation Schema Mapping to WaDE_QA.xlsx* files for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* = **Total_Flow_CFS___Appropriation_GPM_**.
    - *AllocationNativeID* = **WR_Number**.
    - *AllocationOwner* =  **Company**, **FirstName**, and **LastName** fields, see pre-process code for specifics.
    - *AllocationPriorityDate* = **PriorityDate**.
    - *AllocationTypeCV* = **SummaryWRStatus**.
    - *BeneficialUseCategory* = **Uses**.   
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
A1612.0Q | 130.18 | ACTIVE | Stock and/or Domestic

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
### 7) Code File: 7_UTwr_PODSiteToPOUSiteRelationships.py
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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Wyoming Water Development Office (WWDO)](https://wwdc.state.wy.us/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

Wyoming DNRC Staff
- Mabel Jones <mabel.jones1@wyo.gov>
