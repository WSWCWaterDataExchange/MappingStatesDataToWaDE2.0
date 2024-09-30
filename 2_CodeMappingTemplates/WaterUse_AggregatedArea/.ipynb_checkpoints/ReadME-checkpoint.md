# "XX" Aggregated Water Use Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting aggregated water use data made available by the ["XX"](insert link to org here), for inclusion into the Water Data Exchange (WaDE) project.   WaDE enables states to share data with each other and the public in a more streamlined and consistent way.  WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
***input1** | asdf | [link](insert link here) |  [link](insert link here) or Not Provided


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- "XX" Aggregated Water Use Time Series Data: [link](insert link to google drive here)

## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share aggregated water use data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *XXwuag_Aggregated Water Use Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_XXwuag_PreProcessAggregatedWaterUseData**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_XXwuag_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, reportingunits.csv, aggregatedamounts.csv
- **3_XXwuag_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_XXwuag_PreProcessAggregatedWaterUseData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
 - asdf

#### Outputs:
 - Pwuag_xxMain.zip
 - P_Geometry.zip

#### Operation and Steps:
- "fill in description of what to do for pre-processing steps here"



***
## Code File: 2_XXwuag_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (methods.csv, variables.csv, organizations.csv, watersources.csv, reportingunits.csv, aggregatedamounts.csv).

#### Inputs:
- Pwuag_xxMain.zip
- P_Geometry.zip

#### Outputs:
- methods.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- variables.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- organizations.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- watersources.csv
- reportingunits.csv
- aggregatedamounts.csv


## 1) Method Information
Purpose: generate legend of granular methods used on data collection.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign state info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
- "copy paste markdown table values here"

## 2) Variables Information
Purpose: generate legend of granular variables specific to each state.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign state info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
- "copy paste markdown table values here"


## 3) Organization  Information
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign state info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
- "copy paste markdown table values here"


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency info to the *WaDE WaterSources* specific columns.  See *XXwuag_Aggregated Water Use Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceUUID* = ""
    - *WaterQualityIndicatorCV* = ""
    - *WaterSourceName* = ""
    - *WaterSourceNativeID* = ""
    - *WaterSourceTypeCV* = ""
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
- "copy paste markdown table values here"

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


### 5) Reporting Unit Area Information
Purpose: generate a list of polygon areas associated with the state agency specific area on aggregated water use data.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *XXwuag_Aggregated Water Use Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitUUID* = ""
    - *EPSGCodeCV* = 4326
    - *R"eportingUnitName* = ""
    - *ReportingUnitNativeID* = ""
    - *ReportingUnitProductVersion* = ""
    - *ReportingUnitTypeCV* = ""
    - *ReportingUnitUpdateDate* = ""
    - *StateCV* = ""
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Perform error check on output dataframe.
- Export output dataframe *reportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
- "copy paste markdown table values here"

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV


### 6) Aggregated to Area Time Series Information
Purpose: generate master sheet of state agency specified area aggregated water budget information to import into WaDE 2.0.

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign state agency data info to the *WaDE Water Allocations* specific columns.  See *XXwuag_Aggregated Water Use Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *ReportingUnitUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationCropDutyAmount* = ""
    - *Amount* = ""
    - *BeneficialUseCategory* = ""
    - *CommunityWaterSupplySystem* = ""
    - *CropTypeCV* = ""
    - *CustomerTypeCV* = ""
    - *DataPublicationDate* = ""
    - *DataPublicationDOI* = ""
    - *InterbasinTransferFromID* = ""
    - *InterbasinTransferToID* = ""
    - *IrrigatedAcreage* = ""
    - *IrrigationMethodCV* = ""
    - *PopulationServed* = ""
    - *PowerGeneratedGWh* = ""
    - *PowerType* = ""
    - *PrimaryUseCategoryCV* = ""
    - *ReportYearCV* = ""
    - *SDWISIdentifierCV* = ""
    - *TimeframeEnd* = ""
    - *TimeframeStart* = ""
- Perform error check on output dataframe.
- Export output dataframe *aggregatedamounts.csv*.

#### Sample Output (WARNING: not all fields shown):
- "copy paste markdown table values here"

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *aggregatedamounts_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- ReportingUnitUUID
- Amount


***
## Source Data & WaDE Complied Data Assessment
The following info is from a data assessment evaluation of the completed data...

Dataset | Num of Source Entries (rows)
---------- | ---------- 
**"{name of data}"** | "fill value here"


Dataset  | Num of Identified Reporting Unit Areas | Num of Identified Time Series Records
**Compiled WaDE Data** | "fill value here" | "fill value here"


Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
"what was removed" | "count of entries removed" | "action taken (il.e., removed from sites.csv)"input


**Figure 1:** Distribution of Reporting Unit Area Type in reportingunits.csv
![](figures/ReportingUnitType.png)

**Figure 2:** Distribution of Primary Beneficial Uses within the aggregatedamounts.csv
![](figures/PrimaryUseCategory.png)

**Figure 3:** Distribution & Range of Amount within the aggregatedamounts.csv
![](figures/Amount.png)

**Figure 4:** Map of Identified Points within the sites.csv
![](figures/AggAreaMap.png)


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the ["XX"](insert link to org here).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>

"XX" Staff
- asdf