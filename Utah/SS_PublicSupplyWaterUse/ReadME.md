# UT Site Specific Public Supply Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting site specific time series water data made available by the [Utah Division of Water Rights (UDWRi)](https://waterrights.utah.gov/) and the [Utah Division of Water Resources (UDWRe)](https://water.utah.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for aggregated water budget...
- **Water Use Data Portal**, also known as M&I data, and broken up into **System** and **Source** data.  Obtained from the UDWRi website at:  https://waterrights.utah.gov/asp_apps/waterUseData/setFilters.asp
- **Utah Culinary Water Suppliers**, which was used to tie in UDWRi data to location data.  Location information used for WaDE 2.0 purposes reflect the centroid of the water use areas (polygons).  Data was obtained from the Utah Division of Water Resources (UDWRe) website at: https://dwre-utahdnr.opendata.arcgis.com/datasets/utahDNR::culinarywaterserviceareas/explore?location=39.762819%2C-111.525980%2C7.91

Please note that the UDWRe has this webpage for Municipal and Industrial Water Use Data.  The page has helpful notes at the bottom that explain the context of the data.  We didn’t use this data because the Division of Water Rights data source above compiles all the years data together which is easier for WaDE use.
https://dwre-utahdnr.opendata.arcgis.com/pages/municipal-and-industrial-data

Adam Clark summarized:
>The Utah Culinary Water Service Areas spatial database is a combination of work and collaboration between the Division of Water Resources (UDWRe) and the Division of Water Rights (UDWRi) within the Department of Natural Resources, and the Division of Drinking Water (UDDW) within the Department of Environmental Quality. Water Resources is the data steward/creator, but receives input from the other divisions on systems.  Water Rights and Drinking Water both maintain separate non-spatial databases of water systems.  Water Rights is mostly focused on water usage and sources, while Drinking Water is more focused on compliance and water quality.*  While all three divisions share attributes in some ways, they differ in others.  If you were to join their own databases, you would find that the number of systems differs between all three.  The Utah Culinary Water Service Areas spatial database is the Division of Water Resources’ master database that includes all systems, past and present.  It also includes large and small systems, non-public systems, and self-supplied industry.  You will find three columns of system IDs, because all three divisions use different ID systems for tracking/updating.  You can think of the spatial database as a bridge or hybrid between the other two.*  Feel free to use Water Rights' query service to get more information on systems.  Just realize that it will not have information on all of the systems included in the spatial database.  Water Rights uses our feature service in their website to show boundaries for systems, but I guarantee that many of the systems in the service are not used.

![](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Utah/SS_PublicSupplyWaterUse/Utah_data_flow.png)

**System** and **Source** data files were further split to highlight Monthly versus Annual water use for **Source** data, and per individual beneficial use versus a single total use for **System** data.   Unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - UDWRi_SourceData_Monthly_input.csv
 - UDWRi_SourceData_Annual_no0Null_input.csv
 - UDWRi_SystemData_PerUse_input.csv
 - UDWRi_SystemData_Total_no0Null_input
 - UDWRe_CulinaryWaterServiceAreas_input.csv

 Some records were removed under advisement from the UDWRi.  These records either had misssing, NULL, or unverifiable records.  For those removed records, see the following files...
  - removed records.xlsx

 ## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Utah Site Specific Public Supply Data: https://drive.google.com/drive/folders/1RMxFNywr3nWWzx9fVlBIfdL3-aGtTUeW


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share UDWRi's site specific time series water data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *UT_SS_PublicSupplyWaterUse Schema Mapping to WaDE.xlsx*.  Several executable code files were used to extract the state agencies site specific time series data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/).  Those code files are as follows...

- 0_PreProcessUTSSPublicSupplyWaterUseData.ipynb
- 1_UTssps_Methods.py
- 2_UTssps_Variables.py
- 3_UTssps_Organizations.py
- 4_UTssps_WaterSources.py
- 5_UTssps_Sites.py
- 6_UTssps_SiteSpecificAmounts_fact.py
- 7_UTssps_PODSiteToPOUSiteRelationships.py


