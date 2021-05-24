#Date Created: 12/01/2020
#Purpose: To extract AZ site information and populate dataframe for WaDE_QA 2.0.
#Notes: asdf

# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os
# from pyproj import Transformer, transform
# transformer = Transformer.from_proj(4326, 4326)  # A trick to drastically optimize the Transformer of pyproj.
# MT projection = EPSG:4326, same as WGS84 projection used by WaDE 2.0 = epsg:4326.

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Arizona/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/P_ArizonaMaster.csv"
df = pd.read_csv(fileInput)

watersources_fileInput = "ProcessedInputData/watersources.csv"
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe

columnslist = [
    "SiteUUID",
    "RegulatoryOverlayUUIDs",
    "WaterSourceUUID",
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

# For creating WaterSourceUUID
WaterSourceUUIDdict = pd.Series(df_watersources.WaterSourceUUID.values, index = df_watersources.WaterSourceName).to_dict()
def retrieveWaterSourceUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        # strVal = str(colrowValue)
        # strVal = strVal.strip()
        strVal = colrowValue
        outList = WaterSourceUUIDdict[strVal]
    return outList

# For creating SiteNativeID
def assignSiteNativeID(colrowValue):
    strVal = str(colrowValue)
    strVal = strVal.strip()
    if strVal == '' or pd.isnull(strVal):
        outList = "Unspecified"
    else:
        outList = strVal
    return outList

# For creating SiteTypeCV
def assignSiteTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        strVal = str(colrowValue)
        outList = strVal.strip()
    return outList

# For creating SiteUUID
def assignSiteUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "AZwr_S" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist, index=df.index)

print("WaterSourceUUID")
outdf['WaterSourceUUID'] = df.apply(lambda row: retrieveWaterSourceUUID(row['in_WaterSourceName']), axis=1)

print("RegulatoryOverlayUUIDs")
outdf['RegulatoryOverlayUUIDs'] = ""

print("CoordinateAccuracy")
outdf['CoordinateAccuracy'] = "Unspecified"

print("CoordinateMethodCV")
outdf['CoordinateMethodCV'] = "Unspecified"

print("County")
outdf['County'] = df['in_County']

print("EPSGCodeCV")
outdf['EPSGCodeCV'] = "4326"

print("Geometry")
outdf['Geometry'] = ""

print("GNISCodeCV")
outdf['GNISCodeCV'] = ""

print("HUC12")
outdf['HUC12'] = ""

print("HUC8")
outdf['HUC8'] = ""

print("Latitude")
outdf['Latitude'] = df['in_Latitude']

print("Longitude")
outdf['Longitude'] = df['in_Longitude']

print("NHDNetworkStatusCV")
outdf['NHDNetworkStatusCV'] = ""

print("NHDProductCV")
outdf['NHDProductCV'] = ""

print("PODorPOUSite")
outdf['PODorPOUSite'] = df['in_PODorPOUSite']

print("SiteName")
outdf['SiteName'] = df['in_SiteName']

print("SiteNativeID")
outdf['SiteNativeID'] = df.apply(lambda row: assignSiteNativeID(row['in_SiteNativeID']), axis=1)

print("SitePoint")
outdf['SitePoint'] = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = df.apply(lambda row: assignSiteTypeCV(row['in_SiteTypeCV']), axis=1)

print("StateCV")
outdf['StateCV'] = "AZ"

print("USGSSiteID")
outdf['USGSSiteID'] = ""

print("Resetting Index")
outdf.reset_index()

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of SiteNativeID, SiteName, SiteTypeCV
outdf = outdf.drop_duplicates(subset=['SiteNativeID', 'SiteName', 'SiteTypeCV', 'Longitude', 'Latitude'])
outdf = outdf.reset_index(drop=True)
######################################

print("SiteUUID") # has to be one of the last.
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['SiteUUID'] = dftemp.apply(lambda row: assignSiteUUID(row['Count']), axis=1)


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")

dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# SiteUUID
outdf, dfpurge = TestErrorFunctions.SiteUUID_S_Check(outdf, dfpurge)

# RegulatoryOverlayUUIDs
outdf, dfpurge = TestErrorFunctions.RegulatoryOverlayUUIDs_S_Check(outdf, dfpurge)

# WaterSourceUUID
outdf100, dfpurge = TestErrorFunctions.WaterSourceUUID_S_Check(outdf, dfpurge)

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


# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/sites.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/sites_missing.csv', index=False)

print("Done.")
