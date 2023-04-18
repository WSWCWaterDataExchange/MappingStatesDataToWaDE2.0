![image](https://user-images.githubusercontent.com/3268971/127560635-258cc359-d698-4f91-bf8c-a30e214d85b4.png)

# CDWR Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Colorado Division of Water Resources (CDWR)](https://dwr.colorado.gov/about-us/contact-us/denver-office), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 

## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**DWR Water Right - Net Amounts** | data files for surface and groundwater. | [link](https://data.colorado.gov/Water/DWR-Water-Right-Net-Amounts/acsg-f33s/data) | [link](https://data.colorado.gov/Water/DWR-Water-Right-Net-Amounts/acsg-f33s?category=Water&view_name=DWR-Water-Right-Net-Amounts)


One unique files was created to be used as input.  Input files used are as follows...
- DWR_Water_Right_-_Net_Amounts_input.csv.

## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Colorado Allocation Data: https://drive.google.com/drive/folders/1-4_iFyn5rrz6_paiUyZ8UXKSVRb0jkse?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NMOSE's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *NMwr_Allocation Schema Mapping to WaDE.xlsx* & *COwr_Allocation Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the NMOSE's water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_COwr_PreProcessAllocationData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_COwr_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv.
- **3_COwr_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
### 0) Code File: 1_COwr_PreProcessAllocationData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- DWR_Water_Right_-_Net_Amounts_input.csv

#### Outputs:
 - Pwr_coMain.zip

#### Operation and Steps:
- Read the input file and generate temporary input dataframe.
- Format date datatype values to WaDE 2.0 appropriate formats.
- Using provided index, translate provided beneficial uses abbreviations into full terms.
- Format water source type to match WaDE 2.0 appropriate formats, "Unspecified" if not provided.
- Format water source name to match WaDE 2.0 appropriate formats, "Unspecified" if not provided.
- Format GNIS ID to match WaDE 2.0 appropriate formats, "Unspecified" if not provided.
- Two separate fields were provided for allocation flow.  Use the following rules to determine appropriate value...
    - If **Decreed Units** is equal to "C" and **Net Absolute** does not equal to 0, then return **Net Absolute** as allocation flow.
    - If **Decreed Units** is equal to "C" and **Net Conditional** does not equal to 0, then return **Net Conditional** as allocation flow.
    - If neither is true, return a value of "0" for allocation flow.
- Two separate fields were provided for allocation volume.  Use the following rules to determine appropriate value...
    - If **Decreed Units** is equal to "A" and **Net Absolute** does not equal to 0, then return **Net Absolute** as allocation volume.
    - If **Decreed Units** is equal to "A" and **Net Conditional** does not equal to 0, then return **Net Conditional** as allocation volume.
    - If neither is true, return a value of "0" for allocation volume.
- Determine legal status depending on if either **Net Absolute** or **Net Conditional** were used.
- Combine **Admin No**, **Order No**, **Decreed Units**, & **WDID** into single string entry for a unique water right identifier.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *Pwr_coMain.zip*.



***
## Code File: 2_COwr_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv).

#### Inputs:
- Pwr_NMMain.zip

#### Outputs:
- methods.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- variables.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- organizations.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- watersources.csv
- sites.csv
- waterallocations.csv


## 1) Method Information
Purpose: generate legend of granular methods used on data collection.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign agency info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
COwr_M1 | Surface Ground Water | Water Withdrawals


## 2) Variables Information
Purpose: generate legend of granular variables specific to each state.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign agency info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
VariableSpecificUUID | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV
---------- | ---------- | ------------ | ------------
COwr_V1 | 1 | Average | CFS


## 3) Organization  Information
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign agency info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
COwr_O1 | Colorado Division of Water Rights | Doug Stenzel | https://dwr.colorado.gov


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency info to the *WaDE WaterSources* specific columns.  See *[CO_Allocation Schema Mapping_WaDEQA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Colorado/WaterAllocation/CO_Allocation%20Schema%20Mapping_WaDEQA.xlsx)* for specific details.  Items of note are as follows...
    - WaDE *WaterSourceName* = *input_WaterSourceName*, see *0_PreProcessColoradoAllocationData.ipynb* for specifics.
    - WaDE *WaterSourceNativeID* = **GNIS ID** input field.
    - WaDE *WaterSourceTypeCV* = *input_WaterSourceTypeCV*, see *0_PreProcessColoradoAllocationData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
COwr_WS1 | Unspecified | COAL CREEK | 188598 | Surface Water

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate file (e.g. *watersources_missing.xlsx*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


## 5) Site Information
Purpose: generate a list of sites information.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign agency info to the *WaDE Site* specific columns.  See *[CO_Allocation Schema Mapping_WaDEQA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Colorado/WaterAllocation/CO_Allocation%20Schema%20Mapping_WaDEQA.xlsx)* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - WaDE *CoordinateMethodCV* = **Location Accuracy** input field.
    - WaDE *County* = **County** input field.
    - WaDE *Latitude* = **Latitude** input field.
    - WaDE *Longitude* = **Longitude** input field.
    - WaDE *SiteName* = **Structure Name** input field, "Unspecified" if not given.
    - WaDE *SiteNativeID* = **WDID** input field, "Unspecified" if not given.
    - WaDE *SiteTypeCV* = **Structure Type** input field, "Unspecified" if not given.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
COwr_S1 | COwr_WS93 | Digitized | 40.402594 | -104.530193 | HOOVER DITCH

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate file (e.g. *sites_missing.xlsx*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


## 6) AllocationsAmounts Information
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign agency info to the *WaDE Water Allocations* specific columns.  See *[CO_Allocation Schema Mapping_WaDEQA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/Colorado/WaterAllocation/CO_Allocation%20Schema%20Mapping_WaDEQA.xlsx)* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - WaDE *AllocationFlow_CFS* = *in_AllocationFlow_CFS*, see *0_PreProcessColoradoAllocationData.ipynb* for specifics.
    - WaDE *AllocationNativeID* = *in_AllocationNativeID*, see *0_PreProcessColoradoAllocationData.ipynb* for specifics.
    - WaDE *AllocationLegalStatusCV* = *in_AllocationLegalStatusCV*, see *0_PreProcessColoradoAllocationData.ipynb* for specifics. 
    - WaDE *AllocationPriorityDate* = **Appropriation Date** input field.
    - WaDE *AllocationVolume_AF* = *in_AllocationVolume_AF*, see *0_PreProcessColoradoAllocationData.ipynb* for specifics.
    - WaDE *BeneficialUseCategory* = *in_WaDEBenUse*, see *0_PreProcessColoradoAllocationData.ipynb* for specifics. 
    - WaDE *WaterAllocationNativeURL* = **More Information** input field.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | OrganizationUUID | SiteUUID | VariableSpecificUUID  | AllocationFlow_CFS | AllocationLegalStatusCV | AllocationPriorityDate | AllocationVolume_AF | BeneficialUseCategory
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
COwr_M1 | COwr_O1 | COwr_S61925 | COwr_V1 | 0.0001 | Absolute | 1850-01-01 | 0 | Export from State

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate file (e.g. *waterallocations_missing.xlsx*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- SiteUUID
- AllocationPriorityDate
- BeneficialUseCategory
- AllocationAmount or AllocationMaximum
- DataPublicationDate


***
### 7) Code File: 7_COwr_PODSiteToPOUSiteRelationships.py
- Not used at this time.  Need Colorado Point-of-Diversion and Place-of-Use data to work with.


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Colorado Division of Water Resources (CDWR)](https://dwr.colorado.gov/about-us/contact-us/denver-office).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

CDWR Staff
- Brian Macpherson <brian.macpherson@state.co.us>

