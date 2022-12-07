# MDNRC Site Specific Reservoir and Observation Site Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting Site Specific Reservoir and Observation Site series water data made available by the [The Montana Department of Natural Resources and Conservation (MDNRC)](http://dnrc.mt.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Source Data Utilized
The following data was used for aggregated water budget...

- [MDNRC Stream and Gage Explorer Download](https://gis.dnrc.mt.gov/apps/StAGE/#) time series data for stream water surface water, retrieved via saving map to ArcGIS and convert feature-class to table.  Data used in particualar incldued **MGS datasets**, **MGS locaitons**, and **MGS timeseries** tables.


Unique files were created to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - MGS_datasets.csv
 - MGS_locations.csv
 - MGS_timeseries.csv

  ## Storage for WaDE2 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE2 database, can both be found within the WaDE2 sponsored Google Drive.  Please contact WaDE2 staff if unavailable or if you have any questions about the data.
- Montana Site Specific Reservoir and Observation Site Data: https://drive.google.com/drive/folders/1Z7OzJU79arz3OFrRErtTnbv4KoBxZVXh?usp=sharing



## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share MDNRC's Site Specific Reservoir and Observation Site series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *MT_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx*.  Six executable code files were used to extract the state agency's Site Specific Reservoir and Observation Site series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those six code files are as follows...

- PreProcessMTReservoirObservationSites.ipynb
- 1_MTssro_Methods.py
- 2_MTssro_Variables.py
- 3_MTssro_Organizations.py
- 4_MTssro_WaterSources.py
- 5_MTssro_Sites.py
- 6_IDssro_SiteSpecificAmounts_fact.py



***
### 0) Code File: PreProcessMTReservoirObservationSites.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - MGS_datasets.csv
 - MGS_locations.csv
 - MGS_timeseries.csv

#### Outputs:
 - P_mtOSMaster.csv

#### Operation and Steps:
- Create unique dataframes for each inpute file: MGS_datasets, MGS_locations, & MGS_timeseries.
- For MGS_dataset dataframe... 
        - We are only interested in the following information at this time...
            - **SensorLabel** = discharge or stage.
        - Remove uncesseary columns.
    - Left-join merge reduced MGS_dataset dataframe with MGS_locations dataframe via **LocationCode** field.
- For MGS_timeseries dataframe...
    - We only need timeseries records that match the combined MGS_dataset & MGS_locations dataframe.  Crease **SensorID** list, use list to remove unused elements.
    - Convert **Timestamp** string to datetime dtype.
    - Extract date value from **Timestamp** field in form of %mm/%dd/%YYYY.
    - Extract year value from **Timestamp** field in the form of YYYY.
    - Remove uncesseary columns.
- Left-join merge reduced MGS_timeseries dataframe with combined MGS_dataset & MGS_locations dataframe via **SensorID** field.
- Review for errors.
- Export output dataframe as new csv file, *P_mtOSMaster.csv*.



***
### 1) Code File: 1_MTssro_Methods.py
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
MTssro_M1 | Surface Water | Measured



***
### 2) Code File: 2_MTssro_Variables.py
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
MTssro_V1 | Daily | Average | CFS



***
### 3) Code File: 3_MTssro_Organizations.py
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
MTssro_O1 | The Montana Department of Natural Resources and Conservation | Chris Kuntz | http://dnrc.mt.gov/



***
### 4) Code File: 4_MTssro_WaterSources.py
Purpose: generate a list of water sources specific to the Site Specific Reservoir and Observation Site series water data.

#### Inputs:
- P_mtOSMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency info to columns.  See *MT_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - NA.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
MTssro_WS1 | Fresh | Unspecified | WaDEID_MTWS1 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_MTssro_Sites.py
Purpose: generate a list of polygon areas associated with the state agency specific site on aggregated water budget data.

#### Inputs:
- P_mtOSMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to columns.  See *MT_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* respective watersourcecsv files. See code for specific implementation of extraction.
    - *CoordinateMethodCV* = "Unspecified".
    - *Latitude* = **Latitude**.
    - *Longitude* = **Longitude**.
    - *SiteName* = **LocationName**.
    - *PODorPOUSite* = "Gage".
    - *SiteNativeID* = **LocationCode**.
    - *SiteTypeCV* = **LocationType**.
- Consolidate output dataframe into observation site information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
MTssro_S1 | Unspecified | 46.6094 | -110.5768 | NF Musselshell near Delphine | 40A 1500 | Hydrology Station

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_IDssro_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency Site Specific Reservoir and Observation Site series water data to import into WaDE 2.0.

#### Inputs:
- P_mtOSMaster.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water observation site Amounts* data columns.
- Assign state agency data info to columns.  See *MT_SS_ReservoirsObservationSitesSchema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **numericValue1**.
    - *ReportYearCV* = year value extracted from **timeStamp**.
    - *TimeframeStart* = **timeStamp**.
    - *TimeframeEnd* = **timeStamp**.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
MTssro_M1| MTssro_V1 | MTssro_S1 | MTssro_V1 | MTssro_WS1 | 14 | Discharge | 1980 | 05/01/1980 | 5/01/1980 

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
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [The Montana Department of Natural Resources and Conservation (MDNRC)](http://dnrc.mt.gov/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

MDNRC Staff
- Chris Kuntz <CKuntz@mt.gov>