***
### 0) Code File: 0_PreProcessUTSSPublicSupplyWaterUseData.ipynb
Purpose: Pre-process the state agency input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - UDWRi_SourceData_Monthly_input.csv
 - UDWRi_SourceData_Annual_no0Null_input.csv
 - UDWRi_SystemData_PerUse_input.csv
 - UDWRi_SystemData_Total_no0Null_input
 - CulinaryWaterServiceAreas.shp

#### Outputs:
 - P_MasterUTSiteSpecific.csv
 - P_utSSGeometry.csv

#### Operation and Steps:
- For UDWRi System per individual beneficial use data...
    - Read the input file and generate temporary input dataframe.  We are only interested in records that have a "Active" **System Status** value.
    - Create list of unique beneficial uses.  These correspond to use amount columns within the table, which are **Domestic**, **Commercial**, **Industrial**, & **Institutional**.
    - WaDE *VariableCV* field = "Delivered Water Use".
    - WaDE *VariableSpecificCV* field = "Delivered Water Use_Annual_" + entry of the unique beneficial use input.
    - WaDE *Amount* field = amount data out per unique beneficial use input.
    - WADE *BeneficialUse* field = values from unique beneficial use list.
    - WaDE *PopulationServed* field = **Domestic Connections** input.
    - WaDE *ReportYearCV* field = **History Year** input.
    - WaDE *TimeframeStart* = '01/01/' + **History Year** input, for annual data.
    - WaDE *TimeframeEnd* = '12/31/' + **History Year** input, for annual data.
    - WADE *WaterSourceTypeCV* field = Unspecified.
    - Note down common linking element between records and a record's site, known as *linkKey*.  Use **System ID** input.
- For UDWRi System total use data...
    - Similar elements as those noted above for the UDWRi System per individual beneficial use data.  With the following exceptions...
    - WaDE *VariableSpecificCV* field = "Delivered Water Use_Annual_DCII"
    - WaDE *Amount* field = **Total Use** input.
    - WaDE *BeneficialUse* field = "DCII".
 - Concatenate the two System dataframes together into single long dataframe.
 - Left Join UDWRe Culinary Service Area Data data to the combined System dataframe to extract site information.  Join on unique *linkKey* element.  Information of interest include...
    - *linkKey* element = **WRID** input, which should correspond to the *linkkey* used for the System data.
    - WaDE "CoordinateMethodCV" field = "Centroid of Area"
    - WaDE "County" field **COUNTY** input.
    - WaDE "Latitude" field = **Latitude** input, taken from the centroid of the area.
    - WaDE "Longitude" field = **Longitude** input, taken from the centroid of the area.
    - WaDE "PODorPOUSite" field = "POU", for Place of Use.
    - WaDE "SiteName" field = **WRENAME** input.
    - WaDE "SiteNativeID" field = "POU" + **WRID** input.
    - WaDE "SiteTypeCV" field = "Unspecified"
- For UDWRi Source per month data...
    - Read the input file and generate temporary input dataframe.  We are only interested in records that have a "Active" **Source Status** value.
    - Create list of unique variable type entries.  These correspond to type of timeseries amount data within the **Diversion Type** input.  Those values are 'Withdrawal', 'Transfer In', 'Transfer Out', 'Delivery', and 'Return'.
    - Create list of unique beneficial uses.  These correspond to the beneficial use within the **Use Type** field.  Those values are 'Industrial', 'Irrigation', 'Domestic', 'Commercial', 'Geothermal', 'Agricultural', 'Mining', 'Power (Fossil-Fuel)', 'Power (Geothermal)', 'Power (Hydro-Elec)', 'Sewage Treatment', and 'Water Supplier'.
    - Create list of unique abbreviate months.  These correspond to the columns that contain the monthly amount data.  Those inputs are **Jan**, **Feb**, **Mar**, **Apr**, **May**, **Jun**, **Jul**, **Aug**, **Sep**, **Oct**, **Nov**, and **Dec**.
    - Create list of both start and end dates per month.
    - Using a series of for loops, extract the following information...
        - WaDE *VariableCV* field = unique variable type entry noted from **Diversion Type** input.
        - WaDE *VariableSpecificCV* field = "Delivered Water Use_Annual_" + entry of the unique beneficial use input.
        - WaDE *PopulationServed* field = "".
        - WADE *BeneficialUse* field = values from unique beneficial use list.
        - WaDE *ReportYearCV* field = **Year** input.
        - WaDE *CoordinateMethodCV* field = **Representation Node** input.
        - WaDE *Latitude* field = **Lat NAD83** input.
        - WaDE *Longitude* field = **Lon NAD83** input.
        - WaDE *PODorPOUSite'] = "POD"
        - WaDE *SiteName* field = **Source Name** input.
        - WaDE *SiteNativeID* field = **Source ID** input.
        - WaDE *SiteTypeCV* field = **Source Type** input.
        - WaDE *Amount* field = amount data out per unique beneficial use input.
        - WaDE *TimeframeStart* = Unique start data for that month taken from list + **Year** input, for monthly data.
        - WaDE *TimeframeEnd* = Unique end data for that month taken from list + **Year** input, for monthly data.
        - WADE *WaterSourceTypeCV* field = **Source Type** input.
        - Note down common linking element between records and a record's site, known as *linkKey*.  Use **System ID** input.
