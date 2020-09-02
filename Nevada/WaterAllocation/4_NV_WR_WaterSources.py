#Date Created: 06/12/2020
#Purpose: To extract NV water source use information and population dataframe for WaDE_QA 2.0.
#Notes: 1) Little water source info available at this time.  Easier to have simple in out code.

# Note:  Currently using dummy row until more data made available from TX

# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading input csv...")
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Nevada/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/P_MastersNV.csv"
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
        outList = colrowValue
    return outList

# For creating WaterSourceTypeCV
UnknownWSCVDict = {
"EFF" : "Reuse",
"GEO" : "Groundwater",
"LAK" : "Surface Water",
"OGW" : "Groundwater",
"OSW" : "Surface Water",
"RES" : "Reservoir",
"SPR" : "Surface Water",
"STO" : "Storage",
"STR" : "Surface Water",
"UG" : "Groundwater",
"UKN" : "Unknown"}
def assignWaterSourceTypeCV(colrowValue):
    if colrowValue == "" or pd.isnull(colrowValue):
        outList = ""
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = UnknownWSCVDict[String1]
        except:
            outList = "Unknown"
    return outList

# For creating WaDESiteUUID
def assignWaterSourceUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "NV_" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf=pd.DataFrame(columns=columnslist)

print("WaterSourceTypeCV")
outdf['WaterSourceTypeCV'] = df.apply(lambda row: assignWaterSourceTypeCV(row['source']), axis=1)

print("GNISFeatureNameCV")  # Hardcoded
outdf.GNISFeatureNameCV = ""

print("Geometry")  # Hardcoded
outdf.Geometry = ""

print("WaterQualityIndicatorCV")  # Hardcoded
outdf.WaterQualityIndicatorCV = "Unspecified"

print("WaterSourceName")
outdf.WaterSourceName = "Unspecified"
# outdf['WaterSourceName'] = "Unspecified"

print("WaterSourceNativeID")  # has to be one of the last, need length of created outdf
outdf.WaterSourceName = "Unspecified"
# outdf['WaterSourceName'] = "Unspecified"


##############################
# Dropping duplicate
print("Dropping duplicates")
outdf = outdf.drop_duplicates(subset=['WaterSourceTypeCV']).reset_index(drop=True)
##############################

print("WaterSourceUUID") #native source identifier and the organization univeral id. has to be one of the last, need WaterSourceNativeID to create
df["Count"] = range(1, len(df.index) + 1)
outdf['WaterSourceUUID'] = df.apply(lambda row: assignWaterSourceUUID(row['Count']), axis=1)

# Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")  # Hardcoded
dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# WaterSourceUUID_nvarchar(250)_-
mask = outdf.loc[(outdf["WaterSourceUUID"].isnull()) | (outdf["WaterSourceUUID"] == '') | (
            outdf['WaterSourceUUID'].str.len() > 250)].assign(ReasonRemoved='Bad WaterSourceUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[(outdf["WaterSourceUUID"].isnull()) | (outdf["WaterSourceUUID"] == '') | (
                outdf['WaterSourceUUID'].str.len() > 250)].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# Geometry_geometry_Yes
# ???? How to check for geometry datatype

# GNISFeatureNameCV_nvarchar(250)_Yes
mask = outdf.loc[outdf["GNISFeatureNameCV"].str.len() > 250].assign(ReasonRemoved='Bad GNISFeatureNameCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[outdf["GNISFeatureNameCV"].str.len() > 250].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# WaterQualityIndicatorCV_nvarchar(100)_-
mask = outdf.loc[(outdf["WaterQualityIndicatorCV"].isnull()) | (outdf["WaterQualityIndicatorCV"] == '') | (
            outdf['WaterQualityIndicatorCV'].str.len() > 250)].assign(
    ReasonRemoved='Bad WaterQualityIndicatorCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[(outdf["WaterQualityIndicatorCV"].isnull()) | (outdf["WaterQualityIndicatorCV"] == '') | (
                outdf['WaterQualityIndicatorCV'].str.len() > 250)].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# WaterSourceName_nvarchar(250)_Yes
mask = outdf.loc[outdf["WaterSourceName"].str.len() > 250].assign(ReasonRemoved='Bad WaterSourceName').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[outdf["WaterSourceName"].str.len() > 250].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# WaterSourceNativeID_nvarchar(250)_Yes
mask = outdf.loc[outdf["WaterSourceNativeID"].str.len() > 250].assign(
    ReasonRemoved='Bad WaterSourceNativeID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[outdf["WaterSourceNativeID"].str.len() > 250].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# WaterSourceTypeCV_nvarchar(100)_-
mask = outdf.loc[(outdf["WaterSourceTypeCV"].isnull()) | (outdf["WaterSourceTypeCV"] == '') | (
            outdf['WaterSourceTypeCV'].str.len() > 100)].assign(ReasonRemoved='Bad WaterSourceTypeCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[(outdf["WaterSourceTypeCV"].isnull()) | (outdf["WaterSourceTypeCV"] == '') | (
                outdf['WaterSourceTypeCV'].str.len() > 100)].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")
# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/watersources.csv', index=False)

# Report purged values.
if (len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/watersources_missing.csv')  # index=False,

print("Done.")