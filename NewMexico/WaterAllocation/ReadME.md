# NMOSE Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [New Mexico Office of the State Engineer (NMOSE)](https://www.ose.state.nm.us/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

- [**OSE PODs**](https://geospatialdata-ose.opendata.arcgis.com/datasets/OSE::ose-pods/about):  Point of diversion water right sites.

The following unique files were created as input.  Input files used are as follows...
 - OSE_PODst.csv

## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- New Mexico Allocation Data: https://drive.google.com/drive/folders/171lNosVUaf6yXxUL3d7lrRAYZSYaw22s?usp=sharing

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NMOSE's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NV_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *NM_Allocation Schema Mapping to WaDE_QA.xlsx*.  Seven executable code files were used to extract the NMOSE's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (preprocess) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining six code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those seven code files are as follows...

- 0_NM_PreProcessNewMexicoAllocationData.ipynb
- 1_NMwr_Methods.py
- 2_NMwr_Variables.py
- 3_NMwr_Organizations.py
- 4_NMwr_WaterSources.py
- 5_NMwr_Sites.py
- 6_NMwr_AllocationsAmounts_facts.py
- 7_NMwr_PODSiteToPOUSiteRelationships.py


***
### 0) Code File: 0_NM_PreProcessNewMexicoAllocationData.ipynb
Purpose: preprocess the Montana input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 -  OSE_PODst.csv

#### Outputs:
 - P_NewMexicoMaster.csv

#### Operation and Steps:
- Read in the input files & create temporary dataframes.
- Create longitude & latitude values from the existing **easting** & **northing** inputs using projection of init="epsg:26913", proj="utm", zone=13.
- If **ditch_name**  input is blank, replace with "Unspecified".
- Assign "Groundwater" text to **grnd_wtr_s** if not blank, & "Surface Water" text to **surface_co** input if value is not blank & > 0.  For water source type...
  - if both values are are not blank, assign "Surface and Groundwater" text.
  - if groundwater is not blank, assign "Groundwater" text.
  - if groundwater is blank but surface water is not, assign "Surface Water" text.
  - if both values are blank, assign "Unspecified" text.
- Translate **surface_co** input from number code to name using provided dictionary.
- Format **finish_dat_fix** field to %m/%d/%Y format.
- Concatenate **own_fname** & **own_lname** fields together to create an owner name.
- Translate **use_** input from abbreviation to descriptive text of the beneficial using provided dictionary.
- Translate **status** input from abbreviation to descriptive text of the legal status using provided dictionary.
- Generate WaDE specific field *WaterSourceNativeID* from WaDE *WaterSourceName* & *WaterSourceTypeCV* fields.  Used to identify unique sources of water.
- Generate WaDE specific field *SiteNativeID* from WaDE *Latitude*, *Longitude*, & *SiteName* fields.  Used to identify unique sites.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_NewMexicoMaster.csv*.


***
### 1) Code File: 1_NMwr_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **NMOSE** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
NMwr_M1 | Surface Ground | Adjudicated


***
### 2) Code File: 2_NMwr_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **NMOSE** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
NMwr_V1 | 1 | Year | CFS


***
### 3) Code File: 3_MTwr_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **NMOSE** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
NMwr_O1 | New Mexico Office of the State Engineer | David Hatchner (GIS Manager) | https://www.ose.state.nm.us/


***
### 4) Code File: 4_NMwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_NewMexicoMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **NMOSE** info to the *WaDE WaterSources* specific columns.  See *NV_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *NM_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = translated from **surface_co**, see *0_NM_PreProcessNewMexicoAllocationData.ipynb* for specifics. 
    - *WaterSourceTypeCV* = generated list of sources from **SOURCE_TYPE**, see *0_NM_PreProcessNewMexicoAllocationData.ipynb* for specifics.
    - *WaterSourceNativeID* = see *0_NM_PreProcessNewMexicoAllocationData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NMwr_WS1 | Unspecified | Unspecified | WaDENM_WS1 | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_NMwr_Sites.py
Purpose: generate a list of sites information.

#### Inputs:
- P_NewMexicoMaster.csv
- watersources.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **NMOSE** info to the *WaDE Site* specific columns.  See *NV_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *NM_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - *County* = **county** input.
    - *Latitude* = created from **easting** & **northing** inputs, see *0_NM_PreProcessNewMexicoAllocationData.ipynb* for specifics.
    - *Longitude* = created from **easting** & **northing** inputs, see *0_NM_PreProcessNewMexicoAllocationData.ipynb* for specifics.
    - *SiteName* = **ditch_name** inputs, see *0_NM_PreProcessNewMexicoAllocationData.ipynb* for specifics.
    - *SiteNativeID* = *in_SiteNativeID*, see *0_NM_PreProcessNewMexicoAllocationData.ipynb* for specifics.
    - *SiteTypeCV* = "Unspecified".
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
NMwr_S1 | NMwr_WS1 | Unspecified | 35.3044225068985 | -108.145455321569 | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_NMwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_NewMexicoMaster.csv
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
- Assign **NMOSE** info to the *WaDE Water Allocations* specific columns.  See *NV_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *NM_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* = empty.
    - *AllocationLegalStatusCV* = **status** input, see *0_NM_PreProcessNewMexicoAllocationData.ipynb* for specifics.
    - *AllocationNativeID* = **nbr** input as string.
    - *AllocationOwner* = **own_fname** & **own_lname** inputs, see *0_NM_PreProcessNewMexicoAllocationData.ipynb* for specifics.
    - *AllocationPriorityDate* = **finish_dat_fix** input, , see *0_NM_PreProcessNewMexicoAllocationData.ipynb* for specifics.
    - *AllocationVolume_AF* == **restrict_** input, as float.
    - *BeneficialUseCategory* = **use_** input, , see *0_NM_PreProcessNewMexicoAllocationData.ipynb* for specifics.
    - *IrrigatedAcreage* = **total_div** input.
    - *WaterAllocationNativeURL* = **nmwrrs_wrs**
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationVolume_AF | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
NMwr_WR1 | 1 | Permit | Unspecified

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
### 7) Code File: 7_NMwr_PODSiteToPOUSiteRelationships.py
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
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nevada Division of Water Resources [New Mexico Office of the State Engineer (NMOSE)](https://www.ose.state.nm.us/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

NMOSE Staff
- David Hatchner (GIS Manager)<ose.webmaster@state.nm.us>
