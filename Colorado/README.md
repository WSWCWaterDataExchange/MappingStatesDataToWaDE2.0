# WaDE Preparation

This readme details an overview, the specific steps taken, and the final product of the process applied to water rights data made available by the [Colorado Department of Water Rights (UTDWR)](https://cdnr.us/#/division/DWR) for inclusion into the Water Data Exchange (WaDE). 

### Overview 
The Colorado Department of Water Rights hosts its water right data at the [Colorado Information Marketplace](https://data.colorado.gov/Water/DWR-Water-Right-Net-Amounts/acsg-f33s).
The dataset is updated annually. For more information on WaDE, please visit http://wade.westernstateswater.org/


### Summary
This document summarizes the process to prepare and share CODWR’s Water Rights data from the Colorado Information Marketplace database for inclusion in the Western States Water Council’s Water Data Exchange (WaDE 2.0). In order to extract Colorado's water rights data and publish it online through ESRI layers to be ready for WaDE 2.0, you must execute 8 Python Scripts to generate CSV data compatible with WaDE 2.0.

 ## Data Prep
 ### Step 1: Execute 8 Python Scripts to generate CSV data compatible with WaDE 2.0

There are 8 Python Scripts that use queries to extract CODWR’s water rights data into views compatible with WaDE 2.0. Two of the scripts, **beneficialuseDictionary.py** and **waterallocationsFunctions.py**, are required as input scripts for **watersources_Ut.py** and **waterallocations_UT.py**, respectively.  All scripts can be found at the following link in WaDE’s Github repository “MappingStatesDataToWaDE2.0” in the Colorado folder:
https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Colorado
