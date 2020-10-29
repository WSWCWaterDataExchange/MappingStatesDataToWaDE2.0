# IDWR Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Idaho Department of Water Resources (IDWR)](https://idwr.idaho.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Data Utilized
The following data was used for water allocations...

- Point of diversion (POD) data was obtained from IDWR Maps and GIS Data Hub at: https://data-idwr.opendata.arcgis.com/datasets/water-right-pods
- Point of use (PoU) data was obtained from a zipped file from IDWR Maps and GIS Data Hub at: https://data-idwr.opendata.arcgis.com/pages/gis-data#WaterRights
- Extended contact names with field names were provided by the IDWR staff via contact to address missing owner information.

Two unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - ID_Water_Right_PODs_input.xlsx
 - ID_Water_Right_PoUs_input.xlsx
 - IdwrExtendedContactNamesWithFieldNames_input.xlsx

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share IDWR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *ID_Allocation Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the IDWR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those six code files are as follows...

- 0_PreProcessIdahoAllocationData.ipynb
- 1_ID_Methods
- 2_ID_Variables
- 3_ID_Organizations
- 4_ID_WaterSources
- 5_ID_Sites
- 6_ID_AllocationsAmounts_facts


***
### 0) Code File: 0_PreProcessIdahoAllocationData.ipynb
Purpose: Pre-process the Idaho input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - ID_Water_Right_PODs_input.xlsx
 - ID_Water_Right_PoUs_input.xlsx
 - IdwrExtendedContactNamesWithFieldNames_input.xlsx

#### Outputs:
 - P_IdahoMaster.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.
- Left Join PoU data to the POD data via matching **RightsID** field to generate single output dataframe *df*.
- Format **PriorityDate** field to %m/%d/%Y format.
- Generate WaDE Specific Field *WaterSourceType* from IDWR **Source** field (see pre-process code for specific dictionary used to determine water type).
- Generate WaDE Specific Field *SiteType* from IDWR **Source** field (see pre-process code for specific dictionary used to determine water type).
- Extract correct owner name from Extended Contact Name data, generate *Owner_Update* for input.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_IdahoMaster.csv*.


***
### 1) Code File: 1_ID_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **IDWR** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
IDWR_Diversion Tracking | Surface Ground Water | Water Use


***
### 2) Code File: 2_ID_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **IDWR** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
IDWR_Allocation All | 1 | Year | CFS


***
### 3) Code File: 3_ID_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **IDWR** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
IDWR | Idaho Dept. of Water Rights | Linda Davis | https://idwr.idaho.gov/


***
### 4) Code File: 4_ID_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_IdahoMaster.csv

#### Outputs:
- WaterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **IDWR** info to the *WaDE WaterSources* specific columns.  See *ID_Allocation Schema Mapping to WaDE_QA* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = generated list of sources from **Source**, see *0_PreProcessIdahoAllocationData.ipynb* for specifics.
    - *WaterSourceName* = **Source**, Unspecified if not given.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
ID_WS3 | Unspecified | DEEP CREEK | Unspecified | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_ID_Sites.py
Purpose: generate a list of sites where water is diverted (also known as Points Of Diversion, PODs).

#### Inputs:
- P_IdahoMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **IDWR** info to the *WaDE Site* specific columns.  See *ID_Allocation Schema Mapping to WaDE_QA* for specific details.  Items of note are as follows...
    - *CoordinateMethodCV* = **DataSource**, Unspecified if not given.
    - *Latitude* = converted **X** projection from IDWR EPSG:8826 -to- WaDE EPSG:4326.
    - *Longitude* = converted **Y** projection from IDWR EPSG:8826 -to- WaDE EPSG:4326.
    - *SiteName* = **DiversionName**, Unspecified if not given.
    - *SiteNativeID* = **PointOfDiversionID**, Unspecified if not given.
    - *SiteTypeCV* = generated list of sources from **Source**, see *0_PreProcessIdahoAllocationData.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName* & *SiteTypeCV* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ------------ | ------------ | ------------
ID_S9 | Digitized | 43.6997001071638 | -116.354766990569 | EAGLE ELEMENTARY WELL #1

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_ID_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_IdahoMaster.csv
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
- Assign **IDWR** info to the *WaDE Water Allocations* specific columns.  See *ID_Allocation Schema Mapping to WaDE_QA* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationAmount* = **OverallMaxDiversionRate**.
    - *AllocationLegalStatusCV* = **Basis**, Unknown if not given.
    - *AllocationNativeID* = **RightID**.
    - *AllocationOwner* = **Owner_Update**, see *0_PreProcessIdahoAllocationData.ipynb* for specifics.
    - *AllocationPriorityDate* = **PriorityDate**.
    - *AllocationTypeCV* = **Status**, Unknown if not given.
    - *BeneficialUseCategory* = **WaterUse_**, Unspecified if not given.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationAmount | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
10000 | 0.04 | License | DOMESTIC

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
