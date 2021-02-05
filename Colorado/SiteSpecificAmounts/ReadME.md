# (work in progress) CODWR Site Specific Water Data Preparation for WaDE
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to extracting water rights data made available by the [Colorado Division of Water Resources (CODWR)](https://dwr.colorado.gov/), for inclusion into the Water Data Exchange (WaDE) project.  WaDE enables states to share data with each other and the public in a more streamlined and consistent way. WaDE is not intended to replace the states data or become the source for that data but rather to enable regional analysis to inform policy decisions and for planning purposes.


## Overview of Data Utilized
The following data was used for water allocations...

- Monthly time seres data available at teh Colorado [CDSS REST Web Services](https://dwr.state.co.us/rest/get/help#Datasets&#DiversionRecordsController&#gettingstarted&#jsonxml).
- DWR Administrative structure information [link](https://data.colorado.gov/api/views/vz77-kxck/rows.csv?accessType=DOWNLOAD&bom=true&format=true.)


Number of records in the DWR Administrative Structures file that meeting the following.
- Are considered Active
- Possess location information (lat & long)
- Possess a **POR Start** & **POR End** date.

Structure Type | Number of Records
---------- | ----------
WELL | 24227
DITCH | 16389
RESERVOIR | 4221
SPRING | 3314
PUMP | 1880
PIPELINE | 943
REACH | 916
RECHARGE AREA | 740
AUGMENTATION/REPLACEMENT PLAN | 622
OTHER | 453
MEASURING POINT | 399
WELL FIELD | 229
WELL GROUP | 119
MINIMUM FLOW | 76
SEEP | 48
REACH (AGGREGATING) | 46
POWER PLANT | 38
RESERVOIR SYSTEM | 35
STREAM GAGE | 31
MINE | 25
DITCH SYSTEM | 3
EXCHANGE PLAN | 2
LIVESTOCK WATER TANK | 1

