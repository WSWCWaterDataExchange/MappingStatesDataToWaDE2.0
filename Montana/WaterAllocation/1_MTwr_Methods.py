#Date Created: 11/23/2020
#Purpose: To extract MT methods use information and population dataframe for WaDE_QA 2.0.
#Notes:  asdf


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Montana/WaterAllocation"
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

outdf.MethodUUID = ["MT_Water Allocation Adj", "MT_Water Allocation App"]

outdf.ApplicableResourceTypeCV = ["Surface Ground Water", "Surface Ground Water"]

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = ["Water rights that were established prior to July 1,1973 are administered by the Adjudication Bureau. Water rights that were established from July 1, 1973 through the present are administered by the New Appropriations Program.",
                           "Water rights that were established prior to July 1,1973 are administered by the Adjudication Bureau. Water rights that were established from July 1, 1973 through the present are administered by the New Appropriations Program."]

outdf.MethodName = ["Adjudication", "Appropriations"]

outdf.MethodNEMILink = ["'http://dnrc.mt.gov/divisions/water/water-rights", "'http://dnrc.mt.gov/divisions/water/water-rights"]

outdf.MethodTypeCV = ["Adjudication", "Appropriations"]

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
    outdf_nullMand.to_csv('ProcessedInputData/methods_mandatoryFieldMissing.csv')


print("Done.")