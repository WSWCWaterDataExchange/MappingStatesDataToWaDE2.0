# OWRD Water Rights (Allocation amounts) Data Preparation for WaDE
This read me details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Oregon Water Resources Department (OWRD)](https://www.oregon.gov/OWRD/access_Data/Pages/Data.aspx), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined way that allows regional analysis to inform planning purposes.  WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Data Utilized
The following data was used for water rights...

- [**Oregon Access Data Maps.**](https://www.oregon.gov/OWRD/access_Data/Pages/Data.aspx)  The data used here were downloaded from the **"Statewide Water Right Spatial Data with Metadata"**, which contained spatial data for Points of Diversions (PODs) and Points of Use (POUs) in a shapefile format.  Data was imported into [ArcGIS PRO](https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview), then exported table into csv file format.
- [**Oregon Water Right Points of Diversion**](https://arcgis.wrd.state.or.us/data/wr_pod_metadata.pdf) was used to translate and understand the data.
- [**Oregon Water Right Places of Use**](https://arcgis.wrd.state.or.us/data/wr_pou_metadata.pdf) was used to translate and understand the data.

From the available state agency data, the following input files were created, which were used as input to the Python codes that prepares WaDE 2.0 input files.  Input files used are as follows...
 - ORwr_v_pod_public_input.csv


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share OWRD's water right data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *Oregon_Allocation Schema Mapping to WaDE_QA*.  Six executable code files were used to extract the state agencies site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(AllocationAmounts_facts)* is dependent on the previous files.  Those six code files are as follows...

- 0_PreProcessOregonAllocationData.ipynb
- 1_OR_Methods.py
- 2_OR_Variables.py
- 3_OR_Organizations.py
- 4_OR_WaterSources.py
- 5_OR_Sites.py
- 6_OR_AllocationsAmounts_facts.py


***
### 0) Code File: 0_PreProcessOregonAllocationData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - ORwr_v_pod_public_input.csv

#### Outputs:
 - P_OregonMaster.csv
 - inputOregonDataRemoved.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.
- Format **priority_date** field to %m/%d/%Y format.
- Generate WaDE *Owner* by determining company vs individual using **name_company**, **name_last**, and **name_first** input fields. Concatenating name of individual.
- Formate string for WaDE *TimeframeStart* and *TimeframeEnd* fields.  Use **begin_month** and **begin_day** input fields.
- Format string for WaDE *BeneficialUse**.  Use **use_code_description** input field.  Need to remove special characters.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_OregonMaster.csv*.
- Export all input data rows removed for future review (see *inputOregonDataRemoved.csv*).


***
### 1) Code File: 1_OR_Methods.py
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
OWRD_Water Rights | Surface Ground Storage | Adjudicated


***
### 2) Code File: 2_OR_Variables.py
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
OWRD_Allocation All | 1 | Year | CFS


***
### 3) Code File: 3_OR_Organizations.py
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
OWRD | Oregon Water Resources Department | Tom Byler | https://www.oregon.gov/OWRD/


***
### 4) Code File: 4_OR_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_OregonMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency info to the *WaDE WaterSources* specific columns.  See *Oregon_Allocation Schema Mapping to WaDE_QA* for specific details.  Items of note are as follows...
    - *WaterSourceName* = **source**, Unknown if not given.
    - *WaterSourceTypeCV* = **wr_type**, Unknown if not given.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
OR_1 | Fresh | FORMOSA 1 ADIT | Unspecified | groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_OR_Sites.py
Purpose: generate a list of sites where water is diverted (also known as Points Of Diversion, PODs).

#### Inputs:
- P_OregonMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to the *WaDE Site* specific columns.  See *Oregon_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *Latitude* = converted **POINT_X** projection from OWRD EPSG:2992 -to- WaDE EPSG:4326.
    - *Longitude* = converted **POINT_Y** projection from OWRD EPSG:2992 -to- WaDE EPSG:4326.
    - *SiteName* = concatenate **snp_id** & **pod_nbr** together. Unspecified if not given.
    - *SiteNativeID* = **pod_location_id**.
    - *SiteTypeCV* = **source_type** & **pod_nbr**, Unknown if not given.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ------------ | ------------ | ------------
OR_1 | Unspecified | 42.855812902123 | -123.382876619485 | 21755_1

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_OR_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_OregonMaster.csv
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
- Assign stage agency info to the *WaDE Water Allocations* specific columns.  See *Oregon_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationAmount* = **rate_cfs**.
    - *AllocationMaximum* = **max_rate_acre_feet**.
    - *AllocationNativeID* = **snp_id**.
    - *AllocationOwner* = **Owner**.
    - *AllocationPriorityDate* = **priority_date**.
    - *AllocationTypeCV* = **claim_char**, Unspecified if not given.
    - *BeneficialUseCategory* = **use_code_description**, Unknown if not given.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationAmount | AllocationPriorityDate | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
100001 | 0.01 | 6/3/1976 | DOMESTIC INCLUDING LAWN AND GARDEN

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Oregon Water Resources Department (OWRD)](https://www.oregon.gov/OWRD/access_Data/Pages/Data.aspx).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

OWRD Staff
- 