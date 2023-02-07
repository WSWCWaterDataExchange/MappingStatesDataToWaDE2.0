#Date Created: 06/23/2022
#Purpose: To extract SD wr methods use information and populate dataframe for WaDE_QA 2.0.
#Notes: 1) Two different data sets, groundwater vs surface water.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/SouthDakota/WaterAllocation"
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

outdf.MethodUUID = "SDwr_M1"

outdf.ApplicableResourceTypeCV = "Surface Ground Water"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = """WATER RIGHTS METHOD: South Dakaotra water rights are described in the provdied method link DISCLAIMER: The above map dataset is incomplete. There are water permits/rights not included because coordinates for the location have not been established due to the lack of a proper legal description. This is often true of very old filings which did not reference a specific section, township and range. Each water permit/right shown on the map is represented by a single diversion point (pumping location) even though the permit/right may have multiple diversion points. Most of the points shown on the map are calculated values and do NOT represent a precise location of the diversion point. Any reliance on the map results is solely at the user's discretion."""

outdf.MethodName = "South Dakakota Water Rights Method"

outdf.MethodNEMILink = "https://danr.sd.gov/OfficeOfWater/WaterRights/docs/WRAPPLPrimer.pdf"

outdf.MethodTypeCV = "Legal Processes"

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
