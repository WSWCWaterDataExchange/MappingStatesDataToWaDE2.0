# CSWRCB Site Specific Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [California State Water Resources Control Board (CSWRCB)](https://www.waterboards.ca.gov/waterrights/water_issues/programs/ewrims/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Data Utilized
The following data was used for aggregated water budget...

- [Delivered Water - Public System](https://data.ca.gov/dataset/drinking-water-public-water-system-annually-reported-water-production-and-delivery-information) time series data 2013-2016.
- [Public Water system Facilities](https://data.ca.gov/dataset/drinking-water-public-water-system-information) data.
- [California Drinking Water System Area Boundaries](https://gis.data.ca.gov/datasets/fbba842bf134497c9d611ad506ec48cc_0/data?geometry=-160.357%2C31.280%2C-76.729%2C43.454) data.


Unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - deliveredPWS_2013_2016.csv
 - PWS Facility Information.csv
 - CADWS_AreaBoundaries.csv

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CSWRCB's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *CA_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx*.  Six executable code files were used to extract the state agency's site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(SiteSpecificAmounts)* is dependent on the previous files.  Those six code files are as follows...

- 0_PreProcessCASiteSpecificData.ipynb
- 1_CAss_Methods.py
- 2_CAss_Variables.py
- 3_CAss_Organizations.py
- 4_CAss_WaterSources.py
- 5_CAss_Sites.py
- 6_CAss_SiteSpecificAmounts_fact.py
- 7_CAss_PODSiteToPOUSiteRelationships.py



***
### 0) Code File: 0_PreProcessCASiteSpecificData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - deliveredPWS_2013_2016.csv
 - PWS Facility Information.csv
 - CADWS_AreaBoundaries.csv

#### Outputs:
 - P_caSSMaster.csv

#### Operation and Steps:
- Read in input csv data, place into temporary dataframes.
- Left join dataframes together.  Join *deliveredPWS_2013_2016.csv* -to- *PWS Facility Information.csv* via **PWSID** and **Water System No** respectively, and *CADWS_AreaBoundaries.csv* with **SABL_PWSID**.
- Trim down joined dataframe to columns of interest.
- Format column names to remove formatting issues.
- Format water amount column to remove string values, format to numeric.
- Format population value column to integer value.
- Generate WaDE specific *TimeframeStart* & *TimeframeEnd* fields. Assume start date is 01/ + **Month** & **Year**,  and end date is 31/ + + **Month** & **Year**.
- Review for errors.
- Export output dataframe as new csv file, *P_caSSMaster.csv*.



***
### 1) Code File: 1_CAss_Methods.py
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
CSWRCB_Public Drinking Water | Surface Ground Storage | Modeled



***
### 2) Code File: 2_CAss_Variables.py
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
CSWRCB_Site Specific | 1 | Cumulative | G



***
### 3) Code File: 3_CAss_Organizations.py
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
CSWRCB | California State Water Resources Control Board | Greg Gearheart | https://www.waterboards.ca.gov/waterrights/water_issues/programs/ewrims/



***
### 4) Code File: 4_CAss_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_caSSMaster.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency info to columns.  See *CA_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = **Primary Water Source Type**.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName*, *WaterSourceNativeID* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
CAss_WS1 | Fresh | Unspecified | Unspecified | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_CAss_Sites.py
Purpose: generate a list of polygon areas associated with the state agency specific site on aggregated water budget data.

#### Inputs:
- P_caSSMaster.csv

#### Outputs:
- sites.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency info to columns.  See *CA_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *County* = **COUNTY**.
    - *Latitude* = **Lat**.
    - *Longitude* = **Long**.
    - *SiteName* = **Water System Name**.
    - *SiteNativeID* = **SABL_PWSID**.
    - *SiteTypeCV* = **BOUNDARY_T**.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | CoordinateMethodCV | Latitude | Longitude | SiteName | SiteNativeID |SiteTypeCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
CAss_S1 | Centroid of Area | 37.73436363 | -122.0273033 | NORRIS CANYON PROPERTY OWNERS ASSN. | CA0103040 | Water Service Area

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_CAss_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific time series water data to import into WaDE 2.0.

#### Inputs:
- P_caSSMaster.csv
- methods.csv
- variables.csv
- organizations.csv
- watersources.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Site Specific Amounts* data columns.
- Assign state agency data info to columns.  See *CA_SiteSpecificAmounts Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = *in_Amount*, see *0_PreProcessCASiteSpecificData.ipynb* for specific on generation.
    - *CommunityWaterSupplySystem* = **Water System Name**.
    - *PopulationServed* = **Population Of Service Area**.
    - *ReportYearCV* = **Year**.
    - *TimeframeStart* = *in_TimeframeStart*, see *0_PreProcessCASiteSpecificData.ipynb* for specific on generation.
    - *TimeframeEnd* = *in_TimeframeEnd*, see *0_PreProcessCASiteSpecificData.ipynb* for specific on generation.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | TimeframeStart | TimeframeEnd 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
CSWRCB_Public Drinking Water | CSWRCB | CAss_S2 | CSWRCB_Site Specific | CAss_WS1 | 105995 | Unspecified | 2015 | 1/1/2015 | 12/31/2015 

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
### 7) Code File: 7_CAss_PODSiteToPOUSiteRelationships.py
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
- Left-merge site.csv info to the sitespecificamounts dataframe via *SiteUUID* field.
- Split into two new temporary dataframes: one POD centric, the other POU centric.
- For the temporary POD dataframe...
    - Create *PODorPOUSite* field = POD.
- For the temporary POU dataframe
    - Create *PODorPOUSite* field = POU.
- Merge POD & POU dataframes into single output dataframe, only using unique rows.
- Find *SiteUUID* baesed on *PODorPOUSite* field.
- Perform error check on waterallocations dataframe (check for NaN values)
- If waterallocations is not empty, export output dataframe *podsitetopousiterelationships.csv*.



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [California State Water Resources Control Board (CSWRCB)](https://www.waterboards.ca.gov/waterrights/water_issues/programs/ewrims/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

CSWRCB Staff
- Greg Gearheart <Greg.Gearheart@waterboards.ca.gov>