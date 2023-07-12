# NMOSE Reguloatory Overview Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting New Mexico regulatory overlay area data, made available by the [New Mexico Office of the State Engineer (NMOSE)](http://geospatialdata-ose.opendata.arcgis.com/datasets/ose-points-of-diversion), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and cost-effective way.


## Overview of Data Utilized
The following data was used for regulatory overlay area data...
- **Interstate Stream Compact Regions**.  Compacts are formal agreement between states concerning the use of water in rivers or streams, which flow across state boundaries. https://www.ose.state.nm.us/ISC/isc_compacts.php
- **OSE Water Right District Boundary**.  The Water Rights Division's District Offices that administer surface water and groundwater rights within New Mexico and process water rights applications. https://ose.maps.arcgis.com/home/item.html?id=22b6dcc154224d44a20e095542dc14ec
- **Special Conditions Water Right**.  Certain areas within New Mexico might contain restrictions that prohibit the drilling of wells within a basin in order to protect public health, water quality, existing water rights, or protect the state's water resources. https://ose.maps.arcgis.com/home/item.html?id=5617df05c3de4ac8b59594bd51cbab94.

Six unique files were created to be used as input.  Input files used are as follows...
- *InterstateStreamCompactRegions_input.csv*.  Contains tabular regulatory data for stream compacts.
- *NMInterstateStreamCompactRegions.shp*.  Shapefile for stream compat data.
- *OSEWaterRightDistrictBoundary_input.csv*.  Contains tabular regulatory data for state enginer water right districts.
- *OSEDistrictBoundary.shp*.  Shapefile for water right districts.
- *SpecialConditionsWaterRight_input.csv.*  Contains tabular special interest regulatory data for state enginer water right districts.
- *WaterRightRegulations.shp*.  Shapefile for special interest water right areas.


