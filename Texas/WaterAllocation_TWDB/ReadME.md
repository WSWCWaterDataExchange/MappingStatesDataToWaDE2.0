# Texas Water Development Board Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Texas Water Development Board (TWDB)](https://www.twdb.texas.gov/index.asp), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**GroundWater Rights** | Place of Diversion| [link](https://www.twdb.texas.gov/groundwater/data/gwdbrpt.asp) | [link](https://www.twdb.texas.gov/groundwater/faq/faqgwdb.asp)


One shapefile was created to be used as input.  Input files used are as follows...
- TWDB_Groundwater.zip
You then need to convert that zipped shape file to a csv. A easy free way is to upload the shape file to mapshaper.org(https://mapshaper.org/) and then export is as a csv
which is how we transferred the data into a csv file. 
New input file:
- TWDB_Groundwater.csv

## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Texas Water Development Board Allocation Data: https://drive.google.com/drive/folders/18O0lMwqCpqDJUH_ecAxGPtgEDc64ymS1


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *TWDBwr_Allocation Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_TWDBwr_PreProcessAllocationData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_TWDBwr_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv.
- **3_TWDBwr_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_TWDBwr_PreProcessAllocationData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Input: 
- TWDB_Groundwater.csv

#### Outputs:
 - Pwr_twdbMain.zip
 - P_Geometry.zip

#### Operation and Steps:
Using Jupyter Notebook in Python(which is what this is written in and with) is a simple way to run this operation.
- Read in the input file. Create temporary POD dataframes.
- For POD CombinedPOD_Points.csv, set WaDE field PODorPOUSite = POD.
- Generate WaDE specific field WaterSourceTypeC from NVDWR source field (see preprocess code for specific dictionary used).
- Generate WaDE specific field SiteName from NVDWR site_name field (see preprocess code for specific dictionary used).
- Generate WaDE specific field SiteTypeCV from NVDWR source field (see preprocess code for specific dictionary used).
- Generate WaDE specific field SiteNativeID from WaDE Latitude, Longitude, SiteTypeCV & SiteName fields. Used to identify unique sites.
- Generate WaDE specific field WaterSourceNativeID from WaDE WaterSourceName & WaterSourceTypeCV fields. Used to identify unique sources of water.
- Format prior_dt field to %m/%d/%Y format.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, P_Geometry.zip.


***
## Code File: 2_TWDBwr_CreateWaDEInputFiles.ipynb
Purpose: generate WaDE csv input files (methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv).

#### Inputs:
- Pwr_twdbMain.zip

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
- Assign agency info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodName | MethodNEMILink | MethodTypeCV | WaDEDataMappingURL
---------- | ---------- | ------------ | ------------ | ------------ | ------------
TWDBwr_M1 | Groundwater | TWDB Groundwater Database | https://www.twdb.texas.gov/groundwater/data/gwdbrpt.asp | Legal Processes | https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Texas/WaterAllocation_TWDB


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
VariableSpecificUUID | AggregationInterval | AggregationIntervalUnitCV | AggregationStatisticCV | AmountUnitCV | VariableCV | VariableSpecificCV 
---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------
TWDBwr_V1 | WaDE Unspecified | Year | WaDE Unspecified | WaDE Unspecified | Allocation | Allocation


## 3) Organization Information
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign agency info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite | State
---------- | ---------- | ------------ | ------------ | ------------
TWDBwr_O1 | Texas Water Development Board | Bill Billingsley | https://www.twdb.texas.gov/index.asp | TX 


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Break apart AquiferCod entries at Hyphen to get site name and NativeID.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency info to the *WaDE WaterSources* specific columns.  See *TWDBwr_Allocation Schema Mapping_WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceUUID* = ""TWDBwr_WS" + counter"
    - *WaterQualityIndicatorCV* = ""
    - *WaterSourceName* = "Before Hyphen section in AquiferCod"
    - *WaterSourceNativeID* = "After Hyphen section in AquiferCod"
    - *WaterSourceTypeCV* = "Groundwater"
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
TXwr_WS100ALVM | Fresh | Alluvium| 100ALVM | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


## 5) Site Information
Purpose: generate a list of sites information.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign agency info to the *WaDE Site* specific columns.  See *TWDBwr_Allocation Schema Mapping_WaDE.xlsx* for specific details.  Items of note are as follows...
    - *SiteUUID* = ""TWDBwr_S" + counter 
    - *WaterSourceUUIDs* = Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - *CoordinateAccuracy* = ""
    - *CoordinateMethodCV* = "Digitized"
    - *County* = "CountyName"
    - *EPSGCodeCV* = "4326"
    - *Geometry* = ""
    - *GNISCodeCV* = ""
    - *HUC12* = ""
    - *HUC8* = ""
    - *Latitude* = "CoordDDLat"
    - *Longitude* = "CoordDDLon"
    - *NHDNetworkStatusCV* = ""
    - *NHDProductCV* = ""
    - *PODorPOUSite* = "POD"
    - *SiteName* = ""
    - *SiteNativeID* = "StateWellN"
    - *SiteTypeCV* = "WellType"
    - *StateCV* = "TX"																			
    - *USGSSiteID* = ""
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | County | Latitude | Longitude | PODorPOUSite| SiteName | SiteNativeID | SiteTypeCV
---------- | ---------- | ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------
TXwr_SPOD1001201 | TXwr_WS121OGDK | Digitized | Deaf Smith | 34.973333 | -102.948334 | POD | WaDE Blank | POD1001201 | Withdrawal of Water

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
- Assign agency info to the *WaDE Water Allocations* specific columns.  See *TWDBwr_Allocation Schema Mapping_WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationApplicationDate* = ""
    - *AllocationAssociatedConsumptiveUseSiteIDs* = ""
    - *AllocationAssociatedWithdrawalSiteIDs* = ""
    - *AllocationBasisCV* = ""
    - *AllocationChangeApplicationIndicator* = ""
    - *AllocationCommunityWaterSupplySystem* = ""
    - *AllocationCropDutyAmount* = ""
    - *AllocationExpirationDate* = ""
    - *AllocationFlow_CFS* = ""
    - *AllocationLegalStatusCV* = ""
    - *AllocationNativeID* = "StateWellN"
    - *AllocationOwner* =  "OwnerName"
    - *AllocationPriorityDate* = ""
    - *AllocationSDWISIdentifierCV* = ""
    - *AllocationTimeframeEnd* = ""
    - *AllocationTimeframeStart* = ""
    - *AllocationTypeCV* = "Rules of Capture"
    - *AllocationVolume_AF* = ""
    - *BeneficialUseCategory* = "PrimaryWat"
    - *CommunityWaterSupplySystem* = ""
    - *CropTypeCV* = ""
    - *CustomerTypeCV* = ""
    - *DataPublicationDate* = "2023/7/25"
    - *DataPublicationDOI* = ""
    - *ExemptOfVolumeFlowPriority* = "1"
    - *GeneratedPowerCapacityMW* = ""
    - *IrrigatedAcreage* = ""
    - *IrrigationMethodCV* = ""
    - *LegacyAllocationIDs* = ""
    - *OwnerClassificationCV* = ""
    - *PopulationServed* = ""
    - *PowerType* = ""
    - *PrimaryBeneficialUseCategory* = ""
    - *WaterAllocationNativeURL* = "https://www3.twdb.texas.gov/apps/waterdatainteractive//GetReports.aspx?Num=" + **StateWellN** input + "&"Type=GWDB																							
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
|    | AllocationUUID   | MethodUUID   | OrganizationUUID   | SiteUUID           | VariableSpecificUUID   | AllocationApplicationDate   | AllocationAssociatedConsumptiveUseSiteIDs   | AllocationAssociatedWithdrawalSiteIDs   | AllocationBasisCV   | AllocationChangeApplicationIndicator   | AllocationCommunityWaterSupplySystem   | AllocationCropDutyAmount   | AllocationExpirationDate   |   AllocationFlow_CFS | AllocationLegalStatusCV   |   AllocationNativeID | AllocationOwner         | AllocationPriorityDate   | AllocationSDWISIdentifierCV   | AllocationTimeframeEnd   | AllocationTimeframeStart   | AllocationTypeCV   |   AllocationVolume_AF | BeneficialUseCategory   | CommunityWaterSupplySystem   | CropTypeCV   | CustomerTypeCV   | DataPublicationDate   | DataPublicationDOI   |   ExemptOfVolumeFlowPriority | GeneratedPowerCapacityMW   |   IrrigatedAcreage | IrrigationMethodCV   | LegacyAllocationIDs   | OwnerClassificationCV   | PopulationServed   | PowerType   | PrimaryBeneficialUseCategory   | WaterAllocationNativeURL                                                                     |
|---:|:-----------------|:-------------|:-------------------|:-------------------|:-----------------------|:----------------------------|:--------------------------------------------|:----------------------------------------|:--------------------|:---------------------------------------|:---------------------------------------|:---------------------------|:---------------------------|---------------------:|:--------------------------|---------------------:|:------------------------|:-------------------------|:------------------------------|:-------------------------|:---------------------------|:-------------------|----------------------:|:------------------------|:-----------------------------|:-------------|:-----------------|:----------------------|:---------------------|-----------------------------:|:---------------------------|-------------------:|:---------------------|:----------------------|:------------------------|:-------------------|:------------|:-------------------------------|:---------------------------------------------------------------------------------------------|
|  0 | TWDBwr_WR1001201 | TWDBwr_M1    | TWDBwr_O1          | TWDBwr_SPOD1001201 | TWDBwr_V1              |                             |                                             |                                         | WaDE Blank          |                                        |                                        |                            |                            |                    0 | WaDE Blank                |              1001201 | Charlie Hale Bob Ridley |                          |                               |                          |                            | Rules of Capture   |                     0 | Stock                   |                              |              |                  | 04/10/2024            |                      |                            1 |                            |                  0 |                      |                       | Private                 |                    |             | Livestock                      | https://www3.twdb.texas.gov/apps/waterdatainteractive//GetReports.aspx?Num=1001201&Type=GWDB |

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
Notes: podsitetopousiterelationships.csv output only needed if both POD and POU data is present, ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `otherwise produces empty file.`,
       Only have POD information so not applicable. 

#### Operation and Steps:
- Read the sites.csv & waterallocations.csv input files.
- Create three temporary dataframes: one for waterallocations, & two for site info that will store POD and POU data separately.
- For the temporary POD dataframe...
  - Read in site.csv data from sites.csv with a _PODSiteUUID_ field = POD only.
  - Create _PODSiteUUID_ field = _SiteUUID_.
- For the temporary waterallocations dataframe, explode _SiteUUID_ field to create unique rows.
- Left-merge POD dataframe to the waterallocations dataframe via _SiteUUID_ field.
- Consolidate waterallocations dataframe by grouping entries by _AllocationNativeID_ filed.
- Explode the consolidated waterallocations dataframe again using the _PODSiteUUID_ field to create unique rows.
- Perform error check on waterallocations dataframe (check for NaN values)
- If waterallocations is not empty, export output dataframe *podsitetopousiterelationships.csv*.


***
## Source Data & WaDE Complied Data Assessment
The following info is from a data assessment evaluation of the completed data...

Dataset | Num of Source Entries (rows)
---------- | ---------- 
**GroundWater Rights**| 141,605


Dataset  | Num of Identified PODs | Num of Identified POUs | Num of Identified Water Right Records
---------- | ------------ | ------------ | ------------
**Compiled WaDE Data** | 141,605 | 0 | 141,605


Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
Nothing removed | - | -


**Figure 1:** Distribution of POD vs POU Sites within the sites.csv
![](figures/PODorPOUSite.png)

**Figure 2:** Distribution Sites by WaterSourceTypeCV within the sites.csv
![](figures/WaterSourceTypeCV.png)

**Figure 3:** Distribution of Identified Water Right Records by WaDE Categorized Primary Beneficial Uses within the waterallocations.csv
![](figures/PrimaryBeneficialUseCategory.png)

**Figure 4a:** Range of Priority Date of Identified Water Right Records within the waterallocations.csv
<!-- ![](figures/AllocationPriorityDate1.png) -->
- no priority date data

**Figure 4b:** Cumulative distribution of Priority Date of Identified Water Right Records within the waterallocations.csv
<!-- ![](figures/AllocationPriorityDate2.png) -->
- no priority date data

**Figure 5:** Distribution & Range of Flow (CFS) of Identified Water Right Records within the waterallocations.csv
<!-- ![](figures/AllocationFlow_CFS.png) -->
- No Flow (CFS) value provided.

**Figure 6:** Distribution & Range of Volume (AF) of Identified Water Right Records within the waterallocations.csv
<!-- ![](figures/AllocationVolume_AF.png) -->
- No Volume (AF) value provided.

**Figure 7:** Map of Identified Points within the sites.csv
![](figures/PointMap.png)

**Figure 8:** Map of Identified Polygons within the sites.csv
<!-- ![](figures/PolyMap.png) -->
- no POU data


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Texas Water Development Board (TWDB)](https://www.twdb.texas.gov/index.asp).

WSWC Staff
- Adel Abdallah (Project Manager) <adelabdallah@wswc.utah.gov>
- Ryan James (Data Analysis) <rjames@wswc.utah.gov>

Texas Water Development Board Staff
- Bill Billingsley <bill.billingsley@twdb.texas.gov>
  