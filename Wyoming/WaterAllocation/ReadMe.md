# WWDO Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Wyoming Water Development Office (WWDO)](https://wwdc.state.wy.us/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Point of diversion (POD)** | Point of diversion surface and groundwater data files were made temporary available to the WSWC staff by the WWDO via email correspondence and shared through Google Drive. | Links no longer available, contact WWDO for further instructions. | not provided
**Place of Use (POU)** | Place of Use data files were made temporary available to the WSWC staff by the WWDO via email correspondence and shared through Google Drive. | Links no longer available, contact WWDO for further instructions. | not provided

Two unique files were created, one used by the WSWC staff to understand the available data (*"_with Notes"*), the second resulting files to be used as input to the Python codes that prepare WaDE2 input files.  Input files used are as follows...
 - POD_SW_DepthI_FC.csv
 - POD_GW_DepthI_FC.csv
 - POU.csv


## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Wyoming Allocation Data: https://drive.google.com/drive/folders/1hlD3ho_F9HDEzrboeCp2QMf4f1KBy5Cp?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *WYwr_Allocation Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_WYwr_PreProcessAllocationData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_WYwr_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv.
- **3_WYwr_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.

***
## Code File: 1_WYwr_PreProcessAllocationData.ipynb
Purpose: Pre-process the Wyoming input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- POD_SW_DepthI_FC.csv
- POD_GW_DepthI_FC.csv
- POU.csv

#### Outputs:
 - Pwr_wyMain.zip

#### Operation and Steps:
- Read in the input files.  Goal will be to create separate POD and POU centric dataframes, then join together for single long output dataframe.
- For POD data...
    - Perform the following additional actions on the groundwater data...
        - *WaterSourceTypeCV* == Groundwater.
        - *WaterSourceName* == Unspecified.
        - *Latitude* = **Latitude_Double**, ensure float datatype.
        - *Longitude* = **Longitude_Double**, ensure float datatype.
        - *SiteName* = **FacilityName**, ensure string datatype.
        - *SiteTypeCV* = **Facility_type**, ensure string datatype.
        - *AllocationFlow_CFS* = **Total_Flow_CFS___Appropriation_GPM_**, ensure float datatype.
        - *AllocationNativeID* = **WR_Number**, ensure string datatype.
        - *AllocationOwner* =  **Company**, **FirstName**, and **LastName** fields, see pre-process code for specifics.
        - *AllocationPriorityDate* = **PriorityDate**.  Format **PriorityDate** field to %m/%d/%Y format.
        - *AllocationTypeCV* = **SummaryWRStatus**, ensure string datatype.
        - *BeneficialUseCategory* = **Uses**, ensure string datatype.  Use provided WWDO terminology code and **Uses** field, see see pre-process code for specifics.  In addition, include all records that have a "Z" in the **Survey_Type_Survey_Number_Survey_Suffix** for "Wild and Scenic River" benefical uses.
    - Perform the following additional actions on the surface water data...
        - *WaterSourceTypeCV* == Surface Water.
        - *WaterSourceName* == **Stream_Source**, ensure string datatype.
        - *Latitude* = **Latitude_Double**, ensure float datatype.
        - *Longitude* = **Longitude_Double**, ensure float datatype.
        - *SiteName* = **FacilityName**, ensure string datatype.
        - *SiteTypeCV* = **Facility_type**, ensure string datatype.
        - *AllocationFlow_CFS* = **Total_Flow_CFS___Appropriation_GPM_**, ensure float datatype.
        - *AllocationNativeID* = **WR_Number**, ensure string datatype.
        - *AllocationOwner* =  **Company**, **FirstName**, and **LastName** fields, see pre-process code for specifics.
        - *AllocationPriorityDate* = **PriorityDate**.  Format **PriorityDate** field to %m/%d/%Y format.
        - *AllocationTypeCV* = **SummaryWRStatus**, ensure string datatype.
        - *BeneficialUseCategory* = **Uses**, ensure string datatype.  Use provided WWDO terminology code and **Uses** field, see see pre-process code for specifics.    In addition, include all records that have a "Z" in the **Survey_Type_Survey_Number_Survey_Suffix** for "Wild and Scenic River" benefical uses.
    - Concatenate groundwater and surface water dataframes together to create single long output table.
    - Create WaDE POD centric temporary dataframe.  Extract POD relevant data (see preprocessing code).
