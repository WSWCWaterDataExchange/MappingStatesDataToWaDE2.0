# Water Rights (Allocations) Data Preparation for WaDE

This readme details an overview, the specific steps taken, and the final product of the process applied to water rights data made available by the [Montana Department of Natural Resources and Conservation MTDNRC](http://nris.mt.gov/dnrc/waterrights/) for inclusion into the Water Data Exchange (WaDE). For more information on WaDE, please visit http://wade.westernstateswater.org/

### Overview 
The Montana Department of Natural Resources and Conservation MTDNRC hosts its water right data using ArcGIS online at (accessing this requies credentials): https://gis.dnrc.mt.gov/arcgis/rest/services/WRD/WRD_WaDE/MapServer. All data services are available from (also credential required to access): https://gis.dnrc.mt.gov/arcgis/rest/services. The publicly available data are can be accessed from: http://wrqs.dnrc.mt.gov/default.aspx. Explanation of terms/codes in the water rights data such as water rights ID, purpose of use, and status are provided at: http://wrqs.dnrc.mt.gov/WRKey.aspx

### Summary
This document summarizes the process to prepare and share MTDNRC’s Water Rights data for inclusion in the Western States Water Council’s Water Data Exchange (WaDE 2.0). In order to extract the data from the input files and publish it online through ESRI layers to be ready for WaDE 2.0, you must generate CSV data compatible with WaDE 2.0. Some of these are small files with only few rows and can be prepared by manualy modifying existing csv files for other states. The water sources, sites, and water allocations tables are prepared by executing the (Python) Jupyter notebook codes described below.
 
 ## Data Prep
 ### Step 1: Execute 8 Python Notebooks to generate CSV data compatible with WaDE 2.0

There are 3 Jupyter notebook scripts and one Python script that use queries to extract MTDNRC’s water use data into views compatible with WaDE 2.0. The **beneficialuseDictionary.py** holds dictionaries that are required for mapping different codes to their respective names, for example codes for the purpose of water use. The **utilityFunctions.py** holds functions that are required to be called from other scripts **watersources_MT.ipynb**, **sites_MT.ipynb**, and **waterallocations_MT.ipynb**.  All scripts can be found at the following link in WaDE’s Github repository “MappingStatesDataToWaDE2.0” in the Montana folder:
https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Montana

The Python notebooks and Scripts are thus divided into two:

**1. Scripts to prepare the csv files for WaDE 2**
- **sites_MT.ipynb**
- **watersources_MT.ipynb**
- **waterallocations_MT.ipynb**

**2. Dependency scripts**
- **beneficialuseDictionary.py**
- **utilityFunctions.py**


##  1.  sites_MT.ipynb - generate a list of sites where water is allocated
 Input Table (**sample**): 
 **WaterRights_Diversion.csv** (Points of diversions table containing Montana Water Rights data together with site information for for water sources).

Supplemental Script required:
**utilityFunctions.py**

        - generate empty sites.csv file with controlled vocabulary headers
        - assign SiteNativeID from PODID
        - generate WaDESiteUUID
        - Project X and Y coordinates to latitude and longitude 
        - map Site name and Site type from Ditch name and Means of diversion
        - copy results into **sites.csv** and export


#### Sample data (all columns not included):

   WaDESiteUUID | SiteNativeID | SiteName   | SiteTypeCV | Long | Lat | EPSGCodeCV
   ------------ | ------------ | ---------- | ---------- | ---- | --- | ----------
   MT_26        | 1            | RODY DITCH | DITCH      |      |     | EPSG:4326 								

Any data row missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**sites_mandatoryFieldMissing.csv**) for possible future inspection.
  Mandatory fields include: 
 - SiteUUID 
 - SiteName
 - CoordinateMethodCV 
 - EPSGCodeCV

sites.csv is input to waterallocations_MT.ipnb.


##  2. watersources_MT.ipynb - generate list of water sources from which water is allocated from
Table required (**Sample**):
**WaterRights_Simple.csv** (A sample water rights table downloaded from the public water data search engine at: http://wrqs.dnrc.mt.gov/default.aspx).    

Supplemental Script required:
**beneficialuseDictionary.py**
 -Includes Beneficial Use and Allocation Legal Status dictionaries for Montana. 
 
Supplemental Script required 2:
**utilityFunctions.py**

       - generate empty waterSources.csv file with controlled vocabulary headers  
       - map water source name from input table
       - map Water Source Types from input table
       - generate WaterSourceNativeID 
       - generate WaterSourceUUID 
       - drop data if missing WaterSourceUUID, WaterSourceTypeCV, and WaterQualityIndicatorCV
       - copy results into **watersources.csv** and export 
 
  waterSources.csv is input to waterallocations_MT.ipnb.

   #### Sample data (all columns not included):
   
   WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV
   --------------- | ------------------- | --------------- | ----------------- | ----------------------- 
   MT_14            | 14            | CHAMBERLAIN CREEK    | Ground           | Fresh

Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**watersources_mandatoryFieldMissing.csv**) for future inspection. 
Mandatory fields include: 
 - WaterSourceUUID
 - WaterSourceTypeCV
 - WaterQualityIndicatorCV


##  3. waterallocations_MT.ipynb - generate master sheet of water allocations to import into WaDE 2.0
Table required (**Sample**):
**WaterRights_Simple.csv** (A sample water rights table downloaded from the public water data search engine at: http://wrqs.dnrc.mt.gov/default.aspx).      

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
