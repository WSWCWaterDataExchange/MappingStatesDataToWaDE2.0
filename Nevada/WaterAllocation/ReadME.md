# NVDWR Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Nevada Division of Water Resources (NVDWR)](http://water.nv.gov/index.aspx), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Point of diversion (POD)** | Point of diversion water right site data from NVDWR arcgis server. | [link](https://arcgis.shpo.nv.gov/arcgis/rest/services/Water_Resources_Public_Data/WaterRights_POD_POU/FeatureServer) | not given
**Place of Use (POU)** | Place of use water right polygon data from NVDWR arcgis server. | [link](https://arcgis.shpo.nv.gov/arcgis/rest/services/Water_Resources_Public_Data/WaterRights_POD_POU/FeatureServer)
**Permit Owner** | Permit owner data for water right data | [link](https://arcgis.shpo.nv.gov/arcgis/rest/services/Water_Resources_Public_Data/WaterRights_POD_POU/FeatureServer)

Three unique files were created as input.  Input files used are as follows...
 - POD AllApps_2_input.csv
 - PoU AllApps_3_input.csv
 - Permit_Owners_5temp.csv


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Nevada Allocation Data: https://drive.google.com/drive/folders/15oclBZ9uLOneLzr9mR_2C2hM_VTqAgly?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NMOSE's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NVwr_Allocation Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the NMOSE's water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_NVwr_PreProcessAllocationData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_NVwr_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv.
- **3_NVwr_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_NVwr_PreProcessAllocationData.ipynb
Purpose: preprocess the Montana input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - POD AllApps_2_input.csv
 - PoU AllApps_3_input.csv
 - Permit_Owners_5temp.csv

#### Outputs:
 - P_MastersNV.csv

#### Operation and Steps:
- Read in the input files.  Create temporary POD and POU dataframes.  POD and POU data share similar fields.
- For NV, we don't want water rights that are considered: Abandoned, Abrogated, Application, Canceled, Denied, Expired, Forfeited, Ready For Action, Ready for Action (Protested), Rejected, Revoked, Supersceded, Withdrawn
- For POD AllApps_2_input.csv, set WaDE field *PODorPOUSite* = POD.
- For PoU AllApps_3_input.csv, set WaDE field *PODorPOUSite* = POU.
- Concatenate temporary POD & POU dataframes together into single long output dataframe.
- Left-merge Permit_Owners_5temp.csv via **app** field to long concatenated dataframe..  Drop duplicates.
- Generate WaDE specific field *WaterSourceTypeC* from NVDWR **source** field (see preprocess code for specific dictionary used).
- Generate WaDE specific field *SiteName* from NVDWR **site_name** field (see preprocess code for specific dictionary used).
- Generate WaDE specific field *SiteTypeCV* from NVDWR **source** field (see preprocess code for specific dictionary used).
- Generate WaDE specific field *SiteNativeID* from WaDE *Latitude*, *Longitude*, *SiteTypeCV* & *SiteName* fields.  Used to identify unique sites.
- Generate WaDE specific field *WaterSourceNativeID* from WaDE *WaterSourceName* & *WaterSourceTypeCV* fields.  Used to identify unique sources of water.
- Format **prior_dt** field to %m/%d/%Y format.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_MastersNV.csv*.


***
## Code File: 2_NMwr_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv).

#### Inputs:
- Pwr_NMMain.zip

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
- Assign **NVDWR** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
NVwr_M1 | Surface Ground | Estimated


## 2) Variables Information
Purpose: generate legend of granular variables specific to each state.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **NVDWR** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
NVwr_V1 | 1 | Year | AF


## 3) Organization  Information
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **NVDWR** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
NVwr_O1 | Nevada Division of Water Resources | Brian McMenamy | http://water.nv.gov/index.aspx


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **NVDWR** info to the *WaDE WaterSources* specific columns.  See *NV_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *NV_POU_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = generated list of sources from **SOURCE_TYPE**, see *0_PreProcessNevadaAllocationData.ipynb* for specifics.
    - *WaterSourceNativeID* = see *0_PreProcessNevadaAllocationData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NVwr_WS1 | WaDE Unspecified | WaDE Unspecified | WaDENV_WS1 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


## 5) Site Information
Purpose: generate a list of sites information.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **NVDWR** info to the *WaDE Site* specific columns.  See *NV_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *NV_POU_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - *County* = **county_x**.
    - *Latitude* = **x**.
    - *Longitude* = **y**.
    - *SiteName* = *in_SiteName*, see *0_PreProcessNevadaAllocationData.ipynb* for specifics.
    - *SiteNativeID* = *in_SiteNativeID*, see *0_PreProcessNevadaAllocationData.ipynb* for specifics.
    - *SiteTypeCV* = *in_SiteTypeCV*, see *0_PreProcessNevadaAllocationData.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
NVwr_S1 | NVwr_WS1 | Digitized | 41.9883349988497 | -118.527228999731 | WaDE Unspecified

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
- Assign **NVDWR** info to the *WaDE Water Allocations* specific columns.  See *NV_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *NV_POU_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* = **duty_balance**.
    - *AllocationLegalStatusCV* = **app_status**.
    - *AllocationNativeID* = **app**.
    - *AllocationOwner* = **owner_name**.
    - *AllocationPriorityDate* = **prior_dt**.
    - *BeneficialUseCategory* = **mou**.
    - *WaterAllocationNativeURL* = **permit_info**
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
1 | 0 | Canceled | Power

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
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
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nevada Division of Water Resources (NVDWR)]( http://water.nv.gov/index.aspx).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

Nevada DNR Staff
- Brian McMenamy (IT Professional) <bmcmenamy@water.nv.gov>
- Levi Kryder (Chief Hydrology Section) <lkryder@water.nv.gov>
- Caitlan Jellema (Water Use Specialist) <cjellema@water.nv.gov>
- Stephanie Snider (GIS Analyst) <ssnider@water.nv.gov>
