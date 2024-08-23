# Date Created: 02/11/2022
# Author: Ryan James (WSWC)
# Purpose: To create CA agg methods use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) No input csv to read, all values are more easily hardcoded into a list here and then exported to CSV.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/California/AggregatedAmounts"
os.chdir(workingDir)

#WaDE columns
columnslist = [
    "MethodUUID",
    "ApplicableResourceTypeCV",
    "DataConfidenceValue",
    "DataCoverageValue",
    "DataQualityValueCV",
    "MethodDescription",
    "MethodName",
    "MethodNEMILink",
    "MethodTypeCV"]


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist)
outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.MethodUUID = "CAag_M1"

outdf.ApplicableResourceTypeCV = "Surface Ground Reuse Recycled Water"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = "Computed applied, net, and depletion water balances for California. Water balances are simplified water budgets for a water year based on analyses of developed and dedicated water supplies, water uses by sector, water reuses, operational characteristics for an area, and inflows and outflow for a study area that occur above the root zone. Dedicated and developed water supplies include surface water, groundwater, reused and recycled water. Water uses by sector for these analyses include parameters for agriculture, urban, managed wetlands, Wild and Scenic river annual volumes, minimum required instream flows, and minimum required delta outflow, recognizing that water is often used multiple times and benefits multiple sectors. Water balance results show what water was applied to actual uses so that use equals supply. Recent data provided includes water uses and supplies for WYs 2002-2016 at Detailed Analysis Unit by County (DAUCO), Planning Area (PA), Hydrologic Region (HR), and Statewide spatial scales. Computation and aggregation equations for applied, net, and depletion water balances are included in the Standard Operating Procedures (SOPs) for data management and analyses. Metadata are provided in a .txt file which can be opened by any text editor."

outdf.MethodName = "Water Plan Water Balance Data"

outdf.MethodNEMILink = "https://data.cnra.ca.gov/dataset/water-plan-water-balance-data"

outdf.MethodTypeCV = "Computed"


# Check required fields are not null
############################################################################
print("Check required is not null...")
#Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan)
outdf_nullMand = outdf.loc[(outdf["MethodUUID"].isnull()) | (outdf["MethodUUID"] == '') |
                           (outdf["MethodName"].isnull()) | (outdf["MethodName"] == '') |
                           (outdf["MethodDescription"].isnull()) | (outdf["MethodDescription"] == '') |
                           (outdf["ApplicableResourceTypeCV"].isnull()) | (outdf["ApplicableResourceTypeCV"] == '') |
                           (outdf["MethodTypeCV"].isnull()) | (outdf["MethodTypeCV"] == '')]


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/methods.csv', index=False)

# Report purged values.
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/methods_missing.csv', index=False)

print("Done.")
