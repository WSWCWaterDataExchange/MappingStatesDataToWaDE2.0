# UDNR Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Utah Division of Water Rights (DWRi)](https://waterrights.utah.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- **Utah Points of Diversion (POD)** data files for surface and groundwater were downloaded from the Utah SGID services: https://opendata.gis.utah.gov/datasets/utahDNR::utah-points-of-diversion/explore?showTable=true
- **Utah Plac eof Use* (POU)** data files were downloaded from the Utah SGID services: https://opendata.gis.utah.gov/datasets/utahDNR::utah-place-of-use/explore
- **Utility Data & Information** related to POD water rights were downloaded from the PUBDUMP Database table dump Utility: https://www.waterrights.utah.gov/cgi-bin/pubdump.exe?SECURITYKEY=wrt2012access&DUMP_TYPE=DUMP_TAB&DBNAME=WRDB&DBTABLE=WATER_MASTER&Key=New+Table

Seven unique files were created to be used as input.  Input files used are as follows...
- PointsOfDiversion_input.csv.  Contains POD data.
- Utah_Place_of_Use_input.csv.  Contains POU data.
- WRCHEX_WATER_MASTER.csv.  Contains water right related data.
- IRRIGATION_MASTER.csv.  Contains start and end date data for irrigation related to water rights. 
- WTRUSE_MUNICIPAL.csv.  Contains community id related to water rights information.
- WTRUSE_POWER.csv.  Contains power utility information related to water rights.

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share UDNR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *[UT_Allocation Schema Mapping_WaDEQA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Utah/WaterAllocation/UT_Allocation%20Schema%20Mapping_WaDEQA.xlsx)*.  Seven executable code files were used to extract the UDNR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those Seven code files are as follows...

- 0_PreProcessUtahAllocationData.ipynb
- 1_UTwr_Methods.py
- 2_UTwr_Variables.py
- 3_UTwr_Organizations.py
- 4_UTwr_WaterSources.py
- 5_UTwr_Sites.py
- 6_UTwr_AllocationsAmounts_facts.py
- 7_UTwr_PODSiteToPOUSiteRelationships.py


***
### 0) Code File: 0_PreProcessUtahAllocationData.ipynb
Purpose: Pre-process the Wyoming input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- PointsOfDiversion_input.csv.
- Utah_Place_of_Use_input.csv.
- WRCHEX_WATER_MASTER.csv.
- IRRIGATION_MASTER.csv.
- WTRUSE_MUNICIPAL.csv.
- WTRUSE_POWER.csv.

#### Outputs:
 - P_UtahMaster.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes for both POD and POU water right data.  Goal will be to create two separate clean tables and concatenate to single output table.
- POD and POU data share similar field and columns names.
- Perform the following additional actions on the POD data...
    - Left Merge POD data with WRCHEX_WATER_MASTER, IRRIGATION_MASTER, WTRUSE_MUNICIPAL, & WTRUSE_POWER data via **WRNUM** field.
    - Assign WaDE *PODorPOUSite* value = POD.
- Perform the following additional actions on the POU data...
    - Remove empty **WRNUMS** rows, can't match those to anything.
    - Left Merge POD data with WRCHEX_WATER_MASTER, IRRIGATION_MASTER, WTRUSE_MUNICIPAL, & WTRUSE_POWER data via **WRNUM** field.
    - Assign WaDE *PODorPOUSite* value = POU.
- Concatenate POD and POU data into single output dataframe.
- Change / double check data type for **CFS**, **ACFT**, **IRRIGATION_DEPLETION**, **PRIORITY**, **DATE_FILED**, **DATE_TERMINATED** fields.
- Create WaDE *WaterSourceTypeCV* field (see custom dictionary) using **TYPE** field.
- Create WaDE *AllocationTimeframeStart* & *AllocationTimeframeEnd* field using **USE_BEG_DATE** & **USE_END_DATE** fields.
- Create WaDE *SiteTypeCV* field (see custom dictionary) using **SOURCE** field (mostly cleaning input text).
- Create WaDE *LegalStatusCV* field (see custom dictionary) using **STATUS** field (mostly cleaning input text).
- Generate WaDE specific field *WaterSourceNativeID* from WaDE *WaterSourceTypeCV* fields.  Used to identify unique sources of water.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_UtahMaster.csv*.


