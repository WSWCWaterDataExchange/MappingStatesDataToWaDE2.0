# WSDE Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Washington State Department of Ecology (WSDE)](https://ecology.wa.gov/Water-Shorelines/Water-supply/Water-rights), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**WA GWIS_Data download** | Data made available can be found within the **GWIS_SDEexport.zip** option.| [link](https://fortress.wa.gov/ecy/gispublic/DataDownload/wr/GWIS_Data/) | [link](https://fortress.wa.gov/ecy/gispublic/DataDownload/wr/GWIS_Data/GWIS_Data_Dictionary/)
D_PointTable.csv | see above link | obtained from above GWIS_SDEexport.zip | -
D_Point_WR_Doc.csv | see above link | obtained from above GWIS_SDEexport.zip | -
WA_POU_Input.csv | see above link | obtained from above GWIS_SDEexport.zip |-
Person_Plus_EXTRACT_FromWRTSnotGWIS.csv | see above link | obtained from above GWIS_SDEexport.zip | -


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Washington Allocation Data: https://drive.google.com/drive/folders/1Bv21_uF9kGk1FOIRZnmdxNYP2f0POUIN?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *WAwr_Allocation Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_WAwr_PreProcessAllocationData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_WAwr_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv.
- **3_WAwr_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.



***
## Code File: 1_WAwr_PreProcessAllocationData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - D_PointTable.csv
 - D_Point_WR_Doc.csv
 - WA_POU_Input.csv
 - Person_Plus_EXTRACT_FromWRTSnotGWIS.csv

#### Outputs:
 - P_WashingtonMaster.csv

#### Operation and Steps:
- Read in the input files.  Goal will be to create separate POD and POU centric dataframes, then join together for single long output dataframe.
- For POD data...
    - Left Join D_PointTable.csv and D_Point_WR_Doc.csv via **D_Point_ID**, and Person_Plus_EXTRACT_FromWRTSnotGWIS.csv via **WR_Doc_ID**.
    - Generate WaDE *Latitude* & *Longitude* fields with **POINT_X** & **POINT_Y** inputs.  Need to convert EPSG:2927 -to- WaDE accepted EPSG:4326.
    - Format **PriorityDate** field to %m/%d/%Y format.
    - Generate *Owner* field with **PersonFirstNM**, **PersonMINM**, & **PersonLastOrOrganizationNM** inputs.
    - Fill in blank **WaRecRCWClassTypeCode** with *Unspecified* values.
    - Generate WaDE *AllocationFlow_CFS* field with **InstantaneousQuantity** & **InstantaneousUnitCode** inputs.  Need to convert to CFS.
    - Create WaDE POD centric temporary dataframe.  Extract POD relevant data (see preprocessing code).
- For POU data...
    - Left Join WA_POU_Input.csv and Person_Plus_EXTRACT_FromWRTSnotGWIS.csv via **WR_Doc_ID**.
    - Format **PriorityDate** field to %m/%d/%Y format.
    - Generate *Owner* field with **PersonFirstNM**, **PersonMINM**, & **PersonLastOrOrganizationNM** inputs.
    - Fill in blank **WaRecRCWClassTypeCode** with *Unspecified* values.
    - Generate WaDE *AllocationFlow_CFS* field with **InstantaneousQuantity** & **InstantaneousUnitCode** inputs.  Need to convert to CFS.
    - Generate WaDE specific field *SiteNativeID* from WaDE *Latitude* & *Longitude* fields.  Used to identify unique sites.
    - Create WaDE POU centric temporary dataframe.  Extract POU relevant data (see preprocessing code).
- Concatenate temporary POD & POU dataframes together into single long output dataframe.
- Generate WaDE specific field *WaterSourceNativeID* from WaDE *WaterSourceTypeCV* field.  Used to identify unique sources of water.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_WashingtonMaster.csv*.


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
- Assign **WSDE** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
WAwr_M1 | Surface Ground | Adjudicated


## 2) Variables Information
Purpose: generate legend of granular variables specific to each state.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **WSDE** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
WAwr_V1 | 1 | Year | CFS


## 3) Organization Information
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **WSDE** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
WAwr_O1 | Washington State Department of Ecology | Riddle, H. Nicholas | HRID461@ECY.WA.GOV


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency data info to the *WaDE WaterSources* specific columns.  See *WA_Allocation Schema Mapping_WaDEQA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = **WaRecRCWClassTypeCode**, Unspecified if not given.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------
WAwr_WS1 | Fresh | Unspecified | Unspecified | groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


## 5) Site Information
Purpose: generate a list of sites where water is diverted (also known as Points Of Diversion, PODs).

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to the *WaDE Site* specific columns.  See *WA_Allocation Schema Mapping_WaDEQA.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - *CoordinateMethodCV* = **Location_C**, translate abbreviations code with dictionary.  Leave blank if not given.
    - *Latitude* = converted **POINT_X** projection from WSDE EPSG:2927 -to- WaDE EPSG:4326.
    - *Longitude* = converted **POINT_Y** projection from WSDE EPSG:2927 -to- WaDE EPSG:4326.
    - *SiteNativeID* = **D_Point_ID**.
    - *SiteTypeCV* = **D_Point_Ty**, Unknown if blank.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteTypeCV*, *Longitude*, and *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
WAwr_S1 | WAwr_WS1 | field checked with GPS | 46.5836906784566 | -119.798723819468 | 200889

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
- Assign state agency info to the *WaDE Water Allocations* specific columns.  See *WA_Allocation Schema Mapping_WaDEQA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* = **InstantaneousQuantity** & **InstantaneousUnitCode**, covert to GPM or GPD, depending on code value.
    - *AllocationLegalStatusCV* = **WaRecProcessStatusTypeCode**.
    - *AllocationNativeID* = **WR_Doc_ID**.
    - *AllocationOwner* = **Owner**, see *0_PreProcessWashingtonAllocationData.ipynb* for specifics.
    - *AllocationPriorityDate* = **PriorityDate**.
    - *AllocationTypeCV* = **WaRecPhaseTypeCode**, Unknown if not given.
    - *BeneficialUseCategory* = **PurposeOfUseTypeCodes**, translate abbreviations code with dictionary.  Unknown if not given.
    - *IrrigatedAcreage* - **IrrigatedAreaQuantity**.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
2032170 | 0.02 | Active | Domestic single

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Washington State Department of Ecology (WSDE)](https://ecology.wa.gov/Water-Shorelines/Water-supply/Water-rights).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

WSDE Staff
- Riddle, H. Nicholas <HRID461@ECY.WA.GOV>