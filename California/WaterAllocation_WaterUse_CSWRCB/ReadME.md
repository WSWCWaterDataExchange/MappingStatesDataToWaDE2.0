# California State Water Resources Control Board (CSWRCB) Water Rights (Allocation) & Water Use Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights & water use data made available by the [(California State Water Resources Control Board)]("https://www.waterboards.ca.gov/"), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way.  WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**California Water Rights Points of Diversion LIST (Detail Summary List)** | This list includes detail information about every Point of Diversion water rights record in the State Water Resources Control Board's "Electronic Water Rights Information Management System" (EWRIMS) database. | [link](https://data.ca.gov/dataset/california-water-rights-points-of-diversion) | [link](https://data.ca.gov/dataset/1c2117f4-e4be-47f7-9eb5-81b086aefe34/resource/2902511b-6b50-4084-82f0-d1a508a80067/download/ewrims-points-of-diversion-data-dictionary-final.xlsx)
**water-rights-water-use-reported-short** | THIS LIST IS A SIMPLIFIED VERSION OF THE WATER USE EXTENDED DATASET. This list includes detail information for WATER USE as reported annually under each water right as stored in the State Water Resources Control Board's "Electronic Water Rights Information Management System" (EWRIMS) database.a | [link](https://data.ca.gov/dataset/california-water-rights-water-use-reported/resource/621c31ae-7ea0-4915-b7dc-dfcb7efc77b9) | [link](https://data.ca.gov/dataset/california-water-rights-water-use-reported/resource/3d225ee1-f41d-4ddc-9773-d4d8af8aad44)


Input files used are as follows...
- ewrims_flat_file_pod.zip (water right and site information)
- water-rights-water-use-reported-short.zip (water use by water right information)
 

## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- California State Water Resources Control Allocation & Water Use Data: [link](https://drive.google.com/drive/folders/1OXD6SVL5a7IhJKCCb4DE5xL19Au46eqm?usp=drive_link)


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share California State Water Resources Control Board's water rights & water use data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *XX_Allocation and Water Use Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the California State Water Resources Control Board's water rights & water use data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_CSWRCBwr_wu_PreProcessAllocationData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_CSWRCBwr_wu_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, sitespecificamounts.csv, podsitetopousiterelationships.csv.
- **3_CSWRCBwr_wu_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
### 0) Code File: 1_CSWRCBwr_wu_PreProcessAllocationData.ipynb
Purpose: Pre-process the state agency's input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- ewrims_flat_file_pod.zip (water right and site information)
- water-rights-water-use-reported-short.zip (water use by water right information)

#### Outputs:
 - Pwr_wu_Main.zip

#### Operation and Steps:
- Read the input files and generate temporary input dataframes.
- Create WaDE *in_VariableSpecificUUID* based on unit given in the **use_direct_div_rate_units** field.  Separate by either a recognized CFS value or AF value (see below).
- Generate a CFS and a AF value from **use_direct_diversion_rate** input field using the  **use_direct_div_rate_units** input field...
    - CFS values include: Cubic Feet per Second, Gallons per Day (converted to CFS by / 646316.883), Acre-feet per Year (converted to CFS by / 723.968), Gallons per Minute (converted to CFS by / 448.83117).
    - AF values include: Acre-feet, Gallons (converted to AF by / 325850.943).
- Remove trialing '_' and ',' values from  **water_right_type** and **sub_type** input fields.
- At this time, CA does not track priority date.  All data will be considered exempt from WaDE CFS, AF and priority date checks at this time as a temp fix. 
- Any Record with a blank or nan value, replace with a 0 if numeric, or "WaDE_Unspecified" if string or object.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *Pwr_wu_Main.zip*.


***
## Code File: 2_CSWRCBwr_wu_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, sitespecificamounts.csv, podsitetopousiterelationships.csv).

#### Inputs:
- Pwr_wu_Main.zip

