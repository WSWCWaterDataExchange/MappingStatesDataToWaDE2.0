# Date Update: 03/28/2023
# Purpose: To extract NM water source information and populate dataframe for WaDE_QA 2.0.
# Notes: N/A


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Custom Libraries
############################################################################
import sys
# columns
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/MappingFunctions")
import GetColumnsFile

# Test WaDE Data for any Errors
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/ErrorCheckCode")
import TestErrorFunctionsFile


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "G:/Shared drives/WaDE Data/NewMexico/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/Pwr_NewMexicoMain.zip"
df = pd.read_csv(fileInput, compression='zip')

# WaDE columns
WaterSourcseColumnsList = GetColumnsFile.GetWaterSourcesColumnsFunction()


# Custom Site Functions
############################################################################

# For creating WaDESiteUUID
def assignWaterSourceUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "NMwr_WS" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(index=df.index, columns=WaterSourcseColumnsList)  # The output dataframe for CSV.

print("Geometry")
outdf['Geometry'] = ""

print("GNISFeatureNameCV")
outdf['GNISFeatureNameCV'] = ""

print("WaterQualityIndicatorCV")
outdf['WaterQualityIndicatorCV'] = "Fresh"

print("WaterSourceName")
outdf['WaterSourceName'] = df['in_WaterSourceName']

print("WaterSourceNativeID")
outdf["WaterSourceNativeID"] = df['in_WaterSourceNativeID']

print("WaterSourceTypeCV")
outdf['WaterSourceTypeCV'] = df['in_WaterSourceTypeCV']

##############################
# Dropping duplicate
print("Dropping duplicates")
outdf = outdf.drop_duplicates(subset=['WaterSourceName', 'WaterSourceNativeID', 'WaterSourceTypeCV']).reset_index(drop=True)
##############################

print("Adding Data Assessment UUID")
outdf['WaDEUUID'] = df['WaDEUUID']

print("Resetting Index")
outdf.reset_index()


#Error Checking each Field
############################################################################
print("Error checking each field. Purging bad inputs.")
dfpurge = pd.DataFrame(columns=WaterSourcseColumnsList) # Purge DataFrame to hold removed elements
dfpurge['ReasonRemoved'] = ""
dfpurge['IncompleteField'] = ""
outdf, dfpurge = TestErrorFunctionsFile.WaterSourceTestErrorFunctions(outdf, dfpurge)
print(f'Length of outdf DataFrame: ', len(outdf))
print(f'Length of dfpurge DataFrame: ', len(dfpurge))


############################################################################
print("Assign WaterSourceUUID") # has to be one of the last.
outdf = outdf.reset_index(drop=True)
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['WaterSourceUUID'] = dftemp.apply(lambda row: assignWaterSourceUUID(row['Count']), axis=1)
#outdf['WaterSourceUUID'] = outdf.apply(lambda row: assignWaterSourceUUID(row['WaterSourceNativeID']), axis=1)

# Error check WaterSourceUUID
outdf, dfpurge = TestErrorFunctionsFile.WaterSourceUUID_WS_Check(outdf, dfpurge)


# Export to new csv
############################################################################
print("Exporting dataframe...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/watersources.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0): print(f'...', len(dfpurge),  ' records removed.')
dfpurge.insert(0, 'ReasonRemoved', dfpurge.pop('ReasonRemoved'))
dfpurge.to_csv('ProcessedInputData/watersources_missing.csv', index=False)

print("Done")