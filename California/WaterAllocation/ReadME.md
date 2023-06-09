# CSWRCB Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [California State Water Resources Control Board (CSWRCB)](https://www.waterboards.ca.gov), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**California Water Rights Points of Diversion LIST (Detail Summary List)** | This list includes detail information about every Point of Diversion water rights record in the State Water Resources Control Board's "Electronic Water Rights Information Management System" (EWRIMS) database. | [link](https://data.ca.gov/dataset/california-water-rights-points-of-diversion) | [link](https://data.ca.gov/dataset/1c2117f4-e4be-47f7-9eb5-81b086aefe34/resource/2902511b-6b50-4084-82f0-d1a508a80067/download/ewrims-points-of-diversion-data-dictionary-final.xlsx)


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- California Allocation Data: https://drive.google.com/drive/folders/139TPw55eS7cCHLMg9E6qZ1Ew9-P-0og_?usp=sharing

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NMOSE's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *CAwr_Allocation Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the NMOSE's water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_CAwr_PreProcessAllocationData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_CAwr_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv.
- **3_CAwr_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_CAwr_PreProcessAllocationData.ipynb
Purpose: Pre-process the state agency's input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - California Water Rights LIST

#### Outputs:
 - Pwr_caMain.zip

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.
- Create WaDE *in_VariableSpecificUUID* based on unit given in the **use_direct_div_rate_units** field.  Separate by either a recognized CFS value or AF value (see below).
- Generate a CFS and a AF value from **use_direct_diversion_rate** input field using the  **use_direct_div_rate_units** input field...
    - CFS values include: Cubic Feet per Second, Gallons per Day (converted to CFS by / 646316.883), Acre-feet per Year (converted to CFS by / 723.968), Gallons per Minute (converted to CFS by / 448.83117).
    - AF values include: Acre-feet, Gallons (converted to AF by / 325850.943).
- Remove trialing '_' and ',' values from  **water_right_type** and **sub_type** input fields.
- Any record with a 'RIPERIAN', 'PRE1914' or 'Statement of Div and Use' are considered Riparian rights and we want to include into WaDE.  Will allow for exceptions.
- At this time, CA does not track priority date.  Any water right missing a priority date value we will also make exempt at this time as a temp fix. 
- Any Record with a blank or nan value, replace with a 0 if numeric, or "WaDE_Unspecified" if string or object.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *Pwr_CAMain.zip*.


***
## Code File: 2_CAwr_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv).

#### Inputs:
- Pwr_caMain.zip

#### Outputs:
- methods.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- variables.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- organizations.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- watersources.csv
- sites.csv
- waterallocations.csv
- podsitetopousiterelationships.csv


## 1) Method Information
Purpose: generate legend of granular methods used on data collection.

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


## 2) Variables Information
Purpose: generate legend of granular variables specific to each state.

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


## 3) Organization  Information
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

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


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

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


## 5) Site Information
Purpose: generate a list of sites where water is diverted (also known as Points Of Diversion, PODs).

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
SiteUUID | WaterSourceUUID | Latitude | Longitude | PODorPOUSite | SiteName | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
CAwr_S1 | CAwr_WSwadeID49  | 40.9631 | -124.1 | POD | WaDE Blank | Point Of Direct Diversion

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


## 6) AllocationsAmounts Information
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

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
    - *AllocationPriorityDate* not always provided.  Will make this data ExemptOfVolumeFlowPriority = **True** as temp fix.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* , *AllocationFlow_CFS*, & *AllocationVolume_AF* fileds.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationUUID | MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | AllocationFlow_CFS | AllocationLegalStatusCV | AllocationNativeID | AllocationPriorityDate | BeneficialUseCategory
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
CAwr_WRA000016 | CAwr_M1 | CAwr_O1 | CAwr_S404, CAwr_S34881, CAwr_S17603, CAwr_S29028 | CAwr_V1 | 0 | Licensed | A000016 | - | Domestic

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


### 7) POD Site -To- POU Polygon Relationships
Purpose: generate linking element between POD and POU sites that share the same water right.
Note: podsitetopousiterelationships.csv output only needed if both POD and POU data is present, ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `otherwise produces empty file.`

#### Operation and Steps:
- Read the sites.csv & waterallocations.csv input files.
- Create three temporary dataframes: one for waterallocations, & two for site info that will store POD and POU data separately.
- For the temporary POD dataframe...
  - Read in site.csv data from sites.csv with a _PODSiteUUID_ field = POD only.
  - Create _PODSiteUUID_ field = _SiteUUID_.
- For the temporary POU dataframe
  - Read in site.csv data from sites.csv with a _PODSiteUUID_ field = POU only.
  - Create _POUSiteUUID_ field = _SiteUUID_.
- For the temporary waterallocations dataframe, explode _SiteUUID_ field to create unique rows.
- Left-merge POD & POU dataframes to the waterallocations dataframe via _SiteUUID_ field.
- Consolidate waterallocations dataframe by grouping entries by _AllocationNativeID_ filed.
- Explode the consolidated waterallocations dataframe again using the _PODSiteUUID_ field, and again for the _POUSiteUUID_ field to create unique rows.
- Perform error check on waterallocations dataframe (check for NaN values)
- If waterallocations is not empty, export output dataframe _podsitetopousiterelationships.csv_.


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [California State Water Resources Control Board (CSWRCB)](https://www.waterboards.ca.gov).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

CSWRCB Staff
- Greg Gearheart. Deputy Director, Office of Information Management and Analysis, California Water Boards
- Rafael Maestu. Economist/Chief Data Scientist, California Water Boards