## Summary of Data Prep
The following text summarizes the process used by the WSWC staff to prepare and share NMOSE's water rights data for inclusion into the Water Data Exchange (WaDE 2.0) project.  For a complete mapping outline, see *[NM_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/NewMexico/Regulatory/NM_RegulatoryInfo%20Schema%20Mapping%20to%20WaDE_QA.xlsx)*.  Six executable code files were used to extract the NMOSE's water rights data from the above mentioned input files.  Each code file is numbered for order of operation.  The first code file (pre-process) was built and ran within [Jupyter Notebooks](https://jupyter.org/), the remaining four code files were built and operated within [Pycharm Community](https://www.jetbrains.com/pycharm/). The last code file _(RegulatoryReportingUnits_fact)_ is depended on the previous files.  Those Six code files are as follows...

- 0_NMRegulatorySourceDataPreprocess.ipynb
- 1_NMre_Date.py
- 2_NMre_Organizations.py
- 3_NMre_ReportingUnits.py
- 4_NMre_RegulatoryOverlay.py
- 5_NMre_RegulatoryReportingUnits_fact.py



***
### 0) Code File: 0_NMRegulatorySourceDataPreprocess.ipynb
Purpose: Pre-process the state agency input data files and merge them into one master file for simple dataframe creation and extraction.

#### Inputs: 
- InterstateStreamCompactRegions_input.csv
- NMInterstateStreamCompactRegions.shp
- OSEWaterRightDistrictBoundary_input.csv
- OSEDistrictBoundary.shp
- SpecialConditionsWaterRight_input.csv.
- WaterRightRegulations.shp

#### Outputs:
 - P_nmRegMaster.csv
 - P_nmRegGeometry.csv

#### Operation and Steps:
- For tabular regulatory information, read the input files and generate temporary input dataframes for Interstate Stream Compact Regions, OSE Water Right District Boundary, and Special Conditions Water Right Areas.
- Perform the following additional actions on the Interstate Stream Compact Regions tabular data...
    - *in_ReportingUnitName* = **Full_Name**
    - *in_ReportingUnitNativeID* = **OID_**
    - *in_ReportingUnitTypeCV* = "Interstate River Compact"
    - *in_OversightAgency* = **States**
    - *in_RegulatoryDescription& = **RegulatoryDescription**
    - *in_RegulatoryName* = **Full_Name**
    - *in_RegulatoryStatusCV* = "Active"
    - *in_RegulatoryStatute* = "Unspecified"
    - *in_RegulatoryStatuteLink* = **URL**
    - *in_StatutoryEffectiveDate* = **EffectiveDate**
    - *in_RegulatoryOverlayTypeCV* = "Interstate River Compact"
    - *in_WaterSourceTypeCV* = "Surface Water"
- Perform the following additional actions on the OSE Water Right District Boundary tabular data...
    - *in_ReportingUnitName* = **name**
    - *in_ReportingUnitNativeID* = **ose_dist_i**
    - *in_ReportingUnitTypeCV* = "Water Rights District"
    - *in_OversightAgency* = **name** + OSE
    - *in_RegulatoryDescription& = "District operated by a Water Master appointed by the Office of the State Engineer, who is charged with administering the state's water resources. The State Engineer has authority over the supervision, measurement, appropriation, and distribution of all surface and groundwater in New Mexico, including streams and rivers that cross state boundaries."
    - *in_RegulatoryName* = **name** + District
    - *in_RegulatoryStatusCV* = "Active"
    - *in_RegulatoryStatute* = "https://nmonesource.com/nmos/nmsa/en/item/4402/index.do#!fragment/zoupio-_Toc74832537/BQCwhgziBcwMYgK4DsDWszIQewE4BUBTADwBdoAvbRABwEtsBaAfX2zgHYAWADgGYATAFY+HAJQAaZNlKEIARUSFcAT2gBydRIiEwuBIuVrN23fpABlPKQBCagEoBRADKOAagEEAcgGFHE0jAAI2hSdjExIA"
    - *in_RegulatoryStatuteLink* = **URL**
    - *in_StatutoryEffectiveDate* = "08/12/2021"
    - *in_RegulatoryOverlayTypeCV* = "Water Rights District"
    - *in_WaterSourceTypeCV* = "Surface and Groundwater"
- Perform the following additional actions on the Special Conditions Water Right Areas tabular data...
    - *in_ReportingUnitName* = **Name**
    - *in_ReportingUnitNativeID* = **OID_**
    - *in_ReportingUnitTypeCV* = "Special Condition Water Right"
    - *in_OversightAgency* = **jurisdicti**
    - *in_RegulatoryDescription& = **requiremen**
    - *in_RegulatoryName* = **Name**
    - *in_RegulatoryStatusCV* = "Active"
    - *in_RegulatoryStatute* = "Unspecified"
    - *in_RegulatoryStatuteLink* = (leave blank)
    - *in_StatutoryEffectiveDate* = **effect_dat**
    - *in_RegulatoryOverlayTypeCV* = "Special Condition Water Right"
    - *in_WaterSourceTypeCV* = "Surface and Groundwater"
- Concatenate Interstate Stream Compact Regions, OSE Water Right District Boundary, and Special Conditions Water Right Areas tabular dataframes into single output dataframe.
- Generate WaDE specific field *in_RegulatoryOverlayNativeID* from WaDE *in_ReportingUnitName* fields.  Used to identify unique regulatory ovlary reporting areas.
- For shapefile information, read the input files and generate temporary input dataframes for Interstate Stream Compact Regions, OSE Water Right District Boundary, and Special Conditions Water Right Areas.
- Perform the following additional actions on the Interstate Stream Compact Regions shapefile data...
    - *in_ReportingUnitName* = **Full_Name**
    - *in_ReportingUnitTypeCV* = "Interstate River Compact"
    - *in_Geomerty* = **geometry**
- Perform the following additional actions on the Right District Boundary shapefile data...
    - *in_ReportingUnitName* = **name**
    - *in_ReportingUnitTypeCV* = "Water Rights District"
    - *in_Geomerty* = **geometry**
- Perform the following additional actions on the Special Conditions Water Right Areas shapefile data...
    - *in_ReportingUnitName* = **Name**
    - *in_ReportingUnitTypeCV* = "Special Condition Water Right"
    - *in_Geomerty* = **geometry**
- Concatenate Interstate Stream Compact Regions, OSE Water Right District Boundary, and Special Conditions Water Right Areas shapefile dataframes into single output dataframe.
- Inspect output dataframe for additional errors / datatypes.
- Export output dataframe as new csv file, *P_nmRegMaster.csv* for tabular data and *P_nmRegGeometry.csv* for geometry data.



***
### 1) Code File: 1_NMre_Date.py
Purpose: generate legend of granular methods used on data collection.

#### Inputs:
- None

#### Outputs:
- date.csv
- date_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Date* specific columns.
- Assign **NMOSE** info to the *WaDE Date* specific columns (this was hardcoded by hand for simplicity).
- Perform error check on output dataframe.
- Export output dataframe *methods.csv*.

#### Sample Output (WARNING: not all fields shown):
Date | Year 
---------- | ---------- 
8/12/2021 | 2021



***
### 2) Code File: 2_NMre_Organizations.py
Purpose: generate organization directory, including names, email addresses, and website hyperlinks for organization supplying data source.

#### Inputs:
- None

#### Outputs:
- organizations.csv
- organizations_missing.csv (error check only)

#### Operation and Steps:
- Generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Organizations* specific columns.
- Assign **NMOSE** info to the *WaDE Organizations* specific columns (this was hardcoded by hand for simplicity).
- Assign organization UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *organizations.csv*.

#### Sample Output (WARNING: not all fields shown):
OrganizationUUID | OrganizationName | OrganizationContactName | OrganizationWebsite
---------- | ---------- | ------------ | ------------
NMOSE | New Mexico Office of the State Engineer | David Hatchner (GIS Manager) | https://www.ose.state.nm.us/



***
### 3) Code File: 3_NMre_ReportingUnits.py
Purpose: generate a list of polygon areas associated with the state agency regulatory overlay area data.

#### Inputs:
- P_nmRegMaster.csv
- P_nmRegGeometry.csv

#### Outputs:
- reportingunits.csv
- reportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE ReportingUnits* specific columns.
- Assign state agency data info to the *WaDE ReportingUnits* specific columns.  See *NM_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *ReportingUnitName* = in_ReportingUnitName, see *0_NMRegulatorySourceDataPreprocess.ipynb.ipynb* for specifics.
    - *ReportingUnitNativeID* = in_ReportingUnitNativeID, see *0_NMRegulatorySourceDataPreprocess.ipynb.ipynb* for specifics.
    - *ReportingUnitTypeCV* = in_ReportingUnitTypeCV, see *0_NMRegulatorySourceDataPreprocess.ipynb.ipynb* for specifics.
    - *Geometry* = WKT created **Geometry**, see *0_NMRegulatorySourceDataPreprocess.ipynb.ipynb* for specifics.
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *sites.csv*.

#### Sample Output (WARNING: not all fields shown):
ReportingUnitUUID | ReportingUnitName | ReportingUnitTypeCV 
---------- | ---------- | ------------ 
NMre_RU1 | Costilla Creek Compact | Interstate River Compact

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *reportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the reportingunits include the following...
- ReportingUnitUUID
- ReportingUnitName
- ReportingUnitNativeID
- ReportingUnitTypeCV
- StateCV



***
### 4) Code File: 4_NMre_RegulatoryOverlay.py
Purpose: generate master sheet of regulatory overlay area information to import into WaDE 2.0.

#### Inputs:
- P_nmRegMaster.csv.csv

#### Outputs:
- regulatoryoverlays.csv
- regulatoryoverlays_missing.csv (error check only)

#### Operation and Steps:
- Read the input files and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Water Regulatory Overlays* specific columns.
- Assign state agency data info to the *WaDE Water Regulatory Overlays* specific columns.  See *NM_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - *OversightAgency* = in_OversightAgency, see *0_NMRegulatorySourceDataPreprocess.ipynb* for specifics.
    - *RegulatoryDescription* = in_RegulatoryDescription, see *0_NMRegulatorySourceDataPreprocess.ipynb* for specifics.
    - *RegulatoryName* = in_RegulatoryName, see *0_NMRegulatorySourceDataPreprocess.ipynb* for specifics.
    - *RegulatoryOverlayNativeID* = in_RegulatoryOverlayNativeID, see *0_NMRegulatorySourceDataPreprocess.ipynb* for specifics.
    - *RegulatoryStatusCV* = in_RegulatoryStatusCV, see *0_NMRegulatorySourceDataPreprocess.ipynb* for specifics.
    - *RegulatoryStatue* = "Unspecified".
    - *RegulatoryStatuteLink* = in_RegulatoryStatuteLink, see *0_NMRegulatorySourceDataPreprocess.ipynb* for specifics.
    - *StatutoryEffectiveDate* = in_StatutoryEffectiveDate, see *0_NMRegulatorySourceDataPreprocess.ipynb* for specifics.
    - *RegulatoryOverlayTypeCV* = in_RegulatoryOverlayTypeCV, see *0_NMRegulatorySourceDataPreprocess.ipynb* for specifics.
    - *WaterSourceTypeCV* = in_WaterSourceTypeCV, see *0_NMRegulatorySourceDataPreprocess.ipynb* for specifics. 
- Perform error check on output dataframe.
- Export output dataframe *regulatoryoverlays.csv*.

#### Sample Output (WARNING: not all fields shown):
RegulatoryOverlayUUID | OversightAgency | RegulatoryName | RegulatoryStatusCV | StatutoryEffectiveDate
---------- | ---------- | ------------ | ------------ | ------------
CDWR_Water Use | CO,NM | Costilla Creek Compact | Active | 1/1/1946 

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryoverlays_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the water regulatory overlays include the following...
- RegulatoryOverlayUUID
- OversightAgency
- RegulatoryDescription
- RegulatoryName
- RegulatoryStatusCV
- StatutoryEffectiveDate



***
### 5_NMre_RegulatoryReportingUnits_fact.py
Purpose: generate master sheet of regulatory overlay area information and how it algins with reporting unit area information.

#### Inputs:
- P_nmRegMaster.csv
- reportingunits.csv
- regulatoryoverlays.csv

#### Outputs:
- regulatoryreportingunits.csv
- regulatoryreportingunits_missing.csv (error check only)

#### Operation and Steps:
- Read the input file and generate single output dataframe *outdf*.
- Populate output dataframe with *WaDE Regulatory Reportingunits* specific columns.
- Assign state agency data info to the *WaDE Regulatory Reportingunits* specific columns.  See *NM_RegulatoryInfo Schema Mapping to WaDE_QA.xlsx* for specific details.  Items of note are as follows...
    - OrganizationUUID = "NMOSE"
    - *RegulatoryOverlayUUID* = extract from regulatoryoverlays.csv.  Match via in_RegulatoryName, see *0_NMRegulatorySourceDataPreprocess.ipynb.ipynb* for specifics.
    - *ReportingUnitUUID* = extract from reportingunits.csv.  Match via in_ReportingUnitName, see *0_NMRegulatorySourceDataPreprocess.ipynb.ipynb* for specifics. 
- Consolidate output dataframe into site specific information only by dropping duplicate entries, drop by WaDE specific *ReportingUnitName*, *ReportingUnitNativeID* & *ReportingUnitTypeCV* fields.
- Assign reportingunits UUID identifier to each (unique) row.
- Perform error check on output dataframe.
- Export output dataframe *regulatoryreportingunits.csv*.

#### Sample Output (WARNING: not all fields shown):
DataPublicationDate | OrganizationUUID | RegulatoryOverlayUUID | ReportingUnitUUID 
---------- | ---------- | ------------ | ------------ 
8/12/2021 | NMOSE | NMre_RO1 | NMre_RU1

Any data fields that are missing required values and dropped from the WaDE-ready dataset are instead saved in a separate csv file (e.g. *regulatoryreportingunits_missing.csv*) for review.  This allows for future inspection and ease of inspection on missing items.  Mandatory fields for the regulatory reportingunits include the following...
- DataPublicationDate
- OrganizationUUID
- RegulatoryOverlayUUID
- ReportingUnitUUID



***
## Staff Contributions
Data created here was a contribution between the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) and the [New Mexico Office of the State Engineer (NMOSE)](http://geospatialdata-ose.opendata.arcgis.com/datasets/ose-points-of-diversion).

WSWC Staff
- Adel Abdallah <adelabdallah@wswc.utah.gov>
- Ryan James <rjames@wswc.utah.gov>

NMOSE Staff
- David Hatchner (GIS Manager) <ose.webmaster@state.nm.us>
