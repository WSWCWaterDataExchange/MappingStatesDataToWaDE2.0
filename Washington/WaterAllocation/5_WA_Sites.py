#Date Created: 04/01/2020
#Purpose: To extract WA site use information and population dataframe for WaDEQA 2.0.
#Notes: 1) Have to convert from epsg:2927 - to - epsg:4326 in order for lat and long to work in WaDE 2.0.
#       2) Transformer from pyproj is incredibly inefficient.  Did discover trick of preloading necessary coord systems.
#       3) Large files, better to use the '.apply() lambda row' method with a few custom functions, rather than a 'for' loop.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os
from pyproj import Transformer, transform

transformer = Transformer.from_proj(2927, 4326)  # A trick to drastically optimize the Transformer of pyproj.
# Washignton projection = EPSG:2927. WGS84 projection used by WaDE 2.0 = epsg:4326.

# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Washington/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/P_WashingtonMaster.csv"
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

# For Creating CoordinateAccuracy
coordinateAccuracyDictWA = {
    "C":"field checked (without GPS)",
    "G":"field checked with GPS",
    "P":"proposed (does not exist in real world)",
    "PA":"proposed and All-right (does not exist in real world)",
    "PD":"proposed and Dubious (does not exist in real world)",
    "PM":"proposed and Multiple Dubious (does not exist in real world)",
    "PX":"proposed and Centroid Dubious (does not exist in real world)",
    "U":"unchecked",
    "UA":"unchecked and All-right",
    "UD":"unchecked and Dubious",
    "UM":"unchecked and Multiple Dubious",
    "UX":"unchecked and Centroid Dubious",
    "W":"from well log, unchecked",
    "WA":"from well log, unchecked and All-right",
    "WD":"from well log, unchecked and Dubious",
    "WX":"from well log, unchecked and Centroid Dubious"
}
def assignCoordinateAccuracy(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        keyStr = colrowValue.strip()
        try:
            outList = coordinateAccuracyDictWA[keyStr]
        except:
            outList = ''
    return outList

# For creating SiteTypeCV
UnknownSTCVDict = {
    "GC":"ground water collector",
    "HW":"headworks gravity flow (or surface water device unknown)",
    "ID":"irrigation dam",
    "MW":"monitoring well",
    "PM":"surface water pump",
    "RD":"reservoir dam",
    "WL":"well (or ground water device unknown)"}
def assignSiteTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unknown'
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = UnknownSTCVDict[String1]
        except:
            outList = 'Unknown'

    return outList

# For converting projection latitude.
def assignLat(colrowValueLat, colrowValueLong):
    lat, long = transformer.transform(colrowValueLat, colrowValueLong)
    return lat

# For converting projection longitude.
def assignLong(colrowValueLat, colrowValueLong):
    lat, long = transformer.transform(colrowValueLat, colrowValueLong)
    return long

# For creating SiteUUID
def assignSiteUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "WAwr_S" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist, index=df.index)

print("CoordinateAccuracy")
outdf['CoordinateAccuracy'] = df.apply(lambda row: assignCoordinateAccuracy(row['Location_C']), axis=1)

print("againCoordinateMethodCV")
outdf.CoordinateMethodCV = 'Unspecified'

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
outdf['Latitude'] = df.apply(lambda row: assignLat(row['POINT_X'], row['POINT_Y']), axis=1)

print("Longitude")
outdf['Longitude'] = df.apply(lambda row: assignLong(row['POINT_X'], row['POINT_Y']), axis=1)

print("NHDNetworkStatusCV")
outdf.NHDNetworkStatusCV = ""

print("NHDProductCV")
outdf.NHDProductCV = ""

print("PODorPOUSite")
outdf.PODorPOUSite = 'POD'

print("SiteName")
outdf.SiteName = 'Unspecified'

print("SiteNativeID")
outdf['SiteNativeID'] = df['D_Point_ID'].astype(str) # Native dbtype is float. Need to return this value as a string

print("SitePoint")
outdf.SitePoint = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = df.apply(lambda row: assignSiteTypeCV(row['D_Point_Ty']), axis=1)

print("StateCV")
outdf.StateCV = "WA"

print("USGSSiteID")
outdf.USGSSiteID = ""

print("Resetting Index")
outdf.reset_index()

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of SiteNativeID, SiteName, SiteTypeCV, Longitude & Latitude
outdf = outdf.drop_duplicates(subset=['SiteNativeID', 'SiteTypeCV', 'Longitude', 'Latitude'])
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

