# UDWRi Water Rights (Allocation) Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Utah Division of Water Rights (UDWRi)](https://waterrights.utah.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes. 


## Overview of Source Data Utilized
The following data was used for water allocations...

Name | Description | Download Link | Metadata Glossary Link
---------- | ---------- | ------------ | ------------
**Utah Points of Diversion** | POD site data for surface and groundwater sites. | [link](https://opendata.gis.utah.gov/datasets/utahDNR::utah-points-of-diversion/explore?location=39.485303%2C-111.591274%2C-1.00) | [link](https://www.arcgis.com/sharing/rest/content/items/5d530e62e6ca42528dd13e0a453a3b73/info/metadata/metadata.xml?format=default&output=html)
**Utah Place of Use Irrigation** | POU area data. | [link](https://opendata.gis.utah.gov/datasets/utahDNR::utah-place-of-use-irrigation/explore?location=39.471338%2C-111.581749%2C-1.00) | [link](https://www.arcgis.com/sharing/rest/content/items/03919b7306544f8aa69fe09c42fbf76f/info/metadata/metadata.xml?format=default&output=html)


Unique files were created to be used as input.  Input files used are as follows...
- PointsOfDiversion_input.zip.  Contains POD data.
- PlaceOfUseService_input.zip.  Contains POU data.

## Storage for WaDE 2.0 Source and Processed Water Data
The 1) raw input data shared by the state / state agency / data provider (excel, csv, shapefiles, PDF, etc), & the 2) csv processed input data ready to load into the WaDE database, can both be found within the WaDE sponsored Google Drive.  Please contact WaDE staff if unavailable or if you have any questions about the data.
- Utah Allocation Data: https://drive.google.com/drive/folders/1-7c1zFWiz_KISKEOFEaiq1DRaJ5BuAn0?usp=sharing


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *UTwr_Allocation Schema Mapping to WaDE.xlsx*.  Several WaDE csv input files will be created in order to extract the water rights data from the above mentioned input.  Each of these WaDE csv input files was created using the [Python](https://www.python.org/) native language, built and ran within [Jupyter Notebooks](https://jupyter.org/) environment.  Those python files include the following...

- **1_UTwr_PreProcessAllocationData.ipynb**: used to pre-processes the native date into a WaDE format friendly format.  All datatype conversions occur here.
- **2_UTwr_CreateWaDEInputFiles.ipynb**: used to create the WaDE input csv files: methods.csv, variables.csv, organizations.csv, watersources.csv, sites.csv, waterallocations.csv, podsitetopousiterelationships.csv.
- **3_UTwr_WaDEDataAssessmentScript.ipynb**: used to evaluate the WaDE input csv files.


***
## Code File: 1_UTwr_PreProcessAllocationData.ipynb
Purpose: Pre-process the input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- PointsOfDiversion_input.zip.  Contains POD data.
- PlaceOfUseService_input.zip.  Contains POU data.

#### Outputs:
 - Pwr_utMain.zip
 - P_Geometry.zip


#### Operation and Steps:
- Read the input files and generate temporary input dataframes for both POD and POU water right data.  Goal will be to create two separate clean tables and concatenate to single output table.
- POD and POU data share similar field and columns names.
- Perform the following additional actions on the POD data...
    - remove all **CHEXUM** rows & related data.  These indicate the wr is undergoing to change order and is in review.
    - remove white space from **WRNUM** field.
    - Translate abbreviated **USES** field to full terminology using provided list.
- Perform the following additional actions on the POU data...
    - Split and explode data on **WRNUMS** field, need info to be broken out into water right information.
    - remove white space from **WRNUM** field.
- Concatenate POD and POU data into single output dataframe.
- Remove special characters from owner field.
- Change / double check data type for **CFS**, **ACFT**, **ACRES**, **PRIORITY** fields.
- Create WaDE *LegalStatusCV* field (see custom dictionary) using **STATUS** field (mostly cleaning input text).  For UT, we don't want water rights that are considered: Rejected, Disallowed, Withdrawn, Temp Applications, Unapproved, Forfeited, Lapsed, Expired, Terminated
- Generate WaDE specific field *WaterSourceNativeID* from WaDE *WaterSourceTypeCV* fields.  Used to identify unique sources of water.
- Extract geometry values POU shapefile, merge to records using **RECORD_ID** field.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe(s) as new csv file, *Pwr_utMain.zip*, *P_Geometry.zip*.


***
## Code File: 2_UTwr_CreateWaDEInputFiles.ipynb
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
- Assign agency info to the *WaDE Method* specific columns (this was hardcoded by hand for simplicity).
- Assign method UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
MethodUUID | ApplicableResourceTypeCV | MethodTypeCV
---------- | ---------- | ------------
UTwr_M1 | Surface Ground | Adjudicated


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
UTwr_V1 | 1 | Year | CFS


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
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
UTwr_O1 | Utah Division of Water Rights | Craig Miller |"https://water.utah.gov/"


## 4) Water Source Information
Purpose: generate a list of water sources specific to a water right.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE WaterSources* specific columns.
- Assign agency info to the *WaDE WaterSources* specific columns.  See *UTwr_Allocation Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - *WaterSourceName* = "".
    - *WaterSourceNativeID* = *in_WaterSourceNativeID*, see *1_UTwr_PreProcessAllocationData.ipynb* for specifics.
    - *WaterSourceTypeCV* = **SOURCE** input.
- Consolidate output dataframe into water source specific information only by dropping duplicate entries, drop by WaDE specific *WaterSourceName* & *WaterSourceTypeCV* fields.
- Assign water source UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *WaterSources.csv*.

#### Sample Output (WARNING: not all fields shown):
WaterSourceUUID | WaterQualityIndicatorCV | WaterSourceName | WaterSourceNativeID | WaterSourceTypeCV
---------- | ---------- | ------------ | ------------ | ------------
UTwr_WS1 | Fresh | WaDE Unspecified | WaDEUT_WS1 | Groundwater

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *watersources_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water sources include the following...
- WaterSourceUUID
- WaterQualityIndicatorCV
- WaterSourceTypeCV


## 5) Site Information
Purpose: generate a list of sites information.

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Site* specific columns.
- Assign agency info to the *WaDE Site* specific columns.  See *UTwr_Allocation Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *WaterSourceUUID* from waterSources.csv input csv file. See code for specific implementation of extraction.
    - *Geometry* = extracted from POU shapefile, see *1_UTwr_PreProcessAllocationData.ipynb* for specifics.
    - *Latitude* = **Latitude**.
    - *Longitude* = **Longitude**.
    - *SiteNativeID* = **OBJECTID** for POD data, and **RECORD_ID** for POU data.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *SiteNativeID*, *SiteName*, *SiteTypeCV*, *Longitude* & *Latitude* fields.
- Assign site UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
SiteUUID | WaterSourceUUID | CoordinateMethodCV | Latitude | Longitude | SiteName
---------- | ---------- | ---------- | ------------ | ------------ | ------------
UTwr_S1 | UTwr_WS1| Unspecified | 38.6227946 | -109.401786199999 | Non-Production Well: Test

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
- Assign agency info to the *WaDE Water Allocations* specific columns.  See *UTwr_Allocation Schema Mapping to WaDE.xlsx* for specific details.  Items of note are as follows...
    - Extract *MethodUUID*, *VariableSpecificUUID*, *OrganizationUUID*, & *SiteUUID* from respective input csv files. See code for specific implementation of extraction.
    - *AllocationFlow_CFS* = **CFS**.
    - *AllocationVolume_AF* = **ACFT**.
    - *AllocationLegalStatusCV* = *in_LegalStatus*, see *1_UTwr_PreProcessAllocationData.ipynb* for specifics. 
    - *AllocationNativeID* = **WRNUM**.
    - *AllocationOwner* =  **OWNER**.
    - *AllocationPriorityDate* = **PRIORITY**.
    - *IrrigatedAcreage* = **ACRES**.
    - *BeneficialUseCategory* = **USES**.   
    - *WaterAllocationNativeURL* = **WebLink**.
- Consolidate output dataframe into water allocations specific information only by grouping entries by *AllocationNativeID* filed.
- Perform error check on output dataframe.
- Export output dataframe *waterallocations.csv*.

#### Sample Output (WARNING: not all fields shown):
AllocationNativeID | AllocationFlow_CFS | AllocationLegalStatusCV | BeneficialUseCategory
---------- | ---------- | ------------ | ------------
01-1000 | 0 | Diligence Claim | Other, Stockwatering

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
**Utah_Points_of_Diversion** | 382,049 | N/A | N/A | N/A
**Utah_Place_of_Use_Irrigation** | 76,449 | N/A | N/A | N/A
**Compiled WaDE Data** | N/A | 220,029 | 56,888 | 150,745

Assessment of Removed Source Records | Count | Action
---------- | ---------- | ----------
Incomplete or bad entry for Latitude | 1 | Removed from WaDE

**Figure 1:** Distribution of POD vs POU Sites within the sites.csv
![](figures/PODorPOUSite.png)

**Figure 2:** Distribution Sites by WaterSourceTypeCV within the sites.csv
![](figures/WaterSourceTypeCV.png)

**Figure 3:** Distribution of Identified Water Right Records by WaDE Categorized Primary Beneficial Uses within the waterallocations.csv
![](figures/PrimaryBeneficialUseCategory.png)

**Figure 4:** Range of Priority Date of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationPriorityDate.png)

**Figure 5:** Distribution & Range of Flow (CFS) of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationFlow_CFS.png)

**Figure 6:** Distribution & Range of Volume (AF) of Identified Water Right Records within the waterallocations.csv
![](figures/AllocationVolume_AF.png)

**Figure 7:** Map of Identified Points within the sites.csv
![](figures/PointMap.png)

**Figure 8:** Map of Identified Polygons within the sites.csv
![](figures/PolyMap.png)


***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [Utah Division of Water Rights (UDWRi)](https://waterrights.utah.gov//).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

UDWRi Staff
- Jim Reese <jreese@utah.gov>