#### Outputs:
- methods.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- variables.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- organizations.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- watersources.csv
- sites.csv
- waterallocations.csv
- sitespecificamounts.csv
- podsitetopousiterelationships.csv


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
|    | MethodUUID   | ApplicableResourceTypeCV      | DataConfidenceValue   | DataCoverageValue   | DataQualityValueCV   | MethodName                     | MethodNEMILink                                                               | MethodTypeCV    | WaDEDataMappingUrl                                                                                                         |
|---:|:-------------|:------------------------------|:----------------------|:--------------------|:---------------------|:-------------------------------|:-----------------------------------------------------------------------------|:----------------|:---------------------------------------------------------------------------------------------------------------------------|
|  0 | CSWRCBwr_M1  | Surface Water and Groundwater |                       |                     |                      | California Water Rights Method | https://www.waterboards.ca.gov/waterrights/board_info/faqs.html#toc178761079 | Legal Processes | https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/California/WaterAllocation_WaterUse_CSWRCB |

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
|    | VariableSpecificUUID   |   AggregationInterval | AggregationIntervalUnitCV   | AggregationStatisticCV   | AmountUnitCV   | MaximumAmountUnitCV   |   ReportYearStartMonth | ReportYearTypeCV   | VariableCV   | VariableSpecificCV   |
|---:|:-----------------------|----------------------:|:----------------------------|:-------------------------|:---------------|:----------------------|-----------------------:|:-------------------|:-------------|:---------------------|
|  1 | CSWRCBwr_V2            |                     1 | Year                        | Average                  | AF             | AF                    |                      1 | CalendarYear       | Allocation   | Allocation           |


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
|    | OrganizationUUID   | OrganizationContactEmail          | OrganizationContactName   | OrganizationName                               | OrganizationPhoneNumber   | OrganizationPurview                                                                                                                                                                                | OrganizationWebsite             | State   |
|---:|:-------------------|:----------------------------------|:--------------------------|:-----------------------------------------------|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------|:--------|
|  0 | CSWRCBwr_O1        | Greg.Gearheart@waterboards.ca.gov | Greg Gearheart            | California State Water Resources Control Board | 916-341-5892              | The Electronic Water Rights Information Management System (eWRIMS) is a computer database developed by the State Water Resources Control Board to track information on water rights in California. | https://www.waterboards.ca.gov/ | CA      |


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency info to the *WaDE WaterSources* specific columns.  See *XX_Allocation and Water Use Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceUUID* = ""
    - *WaterQualityIndicatorCV* = ""
    - *WaterSourceName* = **SOURCE_NAME** input.
    - *WaterSourceNativeID* = ""
    - *WaterSourceTypeCV* = **SOURCE_TYPE** input.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | WaterSourceUUID     | Geometry   | GNISFeatureNameCV   | WaterQualityIndicatorCV   | WaterSourceName   | WaterSourceNativeID   | WaterSourceTypeCV   |
|---:|:--------------------|:-----------|:--------------------|:--------------------------|:------------------|:----------------------|:--------------------|
|  1 | CSWRCBwr_WSwadeId10 |            |                     | Fresh                     | Witcher Creek     | wadeId10              | Unspecified         |


Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


## 5) Site Information
Purpose: generate a list of sites information.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign agency info to the *WaDE Site* specific columns.  See *XX_Allocation and Water Use Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *SiteUUID* = ""
    - *WaterSourceUUIDs* = Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - *CoordinateAccuracy* = ""
    - *CoordinateMethodCV* = **LOCATION_METHOD** input.
    - *Country* = **COUNTY** input.
    - *EPSGCodeCV* = 4326
    - *Geometry* = ""
    - *GNISCodeCV* = ""
    - *HUC12* = **HUC_12_NUMBER** input
    - *HUC8* = **HUC_8_NUMBER** input.
    - *Latitude* = **LATITUDE** input.
    - *Longitude* = **LONGITUDE** input.
    - *NHDNetworkStatusCV* = ""
    - *NHDProductCV* = ""
    - *PODorPOUSite* = "POD"
    - *SiteName* = **POD_NAME** input.
    - *SiteNativeID* = **POD_ID** input.
    - *SiteTypeCV* = **POD_TYPE** input.
    - *StateCV* = "CA"
    - *USGSSiteID* = ""
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | SiteUUID    | RegulatoryOverlayUUIDs   | WaterSourceUUIDs     | CoordinateAccuracy   | CoordinateMethodCV   | County   |   EPSGCodeCV | GNISCodeCV   |       HUC12 |     HUC8 |   Latitude |   Longitude | NHDNetworkStatusCV   | NHDProductCV   | PODorPOUSite   | SiteName   |   SiteNativeID | SitePoint   | SiteTypeCV                | StateCV   | USGSSiteID   |
|---:|:------------|:-------------------------|:---------------------|:---------------------|:---------------------|:---------|-------------:|:-------------|------------:|---------:|-----------:|------------:|:---------------------|:---------------|:---------------|:-----------|---------------:|:------------|:--------------------------|:----------|:-------------|
|  1 | CSWRCBwr_S3 |                          | CSWRCBwr_WSwadeId755 | WaDE Blank           | GIS_LL               | Kern     |         4326 |              | -2147483648 | 18030012 |    35.3467 |    -119.239 |                      |                | POD            | WaDE Blank |              3 |             | Point Of Direct Diversion | CA        |              |


Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sites_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the sites include the following...
- SiteUUID 
- CoordinateMethodCV
- EPSGCodeCV
- SiteName


