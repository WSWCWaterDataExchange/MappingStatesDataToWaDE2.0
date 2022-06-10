# NDDWR Site Specific Data Preparation for WaDE2
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [North Dakota Department of Water Resources (NDDWR)](https://www.swc.nd.gov/), for inclusion into the Water Data Exchange (WaDE2) project.  WaDE2 enables states to share data with each other and the public in a more streamlined and consistent way. WaDE2 is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 



## Overview of Source Data Utilized
The following data was used for timeseries site specific water data...
- Time series water use permit data was made available temporary to the WaDE2 staff through personal correspondence.  Contact NDDWR or WaDE2 staff for more information.

Unique files were created to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
- **Permit Header.csv**: contains a primary index (Permit_Index).
- **POD.csv**: contains a primary index (POD_Index)  This is tied back to the Permit Header table with the Permit_Index field
- **Water Use.csv**: contains both the POD_Index and the Permit_Index for purposes of aggregating it back to either the POD or the Permit.

## Storage for WaDE2 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE2 database, can both be found within the WaDE2 sponsored Google Drive.  Please contact WaDE2 staff if unavailable or if you have any questions about the data.
- North Dakota Site Specific Data: https://drive.google.com/drive/folders/1DG8PYG9ZU296XYCJaEJTl77fMh0NfYqD?usp=sharing



## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NDDWR's site specific time series water data for inclusion into the Water Data Exchange (WaDE2 2.0) project.  For a complete mapping outline, see *ND_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx*.  Eight executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those code files are as follows...

- 0_PreProcessNDSiteSpecificData.ipynb
- 1_NDss_Methods.py
- 2_NDss_Variables.py
- 3_NDss_Organizations.py
- 4_NDss_WaterSources.py
- 5_NDss_Sites.py
- 6_NDss_SiteSpecificAmounts_fact.py
- 7_NDss_PODSiteToPOUSiteRelationships.py



***
### 0) Code File: 0_PreProcessNDSiteSpecificData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - Permit Header.csv
 - POD.csv
 - Water Use.csv

#### Outputs:
 - P_ndSSMaster.csv

#### Operation and Steps:
- Read in all input files.  Processes will involve matching timeseries water use amount data -> POD site data via POD_Index -> Permit data via Permit_Index.  For Permit data, convert **Permit_Index** to string to match id of other data sets.
- For data...
    - WaDE2 *VariableCV* field = "Withdrawal".
    - WaDE2 *WaterSourceTypeCV* field = **Source** input.
    - WaDE2 *County* field = **County** input.
    - WaDE2 *Latitude* field = **Latitude** input.
    - WaDE2 *Longitude* field = **Longitude** input.
    - WaDE2 *SiteNativeID* field = **POD** input.  Format to string value.
    - WaDE2 *SiteTypeCV* field = **MUN_TYPE** input.
    - WaDE2 *Amount* field = **Reported_AcFt** input.  Will convert from AcFT to MG to match WaDE2 system.
    - WaDE2 *AssociatedNativeAllocationIDs* field = **Permit_Number** input.  Format to string.
    - WaDE2 *Beneficial Use* = **Use_Type** input.
    - WaDE2 *CommunityWaterSupplySystem* field = **Civil_Township** input.
    - WaDE2 *ReportYearCV* field = **Use_Year** input.
    - WaDE2 *TimeframeStart* field = **Use_Year** + "01/01".
    - WaDE2 *TimeframeEnd* field = **Use_Year** + "12/31".
- Restructure *WaterSourceTypeCV* to use WaDE2 appropriate terms.
- Create WaDE2 field *WaterSourceNativeID* field using created *WaterSourceTypeCV* field, which helps to create a unique ID.
- Replace "" or NaN values in *Beneficial Use* with "Unspecified".
- Create WaDE2 field *VariableSpecificCV* by concatenating the words "Withdrawal", the word "Annual", **Use_Type**, and WaDE2 formated **Source**.  Creates unique field to help filter specific timeseries amount type(s).
- Issue of multiple permits per site.  Will aggregate all time series amounts in a  site into a single value.  Groupby *SiteNativeID*, *VariableSpecificCV*, *TimeframeStart*, & *TimeframeEnd*, and sum the **Reported_AcFt** input  per dataset per unique combo.
- Format WaDE2 *TimeframeStart* & *TimeframeEnd* fields to YYYY-MM_DD format.
- Ensure that *Longitude*, *Longitude*, *Amount*,  & *ReportYearCV* are using numeric format.
- Review for errors in timeseries ouput dataframe.
- Export output dataframe as new csv file, *P_ndSSMaster.csv*.



***
### 1) Code File: 1_NDss_Methods.py
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
NDss_M1 | Surface Ground Storage | Unspecified



***
### 2) Code File: 2_NDss_Variables.py
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
NDss_V5 | 1 | Annual | MG | Withdrawal | Withdrawal_Annual_Commercial_Groundwater



***
### 3) Code File: 3_NDss_Organizations.py
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
NDss_O1 | North Dakota Department of Water Resource | Chris Bader | https://www.swc.nd.gov/



***
### 4) Code File: 4_NDss_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_ndSSMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 WaterSources* specific columns.
- Assign state agency info to columns.  See *ND_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = "Unspecified".
    - *WaterSourceNativeID* = see *0_PreProcessNDSiteSpecificData.ipynb* for specifics on generation.
    - *WaterSourceTypeCV* = **Source**, see *0_PreProcessNDSiteSpecificData.ipynb* for specifics on generation.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE2 specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
NDss_WS3 | Fresh | Unspecified | WaDEND_WS3 | Groundwater

Any data fields that are missing required values and dropped from the WaDE2-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_NDss_Sites.py
Purpose: generate a list of sites specific to the site specific time series water data.

#### Inputs:
- P_ndSSMaster.csv
- P_njSSGeometry.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Site* specific columns.
- Assign state agency info to columns.  See *ND_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from watersource.csv input file. See code for specific implementation of extraction.
    - *CoordinateMethodCV* = "Unspecified".
    - *County* = **County**.
    - *Latitude* = **Lattitude**.
    - *Longitude* = **Longitude**.
    - *PODorPOUSite* = "POD" for Point of Diversion.
    - *SiteName* = "Unspecified".
    - *SiteNativeID* = **POD**, see *0_PreProcessNDSiteSpecificData.ipynb* for specifics on generation.
    - *SiteTypeCV* = Unspecified".
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE2 specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID | SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
NDss_S1 | Unspecified | 47.7717479999999 | -104.040925 | Unspecified | 02305925DB | Unspecified

Any data fields that are missing required values and dropped from the WaDE2-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_NDss_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific timeseries water data to import into WaDE2 2.0.

#### Inputs:
- P_ndSSMaster.csv
- variables.csv
- watersources.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE2 Water Site Specific Amounts* data columns.
- Assign state agency data info to columns.  See *ND_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **Reported_AcFt**, converted from AcFT to MG.  See *0_PreProcessNDSiteSpecificData.ipynb* for specifics on generation. 
    - *BeneficialUseCategory* =  **Use_Type**.
    - *CommunityWaterSupplySystem* = **Civil_Township**.
    - *ReportYearCV* = **Use_Year**.
    - *TimeframeStart* = see *0_PreProcessNDSiteSpecificData.ipynb* for specifics on generation.
    - *TimeframeEnd* = see *0_PreProcessNDSiteSpecificData.ipynb* for specifics on generation.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
NDss_M1 | NDss_O1 | NDss_S1 | NJss_V13 | NJss_WS2 | 0 | Irrigation | 1976 | 01/01/1976 | 12/31/1976

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
### 7) Code File: 7_NDss_PODSiteToPOUSiteRelationships.py
Not applicable for the current data.  Missing place of use (POU) data and connections with point of diversions.



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [North Dakota Department of Water Resources (NDDWR)](https://www.swc.nd.gov/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

NDDWR Staff
- Chris Bader <cbader@nd.gov>
