# MDNRC Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Montana Department of Natural Resources and Conservation (MDNRC)](https://opendata-mtdnrc.hub.arcgis.com/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Point of diversion (POD)** | Point of diversion water right data. | [link](https://opendata-mtdnrc.hub.arcgis.com/datasets/wade-pods) | not provided
**Point of use (PoU)** | Place of use water right data. | [link](https://opendata-mtdnrc.hub.arcgis.com/datasets/wade-pous) | not provided

Two unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - WaDE_PODs_input.csv
 - WaDE_PoUs_input.csv


 ## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), 2) WaDE input csv processed data files ready to load into the WaDE database, & 3) data assessment figures and reports overviewing the native state data and which records could not be used, can all be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- [WaDE Montana Allocation Data (link)](https://drive.google.com/drive/folders/1XR9bTKTIxddu3mjOoVeL4AKry4roY0tb?usp=share_link)


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *MT_POD_Allocation Schema Mapping to WaDE.xlsx* & *MT_POU_Allocation Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the NMOSE's water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_MTwr_PreProcessAllocationData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_MTwr_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv.
- **3_MTwr_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_MTwr_PreProcessAllocationData.ipynb
Purpose: pre-process the Montana input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - WaDE_PODs_input.csv

#### Outputs:
 - Pwr_mtMain.zip

#### Operation and Steps:
- Read in the input files.  Goal will be to create separate POD and POU cenetric dataframes, then join together for single long output dataframe.
- For POD data...
    - Generate WaDE specific field *WaterSourceTypeC* from MDNRC **SOURCE_TYPE** field (see preprocess code for specific dictionary used).
    - Format **ENF_PRIORITY_DATE** field to %m/%d/%Y format.
    - Generate WaDE specific field *MethodTypeCV* from MDNRC **ENF_PRIORITY_DATE** field (see preprocess code for specific dictionary used).  Water rights that were established prior to July 1,1973 are administered by the Adjudication Bureau. Water rights that were established from July 1, 1973 through the present are administered by the New Appropriations Program.
    - Generate WaDE Specific Field *TimeframeStart* from MDNRC **PER_DIV_BGN_DT** field (see preprocess code for specific dictionary used).
    - Generate WaDE Specific Field *TimeframeEnd* from MDNRC **PER_DIV_END_DT** field (see preprocess code for specific dictionary used).
    - Create WaDE POD centric temporary dataframe.  Extract POU relevant data (see preprocessing code).
    - Create WaDE POD Native URL by breaking up **WR_NUMBER** for basin code, and numbers in 2000 values and tie to "http://wrqs.dnrc.mt.gov/ResultsWS.aspx?search=simple&index=8&wrnumber=" url.
- For POU data...
    - Generate WaDE specific field *WaterSourceTypeC* from MDNRC **SRCTYPE** field (see preprocess code for specific dictionary used).
    - Format **ENF_PRIORITY_DATE** field to %m/%d/%Y format.
    - Generate WaDE specific field *MethodTypeCV* from MDNRC **ENF_PRIORI** field (see preprocess code for specific dictionary used).  Water rights that were established prior to July 1,1973 are administered by the Adjudication Bureau. Water rights that were established from July 1, 1973 through the present are administered by the New Appropriations Program.
    - Generate WaDE Specific Field *TimeframeStart* from MDNRC **PER_USE_BG** field (see preprocess code for specific dictionary used).
    - Generate WaDE Specific Field *TimeframeEnd* from MDNRC **PER_USE_EN** field (see preprocess code for specific dictionary used).
    - Create WaDE POU centric temporary dataframe.  Extract POU relevant data (see preprocessing code).
    - Generate WaDE specific field *SiteNativeID* from WaDE *Latitude*, *Longitude*, *SiteTypeCV* & *SiteName* fields.  Used to identify unique sites.
    - Create WaDE POU Native URL by breaking up **WRNUMBER** for basin code, and numbers in 2000 values and tie to "http://wrqs.dnrc.mt.gov/ResultsWS.aspx?search=simple&index=8&wrnumber=" url.
- Concatenate temporary POD & POU dataframes together into single long output dataframe.
- Generate WaDE specific field *WaterSourceNativeID* from WaDE *WaterSourceName* & *WaterSourceTypeCV* fields.  Used to identify unique sources of water.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *Pwr_mtMain.zip*.


***
## Code File: 2_MTwr_CreateWaDEInputFiles.ipynb
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
- Assign **MDNRC** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
MTwr_M1 | Surface Water and Groundwater | Adjudication


## 2) Variables Information
Purpose: generate legend of granular variables specific to each state.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **MDNRC** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
MTwr_V1 | 1 | Year | CFS


## 3) Organization  Information
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **MDNRC** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
MTwr_O1 | Montana Dept. of Water Rights | Chris Kuntz | http://dnrc.mt.gov/


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **MDNRC** info to the *WaDE WaterSources* specific columns.  See *MT_POD_Allocation Schema Mapping to WaDE.xlsx* & *MT_POU_Allocation Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = **SOURCE_NAME**, Unspecified if not given.
    - *WaterSourceTypeCV* = generated list of sources from **SOURCE_TYPE**, see *1_MTwr_PreProcessAllocationData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
MTwr_WS7 | Fresh | FROZEN HORSE CREEK | WaDE Unspecified | SURFACE

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


## 5) Site Information
Purpose: generate a list of sites information.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **MDNRC** info to the *WaDE Site* specific columns.  See *MT_POD_Allocation Schema Mapping to WaDE.xlsx* & *MT_POU_Allocation Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - *County* = **LLDS_COUNTY_NAME**.
    - *HUC12* = **HUC_12**.
    - *Latitude* = **X**.
    - *Longitude* = **Y**.
    - *SiteName* = **DITCH_NAME**, Unspecified if not given.
    - *SiteNativeID* = **PODV_ID_SEQ**.
    - *SiteTypeCV* = **MEANS_OF_DIV**, Unspecified if not given.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
MTwr_S1 | MTwr_WS1 | WaDE Unspecified | 45.10645361 | -104.1225607 | WaDE Unspecified 

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
- Assign **MDNRC** info to the *WaDE Water Allocations* specific columns.  See *MT_POD_Allocation Schema Mapping to WaDE.xlsx* & *MT_POU_Allocation Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* = **FLW_RT_CFS**.
    - *AllocationLegalStatusCV* = **WR_STATUS**.
    - *AllocationNativeID* = **WR_NUMBER**.
    - *AllocationOwner* = **ALL_OWNERS**.
    - *AllocationPriorityDate* = **ENF_PRIORITY_DATE**.
    - *AllocationTimeframeEnd* = **PER_DIV_END_DT**.
    - *AllocationTimeframeStart* = **PER_DIV_BGN_DT**.
    - *AllocationTypeCV* = **WR_TYPE**.
    - *AllocationVolume_AF* = **VOLUME**.
    - *BeneficialUseCategory* = **PURPOSES**.
    - *DataPublicationDOI* = **ABST_LINK**.
    - *ExemptOfVolumeFlowPriority* = **WR_TYPE**, see *1_MTwr_PreProcessAllocationData.ipynb* for details.
    - *IrrigatedAcreage* = **MAX_ACRES**.
    - *WaterAllocationNativeURL* = break up **WR_NUMBER** into 1) basin number, and 2) '2000' numbers, see *1_MTwr_PreProcessAllocationData.ipynb* for details. 
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
38H 126342 00 | 0.01 | ACTIVE | STOCK

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Montana Department of Natural Resources and Conservation (MDNRC)](https://opendata-mtdnrc.hub.arcgis.com/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

Montana DNRC Staff
- Chris Kuntz <CKuntz@mt.gov>
- David Coey <dcoey@mt.gov>
- Karen Coleman <Karen.Coleman@mt.gov>
- Matthew Norberg <MNorberg@mt.gov>