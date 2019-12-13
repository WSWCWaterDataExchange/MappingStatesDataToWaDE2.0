# Water Use (Aggregated amounts) Data Preparation for WaDE

This readme details an overview, the specific steps taken, and the final product of the process applied to water use data made available by the [New Mexico Office of the State Engineer NMOSE](http://geospatialdata-ose.opendata.arcgis.com/datasets/ose-points-of-diversion) for inclusion into the Water Data Exchange (WaDE). For more information on WaDE, please visit http://wade.westernstateswater.org/

### Overview 
The New Mexico water use data are aggreged based on two reporting units: one on basis of counties (Summary of withdrawals by county 90-15.xlsx) and the other based on river basins (Summary of withdrawals by River Basin 90-15.xlsx). The codes included here use county based aggregated amounts.

### Summary
This document summarizes the process to prepare and share NMOSE’s Water use data for inclusion in the Western States Water Council’s Water Data Exchange (WaDE 2.0). In order to extract the New Mexico water use data from the input files and publish it online through ESRI layers to be ready for WaDE 2.0, you must generate CSV data compatible with WaDE 2.0. Some of these are small files with only few rows and can be prepared by manualy modifying existing csv files for other states. The aggregated amount and reporting units tables are prepared by executing the (Python) Jupyter notebook codes described below.
 
 ## Data Prep
 ### Step 1: Execute Python Notebooks to generate CSV data compatible with WaDE 2.0

There are 2 Jupyter notebook scripts and one Python script that use queries to extract NMOSE’s water use data into views compatible with WaDE 2.0. The **beneficialuseDictionary.py** holds dictionaries that are required for mapping different codes to their respective names, for example codes for the legal status of water use. The **utilityFunctions.py**, holds functions that are required to be called from other scripts **aggregatedamounts_NM.ipynb** and **reportingunits_NM.ipynb**.  All scripts can be found at the following link in WaDE’s Github repository “MappingStatesDataToWaDE2.0” in the New Mexico folder:
https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/NewMexico

The Python notebooks and Scripts are are thus divided into two:

**1. Scripts to prepare the csv files**
- **reportingunits_NM.ipynb**
- **aggregatedamounts_NM.ipynb**

**2. Dependency scripts**
- **beneficialuseDictionary.py**
- **utilityFunctions.py**



##  1.  reportingunits_NM.ipynb - generate a list of units where water use aggregated
 Input Table: 
 **Summary of withdrawals by county 90-15.xlsx**

Supplemental Script required:
NA

        - read from the input file, spreadsheets for multiple years and concatenate the data into one dataframe for all years
	- generate empty reportingunits.csv file with controlled vocabulary headers
        - assign county names as reporting units names
        - give reporting units IDs 
	- enter default values for fields with constant values or those that do not have values currently
        - copy results into **reportingunits.csv** and export

		ReportingUnitUpdateDate	ReportingUnitProductVersion	
				

#### Sample data (all columns not included):

   ReportingUnitUUID | ReportingUnitName | ReportingUnitTypeCV | StateCV 
   ------------ | ------------ | ---------- | ---- 
   NM_1 | Bernalillo |County | NM 


reportingunit.csv is input to aggregatedamounts_NM.ipnb.


##  2. waterallocations_NM.ipynb - generate master sheet of water allocations to import into WaDE 2.0
 Input Table: 
 **Summary of withdrawals by county 90-15.xlsx**   

Supplemental Script required:
**beneficialuseDictionary.py**
 -Includes dictionaries for different types of variables. 
 
Supplemental Script required 2:
**utilityFunctions.py**

       - read from the input file, spreadsheets for multiple years and concatenate the data into one dataframe for all years
       - generate empty aggregatedalloctions.csv file with controlled vocabulary headers
       - assign water source IDs for each water use
       - read from reportingunits.csv and assign for each water use the corresponding reporting unit ID
       - map water use amount for each row
       - assign default values for fields with constant values or those with no detailed information currently
       - copy results into **aggregatedamounts.csv** and export
        


####  Sample data (all columns not included):
   
   OrganizationUUID | ReportingUnitUUID | PrimaryUseCategory | BeneficialUseCategory | WaterSourceUUID | MethodUUID   
   ---------------- | ----------------- | ------------------ | --------------------- | --------------- | ----------- 
  NMOSE| NM_1| Irrigation   | Public Water Supply | Fresh_Ground |NMOSE_Water_uses

Any row missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**aggregatedamounts_mandatoryFieldMissing.csv**) for future inspection.
Mandatory fields include: 
 - OrganizationUUID
 - ReportingUnitUUID
 - WaterSourceUUID
 - MethodUUID
 - Amount


### Step 2: Modify existing files to generate NM CSV data compatible with WaDE 2.0

##  3. watersources.csv   

The following table is prepared

WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV | GNISFeatureNameCV | Geometry
--------------- | ------------------- | --------------- | ----------------- | ------------------------|-------------------|--------- 
Fresh_Surface	| Fresh_Surface	      | 		| Unspecified	    | Fresh         	      | 		  |		
Fresh_Ground	| Fresh_Ground	      | 		| Unspecified	    | Fresh         	      | 		  |		
Fresh_SW_GW	| Fresh_SW_GW	      | 		| Unspecified	    | Fresh         	      | 		  |		

   		

### 4. variables.csv 
        - all values are hard-coded according to state

#### Sample data (all columns not included):

   VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV 
   ---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- 
  Consumptive Use | Consumptive Use | Cumulative| 1 | Year |1-Oct| WaterYear| Acre feet
  

### 5. methods.csv
       - all values are hard-coded according to state
       
#### Sample data (all columns not included):
   
   MethodUUID | MethodName | MethodDescription| MethodNEMLink 
   ---------------- | ------------ | -------- | ----------  
  NMOSE_Water_uses| New Mexico Water Uses | Withdrawal Volume Estimate| http://geospatialdata-ose.opendata.arcgis.com/search?groupIds=fabf18d6e0634ae38c86475c9ada6498 
 
  
  ### 6. Organizations.csv 
  
        -All variables are hardcoded according to organization.
        
 #### Sample data (all columns not included):
   
   OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite |
   ---------------- | ------------ | -------- | ---------- 
  NMOSE | 	New Mexico Office of the State Engineer | The New Mexico Office of the State Engineer (OSE) provides this geographic data and any associated metadata “as is” without warranty of any kind | https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/NewMexico 

