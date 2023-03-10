# ADWR Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Arizona Department of Water Resources(ADWR)](http://gisdata-azwater.opendata.arcgis.com/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

- [SW QUERY BY SURFACE WATERSHEDS](https://www.azwater.gov/querycenter/query.aspx?qrysessionid=ABBBE0BF2A68326CE040000A16005CA1) for surface water right data (SW QUERY BY SURFACE WATERSHEDS).  Downloaded used all washed under the 'ACTIVE' status.
- [Fillings.shp] for location information related to the SW QUERY BY SURFACE WATERSHEDS data. Provided by personal correspondence with ADWR via email.
- [Well Registry](https://gisdata2016-11-18t150447874z-azwater.opendata.arcgis.com/datasets/34c92af536ec4047aeaf9d93053dc317_0/explore?location=34.103087%2C-111.970052%2C7.92) for groundwater water right data.  Contains use and location info. 


## Storage for input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Arizona Allocation Data: https://drive.google.com/drive/folders/1qxIpa1mGkvChepI4PA7xzIEbs7xuPSJZ?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share ADWR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see **AZ_SW_Allocation Schema Mapping to WaDE_QA.xlsx** and **AZ_GW_Allocation Schema Mapping to WaDE_QA.xlsx**.  Six executable code files were used to extract the ADWR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those six code files are as follows...

- 0_AZwr_PreProcessAllocationData.ipynb
- 1_AZ_Methods.py
- 2_AZ_Variables.py
- 3_AZ_Organizations.py
- 4_AZ_WaterSources.py
- 5_AZ_Sites.py
- 6_AZ_AllocationsAmounts_facts.py
- 7_AZwr_PODSiteToPOUSiteRelationships.py


***
### 0) Code File: 0_AZwr_PreProcessAllocationData.ipynb
Purpose: Pre-process the state agency's input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - SW QUERY BY SURFACE WATERSHEDS
 - Fillings.shp
 - Well Registry

#### Outputs:
 - Pwr_AZMain.csv

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
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *Pwr_AZMain.csv*.


***
### 1) Code File: 1_AZ_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

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


***
### 2) Code File: 2_AZ_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

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


***
### 3) Code File: 3_AZ_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

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


***
### 4) Code File: 4_AZ_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- Pwr_AZMain.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency data info to the *WaDE WaterSources* specific columns.  See **AZ_SW_Allocation Schema Mapping to WaDE_QA.xlsx** and **AZ_GW_Allocation Schema Mapping to WaDE_QA.xlsx** for specific details.  Items of note are as follows...
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


***
### 5) Code File: 5_AZ_Sites.py
Purpose: generate a list of sites where water is diverted (also known as Points Of Diversion, PODs).

#### Inputs:
- Pwr_AZMain.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to the *WaDE Site* specific columns.  See **AZ_SW_Allocation Schema Mapping to WaDE_QA.xlsx** and **AZ_GW_Allocation Schema Mapping to WaDE_QA.xlsx** for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersource.csv input file. See code for specific implementation of extraction.
    - *County* = **COUNTY** for both gw and sw data.
    - *Latitude* = converted **UTM_Y_METE** projection from ADWR EPSG:2927 -to- WaDE EPSG:4326, see *0_AZwr_PreProcessAllocationData.ipynb* for details.
    - *Longitude* = converted **UTM_Y_METE**  to utm & dWGS84 projection, see *0_AZwr_PreProcessAllocationData.ipynb* for details.
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


***
### 6) Code File: 6_AZ_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- Pwr_AZMain.csv
- methods.csv
- variables.csv
- organizations.csv
- watersources.csv
- sites.csv

#### Outputs:
- waterallocations.csv
- waterallocations_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign state agency info to the *WaDE Water Allocations* specific columns.  See **AZ_SW_Allocation Schema Mapping to WaDE_QA.xlsx** and **AZ_GW_Allocation Schema Mapping to WaDE_QA.xlsx** for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* =**QUANTITY**, see *0_AZwr_PreProcessAllocationData.ipynb* for specifics.
    - *AllocationLegalStatusCV* = **STATUS_x** for sw.
    - *AllocationNativeID* = **REGISTRY_I** for gw & **FILE_NO** for sw.
    - *AllocationOwner* = **OWNER_NAME** for gw & **HLDRNAME** for sw.
    - *AllocationPriorityDate* = **PRIOR_DATE** for sw.
    - *AllocationLegalStatus* = **WELL_TYPE_** for gw.
    - *BeneficialUseCategory* = **WATER_USE** for gw & **REG. NO** for sw, see *0_AZwr_PreProcessAllocationData.ipynb* for specifics.
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


***
### 7) Code File: 7_AZwr_PODSiteToPOUSiteRelationships.py
Purpose: generate linking element between POD and POU sites that share the same water right.
Note: podsitetopousiterelationships.csv output only needed if both POD and POU data is present, otherwise produces empty file.

#### Inputs:
- sites.csv
- waterallocations.csv

#### Outputs:
- podsitetopousiterelationships.csv

#### Operation and Steps:
- Read the sites.csv & waterallocations.csv input files.
- Create three temporary dataframes: one for waterallocations, & two for site info that will store POD and POU data separately.
- For the temporary POD dataframe...
    - Read in site.csv data from sites.csv with a *PODSiteUUID* field = POD only.
    - Create *PODSiteUUID* field = *SiteUUID*.
- For the temporary POU dataframe
    - Read in site.csv data from sites.csv with a *PODSiteUUID* field = POU only.
    - Create *POUSiteUUID* field = *SiteUUID*.
- For the temporary waterallocations dataframe, explode *SiteUUID* field to create unique rows.
- Left-merge POD & POU dataframes to the waterallocations dataframe via *SiteUUID* field.
- Consolidate waterallocations dataframe by grouping entries by *AllocationNativeID* filed.
- Explode the consolidated waterallocations dataframe again using the *PODSiteUUID* field, and again for the *POUSiteUUID* field to create unique rows.
- Perform error check on waterallocations dataframe (check for NaN values)
- If waterallocations is not empty, export output dataframe *podsitetopousiterelationships.csv*.


***
### 8) Code File: 8_AZwr_WaDEDataAssessmentScript.py
Purpose: generate visuals and analytics used by the WaDE staff to inspect the processed data.


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Arizona Department of Water Resources(ADWR)](http://gisdata-azwater.opendata.arcgis.com/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

ADWR Staff
- Lisa Williams <lmwilliams@azwater.gov>
- James Dieckhoff <Jdieckhoff@azwater.gov>