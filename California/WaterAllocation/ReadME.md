# CSWRCB Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [California State Water Resources Control Board (CSWRCB)](https://www.waterboards.ca.gov), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- **POD_Attributes** water right metadata & **Points_of_Diversion_20210701** site information, both available from the [eWRIMS POD Download](https://waterrightsmaps.waterboards.ca.gov/viewer/Resources/Images/eWRIMS/download.htm).
- **EWRIMS MASTER FLAT FILE DATA DICTIONARY DRAFT 1-17-20** obtained from personal contact with the CSWRCB and used by the WaDE team for additional metadata.


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CSWRCB's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see **CA_Allocation Schema Mapping to WaDE_QA.xlsx**.  Six executable code files were used to extract the CSWRCB's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those six code files are as follows...

- 0_PreProcessCaliforniaAllocationData.ipynb
- 1_CAwr_Methods.py
- 2_CAwr_Variables.py
- 3_CAwr_Organizations.py
- 4_CAwr_WaterSources.py
- 5_CAwr_Sites.py
- 6_CAwr_AllocationsAmounts_facts.py
- 7_CAwr_PODSiteToPOUSiteRelationships.py


***
### 0) Code File: 0_PreProcessCaliforniaAllocationData.ipynb
Purpose: Pre-process the state agency's input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - POD_Attributes.csv
 - Points_of_Diversion_20210701.csv
 - EWRIMS MASTER FLAT FILE DATA DICTIONARY DRAFT 1-17-20.xlsx

#### Outputs:
 - P_CaliforniaMaster.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.  Merge POD_Attributes & Points_of_Diversion_20210701 dataframes together using left join via **CORE_POD_ID** & **POD_ID** fields, and the EWRIMS MASTER FLAT FILE DATA DICTIONARY DRAFT 1-17-20 dataframe **WR_WATER_RIGHT_ID** field.
- Create WaDE *pridority date* field using **PRIORITY_DATE** (or **APPLICATION_ACCEPTANCE_DATE** field if missing).  Format to %m/%d/%Y.
- Create WaDE *TimeframeStart* field using **DIRECT_DIV_SEASON_START** field.  Format to %m/%d.
- Create WaDE *in_AllocationTimeframeEnd* field using **DIRECT_DIV_SEASON_END** field.  Format to %m/%d.
- Generate WaDE *Owner* field by combining **FIRST_NAME** & **LAST_NAME** fields together, Unpsecified if both blank.
- Create custom WaDE ID for water sources using **SOURCE_NAME** field.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_CaliforniaMaster.csv*.


***
### 1) Code File: 1_CAwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign state agency info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
CSWRCB_Water Rights | Surface water or subsurface water | Adjudicated


***
### 2) Code File: 2_CAwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign state agency info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
CSWRCB_Allocation | 1 | Year | AFY |


***
### 3) Code File: 3_CAwr_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign state agency info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
CSWRCB | California State Water Resources Control Board | Greg Gearheart | https://www.waterboards.ca.gov/


***
### 4) Code File: 4_CAwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_CaliforniaMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency data info to the *WaDE WaterSources* specific columns.  See **CA_Allocation Schema Mapping to WaDE_QA.xlsx** for specific details.  Items of note are as follows...
    - *WaterSourceName* =  **SOURCE_NAME**, Unspecfield if blank.
    - *WaterSourceNativeID* = custom WaDE ID field, see *0_PreProcessCaliforniaAllocationData* for details.
    - *WaterSourceTypeCV* = Surface Water.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------
CAwr_WS1 | Fresh | HOCKER GULCH | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_CAwr_Sites.py
Purpose: generate a list of sites where water is diverted (also known as Points Of Diversion, PODs).

#### Inputs:
- P_CaliforniaMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to the *WaDE Site* specific columns.  See **CA_Allocation Schema Mapping to WaDE_QA.xlsx** for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersource.csv input file. See code for specific implementation of extraction.
    - *CoordinateMethodCV* = **LOCATION_METHOD**.
    - *County* = **COUNTY**.
    - *HUC12* = **HUC_12**.
    - *HU8* = **HUC_8**.
    - *Latitude* = **LATITUDE**.
    - *Longitude* = **LONGITUDE**.
    - *SiteName* = **DIVERSION_SITE_NAME**, Unspecified if blank.
    - *SiteNativeID* = **POD_ID**, Unspecified if blank.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteTypeCV*, *Longitude*, and *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
CAwr_S1 | CAwr_WS1 | Unspecified | 40.73949452 | -123.06921044 | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_CAwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_CaliforniaMaster.csv
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
- Assign state agency info to the *WaDE Water Allocations* specific columns.  See **CA_Allocation Schema Mapping to WaDE_QA.xlsx** for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationLegalStatusCV* = **WR_STATUS**.
    - *AllocationNativeID* = **WR_WATER_RIGHT_ID**.
    - *AllocationOwner* = custom WadE owner field, see *0_PreProcessCaliforniaAllocationData.ipynb* for specifics.
    - *AllocationPriorityDate* = custom WadE owner field, see *0_PreProcessCaliforniaAllocationData.ipynb* for specifics.
    - *AllocationTimeframeEnd* = custom WadE owner field, see *0_PreProcessCaliforniaAllocationData.ipynb* for specifics.
    - *AllocationTimeframeStart* = custom WadE owner field, see *0_PreProcessCaliforniaAllocationData.ipynb* for specifics.
    - *AllocationTypeCV* = **WR_TYPE**.
    - *AllocationVolume_AF* = **FACE_VALUE_AMOUNT**.
    - *BeneficialUseCategory* = **USE_CODE**, Unspecified if Blank.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | SiteUUID | AllocationLegalStatusCV | AllocationVolume_AF | BeneficialUseCategory
---------- | ---------- | ------------ 
10 | CAwr_S49583, CAwr_S49584 | 28959.1 | Licensed | Power

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [California State Water Resources Control Board (CSWRCB)](https://www.waterboards.ca.gov).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

CSWRCB Staff
- asfdv
