# NEDNR Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Nebraska Department of Natural Resources (NEDNR)](https://dnr.nebraska.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for water allocations...
- Surface water rights were obtained from [NEDNR API](https://NEDNR.nebraska.gov/IwipApi/swagger/ui/index#/).  Data from the API was exported to a hard copy for review (see below section *0) Code File: 0_PreProcessNebraskaAllocationData.ipynb* for details).
- **SurfaceWaterWebSimpleSearch_metaData.pdf** which contains metadata to translate water rights data terminology and fields, available at: https://NEDNR.nebraska.gov/media/WaterRights/SurfaceWaterWebSimpleSearch.pdf


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NEDNR's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *ID_Allocation Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the IDWR's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(AllocationAmounts_facts)_ is depended on the previous files.  Those six code files are as follows...

- 0_PreProcessNebraskaAllocationData.ipynb
- 1_NEwr_Methods.py
- 2_NEwr_Variables.py
- 3_NEwr_Organizations.py
- 4_NEwr_WaterSources.py
- 5_NEwr_Sites.py
- 6_NEwr_AllocationsAmounts_facts.py



***
### 0) Code File: 0_PreProcessNebraskaAllocationData.ipynb
Purpose: Pre-process the Idaho input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - None

#### Outputs:
 - NebraskaSurfaceWaterAPIData.xlsx
 - P_NebraskaMaster.csv
 - (optional) DataRemoved_NEDNR.xlsx

#### Operation and Steps:
- Use state agency API to to acquire data.  Save as dataframe (optional: export dataframe to xlsx for visual inspection).
- Format **PriorityDate** field to %m/%d/%Y format.
- Format **HUC12** to int datatype.
- Generate WaDE *BeneficialUseCV* using the **SurfaceWaterWebSimpleSearch_metaData.pdf** for reference.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_NebraskaMaster.csv*.
- (optional) Export error check dataframe *DataRemoved_NEDNR.xlsx*.  Used to track WaDE problematic fields and for state review.



***
### 1) Code File: 1_NEwr_Methods.py
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
NEDNR_Water Rights | Surface Water | Modeled



***
### 2) Code File: 2_NEwr_Variables.py
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
NEDNR_Allocation All | 1 | Year | CFS



***
### 3) Code File: 3_NEwr_Organizations.py
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
NEDNR | Nebraska Department of Natural Resources | Jennifer Schellpeper | https://dnr.nebraska.gov/



***
### 4) Code File: 4_NEwr_WaterSources.py
Purpose: generate a list of water sources specific to a water right.

#### Inputs:
- P_NebraskaMaster.csv

#### Outputs:
- WaterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency info to the *WaDE WaterSources* specific columns.  See *NE_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = **SourceName**, Unspecified if not given.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* field.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ 
NE_1 | Fresh | Wolf Creek | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_NEwr_Sites.py
Purpose: generate a list of sites where water is diverted and used.

#### Inputs:
- P_NebraskaMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to the *WaDE Site* specific columns.  See *NE_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *County* = **County**, Unspecified if not given.
    - *Latitude* = **Lat**.
    - *Longitude* = **Long**.
    - *SiteNativeID* = **PointOfDiversionID**.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude*, & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ------------ | ------------ | ------------
NE_1 | Unspecified | 40.0946892092528 | -96.5146943671114 | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_NEwr_AllocationsAmounts_facts.py
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Inputs:
- P_NebraskaMaster.csv
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
- Assign state agency info to the *WaDE Water Allocations* specific columns.  See *NE_Allocation Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationAmount* = **ProGrant**.
    - *AllocationLegalStatusCV* = **RightStatus**, Unspecified if not given.
    - *AllocationNativeID* = **ApplicationNumber**.
    - *AllocationPriorityDate* = **PriorityDate**.
    - *AllocationTypeCV* = **Status**, Unknown if not given.
    - *BeneficialUseCategory* = **RightUse**, Unknown if not given.  See *0_PreProcessNebraskaAllocationData.ipynb* for specifics on generation.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationAmount | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
A-10003 | 2.64 | Active | DIrrigation from Natural Stream

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nebraska Department of Natural Resources (NEDNR)](https://dnr.nebraska.gov/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

NEDNR Staff
- Jennifer Schellpepe <jennifer.schellpeper@nebraska.gov>
- Kim Menke <kim.menke@nebraska.gov>
- Jesse Bradley <Jesse.Bradley@nebraska.gov>
- Shea Winkler shea.winkler@nebraska.gov
- Dan Kloch <dan.kloch@nebraska.gov>
- Mike Thompson  <mike.thompson@nebraska.gov>
- Ryan Werne <ryan.werner@nebraska.gov>
- B J Green <bj.green@nebraska.gov>