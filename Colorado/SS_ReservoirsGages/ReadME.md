# CODWR Site Specific Reservoir and Dage Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting Site Specific Reservoir and Gage data stream time series water data made available by the [Colorado Division of Water Resources (CODWR)](https://dwr.colorado.gov/about-us/contact-us/denver-office), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for aggregated water budget...

- [**Division Data**](https://dwr.state.co.us/Rest/GET/Help/Api/GET-api-v2-structures-divrec-waterclasses) api from Colorado CDSS REST web services for Division 1-7, with a focus on retrieving wdid data that is **divrectype = WaterClass**, **availableTimesteps = Year**,** and **ciuCode = A** (for active) values only.
- [**Annual WDID Time Series Data**](https://dwr.state.co.us/Rest/GET/Help/Api/GET-api-v2-structures-divrec-divrecyear) api from Colorado CDSS REST web services using wdid list produced from Division 1-7.


Unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - *dfs.xlsx*, which contains division site data.
 - *P_TimeSeries.xlsx*, which contains timeseries data.

 ## Storage for WaDE2 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE2 database, can both be found within the WaDE2 sponsored Google Drive.  Please contact WaDE2 staff if unavailable or if you have any questions about the data.
- Colorado Site Specific Reservoir and Gage Data: https://drive.google.com/drive/folders/1WNOBKKMvapGmaCWrHIzXBAAgfQlCdLOQ?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CODWR's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *CO_SS_ReservoirGageSchema Mapping to WaDE.xlsx*.  Six executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those six code files are as follows...

- 0_PreProcessCOReservoirGages.ipynb
- 1_COssrg_Methods.py
- 2_COssrg_Variables.py
- 3_COssrg_Organizations.py
- 4_COssrg_WaterSources.py
- 5_COssrg_Sites.py
- 6_COssrg_SiteSpecificAmounts_fact.py


***
### 0) Code File: 0_PreProcessCOReservoirGages.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - dfs.xlsx
 - P_TimeSeries.xlsx

#### Outputs:
 - P_coOSMain.csv

#### Operation and Steps:
- For site data...
    - Use Colorado CDSS REST [**Division Data**](https://dwr.state.co.us/Rest/GET/Help/Api/GET-api-v2-structures-divrec-waterclasses) web services to acquire Division Records searching waterclasses data for division 1-7. Save data and generate temporary input **Division** dataframe per division.  Export results to save on future query time.
    - Read in inputs for site data for Division data 1-7.
    - We only want **divrectype** = "DivTotal" for total value, **availableTimesteps** = "Year" for annual value, **ciuCode** = "A" for total Active sites only.
    - Fix **wdid** values that are less then 7 chars long.  Insert a "0" value.
    - Concatenate all sites into single stie dataframe.
- For timeseries data...
  - Using **wdid** list as input into [**Annual WDID Time Series Data**](https://dwr.state.co.us/Rest/GET/Help/Api/GETCOos_M1-api-v2-structures-divrec-divrecyear) web service to retrieve time series info for each wdid of interest. Export results to save on future query time.
  - We only want **measInterval** = "annual" for annual records.
- Merge site with timeseries dataframe using unique key value generated from **wdid** and **waterClassNum**.
- Assign data to WaDE specific fields.
- Generate WaDE specific field *WaterSourceTypeCV* from **waterSource** field.  Separate out between Surface Water and Groundwater.
- Generate WaDE specific field *WaterSourceNativeID* from **waterSource** field.  Used to identify unique sources of water.
- Generate WaDE specific *VariableSpecificCV* from **waterSource** field.  Helps seperate out time series.
- Generate WaDE specific *TimeframeStart* & *TimeframeEnd* fields. Assume start date is 01/01/ + **dataMeasDate** and end date is 12/31/ + **dataMeasDate**.
- Export output dataframe as new csv file, *P_coOSMain.csv*.



***
### 1) Code File: 1_COssrg_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign state agency data info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
COssrg_M1 | Surface Ground Water | Water Use



***
### 2) Code File: 2_COssrg_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign state agency data info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV | VariableCV | VariableSpecificCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------
COssrg_V1 | 1 | Year | AF | Stream Gage | Stream Gage_Annual_DivTotal_Surface Water



***
### 3) Code File: 3_COssrg_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign state agency data info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
COssrg_O1 | Colorado Division of Water Resources| Doug Stenzel | https://dwr.colorado.gov/about-us/contact-us/denver-office



***
### 4) Code File: 4_COssrg_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_coOSMain.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency info to columns.  See *CO_SS_ReservoirGageSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourcetypeCV* = **WaterSourceName**, see *0_PreProcessCOReservoirGages.ipynb* for specifics. 
    - *WaterSourceName* = **WaterSourceName**.
    - *WaterSourceNativeID* = *in_WaterSourceNativeID*, see *0_PreProcessCOReservoirGages.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
COssrg_WS1 | Fresh | SOUTH PLATTE RIVER | WaDECO_WS1 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_COssrg_Sites.py
Purpose: generate a list of polygon areas associated with the state agency specific site on aggregated water budget data.

#### Inputs:
- P_coOSMain.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to columns.  See *CO_SS_ReservoirGageSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersource.csv input file. See code for specific implementation of extraction.
    - *County* = **county**.
    ` *GNISCodeCV* = **gnisId**.
    - *Latitude* = **latdecdeg**.
    - *Longitude* = **longdecdeg**.
    - *SiteName* = **structureName**.
    - *SiteNativeID* = **wdid**.
    - *SiteTypeCV* = **structureType**.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID |CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID | SiteTypeCV
---------- | ---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
COssrg_S1 | COssrg_WS1 | Unspecified | 39.491687 | -103.731685 | MIDDLEMIST DITCH 2 | 100539 | DITCH

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_COssrg_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific time series water data to import into WaDE 2.0.

#### Inputs:
- P_coOSMain.csv
- methods.csv
- variables.csv
- organizations.csv
- watersources.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Site Specific Amounts* data columns.
- Assign state agency data info to columns.  See *CO_SS_ReservoirGageSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **dataValue**.
    - *BeneficialUseCategory* = "DivTotal"
    - *ReportYearCV* = **dataMeasDate**.
    - *TimeframeStart* = 01/01/ + **dataMeasDate**.  See *0_PreProcessCOReservoirGages.ipynb* for specific on generation.
    - *TimeframeEnd* = 12/31/ + **dataMeasDate**.  See *0_PreProcessCOReservoirGages.ipynb* for specific on generation.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
COssrg_M1| COssrg_O1 | COssrg_S1 | COos_V11 | COssrg_WS1 | 971.92 | DivTotal | 1974 | 1/1/1974 | 12/31/1974

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- SiteUUID
- Amount
- BeneficialUseCategory
- DataPublicationDate
- TimeframeEnd
- TimeframeStart


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Colorado Division of Water Resources (CODWR)](https://dwr.colorado.gov/about-us/contact-us/denver-office).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

CODWR Staff
- Doug Stenzel <doug.stenzel@state.co.us>