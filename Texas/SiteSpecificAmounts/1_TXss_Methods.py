# Last Updated: 03/04/2022
# Purpose: To create TX site specific methods use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) Used a list approach.  Needed to have two rows, one with surface water, the other with groundwater.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Texas/SiteSpecificAmounts"
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
# outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.MethodUUID = ["TXss_M1", "TXss_M2"]

outdf.ApplicableResourceTypeCV = ["Surface Ground Water",
                                  "Surface Ground Water"]

outdf.DataConfidenceValue = ["", ""]

outdf.DataQualityValueCV = ["", ""]

outdf.DataCoverageValue = ["", ""]

outdf.MethodDescription = ["Water use intake report for all surveyed public water systems by water planning region, including geographic information, monthly intake volumes and water source (groundwater, surface water or reuse).",
                           "Annual retail water use volumes and connections by use category (single-family, multi-family, commercial, institutional, industrial, agricultural, reuse and unmetered) for all surveyed public water systems."]

outdf.MethodName = ["Historical Municipal Water Intake Report",
                    "Historical Categorical Connections and Volumes"]

outdf.MethodNEMILink = ["", ""]

outdf.MethodTypeCV = ["Estimate", "Estimate"]


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
