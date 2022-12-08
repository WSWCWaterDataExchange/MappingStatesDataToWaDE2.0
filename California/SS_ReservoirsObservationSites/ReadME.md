# CDWR Stream and Reservoir Observation Site Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting stream and reservoir observation site time series water data made available by the [California Department of Water Resources](https://water.ca.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for timeseries observation site water data...

- [California Stream Gages](https://gispublic.waterboards.ca.gov/portal/home/item.html?id=32dfb85bd2744487affe6e3475190093) site data, available for ArcGIS.  Non-federal sites of interest where chosen.
- [Reserovir](https://cdec.water.ca.gov/misc/monthly_res.html) site data, copied from a table and pasted into a csv file.
- Stream gage and reservoir level time series data was aquired using a CDWR API, using specific SensorNums (see *0_PreProcessCAReservoirObservationSites.ipynb* below for specifics).  Non-federal sites of interest where chosen.

Unique files were created to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - StreamGages_caOnly.csv
 - ReservoirGages_caOnly.csv

 ## Storage for WaDE2 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE2 database, can both be found within the WaDE2 sponsored Google Drive.  Please contact WaDE2 staff if unavailable or if you have any questions about the data.
- California Site Specific Reservoir and Gage Data: https://drive.google.com/drive/folders/1VTcznMjDIg8F3vk3SAj_Zf_VcJm6Rniq?usp=sharing



## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CSWRCB's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *CA_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx*.  Six executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those six code files are as follows...

- 0_PreProcessCAReservoirObservationSites.ipynb
- 1_CAssro_Methods.py
- 2_CAssro_Variables.py
- 3_CAssro_Organizations.py
- 4_CAssro_WaterSources.py
- 5_CAssro_Sites.py
- 6_CAssro_SiteSpecificAmounts_fact.py


***
### 0) Code File: 0_PreProcessCAReservoirObservationSites.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple DataFrames creation and extraction.

#### Inputs: 
 - StreamGages_caOnly.csv
 - ReservoirGages_caOnly.csv

#### Outputs:
 - P_caObsRecords.csv

#### Operation and Steps:
- Read in input csv data, place into temporary dataframes for stream and reservoir site data respectively.
- For stream data...
    - Extract list of site IDs from the **siteid**
    - Use **SensorNums=65** for monthly stream gage time series values.
    - Use **siteid** & **SensorNums=65** values with API, tie to stream dataframe.
    - WaDE *in_VariableSpecificCV* field = "Stream Gage_Monthly_Stage_Surface Water".
    - WaDE *WaterSourceTypeCV* field = **streamtype** input.
    - WaDE *HUC12* field = **huc12** input.
    - WaDE *HUC8* field = **huc8** input.
    - WaDE *Latitude* field = **Lat** created using shapefile.
    - WaDE *Longitude* field = **Long** created using shapefile.
    - WaDE *SiteName* field = **sitename** input.
    - WaDE *SiteNativeID* field = **siteid** input.
    - WaDE *SiteTypeCV* field = "Stream Gage".
    - WaDE *Amount* Field = **VALUE** input.
    - WaDE *Beneficial Use* = "Stage".
    - WaDE *CommunityWaterSupplySystem* = **operator** input.
    - WaDE *ReportYear*, *TimeframeStart*, & *TimeframeEnd* all extracted from **DATE TIME** input.
- For reservoir data...
    - Extract list of site IDs from the **ID**
    - Use **SensorNums=15** for monthly stream gage time series values.
    - Use **ID** & **SensorNums=15** values with API, tie to stream dataframe.
    - WaDE *in_VariableSpecificCV* field = "Reservoir Level_Monthly_Storage_Surface Water".
    - WaDE *WaterSourceTypeCV* field = "Surface Water".
    - WaDE *County* field = **County** input.
    - WaDE *Latitude* field = **Latitude** input.
    - WaDE *Longitude* field = **Longitude** input.
    - WaDE *SiteName* field = **Station** input.
    - WaDE *SiteNativeID* field = **ID** input.
    - WaDE *SiteTypeCV* field = "Reservoir Gage".
    - WaDE *Amount* Field = **VALUE** input.
    - WaDE *Beneficial Use* = "Stage".
    - WaDE *CommunityWaterSupplySystem* = **Operating Agency** input.
    - WaDE *ReportYear*, *TimeframeStart*, & *TimeframeEnd* all extracted from **DATE TIME** input.
- Concatenate stream gage and reservoir level DataFrames together into single output dataframe.
- Review for errors.
- Create WaDE Specific *WaterSourceNativeID* field using created *WaterSourceTypeCV* field, helps cut down on searching.
- Export output DataFrames as new csv file, *P_caObsRecords.csv*.


***
### 1) Code File: 1_CAssro_Methods.py
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
CAssro_M1 | Surface Water | Unspecified



***
### 2) Code File: 2_CAssro_Variables.py
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
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
CAssro_V1 | 1 | Monthly | AF



***
### 3) Code File: 3_CAssro_Organizations.py
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
CAssro_O1 | California Department of Water Resources | Jennifer Stricklin | https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/California



***
### 4) Code File: 4_CAssro_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_caObsRecords.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE WaterSources* specific columns.
- Assign state agency info to columns.  See *CA_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceNativeID* = see *0_PreProcessCAReservoirObservationSites.ipynb* for specific on generation.
    - *WaterSourceTypeCV* = see *0_PreProcessCAReservoirObservationSites.ipynb* for specific on generation.
- Consolidate output DataFrames into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output DataFrames.
- Export output DataFrames *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
CAssro_WS1 | Fresh | Unspecified | WaDECA_WS1 | Artificial Path

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_CAssro_Sites.py
Purpose: generate a list of sites specific to the site specific time series water data.

#### Inputs:
- P_caObsRecords.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output DataFrames *outdf*.
- Populate output DataFrames with *WaDE Site* specific columns.
- Assign state agency info to columns.  See *CA_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *County* = **COUNTY**.
    - *Latitude* = **Latitude**.
    - *Longitude* = **Longitude**.
    - *SiteName* = see *0_PreProcessCAReservoirObservationSites.ipynb* for specific on generation.
    - *SiteNativeID* = see *0_PreProcessCAReservoirObservationSites.ipynb* for specific on generation.
    - *SiteTypeCV* = see *0_PreProcessCAReservoirObservationSites.ipynb* for specific on generation.
- Consolidate output DataFrames into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output DataFrames.
- Export output DataFrames *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID |SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
CAssro_S1 | Unspecified | 40.218 | -121.172999999999 | LAKE ALMANOR | ALM | Reservoir Gage

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_CAssro_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific timeseries water data to import into WaDE 2.0.

#### Inputs:
- P_caObsRecords.csv
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
- Assign state agency data info to columns.  See *CA_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = *in_Amount*, see *0_PreProcessCAReservoirObservationSites.ipynb* for specific on generation.
    - *BeneficialUseCategory* =  see *0_PreProcessCAReservoirObservationSites.ipynb* for specific on generation.
    - *CommunityWaterSupplySystem* = see *0_PreProcessCAReservoirObservationSites.ipynb* for specific on generation.
    - *ReportYearCV* = see *0_PreProcessCAReservoirObservationSites.ipynb* for specific on generation.
    - *TimeframeStart* = *in_TimeframeStart*, see *0_PreProcessCAReservoirObservationSites.ipynb* for specific on generation.
    - *TimeframeEnd* = *in_TimeframeEnd*, see *0_PreProcessCAReservoirObservationSites.ipynb* for specific on generation.
- Perform error check on output DataFrames.
- Export output DataFrames *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
CAssro_M1 | CAssro_O1 | CAos_S2 | CAssro_V1 | CAssro_WS1 | 522700 | Stage | 1950 | 04/01/1950 | 04/01/1950 

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [California Department of Water Resources](https://water.ca.gov/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

CDWR Staff
- Jennifer Stricklin <Jennifer.Stricklin@water.ca.gov>