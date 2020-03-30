#Date Created: 03/13/2020
#Purpose: To extract UT methods use information and population dataframe for WaDE_QA 2.0.
#Notes:   1) UT possesses multiple methods


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading inputs...")
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/WaterAllocation"
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

outdf.MethodUUID = ["UT_STREAMFLOW_SUPPLY", "UT_Use", "UT_LEGAVLBLE", "UT_RETURNFLOW", "UT_Consumptive Use Estimate",
                    "UT_Withdrawal Volume Estimate", "UT_INSTREAM_FLOW", "UT_STORAGE_SUPPLY", "UT_WaterAllocation"]

outdf.ApplicableResourceTypeCV = ["Surface Water", "Surface Ground", "Surface Ground", "Surface Water", "Surface Ground",
                                  "Surface Ground", "Surface Water", "Surface Water", "Surface Ground"]

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = ["Average Streamflow Method", "Agricultural Landuse Survey", "Legally Available Water",
                           "Return Flow Estimates", "Consumptive Use Estimate Method", "Diversion Volume Estimate",
                           "Instream Flow Estimate", "Estimate of Reservoir Storage", "Water Rights"]

outdf.MethodName = ["Average Streamflow Method", "Agricultural Landuse Survey", "Legally Available Water",
                    "Return Flow Estimates", "Consumptive Use Estimate Method", "Diversion Volume Estimate",
                    "Instream Flow Estimate", "Estimate of Reservoir Storage", "Water Allocation"]

outdf.MethodNEMILink = ""

outdf.MethodTypeCV = ["Modeled", "Modeled", "Modeled", "Modeled",
                      "Modeled", "Modeled", "Modeled", "Modeled", "Adjudicated"]

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