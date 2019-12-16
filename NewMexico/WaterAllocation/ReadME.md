# Water Rights (Allocations) Data Preparation for WaDE

This readme details an overview, the specific steps taken, and the final product of the process applied to water rights data made available by the [New Mexico Office of the State Engineer NMOSE](http://geospatialdata-ose.opendata.arcgis.com/datasets/ose-points-of-diversion) for inclusion into the Water Data Exchange (WaDE). For more information on WaDE, please visit http://wade.westernstateswater.org/

### Overview 
The New Mexico Office of the State Engineer hosts its water right data using ArcGIS online at: http://geospatialdata-ose.opendata.arcgis.com/datasets/ose-points-of-diversion. The metadata are available from: http://www.ose.state.nm.us/GIS/PODS/nmose_WATERS_PODs_data_dictionary_v8.xlsx 

### Summary
This document summarizes the process to prepare and share NMOSE’s Water Rights data for inclusion in the Western States Water Council’s Water Data Exchange (WaDE 2.0). In order to extract the New Mexico water rights data from the input files and publish it online through ESRI layers to be ready for WaDE 2.0, you must execute 8 Python Scripts to generate CSV data compatible with WaDE 2.0.
 
 ## Data Prep
 ### Step 1: Execute 8 Python Notebooks to generate CSV data compatible with WaDE 2.0

There are 8 Python scripts that use queries to extract NMOSE’s water rights data into views compatible with WaDE 2.0. The **beneficialuseDictionary.py** holds dictionaries that are required for mapping different codes to their respective names, for example codes for the legal status of allocations. The **utilityFunctions.py**, holds functions that are required to be called from other scripts **watersources_NM.ipynb**, **sites_NM.ipynb**, and **waterallocations_NM.ipynb**.  All scripts can be found at the following link in WaDE’s Github repository “MappingStatesDataToWaDE2.0” in the New Mexico folder:
https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/NewMexico

The 8 Scripts are are thus divided into two:

**1. Scripts to prepare the csv files**
- **sites_NM.ipynb**
- **watersources_NM.ipynb**
- **waterallocations_NM.ipynb**
- **methods_NM.ipynb**
- **organizations_NM.ipynb**
- **variables_NM.ipynb**

**2. Dependency scripts**
- **beneficialuseDictionary.py**
- **utilityFunctions.py**



##  1.  sites_NM.ipynb - generate a list of sites where water is allocated
 Input Table: 
 **OSE_Points_of_Diversion.csv** (Points of diversions table containing New Mexico Water Rights data together with site information for for water sources).

Supplemental Script required:
**utilityFunctions.py**

        - generate empty sites.csv file with controlled vocabulary headers
        - assign SiteNativeID from OBJECTID
        - generate WaDESiteUUID
        - Project UTM coordimates to latitude and longitude 
        - drop data if missing latitude/longitude
        - copy results into **sites.csv** and export


#### Sample data (all columns not included):

   WaDESiteUUID | SiteNativeID | SiteTypeCV | Long | Lat
   ------------ | ------------ | ---------- | ---- | ----
   NM_1 | 928 |Groundwater | -107.8822397 |35.16272037

Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**sites_mandatoryFieldMissing.csv**) for possible future inspection.
  Mandatory fields include: 
 - SiteUUID 
 - SiteName
 - CoordinateMethodCV 
 - EPSGCodeCV

sites.csv is input to waterallocations_NM.ipnb.


##  2. watersources_NM.ipynb - generate list of water sources from which water is allocated from
Table required:
**OSE_Points_of_Diversion.csv** (Points of diversions table containing New Mexico Water Rights data together with site information for for water sources).    

Supplemental Script required:
**beneficialuseDictionary.py**
 -Includes the following code dictionaries for New Mexico: Beneficial Use, Allocation Legal Status, Groundwater source type, Coordinate method type, and Coordinate method accuracy. 
 