## 6) AllocationsAmounts Information
Purpose: generate master sheet of water allocations to import into WaDE 2.0.

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Allocations* specific columns.
- Assign agency info to the *WaDE Water Allocations* specific columns.  See *XX_Allocation and Water Use Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationApplicationDate* = **APPLICATION_RECD_DATE** input.
    - *AllocationAssociatedConsumptiveUseSiteIDs* = ""
    - *AllocationAssociatedWithdrawalSiteIDs* = ""
    - *AllocationBasisCV* = ""
    - *AllocationChangeApplicationIndicator* = ""
    - *AllocationCommunityWaterSupplySystem* = ""
    - *AllocationCropDutyAmount* = ""
    - *AllocationExpirationDate* = ""
    - *AllocationFlow_CFS* = **USE_DIRECT_DIVERSION_RATE** & **USE_DIRECT_DIV_RATE_UNITS** inputs, see "1_CSWRCBwr_wu_PreProcessAllocationData.ipynb" for specifics.
    - *AllocationLegalStatusCV* = **WATER_RIGHT_STATUS** input.
    - *AllocationNativeID* = **APPLICATION_NUMBER** input.
    - *AllocationOwner* =  **PRIMARY_OWNER_NAME** input.
    - *AllocationPriorityDate* = **PRIORITY_DATE** input.
    - *AllocationSDWISIdentifierCV* = ""
    - *AllocationTimeframeEnd* = **DIRECT_DIV_SEASON_END** input.
    - *AllocationTimeframeStart* = **DIRECT_DIV_SEASON_START** input.
    - *AllocationTypeCV* = **WATER_RIGHT_TYPE** & **SUB_TYPE** inputs
    - *AllocationVolume_AF* = **USE_DIRECT_DIVERSION_RATE** & **USE_DIRECT_DIV_RATE_UNITS** inputs, see "1_CSWRCBwr_wu_PreProcessAllocationData.ipynb" for specifics.
    - *BeneficialUseCategory* = **USE_CODE** input.
    - *CommunityWaterSupplySystem* = ""
    - *CropTypeCV* = ""
    - *CustomerTypeCV* = ""
    - *DataPublicationDate* = "{use today's date}"
    - *DataPublicationDOI* = ""
    - *ExemptOfVolumeFlowPriority* = "1", we want this to be wade excempt from CFS, AF, and priority date checks.
    - *GeneratedPowerCapacityMW* = ""
    - *IrrigatedAcreage* = ""
    - *IrrigationMethodCV* = ""
    - *LegacyAllocationIDs* = ""
    - *OwnerClassificationCV* = ""
    - *PopulationServed* = ""
    - *PowerType* = ""
    - *PrimaryBeneficialUseCategory* = ""
    - *WaterAllocationNativeURL* = "https://ciwqs.waterboards.ca.gov/ciwqs/ewrims/EWServlet?Redirect_Page=EWPublicAppSummary.jsp&Purpose=getEwrimsPublicSummary&wrWaterRightID=" + **WR_WATER_RIGHT_ID** input.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | AllocationUUID     | MethodUUID   | OrganizationUUID   | SiteUUID                                        | VariableSpecificUUID   | AllocationApplicationDate   | AllocationAssociatedConsumptiveUseSiteIDs   | AllocationAssociatedWithdrawalSiteIDs   | AllocationBasisCV   | AllocationChangeApplicationIndicator   | AllocationCommunityWaterSupplySystem   | AllocationCropDutyAmount   | AllocationExpirationDate   |   AllocationFlow_CFS | AllocationLegalStatusCV   | AllocationNativeID   | AllocationOwner                 | AllocationPriorityDate   | AllocationSDWISIdentifierCV   | AllocationTimeframeEnd   | AllocationTimeframeStart   | AllocationTypeCV   |   AllocationVolume_AF | BeneficialUseCategory   | CommunityWaterSupplySystem   | CropTypeCV   | CustomerTypeCV   | DataPublicationDate   | DataPublicationDOI   |   ExemptOfVolumeFlowPriority | GeneratedPowerCapacityMW   |   IrrigatedAcreage | IrrigationMethodCV   | LegacyAllocationIDs   | OwnerClassificationCV   | PopulationServed   | PowerType   | PrimaryBeneficialUseCategory   | WaterAllocationNativeURL                                                                                                                     |
