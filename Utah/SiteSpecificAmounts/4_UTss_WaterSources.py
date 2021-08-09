# Last Updated: 12/16/2020
# Purpose: To extract UT site specific water source use information and populate dataframe for WaDE_QA 2.0.
# Notes: N/A


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/CustomFunctions/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/SiteSpecificAmounts"
os.chdir(workingDir)
fileInput = "RawinputData/P_MasterUTSiteSpecific.csv"
df = pd.read_csv(fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.

#WaDE columns
columnslist = [
    "WaterSourceUUID",
    "Geometry",
    "GNISFeatureNameCV",
    "WaterQualityIndicatorCV",
    "WaterSourceName",
    "WaterSourceNativeID",
    "WaterSourceTypeCV"]


# Custom Site Functions
############################################################################

#WaterSourceUUID
def assignWaterSourceUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "UTss_WS" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(index=df.index, columns=columnslist)  # The output dataframe for CSV.

print("Geometry")
outdf['Geometry'] = ""

print("GNISFeatureNameCV")
outdf['GNISFeatureNameCV'] = ""

print("WaterQualityIndicatorCV")
outdf['WaterQualityIndicatorCV'] = "Fresh"

print("WaterSourceName")
outdf['WaterSourceName'] = "Unspecified"

print("WaterSourceNativeID")
outdf['WaterSourceNativeID'] = df['in_WaterSourceNativeID']  # see preprocessing.

print("WaterSourceTypeCV")
outdf['WaterSourceTypeCV'] = df['in_WaterSourceTypeCV']  # see preprocessing.

##############################
# Dropping duplicate
print("Dropping duplicates")
outdf = outdf.drop_duplicates(subset=['WaterSourceName', 'WaterSourceNativeID', 'WaterSourceTypeCV']).reset_index(drop=True)
##############################

print("WaterSourceUUID")
df["Count"] = range(1, len(df.index) + 1)
outdf['WaterSourceUUID'] = df.apply(lambda row: assignWaterSourceUUID(row['Count']), axis=1)

print("Resetting Index")
outdf.reset_index()


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")

dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# WaterSourceUUID
outdf, dfpurge = TestErrorFunctions.WaterSourceUUID_WS_Check(outdf, dfpurge)

# Geometry
# ???? How to check for geometry datatype

# GNISFeatureNameCV
outdf, dfpurge = TestErrorFunctions.GNISFeatureNameCV_WS_Check(outdf, dfpurge)

# WaterQualityIndicatorCV
outdf, dfpurge = TestErrorFunctions.WaterQualityIndicatorCV_WS_Check(outdf, dfpurge)

# WaterSourceName
outdf, dfpurge = TestErrorFunctions.WaterSourceName_WS_Check(outdf, dfpurge)

# WaterSourceNativeID
outdf, dfpurge = TestErrorFunctions.WaterSourceNativeID_WS_Check(outdf, dfpurge)

# WaterSourceTypeCV
outdf, dfpurge = TestErrorFunctions.WaterSourceTypeCV_WS_Check(outdf, dfpurge)


# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/watersources.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/watersources_missing.csv', index=False)

print("Done.")
