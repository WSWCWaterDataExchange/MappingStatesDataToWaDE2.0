#Date Created: 12/23/2022
#Purpose: To extract ID methods use information and populate dataframe for WaDE_QA 2.0.
#Notes:   1) Single row of entries, inpVals, for Methods Table.


# Needed Libraries
############################################################################
import os
import pandas as pd
import numpy as np


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Idaho/WaterAllocation"
os.chdir(workingDir)

#WaDE columns
columns = [
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
inpVals = [
    "IDwr_M1",
    "Surface Ground Water",
    "",
    "",
    """The Idaho Department of Water Resources is making this data available as a public service. The Idaho Department of Water Resources strives to ensure that all technical data and other information made available to the public is accurate, complete and in conformance with the Idaho Public Records Act. Neither the Department of Water Resources nor the State of Idaho, however, assumes any legal responsibility for the accuracy or completeness of the information contained on this site. Persons using information from this site for official purposes, or other purposes, for which accuracy and completeness are required, are hereby notified that they should first verify the information with the public records or other primary sources from which the information was obtained."""
    ,
    "Methodology used for tracking diversions in the state of Idaho.",
    "Idaho Water Rights Method",
    "https://idwr.idaho.gov/water-rights/overview/",
    "Legal Processes"]

outdf = pd.DataFrame([inpVals], columns=columns)


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
