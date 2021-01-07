#Date Created: 10/22/2020
#Purpose: To extract ID water source use information and population dataframe for WaDE_QA 2.0.
#Notes: 1) For 'WaterSourceTypeCV', easier to label everything that is not a surface water first.


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
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Idaho/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/P_IdahoMaster.csv"
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
        outList = "Unspecified"
    else:
        outList = colrowValue
    return outList

# For creating WaDESiteUUID
def assignWaterSourceUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "IDwr_WS" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(index=df.index, columns=columnslist)  # The output dataframe for CSV.

print("Geometry")  
outdf.Geometry = ""

print("GNISFeatureNameCV")  
outdf.Geometry = ""

print("WaterQualityIndicatorCV")  
outdf.WaterQualityIndicatorCV = "Unspecified"

print("WaterSourceName")
outdf['WaterSourceName'] = df.apply(lambda row: assignWaterSourceName(row['Source_POD']), axis=1)

print("WaterSourceNativeID")  # has to be one of the last, need length of created outdf
outdf.WaterSourceNativeID = "Unspecified"

print("WaterSourceTypeCV")
outdf['WaterSourceTypeCV']  = df['inputWaterSourceType']

##############################
# Dropping duplicate
print("Dropping duplicates")
outdf = outdf.drop_duplicates(subset=['WaterSourceName', 'WaterSourceTypeCV']).reset_index(drop=True)
##############################

print("WaterSourceUUID") #native source identifier and the organization univeral id. has to be one of the last, need WaterSourceNativeID to create
df["Count"] = range(1, len(df.index) + 1)
outdf['WaterSourceUUID'] = df.apply(lambda row: assignWaterSourceUUID(row['Count']), axis=1)


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