|---:|:-------------------|:-------------|:-------------------|:------------------------------------------------|:-----------------------|:----------------------------|:--------------------------------------------|:----------------------------------------|:--------------------|:---------------------------------------|:---------------------------------------|:---------------------------|:---------------------------|---------------------:|:--------------------------|:---------------------|:--------------------------------|:-------------------------|:------------------------------|:-------------------------|:---------------------------|:-------------------|----------------------:|:------------------------|:-----------------------------|:-------------|:-----------------|:----------------------|:---------------------|-----------------------------:|:---------------------------|-------------------:|:---------------------|:----------------------|:------------------------|:-------------------|:------------|:-------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|
|  1 | CSWRCBwr_WRA000018 | CSWRCBwr_M1  | CSWRCBwr_O1        | CSWRCBwr_S28034,CSWRCBwr_S28036,CSWRCBwr_S28035 | CSWRCBwr_V1            |                             |                                             |                                         | WaDE Blank          |                                        |                                        |                            |                            |                    0 | Licensed                  | A000018              | Glenncolusa Irrigation District |                          |                               | 1-Nov                    | 1-Mar                      | Appropriative      |                     0 | Irrigation              |                              |              |                  | 01/17/2024            |                      |                            1 |                            |                  0 |                      |                       | Private                 |                    |             | Agriculture Irrigation         | https://ciwqs.waterboards.ca.gov/ciwqs/ewrims/EWServlet?Redirect_Page=EWPublicAppSummary.jsp&Purpose=getEwrimsPublicSummary&wrWaterRightID=3 |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- WaterSourceUUID
- SiteUUID
- AllocationPriorityDate
- BeneficialUseCategory
- AllocationAmount or AllocationMaximum
- DataPublicationDate


## 7) SiteSpecificAmounts Information
Purpose: generate master sheet of site-specific amount information to import into WaDE 2.0.

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE site-specific amount* specific columns.
- Assign agency info to the *WaDE site-specific amount* specific columns.  See *XX_Allocation and Water Use Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, *WaterSourceUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *Amount* = **AMOUNT** input.
    - *AssociatedNativeAllocationIDs* = **APPLICATION_NUMBER** input.
    - *BeneficialUseCategory* = see water right above.
    - *CommunityWaterSupplySystem* = ""
    - *CropTypeCV* = ""
    - *CustomerTypeCV* = ""
    - *DataPublicationDate* = ""
    - *DataPublicationDOI* = ""
    - *Geometry* = ""
    - *IrrigatedAcreage* = ""
    - *IrrigationMethodCV* = ""
    - *PopulationServed* = ""
    - *PowerGeneratedGWh* = ""
    - *PowerType* = ""
    - *PrimaryUseCategory* = ""
    - *ReportYearCV* = **YEAR** input.
    - *SDWISIdentifier* = ""
    - *TimeframeEnd* = **MONTH FORMATTED** input.
    - *TimeframeStart* = **MONTH FORMATTED** input.
																						
- Perform error check on output dataframe.
- Export output dataframe *sitespecificamounts.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | MethodUUID   | OrganizationUUID   | SiteUUID        | VariableSpecificUUID   | WaterSourceUUID    |   Amount | AllocationCropDutyAmount   | AssociatedNativeAllocationIDs   | BeneficialUseCategory   | CommunityWaterSupplySystem   | CropTypeCV   | CustomerTypeCV   | DataPublicationDate   | DataPublicationDOI   | Geometry   | IrrigatedAcreage   | IrrigationMethodCV   | PopulationServed   | PowerGeneratedGWh   | PowerType   | PrimaryUseCategory     |   ReportYearCV | SDWISIdentifier   | TimeframeEnd   | TimeframeStart   |
|---:|:-------------|:-------------------|:----------------|:-----------------------|:-------------------|---------:|:---------------------------|:--------------------------------|:------------------------|:-----------------------------|:-------------|:-----------------|:----------------------|:---------------------|:-----------|:-------------------|:---------------------|:-------------------|:--------------------|:------------|:-----------------------|---------------:|:------------------|:---------------|:-----------------|
|  1 | CSWRCBwr_M1  | CSWRCBwr_O1        | CSWRCBwr_S28034 | CSWRCBwr_V4            | CSWRCBwr_WSwadeId7 |     6758 |                            | A000018                         | Irrigation              |                              |              |                  | 01/18/2024            |                      |            |                    |                      |                    |                     |             | Agriculture Irrigation |           2008 |                   | 2008-05-01     | 2008-05-01       |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *sitespecificamounts_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the site-specific amount include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- SiteUUID
- BeneficialUseCategory
- Amount
- DataPublicationDate


