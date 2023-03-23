# WWDO Stream and Reservoir Observation Site Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting stream and reservoir observation site time series water data made available by the [Wyoming Water Development Office](https://wwdc.state.wy.us/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for timeseries observation site water data...

- [seoflow](https://seoflow.wyo.gov/) timeseries site data.  Specifically the 'Total Lake/Reservoir Volume' data and 'Discharge" flow data parameter types.

Unique files were created to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - For both 'Total Lake/Reservoir Volume' and 'Discharge" parameter data types...
    - site information, pulled from the following files...
        - data set label.csv
        - latitude.csv
        - longitude.csv
        - location identifier.csv
        - location name.csv
        - location type.csv
    - timeseries data respectively for each parameter data type per site, pulled from the seoflow API service.
 - ReservoirGages_caOnly.csv

 ## Storage for WaDE2 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE2 database, can both be found within the WaDE2 sponsored Google Drive.  Please contact WaDE2 staff if unavailable or if you have any questions about the data.
- Wyoming Site Specific Reservoir and Gage Data: https://drive.google.com/drive/folders/1tdjmjnqWTTyY-I20HdUbBmJGzDcx7Hil?usp=share_link



## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CSWRCB's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *WY_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx*.  Several executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  Some code files were built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining other code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). Those code files are as follows...

- 0_WYssro_PreProcessAllocationData.ipynb
- 1_WYssro_Methods.py
- 2_WYssro_Variables.py
- 3_WYssro_Organizations.py
- 4_WYssro_WaterSources.py
- 5_WYssro_Sites.py
- 6_WYssro_SiteSpecificAmounts_fact.py
- 7_WYssro_WaDEDataAssessmentScript.ipynb


***
### 0) Code File: 0_WYssro_PreProcessAllocationData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple DataFrames creation and extraction.

#### Inputs: 
 - All site csv files for both 'Total Lake/Reservoir Volume' and 'Discharge" parameter data types.
 - Relevant timeseries data per site for both 'Total Lake/Reservoir Volume' and 'Discharge" parameter data types.

#### Outputs:
 - P_wySSROMain.csv

#### Operation and Steps:
- Site information had to be retrieved and downloaded separately per element.  Read in the following input csv data files per parameter data type...
    - data set label.csv
    - latitude.csv
    - longitude.csv
    - location identifier.csv
    - location name.csv
    - location type.csv
- Left-Merge the site csv files by **Data Set Id** input value.
- To retrieve timeseries data using the seoflow API service...
    - Take the **timeseriesID** input value from the site file and replace " " strings with "%20", and "@" strings with "%40".
    - Using the newly formatted **timeseriesID** input value, use the provided API to retrieve timeseries data per site
        - ex: https://seoflow.wyo.gov/Export/BulkExport?DateRange=EntirePeriodOfRecord&Datasets[0].DatasetName=Total%20Storage.Reservoir%20Capacity%400102HSPR
        - UnitId=198 is AF for 'Total Lake/Reservoir Volume' data, while UnitId=208 is CFS for 'Discharge" data.
        - We want daily data.
- Merge site data with timeseries data via **timeseriesID** and **Data Set Id** values.
- Concatenate 'Total Lake/Reservoir Volume' and 'Discharge" data together into single output dataframe.
- Review for errors.
- Export output DataFrames as new csv file, *P_wySSROMain.csv*.


***
### 1) Code File: 1_WYssro_Methods.py
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
MethodUUID | ApplicableResourceTypeCV | MethodDescription | MethodTypeCV
---------- | ---------- | ------------ | ------------
WYssro_M1 | Surface Water | Reservoir Capacity and Discharge Records | WaDE Unspecified



***
### 2) Code File: 2_WYssro_Variables.py
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
WYssro_V1 | 1 | Daily | AF | Storage | Storage_Daily_Storage_Surface Water



***
### 3) Code File: 3_WYssro_Organizations.py
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
WYssro_O1 | Wyoming Water Development Office | Mabel Jones | https://wwdc.state.wy.us/



***
### 4) Code File: 4_WYssro_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_wySSROMain.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE WaterSources* specific columns.
- Assign state agency info to columns.  See *WY_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = Not given, use *WaDE Unspecified* as filler.
    - *WaterSourceNativeID* = Not given, use *WaDEID_WYws1* as filler.
    - *WaterSourceTypeCV* = "Surface Water"
- Consolidate output DataFrames into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output DataFrames.
- Export output DataFrames *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
WSssro_WS1 | Fresh | WaDE Unspecified | WaDEID_WYws1 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_WYssro_Sites.py
Purpose: generate a list of sites specific to the site specific time series water data.

#### Inputs:
- P_wySSROMain.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE Site* specific columns.
- Assign state agency info to columns.  See *WY_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *CoordinateAccuracy* = Not given, use *WaDE Unspecified* as filler.
    - *CoordinateMethodCV* = Not given, use *WaDE Unspecified* as filler.
    - *County* = Not given, use *WaDE Unspecified* as filler.
    - *HUC12* = Not given, use *WaDE Unspecified* as filler.
    - *HUC8* = Not given, use *WaDE Unspecified* as filler.
    - *Latitude* = **latitude** input.
    - *Longitude* = **longitude** input.
    - *PODorPOUSite* = "Reservoir" for 'Total Lake/Reservoir Volume' data, and "Stream Gage" for 'Discharge" data.
    - *SiteNativeID* = **location identifier** input.
    - *SiteName* = **location name** input.
    - *SiteTypeCV* = "Reservoir/Lake" for 'Total Lake/Reservoir Volume' data, and "Hydrology Station" for 'Discharge" data.
    - *StateCV* = "WY".
- Consolidate output DataFrames into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output DataFrames.
- Export output DataFrames *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID |SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
WYssro_S1 | WaDE Unspecified | 41.71581 | -104.19579 | Hawksprings Reservoir | 0102HSPR | Reservoir/Lake

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_WYssro_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific timeseries water data to import into WaDE 2.0.

#### Inputs:
- P_wySSROMain.csv
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
- Assign state agency data info to columns.  See *WY_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **Average (Acre-ft)** for 'Total Lake/Reservoir Volume' data, and **Value at End of Interval (ft^3/s)** for 'Discharge" data.
    - *BeneficialUseCategory* = "Storage" for 'Total Lake/Reservoir Volume' data, and "Discharge" for 'Discharge" data.
    - *ReportYearCV* = extract year value from either WaDE *TimeframeStart* or *TimeframeEnd* fields.
    - *TimeframeStart* = **Start of Interval (UTC)** input.
    - *TimeframeEnd* = **End of Interval (UTC)** input.
- Perform error check on output DataFrames.
- Export output DataFrames *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
WYssro_M1 | WYssro_O1 | WYssro_S26 | WYssro_V1 | WYssro_WS1 | 0.0 | Storage | 2011 | 2011-09-27 | 2011-09-28

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
### 7) Code File: 7_WYssro_WaDEDataAssessmentScript.py
Purpose: generate visuals and analytics used by the WaDE staff to inspect the processed data.



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Wyoming Water Development Office (WWDO)](https://wwdc.state.wy.us/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

Wyoming DNRC Staff
- Mabel Jones <mabel.jones1@wyo.gov>
