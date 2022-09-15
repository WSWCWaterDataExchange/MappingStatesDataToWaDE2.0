# IDWR Water Rights (Allocation) Data Preparation for WaDE

This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Idaho Department of Water Resources (IDWR)](https://idwr.idaho.gov/), for inclusion into the Water Data Exchange (WaDE) project. WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes.

## Overview of Source Data Utilized

The following data was used for water allocations...

- Point of diversion (POD) data was obtained from IDWR Maps and GIS Data Hub at: https://data-idwr.hub.arcgis.com/datasets/IDWR::water-right-pods/about
- Point of use (PoU) data was obtained from a zipped file from IDWR Maps and GIS Data Hub at: https://idwr.maps.arcgis.com/home/item.html?id=dcadb8412de74f468ce802d61361ca0a

Unique files were created from the above links to be used as input to the Python codes that prepare WaDE2 input files. Input files used are as follows...

- ID_Water_Right_PODs_input.xlsx
- ID_Water_Right_PoUs_input.xlsx

## Storage for WaDE 2.0 Source and Processed Water Data

The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive. Please contact WaDE staff if unavailable or if you have any questions about the data.

- Idaho Allocation Data: https://drive.google.com/drive/folders/1HYjr3B-CPqZ9ncEi_BClax2ADO1rhy5k?usp=sharing

## Summary of Data Prep

The following text summarizes the process used by the WSWC staff to prepare and share IDWR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project. For a complete mapping outline, see _ID_Allocation Schema Mapping to WaDE_QA.xlsx_. Seven executable code files were used to extract the IDWR's water rights data from the above mentioned input files. Each code file is numbered for order of operation. The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining six code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files. Those seven code files are as follows...

- 0_PreProcessIdahoAllocationData.ipynb
- 1_ID_Methods
- 2_ID_Variables
- 3_ID_Organizations
- 4_ID_WaterSources
- 5_ID_Sites
- 6_ID_AllocationsAmounts_facts
- 7_IDwr_PODSiteToPOUSiteRelationships.py

---

### 0) Code File: 0_PreProcessIdahoAllocationData.ipynb

Purpose: Pre-process the Idaho input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs:

- ID_Water_Right_PODs_input.xlsx
- ID_Water_Right_PoUs_input.xlsx

#### Outputs:

- P_IdahoMaster.csv

#### Operation and Steps:

- Read the input files and generate temporary input dataframes. Goal will be to create separate POD and POU centric dataframes, then join together into single output dataframe.
  - For POD data...
  - Left Join POU data to the POD data via matching **RightsID** for use and acreage info.
  - Convert given EPSG 8826 project to WaDE friendly EPSGS 4326.
  - Assign irrigate acreage using **AcreLimit** if > 0, else use **TotalAcres**.
  - Create WaDE POD centric temporary dataframe. Extract ID POD relevant data (see preprocessing code).
- For POU data...
  - Left Join POD data to the POU data via matching **RightsID** for owner, CFS, legal status & basis info.
  - Assign irrigate acreage using **AcreLimit** if > 0, else use **TotalAcres**.
  - Generate WaDE Specific Field _WaterSourceType_ from IDWR **Source** field (see pre-process code for specific dictionary used to determine water type).
  - Extract correct owner name from Extended Contact Name data, generate _Owner_Update_ for input.
  - Create WaDE POU centric temporary dataframe. Extract ID POU relevant data (see preprocessing code).
- Concatenate temporary POD & POU dataframes together into single long output dataframe.
  - Clean text used for water right native ID.
  - Remove special characters from water right owner info.
  - Format **PriorityDate** field to %m/%d/%Y format.
  - Generate WaDE Specific Field _WaterSourceType_ from IDWR **Source** field (see pre-process code for specific dictionary used to determine water type).
  - Generate WaDE specific field _WaterSourceNativeID_ from WaDE **Source** field. Used to identify unique sources of water.
- Extract geometry info from POU shapefile.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, _P_IdahoMaster.csv_.

---

### 1) Code File: 1_ID_Methods.py

Purpose: generate legend of granular methods used on data collection.

#### Inputs:

- None

#### Outputs:

- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:

- Generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE Method_ specific columns.
- Assign **IDWR** info to the _WaDE Method_ specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe _methods.csv_.

#### Sample Output (WARNING: not all fields shown):

| MethodUUID | ApplicableResourceTypeCV | MethodTypeCV |
| ---------- | ------------------------ | ------------ |
| IDwr_M1    | Surface Ground Water     | Water Use    |

---

### 2) Code File: 2_ID_Variables.py

Purpose: generate legend of granular variables specific to each state.

#### Inputs:

- None

#### Outputs:

- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:

- Generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE Variable_ specific columns.
- Assign **IDWR** info to the _WaDE Variable_ specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe _variables.csv_.

#### Sample Output (WARNING: not all fields shown):

| VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV |
| -------------------- | ------------------------- | ---------------------- | ------------ |
| IDwr_V1              | 1                         | Year                   | CFS          |

---

### 3) Code File: 3_ID_Organizations.py

Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:

- None

#### Outputs:

- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:

- Generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE Organizations_ specific columns.
- Assign **IDWR** info to the _WaDE Organizations_ specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe _organizations.csv_.

#### Sample Output (WARNING: not all fields shown):

| OrganizationUUID | OrganizationName            | OrganizationContactName | OrganizationWebsite     |
| ---------------- | --------------------------- | ----------------------- | ----------------------- |
| IDwr_O1          | Idaho Dept. of Water Rights | Linda Davis             | https://idwr.idaho.gov/ |

---

### 4) Code File: 4_ID_WaterSources.py

Purpose: generate a list of water sources specific to a water right.

#### Inputs:

- P_IdahoMaster.csv

#### Outputs:

- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:

- Read the input file and generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE WaterSources_ specific columns.
- Assign **IDWR** info to the _WaDE WaterSources_ specific columns. See _ID_Allocation Schema Mapping to WaDE_QA_ for specific details. Items of note are as follows...
  - _WaterSourceTypeCV_ = generated list of sources from **Source**, see _0_PreProcessIdahoAllocationData.ipynb_ for specifics.
  - _WaterSourceName_ = **Source**, Unspecified if not given.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific _WaterSourceName_ & _WaterSourceTypeCV_ fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe _WaterSources.csv_.

#### Sample Output (WARNING: not all fields shown):

| WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV |
| --------------- | ----------------------- | --------------- | ------------------- | ----------------- |
| ID_WS3          | Fresh                   | DEEP CREEK      | Unspecified         | Surface Water     |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. _watersources_missing.csv_) for review. This allows for future inspection and ease of inspection on missing items. Mandatory fields for the water sources include the following...

- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV

---

### 5) Code File: 5_ID_Sites.py

Purpose: generate a list of sites where water is diverted (also known as Points Of Diversion, PODs).

#### Inputs:

- P_IdahoMaster.csv
- waterSources.csv

#### Outputs:

- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:

- Read the input file and generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE Site_ specific columns.
- Assign **IDWR** info to the _WaDE Site_ specific columns. See _ID_Allocation Schema Mapping to WaDE_QA_ for specific details. Items of note are as follows...
  - Extract _WaterSourceUUID_ from waterSources.csv input csv file. See code for specific implementation of extraction.
  - _CoordinateMethodCV_ = **DataSource**, Unspecified if not given. Centroid if POU data.
  - _Latitude_ = converted **X** projection from IDWR EPSG:8826 -to- WaDE EPSG:4326. Centroid of polygon for POU data.
  - _Longitude_ = converted **Y** projection from IDWR EPSG:8826 -to- WaDE EPSG:4326. Centroid of polygon for POU data.
  - _SiteName_ = **DiversionName**, Unspecified if not given.
  - _SiteNativeID_ = **PointOfDiversionID**, Unspecified if not given.
  - _SiteTypeCV_ = Unspecified.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific _SiteNativeID_, _SiteName_ & _SiteTypeCV_ fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe _sites.csv_.

