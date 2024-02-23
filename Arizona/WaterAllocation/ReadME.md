# ADWR Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Arizona Department of Water Resources(ADWR)](http://gisdata-azwater.opendata.arcgis.com/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**SW QUERY BY SURFACE WATERSHEDS** | surface water right data (SW QUERY BY SURFACE WATERSHEDS).  Downloaded used all washed under the 'ACTIVE' status. | [link](https://www.azwater.gov/querycenter/query.aspx?qrysessionid=ABBBE0BF2A68326CE040000A16005CA1) | not provided
**Fillings** | location information related to the SW QUERY BY SURFACE WATERSHEDS data. | Provided by personal correspondence with ADWR via email. | not provided
**Well Registry** | groundwater water right data.  Contains use and location info. | [link](https://gisdata2016-11-18t150447874z-azwater.opendata.arcgis.com/datasets/34c92af536ec4047aeaf9d93053dc317_0/explore?location=34.103087%2C-111.970052%2C7.92) | not provided


## Storage for input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Arizona Allocation Data: https://drive.google.com/drive/folders/1PTvL2OH-po4MXKupardY0vJWhnLnG089


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *AZwr_SW_Allocation Schema Mapping to WaDE.xlsx* & *AZwr_GW_Allocation Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_AZwr_PreProcessAllocationData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_AZwr_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv.
- **3_AZwr_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_AZwr_PreProcessAllocationData.ipynb
Purpose: Pre-process the state agency's input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - SW QUERY BY SURFACE WATERSHEDS
 - Fillings.shp
 - Well Registry

#### Outputs:
 - Pwr_azMain.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes for groundwater and surface water.  Processes outline consist of combining the two datasets into one workable dataframe. 
- Specific for surface water data...
    - Read in SW QUERY BY SURFACE WATERSHEDS csv files, concatenate into one long dataframe.
    - Clean **REG. NO'** field by removing excess 0 markers.  Used to match with **FILENO** in Fillings.shp input.
    - For amount data, separate value and unit info out from the **QUANTITY** field.
    - TEMP FIX: Drop the following unknown measurement of units for the following terms: 'ACRES', 'Amount Required for Maintenance', 'Feet', 'MIT - Miners Inches Total', 'Miners Inches Per Annum',  'XX - Unknown Code at Load time', 'None',  '',  " ".
    - Note unique unit of amounts as either CSF or AF.
    - Units with CFS include 'Cubic Feet Per Second', Acre-Feet Per Annum (converted to CFS by / 723.968), 'Gallons Per Annum' (converted to CFS by / 235905662.34).
    - Units with AF include 'Acre-Feet', 'Acre-Feet Total', 'CFT - Cubic Feet Total' (converted to AF by / 43559.9), 'Gallons' (converted to AF by / 325850.943).
    - Convert **X_UTMNAD83** and **Y_UTMNAD83** input fields to match WGS84 projection and create *latitude* and *longitude* values.
- Concatenate groundwater and surface water data into single output dataframe.
- For this ADWR, drop non-active AllocationLegalStatusCV values specific to: "INACTIVE - WITHDRAWN", "INACTIVE - CONSOLIDATED", "INACTIVE - AMENDED", "INACTIVE - CANCELLED", "INACTIVE - REJECTED", "INACTIVE - PARTIAL T&S", "INACTIVE - RELINQUISHED", "INACTIVE - FULL T&S", "INACTIVE - INACTIVE", "INACTIVE - FULL ASSIGNMENT", "INACTIVE - PARTIAL ASSIGNMENT"
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *Pwr_azMain.csv*.


***
## Code File: 2_AZwr_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv).

#### Inputs:
- Pwr_azMain.zip

#### Outputs:
- methods.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- variables.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- organizations.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- watersources.csv
- sites.csv
- waterallocations.csv
- podsitetopousiterelationships.csv


## 1) Method Information
Purpose: generate legend of granular methods used on data collection.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign state agency info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
AZwr_M1 | Groundwater | Adjudicated
AZwr_M2 | Surface Water | Adjudicated


## 2) Variables Information
Purpose: generate legend of granular variables specific to each state.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign state agency info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
AZwr_V1 | 1 | Year | CFS
AZwr_V2 | 1 | Year | AF


## 3) Organization Information
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign state agency info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
AZwr_O1 | Arizona Department of Water Resources| Lisa Williams | http://gisdata-azwater.opendata.arcgis.com/


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency data info to the *WaDE WaterSources* specific columns.  See *AZSWwr_Allocation Schema Mapping to WaDE.xlsx* & *AZGWwr_Allocation Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = Unspecified for gw, & **WATERSOURC** for sw.
    - *WaterSourceTypeCV* = *groundwater/well* for gw, & *Surface Water* for sw.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------
AZwr_WS2 | Fresh | 1.5 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


## 5) Site Information
Purpose: generate a list of sites where water is diverted (also known as Points Of Diversion, PODs).

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to the *WaDE Site* specific columns.  See *AZSWwr_Allocation Schema Mapping to WaDE.xlsx* & *AZGWwr_Allocation Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersource.csv input file. See code for specific implementation of extraction.
    - *County* = **COUNTY** for both gw and sw data.
    - *Latitude* = converted **UTM_Y_METE** projection from ADWR EPSG:2927 -to- WaDE EPSG:4326, see *1_AZwr_PreProcessAllocationData.ipynb* for details.
    - *Longitude* = converted **UTM_Y_METE**  to utm & dWGS84 projection, see *1_AZwr_PreProcessAllocationData.ipynb* for details.
    - *SiteNativeID* = **REGISTRY_I** for gw & **CADASTRAL** for sw, Unspecified if blank.
    - *SiteTypeCV* = **WELL_TYPE_** for gw & Unspecified for sw, Unspecified if blank.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteTypeCV*, *Longitude*, and *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
AZwr_S1 | AZwr_WS1 | Unspecified | 32.951858357839 | -111.814054446414 | 60000

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


## 6) AllocationsAmounts Information
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign state agency info to the *WaDE Water Allocations* specific columns.  See *AZSWwr_Allocation Schema Mapping to WaDE.xlsx* & *AZGWwr_Allocation Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* = **PUMPRATE** for gw, **QUANTITY** for sw, see *1_AZwr_PreProcessAllocationData.ipynb* for specifics.
    - *AllocationLegalStatusCV* = **STATUS_x** for sw.
    - *AllocationNativeID* = **REGISTRY_I** for gw & **FILE_NO** for sw.
    - *AllocationOwner* = **OWNER_NAME** for gw & **HLDRNAME** for sw.
    - *AllocationPriorityDate* = **PRIOR_DATE** for sw.
    - *AllocationLegalStatus* = **WELL_TYPE_** for gw.
    - *BeneficialUseCategory* = **WATER_USE** for gw & **REG. NO** for sw, see *1_AZwr_PreProcessAllocationData.ipynb* for specifics.
    - *IrrigatedAcreage* - **IrrigatedAreaQuantity**.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS  | BeneficialUseCategory
---------- | ---------- | ------------ 
200001 | 0 | Active | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- SiteUUID
- AllocationPriorityDate
- BeneficialUseCategory
- AllocationAmount or AllocationMaximum
- DataPublicationDate


### 7) POD Site -To- POU Polygon Relationships
Purpose: generate linking element between POD and POU sites that share the same water right.
Note: podsitetopousiterelationships.csv output only needed if both POD and POU data is present, ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `otherwise produces empty file.`

#### Operation and Steps:
- Read the sites.csv & waterallocations.csv input files.
- Create three temporary dataframes: one for waterallocations, & two for site info that will store POD and POU data separately.
- For the temporary POD dataframe...
  - Read in site.csv data from sites.csv with a _PODSiteUUID_ field = POD only.
  - Create _PODSiteUUID_ field = _SiteUUID_.
- For the temporary POU dataframe
  - Read in site.csv data from sites.csv with a _PODSiteUUID_ field = POU only.
  - Create _POUSiteUUID_ field = _SiteUUID_.
- For the temporary waterallocations dataframe, explode _SiteUUID_ field to create unique rows.
- Left-merge POD & POU dataframes to the waterallocations dataframe via _SiteUUID_ field.
- Consolidate waterallocations dataframe by grouping entries by _AllocationNativeID_ filed.
- Explode the consolidated waterallocations dataframe again using the _PODSiteUUID_ field, and again for the _POUSiteUUID_ field to create unique rows.
- Perform error check on waterallocations dataframe (check for NaN values)
- If waterallocations is not empty, export output dataframe _podsitetopousiterelationships.csv_.


***
## Source Data & WaDE Complied Data Assessment
The following info is from a data assessment evaluation of the completed data...

Dataset | Num of Source Entries (rows) | Num of Identified PODs | Num of Identified POUs | Num of Identified Water Right Records
---------- | ---------- | ------------ | ------------ | ------------
**Well Registry** | 229,051 | N/A | N/A  | N/A 
**SW QUERY BY SURFACE WATERSHEDS** | 256,140 | N/A  | N/A  | N/A 
**WaDE** | N/A | 156,411 | 35,791 | 267,304

Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
Unused WaterSource Record | 1,337 | Removed from watersource.csv
Dual County value provided | 1213 | Removed from sites.csv
Incomplete or bad entry for Latitude | 778 | Removed from sites.csv
Wrong value entry for Latitude | 409 | Removed from sites.csv
Too many ws records to a single site | 9 | Removed from waterallocation.csv
Too many sites applied to a single record | 16240 | Removed from waterallocation.csv
Dual AllocationPriorityDate value provided | 2632 | Removed from waterallocation.csv
Dual Flow provided / missing value | 1375 | Removed from waterallocation.csv
Incomplete or bad entry for VariableSpecificUUID | 1133 | Removed from waterallocation.csv
Dual Volume provided / missing value | 16 | Removed from waterallocation.csv

**Figure 1:** Distribution of POD vs POU Sites within the sites.csv
![](figures/PODorPOUSite.png)

**Figure 2:** Distribution Sites by WaterSourceTypeCV within the sites.csv
![](figures/WaterSourceTypeCV.png)

**Figure 3:** Distribution of Identified Water Right Records by WaDE Categorized Primary Beneficial Uses within the waterallocations.csv
![](figures/PrimaryBeneficialUseCategory.png)

**Figure 4:** Range of Priority Date of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationPriorityDate.png)

**Figure 5:** Distribution & Range of Flow (CFS) of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationFlow_CFS.png)

**Figure 6:** Distribution & Range of Volume (AF) of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationVolume_AF.png)

**Figure 7:** Map of Identified Points within the sites.csv
![](figures/PointMap.png)

**Figure 8:** Map of Identified Polygons within the sites.csv
- No geometry (polygon) data provided.
<!-- ![](figures/PolyMap.png) -->


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Arizona Department of Water Resources(ADWR)](http://gisdata-azwater.opendata.arcgis.com/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

ADWR Staff
- Lisa Williams <lmwilliams@azwater.gov>
- James Dieckhoff <Jdieckhoff@azwater.gov>
- Natalie Mast (AMA Director) <nlmast@azwater.gov>