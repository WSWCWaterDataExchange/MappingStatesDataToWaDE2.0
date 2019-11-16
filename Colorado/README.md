# WaDE Preparation

This readme details an overview, the specific steps taken, and the final product of the process applied to water rights data made available by the [Colorado Department of Water Rights (CODWR)](https://cdnr.us/#/division/DWR) for inclusion into the Water Data Exchange (WaDE). 

### Overview 
The Colorado Department of Water Rights hosts its water right data at the [Colorado Information Marketplace](https://data.colorado.gov/Water/DWR-Water-Right-Net-Amounts/acsg-f33s).
The dataset is updated annually. For more information on WaDE, please visit http://wade.westernstateswater.org/


### Summary
This document summarizes the process to prepare and share CODWR’s Water Rights data from the Colorado Information Marketplace database for inclusion in the Western States Water Council’s Water Data Exchange (WaDE 2.0). In order to extract Colorado's water rights data and publish it online through ESRI layers to be ready for WaDE 2.0, you must execute 7 Python Scripts to generate CSV data compatible with WaDE 2.0.

 ## Data Prep
 ### Step 1: Execute 7 Python Scripts to generate CSV data compatible with WaDE 2.0

There are 7 Python Scripts that use queries to extract CODWR’s water rights data into views compatible with WaDE 2.0. Two of the scripts, **beneficialuseDictionary.py** and **waterallocationsFunctions.py**, are required as input scripts for **waterallocations.py**.  All scripts can be found at the following link in WaDE’s Github repository “MappingStatesDataToWaDE2.0” in the Colorado folder:
https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Colorado


The overall objective of the data migration scripts are to prepare datasets retrieved from state repositories for upload into WaDE 2.0.  This process applied to Colorado Water Rights data, and considering the data included in this dataset involves passing the raw data through seven Python scripts. These scripts are outlined below.

The 7 Scripts are entitled:
- **sites.py**
- **watersources.py**
- **waterallocations.py**
    - **beneficialuseDictionary.py**   
-  **methods.py**
-  **organizations.py**
-  **variables.py**

##  1.  sites.py - generate a list of sites where water is allocated
 Table Required: **DWR_Water_Right_-_Net_Amounts.csv** (Master Table containing Colorado Water Right Net Amount information) from [Colorado Information Marketplace](https://data.colorado.gov/Water/DWR-Water-Right-Net-Amounts/acsg-f33s))

        - generate empty sites.csv file with controlled vocabulary headers
        - drop duplicates of SiteNativeID, SiteName, SiteTypeCV       
        - drop data if missing latitude/longitude
        - hard code "Unknown" for SiteTypeCV value if it is missing      
        - generate WaDESiteUUID (Prepend CODWR with SiteNativeID)
        - drop data if missing WaDESiteUUID, SiteName, CoordinateMethodCV, GNISCodeCV, EPSGCodeCV       
        - copy results into **sites.csv** and export
        
        



#### Sample data (all columns not included):

   WaDESiteUUID | SiteNativeID | SiteTypeCV | Long | Lat|
   ------------ | ------------ | ---------- | ---- | ----|
   CODWR_100501 | 100501 |Ditch | -104.484 |40.37853|

Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**sites_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data.
  Mandatory fields include: 
 - SiteUUID 
 - SiteName
 - CoordinateMethodCV 
 - EPSGCodeCV



##  2. watersources.py - generate list of water sources from which water is allocated from
 Table Required: **DWR_Water_Right_-_Net_Amounts.csv** (Master Table containing Colorado Water Right Net Amount information) from [Colorado Information Marketplace](https://data.colorado.gov/Water/DWR-Water-Right-Net-Amounts/acsg-f33s))

       - generate empty watersources.csv file with controlled vocabulary headers  
       - drop duplicates of SiteNativeID, SiteName, SiteTypeCV   
       - drop data if missing latitude/longitude       
       - generate WaterSourceUUID (Prepend "CODWR" with WaterSourceNativeID
       - drop data if missing WaDESiteUUID, SiteName, CoordinateMethodCV, GNISCodeCV, EPSGCodeCV
       - copy results into **watersources.csv** and export 
 
 
   #### Sample data (all columns not included):
   
   WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV|
   ------------ | ------------ | -------- | ---------- | ---- |
   CODWR_1| 1 | SOUTH PLATTE RIVER | Unknown| Unspecified|

Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**sites_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data. 
  Mandatory fields include: 
 - SiteUUID 
 - SiteName 
 - CoordinateMethodCV 
 - EPSGCodeCV
 
 



##  3. waterallocations.py - generate master sheet of water allocations to import into WaDE 2.0
 Table Required: **DWR_Water_Right_-_Net_Amounts.csv** (Master Table containing Colorado Water Right Net Amount information) from [Colorado Information Marketplace](https://data.colorado.gov/Water/DWR-Water-Right-Net-Amounts/acsg-f33s))

Supplemental Script required:
**beneficialuseDictionary.py**
-Includes the following code dictionaries for Colorado: Beneficial Use, Allocation Legal Status, Allocation Type CV, and Water Source Type CV.

       - generate empty waterallocations.csv file with controlled vocabulary headers
       - generate SiteUUID (Prepend CODWR to NativeSiteID)       
       - call beneficialuseDictionary.py and assign defined beneficial uses to water right 
       - call watersources.csv and look up the WaterSourceUUID based on the "WaterSource" value
       - assign NativeAllocationID by concatenating the three values of these fields with a “-” between them (Admin No, Order          No, Decreed Units)       
       - drop data if OrganizationUUID, VariableSpecificUUID, WaterSourceUUID, MethodUUID, and AllocationPriorityDate are null
       - copy results into **waterallocations.csv** and export


####  Sample data (all columns not included):
   
   OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseCategory | AllocationNativeID | AllocationTypeCV | AllocationOwner | AllocationLegalStatusCV | AllocationAmount | 
   ---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- |------|
 CODWR | CODWR_100501 |CODWR_1| IRRIGATION,RECREATION,FISHERY |20543.0-0-C| |EMPIRE DITCH|Absolute | 612.48| 


Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**sites_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data.
Mandatory fields include: 
 - SiteUUID 
 - SiteName 
 - CoordinateMethodCV
 - EPSGCodeCV
 
 
 


### 4. variables.py - generate legend of granular variables specific to each state
        - all values are hard-coded according to state


#### Sample data (all columns not included):
   
   VariableSpecificUUID | VariableSpecificCV | VariableCV| AggregationStatisticCV | AggregationInterval| AggregationIntervalUnitCV| ReportYearStartMonth | ReportYearTypeCV| AmountUnitCV| MaximumAmountUnitCV|
   ---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- |----|-------|
  CODWR Allocation All | Allocation All | Allocation| Average | 1 |Day| 11|Irrigation|CFS|AFY|
  
  Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**sites_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data.
Mandatory fields include: 
 - SiteUUID 
 - SiteName 
 - CoordinateMethodCV
 - EPSGCodeCV
   

### 5. methods.py - generate legend of granular variables specific to each state detailing water right/allocation/etc data collection.
       - all values are hard-coded according to state
       
#### Sample data (all columns not included):
   
   MethodUUID | MethodName | MethodDescription| MethodNEMLink | ApplicableResourceTypeCV | MethodTypeCV| DataCoverageValue | DataQualityValueCV | DataConfidenceValue|
   ---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- | --------|
  CODWR_DiversionTracking| DiversionTracking | Methodology used for tracking diversions in the state of Colorado|  | Allocation | Water Withdrawals|      |         |        |

Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**sites_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data.
Mandatory fields include: 
 - SiteUUID 
 - SiteName 
 - CoordinateMethodCV
 - EPSGCodeCV
 
 
   
 
