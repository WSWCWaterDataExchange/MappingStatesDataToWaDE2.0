# Water Rights (Allocation amounts) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water allocations data made available by the [Washington State Department of Ecology (WSDE)](https://ecology.wa.gov/Water-Shorelines/Water-supply/Water-rights), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.

## Overview 
The water rights data were obtained from the Geographic Water Information System (GWIS) Data for the state of Washington at: https://fortress.wa.gov/ecy/gispublic/DataDownload/wr/GWIS_Data/

Data dictionary are available from: https://fortress.wa.gov/ecy/gispublic/DataDownload/wr/GWIS_Data/GWIS_Data_Dictionary/

Public website on water rights: https://ecology.wa.gov/Water-Shorelines/Water-supply/Water-rights 

A GWIS ArcSDE Geodatabase (GWIS_SDEexport.zip) was download from the Water Resources' GWIS database.
From the Geodatabase, the following files were exported into a csv file which form the inputs to the Python codes that prepare WaDE2 input files:

 - **Person_Plus_EXTRACT_FromWRTSnotGWIS.csv**
 - **D_Point_WR_Doc.csv**
 - **D_Point.csv**
 - **WR_Doc_POU1.csv**

A table for mapping of 'purpose of use type' codes to beneficial use categories was obtained from WSDE through email. 

The Python scripts described here are [Jupyter Notebooks](https://jupyter.org/) to prepare the water allocations data in csv format that can be ingested into the WaDE2 DB.

## Summary
This document summarizes the process to prepare and share WSDE’s water rights data for inclusion into the WSWC’s Water Data Exchange (WaDE 2.0) project. In order to extract the WSDE’s water allocations data from the input files and publish it online through ESRI layers so that it can be ready for WaDE 2.0, three Python scripts are used to generate CSV files for water sources, sites, and water allocations input tables (Step 1), and three other CSV files are manually created (Step 2), in data tables compatible with WaDE 2.0.

# Step 1: Execute Python Scripts to Generate CSV Data for water sources, sites, and water allocations.
The following scripts use queries to extract WSDE’s water rights data into views compatible with WaDE 2.0 (see list below for name of each script).  

- #1. watersources_WA.ipynb
- #2. sites_WA.ipynb
- #3. waterallocations_WA.ipynb

Note: The outputs from 'watersources_WA.ipynb' and 'sites_WA.ipynb' (water sources and sites csv files) provide inputs to the 'waterallocations_WA.ipynb', so the order in which scripts are operated is important.  

All scripts can be found at the WaDE’s Github repository [MappingStatesDataToWaDE2.0 in the Washington folder](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/edit/master/Washington/).

## 1-1. watersources_OR.ipynb
Purpose: generate a list of water source names, source types, and quality indicators.

#### Inputs: 
- **Person_Plus_EXTRACT_FromWRTSnotGWIS.csv**

Dependency:  None

Supplemental Scripts Required:  None

#### Operation:
- Read the input file and form an output dataframe.
- Generate empty **watersources.csv** file with controlled vocabulary headers.
- Assign water soure type based on the dictionary mapping of the code 'WaRecRCWClassTypeCode'.
- Assign 'Unspecified' for water source names as it doesn't currently exit. 
- Enter default values for fields with constant values or those that do not have values currently.
- Drop duplicate rows if they exist.
- Generate WaterSourceNativeID
- Assign water source UUID to each (unique) row.
- Copy results into **watersources.csv** and export.			

#### Sample Data (Note: not all fields shown):
WaterSourceUUID | WaterSourceNativeID | WaterSourceName | WaterSourceTypeCV | WaterQualityIndicatorCV
------------ | ------------ | -------- | ---------- | ---- 
WA_1  | 1 | Unspecified | surfaceWater | Fresh

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **watersources_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **watersources_WA.ipynb** include the following: 
- WaterSourceUUID
- WaterSourceTypeCV
- WaterQualityIndicatorCV

## 1-2. sites_WA.ipynb
Purpose: generate a list of sites where water is diverted for use (also known as Points Of Diversion, PODs).

Dependency:  None

Supplemental Scripts Required: None

#### Inputs: 
- **D_Point.csv**

#### Operation:   
- Generate empty sites.csv file with controlled vocabulary headers
- Assign SiteNativeID from 'D_Point_ID'
- Specify site type based on dictionary that maps the 'D_Point_Type_CD' code to its respective values
- Leave site name as 'Unspecified'
- Project X and Y coordindates in EPSG:2927 to longitude and latitude in EPSG:4236
- Map the codes in 'Position_With_CD' to Coordinate mathod CV based on the corresponding dictionary
- Map the Coordinate accuracy CV from 'Location_CD' based on the corresponding dictionary
- Drop duplicates if any
- Generate SiteUUID based on SiteNativeID 
- Drop data if missing latitude/longitude
- copy results into **sites.csv** and export.  

#### Sample Data (Note: not all fields shown):
SiteUUID | SiteNativeID | SiteName  | SiteTypeCV | Longitude | Latitude 
------------ | ------------ | ---------- | ---- | ---- | ---- 
WA_104 | 203659 | Unspecified  | well (or ground water device unknown) | -120.0138 | 46.3210 

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **sites_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **sites_WA.ipynb** include the following: 
- SiteUUID 
- SiteName
- CoordinateMethodCV 
- EPSGCodeCV

## 1-3. waterallocations_WA.ipynb
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

Dependency: watersources.csv and sites.csv generated above.

Supplemental Scripts Required: None

#### Inputs: 
- **Person_Plus_EXTRACT_FromWRTSnotGWIS.csv**
- **D_Point_WR_Doc.csv**

#### Operation:
 - Generate empty waterAllocations.csv file with controlled vocabulary headers
 - Assign Native Allocation ID from 'WR_Doc_ID'
 - Get Site IDs from sites.csv based on the mapping between 'D_Point_ID' and 'WR_Doc_ID' through 'D_Point_WR_Doc'. Note there might be multiple sites mapped into one water right
 - Map Watersource IDs from watersources.csv based on source type code 'WaRecRCWClassTypeCode' 
 - Assign Beneficial use category from 'PurposeOfUseTypeCodes' based on mapping table
 - Get Allocation type from 'WaRecPhaseTypeCode' 
 - Get Allocation legal status from 'WaRecProcessStatusTypeCode'
 - Specify Allocation owner by concatenating Last name or Organization name ('PersonLastOrOrganizationNM') and first name ('PersonFirstNM')
 - Get Allocation priority date from 'PriorityDate' and format it in WaDE2 compatible form
 - Assign Allocation time frame start and end the default values of 01/01 and 12/31, respectively
 - Get Allocation amount from 'InstantaneousQuantity', its unit from 'InstantaneousUnitCode', and convert all values to have units of CFS
 - Get Allocation maximum from 'AnnualVolumeQuantity' 
 - Drop rows if both Allocation amount and Allocation maximum are null
 - Drop duplicates if any
 - Copy results into **waterallocations.csv** and export  

#### Sample Data (Note: not all fields shown):
OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseCategory | AllocationNativeID | AllocationOwner | AllocationTypeCV | AllocationLegalStatusCV   
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ---------- | ----------- 
WSDE| WA_2195 | WA_2 | Irrigation, Domestic general | 2066186 |LARSON, ARNOLD V. | Claim | Active  

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. **allocations_mandatoryFieldMissing.csv**) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the **waterallocations_WA.ipynb** include the following: 
- OrganizationUUID
- VariableSpecificUUID
- WaterSourceUUID
- MethodUUID
- AllocationPriorityDate

