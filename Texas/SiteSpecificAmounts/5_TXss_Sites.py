# Last Updated: 01/10/2022
# Purpose: To extract TX site specific site use information and populate dataframe for WaDEQA 2.0.
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
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Texas/SiteSpecificAmounts"
os.chdir(workingDir)
fileInput = "RawinputData/P_MasterTXSiteSpecific.csv"
df = pd.read_csv(fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.

watersources_fileInput = "ProcessedInputData/watersources.csv" # watersource input file
df_watersources = pd.read_csv(watersources_fileInput)  # watersources dataframe

fileInput_shape = "RawinputData/shapeGeometery.csv" # geometry input file
dfshape = pd.read_csv(fileInput_shape)  # geometry dataframe

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

# For creating CoordinateMethodCV
def assignCoordinateMethodCV(colrowValue):
    colrowValue = str(colrowValue).strip()
    if colrowValue == "" or pd.isnull(colrowValue):
        outString = "Unspecified"
    else:
        outString = colrowValue
    return outString

# For creating SiteName
def assignSiteName(colrowValue):
    colrowValue = str(colrowValue).strip()
    if colrowValue == "" or pd.isnull(colrowValue):
        outString = "Unspecified"
    else:
        outString = colrowValue
    return outString

# For creating SiteUUID
def assignSiteUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "TXss_S" + string1
    return outstring

# For Creating Geometry
Geometrydict = pd.Series(dfshape.geometry.values, index = dfshape.PWSId).to_dict()
def retrieveGeometry(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()
        try:
            outList = Geometrydict[String1]
        except:
            outList = ''
    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist, index=df.index)

print("RegulatoryOverlayUUIDs")
outdf['RegulatoryOverlayUUIDs'] = ""

print("WaterSourceUUID")
outdf['WaterSourceUUID'] = df.apply(lambda row: retrieveWaterSourceUUID(row['in_WaterSourceNativeID']), axis=1)

print("CoordinateAccuracy")
outdf['CoordinateAccuracy'] = ""

print("CoordinateMethodCV")
outdf['CoordinateMethodCV'] = df.apply(lambda row: assignCoordinateMethodCV(row['in_CoordinateMethodCV']), axis=1) # see pre-processing

print("County")
outdf['County'] = df['in_County'] # see pre-processing

print("EPSGCodeCV")
outdf['EPSGCodeCV'] = "4326"

print("Geometry")
# outdf['Geometry'] = df.apply(lambda row: retrieveGeometry(row['in_SiteNativeID']), axis=1)

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
outdf['PODorPOUSite'] = "POU"

print("SiteName")
outdf['SiteName'] = df.apply(lambda row: assignSiteName(row['in_SiteName']), axis=1) # see pre-processing

print("SiteNativeID")
outdf['SiteNativeID'] = df['in_SiteNativeID'] # see pre-processing

print("SitePoint")
outdf['SitePoint'] = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = "Public Water Systems"

print("StateCV")
outdf['StateCV'] = "TX"

print("USGSSiteID")
outdf['USGSSiteID'] = ""

print("Resetting Index")
outdf.reset_index()

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of WaterSourceUUID, PODorPOUSite, SiteNativeID, SiteName, SiteTypeCV, Longitude & Latitude.
outdf = outdf.drop_duplicates(subset=['WaterSourceUUID', 'PODorPOUSite', 'SiteNativeID', 'SiteName', 'SiteTypeCV', 'Longitude', 'Latitude']).reset_index(drop=True)
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