# Water Use (Aggregated amounts) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water use data made available by the [California Department of Water Resources (CDWR)](https://data.ca.gov/dataset/water-plan-water-balance-data), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.

## Overview 
The California water use data are obtained from the online [ftp site](ftp://mae2.sdsc.edu/published/).  The water use data are provided in preadsheets for each year that summarize water balance at the Detailed Analysis Units by County (DAUCO), state (ST), hydrologic region (HR), and planning areas (PA) levels of aggregation.

The Python scripts described here are [Jupyter Notebooks](https://jupyter.org/) to prepare the aggregated water use data at DAUCO level for five years (2011 - 2015) for which data currently exist at the ftp site.  

## Summary
This document summarizes the process to prepare and share CDWR’s Water Use data for inclusion into the WSWC’s Water Data Exchange (WaDE 2.0) project.  Input files taken from the [ftp site](ftp://mae2.sdsc.edu/published/) for each year are combined by the scripts into unified dataframe that uses DAUCO as aggregation unit.  In order to extract the CDWR’s water use data from the input files and publish it online through ESRI layers so that it can be ready for WaDE 2.0, two Python scripts are used to generate CSV files for aggregated amounts and reporting units input tables (Step 1), and four other CSV files are manually created (Step 2), in data tables compatible with WaDE 2.0.


# Step 1: Execute Python Scripts to Generate CSV Data for aggregated amounts and reporting units.
The following scripts use queries to extract CDWR’s water use data into views compatible with WaDE 2.0 (see list below for name of each script).  

- #1. reportingunits_CA.ipynb
- #2. aggregatedamounts_CA.ipynb

Note: The outputs from 'reportingunits_CA.ipynb' (reportingunit csv file) provides an input to the 'aggregatedamounts_CA.ipynb', so the order in which scripts are operated is important.  

All scripts can be found at the WaDE’s Github repository [MappingStatesDataToWaDE2.0 in the California folder](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/California).

#### Inputs: The following spreadsheets are inputs to both scripts:

  CA-DWR-WaterBalance-Level2-DP-1000-2015-DAUCO.csv
  CA-DWR-WaterBalance-Level2-DP-1000-2014-DAUCO.csv
  CA-DWR-WaterBalance-Level2-DP-1000-2013-DAUCO.csv
  CA-DWR-WaterBalance-Level2-DP-1000-2012-DAUCO.csv
  CA-DWR-WaterBalance-Level2-DP-1000-2011-DAUCO.csv

Note: If data for others years become available, the scripts can run just for the new data and update the WaDE database.

## 1-1. reportingunits_CA.ipynb
Purpose: generate a list of DAUCO units where water use is aggregated and their associated metadata.

#### Inputs: 
- **spreadsheets listed above**

Dependency:  None

Supplemental Scripts Required:  None

#### Operation:
- Read the input file into one dataframe for all years.
- Generate empty **reportingunits.csv** file with controlled vocabulary headers.
- Assign DAUCOs as reporting units
- Assign reporting units IDs.
- Assign geometry for the coordinate of the center of the reporting unit
- Enter default values for fields with constant values or those that do not have values currently.
- Drop duplicate rows if they exist.
- Copy results into **reportingunits.csv** and export.			

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

---------- | ---------- | ---------------- | ------------- | ------------------------ | ------------ | -------------------| 
------------------ | -----------------

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

