#Date Created: 10/22/2020
#Purpose: To extract ID site use information and population dataframe for WaDEQA 2.0.
#Notes: 1) For 'SiteTypeCV', easier to label everything that is not a surface water first.
#       2) For 'CoordinateMethodCV', list out all Idaho specific CV values (should already be in WaDE Vocab).
#       3) Have to convert from epsg:8826 - to - epsg:4326 in order for lat and long to work in WaDE 2.0.

# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os
from pyproj import Transformer, transform
transformer = Transformer.from_proj(8826, 4326)  # A trick to drastically optimize the Transformer of pyproj.
# Idaho projection = EPSG:8826.  WGS84 projection used by WaDE 2.0 = epsg:4326.


# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Idaho/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/P_IdahoMaster.csv"
df = pd.read_csv(fileInput)

columnslist = [
    "SiteUUID",
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
# For creating CoordinateMethodCV
def assignCoordinateMethodCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        outList = String1
    return outList

# For converting projection latitude.
def assignLat(colrowValueLat, colrowValueLong):
    lat, long = transformer.transform(colrowValueLat, colrowValueLong)
    return lat

# For converting projection longitude.
def assignLong(colrowValueLat, colrowValueLong):
    lat, long = transformer.transform(colrowValueLat, colrowValueLong)
    return long

# For creating SiteName
def assignSiteName(colrowValue):
    colrowValue = str(colrowValue)
    colrowValue = colrowValue.strip()
    if colrowValue == "" or colrowValue == "nan":
        outList = "Unspecified"
    else:
        outList = colrowValue
    return outList

# For creating SiteUUID
def assignSiteUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "IDwr_S" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf=pd.DataFrame(columns=columnslist)

print("CoordinateAccuracy")
outdf.CoordinateAccuracy = ""

print("CoordinateMethodCV")
outdf['CoordinateMethodCV'] = df.apply(lambda row: assignCoordinateMethodCV(row['DataSource_POD']), axis=1)

print("County")
outdf.County = ""

print("EPSGCodeCV")
outdf.EPSGCodeCV = 'EPSG:4326'

print("Geometry") # Hardcoded
outdf.Geometry = ""

print("GNISCodeCV")
outdf.GNISCodeCV = ""

print("HUC12")
outdf.HUC12 = ""

print("HUC8")
outdf.HUC8 = ""

print("Latitude")
outdf['Latitude'] = df.apply(lambda row: assignLat(row['X_POD'], row['Y_POD']), axis=1)

print("Longitude")
outdf['Longitude'] = df.apply(lambda row: assignLong(row['X_POD'], row['Y_POD']), axis=1)

print("NHDNetworkStatusCV")
outdf.NHDNetworkStatusCV = ""

print("NHDProductCV")
outdf.NHDProductCV = ""

print("PODorPOUSite")
outdf['PODorPOUSite'] = "POD"

print("SiteName")
outdf['SiteName'] = df.apply(lambda row: assignSiteName(row['DiversionName_POD']), axis=1)

print("SiteNativeID")
outdf['SiteNativeID'] = df['PointOfDiversionID_POD'].astype(str)

print("SitePoint")
outdf.SitePoint = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = df['inputSiteType']

print("StateCV")
outdf.StateCV = "ID"

print("USGSSiteID")
outdf.USGSSiteID = ""

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of SiteNativeID, SiteName, SiteTypeCV
outdf = outdf.drop_duplicates(subset=['SiteName', 'SiteNativeID', 'SiteTypeCV',  'Latitude', 'Longitude'])
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