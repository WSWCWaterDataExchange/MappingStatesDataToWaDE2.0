# CODWR Site Specific Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [Colorado Division of Water Resources (CODWR)](https://dwr.colorado.gov/about-us/contact-us/denver-office), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for aggregated water budget...

- [**Division Data**](https://dwr.state.co.us/Rest/GET/Help/Api/GET-api-v2-structures-divrec-waterclasses) api from Colorado CDSS REST web services for Division 1-7, with a focus on retrieving wdid data that is **divrectype = WaterClass**, **availableTimesteps = Year**,** and **ciuCode = A** (for active) values only.
- [**Annual WDID Time Series Data**](https://dwr.state.co.us/Rest/GET/Help/Api/GET-api-v2-structures-divrec-divrecyear) api from Colorado CDSS REST web services using wdid list produced from Division 1-7.


Unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - Division Data api data retrieval
 - Annual WDID Time Series Data api data retrieval

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CODWR's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *CO_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those six code files are as follows...

- 0_ColoradoPreProcessSiteSpecificData.ipynb
- 1_COss_Methods.py
- 2_COss_Variables.py
- 3_COss_Organizations.py
- 4_COss_WaterSources.py
- 5_COss_Sites.py
- 6_COss_SiteSpecificAmounts_fact.py
- 7_COss_PODSiteToPOUSiteRelationships.py


***
### 0) Code File: 0_ColoradoPreProcessSiteSpecificData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - Division Data api data retrieval
 - Annual WDID Time Series Data api data retrieval

#### Outputs:
 - P_coSSMaster.csv

#### Operation and Steps:
- Use Colorado CDSS REST [**Division Data**](https://dwr.state.co.us/Rest/GET/Help/Api/GET-api-v2-structures-divrec-waterclasses) web services to acquire Division Records searching waterclasses data for division 1-7. Save data and generate temporary input **Division** dataframe per division.
- For Division data 1-7 ...
    - Reduce **Division** dataframe down to those with the following values: **divrectype** = **WaterClass**, **availableTimesteps** = **Year**,** and **ciuCode** = **A** (for active) values only.
    - Fix formatting issue of ***wdid** field to include 7 chars (required for CDSS Rest Services).
    - Drop duplicate rows from reduced **Division** dataframe.
    - Produce **wdid** list from reduced **Division** dataframe.
    - Using **wdid** list as input into [**Annual WDID Time Series Data**](https://dwr.state.co.us/Rest/GET/Help/Api/GET-api-v2-structures-divrec-divrecyear) web service to retrieve time series info for each wdid of interest, place into temporary **WDID** datafame .
    - Merge resulting **WDID** datafame with **Division** datafame, merge on **wdid** fields.
    - Repeat for remaining divisions.
- Concatenate dataframes together to create single output dataframe.
- Generate WaDE specific field *WaterSourceTypeCV* from **waterSource** field.  Seperate out between Surface Water and Groundwater.
- Generate WaDE specific field *WaterSourceNativeID* from **waterSource** field.  Used to identify unique sources of water.
- Generate WaDE specific field *SiteNativeID* from **latdecdeg**, **longdecdeg**, **structureType** and **structureName** fields.  Used to identify unique sites.
- Generate WaDE specific *TimeframeStart* & *TimeframeEnd* fields. Assume start date is 01/01/ + **dataMeasDate** and end date is 12/31/ + **dataMeasDate**.
- Export output dataframe as new csv file, *P_coSSMaster.csv*.



***
### 1) Code File: 1_COss_Methods.py
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
CO_Water Use Data | Surface Ground Water | Water Use



***
### 2) Code File: 2_COss_Variables.py
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
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
CO_Reservoirs and Gages | 1 | Year | AF



***
### 3) Code File: 3_COss_Organizations.py
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
CODWR | Colorado Division of Water Resources| Doug Stenzel | https://dwr.colorado.gov/about-us/contact-us/denver-office



***
### 4) Code File: 4_COss_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_coSSMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency info to columns.  See *CO_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = **WaterSourceName**.
    - *WaterSourceNativeID* = *in_WaterSourceNativeID*, see *0_ColoradoPreProcessSiteSpecificData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
COss_WS1 | Fresh | SOUTH PLATTE RIVER | WaDECO_WS1 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_COss_Sites.py
Purpose: generate a list of polygon areas associated with the state agency specific site on aggregated water budget data.

#### Inputs:
- P_coSSMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to columns.  See *CO_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersource.csv input file. See code for specific implementation of extraction.
    - *County* = **county**.
    ` *GNISCodeCV* = **gnisId**.
    - *Latitude* = **latdecdeg**.
    - *Longitude* = **longdecdeg**.
    - *SiteName* = **structureName**.
    - *SiteNativeID* = *in_SiteNativeID*, see *0_ColoradoPreProcessSiteSpecificData.ipynb* for specifics.
    - *SiteTypeCV* = **structureType**.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID |CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID |SiteTypeCV
---------- | ---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
COss_S1 | COss_WS1 | Unspecified | 40.317282| -104.376767 | CORONA RANCH DITCH | WaDECO_S1 | DITCH

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_COss_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific time series water data to import into WaDE 2.0.

#### Inputs:
- P_coSSMaster.csv
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
- Assign state agency data info to columns.  See *CO_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **dataValue**.
    - *BeneficialUseCategory* = **useDescr**.
    - *ReportYearCV* = **dataMeasDate**.
    - *TimeframeStart* = 01/01/ + **dataMeasDate**.  See *0_ColoradoPreProcessSiteSpecificData.ipynb* for specific on generation.
    - *TimeframeEnd* = 12/31/ + **dataMeasDate**.  See *0_ColoradoPreProcessSiteSpecificData.ipynb* for specific on generation.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
CO_Water Use Data | CODWR | COss_S1 | CO_Reservoirs and Gages | COss_WS1 | 971.92 | Irrigation | 1974 | 1/1/1974 | 12/31/1974 

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
### 7) Code File: 7_COss_PODSiteToPOUSiteRelationships.py
Purpose: generate linking element between POD and POU sites that share the same water right.
Note: podsitetopousiterelationships.csv output only needed if both POD and POU data is present, otherwise produces empty file.

#### Inputs:
- sites.csv
- sitespecificamounts.csv

#### Outputs:
- podsitetopousiterelationships.csv

#### Operation and Steps:
- Read the sites.csv & sitespecificamounts.csv input files.
- Remove unnecessary columns from needed sitespecificamounts.csv info.
- Explode *SiteUUID* field to create unique rows.
- Left-merge site.csv info to the sitespecificamounts dataframe via *SiteUUID* field.
- Split into two new temporary dataframes: one POD centric, the other POU centric.
- For the temporary POD dataframe...
    - Create *PODorPOUSite* field = POD.
- For the temporary POU dataframe
    - Create *PODorPOUSite* field = POU.
- Merge POD & POU dataframes into single output dataframe, only using unique rows.
- Find *SiteUUID* baesed on *PODorPOUSite* field.
- Perform error check on waterallocations dataframe (check for NaN values)
- If waterallocations is not empty, export output dataframe *podsitetopousiterelationships.csv*.



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Colorado Division of Water Resources (CODWR)](https://dwr.colorado.gov/about-us/contact-us/denver-office).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

CODWR Staff
- Doug Stenzel <doug.stenzel@state.co.us>