# Step 2: Manually Modify Existing Files to Generate CA CSV Data Compatible with WaDE 2.0.
The following is a quick description of three CSV files manually created to be used as inputs into WaDE 2.0.  These tables usually have single rows, so are prepared by manual inspection.


## 2-1. variables.csv 
Purpose: generate legend of granular variables specific to each state.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.

VariableSpecificUUID | VariableSpecificCV | VariableCV | AggregationStatisticCV| AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth| ReportYearTypeCV | AmountUnitCV | MaximumAmountUnitCV
---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- | --------- | -------
WSDE Allocation all  | Allocation All | Allocation | Average | 1 | Year |10 | WaterYear| CFS | AFY

## 2-2. methods.csv
Purpose: generate legend of granular variables specific to each state detailing water right / allocation / etc data collection.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.       

MethodUUID | MethodName | MethodDescription| MethodNEMLink | ApplicableResourceTypeCV | MethodTypeCV | DataCoverageValue | DataQualityValueCV	| DataConfidenceValue
---------- | ---------- | ------------ | ------------- | ------------- | ------------ | -------------| ------------ | ---------- 
WSDE-Water Rights | Washington Water Rights | Water Rights | https://ecology.wa.gov/Water-Shorelines/Water-supply/Water-rights| Surface Ground | Adjudicated	|         |         |                 

  
## 2-3. Organizations.csv
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.
Dependency:  None
Supplemental Scripts Required:  None

#### Inputs:
- See the below prepared table.               

OrganizationUUID | OrganizationName | OrganizationPurview| OrganizationWebsite | OrganizationPhoneNumber |	OrganizationContactName	| OrganizationContactEmail |	OrganizationDataMappingURL |	State 
---------------- | ------------ | -------- | ---------- | ---------- | ------------ | -------------- | ------------ | ---------
WSDE |Washington State Department of Ecology  | The Water Resources' GWIS (Geographic Water Information System) database includes water right place-of-use polygons and associated device points. |  https://ecology.wa.gov/Water-Shorelines/Water-supply/Water-rights | 360-407-6000 |	Riddle, H. Nicholas | HRID461@ECY.WA.GOV |https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Washington	| WA

