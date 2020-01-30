# WaDE Preparation

This repository stores code and data for California water allocations data made available by the [California State Water Resources Control Board (CSWRCB) eWRIMS – Electronic Water Rights Information Management System](https://www.waterboards.ca.gov/waterrights/water_issues/programs/ewrims/) and water use data made available by the [California Department of Water Resources (CDWR)](https://data.ca.gov/dataset/water-plan-water-balance-data) for inclusion into the Water Data Exchange version 2 (WaDE 2). For more information on WaDE, please visit http://wade.westernstateswater.org/

### Overview 
The WaDE 2 organizes data into four specific groups: 

**1. AggregatedAmounts**

**2. Regulatory**

**3. SiteSpecificAmounts**

**4. WaterAllocation**

The data and code for preparation of each group of inputs to WaDE are put into these four directories. 

# Structure
Each folder is for a unique data type that the state shares into WaDE 2.0. It contains 
1) the raw input data shared by the state (excel, csv, shapefiles,PDF, etc)
2) the processed input data into CSV files ready to load into WaDE database
3) the python scripts that process the raw input files and prepare the CSV files   

