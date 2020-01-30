# Water Rights (Allocation amounts) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water allocations data made available by the [Oklahoma Water Resources Board (OWRB)](https://www.owrb.ok.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.

## Overview 
The water rights data were obtained from the OWRB Open Data websites for:

Permitted Surface Water Diversion Points
http://home-owrb.opendata.arcgis.com/datasets/permitted-surface-water-diversion-points?geometry=-119.379%2C31.373%2C-77.565%2C37.701  

Permitted Groundwater Wells (Point coverage)
http://home-owrb.opendata.arcgis.com/datasets/permitted-groundwater-wells  

Dedicated Lands (for groundwater; not used for surface water) (polygon coverage)
http://home-owrb.opendata.arcgis.com/datasets/dedicated-lands  

Areas of Use (polygon coverage) - Should be both for SW and GW and should be different than Dedicated Lands
http://home-owrb.opendata.arcgis.com/datasets/areas-of-use

The following two spreadsheets are downloaded and used as inputs:

 - **Permitted_Surface_Water_Diversion_Points.csv**
 - **Permitted_Ground_Water_Wells**

The Python scripts described here are [Jupyter Notebooks](https://jupyter.org/) to prepare the water allocations data in csv format that can be ingested into the WaDE2 DB.

## Summary
This document summarizes the process to prepare and share OWRB’s water rights data for inclusion into the WSWC’s Water Data Exchange (WaDE 2.0) project. In order to extract the OWRB’s water allocations data from the input files and publish it online through ESRI layers so that it can be ready for WaDE 2.0, three Python scripts are used to generate CSV files for water sources, sites, and water allocations input tables (Step 1), and three other CSV files are manually created (Step 2), in data tables compatible with WaDE 2.0.

# Step 1: Execute Python Scripts to Generate CSV Data for water sources, sites, and water allocations.
The following scripts use queries to extract WSDE’s water rights data into views compatible with WaDE 2.0 (see list below for name of each script).  

- #1. watersources_OK.ipynb
- #2. sites_OK.ipynb
- #3. waterallocations_OK.ipynb

Note: The outputs from 'watersources_OK.ipynb' and 'sites_OK.ipynb' (water sources and sites csv files) provide inputs to the 'waterallocations_OK.ipynb', so the order in which scripts are operated is important.  

All scripts can be found at the WaDE’s Github repository [MappingStatesDataToWaDE2.0 in the Washington folder](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/edit/master/Oklahoma/).

## 1-1. watersources_OK.ipynb
Purpose: generate a list of water source names, source types, and quality indicators.

#### Inputs: 
none: This table contains two rows, one for ground water and one for surface water as there are no pertinent inputs in the input spreadsheets listed above.

Dependency:  None

Supplemental Scripts Required:  None

#### Operation:
- Generate empty **watersources.csv** file with controlled vocabulary headers.
- Assign 'Unspecified' for water source names as it doesn't currently exit. 
- Enter water soure types 'SurfaceWater' and 'GroundWater' to the first and second rows, respectively.
- Enter default values for fields with constant values or those that do not have values currently.
- Drop duplicate rows if they exist.
- Generate WaterSourceNativeIDs 1 and 2 for the first and second rows, respectively.
- Assign water source UUID as 'OK_1' and 'OK_2' for the first and second rows, respectively.
- Copy results into **watersources.csv** and export.			

#### Sample Data (Note: not all fields shown):
WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV
------------ | ------------ | -------- | ---------- | ---- 
OK_1  | 1 | Unspecified | Surface Water | Fresh
OK_2  | 2 | Unspecified | Groundwater   | Fresh

## 1-2. sites_OK.ipynb
Purpose: generate a list of sites where water is diverted for use (also known as Points Of Diversion, PODs).

Dependency:  None

Supplemental Scripts Required: None

#### Inputs: 
 - **Permitted_Surface_Water_Diversion_Points.csv**
 - **Permitted_Ground_Water_Wells**

#### Operation:   
- Generate empty sites.csv file with controlled vocabulary headers.
- Assign SiteNativeID from 'OBJECTID'.
- Specify site type from 'Water Type'.
- Leave site name as 'Unspecified'.
- Copy Longitude and Latitude from 'Longitude' and 'Latitude' in the input files.
- Drop duplicates if any.
- Generate SiteUUID based on SiteNativeID. 
- Drop data if missing latitude/longitude.
- copy results into **sites.csv** and export.  

#### Sample Data (Note: not all fields shown):
SiteUUID | SiteNativeID | SiteName  | SiteTypeCV | Longitude | Latitude 
------------ | ------------ | ---------- | ---- | ---- | ---- 
OK_561 | 561 | Not Provided  | Groundwater | -101.8963 | 36.5747 

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **sites_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **sites_OK.ipynb** include the following: 
- SiteUUID 
- SiteName
- CoordinateMethodCV 
- EPSGCodeCV

## 1-3. waterallocations_OK.ipynb
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

Dependency: watersources.csv and sites.csv generated above.

Supplemental Scripts Required: None

#### Inputs: 
 - **Permitted_Surface_Water_Diversion_Points.csv**
 - **Permitted_Ground_Water_Wells**

#### Operation:
 - Generate empty waterAllocations.csv file with controlled vocabulary headers.
 - Assign Native Allocation ID from 'PERMIT_NUMBER'.
 - Get Site IDs from sites.csv based on the mapping between 'OBJECTID' and 'PERMIT_NUMBER'.
 - Assign the Watersource IDs 'OK_1', 'OK_2' based on the water soure type being surface water or ground water, respectively.
 - Assign Beneficial use category from 'PRIMARY_PURPOSE'.
 - Get Allocation type from 'PERMIT_TYPE'. 
 - Get Allocation legal status from 'STATUS'.
 - Get Allocation owner from 'ENTITY_NAME'.
 - Get Allocation priority date from 'DATE_ISSUED' 
 - Get Allocation application date from 'DATE_FILED'.
 - Assign Allocation time frame start and end the default values of 01/01 and 12/31, respectively.
 - Get Allocation maximum from 'TOTAL_PERMITTED_ACRE_FEET'. 
 - Drop rows if both Allocation amount and Allocation maximum are null.
 - Drop duplicates if any.
 - Copy results into **waterallocations.csv** and export.  

#### Sample Data (Note: not all fields shown):
OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseCategory | AllocationNativeID | AllocationOwner | AllocationTypeCV | AllocationLegalStatusCV   
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ---------- | ----------- 
WSDE| WA_2195 | WA_2 | Irrigation, Domestic general | 2066186 |LARSON, ARNOLD V. | Claim | Active  

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **allocations_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **waterallocations_OK.ipynb** include the following: 
- OrganizationUUID
- VariableSpecificUUID
- WaterSourceUUID
- MethodUUID
- AllocationPriorityDate

# Step 2: Manually Modify Existing Files to Generate OK CSV Data Compatible with WaDE 2.0.
The following is a quick description of three CSV files manually created to be used as inputs into WaDE 2.0.  These tables usually have single rows, so are prepared by manual inspection.


## 2-1. variables.csv 
Purpose: generate legend of granular variables specific to each state.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.

VariableSpecificUUID | VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV | MaximumAmountUnitCV
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- | --------- | -------
OWRB Allocation all  | Allocation All | Allocation | Average | 1 | Year |10 | WaterYear| CFS | AFY

## 2-2. methods.csv
Purpose: generate legend of granular variables specific to each state detailing water right / allocation / etc data collection.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.       

MethodUUID | MethodName | MethodDescription| MethodNEMLink | ApplicableResourceTypeCV | MethodTypeCV | DataCoverageValue | DataQualityValueCV	| DataConfidenceValue
---------- | ---------- | ------------ | ------------- | ------------- | ------------ | -------------| ------------ | ---------- 
OWRB_Water_rights | Oklahoma water rights | The OWRB appropriates stream and groundwater supplies to various water users in the state. Permits are issued for the use of both surface and groundwaters in Oklahoma (domestic uses are exempt) and all waters must be used beneficially without waste. | https://owrb.maps.arcgis.com/apps/webappviewer/index.html?id=db6e61cfdbc74a4d8b919b2eceef8d43| Allocation | Water Allocation	|         |         |                 

  
## 2-3. Organizations.csv
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.               

OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite | OrganizationPhoneNumber |	OrganizationContactName	| OrganizationContactEmail |	OrganizationDataMappingURL |	State 
---------------- | ------------ | -------- | ---------- | ---------- | ------------ | -------------- | ------------ | ---------
OWRB |Oklahoma Water Resources Board | OWRB produces and maintains datasets related to water in Oklahoma. | https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Oklahoma | 303-866-3581 |	Rebecca Mitchell | abc@co.com |https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Oklahoma	| OK