- For UDWRi Source annual data...
    - Similar elements as those noted above for the UDWRi Source per month data.  With the following exceptions...
    - WADE *BeneficialUse* field = "Total"
    - WaDE *Amount* field = **Total** input, for annual data.
    - WaDE *TimeframeStart* = '01/01/' + **Year** input, for annual data.
    - WaDE *TimeframeEnd* = '12/31/' + **Year** input, for annual data.
 - Concatenate the two Source dataframes together into single long dataframe.
 - Concatenate the two larger System & Source dataframes together into single dataframe.
 - Check and clean data types, notably *WaterSourceType*, *TimeFrameStart* & *TimeFrameEnd*, *Latitude* & *Longitude*, and *Amount* values.
 - Generate WaDE specific *WaterSourceNativeID* using inputs for unique water source type inputs.
 - Create shapefile specific dataframe.  Extract shapefile **geometry** input information CulinaryWaterServiceAreas shapefiles. Note down site native ID as **WRID** input, which corresponds to the above UDWRi data.
 - Export output dataframe as new csv file, *P_MasterUTSiteSpecific.csv* & *P_utSSGeometry.csv*.



***
### 1) Code File: 1_UTssps_Methods.py
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
UTssps_M1 | Surface Water & Groundwater | Estimated



***
### 2) Code File: 2_UTssps_Variables.py
Purpose: generate legend of granular variables specific to each state.

#### Inputs:
- None

#### Outputs:
- variables.csv
- variables_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign state agency info info to the *WaDE WaterSources* specific columns.  See *UT_SS_PublicSupplyWaterUse Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *VariableCV* = *in_VariableCV*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
    - *VariableSpecificCV* = *in_VariableSpecificCV*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV | VariableCV | VariableSpecificCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------
UTssps_V1 | 1 | Year | G | Delivered Water Use | Delivered Water Use_Annual_Commercial_Unspecified



***
### 3) Code File: 3_UTssps_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign state agency data info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
UTssps_O1 | Utah Division of Water Rights | James Greer | https://waterrights.utah.gov/



***
### 4) Code File: 4_UTssps_WaterSources.py
Purpose: generate a list of water sources specific to the site specific time series water data.

#### Inputs:
- P_MasterUTSiteSpecific.csv

#### Outputs:
- waterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency info info to the *WaDE WaterSources* specific columns.  See *UT_SS_PublicSupplyWaterUse Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceNativeID* = *in_WaterSourceNativeID*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
    - *WaterSourceTypeCV* = *in_WaterSourceTypeCV*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
UTssps_WS1 | Fresh | Unspecified | WaDEUT_WS1 | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV



***
### 5) Code File: 5_UTssps_Sites.py
Purpose: generate a list of polygon areas associated with the state agency specific site on aggregated water budget data.

#### Inputs:
- P_MasterUTSiteSpecific.csv

