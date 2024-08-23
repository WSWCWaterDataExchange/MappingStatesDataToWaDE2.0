# Last Updated: 10/12/2022
# Purpose: To create NJ site specific public supply methods use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) Used a list approach.  Needed to have two rows, one with surface water, the other with groundwater.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/NewJersey/SS_PublicSupplyWaterUse"
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

outdf.MethodUUID = "NJssps_M1"

outdf.ApplicableResourceTypeCV = "Surface Ground Water"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = "The underlying data are available online from multiple New Jersey Department of Environmental Protection (NJDEP) programs through DataMiner (www.nj.gov/dep/opra/). This data is collected from each program, quality assured, enhanced, and then reformatted by NJGS before it is loaded into NJWaTr. NJGS’s QA/QC process determines the best estimate of actual water use for each individual site, and as a result these volumes may be different from other NJDEP sources which have different end uses and purposes. The NJWaTr data is simplified through a series of queries into the tables found in this publication."

outdf.MethodName = "Geological and Water Survey Digital Geodata Series"

outdf.MethodNEMILink = "https://www.nj.gov/dep/njgs/geodata/dgs10-3.htm"

outdf.MethodTypeCV = "Estimate"


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
