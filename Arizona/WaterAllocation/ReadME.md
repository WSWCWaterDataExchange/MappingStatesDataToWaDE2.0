# ADWR Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Arizona Department of Water Resources(ADWR)](http://gisdata-azwater.opendata.arcgis.com/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- [SW QUERY BY SURFACE WATERSHEDS](http://www.azwater.gov/querycenter/query.aspx?qrysessionid=ABBBE0BF2A68326CE040000A16005CA1) for surface water point of diversion data (ADWR_Surface_Watersheds).
- [Surface Water Data](https://new.azwater.gov/gis) for surface water point of diversion data (SWR_fillings_POD).
- [Wells 55 Registry](https://new.azwater.gov/gis) point of diversion groundwater data (WELLS_wellRegistry).
- [Groundwater Site Inventory](https://new.azwater.gov/gis) for location information for groundwater data (GWSI_SITES).

Only data relevant to point of diversion was used at this time.


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share ADWR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see [*surfacewaterAZ_Allocation Schema Mapping to WaDE_QA.xlsx*](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Arizona/WaterAllocation/surfacewaterAZ_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx) and [*groundwaterAZ_Allocation Schema Mapping to WaDE_QA.xlsx*](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Arizona/WaterAllocation/groundwaterAZ_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx).  Six executable code files were used to extract the ADWR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those six code files are as follows...

- 0_PreProcessArizonaAllocationData.ipynb
- 1_AZ_Methods.py
- 2_AZ_Variables.py
- 3_AZ_Organizations.py
- 4_AZ_WaterSources.py
- 5_AZ_Sites.py
- 6_AZ_AllocationsAmounts_facts.py


***
### 0) Code File: 0_PreProcessArizonaAllocationData.ipynb
Purpose: Pre-process the state agency's input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - WELLS_wellRegistry.csv
 - GWSI_SITES.csv
 - SWR_fillings_POD.csv
 - ADWR_Surface_Watersheds_POD.csv

#### Outputs:
 - P_ArizonaMaster.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes for groundwater and surface water.  Processes outline consits of combning the two datasets into one workable dataframe. 
- For groundwater data...
    - Left join *WELLS_wellRegistry.csv* & *GWSI_SITES.csv* together, use **REG_ID** fields.
    - Create WaDE *latitude* and *longitude* fields by converting **UTM_X_METE** & **UTM_Y_METE** to utm & dWGS84 projection.
    - Assign groundwater data to WaDE appropriate fields.
    - Remove duplicate rows.
- For surface water data...
    - Create beneficial use field with **Reg. NO** field.
    - Left join *SWR_fillings_POD.csv* & *ADWR_Surface_Watersheds_POD.csv* together, use **FILE_NO** & **REG. NO** fields.
    - Create WaDE *latitude* and *longitude* fields by converting **UTM_X_METE** & **UTM_Y_METE** to utm & dWGS84 projection.
    - For flow data, separate value and unit info out from the **QUANTITY** field.  CFS data will include all values with a **Cubic Feet Per Second** unit.
    - For volume data, separate value and unit info out from the **QUANTITY** field.  Volume data will include all values with a **Acre-Feet Per Annum**, **Acre-Feet**, **Acre-Feet Total**, **ACRES**, **CFT - Cubic Feet Total**, **Feet**, **Gallons**, **Gallons Per Annum**, **Miners Inches Per Annum**, and **MIT - Miners Inches Total** unit.  Gallon and Miner's Inches volume data will need to be converted to AF.
    - Assign surface water data to WaDE appropriate fields.
    - Remove duplicate rows.
- Concatenate groundwater and surface water data into single output dataframe.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_ArizonaMaster.csv*.


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
ADWR_Water Rights GW | Groundwater | Adjudicated
ADWR_Water Rights SW | Surface Water | Adjudicated


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
ADWR_Allocation All | 1 | Year | CFS


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
ADWR | Arizona Department of Water Resources| Lisa Williams | http://gisdata-azwater.opendata.arcgis.com/


***
### 4) Code File: 4_AZ_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_ArizonaMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency data info to the *WaDE WaterSources* specific columns.  See [*surfacewaterAZ_Allocation Schema Mapping to WaDE_QA.xlsx*](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Arizona/WaterAllocation/surfacewaterAZ_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx) and [*groundwaterAZ_Allocation Schema Mapping to WaDE_QA.xlsx*](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Arizona/WaterAllocation/groundwaterAZ_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx) for specific details.  Items of note are as follows...
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
- P_ArizonaMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to the *WaDE Site* specific columns.  See [*surfacewaterAZ_Allocation Schema Mapping to WaDE_QA.xlsx*](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Arizona/WaterAllocation/surfacewaterAZ_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx) and [*groundwaterAZ_Allocation Schema Mapping to WaDE_QA.xlsx*](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Arizona/WaterAllocation/groundwaterAZ_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx) for specific details.  Items of note are as follows...
    - *County* = **COUNTY** for both gw and sw data.
    - *Latitude* = converted **UTM_Y_METE** projection from ADWR EPSG:2927 -to- WaDE EPSG:4326, see *0_PreProcessArizonaAllocationData.ipynb* for details.
    - *Longitude* = converted **UTM_Y_METE**  to utm & dWGS84 projection, see *0_PreProcessArizonaAllocationData.ipynb* for details.

    - *SiteNativeID* = **REGISTRY_I** for gw & **CADASTRAL** for sw, Unspecified if blank.
    - *SiteTypeCV* = **WELL_TYPE_** for gw & Unspecified for sw, Unspecified if blank.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteTypeCV*, *Longitude*, and *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteNativeID
---------- | ---------- | ------------ | ------------ | ------------
AZwr_S1 | Unspecified | 32.951858357839 | -111.814054446414 | 60000

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_AZ_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_ArizonaMaster.csv
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
- Assign state agency info to the *WaDE Water Allocations* specific columns.  See [*surfacewaterAZ_Allocation Schema Mapping to WaDE_QA.xlsx*](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Arizona/WaterAllocation/surfacewaterAZ_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx) and [*groundwaterAZ_Allocation Schema Mapping to WaDE_QA.xlsx*](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Arizona/WaterAllocation/groundwaterAZ_Allocation%20Schema%20Mapping%20to%20WaDE_QA.xlsx) for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* =**QUANTITY**, see *0_PreProcessArizonaAllocationData.ipynb* for specifics.
    - *AllocationLegalStatusCV* = **STATUS_x** for sw.
    - *AllocationNativeID* = **REGISTRY_I** for gw & **FILE_NO** for sw.
    - *AllocationOwner* = **OWNER_NAME** for gw & **HLDRNAME** for sw.
    - *AllocationPriorityDate* = **PRIOR_DATE** for sw.
    - *AllocationTypeCV* = **WELL_TYPE_** for gw.
    - *BeneficialUseCategory* = **WATER_USE** for gw & **REG. NO** for sw, see *0_PreProcessArizonaAllocationData.ipynb* for specifics.
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


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Arizona Department of Water Resources(ADWR)](http://gisdata-azwater.opendata.arcgis.com/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

ADWR Staff
- Lisa Williams <lmwilliams@azwater.gov>
- James Dieckhoff <Jdieckhoff@azwater.gov>