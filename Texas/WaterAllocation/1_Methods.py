#Date Created: 06/08/2020
#Purpose: To extract TX methods use information and population dataframe for WaDE_QA 2.0.
#Notes:   1) Single row of entries, inpVals, for Methods Table.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading inputs...")
workingDir="/Users/augustus/Desktop/WSWC/WaDE/MappingStatesDataToWaDE2.0/Texas/WaterAllocation/"
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
    "TCEQ_WaterRights",
    "Surface Ground",
    np.nan,
    np.nan,
    np.nan,
    "Methodology used for tracking diversions in the state of Texas.",
    "Texas Water Rights",
    "https://tceq.maps.arcgis.com/home/item.html?id=796b001513b9407a9818897b4dc1ec4d",
    "Estimated"]

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

outdf.to_csv('ProcessedInputData/methods.csv', index=False)

#Report missing values if need be to separate csv
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/methods_mandatoryFieldMissing.csv')  # index=False,


print("Done.")