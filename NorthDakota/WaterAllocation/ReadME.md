# Water Rights (Allocation amounts) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water allocations data made available by the [North Dakota State Water Commission (NDSWC)](https://swc.nd.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.

## Overview 
The water rights data were obtained from the North Dakota State Water Commission map services: https://mapservice.swc.nd.gov/

'**Water permits**' layer was downloaded from this web based map, the shapefile downloaded was then exported to a csv file in QGIS:
 - **Permits.csv**

The Python scripts described here are [Jupyter Notebooks](https://jupyter.org/) to prepare the water allocations data in csv format that can be ingested into the WaDE2 DB.

## Summary
This document summarizes the process to prepare and share NDSWC’s water rights data for inclusion into the WSWC’s Water Data Exchange (WaDE 2.0) project. In order to extract the NDSWC’s water allocations data from the input files and publish it online through ESRI layers so that it can be ready for WaDE 2.0, three Python scripts are used to generate CSV files for water sources, sites, and water allocations input tables (Step 1), and three other CSV files are manually created (Step 2), in data tables compatible with WaDE 2.0.

# Step 1: Execute Python Scripts to Generate CSV Data for water sources, sites, and water allocations.
The following scripts use queries to extract NDSWC’s water rights data into views compatible with WaDE 2.0 (see list below for name of each script).  

- #1. watersources_ND.ipynb
- #2. sites_ND.ipynb
- #3. waterallocations_ND.ipynb

Note: The outputs from 'watersources_ND.ipynb' and 'sites_ND.ipynb' (water sources and sites csv files) provide inputs to the 'waterallocations_ND.ipynb', so the order in which scripts are operated is important.  

All scripts can be found at the WaDE’s Github repository [MappingStatesDataToWaDE2.0 in the North Dakota folder](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/edit/master/NorthDakota/).

## 1-1. watersources_ND.ipynb
Purpose: generate a list of water source names, source types, and quality indicators.

#### Inputs: 
- **Permits.csv**

Dependency:  None

Supplemental Scripts Required:  None

#### Operation:
- Read the input file and form an output dataframe.
- Generate empty **watersources.csv** file with controlled vocabulary headers.
- Get water soure type from 'Source'. Put 'Unknown' for empty 'Source'.
- Get water source name from 'source_nam' and put 'Unspecified' if 'Source_nam' doesn't exist. 
- Enter default values for fields with constant values or those that do not have values currently.
- Drop duplicate rows if they exist.
- Generate WaterSourceNativeID.
- Assign water source UUID to each (unique) row.
- Copy results into **watersources.csv** and export.			

#### Sample Data (Note: not all fields shown):
WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV
------------ | ------------ | -------- | ---------- | ---- 
ND_3	| 3	| Charbonneau Creek	| Surface Water | Fresh

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **watersources_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **watersources_ND.ipynb** include the following: 
- WaterSourceUUID
- WaterSourceTypeCV
- WaterQualityIndicatorCV

## 1-2. sites_ND.ipynb
Purpose: generate a list of sites where water is diverted for use (also known as Points Of Diversion, PODs).

Dependency:  None

Supplemental Scripts Required: None

#### Inputs: 
- **Permits.csv**

#### Operation:   
- Generate empty sites.csv file with controlled vocabulary headers.
- Assign SiteNativeID from 'pod'.
- Get site type from 'source'.
- Get site name from 'aquifer', and enter 'Unspecified' if it doesn't exist.
- Get Longitude and Latitude from 'longitude' and 'latitude', respectively.
- Map the codes in 'Position_With_CD' to Coordinate mathod CV based on the corresponding dictionary.
- Leave Coordinate method CV as 'Unspecified'.
- Drop duplicates if any.
- Generate SiteUUID based on SiteNativeID. 
- Drop data if missing latitude/longitude.
- copy results into **sites.csv** and export.  

#### Sample Data (Note: not all fields shown):
SiteUUID | SiteNativeID | SiteName  | SiteTypeCV | Longitude | Latitude 
------------ | ------------ | ---------- | ---- | ---- | ---- 
ND_1 | 13007302B | Unspecified  | Ground Water | -99.78988 | 46.1113 

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **sites_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **sites_ND.ipynb** include the following: 
- SiteUUID 
- SiteName
- CoordinateMethodCV 
- EPSGCodeCV

## 1-3. waterallocations_ND.ipynb
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

Dependency: watersources.csv and sites.csv generated above.

Supplemental Scripts Required: None

#### Inputs: 
- **Permits.csv**

#### Operation:
 - Generate empty waterAllocations.csv file with controlled vocabulary headers.
 - Assign Native Allocation ID from 'permit_num'.
 - Get Site IDs from sites.csv based on the mapping between 'pod' and 'permit_num'. Note there might be multiple sites mapped into one water right.
 - Map Watersource IDs from watersources.csv based on source type and source name.
 - Assign Beneficial use category from 'use_type'.
 - Get Allocation legal status from 'status'.
 - Specify Allocation owner from 'permit_hol'.
 - Get Allocation priority date from 'priority_d'.
 - Assign Allocation time frame start from 'period_sta' 
 - Assign allocatino time frame end from 'period_end'
 - Get Allocation amount from 'req_rate'.
 - Get Allocation maximum from 'req_acft'. 
 - Drop rows if both Allocation amount and Allocation maximum are null.
 - Drop duplicates if any.
 - Copy results into **waterallocations.csv** and export.  

#### Sample Data (Note: not all fields shown):
OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseCategory | AllocationNativeID | AllocationOwner | AllocationTypeCV | AllocationLegalStatusCV   
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ---------- | ----------- 
NDSWC | ND_9, ND_9355, ND_9937 | ND_4 | Irrigation | 8A |WEYRAUCH, DANIEL |  | Perfected  

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **allocations_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **waterallocations_ND.ipynb** include the following: 
- OrganizationUUID
- VariableSpecificUUID
- WaterSourceUUID
- MethodUUID
- AllocationPriorityDate

# Step 2: Manually Modify Existing Files to Generate ND CSV Data Compatible with WaDE 2.0.
The following is a quick description of three CSV files manually created to be used as inputs into WaDE 2.0.  These tables usually have single rows, so are prepared by manual inspection.


## 2-1. variables.csv 
Purpose: generate legend of granular variables specific to each state.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.

VariableSpecificUUID | VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV | MaximumAmountUnitCV
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- | --------- | -------
NDSWC Allocation all  | Allocation All | Allocation | Average | 1 | Year |10 | WaterYear| CFS | AFY

## 2-2. methods.csv
Purpose: generate legend of granular variables specific to each state detailing water right / allocation / etc data collection.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.       

MethodUUID | MethodName | MethodDescription| MethodNEMLink | ApplicableResourceTypeCV | MethodTypeCV | DataCoverageValue | DataQualityValueCV	| DataConfidenceValue
---------- | ---------- | ------------ | ------------- | ------------- | ------------ | -------------| ------------ | ---------- 
NDSWC-Water Rights | North Dakota Water Rights | Water Rights | https://mapservice.swc.nd.gov/| Surface Ground | Adjudicated	|         |         |                 

  
## 2-3. Organizations.csv
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.               

OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite | OrganizationPhoneNumber |	OrganizationContactName	| OrganizationContactEmail |	OrganizationDataMappingURL |	State 
---------------- | ------------ | -------- | ---------- | ---------- | ------------ | -------------- | ------------ | ---------
NDSWC |North Dakota State Water Commission | The Water Appropriation Division is responsible for the appropriation and management of the state’s water resources in accordance with Article XI of the North Dakota Constitution and Chapter 61 of North Dakota Century Code. |	https://swc.nd.gov/theswc/water_appropriations.html	| (701) 328-2754.	| Jon Patch	| abc@co.com |	https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/NorthDakota	| ND

