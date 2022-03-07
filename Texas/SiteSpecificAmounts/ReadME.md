# TWDB Site Specific Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [Texas Water Development Board (TWDB)](https://www.twdb.texas.gov/index.asp), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Data Utilized
The following data was used for timeseries site specific water data...

- [Public Water Systems - Historical](https://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp) time series data.  Had to download each region area (A-P) individualy and combine into one workable file.
- [Historical Categorical Connections and Volumes by Public Water System](https://www.twdb.texas.gov/waterplanning/waterusesurvey/estimates/index.asp) annual retail wate ruse volumes 2019-2016.
- [Water Service Boundaries](https://www3.twdb.texas.gov/apps/waterserviceboundaries) shapefile for Public Water Systems site information.
- [20220106 PWS-SurveyNO bridge table]() csv file, provided by personal corespondance between WSWC and TWDB to join Public Water Systems - Historical timeseries data with the Public Water Systems boundary information.

Unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - HistoricalMunicipal_A.csv -to- HistoricalMunicipal_P.csv
 - PWS_Export.shp
 - 20220106 PWS-SurveyNO bridge table.csv

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share TWDB's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *TX_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those six code files are as follows...

- 0_PreProcessCASiteSpecificData.ipynb
- 1_TXss_Methods.py
- 2_TXss_Variables.py
- 3_TXss_Organizations.py
- 4_TXss_WaterSources.py
- 5_TXss_Sites.py
- 6_TXss_SiteSpecificAmounts_fact.py
- 7_TXss_PODSiteToPOUSiteRelationships.py



***
### 0) Code File: 0_PreProcessCASiteSpecificData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - HistoricalMunicipal_A.csv -to- HistoricalMunicipal_P.csv
 - PWS_Export.shp
 - 20220106 PWS-SurveyNO bridge table.csv

#### Outputs:
 - P_txSSMaster.csv

#### Operation and Steps:
- Read in HistoricalMunicipal_A.csv -to- HistoricalMunicipal_P.csv input csv files, PWS_Export.shp shapefile data, 20220106 PWS-SurveyNO bridge table data and place into temporary dataframes.
- Concatenate HistoricalMunicipal data into one long workable dataframe.
- Left join dataframes together.  Join HistoricalMunicipal data -to- 20220106 PWS-SurveyNO bridge table bridge table via **TWDB_Survey_No** and **Water surveyNo No** respectively, and PWS_Export shapefile info via **pwsCode2** with **PWSId**.
- As a whole, there are 6 different timeseries that will be incorporated into the WaDE 2.0 architecture.  These timeseries differ by time interval type and water source type…
    - for time interval type: Monthly or Annual
    - for water source type: Groundwater, Surface Water, or Reuse.
- For the data set...
    - WaDE *WaterSourceName* field = specific to water source type and site, based on **Organization**, **Aquifer_Source**, & **Surface_Water_Source** input.
    - WaDE *WaterSourceTypeCV* field = **Water_Type** input.
    - WaDE *CoordinateMethodCV field = **Source** input.
    - WaDE *County* field = **County_Used** input.
    - WaDE *Latitude* field = **Lat** input.
    - WaDE *Longitude* field = **Long** input.
    - WaDE *SiteName* field = **pwsName_y** input.
    - WaDE *SiteNativeID* field = **PWSId** input.
    - WaDE *Amount* field = timeseries specific of **Jan**, **Feb**, **Mar**, **Apr**, **May**, **Jun**, **Jul**, **Aug**, **Sep**, **Oct**, **Nov**, **Dec**, or **Total_Intake__Gallons_** inputs respectively, depending on timeseries of interest.
    - WaDE *Beneficial Use* = dependent on timeseries of interest.
    - WaDE *CommunityWaterSupplySystem* field = **pwsName_y** input.
    - WaDE *PopulationServed* field = **Population_Served** input.
    - WaDE *ReportYearCV* field = **Year** input.
    - WaDE *TimeframeStart* field = "01/01" + **Year** input.
    - WaDE *TimeframeEnd* field = month specific end date + **Year** input.
- Concatenate time series info into one long output dataframe.
- Format WaDE *TimeframeStart* & *TimeframeEnd* fields to YYYY-MM_DD format.
- Review for errors.
- Create WaDE Specific *WaterSourceNativeID* field using created *WaterSourceTypeCV* field, helps cut down on searching.
- Export output dataframe as new csv file, *P_txSSMaster.csv*.



***
### 1) Code File: 1_TXss_Methods.py
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
TXss_M1 | Surface Ground Storage | Estimate



***
### 2) Code File: 2_TXss_Variables.py
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
TXss_V1 | 1 | Annual | G | Intake | Intake_Annual_MI_Groundwater



***
### 3) Code File: 3_TXss_Organizations.py
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
TXss_O1 | Texas Water Development Board | Natalie Houston | https://www.twdb.texas.gov/index.asp



***
### 4) Code File: 4_TXss_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_txSSMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency info to columns.  See *TX_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = see *0_PreProcessCASiteSpecificData.ipynb* for specific on generation.
    - *WaterSourceNativeID* = see *0_PreProcessCASiteSpecificData.ipynb* for specific on generation.
    - *WaterSourceTypeCV* = **Water_Type**.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
TXss_WS1 | Fresh | OGALLALA AQUIFER | WaDETX_WS1 | Ground Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_TXss_Sites.py
Purpose: generate a list of sites specific to the site specific time series water data.

#### Inputs:
- P_txSSMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to columns.  See *TX_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersource.csv input file. See code for specific implementation of extraction.
    - *CoordinateMethodCV* = **Source**.
    - *County* = **County_Used**.
    - *Latitude* = **Lat**, generated from centroid of PWS area in the PWS_Export.shp input file.
    - *Longitude* = **Long**, generated from centroid of PWS area in the PWS_Export.shp input file.
    - *PODorPOUSite* = "POU" for Point of Use.
    - *SiteName* = **pwsName_y**.
    - *SiteNativeID* = **PWSId**.
    - *SiteTypeCV* = "Public Water Systems".
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID |SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
TXss_S1 | System | 36.4451440719 | -100.323255749 | DARROUZETT MUNICIPAL WATER SYSTEM | TX1480002 | Public Water Systems

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_TXss_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific timeseries water data to import into WaDE 2.0.

#### Inputs:
- P_txSSMaster.csv
- variables.csv
- watersources.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Site Specific Amounts* data columns.
- Assign state agency data info to columns.  See *TX_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = see *0_PreProcessCASiteSpecificData.ipynb* for specific on generation.
    - *BeneficialUseCategory* =  "Municipal".
    - *CommunityWaterSupplySystem* = **pwsName_y**.
    - *CustomerTypeCV* = "Municipal".
    - *ReportYearCV* = **Year**.
    - *TimeframeStart* = see *0_PreProcessCASiteSpecificData.ipynb* for specific on generation.
    - *TimeframeEnd* = see *0_PreProcessCASiteSpecificData.ipynb* for specific on generation.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
TXss_M1 | TXss_O1 | TXss_S1 | TXss_V4 | TXss_WS510 | 1486000000 | Municipal | 2021 | 01/01/2021 | 01/31/2021

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
### 7) Code File: 7_TXss_PODSiteToPOUSiteRelationships.py
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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Texas Water Development Board (TWDB)](https://www.twdb.texas.gov/index.asp).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

TWDB Staff
- Natalie Houston <nhouston@usgs.gov>