#### Outputs:
- sites.csv
- waterSources.csv
- sites_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign state agency data info to the *WaDE Site* specific columns.  See *UT_SS_PublicSupplyWaterUse Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - *CoordinateMethodCV* = *in_CoordinateMethodCV*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
    - *County* = *in_County*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
    - *Latitude* = *in_Latitude*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
    - *Longitude* = *in_Longitude*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
    - *PODorPOUSite* = *in_PODorPOUSite*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
    - *SiteName* = *in_SiteName*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
    - *SiteNativeID* == *in_SiteNativeID*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
    - *SiteTypeCV* = *in_SiteTypeCV*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, group by WaDE specific *WaterSourceUUID*, *PODorPOUSite*, *SiteName*, *SiteNativeID*, *SiteTypeCV*, *Latitude*, and *Longitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
UTssps_S1 | UTss_WS1| Representation Node | 37.30907717 | -113.4294115 | Oak Grove Spring (WS001)

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName



***
### 6) Code File: 6_UTssps_SiteSpecificAmounts_fact.py
Purpose: generate master sheet of state agency site specific time series water data to import into WaDE 2.0.

#### Inputs:
- P_MasterUTSiteSpecific.csv
- variables.csv
- sites.csv

#### Outputs:
- sitespecificamounts.csv
- sitespecificamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Site Specific Public Supply Amounts* data columns.
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *UT_SS_PublicSupplyWaterUse Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = *in_Amount*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specific on generation.
    - *CustomerTypeCV* = "Public"
    - *PopulationServed* = *in_PopulationServed*, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specific on generation.
    - *ReportYearCV* = *in_ReportYearCV, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specific on generation.
    - *TimeframeStart* = *in_TimeframeStart, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specific on generation.
    - *TimeframeEnd* = *in_TimeframeEnd, see *0_PreProcessUTSSPublicSupplyWaterUseData.ipynb* for specific on generation.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID  | Amount | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ 
UTssps_M1 | UTssps_O1 | UTssps_S1 | UTssps_V1 | 89.07131598 | 1979

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
### 7) Code File: 7_UTssps_PODSiteToPOUSiteRelationships.ipynb
Purpose: generate linking element between POD and POU sites that share the same water right.
Note: podsitetopousiterelationships.csv output only needed if both POD and POU data is present, otherwise produces empty file.

#### Inputs:
- P_MasterUTSiteSpecific.csv
- sites.csv
- sitespecificamounts.csv

#### Outputs:
- podsitetopousiterelationships.csv

#### Operation and Steps:
- Read the P_MasterUTSiteSpecific.csv, sites.csv & sitespecificamounts.csv input files.
- Extract *in_SiteNativeID* & *linkKey* from P_MasterUTSiteSpecific.csv.
- Create a POU site specific dataframe by extracting *SiteUUID*, *SiteNativeID* & *PODorPOUSite*, where *PODorPOUSite* = "POU".
- Create a POD site specific dataframe by extracting *SiteUUID*, *SiteNativeID* & *PODorPOUSite*, where *PODorPOUSite* = "POD".
- Extract *SiteUUID*, *TimeframeStart*, & *TimeframeEnd* from sitespecificamounts.csv.
- Left-join POU sites with extracted sitespecificamounts via *SiteUUID*, and left-join P_MasterUTSiteSpecific via *SiteNativeID*.
- Left-join POD sites with extracted sitespecificamounts via *SiteUUID*, and left-join P_MasterUTSiteSpecific via *SiteNativeID*.
- Left-join POD site dataframe with POU site dataframe via *linkKey* field.
- Check and remove duplicates.  Remove NaN rows.
- If table is not empty, export output dataframe *podsitetopousiterelationships.csv*.



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Utah Division of Water Rights (UDWRi)](https://waterrights.utah.gov/) and the [Utah Division of Water Resources (UDWRe)](https://water.utah.gov/)

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

UDWRe Staff
- Jessie Pierson <jpierson@utah.gov>
- Tom Moore <tmoore@utah.gov>
- Aaron Austin <aaronaustin@utah.gov>
- Craig Miller <craigmiller@utah.gov>
- Leila Ahmadi <lahmadi@utah.gov>

UDWRi Staff
- Jim Reese <jreese@utah.gov>
