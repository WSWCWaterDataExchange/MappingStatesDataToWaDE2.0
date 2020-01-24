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
- Assign water source UUID to each (unique) row.
- Copy results into **watersources.csv** and export.			

#### Sample Data (Note: not all fields shown):
ReportingUnitUUID	| ReportingUnitNativeID | ReportingUnitName | ReportingUnitTypeCV | ReportingUnitUpdateDate | EPSGCodeCV | Geometry
------------------| --------------------- | ----------------- | --------------------| ------------------------| ---------- | ---------
CA_DAU01949 | DAU01949	| Gualala	| Detailed Analysis Unit by County (DAUCO)	| 1/2/2020	|	EPSG:4326 | POINT (-123.28035020000002 38.66392589)


## 1-2. aggregatedallocations_CA.ipynb
Purpose: generate master sheet of water uses to import into WaDE 2.0.

Dependency:  None

Supplemental Scripts Required: None

#### Inputs: 
- **spreadsheets listed above**
- **reportingunits.csv**
- **watersources.csv**

#### Operation:   
- Read the input files and join contents into one dataframe for all years.
- Generate empty **aggregatedalloctions.csv** file with controlled vocabulary headers.
- Assign water source IDs from water sources input file.
- Assign for each water use the corresponding reporting unit ID from reporting units input file.
- Assign beneficial uses from the column **CategoryA** in the input files.
- Calculate water use amount for each row as aggregate (Sum) of those for unique DAUCO and Beneficial use (CategoryA) groups. Convert units to AF
- Assign default values for fields with constant values or those with no detailed information currently.
- Copy results into **aggregatedamounts.csv** and export.
        

#### Sample Data (Note: not all fields shown):
OrganizationUUID | ReportingUnitUUID | BeneficialUseCategory | WaterSourceUUID | MethodUUID | ReportYearCV | Amount   
---------------- | ----------------- | ------------------ | --------------------- | --------------- | ----------- | --------- 
CDWR | CA_DAU04827| Instream Flow Requirements | CA_1 | CDWR_Water_uses | 2011 | 723700

Any rows that are missing required fields are dropped from the WaDE-ready dataset and instead are saved in a separate csv file (e.g. **aggregatedamounts_mandatoryFieldMissing.csv**) for review.  This allows for ease of future inspection on missing items.  Mandatory fields for the **aggregatedallocations_CA.ipynb** include the following:
- OrganizationUUID
- ReportingUnitUUID
- WaterSourceUUID
- MethodUUID
- Amount


# Step 2: Manually Modify Existing Files to Generate CA CSV Data Compatible with WaDE 2.0.
The following is a quick description of four CSV files manually created by hand to be used as inputs into WaDE 2.0.  These tables usually have single rows, so are prepared by manual inspection.


## 2-1. watersources.csv
Purpose: generate list of water sources from which water is allocated from.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
 - See the below prepared table.

WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV | GNISFeatureNameCV | Geometry
--------------- | ------------------- | --------------- | ----------------- | ------------------------|-------------------|--------- 
CA_1	| 1     | Unspecificed	| Groundwater, Surface Water  | Fresh         	      | 		  |		

   		

## 2-2. variables.csv 
Purpose: generate legend of granular variables specific to each state.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.

VariableSpecificUUID | VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV 
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- | -------------
Consumptive Use  | Consumptive Use | Consumptive Use | Cumulative| 1 | Year |1-Jan| CalendarYear| Acre feet
  

## 2-3. methods.csv
Purpose: generate legend of granular variables specific to each state detailing water right / allocation / etc data collection.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.       

MethodUUID | MethodName | MethodDescription| MethodNEMLink | ApplicableResourceTypeCV | MethodTypeCV | DataCoverageValue | DataQualityValueCV	| DataConfidenceValue
---------- | ---------- | ------------ | ------------- | ------------- | ------------ | -------------| ------------ | ---------- 
CDWR_Water_uses | California Water Uses | OWIA Standard Operating Procedure: Water Balance | ftp://mae2.sdsc.edu/published/ | Unspecified | Water Use	|         |         |                 

  
## 2-4. Organizations.csv
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.               

OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite | OrganizationPhoneNumber |	OrganizationContactName	| OrganizationContactEmail |	OrganizationDataMappingURL |	State 
---------------- | ------------ | -------- | ---------- | ---------- | ------------ | -------------- | ------------ | ---------
CDWR |California Department of Water Resources | Department of Water Resources California Water Plan program computes applied, net, and depletion water balances for California. | https://data.ca.gov/dataset/water-plan-water-balance-data | xxx-xxx-xxxx |	Jennifer Stricklin | Jennifer.Stricklin@water.ca.gov | https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/California	| CA


