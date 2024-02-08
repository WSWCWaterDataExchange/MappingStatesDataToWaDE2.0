# WaDE Preparation
This repository stores code and data for water data / informatoin made available by the state for inclusion into the [Water Data Exchange]( https://westernstateswater.org/wade/) (i.e., WaDE 2.0).

---
### Overview 
The WaDE 2 organizes data into specific types. **NOTE: all data types available for states at this time.**

**1. WaterAllocation**
-	In the western U.S., water rights (a.k.a., water allocation) are based on the prior appropriation doctrine “First in time, first in right.”  Each water right has an allocated amount of water (based on a volumetric quantity or a flow rate) with a designated beneficial use (e.g., agriculture) and sometimes multiple uses, which may come from one or many specified water sources.  

**2. Regulatory**
-	Regulatory boundaries related to water right administration or regulation purposes.

**3. AggregatedAmounts**
-	Aggregated water use, supply, and transfers may be estimated or calculated from user-reported data over-reporting units (i.e. water budgets).  A water resource agency’s water budget estimate is most often estimated annually with a one-year lag time.  Water budgets within a basin have historically been categorized by both withdrawals (i.e., how much water was taken from a stream, spring, or reservoir) and consumptive use (i.e., how much water was used or depleted by the application of the water withdrawal).

**4. SiteSpecificAmounts**
-	Knowing river and reservoir status can help with long-term planning and flood forecasting modeling. Two relative measurements often used are discharge and gage height. Discharge is the rate at which a volume of water passes by a particular location. Gage height is a measurement of the distance between the water’s surface above the stream gage’s datum reference point (i.e., a unique reference point used to accommodate for changes in a stream channel over time).

---
Each folder is for a unique data type that the state shares into WaDE 2.0. Each folder contains a ReadMe / documentation on how the data was prepared, including...
1) raw source file location / WaDE processed file storage on a Google Drive.
2) how the raw source data was processed and prepared for WaDE using Python.
3) documentation on the amount of imported, removed, and analytics on key summaries and findings of the processed data.


