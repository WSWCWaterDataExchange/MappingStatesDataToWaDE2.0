# UDWRe Stream and Reservoir Observation Site Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting stream and reservoir observation site time series water data made available by the [Utah Division of Water Resources (UDWRe](https://water.utah.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for timeseries observation site water data...0_UTssro_PreProcessAllocationData.ipynb

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Distribution_Stations** | Site data for stream gages and reservoirs. | personal email correspondence | not provided
**timeseries data** | Timeseries data for stream gages and reservoirs related to discharge, storage, or evaporation.  Retrieved via provided API from UDWRe. POU area data. | - | not provided

Unique files were created to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - Distribution_Stations.csv
 - url_timeseries.zip

 ## Storage for WaDE2 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE2 database, can both be found within the WaDE2 sponsored Google Drive.  Please contact WaDE2 staff if unavailable or if you have any questions about the data.
- Utah Site Specific Reservoir and Gage Data: https://drive.google.com/drive/folders/1rLCAD6QJWlIav8WWDwJy4Uk9uq_aZ3cV?usp=share_link



## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share UDWRe's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *UTssro_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx*.  Several executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), while the remaining code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). Those code files are as follows...

- 0_UTssro_PreProcessAllocationData.ipynb
- 1_UTssro_Methods.py
- 2_UTssro_Variables.py
- 3_UTssro_Organizations.py
- 4_UTssro_WaterSources.py
- 5_UTssro_Sites.py
- 6_UTssro_SiteSpecificAmounts_fact.py


***
### 0) Code File: 0_UTssro_PreProcessAllocationData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple DataFrames creation and extraction.

#### Inputs: 
 - Distribution_Stations.csv
 - url_timeseries.zip

#### Outputs:
 - P_utSSROMain.zip

#### Operation and Steps:
- Read in Distribution_Stations input csv data, place into temporary dataframes.
- Using **STATION_ID** input, use provided API service to retrieve timeseries info
    - ex: "https://www.waterrights.utah.gov/dvrtdb/DailyCommaData.asp?BYEAR=1900&EYEAR=2023&StationId=" + **STATION_ID**.
    - save to zipped csv file for future use.
- For retrieved timeseries data...
    - create *in_VariableCV* input based on **Units** input. Use following rules...
        - *cfs*, *discharge in cfs* = Discharge
        - *height in feet* = Stage
        - *storage in acft* = Storage
        - *discharge in acft* = Discharge AF
        - *diversion in acft* = Diversion
        - *evaporation in cfs* = Evaporation
    - create *in_SiteTypeCV* input based on based on **Units** input. Use following rules...
        - *cfs*, *discharge in cfs*, *height in feet*, *discharge in acft*, *diversion in acft*, *evaporation in cfs* = Stream Gage
        - *storage in acft* = Reservoir
    - create *in_BeneficialUseCategory* input based on **Units** input. Use following rules...
        - *cfs*, *discharge in cfs* = Discharge
        - *height in feet* = Stage
        - *storage in acft* = Storage
        - *discharge in acft* = Discharge AF
        - *diversion in acft* = Diversion
        - *evaporation in cfs* = Evaporation
- Review for errors.
- Create WaDE Specific *WaterSourceNativeID* field using created *WaterSourceTypeCV* field, helps cut down on searching.
- Export output DataFrames as new csv file, *P_utSSROMain.zip*.


***
### 1) Code File: 1_UTssro_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE Method* specific columns.
- Assign state agency data info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output DataFrames.
- Export output DataFrames *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
UTssro_M1 | Surface Water | WaDE Unspecified



***
### 2) Code File: 2_UTssro_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE Variable* specific columns.
- Assign state agency data info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output DataFrames.
- Export output DataFrames *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV | VariableCV | VariableSpecificCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------
UTssro_V1 | 1 | Daily | AF | Discharge AF | Discharge AF_Daily_Discharge_Surface Water



***
### 3) Code File: 3_UTssro_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE Organizations* specific columns.
- Assign state agency data info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output DataFrames.
- Export output DataFrames *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
UTssro_O1 | Utah Division of Water Resources | Craig Miller | https://water.utah.gov/



***
### 4) Code File: 4_UTssro_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_utSSROMain.zip

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE WaterSources* specific columns.
- Assign state agency info to columns.  See *UTssro_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = Surface Water
- Consolidate output DataFrames into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output DataFrames.
- Export output DataFrames *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
UTssro_WS1 | Fresh | ASHLEY CREEK | WaDEUT_WS1 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_UTssro_Sites.py
Purpose: generate a list of sites specific to the site specific time series water data.

#### Inputs:
- P_utSSROMain.zip

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE Site* specific columns.
- Assign state agency info to columns.  See *UTssro_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *Latitude* = **Latitude**.
    - *Longitude* = **Longitude**.
    - *SiteName* = **NAME**.
    - *SiteTypeCV* = see *0_UTssro_PreProcessAllocationData.ipynb* for specific on generation.
- Consolidate output DataFrames into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output DataFrames.
- Export output DataFrames *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID |SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
UTssro_S1 | WaDE Unspecified | 40.404864813 | -111.528665263999 | DEER CREEK RESERVOIR (DAILY CONTENTS) | 122 | Reservoir

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_UTssro_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific timeseries water data to import into WaDE 2.0.

#### Inputs:
- P_utSSROMain.zip
- methods.csv
- variables.csv
- organizations.csv
- watersources.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE Water Site Specific Amounts* data columns.
- Assign state agency data info to columns.  See *UTssro_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = *in_Amount*, see *0_UTssro_PreProcessAllocationData.ipynb* for specific on generation.
    - *BeneficialUseCategory* =  see *0_UTssro_PreProcessAllocationData.ipynb* for specific on generation.
    - *ReportYearCV* = see *0_UTssro_PreProcessAllocationData.ipynb* for specific on generation.
    - *TimeframeStart* = *in_TimeframeStart*, see *0_UTssro_PreProcessAllocationData.ipynb* for specific on generation.
    - *TimeframeEnd* = *in_TimeframeEnd*, see *0_UTssro_PreProcessAllocationData.ipynb* for specific on generation.
- Perform error check on output DataFrames.
- Export output DataFrames *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
UTssro_M1 | UTssro_O1 | UTssro_S594 | UTssro_V2 | UTssro_WS1 | 0 | Discharge | 1962 | 7/1/1962 | 7/1/1962

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Utah Division of Water Rights (UDWRi)](https://waterrights.utah.gov//).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

UDWRi Staff
- Jim Reese <jreese@utah.gov>