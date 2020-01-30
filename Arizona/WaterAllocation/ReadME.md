# Water Rights (Allocation amounts) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water allocations data made available by the [Arizona Department of Water Resources (ADWR)](https://new.azwater.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.

## Overview 
The water rights data were obtained from the Arizona Department of Water Resources (ADWR) GIS data:
http://gisdata-azwater.opendata.arcgis.com/

Overview of Arizona Groundwater management Code can be found at:
http://infoshare.azwater.gov/docushare/dsweb/Get/Document-11348/Groundwater_Code_Overview.pdf

The following two spreadsheets for wells data were downloaded 
  - **Well_Registry_Wells55.csv**
  - **GWSI_Sites.csv**
  
According to background data at the ADWR website (http://gisdata-azwater.opendata.arcgis.com/datasets/4ab4a7d7761b49d79fec040880afb1d3_0), the '**Wells 55 Registry**' contains all wells registered in the state. The '**Groundwater Well Site Inventory (GWSI)**' contains well locations, construction, and water level measurements for wells located and sampled in the field. Out of 44239 well records in GWSI database, 23150 have a '**Wells 55 Registry ID**'. Here, the records of these two tables were joined based on the **Wells 55 Registry ID** field and form the input table to the WaDE import codes. 

The Python scripts described here are [Jupyter Notebooks](https://jupyter.org/) to prepare the water allocations data in csv format that can be ingested into the WaDE2 DB.

## Summary
This document summarizes the process to prepare and share ADWR’s water rights data for inclusion into the WSWC’s Water Data Exchange (WaDE 2.0) project. In order to extract the WSDE’s water allocations data from the input files and publish it online through ESRI layers so that it can be ready for WaDE 2.0, two Python scripts are used to generate CSV files for sites and water allocations input tables (Step 1), and four other CSV files are manually created (Step 2), in data tables compatible with WaDE 2.0.

# Step 1: Execute Python Scripts to Generate CSV Data for sites and water allocations.
The following scripts use queries to extract WSDE’s water rights data into views compatible with WaDE 2.0 (see list below for name of each script).  

- #1. sites_AZ.ipynb
- #2. waterallocations_AZ.ipynb

Note: The outputs from 'sites_AZ.ipynb' (sites csv file) provide inputs to the 'waterallocations_AZ.ipynb', so the order in which scripts are operated is important.  

All scripts can be found at the WaDE’s Github repository [MappingStatesDataToWaDE2.0 in the Arizona folder](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/edit/master/Arizona/).

## 1-1. sites_AZ.ipynb
Purpose: generate a list of sites where water is diverted for use (also known as Points Of Diversion, PODs).

Dependency:  None

Supplemental Scripts Required: None

#### Inputs: 
  - **Well_Registry_Wells55.csv**
  - **GWSI_Sites.csv**
  
#### Operation:   
- Generate empty sites.csv file with controlled vocabulary headers.
- Assign SiteNativeID from 'SITE_ID'.
- Specify site type from 'WELL_TYPE'.
- Leave site name as 'Unspecified'.
- Project 'UTM_X_METERS' and 'UTM_Y_METERS' coordindates in NAD 83 UTM Zone 12 to longitude and latitude in EPSG:4236.
- Leave the CoordinateMethodCV as 'Unspecified'.
- Specify StateCV as 'AZ'
- Drop duplicates if any.
- Generate SiteUUID based on SiteNativeID. 
- Drop data if missing latitude/longitude.
- copy results into **sites.csv** and export.  

#### Sample Data (Note: not all fields shown):
SiteUUID | SiteNativeID | SiteName  | SiteTypeCV | Longitude | Latitude 
------------ | ------------ | ---------- | ---- | ---- | ---- 
AZ_334708112295301 | 334708112295301 | Unspecified  | INDEX | -112.4981 | 33.7849 

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **sites_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **sites_AZ.ipynb** include the following: 
- SiteUUID 
- SiteName
- CoordinateMethodCV 
- EPSGCodeCV

## 1-2. waterallocations_AZ.ipynb
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

Dependency: sites.csv generated above.

Supplemental Scripts Required: None

#### Inputs: 
  - **Well_Registry_Wells55.csv**
  - **GWSI_Sites.csv**

#### Operation:
 - Generate empty waterAllocations.csv file with controlled vocabulary headers.
 - Assign Native Allocation ID from 'REGISTRY_ID'.
 - Get Site IDs from sites.csv based on the mapping between 'SITE_ID' and 'REGISTRY_ID'.
 - Assign Beneficial use category from 'WATER_USE'.
 - Get Allocation type from 'WELLTYPE'. 
 - Specify Allocation owner from 'OWNER_NAME'.
 - Get Allocation priority date from 'APPLICATION_DATE' and format it in WaDE2 compatible form.
 - Assign Allocation time frame start and end the default values of 01/01 and 12/31, respectively.
 - Get Allocation amount from 'PUMPRATE'.
 - Get Allocation maximum from 'TESTEDRATE', assuming the test rate here means maximum allowed pumping rate.
 - Drop rows if both Allocation amount and Allocation maximum are null.
 - Drop duplicates if any.
 - Copy results into **waterallocations.csv** and export.  

#### Sample Data (Note: not all fields shown):
OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseCategory | AllocationNativeID | AllocationOwner | AllocationTypeCV | AllocationLegalStatusCV   
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ---------- | ----------- 
ADWR| AZ_334708112295301 | AZ_1 | INDUSTRIAL | 60001 |SFI GRAND VISTA, LLC  | NON-EXEMPT - NON-SERVICE |  

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **allocations_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **waterallocations_AZ.ipynb** include the following: 
- OrganizationUUID
- VariableSpecificUUID
- WaterSourceUUID
- MethodUUID
- AllocationPriorityDate

# Step 2: Manually Modify Existing Files to Generate AZ CSV Data Compatible with WaDE 2.0.
The following is a quick description of three CSV files manually created to be used as inputs into WaDE 2.0.  These tables usually have single rows, so are prepared by manual inspection.


## 2-1. watersources.csv
Purpose: generate a list of water source names, source types, and quality indicators.

Dependency:  None

Supplemental Scripts Required:  None
	
#### Sample Data (Note: not all fields shown):
WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV
------------ | ------------ | -------- | ---------- | ---- 
AZ_1  | 1 | Unknown | Groundwater well | Fresh

## 2-2. variables.csv 
Purpose: generate legend of granular variables specific to each state.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.

VariableSpecificUUID | VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV | MaximumAmountUnitCV
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- | --------- | -------
ADWR Allocation all  | Allocation All | Allocation | Average | 1 | Year |10 | WaterYear| CFS | AFY

## 2-3. methods.csv
Purpose: generate legend of granular variables specific to each state detailing water right / allocation / etc data collection.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.       

MethodUUID | MethodName | MethodDescription| MethodNEMLink | ApplicableResourceTypeCV | MethodTypeCV | DataCoverageValue | DataQualityValueCV	| DataConfidenceValue
---------- | ---------- | ------------ | ------------- | ------------- | ------------ | -------------| ------------ | ---------- 
ADWR-Water Rights | Arizona Water Rights | Water Rights | http://gisdata-azwater.opendata.arcgis.com/| Groundwater | Adjudicated	|         |         |                 

  
## 2-4. Organizations.csv
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.               

OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite | OrganizationPhoneNumber |	OrganizationContactName	| OrganizationContactEmail |	OrganizationDataMappingURL |	State 
---------------- | ------------ | -------- | ---------- | ---------- | ------------ | -------------- | ------------ | ---------
ADWR |Arizona Department of Water Resources  | The Arizona Department of Water Resources is the steward of Arizona’s water future and ensures long-term, reliable water supplies to support the continued economic prosperity of the State. |  http://gisdata-azwater.opendata.arcgis.com/ | 602-771-8500 |	Rebecca Mitchell | abc@co.com |https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Arizona | AZ