### 8) POD Site -To- POU Polygon Relationships
Purpose: generate linking element between POD and POU sites that share the same water right.
Note: podsitetopousiterelationships.csv output only needed if both POD and POU data is present, ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `otherwise produces empty file.`

#### Operation and Steps:
- Read the sites.csv & waterallocations.csv input files.
- Create three temporary dataframes: one for waterallocations, & two for site info that will store POD and POU data separately.
- For the temporary POD dataframe...
  - Read in site.csv data from sites.csv with a _PODSiteUUID_ field = POD only.
  - Create _PODSiteUUID_ field = _SiteUUID_.
- For the temporary POU dataframe
  - Read in site.csv data from sites.csv with a _PODSiteUUID_ field = POU only.
  - Create _POUSiteUUID_ field = _SiteUUID_.
- For the temporary waterallocations dataframe, explode _SiteUUID_ field to create unique rows.
- Left-merge POD & POU dataframes to the waterallocations dataframe via _SiteUUID_ field.
- Consolidate waterallocations dataframe by grouping entries by _AllocationNativeID_ filed.
- Explode the consolidated waterallocations dataframe again using the _PODSiteUUID_ field, and again for the _POUSiteUUID_ field to create unique rows.
- Perform error check on waterallocations dataframe (check for NaN values)
- If waterallocations is not empty, export output dataframe _podsitetopousiterelationships.csv_.


***
## Source Data & WaDE Complied Data Assessment
The following info is from a data assessment evaluation of the completed data...

Dataset | Num of Source Entries (rows)
---------- | ---------- 
**ewrims_flat_file_pod** | 64,873
**water-rights-water-use-reported-short** (rows):  | 11,731,056


Dataset  | Num of Identified PODs | Num of Identified POUs | Num of Identified Water Right Records | Num of Identified Water Use Records
---------- | ------------ | ------------ | ------------ | ------------
**Compiled WaDE Data** | 34,551 | 0 | 41,342 | 1,973,879


Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
Unused WaterSource Record    | 1,462 | removed from watersources.csv input
Unused Site Record                      | 13,235 | removed from sites.csv input
Incomplete or bad entry for Latitude     | 1,960 | removed from sites.csv input
Incomplete or bad entry for SiteUUID    | 1,822 | removed from waterallocations.csv input
Negative, blank, or 0 Amount values                     | 4,605,163 | removed from sitespecificamounts.csv input
Not Unique combination of SiteSpecificAmounts record    | 767,372 | removed from sitespecificamounts.csv input
Incomplete or bad entry for SiteUUID                    | 72,429 | removed from sitespecificamounts.csv input


**Figure 1:** Distribution of POD vs POU Sites within the sites.csv
![](figures/PODorPOUSite.png)

**Figure 2:** Distribution Sites by WaterSourceTypeCV within the sites.csv
![](figures/WaterSourceTypeCV.png)

**Figure 3:** Distribution of Identified Water Right Records by WaDE Categorized Primary Beneficial Uses within the waterallocations.csv
![](figures/PrimaryBeneficialUseCategory.png)

**Figure 4a:** Range of Priority Date of Identified Water Right Records within the waterallocations.csv
<!-- ![](figures/AllocationPriorityDate1.png) -->
- Priority Date not required

**Figure 4b:** Cumulative distribution of Priority Date of Identified Water Right Records within the waterallocations.csv
<!-- ![](figures/AllocationPriorityDate2.png) -->
- Priority Date not required

**Figure 5:** Distribution & Range of Flow (CFS) of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationFlow_CFS.png)

**Figure 6:** Distribution & Range of Volume (AF) of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationVolume_AF.png)

**Figure 7:** Distribution & Range of Amount (CFS) within the sitespecificamounts.csv
![](figures/Amount.png)

**Figure 8:** Map of Identified Points within the sites.csv
![](figures/PointMap.png)

**Figure 9:** Map of Identified Polygons within the sites.csv
![](figures/PolyMap.png)


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [California State Water Resources Control Board (CSWRCB)](https://www.waterboards.ca.gov).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>

CSWRCB Staff
- Greg Gearheart. Deputy Director, Office of Information Management and Analysis, California Water Boards
- Rafael Maestu. Economist/Chief Data Scientist, California Water Boards