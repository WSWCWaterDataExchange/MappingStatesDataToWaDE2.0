# IDWR Site Specific Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [Idaho Dept. of Water Resources (IDWR)](https://idwr.idaho.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for aggregated water budget...

- [Aqua Info](https://research.idwr.idaho.gov/apps/hydrologic/aquainfo/) time series data, retrieved via API.


Unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - P_idSSMaster.csv


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share IDWR's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *ID_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those six code files are as follows...

- 0_PreProcessIDSiteSpecificData.ipynb
- 1_IDss_Methods.py
- 2_IDss_Variables.py
- 3_IDss_Organizations.py
- 4_IDss_WaterSources.py
- 5_IDss_Sites.py
- 6_IDss_SiteSpecificAmounts_fact.py
- 7_IDss_PODSiteToPOUSiteRelationships.py



***
### 0) Code File: 0_PreProcessIDSiteSpecificData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
- [Aqua Info](https://research.idwr.idaho.gov/apps/hydrologic/aquainfo/) time series data, retrieved via API.

#### Outputs:
 - P_idSSMaster.csv

#### Operation and Steps:
- Retrieve ID discharge station site information from the Aqua Info API, place into temporary location dataframe.
- Create unique url string using **uniqueId**, **rawStartTime**, and **rawEndTime** to retrieve time series information for each site.
- Trim down retrieved site info information dataframe to sites that have records of **label** values of Daily.
- Retrieve time series data using the unique url created, place into temporary time series dataframe.
- Combine location dataframe with time series dataframe, join on **niqueId** values unique to the site (not the times series recording version).
- Format **timeStamp** field to WaDE specific time format.
- Extract year value from **timeStamp** field.
- Review for errors.
- Export output dataframe as new csv file, *P_idSSMaster.csv*.



***
### 1) Code File: 1_IDss_Methods.py
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
IDWR_AquaInfo | Surface Water | Measured



***
### 2) Code File: 2_IDss_Variables.py
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
IDWR_Reservoirs and Gages | Daily | Average | CFS



***
### 3) Code File: 3_IDss_Organizations.py
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
IDWR | Idaho Dept. of Water Resources | Linda Davis | https://idwr.idaho.gov/



***
### 4) Code File: 4_IDss_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_idSSMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency info to columns.  See *ID_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - NA.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
IDss_WS1 | Fresh | Unspecified | Unspecified | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_IDss_Sites.py
Purpose: generate a list of polygon areas associated with the state agency specific site on aggregated water budget data.

#### Inputs:
- P_idSSMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to columns.  See *ID_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* respective watersourcecsv files. See code for specific implementation of extraction.
    - *Latitude* = **latitude**.
    - *Longitude* = **longitude**.
    - *SiteName* = **locationName**.
    - *SiteNativeID* = **identifier**.
    - *SiteTypeCV* = **locationType**.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
IDss_S2 | Unspecified | 42.95033541 | -115.9747944 | Snake River Irrigation District | 2002-1 | Hydrology Station

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_IDss_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific time series water data to import into WaDE 2.0.

#### Inputs:
- P_idSSMaster.csv
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
- Assign state agency data info to columns.  See *ID_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **numericValue1**.
    - *ReportYearCV* = year value extracted from **timeStamp**.
    - *TimeframeStart* = **timeStamp**.
    - *TimeframeEnd* = **timeStamp**.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
IDWR_AquaInfo | IDWR | IDss_S1 | IDWR_Site Specific | IDss_WS1 | 0.5175 | Unspecified | 2019 | 10/22/2019 | 10/22/2019 

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
### 7) Code File: 7_IDss_PODSiteToPOUSiteRelationships.py
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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Idaho Dept. of Water Resources (IDWR)](https://idwr.idaho.gov/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

IDWR Staff
- Linda Davis <linda.davis@idwr.idaho.gov>