# Date Updated: 03/24/2022
# Purpose: To extract UT site use information and population dataframe for WaDEQA 2.0.
# Notes: N/A


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
workingDir = "G:/Shared drives/WaDE Data/Utah/WaterAllocation"  # Specific to my machine, will need to change.
os.chdir(workingDir)
fileInput = "RawinputData/P_UtahMaster.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
fileInput_shape = "RawinputData/P_utGeometry.csv"
dfshape = pd.read_csv(fileInput_shape)

df = pd.read_csv(fileInput)
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe

columnslist = [
    "WaDEUUID",
    "SiteUUID",
    "RegulatoryOverlayUUIDs",
    "WaterSourceUUIDs",
    "CoordinateAccuracy",
    "CoordinateMethodCV",
    "County",
    "EPSGCodeCV",
    "Geometry",
    "GNISCodeCV",
    "HUC12",
    "HUC8",
    "Latitude",
    "Longitude",
    "NHDNetworkStatusCV",
    "NHDProductCV",
    "PODorPOUSite",
    "SiteName",
    "SiteNativeID",
    "SitePoint",
    "SiteTypeCV",
    "StateCV",
    "USGSSiteID"]

# Custom Functions
############################################################################

# For Creating Geometry
Geometrydict = pd.Series(dfshape.geometry.values, index = dfshape.in_SiteNativeID).to_dict()
def retrieveGeometry(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = Geometrydict[String1]
        except:
            outList = ''
    return outList

# For creating SiteName
def assignSiteName(colrowValue):
    if colrowValue == "" or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        outList = colrowValue.strip()
    return outList

# For creating SiteUUID
def assignSiteUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "UTwr_S" + string1
    return outstring

# For creating WaterSourceUUID
WaterSourceUUIDdict = pd.Series(df_watersources.WaterSourceUUID.values, index = df_watersources.WaterSourceNativeID).to_dict()
def retrieveWaterSourceUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = WaterSourceUUIDdict[String1]
        except:
            outList = ''
    return outList



# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist, index=df.index)

print("WaterSourceUUIDs")
outdf['WaterSourceUUIDs'] = df.apply(lambda row: retrieveWaterSourceUUID(row['in_WaterSourceNativeID']), axis=1)

print("RegulatoryOverlayUUIDs")
outdf['RegulatoryOverlayUUIDs'] = ""

print("CoordinateAccuracy")
outdf['CoordinateAccuracy'] = "Unspecified"

print("CoordinateMethodCV")
outdf['CoordinateMethodCV'] = "Unspecified"

print("County")
outdf['County'] = ""

print("EPSGCodeCV")
outdf['EPSGCodeCV'] = "4326"

print("Geometry")
outdf['Geometry'] = df.apply(lambda row: retrieveGeometry(row['in_SiteNativeID']), axis=1)

print("GNISCodeCV")
outdf['GNISCodeCV'] = ""

print("HUC12")
outdf['HUC12'] = ""

print("HUC8")
outdf['HUC8'] = ""

print("Latitude")
outdf['Latitude'] = df['in_Latitude']  # See preprocessing

print("Longitude")
outdf['Longitude'] = df['in_Longitude']  # See preprocessing

print("NHDNetworkStatusCV")
outdf['NHDNetworkStatusCV'] = ""

print("NHDProductCV")
outdf['NHDProductCV'] = ""

print("PODorPOUSite")
outdf['PODorPOUSite'] = df['in_PODorPOUSite']  # See preprocessing

print("SiteName")
outdf['SiteName'] = df.apply(lambda row: assignSiteName(row['in_SiteName']), axis=1)  # See preprocessing

print("SiteNativeID")
outdf['SiteNativeID'] = df['in_SiteNativeID']  # See preprocessing

print("SitePoint")
outdf['SitePoint'] = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = df['in_SiteTypeCV']  # See preprocessing

print("StateCV")
outdf['StateCV'] = "UT"

print("USGSSiteID")
outdf['USGSSiteID'] = ""

print("Adding Data Assessment UUID")
outdf['WaDEUUID'] = ""

print("Resetting Index")
outdf.reset_index()

print("Joining outdf duplicates based on key fields...")
outdf = outdf.replace(np.nan, "")  # Replaces NaN values with blank.
groupbyList = ['PODorPOUSite', 'SiteNativeID', 'SiteName', 'SiteTypeCV', 'Longitude', 'Latitude']
outdf = outdf.groupby(groupbyList).agg(lambda x: ','.join([str(elem) for elem in (list(set(x))) if elem!=''])).replace(np.nan, "").reset_index()
outdf = outdf[columnslist]  # reorder the dataframe's columns based on columnslist


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")
purgecolumnslist = ["ReasonRemoved", "WaDEUUID", "RowIndex", "IncompleteField_1", "IncompleteField_2"]
dfpurge = pd.DataFrame(columns=purgecolumnslist) # Purge DataFrame to hold removed elements

# RegulatoryOverlayUUIDs
outdf, dfpurge = TestErrorFunctions.RegulatoryOverlayUUIDs_S_Check(outdf, dfpurge)

# WaterSourceUUID
outdf100, dfpurge = TestErrorFunctions.WaterSourceUUIDs_S_Check(outdf, dfpurge)

# CoordinateAccuracy
outdf, dfpurge = TestErrorFunctions.CoordinateAccuracy_S_Check(outdf, dfpurge)

# CoordinateMethodCV
outdf, dfpurge = TestErrorFunctions.CoordinateMethodCV_S_Check(outdf, dfpurge)

# County
outdf, dfpurge = TestErrorFunctions.County_S_Check(outdf, dfpurge)

# EPSGCodeCV
outdf, dfpurge = TestErrorFunctions.EPSGCodeCV_S_Check(outdf, dfpurge)

# Geometry
# ???? How to check for geometry datatype

# GNISCodeCV
outdf, dfpurge = TestErrorFunctions.GNISCodeCV_S_Check(outdf, dfpurge)

# HUC12
outdf, dfpurge = TestErrorFunctions.HUC12_S_Check(outdf, dfpurge)

# HUC8
outdf, dfpurge = TestErrorFunctions.HUC8_S_Check(outdf, dfpurge)

# Latitude
outdf, dfpurge = TestErrorFunctions.Latitude_S_Check(outdf, dfpurge)

# Longitude
outdf, dfpurge = TestErrorFunctions.Longitude_S_Check(outdf, dfpurge)

# NHDNetworkStatusCV
outdf, dfpurge = TestErrorFunctions.NHDNetworkStatusCV_S_Check(outdf, dfpurge)

# NHDProductCV
outdf, dfpurge = TestErrorFunctions.NHDProductCV_S_Check(outdf, dfpurge)

# PODorPOUSite
outdf, dfpurge = TestErrorFunctions.PODorPOUSite_S_Check(outdf, dfpurge)

# # SiteName
outdf, dfpurge = TestErrorFunctions.SiteName_S_Check(outdf, dfpurge)

# SiteNativeID
outdf, dfpurge = TestErrorFunctions.SiteNativeID_S_Check(outdf, dfpurge)

# SitePoint
# ???? How to check for geometry datatype

# SiteTypeCV
outdf, dfpurge = TestErrorFunctions.SiteTypeCV_S_Check(outdf, dfpurge)

# StateCV
outdf, dfpurge = TestErrorFunctions.StateCV_S_Check(outdf, dfpurge)

# USGSSiteID
outdf, dfpurge = TestErrorFunctions.USGSSiteID_S_Check(outdf, dfpurge)


############################################################################
print("Assign SiteUUID") # has to be one of the last.
outdf = outdf.reset_index(drop=True)
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['SiteUUID'] = dftemp.apply(lambda row: assignSiteUUID(row['Count']), axis=1)

# Error check SiteUUID
outdf, dfpurge = TestErrorFunctions.SiteUUID_S_Check(outdf, dfpurge)


# Remove WaDEUUID field from import file (only needed for purge info).
############################################################################
print("Drop Assessment WaDEUUID")
outdf = outdf.drop(['WaDEUUID'], axis=1)


# Export to new csv
############################################################################
print("Exporting outdf and dfpurge dataframes...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/sites.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_excel('ProcessedInputData/sites_missing.xlsx', index=False)

print("Done.")
