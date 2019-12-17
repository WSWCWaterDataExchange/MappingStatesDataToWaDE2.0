# Water Use (Aggregated amounts) Data Preparation for WaDE

This readme details an overview, the specific steps taken, and the final product of the process applied to water use data made available by the [Texas Water Development Board (TWDB)](http://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp) for inclusion into the Water Data Exchange (WaDE). For more information on WaDE, please visit http://wade.westernstateswater.org/

### Overview 
The codes and data here provide the Texas water use information which are aggreged based on two reporting units, counties and river basins.

### Summary
This document summarizes the process to prepare and share TWDB’s Water use data for inclusion in the Western States Water Council’s Water Data Exchange (WaDE 2.0). In order to extract the Texas water use data from the input files and publish it online through ESRI layers to be ready for WaDE 2.0, you must generate CSV data compatible with WaDE 2.0. Some of these are small files with only few rows and can be prepared by manualy modifying existing csv files for other states. The aggregated amount and reporting units tables are prepared by executing the (Python) Jupyter notebook codes described below.
 
 ## Data Prep
 ### Step 1: Execute Python Notebooks to generate CSV data compatible with WaDE 2.0

There are 3 Jupyter notebook scripts and one Python script that use queries to extract TWDB’s water use data into views compatible with WaDE 2.0. The **beneficialuseDictionary.py** holds dictionaries that are required for mapping different codes to their respective names, for example codes for the legal status of water use. The **utilityFunctions.py**, holds functions that are required to be called from other scripts **aggregatedamounts_NM.ipynb** and **reportingunits_NM.ipynb**. The script **Prepare_TWDB_data_For_WaDE.ipynb** is a pre-processing code that extracts from the input files (in multiple folders) obtained from TWDB, csv files that serve as intermediate input files. All scripts can be found at the following link in WaDE’s Github repository “MappingStatesDataToWaDE2.0” in the Texas folder:
https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Texas

The Python notebooks and Scripts are thus divided into three:

**1. Scripts to prepare the intermediate csv files**
- **Prepare_TWDB_data_For_WaDE.ipynb**

**2. Scripts to prepare the csv files for WaDE 2**
- **reportingunits_NM.ipynb**
- **aggregatedamounts_NM.ipynb**

**3. Dependency scripts**
- **beneficialuseDictionary.py**
- **utilityFunctions.py**



##  1.  Prepare_TWDB_data_For_WaDE.ipynb - generate a number of intermediate csv files that provide inputs to the aggregated use codes below
 Input Files: 
 
 **Multiple folders holdign two spreadsheets for each year, e.g., for year 2001:**
 
 2001/SumFinal_BasinReport.xlsx
 
 2001/SumFinal_CountyReport.xlsx

Supplemental Script required:
NA

        - read from the input file in each directory, pivot and concatenate the data in multiple spreadsheets
        - generate the following files that form intermediate inputs
				

#### outputs:

S_USE_AMOUNT.csv

SUMMARY_USE.csv

REPORTING_UNIT.csv

REPORT.csv

S_USE_IRRIGATION.csv

LU_BENEFICIAL_USE.csv

These serve as inputs to the following scripts


##  2.  reportingunits_NM.ipynb - generate a list of units where water use aggregated
 Input Table: 
 **REPORTING_UNIT.csv**

Supplemental Script required:
NA

        - read the input file into one dataframe for all years
        - generate empty reportingunits.csv file with controlled vocabulary headers
        - assign county names and basin names as reporting units names
        - assign reporting units IDs
        - enter default values for fields with constant values or those that do not have values currently
        - drop duplicate rows if they exist
        - copy results into **reportingunits.csv** and export
				

#### Sample data (all columns not included):
   
ReportingUnitUUID	| ReportingUnitNativeID | ReportingUnitName | ReportingUnitTypeCV | ReportingUnitUpdateDate | EPSGCodeCV
------------------| --------------------- | ----------------- | --------------------| ------------------------| ---------
TX_12 | 12	| BRAZOS	| Basin	| 12/5/2019	|	EPSG:4326



##  3. aggregatedallocations_NM.ipynb - generate master sheet of water uses to import into WaDE 2.0
 Input Tables: 
 **"S_USE_AMOUNT.csv**
 **SUMMARY_USE.csv"**   

Supplemental Script required:
**LU_BENEFICIAL_USE.csv**
 -Includes beneficial use dictionaries. 
 
Supplemental Script required 2:
NA

       - read the input files and join contents into one dataframe for all years
       - generate empty aggregatedalloctions.csv file with controlled vocabulary headers
       - assign water source IDs for each water use
       - assign for each water use the corresponding reporting unit ID
       - assign benefical uses from dictionary constructed based on input file LU_BENEFICIAL_USE.csv
       - map water use amount for each row
       - assign default values for fields with constant values or those with no detailed information currently
       - copy results into **aggregatedamounts.csv** and export
        

####  Sample data (all columns not included):
   
   OrganizationUUID | ReportingUnitUUID | BeneficialUseCategory | WaterSourceUUID | MethodUUID | ReportYearCV | PopulationServed   
   ---------------- | ----------------- | ------------------ | --------------------- | --------------- | ----------- | --------- 
  TWDB | TX_12| Municipal_ground | TWDB_1 | TWDB_Water_uses| 2000 | 2127781

Any row missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**aggregatedamounts_mandatoryFieldMissing.csv**) for future inspection.
Mandatory fields include: 
 - OrganizationUUID
 - ReportingUnitUUID
 - WaterSourceUUID
 - MethodUUID
 - Amount


### Step 2: Modify existing files to generate NM CSV data compatible with WaDE 2.0

##  3. watersources.csv   

 - The following table is prepared


WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV | GNISFeatureNameCV | Geometry
--------------- | ------------------- | --------------- | ----------------- | ------------------------|-------------------|--------- 
TWDB_1	| 1     | 		| Ground	    | Fresh         	      | 		  |		
TWDB_2	| 2	    | 		| Surface	    | Fresh         	      | 		  |		
TWDB_3	| 3	    | 		| Reuse	    | Fresh         	      | 		  |		

   		

### 4. variables.csv 
        - all values are hard-coded according to state

#### Sample data (all columns not included):

   VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV 
   ---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- 
  Consumptive Use | Consumptive Use | Cumulative| 1 | Year |1-Jan| CalendarYear| Acre feet
  

### 5. methods.csv
       - all values are hard-coded according to state
       
#### Sample data (all columns not included):
   
   MethodUUID | MethodName | MethodDescription| MethodNEMLink 
   ---------------- | ------------ | -------- | ----------  
  TWDB_Water_uses| Texas Water Uses | Historical Water Use Estimates| http://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp 	

  
### 6. Organizations.csv 
  
        -All variables are hardcoded according to organization.
        
 #### Sample data (all columns not included):
   
   OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite |
   ---------------- | ------------ | -------- | ---------- 
  TWDB |Texas Water Development Board | Each year the Texas Water Development Board conducts an annual survey of ground and surface water use by municipal and industrial entities within the state of Texas | http://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp
 
