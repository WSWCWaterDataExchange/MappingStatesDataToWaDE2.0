# UT Site Specific Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [Utah Division of Water Rights (UDWRi)](https://www.waterrights.utah.gov/contact.asp), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for aggregated water budget...

- **Water Use Data Portal**, also known as M&I data, and broken up into **System** and **Source** data.  Obtained from the UDWRi website at:  https://waterrights.utah.gov/asp_apps/waterUseData/setFilters.asp
- **Utah Culinary Water Suppliers**, which was used to tie in UDWRi data to location data.  Location information used for WaDE 2.0 purposes reflect the centroid of the water use areas (polygons).  Data was obtained from the Utah Division of Water Resources (UDWRe) website at: https://utahdnr.maps.arcgis.com/apps/webappviewer/index.html?id=050cace4aa4a43f5a38dbea00fb7f894



Please note that the UDWRe has this webpage for Municipal and Industrial Water Use Data.  The page has helpful notes at the bottom that explain the context of the data.  We didn’t use this data because the Division of Water Rights data source above compiles all the years data together which is easier for WaDE use.
https://dwre-utahdnr.opendata.arcgis.com/pages/municipal-and-industrial-data

Adam Clark summarized:
>The Utah Culinary Water Service Areas spatial database is a combination of work and collaboration between the Division of Water Resources (UDWRe) and the Division of Water Rights (UDWRi) within the Department of Natural Resources, and the Division of Drinking Water (UDDW) within the Department of Environmental Quality. Water Resources is the data steward/creator, but receives input from the other divisions on systems.  Water Rights and Drinking Water both maintain separate non-spatial databases of water systems.  Water Rights is mostly focused on water usage and sources, while Drinking Water is more focused on compliance and water quality.*  While all three divisions share attributes in some ways, they differ in others.  If you were to join their own databases, you would find that the number of systems differs between all three.  The Utah Culinary Water Service Areas spatial database is the Division of Water Resources’ master database that includes all systems, past and present.  It also includes large and small systems, non-public systems, and self-supplied industry.  You will find three columns of system IDs, because all three divisions use different ID systems for tracking/updating.  You can think of the spatial database as a bridge or hybrid between the other two.*  Feel free to use Water Rights' query service to get more information on systems.  Just realize that it will not have information on all of the systems included in the spatial database.  Water Rights uses our feature service in their website to show boundaries for systems, but I guarantee that many of the systems in the service are not used.

![](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Utah/SiteSpecificAmounts/Utah_data_flow.png)

Unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - UDWRi_SystemData_input.csv
 - UDWRi_SourceData_input.csv
 - UDWRe_CulinaryWaterServiceAreas_input.csv

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share UDWR's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *UT_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the state agenecies site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those six code files are as follows...

- 0_PreProcessUTSiteSpecificData.ipynb
- 1_UTss_Methods.py
- 2_UTss_Variables.py
- 3_UTss_Organizations.py
- 4_UTss_WaterSources.py
- 5_UTss_Sites.py
- 6_UTss_SiteSpecificAmounts_fact.py
- 7_UTss_PODSiteToPOUSiteRelationships.py



***
### 0) Code File: 0_PreProcessUTSiteSpecificData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - UDWRi_SystemData_input.csv
- UDWRi_SourceData_input.csv
 - UDWRe_CulinaryWaterServiceAreas_input.csv

#### Outputs:
 - P_MasterUTSiteSpecific.csv

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.
- For UDWRi System Data...
    - Seperate out **System** data annual water use and connection number by reported customer type: *Domestic*, *Commercial*, *Industrial*, *Institutional* & *Total*.  Create temp dataframes for each customer type.
    - Concatenate temp customer type dataframes into new longer UDWRi System Data dataframe.
    - Drop duplicate entries.
- For UDWRi Source Data...
    - Set WaDE *WaterSourcetiypeCV* field using custom dictoinary and **Source Type** entry.
    - WaDE *VariableCV* field = **Diversion Type** input.
    - WaDE *CoordinateMethodCV* field = **Representation Node** input.
    - WaDE *Latitude* field = **Lat NAD83** input.
    - WaDE *Longitude* field = **Lon NAD83** input.
    - WaDE *PODorPOUSite'] = "POD"
    - WaDE *SiteName* field = **Source Name** input.
    - WaDE *SiteNativeID* field = **Source ID** input.
    - WaDE *SiteTypeCV* field = **Source Type** input.
    - Drop duplicate entries.
- For UDWRe Culinary Service Area Data...
    - WaDE *WaterSourcetiypeCV* field =  Unspecified.
    - WaDE *VariableCV* field = Unspecified.
    - WaDE *CoordinateMethodCV* field = Centroid of Area
    - WaDE *Latitude* field = **Latitude** input.
    - WaDE *Longitude* field = **Longitude** input.
    - WaDE *PODorPOUSite'] = "POU"
    - WaDE *SiteName* field = **WRENAME** input.
    - WaDE *SiteNativeID* field = **WRID** input.
    - WaDE *SiteTypeCV* field = Unspecified
    - Drop duplicate entries.
- Concatenate UDWRi Source Data with DWRe Culinary Service Area Data to create one long dataframe.
- Left join new longer UDWRi System Data with UDWRi Source Data & UDWRe Culinary Service Area Data using **System ID** too **WRID** **System ID** fields.
- Generate WaDE specific *TimeframeStart* & *TimeframeEnd* fields. Assume start date is 01/01/+**History Year** and end date is 12/31/+**History Year**.
- Create WaDE custom water source native id field to help join water sources to sites.
- Forat WaDE *Population* field to int data type.
- Export output dataframe as new csv file, *P_MasterUTSiteSpecific.csv*.



***
### 1) Code File: 1_UTss_Methods.py
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
UDWRi_Water Use Data | Surface Ground Water | Measured



***
### 2) Code File: 2_UTss_Variables.py
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
### 3) Code File: 3_UTss_Organizations.py
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
### 4) Code File: 4_UTss_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_MasterUTSiteSpecific.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency info info to the *WaDE WaterSources* specific columns.  See *UT_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceNativeID* = *in_WaterSourceNativeID*, see *0_PreProcessUTSiteSpecificData.ipynb* for specifics.
    - *WaterSourceTypeCV* = *in_WaterSourceTypeCV*, see *0_PreProcessUTSiteSpecificData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
UTwr_WS1 | Fresh | Unspecified | WaDEUT_WS1 | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_UTss_Sites.py
Purpose: generate a list of polygon areas associated with the state agency specific site on aggregated water budget data.

#### Inputs:
- P_MasterUTSiteSpecific.csv

#### Outputs:
- sites.csv
- waterSources.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency data info to the *WaDE Site* specific columns.  See *UT_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - *CoordinateMethodCV* = *in_CoordinateMethodCV*, see *0_PreProcessUTSiteSpecificData.ipynb* for specifics.
    - *County* = **County**
    - *Latitude* = *in_Latitude*, see *0_PreProcessUTSiteSpecificData.ipynb* for specifics.
    - *Longitude* = *in_Longitude*, see *0_PreProcessUTSiteSpecificData.ipynb* for specifics.
    - *PODorPOUSite* = *in_PODorPOUSite*, see *0_PreProcessUTSiteSpecificData.ipynb* for specifics.
    - *SiteName* = *in_SiteName*, see *0_PreProcessUTSiteSpecificData.ipynb* for specifics.
    - *SiteNativeID* == *in_SiteNativeID*, see *0_PreProcessUTSiteSpecificData.ipynb* for specifics.
    - *SiteTypeCV* = *in_SiteTypeCV*, see *0_PreProcessUTSiteSpecificData.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
UTss_S1 | UTss_WS1| Representation Node | 37.30907717 | -113.4294115 | Oak Grove Spring (WS001)

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_UTss_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific time series water data to import into WaDE 2.0.

#### Inputs:
- P_MasterUTSiteSpecific.csv
- variables.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Site Specific Amounts* data columns.
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *UT_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = *WaterUse*, see *0_PreProcessUTSiteSpecificData.ipynb* for specific on generation.
    - *CommunityWaterSupplySystem* = **System Name**, UDWRi.
    - *CustomerTypeCV* = *BenUse*, see *0_PreProcessUTSiteSpecificData.ipynb* for specific on generation.
    - *PopulationServed* = **Population**, UDWRi.
    - *ReportYearCV* = **History Year**.
    - *TimeframeStart* = 01/01/+**History Year**.  See *0_PreProcessUTSiteSpecificData.ipynb* for specific on generation.
    - *TimeframeEnd* = 12/31/+**History Year**.  See *0_PreProcessUTSiteSpecificData.ipynb* for specific on generation.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID  | Amount | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ 
UDWRi_Water Use Data | UDWRi | UTss_S1 | UDWRi_Site Specific Withdrawal | 89.07131598 | 1979

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
### 7) Code File: 7_UTss_PODSiteToPOUSiteRelationships.py
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
