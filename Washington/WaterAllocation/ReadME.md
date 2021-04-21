# WSDE Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Washington State Department of Ecology (WSDE)](https://ecology.wa.gov/Water-Shorelines/Water-supply/Water-rights), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...

- [WA GWIS_Data download](https://fortress.wa.gov/ecy/gispublic/DataDownload/wr/GWIS_Data/). Data made available can be found within the **GWIS_SDEexport.zip** option.
- D_PointTable.csv, obtained from above GWIS_SDEexport.zip.
- D_Point_WR_Doc.csv, obtained from above GWIS_SDEexport.zip.
- Person_Plus_EXTRACT_FromWRTSnotGWIS.csv, obtained from above GWIS_SDEexport.zip.
- [GWIS_Data_Dictionary](https://fortress.wa.gov/ecy/gispublic/DataDownload/wr/GWIS_Data/GWIS_Data_Dictionary/).  Used to interpret and understand the WA data.


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share WSDE's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *WA_Allocation Schema Mapping_WaDEQA.xlsx*.  Six executable code files were used to extract the WSDE's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those six code files are as follows...

- 0_PreProcessWashingtonAllocationData.ipynb
- 1_WA_Methods.py
- 2_WA_Variables.py
- 3_WA_Organizations.py
- 4_WA_WaterSources.py
- 5_WA_Sites.py
- 6_WA_AllocationsAmounts_facts.py


***
### 0) Code File: 0_PreProcessWashingtonAllocationData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - D_PointTable.csv
 - D_Point_WR_Doc.csv
 - Person_Plus_EXTRACT_FromWRTSnotGWIS.csv

#### Outputs:
 - P_WashingtonMaster.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.
- Left Join D_PointTable.csv -to- D_Point_WR_Doc.csv via **D_Point_ID**, and Person_Plus_EXTRACT_FromWRTSnotGWIS.csv via **WR_Doc_ID**.  Generate single output dataframe *df*.
- Format **PriorityDate** field to %m/%d/%Y format.
- Fill in blank **WaRecRCWClassTypeCode** with *Unknown* values.
- Drop rows with null **WaRecPhaseTypeCode** values, used for WaDE specific *AllocationTypeCV* field.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_WashingtonMaster.csv*.


***
### 1) Code File: 1_WA_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

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
WSDE_Water Rights | Surface Ground | Adjudicated


***
### 2) Code File: 2_WA_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

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
WSDE_Allocation All | 1 | Year | CFS


***
### 3) Code File: 3_WA_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

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
WSDE | Washington State Department of Ecology | Riddle, H. Nicholas | HRID461@ECY.WA.GOV


***
### 4) Code File: 4_WA_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_WashingtonMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

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


***
### 5) Code File: 5_WA_Sites.py
Purpose: generate a list of sites where water is diverted (also known as Points Of Diversion, PODs).

#### Inputs:
- P_WashingtonMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to the *WaDE Site* specific columns.  See *WA_Allocation Schema Mapping_WaDEQA.xlsx* for specific details.  Items of note are as follows...
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
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteNativeID
---------- | ---------- | ------------ | ------------ | ------------
WAwr_S1 | field checked with GPS | 46.5836906784566 | -119.798723819468 | 200889

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_WA_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_WashingtonMaster.csv
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
- Assign state agency info to the *WaDE Water Allocations* specific columns.  See *WA_Allocation Schema Mapping_WaDEQA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
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
- WaterSourceUUID
- SiteUUID
- AllocationPriorityDate
- BeneficialUseCategory
- AllocationAmount or AllocationMaximum
- DataPublicationDate


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Washington State Department of Ecology (WSDE)](https://ecology.wa.gov/Water-Shorelines/Water-supply/Water-rights).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

WSDE Staff
- asdf