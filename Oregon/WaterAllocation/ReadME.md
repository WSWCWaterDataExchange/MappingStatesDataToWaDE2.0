# Water Rights (Allocation amounts) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water allocations data made available by the [Oregon Water Resources Department (OWRD)](https://www.oregon.gov/OWRD/access_Data/Pages/Data.aspx), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.

## Overview 
The water rights data were downloaded from the website https://www.oregon.gov/OWRD/access_Data/Pages/Data.aspx

There are multiple rows for different data types. The data used here were downloaded from the row named **"Statewide Water Right Spatial Data with Metadata"**. Spatial data for Points of Diversions (PODs) and Points of Use (POUs) and a file linking water rights to PODs are available in Geodatabase and shapefile formats which we exported to CSV files (in QGIS) to be used as inputs to the Python codes developed here to prepare WaDE2 input files:

 - **wr_pod_nhdevent.csv**
 - **wr_v_pod_public.csv   (POD info with related Water right)**      
 
PODs refer to Water right surface Points of Diversion (POD) and groundwater Points of Appropriation (POA) locations in the state of Oregon.

The Python scripts described here are [Jupyter Notebooks](https://jupyter.org/) to prepare the water allocations data in csv format that can be ingested into the WaDE2 DB.  

## Documentations
The following documentation downloaded from the website above provides the metadata information:

 - **wr_pod_metadata.pdf**

And the water rights related code keys are available at: **https://www.oregon.gov/owrd/WRDFormsPDF/wris_code_key.pdf**

## Summary
This document summarizes the process to prepare and share OWRD’s water rights data for inclusion into the WSWC’s Water Data Exchange (WaDE 2.0) project. In order to extract the OWRD’s water allocations data from the input files and publish it online through ESRI layers so that it can be ready for WaDE 2.0, three Python scripts are used to generate CSV files for water sources, sites, and water allocations input tables (Step 1), and three other CSV files are manually created (Step 2), in data tables compatible with WaDE 2.0.

# Step 1: Execute Python Scripts to Generate CSV Data for water sources, sites, and water allocations.
The following scripts use queries to extract OWRD’s water rights data into views compatible with WaDE 2.0 (see list below for name of each script).  

- #1. watersources_OR.ipynb
- #2. sites_OR.ipynb
- #3. waterallocations_OR.ipynb

Note: The outputs from 'watersources_OR.ipynb' and 'sites_OR.ipynb' (water sources and sites csv files) provide inputs to the 'waterallocations_OR.ipynb', so the order in which scripts are operated is important.  

All scripts can be found at the WaDE’s Github repository [MappingStatesDataToWaDE2.0 in the Oregon folder](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/edit/master/Oregon/).

#### Inputs: The following spreadsheet is input file to all scripts:

- **wr_v_pod_public_xy.csv**   (POD file including the relationship between water rights and POD and xy coordinates of PODs)

## 1-1. watersources_OR.ipynb
Purpose: generate a list of water source names, source types, and quality indicators.

#### Inputs: 
- **spreadsheet listed above**

Dependency:  None

Supplemental Scripts Required:  None

#### Operation:
- Read the input file.
- Form the output dataframe.
- Generate empty **watersources.csv** file with controlled vocabulary headers.
- Assign water soure type based on the dictionary mapping the code 'wr_type' to storage, surface water, and ground water.
- Assign water source name from 'source' if it exists, or else put source name as 'Unspecified'.
- Enter default values for fields with constant values or those that do not have values currently.
- Drop duplicate rows if they exist.
- Generate WaterSourceNativeID.
- Assign water source UUID to each (unique) row.
- Copy results into **watersources.csv** and export.			

#### Sample Data (Note: not all fields shown):
WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV
------------ | ------------ | -------- | ---------- | ---- 
OR_1  | 1 | FORMOSA 1 ADIT | groundwater | Fresh

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **watersources_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **watersources_OR.ipynb** include the following: 
- WaterSourceUUID
- WaterSourceTypeCV
- WaterQualityIndicatorCV

## 1-2. sites_OR.ipynb
Purpose: generate a list of sites where water is diverted for use (also known as Points Of Diversion, PODs).

Dependency:  None

Supplemental Scripts Required: None

#### Inputs: 
- **spreadsheet listed above**

#### Operation:   
- Generate empty sites.csv file with controlled vocabulary headers.
- Assign SiteNativeID from 'pod_location_id'.
- Specify site type based on dictionary that maps the 'source_type' code to its respective values.
- Leave site name as 'Unspecified'.
- Project X and Y coordindates in EPSG:2992 to longitude and latitude in EPSG:4236.
- Enter coordinate mathod as 'Unspecified'.
- Specify State controlled vocabulary as 'OR'.
- Drop duplicates if any.
- Generate SiteUUID based on SiteNativeID. 
- Drop data if missing latitude/longitude.
- copy results into **sites.csv** and export.  

#### Sample Data (Note: not all fields shown):
SiteUUID | SiteNativeID | SiteName  | SiteTypeCV | Longitude | Latitude | StateCV
------------ | ------------ | ---------- | ---- | ---- | ---- | -------
OR_6909 | 6909 | Unspecified  | well  | -123.3828 | 42.8558 | OR

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **sites_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **sites_OR.ipynb** include the following: 
- SiteUUID 
- SiteName
- CoordinateMethodCV 
- EPSGCodeCV

## 1-3. waterallocations_OR.ipynb
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

Dependency: watersources.csv and sites.csv generated above.

Supplemental Scripts Required: None

#### Inputs: 
- **spreadsheet listed above**

#### Operation:
 - Generate empty waterAllocations.csv file with controlled vocabulary headers.
 - Assign Native Allocation ID from 'snp_id'.
 - Map Site IDs from sites.csv based on the 'pod_location_id's that correspond to the NativeAllocationID ('snp_id'). Note there might be multiple sites mapped into one water right.
 - Map Watersource IDs from watersources.csv based on source name and source type.
 - Assign Beneficial Use from 'use_code_description'.
 - Map Allocation type from dictionary for 'claim_char' code. 
 - Specify Allocation owner as company name from 'name_company' or the 'name_last' and 'name_first' of individual owners.
 - Get Allocation priority date from 'priority_date' and format it in WaDE2 compatible form.
 - Get Allocation time frame start by concatenating 'begin_month' and 'begin_day' and formating them to 'mm/dd' form.
 - Get Allocation time frame end by concatenating 'end_month' and 'end_day' and formating them to 'mm/dd' form.
 - Get Allocation amount from 'rate_cfs' for each POD corresponding to a given water right, and aggregate/sum them to obtain value for a the water right.
 - Get Allocation maximum from 'max_rate_acre_feet' for each POD corresponding to a given water right, and aggregate/sum them to obtain value for a the water right.
 - Assign WaterAllcation Native URL from 'wris_link'.
 - Drop rows if both Allocation amount and Allocation maximum are null.
 - Drop duplicates if any.
 - Copy results into **waterallocations.csv** and export.  

#### Sample Data (Note: not all fields shown):
OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseCategory | AllocationNativeID | AllocationOwner | AllocationTypeCV | AllocationLegalStatusCV   
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ---------- | ----------- 
OWRD| OR_6909, OR_6910| OR_1  | MINING | 21755 |FORMOSA EXPLORATION INC. |  |  

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **allocations_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **waterallocations_OR.ipynb** include the following: 
- OrganizationUUID
- VariableSpecificUUID
- WaterSourceUUID
- MethodUUID
- AllocationPriorityDate

# Step 2: Manually Modify Existing Files to Generate OR CSV Data Compatible with WaDE 2.0.
The following is a quick description of three CSV files manually created to be used as inputs into WaDE 2.0.  These tables usually have single rows, so are prepared by manual inspection.


## 2-1. variables.csv 
Purpose: generate legend of granular variables specific to each state.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.

VariableSpecificUUID | VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV | MaximumAmountUnitCV
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- | --------- | -------
OWRD Allocation all  | Allocation All | Allocation | Average | 1 | Year |10 | WaterYear| CFS | AFY

## 2-2. methods.csv
Purpose: generate legend of granular variables specific to each state detailing water right / allocation / etc data collection.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.       

MethodUUID | MethodName | MethodDescription| MethodNEMLink | ApplicableResourceTypeCV | MethodTypeCV | DataCoverageValue | DataQualityValueCV	| DataConfidenceValue
---------- | ---------- | ------------ | ------------- | ------------- | ------------ | -------------| ------------ | ---------- 
OWRD-Water Rights | Oregon Water Rights | Water Rights | https://www.oregon.gov/OWRD/access_Data/Pages/Data.aspx| Surface/Ground/Storage | Adjudicated	|         |         |                 

  
## 2-3. Organizations.csv
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.               

OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite | OrganizationPhoneNumber |	OrganizationContactName	| OrganizationContactEmail |	OrganizationDataMappingURL |	State 
---------------- | ------------ | -------- | ---------- | ---------- | ------------ | -------------- | ------------ | ---------
OWRD |Oregon Water Resources Department | Water right surface Points of Diversion (POD) and groundwater Points of Appropriation (POA) locations in the state of Oregon are collectively referred to as PODs. | https://www.oregon.gov/OWRD/access_Data/Pages/Data.aspx   | 503-986-0900 |	Tom Byler | wrd_dl_Director@oregon.gov |https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Oregon	| OR