#### Sample Output (WARNING: not all fields shown):

| SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude         | Longitude         | SiteName                 |
| -------- | --------------- | ------------------ | ---------------- | ----------------- | ------------------------ |
| ID_S9    | IDwr_WS1        | Digitized          | 43.6997001071638 | -116.354766990569 | EAGLE ELEMENTARY WELL #1 |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. _sites_missing.csv_) for review. This allows for future inspection and ease of inspection on missing items. Mandatory fields for the sites include the following...

- SiteUUID
- CoordinateMethodCV
- EPSGCodeCV
- SiteName

---

### 6) Code File: 6_ID_AllocationsAmounts_facts.py

Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:

- P_IdahoMaster.csv

#### Outputs:

- waterallocations.csv
- waterallocations_missing.csv (error check only)

#### Operation and Steps:

- Read the input files and generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE Water Allocations_ specific columns.
- Assign **IDWR** info to the _WaDE Water Allocations_ specific columns. See _ID_Allocation Schema Mapping to WaDE_QA_ for specific details. Items of note are as follows...
  - Extract _MethodUUID_, _VariableSpecificUUID_, _OrganizationUUID_, & _SiteUUID_ from respective input csv files. See code for specific implementation of extraction.
  - _AllocationBasisCV_ = **Basis**.
  - _AllocationFlow_CFS_ = **OverallMaxDiversionRate**.
  - _AllocationLegalStatusCV_ = **Status**.
  - _AllocationNativeID_ = **WaterRightNumber**.
  - _AllocationOwner_ = **Owner**.
  - _AllocationPriorityDate_ = **PriorityDate**.
  - _BeneficialUseCategory_ = **WaterUse**, Unspecified if not given.
  - _IrrigatedAcreage_ = 'If **AcreLimit** > 0, = **AcreLimit**, else use **TotalAcre**.
  - _WaterAllocationNativeURL_ = **WRDocs**.
- Consolidate output dataframe into water allocations specific information only by grouping entries by _AllocationNativeID_ filed.
- Perform error check on output dataframe.
- Export output dataframe _waterallocations.csv_.

#### Sample Output (WARNING: not all fields shown):

| AllocationUUID | MethodUUID | OrganizationUUID | SiteUUID                  | VariableSpecificUUID | AllocationFlow_CFS | AllocationPriorityDate | BeneficialUseCategory |
| -------------- | ---------- | ---------------- | ------------------------- | -------------------- | ------------------ | ---------------------- | --------------------- |
| IDwr_WR1       | IDwr_M1    | IDwr_O1          | IDwr_S406997,IDwr_S153532 | IDwr_V1              | 180                | 4/1/1939               | IRRIGATION            |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. _waterallocations_missing.csv_) for review. This allows for future inspection and ease of inspection on missing items. Mandatory fields for the water allocations include the following...

- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- SiteUUID
- AllocationPriorityDate
- BeneficialUseCategory
- AllocationAmount or AllocationMaximum
- DataPublicationDate

---

### 7) Code File: 7_IDwr_PODSiteToPOUSiteRelationships.py

Purpose: generate linking element between POD and POU sites that share the same water right.
Note: podsitetopousiterelationships.csv output only needed if both POD and POU data is present, otherwise produces empty file.

#### Inputs:

- sites.csv

#### Outputs:

- podsitetopousiterelationships.csv

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

---

## Staff Contributions

Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Idaho Department of Water Resources (IDWR)](https://idwr.idaho.gov/).

WSWC Staff

- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

IDWR Staff

- Linda Davis <linda.davis@idwr.idaho.gov>
- Danielle Favreau <Danielle.Favreau@idwr.idaho.gov>
- Dan Narsavage <Dan.Narsavage@idwr.idaho.gov>
- Phil Blankenau <phil.blankenau@idwr.idaho.gov>