# SiteUUID_nvarchar(200)_
mask = outdf.loc[ (outdf["SiteUUID"].isnull()) | (outdf["SiteUUID"] == '') | (outdf['SiteUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad SiteUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[ (outdf["SiteUUID"].isnull()) | (outdf["SiteUUID"] == '') | (outdf['SiteUUID'].str.len() > 200) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# CoordinateAccuracy_nvarchar(255)_Yes
mask = outdf.loc[ outdf["CoordinateAccuracy"].str.len() > 255 ].assign(ReasonRemoved='Bad CoordinateAccuracy').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["CoordinateAccuracy"].str.len() > 255 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# CoordinateMethodCV_nvarchar(100)_-
mask = outdf.loc[ (outdf["CoordinateMethodCV"].isnull()) | (outdf["CoordinateMethodCV"] == '') | (outdf['CoordinateMethodCV'].str.len() > 100) ].assign(ReasonRemoved='Bad CoordinateMethodCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[ (outdf["CoordinateMethodCV"].isnull()) | (outdf["CoordinateMethodCV"] == '') | (outdf['CoordinateMethodCV'].str.len() > 100) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# County_nvarchar(20)_Yes
mask = outdf.loc[ outdf["County"].str.len() > 20 ].assign(ReasonRemoved='Bad County').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["County"].str.len() > 20 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# EPSGCodeCV_nvarchar(50)_-
mask = outdf.loc[ (outdf["EPSGCodeCV"].isnull()) | (outdf["EPSGCodeCV"] == '') | (outdf['EPSGCodeCV'].str.len() > 50) ].assign(ReasonRemoved='Bad EPSGCodeCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[ (outdf["EPSGCodeCV"].isnull()) | (outdf["EPSGCodeCV"] == '') | (outdf['EPSGCodeCV'].str.len() > 50) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# Geometry_geometry_Yes
# ???? How to check for geometry datatype

# GNISCodeCV_nvarchar(250)_Yes
mask = outdf.loc[ outdf["GNISCodeCV"].str.len() > 250 ].assign(ReasonRemoved='Bad GNISCodeCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["GNISCodeCV"].str.len() > 250 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# HUC12_nvarchar(20)_Yes
mask = outdf.loc[ outdf["HUC12"].str.len() > 20 ].assign(ReasonRemoved='Bad HUC12').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["HUC12"].str.len() > 20 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# HUC8_nvarchar(20)_Yes
mask = outdf.loc[ outdf["HUC8"].str.len() > 20 ].assign(ReasonRemoved='Bad HUC8').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["HUC8"].str.len() > 20 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# Latitude_float_-
mask = outdf.loc[ (outdf["Latitude"].isnull()) | (outdf["Latitude"] == '') | (outdf["Latitude"] < 20) ].assign(ReasonRemoved='Bad Latitude').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ (outdf["Latitude"].isnull()) | (outdf["Latitude"] == '') | (outdf["Latitude"] < 20) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# Longitude_float_-
mask = outdf.loc[ (outdf["Longitude"].isnull()) | (outdf["Longitude"] == '') | (outdf["Longitude"] > -80) ].assign(ReasonRemoved='Bad Longitude').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ (outdf["Longitude"].isnull()) | (outdf["Longitude"] == '') | (outdf["Longitude"] > -80) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# NHDNetworkStatusCV_nvarchar(50)_Yes
mask = outdf.loc[ outdf["NHDNetworkStatusCV"].str.len() > 50 ].assign(ReasonRemoved='Bad NHDNetworkStatusCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["NHDNetworkStatusCV"].str.len() > 50 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# NHDProductCV_nvarchar(50)_Yes
mask = outdf.loc[ outdf["NHDProductCV"].str.len() > 50 ].assign(ReasonRemoved='Bad NHDProductCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["NHDProductCV"].str.len() > 50 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# PODorPOUSite_nvarchar(50)_Yes
mask = outdf.loc[ outdf["PODorPOUSite"].str.len() > 50 ].assign(ReasonRemoved='Bad PODorPOUSite').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["PODorPOUSite"].str.len() > 50 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# SiteName_nvarchar(500)_
mask = outdf.loc[ (outdf["SiteName"].isnull()) | (outdf["SiteName"] == '') | (outdf['SiteName'].str.len() > 500) ].assign(ReasonRemoved='Bad SiteName').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[ (outdf["SiteName"].isnull()) | (outdf["SiteName"] == '') | (outdf['SiteName'].str.len() > 500) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# SiteNativeID_nvarchar(50)_Yes
mask = outdf.loc[ outdf["SiteNativeID"].str.len() > 50 ].assign(ReasonRemoved='Bad SiteNativeID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["SiteNativeID"].str.len() > 50 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# SitePoint_geometry_Yes
# ???? How to check for geometry datatype

# SiteTypeCV_nvarchar(100)_Yes
mask = outdf.loc[ outdf["SiteTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Bad SiteTypeCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["SiteTypeCV"].str.len() > 100 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# StateCV_nvarchar(2)_Yes
mask = outdf.loc[ outdf["StateCV"].str.len() > 2 ].assign(ReasonRemoved='Bad StateCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["StateCV"].str.len() > 2 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# USGSSiteID_nvarchar(250)_Yes
mask = outdf.loc[ outdf["USGSSiteID"].str.len() > 250 ].assign(ReasonRemoved='Bad USGSSiteID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["USGSSiteID"].str.len() > 250 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)


# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")
# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/sites.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/sites_missing.csv')  # index=False,

print("Done.")

