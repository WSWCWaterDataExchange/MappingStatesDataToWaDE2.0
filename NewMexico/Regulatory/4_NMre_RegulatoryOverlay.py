# Date Created: 08/12/2021
# Author: Ryan James (WSWC)
# Purpose: To create NM regulatory overlay information and populate a dataframe WaDEQA 2.0.
# Notes: N/A


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
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/NewMexico/Regulatory"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_nmRegMaster.csv"
df_DM = pd.read_csv(M_fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.

#WaDE dataframe columns
columnslist = [
    "RegulatoryOverlayUUID",
    "OversightAgency",
    "RegulatoryDescription",
    "RegulatoryName",
    "RegulatoryOverlayNativeID",
    "RegulatoryStatusCV",
    "RegulatoryStatute",
    "RegulatoryStatuteLink",
    "StatutoryEffectiveDate",
    "StatutoryEndDate",
    "RegulatoryOverlayTypeCV",
    "WaterSourceTypeCV"]


# Custom Functions
############################################################################

# For creating RegulatoryOverlayUUID
def assignRegulatoryOverlayUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "NMre_RO" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("OversightAgency")
outdf['OversightAgency'] = df_DM['in_OversightAgency']  # See pre-processing.

print("RegulatoryDescription")
outdf['RegulatoryDescription'] = df_DM['in_RegulatoryDescription']  # See pre-processing.

print("RegulatoryName")
outdf['RegulatoryName'] = df_DM['in_RegulatoryName']  # See pre-processing.

print("RegulatoryOverlayNativeID")
outdf['RegulatoryOverlayNativeID'] = df_DM['in_RegulatoryOverlayNativeID']  # See pre-processing.

print("RegulatoryStatusCV")
outdf['RegulatoryStatusCV'] = df_DM['in_RegulatoryStatusCV']  # See pre-processing.

print("RegulatoryStatute")
outdf['RegulatoryStatute'] = ""

print("RegulatoryStatuteLink")
outdf['RegulatoryStatuteLink'] = df_DM['in_RegulatoryStatuteLink']  # See pre-processing.

print("StatutoryEffectiveDate")
outdf['StatutoryEffectiveDate'] = df_DM['in_StatutoryEffectiveDate']  # See pre-processing.

print("StatutoryEndDate")
outdf['StatutoryEndDate'] = ""

print("RegulatoryOverlayTypeCV")
outdf['RegulatoryOverlayTypeCV'] = df_DM['in_RegulatoryOverlayTypeCV']  # See pre-processing.

print("WaterSourceTypeCV")
outdf['WaterSourceTypeCV'] = df_DM['in_WaterSourceTypeCV']  # See pre-processing.

print("Resetting Index")
outdf.reset_index()

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of RegulatoryName, RegulatoryOverlayNativeID, RegulatoryStatusCV, RegulatoryOverlayTypeCV, WaterSourceTypeCV
outdf = outdf.drop_duplicates(subset=['RegulatoryName', 'RegulatoryOverlayNativeID', 'RegulatoryStatusCV', 'RegulatoryOverlayTypeCV', 'WaterSourceTypeCV']).reset_index(drop=True)
######################################

print("RegulatoryOverlayUUID") # has to be one of the last.
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['RegulatoryOverlayUUID'] = dftemp.apply(lambda row: assignRegulatoryOverlayUUID(row['Count']), axis=1)


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# None at the moment


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")

dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# RegulatoryOverlayUUID
outdf, dfpurge = TestErrorFunctions.RegulatoryOverlayUUID_RE_Check(outdf, dfpurge)

# OversightAgency
outdf, dfpurge = TestErrorFunctions.OversightAgency_RE_Check(outdf, dfpurge)

# RegulatoryDescription
outdf, dfpurge = TestErrorFunctions.RegulatoryDescription_RE_Check(outdf, dfpurge)

# RegulatoryName
outdf, dfpurge = TestErrorFunctions.RegulatoryName_RE_Check(outdf, dfpurge)

# RegulatoryOverlayNativeID
outdf, dfpurge = TestErrorFunctions.RegulatoryOverlayNativeID_RE_Check(outdf, dfpurge)

# RegulatoryStatusCV
outdf, dfpurge = TestErrorFunctions.RegulatoryStatusCV_RE_Check(outdf, dfpurge)

# RegulatoryStatute
outdf, dfpurge = TestErrorFunctions.RegulatoryStatute_RE_Check(outdf, dfpurge)

# RegulatoryStatuteLink
outdf, dfpurge = TestErrorFunctions.RegulatoryStatuteLink_RE_Check(outdf, dfpurge)

# StatutoryEffectiveDate
outdf, dfpurge = TestErrorFunctions.StatutoryEffectiveDate_RE_Check(outdf, dfpurge)

# StatutoryEndDate
outdf, dfpurge = TestErrorFunctions.StatutoryEndDate_RE_Check(outdf, dfpurge)

# RegulatoryOverlayTypeCV
outdf, dfpurge = TestErrorFunctions.RegulatoryOverlayTypeCV_RE_Check(outdf, dfpurge)

# WaterSourceTypeCV
outdf, dfpurge = TestErrorFunctions.WaterSourceTypeCV_RE_Check(outdf, dfpurge)


# Export to new csv
############################################################################
print("Exporting dataframe outdf100 to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/regulatoryoverlays.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/regulatoryoverlays_missing.csv', index=False)

print("Done.")
