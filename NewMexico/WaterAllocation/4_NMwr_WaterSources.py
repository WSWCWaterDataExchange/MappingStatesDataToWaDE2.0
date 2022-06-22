#Date Created: 06/21/2022
#Purpose: To extract NM water source use information and populate dataframe for WaDE_QA 2.0.
#Notes: 1) Some data solved with pre-processes code.

# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "G:/Shared drives/WaDE Data/NewMexico/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/P_NewMexicoMaster.csv"
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

# For creating WaterSourceNativeID
def assignWaterSourceNativeID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        strvalue = str(colrowValue)
        outList = strvalue.strip()
    return outList

# For creating WaterSourceTypeCV
def assignWaterSourceTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        strvalue = str(colrowValue)
        outList = strvalue.strip()
    return outList

# For creating WaDESiteUUID
def assignWaterSourceUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "NMwr_WS" + string1
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

print("WaterSourceName")  # see pre-processed code
outdf['WaterSourceName'] = df['in_WaterSourceName']

print("WaterSourceNativeID")  # see pre-processed code
outdf['WaterSourceNativeID'] = df['in_WaterSourceNativeID']

print("WaterSourceTypeCV")  # see pre-processed code
outdf['WaterSourceTypeCV'] = df.apply(lambda row: assignWaterSourceTypeCV(row['in_WaterSourceTypeCV']), axis=1)

##############################
# Dropping duplicate
print("Dropping duplicates")
outdf = outdf.drop_duplicates(subset=['WaterSourceName', 'WaterSourceNativeID', 'WaterSourceTypeCV']).reset_index(drop=True)
##############################

print("Resetting Index")
outdf.reset_index()


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")
purgecolumnslist = ["ReasonRemoved", "RowIndex", "IncompleteField_1", "IncompleteField_2"]
dfpurge = pd.DataFrame(columns=purgecolumnslist) # Purge DataFrame to hold removed elements

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


############################################################################
print("Assign WaterSourceUUID") # has to be one of the last.
outdf = outdf.reset_index(drop=True)
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['WaterSourceUUID'] = dftemp.apply(lambda row: assignWaterSourceUUID(row['Count']), axis=1)

# Error check WaterSourceUUID
outdf, dfpurge = TestErrorFunctions.WaterSourceUUID_WS_Check(outdf, dfpurge)


# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/watersources.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_excel('ProcessedInputData/watersources_missing.xlsx', index=False)

print("Done.")
