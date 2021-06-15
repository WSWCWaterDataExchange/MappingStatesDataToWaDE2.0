# UDWRi Site Specific Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [Utah Division of Water Rights (UDWRi)](https://www.waterrights.utah.gov/contact.asp), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for aggregated water budget...

- **Water Use Data Portal**, also known as M&I data, and broken up into **System** data.  Obtained from the UDWRi website at:  https://waterrights.utah.gov/asp_apps/waterUseData/setFilters.asp
- **Utah Culinary Water Service Areas**, which was used to tie in UDWRi data to location data.  Location information used for WaDE 2.0 purposes reflect the centroid of the water use areas (polygons).  Data was obtained from the Utah Division of Water Resources (UDWRe) website at: https://opendata.gis.utah.gov/datasets/1d2535e8c31247b9aaff664f6ac9c45d_0?geometry=-131.898%2C36.940%2C-91.216%2C42.682.

Please note that the UDWRe has this webpage for Municipal and Industrial Water Use Data.  The page has helpful notes at the bottom that explain the context of the data.  We didn’t use this data because the Division of Water Rights data source above compiles all the years data together which is easier for WaDE use.
https://dwre-utahdnr.opendata.arcgis.com/pages/municipal-and-industrial-data

Adam Clark summarized:
>The Utah Culinary Water Service Areas spatial database is a combination of work and collaboration between the Division of Water Resources (UDWRe) and the Division of Water Rights (UDWRi) within the Department of Natural Resources, and the Division of Drinking Water (UDDW) within the Department of Environmental Quality. Water Resources is the data steward/creator, but receives input from the other divisions on systems.  Water Rights and Drinking Water both maintain separate non-spatial databases of water systems.  Water Rights is mostly focused on water usage and sources, while Drinking Water is more focused on compliance and water quality.*  While all three divisions share attributes in some ways, they differ in others.  If you were to join their own databases, you would find that the number of systems differs between all three.  The Utah Culinary Water Service Areas spatial database is the Division of Water Resources’ master database that includes all systems, past and present.  It also includes large and small systems, non-public systems, and self-supplied industry.  You will find three columns of system IDs, because all three divisions use different ID systems for tracking/updating.  You can think of the spatial database as a bridge or hybrid between the other two.*  Feel free to use Water Rights' query service to get more information on systems.  Just realize that it will not have information on all of the systems included in the spatial database.  Water Rights uses our feature service in their website to show boundaries for systems, but I guarantee that many of the systems in the service are not used.

![](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Utah/SiteSpecificAmounts/UDWRi/Utah_data_flow.png)

Unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - UDWRi_SystemData_input
 - UDWRe_CulinaryWaterServiceAreas_input

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share UDWR's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *UDWRi MI_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the state agenecies site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those six code files are as follows...

- 0_PreProcessUDWRiSiteSpecificData.ipynb
- 1_UDWRi_SS_Methods.py
- 2_UDWRi_SS_Variables.py
- 3_UDWRi_SS_Organizations.py
- 4_UDWRi_SS_WaterSources.py
- 5_UDWRi_SS_Sites.py
- 6_UDWRi_SS_SiteSpecificAmounts_fact.py


***
### 0) Code File: 0_PreProcessUDWRiSiteSpecificData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - UDWRi_SystemData_input
 - UDWRe_CulinaryWaterServiceAreas_input

#### Outputs:
 - P_MasterUTSiteSpecific.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.
- Drop unused **System** & **Utah Culinary Water Service Area** data fields not used for WaDE import to minimize file size.
- Seperate out **System** data annual water use and connection number by reported customer type: *Domestic*, *Commercial*, *Industrial*, *Institutional* & *Total*.  Create temp dataframes for each customer type.
- Concatenate temp customer type dataframes into new longer dataframe.
- Left join new longer **System** by customer type and **Utah Culinary Water Service Area** on **System ID** and **WRID**.
- Generate WaDE specific *TimeframeStart* & *TimeframeEnd* fields. Assume start date is 01/01/+**History Year** and end date is 12/31/+**History Year**.
- Export output dataframe as new csv file, *P_MasterUTSiteSpecific.csv*.


***
### 1) Code File: 1_UDWRi_SS_Methods.py
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
UDWRi_Water Use Data | Unspecified | Unspecified


***
### 2) Code File: 2_UDWRi_SS_Variables.py
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
UDWRi_Site Specific | 1 | Year | AFY


***
### 3) Code File: 3_UDWRi_SS_Organizations.py
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
UDWRi | Utah Division of Water Rights | James Greer | https://waterrights.utah.gov/


***
### 4) Code File: 4_UDWRi_SS_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- None

#### Outputs:
- None

#### Operation and Steps:
- Input data used as this time is relevant to **System** data only and is missing vital water source information.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
UTSS_WS1 | Unspecified | Unspecified | Unspecified | Unspecified

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_UDWRi_SS_Sites.py
Purpose: generate a list of polygon areas associated with the state agency specific site on aggregated water budget data.

#### Inputs:
- P_MasterUTSiteSpecific.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency data info to the *WaDE Site* specific columns.  See *UDWRi MI_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *County* = **County**, UDWRi.
    - *Latitude* = **Latitude**, UDWRe.
    - *Longitude* = **Longitude**, UDWRe.
    - *SiteName* = **System Name**, UDWRi.
    - *SiteNativeID* == **System ID**, UDWRi.
    - *SiteTypeCV* = **System Type**, UDWRi & Unknown if not provided.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE specific *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | SiteName | SiteTypeCV 
---------- | ---------- | ------------ 
UTSS_S1 | Leeds Domestic Water Users Association | Public

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


***
### 6) Code File: 6_UDWRi_SS_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific time series water data to import into WaDE 2.0.

#### Inputs:
- P_MasterUTSiteSpecific.csv
- P_Geometry.csv
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
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *UDWRi MI_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = *WaterUse*, see *0_PreProcessUDWRiSiteSpecificData.ipynb* for specific on generation.
    - *CommunityWaterSupplySystem* = **System Name**, UDWRi.
    - *CustomerTypeCV* = *BenUse*, see *0_PreProcessUDWRiSiteSpecificData.ipynb* for specific on generation.
    - *PopulationServed* = **Population**, UDWRi.
    - *ReportYearCV* = **History Year**.
    - *TimeframeStart* = 01/01/+**History Year**.  See *0_PreProcessUDWRiSiteSpecificData.ipynb* for specific on generation.
    - *TimeframeEnd* = 12/31/+**History Year**.  See *0_PreProcessUDWRiSiteSpecificData.ipynb* for specific on generation.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
UDWRi_Water Use Data | UDWRi | UTSS_S1 | UDWRi_Site Specific Withdrawal | UTSS_WS1 | 89.07131598 | 1979

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- ?


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Utah Division of Water Resources (UDWRe)](https://water.utah.gov/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

UDWRe Staff
- Jessie Pierson <jpierson@utah.gov>
- Tom Moore <tmoore@utah.gov>
- Aaron Austin <aaronaustin@utah.gov>
- Craig Miller <craigmiller@utah.gov>
- Leila Ahmadi <lahmadi@utah.gov>