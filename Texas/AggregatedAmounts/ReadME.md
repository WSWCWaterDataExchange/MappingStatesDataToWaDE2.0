# Water Use (Aggregated amounts) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water use data made available by the [Texas Water Development Board (TWDB)](http://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.

## Overview 
Texas hosts its water use data online at the [TWDB Website](http://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp).  Texas water use information are aggreged based on two reporting units: counties and river basins.

Python scripts described here for inclusion into WaDE are operated using [Jupyter Notebooks](https://jupyter.org/).

## Summary
This document summarizes the process to prepare and share TWDB’s Water Use data for inclusion into the WSWC’s Water Data Exchange (WaDE 2.0) project.  Input files are taken directly from the [TWDB’s]( http://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp) website.  In order to extract the TWDB’s water use data from the input files and publish it online through ESRI layers so that it can be ready for WaDE 2.0, five separate Python scripts to generate CSV specific data (Step 1), and four manual created CSV files (Step 2),  need to be executed so that the data will be compatible with WaDE 2.0.


# Step 1: Execute Python Scripts to Generate CSV Data Compatible with WaDE 2.0.
The following scripts use queries to extract TWDB’s water use data into views compatible with WaDE 2.0 (see list below for name of each script).  The scripts are further divided into three categories: 1) scripts to create input CSV files, 2) scripts to prepare the csv files for WaDE 2.0, 3) and dependency scripts.

**Scripts to Create Input CSV Files**
- #1. Prepare_TWDB_data_For_WaDE.ipynb

**Scripts to Prepare the CSV Files for WaDE 2.0**
- #2. reportingunits_TX.ipynb
- #3. aggregatedamounts_TX.ipynb

**Dependency Scripts**
- beneficialuseDictionary.py
- utilityFunctions.py

The order in which scripts are operated is important as some act as inputs into others.  The recommended order is that laid here.

The **Prepare_TWDB_data_For_WaDE.ipynb** script is a pre-processing code that extracts from the available files obtained from TWDB into a workable CSV file.  The **beneficialuseDictionary.py** dependency script holds dictionaries that are required for mapping different codes to their respective names, for example codes for the legal status of water use.  The **utilityFunctions.py** dependency script holds functions that are required to be called from other scripts **aggregatedamounts_TX.ipynb** and **reportingunits_TX.ipynb**.  

All scripts can be found at the WaDE’s Github repository [MappingStatesDataToWaDE2.0 in the Texas folder](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Texas).

## 1-1. Prepare_TWDB_data_For_WaDE.ipynb
Purpose: generate a number of intermediate CSV files that provide inputs to the aggregated use codes below

Dependency: the output of the **Prepare_TWDB_data_For_WaDE.ipynb** serves as inputs for the **reportingunits_TX.ipynb** and the **aggregatedallocations_TX.ipynb** files.

Supplemental Scripts Required:  None.
 
#### Input:
- Multiple folders holding water use data spreadsheets for each year (e.g. 2001/SumFinal_BasinReport.xlsx, 2001/SumFinal_CountyReport.xlsx, etc.).

#### Operation: 
- Read from the input file in each directory, spreadsheets for multiple years and pivot and concatenate the data.
- Generate the files that form intermediate inputs.


## 1-2. reportingunits_TX.ipynb
Purpose: generate a list of units where water use aggregated.

Dependency:  None

Supplemental Scripts Required:  **Prepare_TWDB_data_For_WaDE.ipynb**

#### Input: 
- **REPORTING_UNIT.csv**.  

#### Operation:
- Read the input file into one dataframe for all years.
- Generate empty **reportingunits.csv** file with controlled vocabulary headers.
- Assign county names and basin names as reporting units names.
- Assign reporting units IDs.
- Enter default values for fields with constant values or those that do not have values currently.
- Drop duplicate rows if they exist.
- Copy results into **reportingunits.csv** and export.			

#### Sample Data (Note: not all fields shown):
ReportingUnitUUID	| ReportingUnitNativeID | ReportingUnitName | ReportingUnitTypeCV | ReportingUnitUpdateDate | EPSGCodeCV
------------------| --------------------- | ----------------- | --------------------| ------------------------| ---------
TX_12 | 12	| BRAZOS	| Basin	| 12/5/2019	|	EPSG:4326


## 1-3. aggregatedallocations_TX.ipynb
Purpose: generate master sheet of water uses to import into WaDE 2.0.

Dependency:  None

Supplemental Scripts Required:
- **LU_BENEFICIAL_USE.csv**.  Includes beneficial use dictionaries.
- **Prepare_TWDB_data_For_WaDE.ipynb**

#### Input: 
- **S_USE_AMOUNT.csv**
- **SUMMARY_USE.csv**

#### Operation:   
- Read the input files and join contents into one dataframe for all years.
- Generate empty **aggregatedalloctions.csv** file with controlled vocabulary headers.
- Assign water source IDs for each water use.
- Assign for each water use the corresponding reporting unit ID.
- Assign beneficial uses from dictionary constructed based on input file **LU_BENEFICIAL_USE.csv**.
- Map water use amount for each row.
- Assign default values for fields with constant values or those with no detailed information currently.
- Copy results into **aggregatedamounts.csv** and export.
        

#### Sample Data (Note: not all fields shown):
OrganizationUUID | ReportingUnitUUID | BeneficialUseCategory | WaterSourceUUID | MethodUUID | ReportYearCV | PopulationServed   
---------------- | ----------------- | ------------------ | --------------------- | --------------- | ----------- | --------- 
TWDB | TX_12| Municipal_ground | TWDB_1 | TWDB_Water_uses| 2000 | 2127781

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **aggregatedamounts_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **aggregatedallocations_NM.ipynb** include the following:
- OrganizationUUID
- ReportingUnitUUID
- WaterSourceUUID
- MethodUUID
- Amount


# Step 2: Manually Modify Existing Files to Generate TX CSV Data Compatible with WaDE 2.0.
The following is a quick description of four CSV files manually created by hand to be used as inputs into WaDE 2.0.  These values were derived from the [TWDB’s]( http://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp) by manual inspection.


## 2-1. watersources.csv
Purpose: generate list of water sources from which water is allocated from.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
 - See the below prepared table.

WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV | GNISFeatureNameCV | Geometry
--------------- | ------------------- | --------------- | ----------------- | ------------------------|-------------------|--------- 
TWDB_1	| 1     | 		| Ground	    | Fresh         	      | 		  |		
TWDB_2	| 2	    | 		| Surface	    | Fresh         	      | 		  |		
TWDB_3	| 3	    | 		| Reuse	    | Fresh         	      | 		  |		

   		

## 2-2. variables.csv 
Purpose: generate legend of granular variables specific to each state.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.

VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV 
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- 
Consumptive Use | Consumptive Use | Cumulative| 1 | Year |1-Jan| CalendarYear| Acre feet
  

## 2-3. methods.csv
Purpose: generate legend of granular variables specific to each state detailing water right / allocation / etc data collection.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.       

MethodUUID | MethodName | MethodDescription| MethodNEMLink 
---------------- | ------------ | -------- | ----------  
TWDB_Water_uses| Texas Water Uses | Historical Water Use Estimates| http://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp 	

  
## 2-4. Organizations.csv
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.               

OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite |
---------------- | ------------ | -------- | ---------- 
TWDB |Texas Water Development Board | Each year the Texas Water Development Board conducts an annual survey of ground and surface water use by municipal and industrial entities within the state of Texas | http://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp

