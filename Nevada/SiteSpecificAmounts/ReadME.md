# NDWR Site Specific Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [Nevada Division of Water Resources (NDWR)](http://water.nv.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for aggregated water budget...

- [Surface Water Monitoring Measures](https://data-ndwr.hub.arcgis.com/datasets/NDWR::surface-water-monitoring-measures/about) time series data to assess the condition of the groundwater and surface water systems.
- [Surface Water Monitoring Sites](https://data-ndwr.hub.arcgis.com/datasets/NDWR::surface-water-monitoring-sites/about) shapefile location data to pair time series data to sites.

Unique files were created to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - Surface_Water_Monitoring_Sites_and_Measures.csv
 - SurfaceWaterMonitoringSites.shp


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NDWR's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NV_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those six code files are as follows...

- 0_PreProcessNVSiteSpecificData.ipynb
- 1_NVss_Methods.py
- 2_NVss_Variables.py
- 3_NVss_Organizations.py
- 4_NVss_WaterSources.py
- 5_NVss_Sites.py
- 6_NVss_SiteSpecificAmounts_fact.py
- 7_NVss_PODSiteToPOUSiteRelationships.py



***
### 0) Code File: 0_PreProcessNVSiteSpecificData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - Surface_Water_Monitoring_Sites_and_Measures.csv
 - SurfaceWaterMonitoringSites.shp

#### Outputs:
 - P_nvSSMaster.csv

#### Operation and Steps:
- Create unique dataframes for each inpute file: Surface_Water_Monitoring_Sites_and_Measures.csv & SurfaceWaterMonitoringSites.shp.
- Left-join merge both datasets together via **Site_Name** field.
- For the merged dataset...
    - Preserve the following fields: **Source_Nam**, **County**, **Lat_DD_NAD**, **Lon_DD_NAD**, **Site_Name**, **AutoID**, **Source_Des**, **Units**, **Discharge**, & **Measure_date**.
    - For WaDE, convert **Discharge** GPM to CFS using **Units** input field if need be.
    - Extract WadE specific *ReportyYearCV* value from **Measure_date** input field in the form of YYYY.
    - Convert **Measure_date** to %mm/%dd/%YYYY format.
    - Remove NULL values from **Site_Name** and replace with "Unspecified".
    - Determine WaDE specific *WaterSourceTypeCV* field using **Site_Name** input field.  Inputs of "wells", "well", "flowing well" & "spring" will be considred Groundwater, while everthing else is Surface Water.
    - Create WaDe Specific *WaterSourceNativeID* field using **Source_Nam** input field.
- Review for errors.
- Export output dataframe as new csv file, *P_nvSSMaster.csv*.



***
### 1) Code File: 1_NVss_Methods.py
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
NVss_M1 | Surface Water | Measured



***
### 2) Code File: 2_NVss_Variables.py
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
NVss_V1 | Daily | Average | CFS



***
### 3) Code File: 3_NVss_Organizations.py
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
NVss_O1 | Nevada Division of Water Resources | Brian McMenamy | http://water.nv.gov



***
### 4) Code File: 4_NVss_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_nvSSMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency info to columns.  See *NV_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = **Source_Nam**.
    - *WaterSourceNativeID* = custom, see *0_PreProcessNVSiteSpecificData.ipynb* for specifics.
    - *WaterSourceTypeCV* = custom, see *0_PreProcessNVSiteSpecificData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NVss_WS1 | Fresh | BARTLETT CREEK | WaDENV_WS1 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_NVss_Sites.py
Purpose: generate a list of polygon areas associated with the state agency specific site on aggregated water budget data.

#### Inputs:
- P_nvSSMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to columns.  See *NV_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* respective watersourcecsv files. See code for specific implementation of extraction.
    - *CoordinateMethodCV* = "Unspecified".
    - *County* = **County**.
    - *Latitude* = **'Lat_DD_NAD**.
    - *Longitude* = **Lon_DD_NAD**.
    - *PODorPOUSite* = "Gage".
    - *SiteName* = **Site_Name**.
    - *SiteNativeID* = **AutoID**.
    - *SiteTypeCV* = **Source_Des**.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
NVss_S1 | Unspecified | 41.47777 | -118.78836 | 028  N41 E28 17AADD1 | 28 | STREAM

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_NVss_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific time series water data to import into WaDE 2.0.

#### Inputs:
- P_nvSSMaster.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Site Specific Amounts* data columns.
- Assign state agency data info to columns.  See *NV_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **Discharge** as a float in CFS.
    - *ReportYearCV* = year value extracted from **Measure_date**.
    - *TimeframeStart* = **Measure_date**.
    - *TimeframeEnd* = **Measure_date**.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
NVss_M1 | NVss_O1 | NVss_S1 | NVss_V1 | NVss_WS1 | 0.91 | Unspecified | 1939 | 05/27/1939 | 05/27/1939

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
### 7) Code File: 7_NVss_PODSiteToPOUSiteRelationships.py
Purpose: generate linking element between POD and POU sites that share the same water right.
Note: podsitetopousiterelationships.csv output only needed if both POD and POU data is present, otherwise produces empty file.

There are no PODs and POUs to link at this time.

<!-- #### Inputs:
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
- If waterallocations is not empty, export output dataframe *podsitetopousiterelationships.csv*. -->

***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nevada Division of Water Resources (NDWR)](http://water.nv.gov/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

NDWR Staff
- Brian McMenamy <bmcmenamy@water.nv.gov>