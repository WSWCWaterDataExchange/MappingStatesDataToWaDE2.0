# TCEQ Stream and Reservoir Observation Site Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting stream and reservoir observation site time series water data made available by the [Texas Commission on Environmental Quality (TCEQ)](https://www.tceq.texas.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for timeseries observation site water data...

- [Reservoir data](https://www.waterdatafortexas.org/reservoirs/download) provided both site data and timeseries data for reservoir locations.
- Site information available in both csv and JSON format.  Longitude and Latitude information extracted from the **gauge_location** field ahead of time.
- Reservoir storage & reservoir level timeseries data was gathered using site info and provided url service (ex: https://www.waterdatafortexas.org/reservoirs/individual/b-a-steinhagen.csv)

Unique files were created to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - *recent-conditions.csv*, which contains site info.
 - *timeSeriesData.zip*, which contains reservoir storage & reservoir level timeseries. Saved to zip to conserve room.

 ## Storage for WaDE2 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE2 database, can both be found within the WaDE2 sponsored Google Drive.  Please contact WaDE2 staff if unavailable or if you have any questions about the data.
- Texas Site Specific Reservoir and Gage Data: https://drive.google.com/drive/folders/1swm35OFnojM7HuVWcrrp1LcGs2jkYX_C?usp=share_link



## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CSWRCB's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *TX_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx*.  Seven executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those six code files are as follows...

- 0_PreProcessTXReservoirObservationSites.ipynb
- 1_TXssro_Methods.py
- 2_TXssro_Variables.py
- 3_TXssro_Organizations.py
- 4_TXssro_WaterSources.py
- 5_TXssro_Sites.py
- 6_TXssro_SiteSpecificAmounts_fact.py


***
### 0) Code File: 0_PreProcessTXReservoirObservationSites.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple DataFrames creation and extraction.

#### Inputs: 
 - recent-conditions.csv
 - timeSeriesData.zip

#### Outputs:
 - P_txSSROMain.zip

#### Operation and Steps:
- Read in input csv data, place into temporary dataframes for stream site data.
- Create temporary *apiSiteName* field from provided **short_name** field by removing speical characters.
- Create list of *apiSiteName* values.  This will be used as part of the url timeseries service to gather data for each site.
- To gather time series data...
    - Use generated *apiSiteName* list to gather data from url service, use format of "https://www.waterdatafortexas.org/reservoirs/individual/" + str(apiSiteNameList[i]) + ".csv" as input.
    - Attach *apiSiteName* to timeseries data.
    - Join site data to timeseries data via *apiSiteName* field.
    - Concatenate each site into single output dataframe.
    - Resulting output file is rather large, save to zip file as *timeSeriesData.zip*.
- For output dataframe information...
    - WaDE *in_VariableCV* field = "Reservoir Level" & "Reservoir Storage" respectively.
    - WaDE *WaterSourceTypeCV* field = "Surface Water"
    - WaDE *Latitude* field = **Latitude** extracted from **gauge_location** input.
    - WaDE *Longitude* field = **Longitude** **gauge_location** input.
    - WaDE *SiteName* field = **short_name** input.
    - WaDE *SiteNativeID* field = **siteid** input.
    - WaDE *SiteTypeCV* field = "Reservoir".
    - WaDE *Amount* Field = **water_level** for Reservoir Level & **reservoir_storage** for Reservoir Storage respectively.
    - WaDE *Beneficial Use* = "Storage".
    - WaDE *ReportYear* field = **date** input, extract year value.
    - WaDE *TimeframeStart* field = **date** input (working with daily data).
    - WaDE *TimeframeEnd* field = **date** input (working with daily data).
- Concatenate Reservoir Level & Reservoir Storage data together into single output dataframe.
- Create WaDE Specific *SiteNativeID* field using created *SiteName* field for unique values, helps cut down on searching.
- Review for errors.
- Export output DataFrames as new csv file, *P_txSSROMain.zip*.


***
### 1) Code File: 1_TXssro_Methods.py
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
TXssro_M1 | Surface Water | Measured



***
### 2) Code File: 2_TXssro_Variables.py
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
TXssro_V1 | 1 | Daily | FT | Reservoir Level | Reservoir Level_Daily_Storage_Surface Water



***
### 3) Code File: 3_TXssro_Organizations.py
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
TXssro_O1 | Texas Commission on Environmental Quality | Kathy Alexander | https://www.tceq.texas.gov/



***
### 4) Code File: 4_TXssro_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_txSSROMain.zip

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE WaterSources* specific columns.
- Assign state agency info to columns.  See *TX_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceNativeID* = single entry of WaDEWS_WS1.
    - *WaterSourceTypeCV* = single entry of "Surface Water"
- Consolidate output DataFrames into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output DataFrames.
- Export output DataFrames *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
TXssro_WS1 | Fresh | Unspecified | WaDETX_WS1 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_TXssro_Sites.py
Purpose: generate a list of sites specific to the site specific time series water data.

#### Inputs:
- P_txSSROMain.zip

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE Site* specific columns.
- Assign state agency info to columns.  See *TX_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - WaDE *Latitude* field = **Latitude** extracted from **gauge_location** input.
    - WaDE *Longitude* field = **Longitude** **gauge_location** input.
    - WaDE *SiteName* field = **short_name** input.
    - WaDE *SiteNativeID* field = **siteid** input.
    - WaDE *SiteTypeCV* field = "Reservoir".
- Consolidate output DataFrames into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output DataFrames.
- Export output DataFrames *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
TXssro_S1 | Unspecified | 32.23457718 | -99.88897705 | LAKE ALMANOR | Abilene | Reservoir

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_TXssro_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific timeseries water data to import into WaDE 2.0.

#### Inputs:
- P_txSSROMain.zip
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
- Assign state agency data info to columns.  See *TX_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - WaDE *Amount* Field = **water_level** for Reservoir Level & **reservoir_storage** for Reservoir Storage respectively.
    - WaDE *Beneficial Use* = "Storage".
    - WaDE *ReportYear* field = **date** input, extract year value.
    - WaDE *TimeframeStart* field = **date** input (working with daily data).
    - WaDE *TimeframeEnd* field = **date** input (working with daily data).
- Perform error check on output DataFrames.
- Export output DataFrames *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
TXssro_M1 | TXssro_O1 | TXssro_S2 | TXssro_V1 | TXssro_WS1 | 1999.87 | Storage | 1999 | 03/05/1999 | 03/05/1999

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Texas Commission on Environmental Quality (TCEQ)](https://www.tceq.texas.gov/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

TCEQ Staff
- Kathy Alexander <kathy.alexander@tceq.texas.gov>