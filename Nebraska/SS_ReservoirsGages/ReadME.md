# Nebraska NDNR Site Specific Reservoir and Gage Data Preparation for WaDE2
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [Nebraska Department of Natural Resources (NDNR)](https://dnr.nebraska.gov/contact), for inclusion into the Water Data Exchange (WaDE2) project.  WaDE2 enables states to share data with each other and the public in a more streamlined and consistent way. WaDE2 is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 
NE_SiteSpecificReservoirGageSchema Mapping to WaDE.xlsx


## Overview of Source Data Utilized
The following data was used for timeseries site specific water data...
- [StreamGage GetStationList](https://nednr.nebraska.gov/IwipApi/swagger/ui/index#/StreamGage) API service to retrieve site data.
- [StreamGage DailyMeanByYear](https://nednr.nebraska.gov/IwipApi/swagger/ui/index#/StreamGage) API service to retrieve timeseries data per site.

Unique files were created to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - **StreamGageGetStationList.csv**, gage site location.
 - **DailyMeanByYear.csv**, timeseries data for gage.

## Storage for WaDE2 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE2 database, can both be found within the WaDE2 sponsored Google Drive.  Please contact WaDE2 staff if unavailable or if you have any questions about the data.
- Nebraska Site Specific Reservoir and Gage Data: https://drive.google.com/drive/folders/1OWSAnPH3li_we58VwWVHqonsDLB2FqvJ



## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share DWSG's site specific time series water data for inclusion into the Water Data Exchange (WaDE2 2.0) project.  For a complete mapping outline, see *NE_SiteSpecificReservoirGageSchema Mapping to WaDE.xlsx*.  Eight executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those code files are as follows...

- 0_PreProcessNebraskaReservoirGages.ipynb
- 1_NEssrg_Methods.py
- 2_NEssrg_Variables.py
- 3_NEssrg_Organizations.py
- 4_NEssrg_WaterSources.py
- 5_NEssrg_Sites.py
- 6_NEssrg_SiteSpecificAmounts_fact.py
- 7_NEssrg_PODSiteToPOUSiteRelationships.py



***
### 0) Code File: 0_PreProcessNebraskaReservoirGages.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - StreamGageGetStationList.csv
 - DailyMeanByYear.csv

#### Outputs:
 - P_neSSRGMain.csv

#### Operation and Steps:
- If not done already, use NDNR API service to retrieve gage site data & timeseries data.
- Read in all input files.
- Left join gage site data to timeseries data via **StationNumber** field.
- **StationNumber** requires 8 digits, fill in with leading 0s if need be.
- Convert **Date** field to fields to YYYY-MM_DD format.
- Review for errors in both timeseries and shapefile ouput dataframes
- Export output dataframe(s) as new csv file, *P_neSSRGMain.csv*.



***
### 1) Code File: 1_NEssrg_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Method* specific columns.
- Assign state agency data info to the *WaDE2 Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
NEssrg_M1 | Surface Water | Unspecified



***
### 2) Code File: 2_NEssrg_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:NEssrg_O1
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Variable* specific columns.
- Assign state agency data info to the *WaDE2 Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV | VariableCV | VariableSpecificCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------
NEssrg_V1 | 1 | Daily | CFS | Stream Gage | Stream Gage_Daily_Unspecified_Surface Water



***
### 3) Code File: 3_NEssrg_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Organizations* specific columns.
- Assign state agency data info to the *WaDE2 Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
NEssrg_O1 | Nebraska Department of Natural Resources | Jennifer Schellpeper | https://dnr.nebraska.gov/contact



***
### 4) Code File: 4_NEssrg_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_neSSRGMain.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 WaterSources* specific columns.
- Assign state agency info to columns.  See *NE_SiteSpecificReservoirGageSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = "Unspecified".
    - *WaterSourceNativeID* = "WaDENE_WS1"
    - *WaterSourceTypeCV* = "Surface Water"
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE2 specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NEssrg_WS1 | Fresh | Unspecified | WaDENE_WS1 | Surface Water

Any data fields that are missing required values and dropped from the WaDE2-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_NEssrg_Sites.py
Purpose: generate a list of sites specific to the site specific time series water data.

#### Inputs:
- P_neSSRGMain.csv
- P_nmSSPWGeometry.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Site* specific columns.
- Assign state agency info to columns.  See *NE_SiteSpecificReservoirGageSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersources.csv input file. See code for specific implementation of extraction.
    - *Latitude* =  see *0_PreProcessNebraskaReservoirGages.ipynb* for specifics on generation.
    - *Longitude* = see *0_PreProcessNebraskaReservoirGages.ipynb* for specifics on generation.
    - *PODorPOUSite* = "Gage".
    - *SiteName* = **StationName** field.
    - *SiteNativeID* = **StationNumber** field.
    - *SiteTypeCV* = **StationTypeDescription** field..
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE2 specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
NEssrg_S1 | Unspecified | 42.6351 | -100.8721 | Ainsworth Canal from Merritt Reservoir | 1000 | Canal/Pump

Any data fields that are missing required values and dropped from the WaDE2-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_NEssrg_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific timeseries water data to import into WaDE2 2.0.

#### Inputs:
- P_neSSRGMain.csv
- variables.csv
- watersources.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Water Site Specific Reservoir and Gage Amounts* data columns.
- Assign state agency data info to columns.  See *NE_SiteSpecificReservoirGageSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **Value** field.
    - *BeneficialUseCategory* =  "Unspecified".
    - *ReportYearCV* = extract year value from **Date** field.
    - *TimeframeStart* = **Date** field in YYYY-MM-DD format.
    - *TimeframeEnd* = **Date** field in YYYY-MM-DD format.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
NEssrg_M1 | NEssrg_O1 | NEssrg_S1 | NMssps_V1 | NMssps_WS1 | 15.0 | Unspecified | 1/1/2022| 1/1/2022

Any data fields that are missing required values and dropped from the WaDE2-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nevada Division of Water Resources [Nebraska Office of the State Engineer (NDNR)](https://www.ose.state.nm.us/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

NDNR Staff
- Jennifer Schellpeper <jennifer.schellpeper@nebraska.gov>