***
### 1) Code File: 1_UTwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **UDNR** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
UT_Water Allocation | Surface Ground | Adjudicated


***
### 2) Code File: 2_UTwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **UDNR** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
WY_Allocation | 1 | Year | CFS


***
### 3) Code File: 3_UTwr_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **UTDWRi** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
UTDWRi | Utah Division of Water Rights | James Greer |"https://water.utah.gov/"


***
### 4) Code File: 4_UTwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_UtahMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **UDNR** info to the *WaDE WaterSources* specific columns.  See *[UT_Allocation Schema Mapping_WaDEQA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Utah/WaterAllocation/UT_Allocation%20Schema%20Mapping_WaDEQA.xlsx)* for specific details.  Items of note are as follows...
    - *WaterSourceName* = Unspecified.
    - *WaterSourceNativeID* = *in_WaterSourceNativeID*, see *0_PreProcessUtahAllocationData.ipynb* for specifics.
    - *WaterSourceTypeCV* = *in_WaterSourceTypeCV*, see *0_PreProcessUtahAllocationData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
UTwr_WS1 | Fresh | Unspecified | WaDEUT_WS1 | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_UTwr_Sites.py
Purpose: generate a list of sites information.

#### Inputs:
- P_UtahMaster.csv

#### Outputs:
- sites.csv
- waterSources.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **UDNR** info to the *WaDE Site* specific columns.  See *[UT_Allocation Schema Mapping_WaDEQA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Utah/WaterAllocation/UT_Allocation%20Schema%20Mapping_WaDEQA.xlsx)* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - *Latitude* = **Latitude**.
    - *Longitude* = **Longitude**.
    - *SiteName* = **SOURCE**, Unspecified if not given.
    - *SiteNativeID* = **OBJECTID**.
    - *SiteTypeCV* = *in_SiteTypeCV*, see *0_PreProcessUtahAllocationData.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
UTwr_S1 | UTwr_WS1| Unspecified | 38.6227946 | -109.401786199999 | Non-Production Well: Test

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_UTwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_UtahMaster.csv
- methods.csv
- variables.csv
- organizations.csv
- sites.csv

#### Outputs:
- waterallocations.csv
- waterallocations_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign **UDNR** info to the *WaDE Water Allocations* specific columns.  See *[UT_Allocation Schema Mapping_WaDEQA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Utah/WaterAllocation/UT_Allocation%20Schema%20Mapping_WaDEQA.xlsx)* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationApplicationDate* = **DATE_FILED**.
    - *AllocationCommunityWaterSupplySystem* = **MUNICIPALITY**.
    - *AllocationCropDutyAmount* = **IRRIGATION_DEPLETION**.
    - *AllocationExpirationDate* = **DATE_TERMINATED**.
    - *AllocationFlow_CFS* = **CFS**.
    - *AllocationLegalStatusCV* = *in_LegalStatus*, see *0_PreProcessUtahAllocationData.ipynb* for specifics. 
    - *AllocationNativeID* = **WRNUM**.
    - *AllocationOwner* =  **OWNER**.
    - *AllocationPriorityDate* = **PRIORITY**.
    - *AllocationTimeframeEnd* = *in_AllocationTimeframeEnd*, see *0_PreProcessUtahAllocationData.ipynb* for specifics.
    - *AllocationTimeframeStart* = *in_AllocationTimeframeStart*, see *0_PreProcessUtahAllocationData.ipynb* for specifics. 
    - *AllocationVolume_AF* = **ACFT**.
    - *BeneficialUseCategory* = **USES**.   
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
01-1000 | 0 | Diligence Claim | Other,Stockwatering

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- SiteUUID
- AllocationPriorityDate
- BeneficialUseCategory
- AllocationAmount or AllocationMaximum
- DataPublicationDate


***
### 7) Code File: 7_UTwr_PODSiteToPOUSiteRelationships.py
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
- If waterallocations dataframe is not empty, export output dataframe *podsitetopousiterelationships.csv*.


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Utah Division of Water Rights (DWRi)](https://waterrights.utah.gov//).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

DWRi Staff
- Jim Reese <jreese@utah.gov>
