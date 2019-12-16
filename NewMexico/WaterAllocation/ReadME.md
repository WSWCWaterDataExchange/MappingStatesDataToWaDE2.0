# Water Rights (Allocations) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting New Mexico water rights data, made available by the [New Mexico Office of the State Engineer (NMOSE)](http://geospatialdata-ose.opendata.arcgis.com/datasets/ose-points-of-diversion), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.

## Overview 
The NMOSE hosts its water rights data using ArcGIS online at: http://geospatialdata-ose.opendata.arcgis.com/datasets/ose-points-of-diversion.

The metadata for the water rights data is available at: http://www.ose.state.nm.us/GIS/PODS/nmose_WATERS_PODs_data_dictionary_v8.xlsx.

Python scripts described here for inclusion into WaDE are operated using [Jupyter Notebooks](https://jupyter.org/).

## Summary
This document summarizes the process to prepare and share NMOSE’s Water Rights data for inclusion into the WSWC’s Water Data Exchange (WaDE 2.0) project.  Input files are taken directly from the [NMOSE](http://geospatialdata-ose.opendata.arcgis.com/datasets/ose-points-of-diversion) website.  In order to extract the NMOSE water rights data from the input files and publish it online through ESRI layers so that it can be ready for WaDE 2.0, eight separate Python scripts to generate CSV specific data need to be executed so that the data will be compatible with WaDE 2.0.
 
The following Python scripts use queries to extract NMOSE’s water rights data into WaDE 2.0 (see below list for names of each script).  Those Python scripts are further divided into two categories: scripts that prepare CSV files **(6)** which need to be ran in the provide order, and dependency scripts **(2)** which hold useful information but do not need to be operated.  The NMOSE extraction scripts are as follows

**Scripts to prepare the CSV files (must run these)**
-	**#1. sites_NM.ipynb**
-	**#2. watersources_NM.ipynb**
-	**#3. variables_NM.ipynb**
-	**#4. methods_NM.ipynb**
-	**#5. organizations_NM.ipynb**
-	**#6. waterallocations_NM.ipynb**

**Dependency Scripts**
 - **beneficialuseDictionary.py**
 - **utilityFunctions.py**

The order in which scripts are operated is important as the **waterallocations_NM.ipynb** script is dependet on inputs from the others.  The **beneficialuseDictionary.py** dependency script holds Python specific dictionaries that are required for mapping different codes to their respective names (e.g. codes for the legal status of allocations).  The **utilityFunctions.py** dependency script holds Python functions that are required for three of the scripts (e.g. **watersources_NM.ipynb**, **sites_NM.ipynb**, and **waterallocations_NM.ipynb**) to prepare the CSV files.

All scripts can be found in the WaDE’s Github repository [MappingStatesDataToWaDE2.0 in the New Mexico folder]( https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/NewMexico). 



# Python Script Information
The following is a quick description of the six Python scripts that prepare the CSV files, their purpose, their dependencies, how they relate to the dependency scripts, an example of their input tables, and mandatory fields required for creation. 

## 1. sites_NM.ipynb
Purpose: generate a list of sites where water is allocated.

Dependency: the output **sites.csv** file is an input to the **waterallocations_NM.ipnb**.

Supplemental Scripts Required:
- **utilityFunctions.py**
  - generate empty sites.csv file with controlled vocabulary headers
  - assign SiteNativeID from OBJECTID
  - generate WaDESiteUUID
  - Project UTM coordinates to latitude and longitude 
  - drop data if missing latitude/longitude
  - copy results into **sites.csv** and export

Input: **OSE_Points_of_Diversion.csv** (Points of diversions table containing New Mexico Water Rights data together with site information for water sources).

#### Sample Data (Note: not all fields shown):
WaDESiteUUID | SiteNativeID | SiteTypeCV | Long | Lat
------------ | ------------ | ---------- | ---- | ----
NM_1 | 928 |Groundwater | -107.8822397 |35.16272037

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **sites_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **sites_NM.ipynb** include the following: 
- SiteUUID 
- SiteName
- CoordinateMethodCV 
- EPSGCodeCV


## 2. watersources_NM.ipynb
Purpose: generate list of water sources from which water is allocated from.

Dependency: the output **waterSources.csv** is an input to the **waterallocations_NM.ipnb**.

Supplemental Scripts Required:
- **beneficialuseDictionary.py**
   - Includes the following code dictionaries for New Mexico: Beneficial Use, Allocation Legal Status, Groundwater source type, Coordinate method type, and Coordinate method accuracy.
- **utilityFunctions.py**
  - generate empty waterSources.csv file with controlled vocabulary headers  
  - assign defined Water Source Types 
  - generate WaterSourceNativeID 
  - generate WaterSourceUUID 
  - drop data if missing WaterSourceUUID, WaterSourceTypeCV, and WaterQualityIndicatorCV
  - copy results into **watersources.csv** and export

Input:  **OSE_Points_of_Diversion.csv** (Points of diversions table containing New Mexico Water Rights data together with site information for water sources).    

#### Sample Data (Note: not all fields shown):
WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV
------------ | ------------ | -------- | ---------- | ---- 
NM_1 | 1 | Unspecified | Unknown | Fresh

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **watersources_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **watersource_NM.ipynb** include the following: 
- WaterSourceUUID
- WaterSourceTypeCV
- WaterQualityIndicatorCV


## 3. variables_NM.ipynb
Purpose: generate legend of granular variables specific to each state

Dependency: None

Supplemental Scripts Required: None

All values for the **variables_NM.ipynb** are hard-coded according to state.

#### Sample Data (Note: not all fields shown):
VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV | MaximumAmountUnitCV
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- |----|
Allocation All | Allocation | Average| 1 | Year |10| WaterYear| CFS|AF| 


## 4. methods_NM.ipynb
Purpose: generate legend of granular variables specific to each state detailing water right/allocation/etc data collection.

Dependency: None

Supplemental Scripts Required: None

All values for the **methods _NM.ipynb** are hard-coded according to state.
       
#### Sample Data (Note: not all fields shown):
MethodUUID | MethodName | MethodDescription| MethodNEMLink | 
---------------- | ------------ | -------- | ---------- |
NM_WaterAllocation| Water Allocation | Water Rights| http://geospatialdata-ose.opendata.arcgis.com/search?groupIds=fabf18d6e0634ae38c86475c9ada6498 | 
 

### 5. Organizations_NM.ipynb
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source

Dependency: None

Supplemental Scripts Required: None

All values for the **Organizations_NM.ipynb** are hard-coded according to state.
        
#### Sample Data (Note: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite |
---------------- | ------------ | -------- | ---------- | 
NMOSE | 	New Mexico Office of the State Engineer | The New Mexico Office of the State Engineer (OSE) provides this geographic data and any associated metadata “as is” without warranty of any kind | https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/NewMexico |


## 6. waterallocations_NM.ipynb
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

Dependency: None

Supplemental Scripts Required:
- **beneficialuseDictionary.py**
  - Includes the following code dictionaries for New Mexico: Beneficial Use, Allocation Legal Status, Groundwater source type, Coordinate method type, and Coordinate method accuracy.
- **utilityFunctions.py**
  - generate empty waterAllocations.csv file with controlled vocabulary headers
  - call functions from utilityFunctions.py referencing the respective dictionaries to assign defined Beneficial Use, Allocation
  - Legal Status, Groundwater source type, Coordinate method type, and Coordinate method accuracy to water right
  - reference waterSources.csv and assign WaDE prepared water sources to water right
  - reference sites.csv to map the respective sites (points of diversion) to water right
  - assign AllocationOwner based on Company OR FirstName/LastName
  - drop data if AllocationAmount and Allocation Maximum are null
  - copy results into **waterallocations.csv** and export

Input: **OSE_Points_of_Diversion.csv** (Points of diversions table containing New Mexico Water Rights data together with site information for water sources).    

#### Sample Data (Note: not all fields shown):
OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseCategory | AllocationNativeID | AllocationOwner | AllocationLegalStatusCV   
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- 
NMOSE| NM_32| NM_1   | 72-12-1 livestock watering | 43 |MHEALY, EDMUND | Permit |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **allocations_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **waterallocations _NM.ipynb** include the following: 
- OrganizationUUID
- VariableSpecificUUID
- WaterSourceUUID
- MethodUUID
- AllocationPriorityDate

