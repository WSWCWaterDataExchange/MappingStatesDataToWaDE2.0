#Date Created: 12/23/2020
#Purpose: To extract OR water source use information and population dataframe for WaDE_QA 2.0.
#Notes:

# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Oregon/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/P_OregonMaster.csv"
df = pd.read_csv(fileInput)

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

# For creating WaterSourceName
def assignWaterSourceName(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unknown"
    else:
        outList = colrowValue.strip()
    return outList

# For creating WaterSourceTypeCV
WSTypeDict = {
    "ST": "storage",
    "GW": "groundwater",
    "SW": "surface water"
}
def assignWaterSourceTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unknown'
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = WSTypeDict[String1]
        except:
            outList = 'Unknown'

    return outList

# For creating WaterSourceUUID
def assignWaterSourceUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "ORwr_WS" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(index=df.index, columns=columnslist)  # The output dataframe for CSV.

print("Geometry")  # Hardcoded
outdf.Geometry = ""

print("GNISFeatureNameCV")  # Hardcoded
outdf.GNISFeatureNameCV = ""

print("WaterQualityIndicatorCV")  # Hardcoded
outdf.WaterQualityIndicatorCV = "Fresh"

print("WaterSourceName")  # Hardcoded
outdf['WaterSourceName'] = df.apply(lambda row: assignWaterSourceName(row['source']), axis=1)

print("WaterSourceNativeID")  # has to be one of the last, need length of created outdf
outdf.WaterSourceNativeID = "Unspecified"

print("WaterSourceTypeCV")
outdf['WaterSourceTypeCV'] = df.apply(lambda row: assignWaterSourceTypeCV(row['wr_type']), axis=1)

##############################
# Dropping duplicate
print("Dropping duplicates")
outdf = outdf.drop_duplicates(subset=['WaterSourceName', 'WaterSourceTypeCV']).reset_index(drop=True)
##############################

print("WaterSourceUUID")
df["Count"] = range(1, len(df.index) + 1)
outdf['WaterSourceUUID'] = df.apply(lambda row: assignWaterSourceUUID(row['Count']), axis=1)

print("Resetting Index")  # Hardcoded
outdf.reset_index()


#Error Checking Each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")  # Hardcoded
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