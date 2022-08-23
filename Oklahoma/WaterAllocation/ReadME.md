# OWRB Water Rights (Allocation) Data Preparation for WaDE

This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Oklahoma Water Resources Board (OWRB)](https://www.owrb.ok.gov/), for inclusion into the Water Data Exchange (WaDE) project. WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes.

## Overview of Source Data Utilized

The following data was used for water allocations...

- Permitted Surface Water Diversion Points: http://home-owrb.opendata.arcgis.com/datasets/permitted-surface-water-diversion-points?geometry=-119.379%2C31.373%2C-77.565%2C37.701
- Permitted Groundwater Wells (Point coverage): https://home-owrb.opendata.arcgis.com/datasets/permitted-groundwater-wells
- Area of Use data: https://home-owrb.opendata.arcgis.com/datasets/areas-of-use?geometry=-109.718%2C33.749%2C-87.404%2C36.886

These datasets were saved to a local csv file copy to be used as input to the Python codes that prepare WaDE2 input files. Files can be found in the [RawInputData Folder](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Oklahoma/WaterAllocation/RawInputData)/ Input files used are as follows...

- Permitted_Groundwater_Wells.csv
- Permitted_Surface_Water_Diversion_Points.csv
- OK_AreasofUse.csv

## Storage for WaDE 2.0 Source and Processed Water Data

The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive. Please contact WaDE staff if unavailable or if you have any questions about the data.

- Oklahoma Allocation Data: https://drive.google.com/drive/folders/183InFU3MOyzxPx4r2e2FI6rU8-bIayOG?usp=sharing

## Summary of Data Prep

The following text summarizes the process used by the WSWC staff to prepare and share OWRB's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project. For a complete mapping outline, see _OK_Allocation Schema Mapping to WaDE_QA.xlsx_. Eight executable code files were used to extract the OWRB's water rights data from the above mentioned input files. Each code file is numbered for order of operation. The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining seven code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The code file _(AllocationsAmounts_facts.py)_ is depended on the previous files. Those Seven code files are as follows...

- 0_PreProcessOklahomaAllocationData.ipynb
- 1_OKwr_Methods.py
- 2_OKwr_Variables.py
- 3_OKwr_Organizations.pys
- 4_OKwr_WaterSources.py
- 5_OKwr_Sites.py
- 6_OKwr_AllocationsAmounts_facts.py
- 7_OKwr_PODSiteToPOUSiteRelationships.py

---

### 0) Code File: 0_PreProcessOklahomaAllocationData.ipynb

Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs:

- Permitted_Groundwater_Wells.csv
- Permitted_Surface_Water_Diversion_Points.csv
- OK_AreasofUse.csv

#### Outputs:

- P_OklahomaMaster.csv

#### Operation and Steps:

- Read in the input files. Goal will be to create separate POD and POU centric dataframes, then join together for single long output dataframe. POD & POU data share similar fields.
- For POD data...
  - Concatenate Permitted_Groundwater_Wells.csv & Permitted_Surface_Water_Diversion_Points.csv into one long dataframe. Both share similar fields.
  - Set WaDE _PODorPOUSite_ field = POD.
  - Format **DATE_FILED** & **DATE_ISSUED** fields to %m/%d/%Y format.
- For POU data...
  - Set WaDE _PODorPOUSite_ field = POU.
  - Format **DATE_FILED** & **DATE_ISSUED** fields to %m/%d/%Y format.
- Concatenate temporary POD & POU dataframes together into single long output dataframe.
- Format strings from **PRIMARY_PURPOSE** to reduce errors.
- Format strings from **ENTITY_NAME** to reduce owner name error.
- Generate WaDE specific field _SiteNativeID_ from WaDE _Latitude_, _Longitude_, & _PODorPOUSite_ fields. Used to identify unique sites.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, _P_OklahomaMaster.csv_.

---

### 1) Code File: 1_OKwr_Methods.py

Purpose: generate legend of granular methods used on data collection.

#### Inputs:

- None

#### Outputs:

- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:

- Generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE Method_ specific columns.
- Assign **OWRB** info to the _WaDE Method_ specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe _methods.csv_.

#### Sample Output (WARNING: not all fields shown):

| MethodUUID | ApplicableResourceTypeCV | MethodTypeCV     |
| ---------- | ------------------------ | ---------------- |
| OKwr_M1    | Surface Ground Water     | Water Allocation |

---

### 2) Code File: 2_OKwr_Variables.py

Purpose: generate legend of granular variables specific to each state.

#### Inputs:

- None

#### Outputs:

- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:

- Generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE Variable_ specific columns.
- Assign **OWRB** info to the _WaDE Variable_ specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe _variables.csv_.

#### Sample Output (WARNING: not all fields shown):

| VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV |
| -------------------- | ------------------------- | ---------------------- | ------------ |
| OKwr_V1              | 1                         | Year                   | CFS          |

---

### 3) Code File: 3_OKwr_Organizations.py

Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:

- None

#### Outputs:

- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:

- Generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE Organizations_ specific columns.
- Assign **OWRB** info to the _WaDE Organizations_ specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe _organizations.csv_.

#### Sample Output (WARNING: not all fields shown):

| OrganizationUUID | OrganizationName               | OrganizationContactName | OrganizationWebsite      |
| ---------------- | ------------------------------ | ----------------------- | ------------------------ |
| OKwr_O1          | Oklahoma Water Resources Board | David Hamilton          | https://www.owrb.ok.gov/ |

---

### 4) Code File: 4_OKwr_WaterSources.py

Purpose: generate a list of water sources specific to a water right.

#### Inputs:

- P_OklahomaMaster.csv

#### Outputs:

- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:

- Read the input file and generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE WaterSources_ specific columns.
- Assign **OWRB** info to the _WaDE WaterSources_ specific columns. See _OK_Allocation Schema Mapping to WaDE_QA.xlsx_ for specific details. Items of note are as follows...
  - _WaterSourceNativeID_ = Use custom made ID value.
  - _WaterSourceTypeCV_ = **WATER**, Unspecified if not given.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific _WaterSourceName_ & _WaterSourceTypeCV_ fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe _WaterSources.csv_.

#### Sample Output (WARNING: not all fields shown):

| WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV |
| --------------- | ----------------------- | --------------- | ------------------- | ----------------- |
| OKwr_WS2        | Fresh                   | Unspecified     | WaDEOK_WS1          | Groundwater       |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. _watersources_missing.csv_) for review. This allows for future inspection and ease of inspection on missing items. Mandatory fields for the water sources include the following...

- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV

---

### 5) Code File: 5_OKwr_Sites.py

Purpose: generate a list of sites information.

#### Inputs:

- P_OklahomaMaster.csv
- watersources.csv

#### Outputs:

- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:

- Read the input file and generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE Site_ specific columns.
- Assign **OWRB** info to the _WaDE Site_ specific columns. See _OK_Allocation Schema Mapping to WaDE_QA.xlsx_ for specific details. Items of note are as follows...
  - Extract _WaterSourceUUID_ from waterSources.csv input csv file. See code for specific implementation of extraction.
  - _County_ = **COUNTY**.
  - _HUC8_ = **HYDRO_UNIT**, empty if not provided.
  - _Latitude_ = **LATITUDE**.
  - _Longitude_ = **LONGITUDE**.
  - _SiteNativeID_ = **OBJECTID**, Unspecified if not given.
  - _SiteTypeCV_ = **WATER**.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific _SiteNativeID_, _SiteName_, _SiteTypeCV_, _Longitude_ & _Latitude_ fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe _sites.csv_.

#### Sample Output (WARNING: not all fields shown):

| SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude    | Longitude    | SiteName    | SiteTypeCV  |
| -------- | --------------- | ------------------ | ----------- | ------------ | ----------- | ----------- |
| OKwr_S1  | OKwr_WS1        | Unspecified        | 36.57472754 | -101.8963396 | Unspecified | Groundwater |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. _sites_missing.csv_) for review. This allows for future inspection and ease of inspection on missing items. Mandatory fields for the sites include the following...

- SiteUUID
- CoordinateMethodCV
- EPSGCodeCV
- SiteName

---

### 6) Code File: 6_OKwr_AllocationsAmounts_facts.py

Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:

- P_OklahomaMaster.csv
- methods.csv
- variables.csv
- organizations.csv
- sites.csv

#### Outputs:

- waterallocations.csv
- waterallocations_missing.csv (error check only)

#### Operation and Steps:

- Read the input files and generate single output dataframe _outdf_.
- Populate output dataframe with _WaDE Water Allocations_ specific columns.
- Assign **OWRB** info to the _WaDE Water Allocations_ specific columns. See _OK_Allocation Schema Mapping to WaDE_QA.xlsx_ for specific details. Items of note are as follows...
  - Extract _MethodUUID_, _VariableSpecificUUID_, _OrganizationUUID_, & _SiteUUID_ from respective input csv files. See code for specific implementation of extraction.
  - _AllocationApplicationDate_ = **DATE_FILED**.
  - _AllocationLegalStatusCV_ = **WR_STATUS**.
  - _AllocationVolume_AF_ = **TOTAL_PERMITTED_ACRE_FEET**.
  - _AllocationNativeID_ = **PERMIT_NUMBER**.
  - _AllocationOwner_ = **ENTITY_NAME**.
  - _AllocationPriorityDate_ = **DATE_ISSUED**.
  - _AllocationTypeCV_ = **PERMIT_TYPE**.
  - _BeneficialUseCategory_ = **PRIMARY_PURPOSE**.
- Consolidate output dataframe into water allocations specific information only by grouping entries by _AllocationNativeID_ filed.
- Perform error check on output dataframe.
- Export output dataframe _waterallocations.csv_.

#### Sample Output (WARNING: not all fields shown):

| AllocationNativeID | AllocationLegalStatusCV | AllocationVolume_AF | BeneficialUseCategory |
| ------------------ | ----------------------- | ------------------- | --------------------- |
| 18960001           | ACTIVE                  | 52                  | STOCK                 |

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

### 7) Code File: 7_OKwr_PODSiteToPOUSiteRelationships.py

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

Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Oklahoma Water Resources Board (OWRB)](https://www.owrb.ok.gov/).

WSWC Staff

- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

OWRB Staff

- David Hamilton <david.hamilton@owrb.ok.gov>