Supplemental Script required 2:
**utilityFunctions.py**

       - generate empty waterSources.csv file with controlled vocabulary headers  
       - assign defined Water Source Types 
       - generate WaterSourceNativeID 
       - generate WaterSourceUUID 
       - drop data if missing WaterSourceUUID, WaterSourceTypeCV, and WaterQualityIndicatorCV
       - copy results into **watersources.csv** and export 
 
  waterSources.csv is input to waterallocations_NM.ipnb.


   #### Sample data (all columns not included):
   
   WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV
   ------------ | ------------ | -------- | ---------- | ---- 
   NM_1 | 1 | Unspecificed | Unknown | Fresh

Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**watersources_mandatoryFieldMissing.csv**) for future inspection. 
  Mandatory fields include: 
 - WaterSourceUUID
 - WaterSourceTypeCV
 - WaterQualityIndicatorCV


##  3. waterallocations_NM.ipynb - generate master sheet of water allocations to import into WaDE 2.0
**OSE_Points_of_Diversion.csv** (Points of diversions table containing New Mexico Water Rights data together with site information for for water sources).    

Supplemental Script required:
**beneficialuseDictionary.py**
 -Includes the following code dictionaries for New Mexico: Beneficial Use, Allocation Legal Status, Groundwater source type, Coordinate method type, and Coordinate method accuracy. 
 
Supplemental Script required 2:
**utilityFunctions.py**

       - generate empty waterAllocations.csv file with controlled vocabulary headers
       - call functions from utilityFunctions.py referencing the repective dictionaries to assign defined Beneficial Use, Allocation   
         Legal Status, Groundwater source type, Coordinate method type, and Coordinate method accuracy to water right 
       - reference waterSources.csv and assign WaDE prepared water sources to water right
       - reference sites.csv to map the respective sites (points of diversion) to water right
       - assign AllocationOwner based on Company OR FirstName/LastName
       - drop data if AllocationAmount and Allocation Maximum are null
       - copy results into **UTWaterAllocations.csv** and export
        


####  Sample data (all columns not included):
   
   OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseCategory | AllocationNativeID | AllocationOwner | AllocationLegalStatusCV   
   ---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- 
  NMOSE| NM_32| NM_1   | 72-12-1 livestock watering | 43 |MHEALY, EDMUND | Permit |

Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**allocations_mandatoryFieldMissing.csv**) for future inspection.
Mandatory fields include: 
 - OrganizationUUID
 - VariableSpecificUUID
 - WaterSourceUUID
 - MethodUUID
 - AllocationPriorityDate
 
 

 
### 4. variables_NM.ipynb - generate legend of granular variables specific to each state
        - all values are hard-coded according to state


#### Sample data (all columns not included):
   
   VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV | MaximumAmountUnitCV
   ---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- |----|
  Allocation All | Allocation | Average| 1 | Year |10| WaterYear| CFS|AF|
  
   MethodUUID	MethodName	MethodDescription	MethodNEMILink	ApplicableResourceTypeCV	MethodTypeCV
	Water Allocation				Adjudicated

  
### 5. methods_NM.ipynb - generate legend of granular variables specific to each state detailing water right/allocation/etc data collection.
       - all values are hard-coded according to state
       
#### Sample data (all columns not included):
   
   MethodUUID | MethodName | MethodDescription| MethodNEMLink | 
   ---------------- | ------------ | -------- | ---------- | 
  NM_WaterAllocation| Water Allocation | Water Rights| http://geospatialdata-ose.opendata.arcgis.com/search?groupIds=fabf18d6e0634ae38c86475c9ada6498 | 
 
  
  ### 6. Organizations_NM.ipynb - generate organization directory, including names, email addresses, and website hyper links for organization suppyling data source
  
        -All variables are hardcoded according to organization.
        
 #### Sample data (all columns not included):
   
   OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite |
   ---------------- | ------------ | -------- | ---------- | 
  NMOSE | 	New Mexico Office of the State Engineer | The New Mexico Office of the State Engineer (OSE) provides this geographic data and any associated metadata “as is” without warranty of any kind | https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/NewMexico |

