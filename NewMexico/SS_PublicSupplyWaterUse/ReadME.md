# New Mexico NMOSE Site Specific Public Supply Data Preparation for WaDE2
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [New Mexico Office of the State Engineer (HMOSE)](https://www.ose.state.nm.us/), for inclusion into the Water Data Exchange (WaDE2) project.  WaDE2 enables states to share data with each other and the public in a more streamlined and consistent way. WaDE2 is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 



## Overview of Source Data Utilized
The following data was used for timeseries site specific water data...
- [NM PWS Points](https://catalog.newmexicowaterdata.org/dataset/public-water-supply-areas) time series and site info data. Data is withdrawal per point of diversion site.
- [NM_PWS AreasJ](https://catalog.newmexicowaterdata.org/dataset/public-water-supply-areas) shapefile area data to tie POU for POD timeseries data.

Unique files were created to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - **NMPWSPoints.csv**, timeseries withdrawal data per point of diversion.
 - **nm_pws.csv**, area data. has the keys needed to attach shapefile info
 - **nm_pws.shp** files to extract geometry from.

## Storage for WaDE2 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE2 database, can both be found within the WaDE2 sponsored Google Drive.  Please contact WaDE2 staff if unavailable or if you have any questions about the data.
- New Mexico Site Specific Public Supply Data: https://drive.google.com/drive/folders/1Ow7qEDA5MWz__1UxTNKZOizBbQB5vh9V



## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share DWSG's site specific time series water data for inclusion into the Water Data Exchange (WaDE2 2.0) project.  For a complete mapping outline, see *NM_SS_PublicSupplyWaterUse Schema Mapping to WaDE.xlsx*.  Eight executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those code files are as follows...

- 0_PreProcessNMSSPublicSupplyWaterUseData.ipynb
- 1_NMssps_Methods.py
- 2_NMssps_Variables.py
- 3_NMssps_Organizations.py
- 4_NMssps_WaterSources.py
- 5_NMssps_Sites.py
- 6_NMssps_SiteSpecificAmounts_fact.py
- 7_NMssps_PODSiteToPOUSiteRelationships.py



***
### 0) Code File: 0_PreProcessNMSSPublicSupplyWaterUseData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - **NMPWSPoints.csv**, timeseries withdrawal data per point of diversion.
 - **nm_pws.csv**, area data. has the keys needed to attach shapefile info
 - **nm_pws.shp** files to extract geometry from.

#### Outputs:
 - P_nmSSPWMain.csv
 - P_nmSSPWGeometry.csv

#### Operation and Steps:
- Read in all input files.
- For timeseries withdrawal POD data there will be four different datasets separated out by year and water source type....
    - we only want to work with active records, **DWB_STATUS = A**.
    - *VariableCV* field = *Withdrawal*
    - *WaterSourceTypeCV* field = Groundwater or Surface Water, depnding on timeseries.
    - *County* field = **CountyName_HA** input.
    - *HUC8* field = **HUC_8** input. 
    - *Latitude* field = **Latitude** input.
    - *Longitude* field = **Longitude** input.
    - *PODorPOUSite* field = POD.
    - *SiteName* field = Unspecified.
    - *SiteNativeID* field = **ID** input.
    - *Amount* field = **F2010_GW_AFY**, **F2015_GW_AFY**, **F2010_SW_AFY**, **F2015_SW_AFY** inputs repetitively per dataset.
    - *Beneficial Use Category* = Unspecified.
    - *CommunityWaterSupplySystem* field = **Public_Water_System_Name_2019** input.
    - *PopulationServed* field = **F2010_Population** or **F2015_Population** inputs repetitively per dataset. Format to numeric.
    - *ReportYearCV* field = 2010 or 2015 repetitively per dataset.
    - *TimeframeStart* field = "01/01/" + 2010 or 2015 repetitively per dataset.
    - *TimeframeEnd* field = "12/31/" + 2010 or 2015 repetitively per dataset.
    - Concatenate all timeseries withdrawal POD dataframes into single POD dataframe.
- For place of use data...
    - left-join input timeseries withdrawal POD data by left_on=**Wt_S_ID** & right_on=**WaterSystem_ID** to extract a few values
    - *Latitude* field = **cent_Lat**, extract from shapefile.
    - *Longitude* field = **cent_Long**, extract from shapefile.
    - *PODorPOUSite* field = POU.
    - *SiteName* field = **PblcSyN** input.
    - *SiteNativeID* field = **Wt_S_ID** input.
    - *CommunityWaterSupplySystem* field = **PblcSyN** input.
- Concatenate both POD and POU dataframes into single output dataframe.
- Create WaDE2 field *VariableSpecificCV* by concatenating the words "Withdrawal_Annual_Unspecified" respectively with the water source type of each timeseries.
- Create WaDE2 field *WaterSourceNativeID* field using created *WaterSourceTypeCV* field, which helps to create a unique ID.
- Format WaDE2 *TimeframeStart* & *TimeframeEnd* fields to YYYY-MM_DD format.
- For shapefile data...
    - Read in nm_pws.shp data, create shapefile dataframe.
    - WaDE2 *SiteNativeID* field = **Wt_S_ID** input, format to string value.
    - WaDE2 *Geometry* field = **geometry** input.
- Review for errors in both timeseries and shapefile ouput dataframes
- Export output dataframe(s) as new csv file, *P_nmSSPWMain.csv* & *P_nmSSPWGeometry.csv*.



***
### 1) Code File: 1_NMssps_Methods.py
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
NMssps_M1 | Surface Water & Groundwater | Estimated



***
### 2) Code File: 2_NMssps_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:NMssps_O1
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
NMssps_V5 | 1 | Annual | AF | Withdrawal | Withdrawal_Annual_Unspecified_Groundwater



***
### 3) Code File: 3_NMssps_Organizations.py
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
NMssps_O1 | New Mexico Office of the State Engineer | David Hatchner (GIS Manager) | https://www.ose.state.nm.us/



***
### 4) Code File: 4_NMssps_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_nmSSPWMain.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 WaterSources* specific columns.
- Assign state agency info to columns.  See *NM_SS_PublicSupplyWaterUse Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = "Unspecified".
    - *WaterSourceNativeID* = see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *WaterSourceTypeCV* = * see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE2 specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NMssps_WS1 | Fresh | Unspecified | WaDNMD_WS1 | Groundwater

Any data fields that are missing required values and dropped from the WaDE2-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_NMssps_Sites.py
Purpose: generate a list of sites specific to the site specific time series water data.

#### Inputs:
- P_nmSSPWMain.csv
- P_nmSSPWGeometry.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Site* specific columns.
- Assign state agency info to columns.  See *NM_SS_PublicSupplyWaterUse Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersource.csv input file. See code for specific implementation of extraction.
    - *County* = **CountyName_HA**.
    - *Geometry* = **geometry** input from shapefile data, match via *SiteNativeID*.
    - *Latitude* =  see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *Longitude* = see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *PODorPOUSite* = POU or POD
    - *SiteName* = see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *SiteNativeID* = see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *SiteTypeCV* = Unspecified.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE2 specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
NMssps_S1 | Unspecified | 34.94121336 | -106.2738511 | Unspecified | 1 | Unspecified

Any data fields that are missing required values and dropped from the WaDE2-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_NMssps_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific timeseries water data to import into WaDE2 2.0.

#### Inputs:
- P_nmSSPWMain.csv
- variables.csv
- watersources.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Water Site Specific Public Supply Amounts* data columns.
- Assign state agency data info to columns.  See *NM_SS_PublicSupplyWaterUse Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *BeneficialUseCategory* =  see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *CommunityWaterSupplySystem* = see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *PopulationServed* = see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *ReportYearCV* = see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *TimeframeStart* = see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *TimeframeEnd* = see *0_PreProcessNMSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
NMssps_M1 | NMssps_O1 | NMssps_S1 | NMssps_V1 | NMssps_WS1 | 6.575 | Unspecified | 01/01/2010 | 12/31/2010

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
### 7) Code File: 7_NMssps_PODSiteToPOUSiteRelationships.py
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
- Left-merge site.csv info to the sitespecificamounts DataFrames via *SiteUUID* field.
- Split into two new temporary dataframes: one POD centric, the other POU centric.
- For the temporary POD DataFrames...
    - Create *PODorPOUSite* field = POD.
- For the temporary POU DataFrames
    - Create *PODorPOUSite* field = POU.
- Merge POD & POU dataframes into single output DataFrames, only using unique rows.
- Find *SiteUUID* baesed on *PODorPOUSite* field.
- Perform error check on waterallocations DataFrames (check for NaN values)
- If waterallocations is not empty, export output DataFrames *podsitetopousiterelationships.csv*.



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Nevada Division of Water Resources [New Mexico Office of the State Engineer (NMOSE)](https://www.ose.state.nm.us/).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

NMOSE Staff
- David Hatchner (GIS Manager)<ose.webmaster@state.nm.us>
