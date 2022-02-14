# CDWR Aggregated Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting aggregated water budget data made available by the [California Department of Water Resources (CDWR)](https://data.ca.gov/dataset/water-plan-water-balance-data), for inclusion into the Water Data Exchange (WaDE) project.   WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Data Utilized
The following data was used for aggregated water budget...

- [**Water Plan Water Balance Data**](https://data.cnra.ca.gov/dataset/water-plan-water-balance-data) aggregrated time series water budget files csv for HR, PA, and DAU regions.  Data used was for the years 2002-2016.  In total there are 45 separate csv files (15 HR, 15 PA, & 15 DAU).
- **Water_Plan_Planning_Areas-shp** files were used to extract geometry, create shape files, and were obtained from the [DWR Atlas](https://atlas-dwr.opendata.arcgis.com/datasets/a911dd793cae48f1a3662e08f4811382_0?geometry=-152.647%2C31.071%2C-85.894%2C43.276).
- **Hydrologic_Regions-shp** files were used to extract geometry, create shape files, and were obtained from the [DWR Atlas](https://atlas-dwr.opendata.arcgis.com/datasets/2a572a181e094020bdaeb5203162de15_0).
- **DAUCO-shp** files were used to extract geometry, create shape files, and were provided with previous WaDE 1.0 correspondence in the past between the CDWR and the WSWC.  DAUCO is more granular than the actual county shape (see below Figure 1).
   
![](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/California/AggregatedAmounts/RawInputData/Images/DAUCOvsCounty.PNG)
**Figure 1:** Detailed Analysis Units by County (DAUCO) by CA vs County

From the above mentioned provided data links, the following input files were used as input to the Python codes that prepare WaDE 2.0 input files.  Input files used are as follows...
 - CA-DWR-WaterBalance-Level2-DP-1000-2002-HR to ...2016-HR csv files (see HR_input).
 - CA-DWR-WaterBalance-Level2-DP-1000-2002-PA to ...2016-PA csv files (see PA_input).
 - CA-DWR-WaterBalance-Level2-DP-1000-2002-DAUCO to ...2016 csv files (see DAU_input).
 - Hydrologic_Regions shapefile.
 - Water_Plan_Planning_Areas shapefile.
 - DAUCO shapefile.

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share CDWR's aggregated water budget data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *CA_Aggregated Schema Mapping to WaDE_QAR.xlsx*.  Six executable code files were used to extract the CDWR's aggregated water budget data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining five code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file *(AggregatedAmounts_facts)* is dependent on the previous files.  Those six code files are as follows...

- 0_CAAggregatedDataPreprocess.ipynb
- 1_CAag_Methods.py
- 2_CAag_Variables.py
- 3_CAag_Organizations.py
- 4_CAag_WaterSources.py
- 5_CAag_ReportingUnits.py
- 6_CAag_AggregatedAmounts_facts.py


***
### 0) Code File: 0_CAAggregatedDataPreprocess.ipynb
Purpose: Pre-process the Arizona input data files into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - CA-DWR-WaterBalance-Level2-DP-1000-2002-HR to ...2016-HR csv files (see HR_input).
 - CA-DWR-WaterBalance-Level2-DP-1000-2002-PA to ...2016-PA csv files (see PA_input).
 - CA-DWR-WaterBalance-Level2-DP-1000-2002-DAUCO to ...2016 csv files (see DAU_input).
 - Hydrologic_Regions shapefile.
 - Water_Plan_Planning_Areas shapefile.
 - DAUCO shapefile.


#### Outputs:
 - P_caAggMaster.csv
 - P_caGeometry.csv

#### Operation and Steps:
- Read in HR_input csv files, concatenate into single long temporary HR dataframe.
- Read in PA_input csv files, concatenate into single long temporary PA dataframe.
- Read in DAU_input csv files, concatenate into single long temporary DAU dataframe.
- For temporary HR dataframe only...
    - Retreieve WaDE specific *ReportingUnitNativeID* for HR shapes from DAU_input **HR_CODE** field (not originaly provdied in HR_input but found within DAU_input).
- For temporary HR, PA, and DAU dataframes...
    - Create WaDE specific *VariableSpecificCV* field by combining **CategoryC** + "_Annual_" + **CategoryA** + "_Surface Ground Water".
    - Create WaDE specific *TimeframeStart** from **Year** input + -01-01".
    - Create WaDE specific *TimeframeEnd** from **Year** input + "-12-31".
- Concatenate temporary HR, PA, and DAU dataframes together into single long output dataframe.
- Ensure date data is in YYYY-MM-DD format.
- Generated WKT values from Hydrologic_Regions, Water_Plan_Planning_Areas, & DAUCO shapefiles.
- Inspect dataframes for errors.
- Export output dataframe as new csv files, *P_caAggMaster.csv* & *P_caGeometry.csv*.


***
### 1) Code File: - 1_CAag_Methods.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- methods.csv
- methods_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign state agency data  info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
CAag_M1 | Surface Ground Reuse Recycled Water | Computed


***
### 2) Code File: 2_CAag_Variables.py
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
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV | VariableCV | VariableSpecificCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------
CAag_V1 | 1 | Annual | AFY | Applied Water Use | Applied Water Use_Annual_Agriculture_Surface Ground Water


***
### 3) Code File: 3_CAag_Organizations.py
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
OrganizationUUID | OrganizationName  | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
CAagO1 | California Department of Water Resources | Jennifer Stricklin | https://water.ca.gov/


***
### 4) Code File: 4_CAag_WaterSources.py
Purpose: generate a list of water sources specific to an aggregated water budget data area.

#### Inputs:
- P_caAggMaster.csv

#### Outputs:
- WaterSources.csv
- watersources_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign state agency data info to the *WaDE WaterSources* specific columns.  See *CA_Aggregated Schema Mapping to WaDE_QAR.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceTypeCV* = Groundwater, Surface Water.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceTypeCV* field.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
CAag_WS1 | Fresh | Unspecified | WaDECA_WS1 | Surface and Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


***
### 5) Code File: 5_CAag_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency specific area on aggregated water budget data.

#### Inputs:
- P_caAggMaster.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *CA_Aggregated Schema Mapping to WaDE_QAR.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = **HR**, **PA**, & **DAU_NAME** input fields respectively for each area type.
    - *ReportingUnitNativeID* = **HR_CODE**, **PA**, & **DAU** respectively for each area type.
    - *ReportingUnitTypeCV* = "Hydrologic Region", "Planning Area", & "Detailed Analysis Units by County" respectively for each area type.
    - *Geometry* = WKT created **Geometry**, see *0_CAAggregatedDataPreprocess.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | ReportingUnitName | ReportingUnitTypeCV 
---------- | ---------- | ------------ 
CAag_RU1 | 101 | Planning Area

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV


***
### 6) Code File: 6_CAag_AggregatedAmounts_facts.py
Purpose: generate master sheet of state agency specified area aggregated water budget information to import into WaDE 2.0.

#### Inputs:
- P_caAggMaster.csv
- methods.csv
- variables.csv
- organizations.csv
- watersources.csv
- reportingunits.csv

#### Outputs:
- aggregatedamounts.csv
- aggregatedamounts_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *CA_Aggregated Schema Mapping to WaDE_QAR.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *ReportingUnitUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **KAcreFt** input field.
    - *BeneficialUseCategory* = **CategoryA** input field.
    - *ReportYearCV* = **Year** input field.
    - *TimeframeStart* = see *0_CAAggregatedDataPreprocess.ipynb* for specific implementation.
    - *TimeframeEnd* = see *0_CAAggregatedDataPreprocess.ipynb* for specific implementation.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | ReportingUnitUUID | VariableSpecificUUID | WaterSourceUUID | Amount | BeneficialUseCategory | ReportYearCV
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | -----------
CAag_M1 | CAag_O1 | CAag_RU1 | CAag_V1 | CAag_WS1 | 1175.6 | Agricultural | 2002

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- ReportingUnitUUID
- Amount


## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [California Department of Water Resources (CDWR)](https://data.ca.gov/dataset/water-plan-water-balance-data).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>
- Adel Abdallah <adelabdallah@wswc.utah.gov>

CDWR Staff
- Jennifer Stricklin <Jennifer.Stricklin@water.ca.gov>
- Gary Darling <Gary.Darling@water.ca.gov>

San Diego Supercomputer Center
- John Helly <hellyj@ucsd.edu>