# Water Rights (Allocations) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting Montana water rights data, made available by the [Montana Department of Natural Resources and Conservation (MTDNRC)](http://nris.mt.gov/dnrc/waterrights/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.

### Overview 
The MTDNRC hosts its water right data online at: http://wrqs.dnrc.mt.gov/default.aspx. 

The metadata for the water rights data is available at: http://wrqs.dnrc.mt.gov/WRKey.aspx

In addition, MTDNRC also hosts its water right data using ArcGIS online at (**accessing this requires credentials**): https://gis.dnrc.mt.gov/arcgis/rest/services/WRD/WRD_WaDE/MapServer.

All data services are available from (**accessing this requires credentials**): https://gis.dnrc.mt.gov/arcgis/rest/services.

### Summary
This document summarizes the process to prepare and share MTDNRC’s Water Rights data for inclusion into the WSWC’s Water Data Exchange (WaDE 2.0) project.  Input files are taken directly from the [MTDNRC website]( http://nris.mt.gov/dnrc/waterrights/).  In order to extract the MTDNRC’s water rights data from the input files and publish it online through ESRI layers so that it can be ready for WaDE 2.0, five separate Python scripts to generate CSV specific data (Step 1), and three manual created CSV files (Step 2), need to be executed so that the data will be compatible with WaDE 2.0.


# Step 1: Execute Python Scripts to Generate CSV Data Compatible with WaDE 2.0.
The following scripts use queries to extract MTDNRC water use data into views compatible with WaDE 2.0 (see list below for name of each script).  The scripts are further divided into two categories: 1) scripts to prepare the csv files for WaDE 2.0, 2) and dependency scripts.

**Scripts to Prepare the CSV Files for WaDE 2.0**
- #1. sites_MT.ipynb
- #2. watersources_MT.ipynb
- #3. waterallocations_MT.ipynb

**Dependency Scripts**
- beneficialuseDictionary.py
- utilityFunctions.py

The order in which scripts are operated is important as some act as inputs into others.  The recommended order is that laid out here.

The **beneficialuseDictionary.py** dependency script holds dictionaries that are required for mapping different codes to their respective names, for example codes for the purpose of water use.  The **utilityFunctions.py** dependency script holds functions that are required to be called from other scripts **watersources_MT.ipynb**, **sites_MT.ipynb**, and **waterallocations_MT.ipynb**.  

All scripts can be found at the WaDE’s Github repository [MappingStatesDataToWaDE2.0 in the Montana folder](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Montana).


## 1-1. sites_MT.ipynb
Purpose: generate a list of sites where water is allocated.

Dependency:  the output **sites.csv** file is an input to the **waterallocations_MT.ipnb**.

Supplemental Scripts Required:
- **utilityFunctions.py**
   - Generate empty **sites.csv** file with controlled vocabulary headers.
   - Assign SiteNativeID from PODID.
   - Generate WaDESiteUUID.
   - Project X and Y coordinates to latitude and longitude.
   - Map Site name and Site type from Ditch name and Means of diversion.
   - Copy results into **sites.csv** and export.
 
#### Input: 
- **WaterRights_Diversion.csv**.  Points of diversions table containing Montana water rights data together with site information for water sources.

