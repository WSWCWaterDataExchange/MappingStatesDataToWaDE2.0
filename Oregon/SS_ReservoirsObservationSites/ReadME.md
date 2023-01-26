# Oregon OWRD Site Specific Reservoir and Observation Site Data Preparation for WaDE2
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [Oregon Department of Natural Resources (OWRD)](https://dnr.nebraska.gov/contact), for inclusion into the Water Data Exchange (WaDE2) project.  WaDE2 enables states to share data with each other and the public in a more streamlined and consistent way. WaDE2 is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 
OR_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx


## Overview of Source Data Utilized
The following data was used for timeseries site specific water data...
- OWRD_gages shapefile data of site information, provided by personal correspondence via email.
- Stream gage timeseries data retrieved through Oregon API, not fully available to the public.

Unique files were created to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - **OWRD_gages.csv**, gage site location.
 - **timeseriesData.csv**, timeseries data for gage.

## Storage for WaDE2 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE2 database, can both be found within the WaDE2 sponsored Google Drive.  Please contact WaDE2 staff if unavailable or if you have any questions about the data.
- Oregon Site Specific Reservoir and Observation Site Data: https://drive.google.com/drive/folders/1UDoVZrfC9sJzgwqwI4tuFDte4HMgg3X_?usp=sharing


 ## Unique Data Notes
 OWRD was not confident in the accuracy of records with a start date before 1950.  All records pre-1950 were removed from the timeseries before uploaded to the WaDE 2.0 cloud database.


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share DWSG's site specific time series water data for inclusion into the Water Data Exchange (WaDE2 2.0) project.  For a complete mapping outline, see *OR_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx*.  Eight executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those code files are as follows...

- 0_PreProcessOregonReservoirGages.ipynb
- 1_ORssro_Methods.py
- 2_ORssro_Variables.py
- 3_ORssro_Organizations.py
- 4_ORssro_WaterSources.py
- 5_ORssro_Sites.py
- 6_ORssro_SiteSpecificAmounts_fact.py
- 7_ORssro_PODSiteToPOUSiteRelationships.py



***
### 0) Code File: 0_PreProcessOregonReservoirGages.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - OWRD_gages.csv
 - timeseriesData.csv

#### Outputs:
 - P_orSSRGMain.csv

#### Operation and Steps:
- If not done already, use OWRD API service to retrieve gage site data & timeseries data.
- Read in all input files.
- Left join gage site data to timeseries data via **station_nbr** & **station_nb** fields.
- **StationNumber** requires 8 digits, fill in with leading 0s if need be.
- Fill in Null & blank values for **streamfl_1** fields for water source type & **source_t_1** for site type.
- Convert **Date** field to fields to YYYY-MM_DD format.
- Review for errors in both timeseries and shapefile ouput dataframes
- Export output dataframe(s) as new csv file, *P_orSSRGMain.csv*.



***
### 1) Code File: 1_ORssro_Methods.py
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
ORssro_M1 | Surface Water | Unspecified



***
### 2) Code File: 2_ORssro_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:NEssro_O1
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
ORssro_V1 | 1 | Daily | CFS | Stream Gage | Stream Gage_Daily_Unspecified_Surface Water



***
### 3) Code File: 3_ORssro_Organizations.py
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
ORssro_O1 | Oregon Department of Natural Resources | Tom Byler | https://www.oregon.gov/owrd/Pages/index.aspx



***
### 4) Code File: 4_ORssro_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_orSSRGMain.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 WaterSources* specific columns.
- Assign state agency info to columns.  See *OR_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = "Unspecified".
    - *WaterSourceNativeID* = "WaDEOR_WS1"
    - *WaterSourceTypeCV* = **streamfl_1** field.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE2 specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
ORssro_WS1 | Fresh | Unspecified | WaDENE_WS1 | Runoff

Any data fields that are missing required values and dropped from the WaDE2-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_ORssro_Sites.py
Purpose: generate a list of sites specific to the site specific time series water data.

#### Inputs:
- P_orSSRGMain.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Site* specific columns.
- Assign state agency info to columns.  See *OR_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersources.csv input file. See code for specific implementation of extraction.
    - *County* = **county_nam** field.
    - *Latitude* =  **latitude_d** field.
    - *Longitude* = **longitude_** field.
    - *PODorPOUSite* = "Gage".
    - *SiteName* = **station_na** field.
    - *SiteNativeID* = **station_nb** field.
    - *SiteTypeCV* = **source_t_1** field.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE2 specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
ORssro_S1 | Unspecified | 42.072466 | -119.963672 | TWENTYMILE CR NR ADEL, OR | 10366000 | Stream

Any data fields that are missing required values and dropped from the WaDE2-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_ORssro_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific timeseries water data to import into WaDE2 2.0.

#### Inputs:
- P_orSSRGMain.csv
- variables.csv
- watersources.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Water Site Specific Reservoir and Observation Site Amounts* data columns.
- Assign state agency data info to columns.  See *OR_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **mean_daily_flow_cfs** field.
    - *BeneficialUseCategory* =  "Unspecified".
    - *ReportYearCV* = extract year value from **record_date** field.
    - *TimeframeStart* = **record_date** field in YYYY-MM-DD format.
    - *TimeframeEnd* = **record_date** field in YYYY-MM-DD format.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
ORssro_M1 | ORssro_O1 | ORssro_S1 | ORssps_V1 | ORssps_WS1 | 2610 | Unspecified | 3/1/1910 | 3/1/1910

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nevada Division of Water Resources [Oregon Office of the State Engineer (OWRD)](https://www.ose.state.nm.us/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

OWRD Staff
- Tom Byler <https://www.oregon.gov/owrd/Pages/index.aspx>
