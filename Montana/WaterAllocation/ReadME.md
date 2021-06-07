# MDNRC Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Montana Department of Natural Resources and Conservation (MDNRC)](https://opendata-mtdnrc.hub.arcgis.com/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- Point of diversion (POD) data was obtained from MDNRC Maps and GIS Data Hub at: https://opendata-mtdnrc.hub.arcgis.com/datasets/wade-pods
- Point of use (PoU) data was obtained from MDNRC Maps and GIS Data Hub at: https://opendata-mtdnrc.hub.arcgis.com/datasets/wade-pous

Two unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - WaDE_PODs_input.csv
 - WaDE_PoUs_input.csv (have not incorporated yet)

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share MDNRC's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *MT_Allocation Schema Mapping to WaDE_QA.xlsx*.  Seven executable code files were used to extract the MDNRC's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (preprocess) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining six code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those seven code files are as follows...

- 0_PreProcessMontanaWaterRightData.ipynb
- 1_MTwr_Methods.py
- 2_MTwr_Variables.py
- 3_MTwr_Organizations.pys
- 4_MTwr_WaterSources.py
- 5_MTwr_Sites.py
- 6_MTwr_AllocationsAmounts_fac`ts.py
- 7_MTwr_PODSiteToPOUSiteRelationships.py


***
### 0) Code File: 0_PreProcessMontanaWaterRightData.ipynb
Purpose: preprocess the Montana input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - WaDE_PODs_input.csv

#### Outputs:
 - P_MontanaMaster.csv

#### Operation and Steps:
- Read in the input files.  Goal will be to create separate POD and POU cenetric dataframes, then join together for single long output dataframe.
- For POD data...
    - Generate WaDE specific field *WaterSourceTypeC* from MDNRC **SOURCE_TYPE** field (see preprocess code for specific dictionary used).
    - Format **ENF_PRIORITY_DATE** field to %m/%d/%Y format.
    - Generate WaDE specific field *MethodTypeCV* from MDNRC **ENF_PRIORITY_DATE** field (see preprocess code for specific dictionary used).  Water rights that were established prior to July 1,1973 are administered by the Adjudication Bureau. Water rights that were established from July 1, 1973 through the present are administered by the New Appropriations Program.
    - Generate WaDE Specific Field *TimeframeStart* from MDNRC **PER_DIV_BGN_DT** field (see preprocess code for specific dictionary used).
    - Generate WaDE Specific Field *TimeframeEnd* from MDNRC **PER_DIV_END_DT** field (see preprocess code for specific dictionary used).
    - Create WaDE POD centric temporary dataframe.  Extract POU relevant data (see preprocessing code).
- For POU data...
    - Generate WaDE specific field *WaterSourceTypeC* from MDNRC **SRCTYPE** field (see preprocess code for specific dictionary used).
    - Format **ENF_PRIORITY_DATE** field to %m/%d/%Y format.
    - Generate WaDE specific field *MethodTypeCV* from MDNRC **ENF_PRIORI** field (see preprocess code for specific dictionary used).  Water rights that were established prior to July 1,1973 are administered by the Adjudication Bureau. Water rights that were established from July 1, 1973 through the present are administered by the New Appropriations Program.
    - Generate WaDE Specific Field *TimeframeStart* from MDNRC **PER_USE_BG** field (see preprocess code for specific dictionary used).
    - Generate WaDE Specific Field *TimeframeEnd* from MDNRC **PER_USE_EN** field (see preprocess code for specific dictionary used).
    - Create WaDE POU centric temporary dataframe.  Extract POU relevant data (see preprocessing code).
    - Generate WaDE specific field *SiteType* from WaDE *Latitude*, *Longitude*, *SiteTypeCV* & *SiteName* fields.  Used to identify unique sites.
- Concatenate temporary POD & POU dataframes together into single long output dataframe.
- Generate WaDE specific field *WaterSourceNativeID* from WaDE *WaterSourceName* & *WaterSourceTypeCV* fields.  Used to identify unique sources of water.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_MontanaMaster.csv*.


***
### 1) Code File: 1_MTwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **MDNRC** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
MT_Water Allocation Adj | Surface Ground Water | Adjudication


***
### 2) Code File: 2_MTwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **MDNRC** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
MT_Consumptive Use | 1 | Year | CFS


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
- Assign **MDNRC** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
MDNRC | Montana Dept. of Water Rights | Chris Kuntz | http://dnrc.mt.gov/


***
### 4) Code File: 4_MTwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_MontanaMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **MDNRC** info to the *WaDE WaterSources* specific columns.  See *MT_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = **SOURCE_NAME**, Unspecified if not given.
    - *WaterSourceTypeCV* = generated list of sources from **SOURCE_TYPE**, see *0_PreProcessMontanaWaterRightData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
MTwr_WS7 | Fresh | FROZEN HORSE CREEK | Unspecified | SURFACE

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_MTwr_Sites.py
Purpose: generate a list of sites information.

#### Inputs:
- P_MontanaMaster.csv
- watersources.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **MDNRC** info to the *WaDE Site* specific columns.  See *MT_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *County* = **LLDS_COUNTY_NAME**.
    - *HUC12* = **HUC_12**.
    - *Latitude* = **X**.
    - *Longitude* = **Y**.
    - *SiteName* = **DITCH_NAME**, Unspecified if not given.
    - *SiteNativeID* = **PODV_ID_SEQ**.
    - *SiteTypeCV* = **MEANS_OF_DIV**, Unspecified if not given.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
MTwr_S1 | MTwr_WS1 | Unknown | 45.10645361 | -104.1225607 | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_MTwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_MontanaMaster.csv
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
- Assign **MDNRC** info to the *WaDE Water Allocations* specific columns.  See *MT_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* = **FLW_RT_CFS**.
    - *AllocationLegalStatusCV* = **WR_STATUS**.
    - *AllocationNativeID* = **WR_NUMBER**.
    - *AllocationOwner* = **ALL_OWNERS**.
    - *AllocationPriorityDate* = **ENF_PRIORITY_DATE**.
    - *AllocationTimeframeEnd* = **PER_DIV_END_DT**.
    - *AllocationTimeframeStart* = **PER_DIV_BGN_DT**.
    - *AllocationTypeCV* = **WR_TYPE**.
    - *AllocationVolume_AF* = **VOLUME**.
    - *BeneficialUseCategory* = **PURPOSES**.
    - *DataPublicationDOI* = **ABST_LINK**.
    - *ExemptOfVolumeFlowPriority* = **WR_TYPE**, see *0_PreProcessMontanaWaterRightData.ipynb* for details.
    - *IrrigatedAcreage* = **MAX_ACRES**.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
38H 126342 00 | 0.01 | ACTIVE | STOCK

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
### 7) Code File: 7_MTwr_PODSiteToPOUSiteRelationships.py
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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Montana Department of Natural Resources and Conservation (MDNRC)](https://opendata-mtdnrc.hub.arcgis.com/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

Montana DNRC Staff
- Chris Kuntz <CKuntz@mt.gov>
- David Coey <dcoey@mt.gov>
- Karen Coleman <Karen.Coleman@mt.gov>
- Matthew Norberg <MNorberg@mt.gov>