#### Sample Data (Note: not all fields shown):
WaDESiteUUID | SiteNativeID | SiteName   | SiteTypeCV | Long | Lat | EPSGCodeCV
------------ | ------------ | ---------- | ---------- | ---- | --- | ----------
MT_26        | 1            | RODY DITCH | DITCH      |      |     | EPSG:4326 						

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate CSV file (e.g. **sites_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **sites_MT.ipynb** include the following:
- SiteUUID 
- SiteName
- CoordinateMethodCV 
- EPSGCodeCV


## 1-2. watersources_MT.ipynb
Purpose: generate list of water sources from which water is allocated from.

Dependency:  the output **watersources.csv** file is an input to the **waterallocations_MT.ipnb**.

Supplemental Scripts Required:
- **beneficialuseDictionary.py**.  Includes Beneficial Use and Allocation Legal Status dictionaries for Montana.
- **utilityFunctions.py**
   - Generate empty **waterSources.csv** file with controlled vocabulary headers.
   - Map water source name from input table.
   - Map Water Source Types from input table.
   - Generate WaterSourceNativeID.
   - Generate WaterSourceUUID.
   - Drop data if missing WaterSourceUUID, WaterSourceTypeCV, and WaterQualityIndicatorCV.
   - Copy results into **watersources.csv** and export.

#### Input: 
- **WaterRights_Simple.csv**.  A sample water rights table downloaded from the public water data search engine at: http://wrqs.dnrc.mt.gov/default.aspx.    

#### Sample Data (Note: not all fields shown):   
WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV
--------------- | ------------------- | --------------- | ----------------- | ----------------------- 
MT_14            | 14            | CHAMBERLAIN CREEK    | Ground           | Fresh

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate CSV file (e.g. **watersources_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **watersources_MT.ipynb** include the following:
- WaterSourceUUID
- WaterSourceTypeCV
- WaterQualityIndicatorCV


## 1-3. waterallocations_MT.ipynb
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

Dependency:  None

Supplemental Scripts Required:
- **beneficialuseDictionary.py**.  Includes Beneficial Use and Allocation Legal Status dictionaries for Montana.
- **utilityFunctions.py**.
   - Generate empty **waterAllocations.csv** file with controlled vocabulary headers.
   - Reference **sites.csv** to map the respective SiteUUID for sites (points of diversion) to water right table based on PODID.
   - Map WaterSourceUUID from watersources.csv based on Source type and Source name.
   - Map Beneficial Uses and Allocation legal status from the respective dictionaries.
   - Assign AllocationOwner based on Company OR FirstName / LastName.
   - Parse Allocation start and end time frame strings to fit WaDE2 specification.
   - Assign allocation native ID from WRNUMBER.
   - Map Allocation amount and Allocation acreage.
   - Drop data if both AllocationAmount and AllocationMaximum are null.
   - Copy results into **waterallocations.csv** and export.

#### Input: 
 - **WaterRights_Simple.csv**.  A sample water rights table downloaded from the public water data search engine at: http://wrqs.dnrc.mt.gov/default.aspx.

#### Sample Data (Note: not all fields shown):      
OrganizationUUID | AllocationNativeID | BeneficialUseCategory | AllocationLegalStatusCV | AllocationOwner    
---------------- | ------------------ | --------------------- | ----------------------- | --------------- 
MTDNRC           | 38H 102244 00      | STOCK                 | ACTIVE                  | USA (DEPT OF INTERIOR BUREAU OF LAND MGMT)

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate CSV file (e.g. **allocations_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **waterallocations_MT.ipynb** include the following:
- OrganizationUUID
- VariableSpecificUUID
- WaterSourceUUID
- MethodUUID
- AllocationPriorityDate



# Step 2: Manually Modify Existing Files to Generate MT CSV Data Compatible with WaDE 2.0.
The following is a quick description of four CSV files manually created by hand to be used as inputs into WaDE 2.0.  These values were derived from the [MTDNRC website](http://nris.mt.gov/dnrc/waterrights/) by manual inspection.


## 2-1. variables.csv
Purpose: generate legend of granular variables specific to each state.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
 - See the below prepared table (not all values shown).
   
VariableSpecificUUID | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV | MaximumAmountUnitCV
-------------------- | ---------- | -------- | ---------- | ----------- | ---------- | ----------- | --------- |----
 MTDNRC Allocation all | Allocation | Average| 1 | Year |10| WaterYear| CFS|AF|
  

## 2-2. methods.csv 
Purpose: generate legend of granular variables specific to each state detailing water right/allocation/etc data collection.

Dependency:  None

Supplemental Scripts Required:  None

#### Inputs:
 - See the below prepared table (not all values shown).
   
MethodUUID | MethodName | MethodDescription| MethodNEMLink | MethodTypeCV
---------- | ---------  | ---------------- | ------------- | ------------
MTDNRC-Water Rights Water Allocation | Montana Water Rights| Water Rights | http://wrqs.dnrc.mt.gov/default.aspx | Adjudicated
 
   
## 2-3. organizations.csv
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

Dependency:  None

Supplemental Scripts Required:  None
  
#### Inputs:
 - See the below prepared table (not all values shown).
   
 OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite 
 ---------------- | ---------------- | ------------------ | -------------------  
MTDNRC           | Montana Department of Natural Resources and Conservation    | A water right allows you to legally use water in a prescribed manner, but not to own the water itself. Without diversion and beneficial use, there is no water right. | http://nris.mt.gov/dnrc/waterrights/
