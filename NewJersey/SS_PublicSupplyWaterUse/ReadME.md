# New Jersey DWSG Site Specific Public Supply Data Preparation for WaDE2
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [New Jersey Division of Water Supply and Geoscience (DWSG)](https://www.nj.gov/dep/watersupply/), for inclusion into the Water Data Exchange (WaDE2) project.  WaDE2 enables states to share data with each other and the public in a more streamlined and consistent way. WaDE2 is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 



## Overview of Source Data Utilized
The following data was used for timeseries site specific water data...
- [Water Transfer Model Withdrawal, Use, and Return Data Summaries](https://www.nj.gov/dep/njgs/geodata/dgs10-3.htm) time series data. Data is withdrawal and return data "per site" within a municipal boundary area.  There are multiple sites per municipal boundary area.
- [Municipal Boundaries of NJ](https://gisdata-njdep.opendata.arcgis.com/datasets/newjersey::municipal-boundaries-of-nj/about) shapefile data for municipal areas.

Unique files were created to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - **return_MunDischarge.csv**, timeseries amount info for return data
 - **return_MunInfo.csv**, has the keys needed to attach shapefile info
 - **return_MunSiteInfo.csv**, has water source & type info for return data
 - **withd_MunWithdrawal.csv**, timeseries amount info for withdrawal data
 - **withd_MunInfo.csv**, has the keys needed to attach shapefile info
 - **withd_MunSiteInfo.csv**, has water source & type info for withdrawal data
 - **Municipal_Boundaries_of_NJ.xlsx** & **shp** files

## Storage for WaDE2 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE2 database, can both be found within the WaDE2 sponsored Google Drive.  Please contact WaDE2 staff if unavailable or if you have any questions about the data.
- New Jersey Site Specific Public Supply Data: https://drive.google.com/drive/folders/1dU7nAtYHMLfnm40uEVarWzYvvJdRnn_W?usp=sharing



## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share DWSG's site specific time series water data for inclusion into the Water Data Exchange (WaDE2 2.0) project.  For a complete mapping outline, see *NJ_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx*.  Eight executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those code files are as follows...

- 0_PreProcessNJSSPublicSupplyWaterUseData.ipynb
- 1_NJssps_Methods.py
- 2_NJssps_Variables.py
- 3_NJssps_Organizations.py
- 4_NJssps_WaterSources.py
- 5_NJssps_Sites.py
- 6_NJssps_SiteSpecificAmounts_fact.py
- 7_NJssps_PODSiteToPOUSiteRelationships.py



***
### 0) Code File: 0_PreProcessNJSSPublicSupplyWaterUseData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - return_MunDischarge.csv
 - return_MunInfo.csv
 - return_MunSiteInfo.csv
 - withd_MunWithdrawal.csv
 - withd_MunInfo.csv
 - withd_MunSiteInfo.csv
 - Municipal_Boundaries_of_NJ.xlsx & shp files

#### Outputs:
 - P_njSSMaster.csv
 - P_njSSGeometry.csv

#### Operation and Steps:
- Read in all input files.  Process will involve matching timeseries amount data to the info data via **MCDCode** field -> timeseries amount data to shapefile data via **GNISCode** field -> and timeseries amount to siteinfo data via **SiteName** field.  Repeat process for both return and withdrawal data.
- For both return and withdrawal data...
    - WaDE2 *VariableCV* field = *Return* or *Withdrawal* respectively per dataset.
    - WaDE2 *WaterSourceTypeCV* field = **GWorSW** input.  Will need to translate from abbreviation to full words.
    - WaDE2 *County* field = **COUNTY** input.
    - WaDE2 *NISCodeCV* field = **GNIS** input.
    - WaDE2 *Latitude* field = **Lat** input, generated from centroid of area from the shapefile data.
    - WaDE2 *Longitude* field = **Long** input, generated from centroid of area from the shapefile data.
    - WaDE2 *SiteName* field = **NAME** input.
    - WaDE2 *SiteNativeID* field = **GNIS** input.  Format to string value.
    - WaDE2 *SiteTypeCV* field = **MUN_TYPE** input.
    - WaDE2 *Amount* field = **ReturnMG** or **WithdrawalMG** inputs repetitively per dataset.
    - WaDE2 *AssociatedNativeAllocationIDs* field = **PermitNumber** input.
    - WaDE2 *Beneficial Use* = **UseGroup** input.
    - WaDE2 *CommunityWaterSupplySystem* field = **GNIS_NAME** input.
    - WaDE2 *PopulationServed* field = **POP2010** input.  Format to numeric value.
    - WaDE2 *ReportYearCV* field = **YearNumber** input.  Format to numeric value.
    - WaDE2 *TimeframeStart* field = **YearNumber** + **MonthNumber** "01" input.  Format to YYYY-MM_DD.
    - WaDE2 *TimeframeEnd* field = **YearNumber** + **MonthNumber** "28" input.  Format to YYYY-MM_DD.  Temp fix of 28 for easy data input.
- Concatenate both return and withdrawal timeseries info into single output dataframe.
- Create WaDE2 field *WaterSourceNativeID* field using created *WaterSourceTypeCV* field, which helps to create a unique ID.
- Create WaDE2 field *VariableSpecificCV* by concatenating the words "Return" or "Withdrawal" respectively, the word "Monthly", **UseGroup**, and translated **GWorSW**.  Creates unique field to help filter specific timeseries amount type(s).
- Multiple sites per area.  Decision made to aggregate each site amounts per area.  Groupby *SiteNativeID*, *VariableSpecificCV*, *TimeframeStart*, & *TimeframeEnd*, and sum the **ReturnMG** or **WithdrawalMG** inputs repetitively per dataset per unique combo.
- Format WaDE2 *TimeframeStart* & *TimeframeEnd* fields to YYYY-MM_DD format.
- For shapefile data...
    - Read in Municipal_Boundaries_of_NJ.shp data, create shapefile dataframe.
    - WaDE2 *SiteNativeID* field = **GNIS** input, format to string value.
    - WaDE2 *Geometry* field = **geometry** input.
- Review for errors in both timeseries and shapefile ouput dataframes
- Export output dataframe(s) as new csv file, *P_njSSMaster.csv* & *P_njSSGeometry.csv*.



***
### 1) Code File: 1_NJssps_Methods.py
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
NJssps_M1 | Surface Ground Water | Estimate



***
### 2) Code File: 2_NJssps_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
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
NJssps_V5 | 1 | Monthly | MG | Return | Return_Monthly_Potable Supply_Groundwater



***
### 3) Code File: 3_NJssps_Organizations.py
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
NJssps_O1 | New Jersey Division of Water Supply and Geoscience | Steven Domber, Kent Barr | https://www.nj.gov/dep/watersupply/



***
### 4) Code File: 4_NJssps_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_njSSMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 WaterSources* specific columns.
- Assign state agency info to columns.  See *NJ_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = "Unspecified".
    - *WaterSourceNativeID* = see *0_PreProcessNJSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *WaterSourceTypeCV* = **GWorSW**, see *0_PreProcessNJSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE2 specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NJssps_WS1 | Fresh | Unspecified | WaDENJ_WS3 | Groundwater

Any data fields that are missing required values and dropped from the WaDE2-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_NJssps_Sites.py
Purpose: generate a list of sites specific to the site specific time series water data.

#### Inputs:
- P_njSSMaster.csv
- P_njSSGeometry.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Site* specific columns.
- Assign state agency info to columns.  See *NJ_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersource.csv input file. See code for specific implementation of extraction.
    - *CoordinateMethodCV* = "Centroid of Area"
    - *County* = **COUNTY**.
    - *Geometry* = **geometry** input from shapefile data, match via *SiteNativeID*.
    - *Latitude* = **Lat**, see *0_PreProcessNJSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *Longitude* = **Long**, see *0_PreProcessNJSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *PODorPOUSite* = "POU" for Point of Use.
    - *SiteName* = **NAME**.
    - *SiteNativeID* = **GNIS**, see *0_PreProcessNJSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *SiteTypeCV* = **MUN_TYPE**.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE2 specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
NJssps_S1 | Centroid of Area | 40.7242762719 | -74.2317529168999 | Irvington | 877363 | Township

Any data fields that are missing required values and dropped from the WaDE2-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_NJssps_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific timeseries water data to import into WaDE2 2.0.

#### Inputs:
- P_njSSMaster.csv
- variables.csv
- watersources.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Water Site Specific Public Supply Amounts* data columns.
- Assign state agency data info to columns.  See *NJ_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **ReturnMG** or **WithdrawalMG**.
    - *BeneficialUseCategory* =  **UseGroup**.
    - *CommunityWaterSupplySystem* = **GNIS_NAME**.
    - *CustomerTypeCV* = "Municipal".
    - *PopulationServed* = **POP2010**.
    - *ReportYearCV* = **YearNumber**.
    - *TimeframeStart* = see *0_PreProcessNJSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
    - *TimeframeEnd* = see *0_PreProcessNJSSPublicSupplyWaterUseData.ipynb* for specifics on generation.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
NJssps_M1 | NJssps_O1 | NJssps_S460 | NJss_V2 | NJssps_WS1 | 0.0719999969005585 | Not Classified | 2000 | 10/1/2000 | 10/28/2000

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
### 7) Code File: 7_NJssps_PODSiteToPOUSiteRelationships.py
Not applicable for the current data.  Missing point of distribution data and connections with place of use.



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [New Jersey Division of Water Supply and Geoscience (DWSG)](https://www.nj.gov/dep/watersupply/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

DWSG Staff
- Steven Domber <Steven.Domber@dep.nj.gov>
- Kent Barr <Kent.Barr@dep.nj.gov>
