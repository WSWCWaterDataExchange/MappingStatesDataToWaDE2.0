#Date Created: 03/11/2022
#Author: Ryan James, WSWC
#Purpose: To extract CO water source use information and populate dataframe for WaDE_QA 2.0.
#Notes: 1) For 'WaterSourceTypeCV', easier to label everything that is not a surface water first.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/CustomFunctions/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Colorado/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/P_ColoradoMaster.csv"
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


# Custom Functions
############################################################################

# For creating WaDESiteUUID
def assignWaterSourceUUID(colrowValue):
    string1 = str(colrowValue)
    outString = "COwr_WS" + string1
    return outString


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(index=df.index, columns=columnslist)  # The output dataframe for CSV.

print("Geometry")
outdf['Geometry'] = ""

print("GNISFeatureNameCV")
outdf['GNISFeatureNameCV'] = ""

print("WaterQualityIndicatorCV")
outdf['WaterQualityIndicatorCV'] = "Unspecified"

print("WaterSourceName")
outdf['WaterSourceName'] = df['input_WaterSourceName']

print("WaterSourceNativeID")
outdf['WaterSourceNativeID'] = df['GNIS ID']

print("WaterSourceTypeCV")
outdf['WaterSourceTypeCV'] = df['input_WaterSourceTypeCV']

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
purgecolumnslist = ["ReasonRemoved", "RowIndex", "IncompleteField_1", "IncompleteField_2"]
dfpurge = pd.DataFrame(columns=purgecolumnslist) # Purge DataFrame to hold removed elements

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
    dfpurge.to_excel('ProcessedInputData/watersources_missing.xlsx', index=False)

print("Done.")