- For POU data...
    - *AllocationPriorityDate* = **PriorityDate**.  Format **PriorityDate** field to %m/%d/%Y format.
    - *BeneficialUseCategory* = **Uses**, ensure string datatype.  Use provided WWDO terminology code and **Uses** field, see see pre-process code for specifics.  In addition, include all records that have a "Z" in the **Survey** for "Wild and Scenic River" benefical uses.
    - Create WaDE POU centric temporary dataframe.  Extract POU relevant data (see preprocessing code).
- Concatenate temporary POD & POU dataframes together into single long output dataframe.
- Remove the following records with the **SummaryWRStatus** value = "Incomplete", "Unadjudicated", "Suspended", "Rejected".  WaDE primarily focuses on what can be considered an Active legal right.
- Generate WaDE specific field *SiteNativeID* from *Latitude*, *Longitude*, *SiteType* and *SiteName* fields.  Used to identify unique sites.
- Generate WaDE specific field *WaterSourceNativeID* from *WaterSourceName* & *WaterSourceTypeCV* fields.  Used to identify unique sources of water.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *Pwr_wyMain.zip*.


***
## Code File: 2_NMwr_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv).

#### Inputs:
- Pwr_NMMain.zip

#### Outputs:
- methods.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- variables.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- organizations.csv ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Create by hand.`
- watersources.csv
- sites.csv
- waterallocations.csv
- podsitetopousiterelationships.csv


## 1) Method Information
Purpose: generate legend of granular methods used on data collection.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Method* specific columns.
- Assign **WWDO** info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | MethodUUID   | ApplicableResourceTypeCV   | DataConfidenceValue   | DataCoverageValue   | DataQualityValueCV   | MethodName                  | MethodNEMILink                                                      | MethodTypeCV    | WaDEDataMappingUrl                                                                      |
|---:|:-------------|:---------------------------|:----------------------|:--------------------|:---------------------|:----------------------------|:--------------------------------------------------------------------|:----------------|:----------------------------------------------------------------------------------------|
|  0 | WYwr_M1      | Surface Ground Water       |                       |                     |                      | Wyoming Water Rights Method | https://waterplan.state.wy.us/plan/bear/2001/techmemos/waterlaw.pdf | Legal Processes | https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Wyoming |


## 2) Variables Information
Purpose: generate legend of granular variables specific to each state.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Variable* specific columns.
- Assign **WWDO** info to the *WaDE Variable* specific columns (this was hardcoded by hand for simplicity).
- Assign variable UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *variables.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | VariableSpecificUUID   |   AggregationInterval | AggregationIntervalUnitCV   | AggregationStatisticCV   | AmountUnitCV   | MaximumAmountUnitCV   |   ReportYearStartMonth | ReportYearTypeCV   | VariableCV      | VariableSpecificCV   |
|---:|:-----------------------|----------------------:|:----------------------------|:-------------------------|:---------------|:----------------------|-----------------------:|:-------------------|:----------------|:---------------------|
|  0 | WYwr_V1                |                     1 | Year                        | Average                  | CFS            | AFY                   |                     11 | WaterYear          | Consumptive Use | Consumptive Use      |


## 3) Organization Information
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **WWDO** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | OrganizationUUID   | OrganizationContactEmail   | OrganizationContactName   | OrganizationName                 | OrganizationPhoneNumber   | OrganizationPurview                                                                                                                                                                                                    | OrganizationWebsite       | State   |
|---:|:-------------------|:---------------------------|:--------------------------|:---------------------------------|:--------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------|:--------|
|  0 | WYwr_OR1           | mabel.jones1@wyo.gov       | Mabel Jones               | Wyoming Water Development Office | 307-777-7626              | This agency contributes to the quality of life by addressing the water resources needs of our citizens through the construction of new water supply projects and the rehabilitation of existing water supply projects. | https://wwdc.state.wy.us/ | WY      |


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign **WWDO** info to the *WaDE WaterSources* specific columns.  See *WY_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *WY_POU_Allocation Schema Mapping to WaDE_QA.xlsx* files for specific details.  Items of note are as follows...
    - *WaterSourceName* = *in_WaterSourceName*, Unspecified if not given, see *0_PreProcessWyomingAllocationData.ipynb* for specifics.
    - *WaterSourceNativeID* = *in_WaterSourceNativeID*, see *0_PreProcessWyomingAllocationData.ipynb* for specifics.
    - *WaterSourceTypeCV* = *in_WaterSourceTypeCV*, see *0_PreProcessWyomingAllocationData.ipynb* for specifics.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | WaterSourceUUID   | Geometry   | GNISFeatureNameCV   | WaterQualityIndicatorCV   | WaterSourceName   | WaterSourceNativeID   | WaterSourceTypeCV   |
|---:|:------------------|:-----------|:--------------------|:--------------------------|:------------------|:----------------------|:--------------------|
|  0 | WYwr_WwadeID1     |            |                     | Fresh                     | WaDE Blank        | wadeID1               | Groundwater         |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


## 5) Site Information
Purpose: generate a list of sites information.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign **WWDO** info to the *WaDE Site* specific columns.  See *WY_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *WY_POU_Allocation Schema Mapping to WaDE_QA.xlsx* files for specific details.  Items of note are as follows...
    - *Latitude* = **Latitude_Double**.
    - *Longitude* = **Longitude_Double**.
    - *SiteName* = **FacilityName**, Unspecified if not given.
    - *SiteNativeID* = *in_SiteNativeID*, see *0_PreProcessWyomingAllocationData.ipynb* for specifics.
    - *SiteTypeCV* = **Facility_type**, Unspecified if not given.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | SiteUUID      | RegulatoryOverlayUUIDs   | WaterSourceUUIDs   | CoordinateAccuracy   | CoordinateMethodCV   | County   |   EPSGCodeCV | GNISCodeCV   |        HUC12 |     HUC8 |   Latitude |   Longitude | NHDNetworkStatusCV   | NHDProductCV   | PODorPOUSite   | SiteName    | SiteNativeID   | SitePoint   | SiteTypeCV   | StateCV   | USGSSiteID   |
|---:|:--------------|:-------------------------|:-------------------|:---------------------|:---------------------|:---------|-------------:|:-------------|-------------:|---------:|-----------:|------------:|:---------------------|:---------------|:---------------|:------------|:---------------|:------------|:-------------|:----------|:-------------|
|  0 | WYwr_SwadeID1 | WYre_RO18                | WYwr_WwadeID1      | WaDE Blank           | WaDE Blank           | Niobrara |         4326 |              | 101201040202 | 10120104 |    42.9129 |    -104.461 |                      |                | POD            | O W Well #1 | wadeID1        |             | Well         | WY        |              |

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
- Assign **WWDO** info to the *WaDE Water Allocations* specific columns.  See *WY_POD_Allocation Schema Mapping to WaDE_QA.xlsx* & *WY_POU_Allocation Schema Mapping to WaDE_QA.xlsx* files for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* = **Total_Flow_CFS___Appropriation_GPM_**.
    - *AllocationNativeID* = **WR_Number**.
    - *AllocationOwner* =  **Company**, **FirstName**, and **LastName** fields, see pre-process code for specifics.
    - *AllocationPriorityDate* = **PriorityDate**.
    - *AllocationTypeCV* = **SummaryWRStatus**.
    - *BeneficialUseCategory* = **Uses**. 
    - *WaterAllocationNativeURL* = "http://seoweb.wyo.gov/e-Permit/Common/Login.aspx"
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | AllocationUUID   | MethodUUID   | OrganizationUUID   | SiteUUID          | VariableSpecificUUID   | AllocationApplicationDate   | AllocationAssociatedConsumptiveUseSiteIDs   | AllocationAssociatedWithdrawalSiteIDs   | AllocationBasisCV   | AllocationChangeApplicationIndicator   | AllocationCommunityWaterSupplySystem   | AllocationCropDutyAmount   | AllocationExpirationDate   |   AllocationFlow_CFS | AllocationLegalStatusCV   |   AllocationNativeID | AllocationOwner              | AllocationPriorityDate   | AllocationSDWISIdentifierCV   | AllocationTimeframeEnd   | AllocationTimeframeStart   | AllocationTypeCV    |   AllocationVolume_AF | BeneficialUseCategory    | CommunityWaterSupplySystem   | CropTypeCV   | CustomerTypeCV   | DataPublicationDate   | DataPublicationDOI   |   ExemptOfVolumeFlowPriority | GeneratedPowerCapacityMW   |   IrrigatedAcreage | IrrigationMethodCV   | LegacyAllocationIDs   | OwnerClassificationCV   | PopulationServed   | PowerType   | PrimaryBeneficialUseCategory   | WaterAllocationNativeURL                         |
|---:|:-----------------|:-------------|:-------------------|:------------------|:-----------------------|:----------------------------|:--------------------------------------------|:----------------------------------------|:--------------------|:---------------------------------------|:---------------------------------------|:---------------------------|:---------------------------|---------------------:|:--------------------------|---------------------:|:-----------------------------|:-------------------------|:------------------------------|:-------------------------|:---------------------------|:--------------------|----------------------:|:-------------------------|:-----------------------------|:-------------|:-----------------|:----------------------|:---------------------|-----------------------------:|:---------------------------|-------------------:|:---------------------|:----------------------|:------------------------|:-------------------|:------------|:-------------------------------|:-------------------------------------------------|
|  0 | WYwr_WR41419     | WYwr_M1      | WYwr_OR1           | WYwr_SwadeID58957 | WYwr_V1                |                             |                                             |                                         | WaDE Blank          |                                        |                                        |                            |                            |                    0 | Fully Adjudicated         |                41419 | Boardman, Russell And Leslie | 1887-04-30               |                               |                          |                            | Prior Appropriation |                     0 | Irrigation Surface Water |                              |              |                  | 08/11/2024            |                      |                            0 |                            |                  0 | 24.65,16.0,30.75     |                       | Private                 |                    |             | Agriculture Irrigation         | http://seoweb.wyo.gov/e-Permit/Common/Login.aspx |

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *waterallocations_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water allocations include the following...
- MethodUUID
- VariableSpecificUUID
- OrganizationUUID
- SiteUUID
- AllocationPriorityDate
- BeneficialUseCategory
- AllocationAmount or AllocationMaximum
- DataPublicationDate


### 7) POD Site -To- POU Polygon Relationships
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

Dataset | Num of Source Entries (rows) | Num of Identified PODs | Num of Identified POUs | Num of Identified Water Right Records
---------- | ---------- | ------------ | ------------ | ------------
**Point of diversion (POD)_GW** | 2,323 | -| -| -
**Point of diversion (POD)_SW** | 9,659 | -| -| -
**Place of Use (POU)** | 491,676 | -| -| -
**WaDE Imports** | - | 9,173  | 56,160  | 64,648


Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
Unused WaterSource Record | 46 | Removed from watersource.csv
Unused Site Record | 2,376 | Removed from sites.csv
Incomplete or bad entry for Latitude | 934 | Removed from sites.csv
Too many entries / too long of entry for SiteName | 727 | Removed from sites.csv
MUltiple entries for SiteTypeCV | 5 | Removed from sites.csv
Incomplete or bad entry for SiteUUID | 1227 | Removed from waterallocations.csv
Incomplete or bad entry for IrrigationMethodCV | 306 | Removed from waterallocations.csv
Incomplete or bad entry for AllocationPriorityDate | 125 | Removed from waterallocations.csv
Incomplete or bad entry for Flow | 123 | Removed from waterallocations.csv
Incomplete or bad entry for AllocationLegalStatusCV | 2 | Removed from waterallocations.csv

**Figure 1:** Distribution of POD vs POU Sites within the sites.csv
![](figures/PODorPOUSite.png)

**Figure 2:** Distribution Sites by WaterSourceTypeCV within the sites.csv
![](figures/WaterSourceTypeCV.png)

**Figure 3:** Distribution of Identified Water Right Records by WaDE Categorized Primary Beneficial Uses within the waterallocations.csv
![](figures/PrimaryBeneficialUseCategory.png)

**Figure 4a:** Range of Priority Date of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationPriorityDate1.png)

**Figure 4b:** Cumulative distribution of Priority Date of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationPriorityDate2.png)

**Figure 5:** Distribution of Legal Status of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationLegalStatusCV.png)

**Figure 6:** Distribution & Range of Flow (CFS) of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationFlow_CFS.png)

**Figure 7:** Distribution & Range of Volume (AF) of Identified Water Right Records within the waterallocations.csv
<!-- ![](figures/AllocationVolume_AF.png) -->
 - No volume data provided

**Figure 8:** Map of Identified Points within the sites.csv
![](figures/PointMap.png)

**Figure 9:** Map of Identified Polygons within the sites.csv
<!-- ![](figures/PolyMap.png) -->
- no polygon geometry data provided.



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Wyoming Water Development Office (WWDO)](https://wwdc.state.wy.us/).

WSWC Staff
- Ryan James <rjames@wswc.utah.gov>

Wyoming DNRC Staff
- Mabel Jones <mabel.jones1@wyo.gov>
