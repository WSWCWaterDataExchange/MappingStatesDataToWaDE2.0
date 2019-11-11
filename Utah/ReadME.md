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
 Table Required: **Water_Master.csv** (Master Table containing Utah Water Right and Exchange Information on PUBDUMP) 

- generate empty sites.csv file with controlled vocabulary headers
- assign SiteNativeID from RECORD_ID
- generate WaDESiteUUID (Concatenate UT with SiteNativeID)
- drop data if missing latitude/longitude
- copy results into sites.csv and export



Sample data (all columns not included):

   WaDESiteUUID | SiteNativeID | SiteTypeCV | Long | Lat
   ------------ | ------------ | ---------- | ---- | ----
   UTDWRE_177983 | 177983 |U | 431092.606 |4616232.618

Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**sites_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data.
Mandatory fields include: 
- SiteUUID 
- SiteName
- CoordinateMethodCV 
- EPSGCodeCV



##  2. watersources_UT.py - generate list of water sources from which water is allocated from
Tables required:
**Water_Master.csv** (Master Table containing Utah Water Right and Exchange Information from PUBDUMP) and **PointofDiversionTable.csv** (Water Rights, Change, and Exchange Point of Diversion Table from PUBDUMP)    

Supplemental Script required:
**beneficialuseDictionary.py**
 -Includes the following code dictionaries for Utah: Beneficial Use, Allocation Legal Status, Allocation Type CV, Water Source Type CV, and Site Type. 

 - generate empty UTWaterSources.csv file with controlled vocabulary headers  
 - call beneficialUseDictionary.py and assign defined Water Source Types to their respective codes
 - generate WaterSourceNativeID 
 - generate WaterSourceUUID (Concatenate UT with WaterSourceNativeID)
 - drop data if missing WaterSourceUUID, WaterSourceTypeCV, and WaterQualityIndicatorCV
 - copy results into **UTWaterSources.csv** and export 
**UTWaterSources.csv is input to waterallocations_UT.py.**

   Sample data (all columns not included):
   
   WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV
   ------------ | ------------ | -------- | ---------- | ---- 
   UT_1 | 1 | Underground Water Well  | groundwaterall | Fresh

Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**sites_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data. 
Mandatory fields include: 
- SiteUUID 
- SiteName 
- CoordinateMethodCV 
- EPSGCodeCV






##  3. waterallocations_UT.py - generate master sheet of water allocations to import into WaDE 2.0
Table Required: **Water_Master.csv** (Master Table containing Utah Water Right and Exchange Information on PUBDUMP) 

Supplemental Script required:
**waterallocationFunctions.py**

 - generate empty UTWaterAllocations.csv file with controlled vocabulary headers
 - call waterallocationFunctions.py and assign defined beneficial uses to water right 
 - call UTWaterSources.csv and assign WaDE prepared water sources to water right
 - assign AllocationOwner based on Company OR FirstName/LastName
 - drop data if AllocationAmount and Allocation Maximum are null
 - copy results into **UTWaterAllocations.csv** and export
        


  Sample data (all columns not included):
   
   OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseCategory | AllocationNativeID | AllocationTypeCV | AllocationOwner | AllocationLegalStatusCV | AllocationAmount | 
   ---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- |------|
  UTDWRE | UTDWRE_72714 | UTDWRE_2 | Irrigation, Stockwatering | 61-2981 |Underground Water Claim| Morgan Ranches, LLC | Certificated | 0.4223| 


Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (sites_mandatoryFieldMissing.csv) to be passed back to the organization supplying the data.
Mandatory fields include: 
- SiteUUID 
- SiteName 
- CoordinateMethodCV
- EPSGCodeCV
