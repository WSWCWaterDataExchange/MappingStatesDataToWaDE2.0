# WaDE Preperation

This readme details an overview, the specific steps taken, and the final product of the process applied to water use data submitted by the [Wyoming Water Development Office (WWDO)](http://wwdc.state.wy.us) for inclusion into the Water Data Exchange (WaDE). 

## Overview 
For inclusion into WaDE, WWDO submitted a state-wide Point-of-Diversion (POD) water use dataset.  A POD is the geographical location where water is diverted from a source, a stream for example, and point to some beneficial use.  It is at this point that POD transitions to Point of Use (POU).  While a water right may have any number of POUs or PODs, WWDO has restricted water rights to having a single POD.  This organizational method thus provides a 1-to-1 relationship between an adjudicated water right and an additional stress on the statewide watershed.  A number of details are included in a water right, these include:
  * water right priority date
  * water right owner
  * beneficial uses
  * etc 
 
 A sample of WWDO POD data is included in Table 1.  Note that names and location have been changed for legal reasons.
 
 Table 1.
 
 PermitNumber | OrderRecord | WRNumber | PriorityDate | SummaryWRStatus | Company | Uses | TotalFlow(CFS) | StreamSource
 ------------ | ----------- | -------- | ------------ | --------------- | ------- | ---- | -------------- | -------------
 1001 | OR 01/123 | CR CC12/345 | 01/14/1886 | FullyAdjudicated | John Doe Irrigation | IRR_SW, STO, FIS| 71.43 | Laramie River
 
 
This data is stored in [e-permit](http://seoweb.wyo.gov/e-Permit/common/login.aspx?ReturnUrl=%2fe-Permit%2f), an online portal maintained by the [Wyoming State Engineer's Office](https://sites.google.com/a/wyo.gov/seo/), and was prepared into a dataset by [need name]

## Data Prep
The overall objective of the data migration scripts are to prepare datasets retrieved from state repositories for upload into WaDE.  This process applied to Wyoming POD data, and considering the data included in this dataset involves passing the raw data through three scripts.  These scripts are outlined below.

Modules required: Dictionaries_WY.py
###  1. sites_WY.py - generate list of sites where water is allocated
        - generate empty sites.csv file with controlled vocabulary headers
        - call Dictionaries_WY.py and determine diversion infrastructure (work) type
        - generate SiteNativeID (Wyoming POD data does not include native ID)
        - generate WaDESiteUUID from generated SiteNativeID
        - drop data if missing lat/lon
        - copy results into sites.csv and export 
        
   Sample data (all columns not included):
   
   WaDESiteUUID | SiteNativeID | SiteName | SiteTypeCV | Long | Lat
   ------------ | ------------ | -------- | ---------- | ---- | ----
   WWDO_100001 | 1000001 | PIONEER CANAL | Ditch | -105 | -40 |
   
   Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**sites_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data.
   Mandatory fields include:
    - SiteUUID
    - SiteName
    - CoordinateMethodCV
    - EPSGCodeCV
     
###  2. watersources_WY.py - generate list of water sources from which water is allocated from 
        - generate empty watersources.csv file with controlled vocabulary headers
        - generate WaterSourceNativeID (Wyoming POD data does not include native ID)
        - generate WaterSourceUUID from generate WaterSourceNativeID
        - drop data if missing WaterSourceUUID, WaterSourceType, AND WaterQualityIndicator
        - copy results into watersources.csv and export
        
   Sample data (all columns not included):
   
   WaterSourceUUID | WaterSourceID | WaterSource | WaterSourceTypeCV | WaterQualityIndicatorCV
   ------------ | ------------ | -------- | ---------- | ---- 
   WWDO_1 | 1 | LARAMIE RIVER  | Unknown | Unspecified 
   
   Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**watersources_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data.
   Mandatory fields include:
    - WaterSourceUUID
    - WaterSourceTypeCV
    - WaterQualityIndicatorCV
        
###  3. waterallocations_WY.py - generate master sheet of water allocations to import into WaDE
        - generate empty waterallocations.csv file with controlled vocabulary headers
        - call sites.csv and assign WaDE prepared sites to water right 
        - call Dictionaries_WY.py and assign defined benefical uses to water right 
        - call watersources.csv and assign WaDE prepared water sources to water right
        - assign AllocationOwner based on Company OR FirstName/LastName
        - copy data to waterallocation.csv
        - drop data if AllocationAmount AND AllocationMaximum are null
        - export to csv
        
  Sample data (all columns not included):
   
   OrganizationUUID | SiteUUID | WaterSourceUUID | BeneficialUseID | NativeAllocationID | AllocationOwner | AllocationLegalStatus | AllocationAmount | 
   ---------------- | ------------ | -------- | ---------- | ----------- | ---------- | ----------- | --------- 
   WWDO | WWDO_100001 | WWDO_1 | IRRIGATION | CR CC48/006 | JOHN DOE IRRIGATION | FullyAdjudicated | 71.43


Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**waterallocations_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data.
 Mandatory fields include:
    - OrganizationUUID
    - VariableSpecificUUID
    - WaterSourceUUID
    - MethodUUID
    - Allocation Priority Date

###  4. variable_WY.py - generate legend of granular variables specific to each state
        - all values are hard-coded according to state
        
  Sample data 
  
  VariableSpecificUUID | VariableSpecificCV | VariableCV | AggregationStatisticCV | AggregationInterval | AggregationIntervalUnitCV | ReportYearStartMonth | ReportYearTypeCV | AmountUnitCV
  -------------------- | ------------------ | ---------- | ---------------------- | ------------------- | ------------------------ | ----------------- | ---------------- | ---------
 
Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file         (**variables_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data.
 Mandatory fields include:
    - VariableSpecificUUID
    - VariableSpecificCV
    - AggregationStatisticCV
    - AggregationInterval
    - AggregationIntervalUnitCV
    - ReportYearStartMonth
    - ReportYearTypeCV
    - AmountUnitCV
  
###  5. methods_WY.py - generatte legend of granular variables specific to each state detailing water right/allocation/etc data collection. 
        - all values are hard-coded according to state
        
  Sample data 

  MethodUUID | MethodName | MethodDescription | MethodNEMILink | ApplicableResourceTypeCV | MethodTypeCV | DataCoverageValue | DataQualityValueCV | DataConfidenceValue
  ---------- | ---------- | ----------------- | -------------- | ------------------------ | ------------ | ----------------- | ------------------ | -------------------
  
  
Any data missing required values and dropped from the WaDE-ready dataset are saved in a csv file (**methods_mandatoryFieldMissing.csv**) to be passed back to the organization supplying the data. 
 Mandatory fields include:
    - MethodUUID
    - MethodName
    - MethodDescription
    - ApplicableResourceTypeCV
    - MethodTypeCV
        
        
        
        
        
        
