#Last Updated: 11/17/2022
#Author: Ryan James (WSWC)
#Purpose: To create NM site specific public supply water use methods use information and population dataframe for WaDE_QA 2.0.
#Notes: 1) Used a list approach.  Needed to have two rows, one with surface water, the other with groundwater.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/NewMexico/SS_PublicSupplyWaterUse"
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

outdf.MethodUUID = "NMssps_M1"

outdf.ApplicableResourceTypeCV = "Surface Water & Groundwater"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = "The Public Water Suppliers (PWS) shapefiles are a data set of non-transient PWS locations, their associated service areas, and the locations of their supply sources. The data is furnished by the Office of the State Engineer (OSE) and may be subject to potential errors. The data is accepted for use by the recipient, individual, or entity with the expressed understanding that the OSE and author(s) of the data make no warranties, expressed or implied, concerning the accuracy, completeness, reliability, usability or suitability for any particular purpose of the data.."

outdf.MethodName = "Estimated"

outdf.MethodNEMILink = ""

outdf.MethodTypeCV = "Estimated"


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

#Report missing values if need be to separate csv
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/methods_missing.csv', index=False)

print("Done.")
