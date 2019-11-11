# WaDE Preparation

This readme details an overview, the specific steps taken, and the final product of the process applied to water rights data made available by the [Utah Division of Water Rights (UTDWR)](https://www.waterrights.utah.gov/contact.asp) for inclusion into the Water Data Exchange (WaDE). 

### Overview 
The Utah Division of Water Rights hosts its water right data at the [PUBDUMP Database table dump Utility](https://www.waterrights.utah.gov/cgi-bin/pubdump.exe?DBNAME=WRDB&SECURITYKEY=wrt2012access).
The dataset is updated annually. For more information on WaDE, please visit http://wade.westernstateswater.org/


### Summary
This document summarizes the process to prepare and share UTDWR’s Water Rights data from the PUBDUMP database for inclusion in the Western States Water Council’s Water Data Exchange (WaDE 2.0). In order to extract Utah water rights data from the PUBDUMP database and publish it online through ESRI layers to be ready for WaDE 2.0, you must execute 8 Python Scripts to generate CSV data compatible with WaDE 2.0.
 
 ## Data Prep
 ### Step 1: Execute 8 Python Scripts to generate CSV data compatible with WaDE 2.0

There are 8 Python Scripts that use queries to extract UTDWR’s water rights data into views compatible with WaDE 2.0. Two of the scripts, beneficialuseDictionary.py and waterallocationsFunctions.py, are required as input scripts for watersources_Ut.py and waterallocations_UT.py, respectively.  All scripts can be found at the following link in WaDE’s Github repository “MappingStatesDataToWaDE2.0” in the Utah folder:
https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Utah


The overall objective of the data migration scripts are to prepare datasets retrieved from state repositories for upload into WaDE 2.0.  This process applied to Utah Water Rights data, and considering the data included in this dataset involves passing the raw data through eight Python scripts. These scripts are outlined below.

The 8 Scripts are entitled:
- sites_UT.py
- watersources_UT.py
   - beneficialuseDictionary.py
- waterallocations_UT.py
   - waterallocationsFunctions.py
-  methods_UT.py
-  organizations_UT.py
-  variables_UT.py




##  1.  sites_UT.py - generate a list of sites where water is allocated
### Table Required: Water_Master.csv (Master Table containing Utah Water Right and Exchange Information) 

- generate empty sites.csv file with controlled vocabulary headers
- assign SiteNativeID from RECORD_ID
- generate WaDESiteUUID (Concatenate UT with SiteNativeID)
- drop data if missing latitude/longitude
- copy results into sites.csv and export

Sample data (all columns not included):

   WaDESiteUUID | SiteNativeID | SiteTypeCV | Long | Lat
   ------------ | ------------ | ---------- | ---- | ----
   UTDWRE_177983 | 177983 |U | 431092.606 |4616232.618
     
##  2. watersources_UT.py - generate list of water sources from which water is allocated from
### Table Required: Water_Master.csv (Master Table containing Utah Water Right and Exchange Information)     

- generate empty watersources.csv file with controlled vocabulary headers
- generate WaterSourceNativeID (Wyoming POD data does not include native ID)
- generate WaterSourceUUID from generate WaterSourceNativeID
- drop data if missing WaterSourceUUID, WaterSourceType, AND WaterQualityIndicator
- copy results into watersources.csv and export
        
   Sample data (all columns not included):
   
   WaterSourceUUID | WaterSourceID | WaterSource | WaterSourceTypeCV | WaterQualityIndicatorCV
   ------------ | ------------ | -------- | ---------- | ---- 
   WWDO_1 | 1 | LARAMIE RIVER  | Unknown | Unspecified 
        
###  3. waterallocations_WY.py - generate master sheet of water allocations to import into WaDE
        - generate empty waterallocations.csv file with controlled vocabulary headers
        - call sites.csv and assign WaDE prepared sites to water right 
        - call Dictionaries_WY.py and assign defined benefical uses to water right 
        - call watersources.csv and assign WaDE prepared water sources to water right
        - assign AllocationOwner based on Company OR FirstName/LastName
        - copy data to waterallocation.csv
        - drop data if AllocationAmount AND AllocationMaximum are null
        - export to csv
        
  Sample data (all columns not included):
   
   OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseID | NativeAllocationID | AllocationOwner | AllocationLegalStatus | AllocationAmount | 
   ---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- 
   WWDO | WWDO_100001 | WWDO_1 | IRRIGATION | CR CC48/006 | JOHN DOE IRRIGATION | FullyAdjudicated | 71.43


Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file to be passed back to the data supplier. 
