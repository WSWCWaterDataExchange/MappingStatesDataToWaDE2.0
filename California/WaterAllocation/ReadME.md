# Water Rights (Allocation amounts) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water allocations data made available by the [California State Water Resources Control Board (CSWRCB) eWRIMS – Electronic Water Rights Information Management System](https://www.waterboards.ca.gov/waterrights/water_issues/programs/ewrims/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.

## Overview 
The California water rights data are available through multiple sites: 

- [Water rights records Search](https://ciwqs.waterboards.ca.gov/ciwqs/ewrims/EWServlet?Redirect_Page=EWWaterRightPublicSearch.jsp&Purpose=getEWAppSearchPage)

- [Web GIS data](https://waterrightsmaps.waterboards.ca.gov/viewer/index.html?viewer=eWRIMS.eWRIMS_gvh#).  

- [Tableau dashboard](https://public.tableau.com/profile/rafael.maestu#!/vizhome/WaterRightsTypesbyWatershedHUC6SENIORRIGHTS/HUC6Dashboard)  

The data used in the design and coding of the WaDE2 inputs was in following spreadsheet as a preliminary dataset obtained from CSWRCB, and it is used as input for the tables below.

**EWRIMS MASTER FLAT FILE DATA DICTIONARY DRAFT 1-17-20.xlsx**

The Python scripts described here are [Jupyter Notebooks](https://jupyter.org/) to prepare the water allocations data in csv format that can be ingested into the WaDE2 DB.  

## Summary
This document summarizes the process to prepare and share CSWRCB’s water rights data for inclusion into the WSWC’s Water Data Exchange (WaDE 2.0) project. In order to extract the CSWRCB’s water use data from the input files and publish it online through ESRI layers so that it can be ready for WaDE 2.0, three Python scripts are used to generate CSV files for water sources, sites, and water allocations input tables (Step 1), and three other CSV files are manually created (Step 2), in data tables compatible with WaDE 2.0.

# Step 1: Execute Python Scripts to Generate CSV Data for water sources, sites, and water allocations.
The following scripts use queries to extract CDWR’s water use data into views compatible with WaDE 2.0 (see list below for name of each script).  

- #1. watersources_CA.ipynb
- #2. sites_CA.ipynb
- #3. waterallocations_CA.ipynb

Note: The outputs from 'watersources_CA.ipynb' and 'sites_CA.ipynb' (water sources and sites csv files) provide inputs to the 'waterallocations_CA.ipynb', so the order in which scripts are operated is important.  

All scripts can be found at the WaDE’s Github repository [MappingStatesDataToWaDE2.0 in the California folder](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/California).

#### Inputs: The following spreadsheet is input file to all scripts:

  EWRIMS MASTER FLAT FILE DATA DICTIONARY DRAFT 1-17-20.xlsx

## 1-1. watersources_CA.ipynb
Purpose: generate a list of water source names, source types, and quality indicators.

#### Inputs: 
- **spreadsheet listed above**

Dependency:  None

Supplemental Scripts Required:  None

#### Operation:
- Read the input file into one dataframe for all years.
- Generate empty **watersources.csv** file with controlled vocabulary headers.
- Get all unique water source names from the input file and assign them to the output dataframe
- Assign soure type if it exists.
- Enter default values for fields with constant values or those that do not have values currently.
- Drop duplicate rows if they exist.
- Generate WaterSourceNativeID
- Assign water source UUID to each (unique) row.
- Copy results into **watersources.csv** and export.			

#### Sample Data (Note: not all fields shown):
WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV
------------ | ------------ | -------- | ---------- | ---- 
CA_2  | 2 | LAKE DOMINGO | Surface | Fresh

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **watersources_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **watersources_CA.ipynb** include the following: 
- WaterSourceUUID
- WaterSourceTypeCV
- WaterQualityIndicatorCV

## 1-2. sites_CA.ipynb
Purpose: generate a list of sites where water is diverted for use (also Points OF Diversion, PODs).

Dependency:  None

Supplemental Scripts Required: None

#### Inputs: 
- **spreadsheet listed above**

#### Operation:   
- Generate empty sites.csv file with controlled vocabulary headers
- Assign SiteNativeID from POD_ID
- Specify site name from DIVERSION_SITE_NAME in input file
- Specify site type from TYPE_OF_DIVERSION_FACILITY in the input file
- Copy latitude and longitude values
- Specify coordinate mathod based on LOCATION_METHOD in the input file
- Drop duplicates if any
- Generate SiteUUID based on SiteNativeID 
- Drop data if missing latitude/longitude
- copy results into **sites.csv** and export.  

#### Sample Data (Note: not all fields shown):
SiteUUID | SiteNativeID | SiteName  | SiteTypeCV | Longitude | Latitude
------------ | ------------ | ---------- | ---- | ---- | ----
CA_65767 | 65767 | REINHAKEL DITCH  | Gravity  | -118.4468 | 37.3685

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **sites_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **sites_CA.ipynb** include the following: 
- SiteUUID 
- SiteName
- CoordinateMethodCV 
- EPSGCodeCV

## 1-3. waterallocations_CA.ipynb
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

Dependency: watersources.csv and sites.csv generated above.

Supplemental Scripts Required: None

#### Inputs: 
- **spreadsheet listed above**

#### Operation:
 - Generate empty waterAllocations.csv file with controlled vocabulary headers
 - Assign Native Allocation ID from APPLICATION_NUMBER 
 - Map Site IDs from sites.csv based on POD_ID corresanding to NativeAllocationID
 - Map Watersource IDs from watersources.csv based on SOURCE_NAME corresponding to NativeAllocationID 
 - Assign Beneficial Use from USE_CODE
 - Assign Allocation type from WATER_RIGHT_TYPE
 - Assign Legal status from WATER_RIGHT_STATUS
 - Assign Allocation owner from PRIMARY_OWNER_NAME
 - Get Allocation priority date from PRIORITY_DATE or APPLICATION_ACCEPTANCE_DATE
 - Map Allocation time frame start and time frame end from DIRECT_DIV_SEASON_START and DIRECT_DIV_SEASON_END
 - Format the datetime data above in the WaDE2 DB compatible form
 - Get Allocation amount from MAX_RATE_OF_DIVERSION and convert units from Gallons per minute to CFS
 - Get Allocation maximum from USE_DIRECT_DIV_ANNUAL_AMOUNT
 - Assign Irrigated acreage from USE_NET_ACREAGE
 - Drop rows if both Allocation amount and Allocation maximum are null
 - Drop duplicates if any
 - Copy results into **waterallocations.csv** and export  

#### Sample Data (Note: not all fields shown):
OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseCategory | AllocationNativeID | AllocationOwner | AllocationTypeCV | AllocationLegalStatusCV   
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ---------- | ----------- 
CSWRCB| CA_60498| CA_2  | Dust Control | T032025 |569 EAST COUNTY BOULEVARD, LLC | Temporary Permit | Cancelled 

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **allocations_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **waterallocations_CA.ipynb** include the following: 
- OrganizationUUID
- VariableSpecificUUID
- WaterSourceUUID
- MethodUUID
- AllocationPriorityDate

# Step 2: Manually Modify Existing Files to Generate CA CSV Data Compatible with WaDE 2.0.
The following is a quick description of three CSV files manually created to be used as inputs into WaDE 2.0.  These tables usually have single rows, so are prepared by manual inspection.


## 2-1. variables.csv 
Purpose: generate legend of granular variables specific to each state.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.

VariableSpecificUUID | VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV | MaximumAmountUnitCV
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- | --------- | -------
CSWRCB Allocation all  | Allocation All | Allocation | Average | 1 | Year |10 | WaterYear| CFS | AFY

## 2-2. methods.csv
Purpose: generate legend of granular variables specific to each state detailing water right / allocation / etc data collection.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.       

MethodUUID | MethodName | MethodDescription| MethodNEMLink | ApplicableResourceTypeCV | MethodTypeCV | DataCoverageValue | DataQualityValueCV	| DataConfidenceValue
---------- | ---------- | ------------ | ------------- | ------------- | ------------ | -------------| ------------ | ---------- 
CSWRCB-Water Rights | California Water Rights | Water Rights | https://www.waterboards.ca.gov/waterrights/water_issues/programs/ewrims/ | Surface water or subsurface water | Adjudicated	|         |         |                 

  
## 2-3. Organizations.csv
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.               

OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite | OrganizationPhoneNumber |	OrganizationContactName	| OrganizationContactEmail |	OrganizationDataMappingURL |	State 
---------------- | ------------ | -------- | ---------- | ---------- | ------------ | -------------- | ------------ | ---------
CSWRCB |California State Water Resources Control Board | The Electronic Water Rights Information Management System (eWRIMS) is a computer database developed by the State Water Resources Control Board to track information on water rights in California. | https://www.waterboards.ca.gov/waterrights/water_issues/programs/ewrims/ | 916-341-5892 |	Greg Gearheart | Greg.Gearheart@waterboards.ca.gov | https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/California	| CA


