#Date Created: 04/07/2020
#Purpose: To create OK methods use information and population dataframe for WaDE_QA 2.0.
#Notes:


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Oklahoma/WaterAllocation"
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

outdf.MethodUUID = "OWRB_Water Rights"

outdf.ApplicableResourceTypeCV = "Allocation"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = "The OWRB appropriates stream and groundwater supplies to various water users in the state. Permits are issued for the use of both surface and groundwaters in Oklahoma (domestic uses are exempt) and all waters must be used beneficially without waste."

outdf.MethodName = "Oklahoma Water Rights"

outdf.MethodNEMILink = "https://owrb.maps.arcgis.com/apps/webappviewer/index.html?id=db6e61cfdbc74a4d8b919b2eceef8d43"

outdf.MethodTypeCV = "Water Allocation"


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
    outdf_nullMand.to_csv('ProcessedInputData/methods_missing.csv')  # index=False,


print("Done.")