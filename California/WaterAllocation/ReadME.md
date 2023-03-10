# CSWRCB Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [California State Water Resources Control Board (CSWRCB)](https://www.waterboards.ca.gov), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

- [**California Water Rights LIST (Detail Summary List)**](https://data.ca.gov/dataset/water-rights):  detail information about every water rights record in the State Water Resources Control Board's "Electronic Water Rights Information Management System" (EWRIMS) database. The unique identifier for the dataset is "Application ID". The dataset provides one record per Application ID and all the existing associated data to that record. Riparian rights, anything with water right type = "Statement of Div and Use" make exempt.  We want to include these records.


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CSWRCB's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see **CAwr_Allocation Schema Mapping to WaDE.xlsx**.  The following executable code files were used to extract the CSWRCB's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  Some information is considered simple enough to work and can be completed by hand (e.g., method.csv, variable.csv, organization.csv).  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining  code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those code files used for this project are as follows...

- 0_CAwr_PreProcessAllocationData.ipynb
- 4_CAwr_WaterSources.py
- 5_CAwr_Sites.py
- 6_CAwr_AllocationsAmounts_facts.py
- 7_CAwr_PODSiteToPOUSiteRelationships.py
- 8_CAwr_WaDEDataAssessmentScript.py

## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- California Allocation Data: https://drive.google.com/drive/folders/139TPw55eS7cCHLMg9E6qZ1Ew9-P-0og_?usp=sharing


***
### 0) Code File: 0_CAwr_PreProcessAllocationData.ipynb
Purpose: Pre-process the state agency's input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - California Water Rights LIST

#### Outputs:
 - Pwr_CAMain.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.
- Create WaDE *in_VariableSpecificUUID* based on unit given in the **use_direct_div_rate_units** field.  Separate by either a recognized CFS value or AF value (see below).
- Generate a CFS and a AF value from **use_direct_diversion_rate** input field using the  **use_direct_div_rate_units** input field...
    - CFS values include: Cubic Feet per Second, Gallons per Day (converted to CFS by / 646316.883), Acre-feet per Year (converted to CFS by / 723.968), Gallons per Minute (converted to CFS by / 448.83117).
    - AF values include: Acre-feet, Gallons (converted to AF by / 325850.943).
- Remove trialing '_' and ',' values from  **water_right_type** and **sub_type** input fields.
- Any record with a 'RIPERIAN', 'PRE1914' or 'Statement of Div and Use' are considered Riparian rights and we want to include into WaDE.  Will allow for exceptions.
- Any Record with a blank or nan value, replace with a 0 if numeric, or "WaDE_Unspecified" if string or object.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *Pwr_CAMain.csv*.


***
### 1) Code File: 1_CAwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
$${\color{red}Create by hand.}$$

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
CAwr_M1 | Surface water or subsurface water | Adjudicated


***
### 2) Code File: 2_CAwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`

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
CAwr_V1 | 1 | Year | AFY |


***
### 3) Code File: 3_CAwr_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`

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
CAwr_O1 | California State Water Resources Control Board | Greg Gearheart | https://www.waterboards.ca.gov/


***
### 4) Code File: 4_CAwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- Pwr_CAMain.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency data info to the *WaDE WaterSources* specific columns.  See **CAwr_Allocation Schema Mapping to WaDE.xlsx** for specific details.  Items of note are as follows...
    - *WaterSourceName* =  **source_name**, "WaDE_Unspecfield" if blank.
    - *WaterSourceNativeID* = custom WaDE ID field, see *0_PreProcessCaliforniaAllocationData* for details.
    - *WaterSourceTypeCV* = **source_type**, "WaDE_Unspecfield" if blank.
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
- Pwr_CAMain.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to the *WaDE Site* specific columns.  See **CAwr_Allocation Schema Mapping to WaDE.xlsx** for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersource.csv input file. See code for specific implementation of extraction.
    - *CoordinateMethodCV* = **location_method**.
    - *County* = **county**.
    - *HUC12* = **huc_12_number**.
    - *HU8* = **huc_8_number**.
    - *Latitude* = **latitude**.
    - *Longitude* = **longitude**.
    - *SiteName* = **pod_name**, "WaDE_Unspecified" if blank.
    - *SiteNativeID* = **pod_id**, "WaDE_Unspecified" if blank.
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
- Pwr_CAMain.csv
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
- Assign state agency info to the *WaDE Water Allocations* specific columns.  See **CAwr_Allocation Schema Mapping to WaDE.xlsx** for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationApplicationDateID* = **application_recd_date**, format to %m/%d/%Y.
    - *AllocationFlow_CFS* = **use_direct_diversion_rate**inputs, see *0_CAwr_PreProcessAllocationData.ipynb* for specifics.
    - *AllocationLegalStatusCV* = **water_right_status**, "WaDE_Unspecified" if blank.
    - *AllocationNativeID* = **application_number**.
    - *AllocationOwner* = **primary_owner_name**,
    - *AllocationPriorityDate* = **priority_date**, format to %m/%d/%Y.
    - *AllocationTimeframeEnd* = **direct_div_season_end**.
    - *AllocationTimeframeStart* = **direct_div_season_start**.
    - *AllocationTypeCV* = **water_right_type + sub_type**.
    - *AllocationVolume_AF* = **use_direct_diversion_rate**inputs, see *0_CAwr_PreProcessAllocationData.ipynb* for specifics.
    - *BeneficialUseCategory* = **use_code**, "WaDE_Unspecified" if blank.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* , *AllocationFlow_CFS*, & *AllocationVolume_AF* fileds.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationUUID | SiteUUID | AllocationLegalStatusCV | AllocationFlow_CFS | BeneficialUseCategory
---------- | ---------- | ------------ | ---------- | ----------
CAwr_WR1 | CAwr_S17128| Licensed | 2.5 | Irrigation

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
Not used for this project...


***
### 8) Code File: 8_CAwr_WaDEDataAssessmentScript.py
Purpose: generate visuals and analytics used by the WaDE staff to inspect the processed data.


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [California State Water Resources Control Board (CSWRCB)](https://www.waterboards.ca.gov).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

CSWRCB Staff
- Greg Gearheart. Deputy Director, Office of Information Management and Analysis, California Water Boards
- Rafael Maestu. Economist/Chief Data Scientist, California Water Boards
