#Date Created: 10/22/2020
#Purpose: To extract ID site use information and population dataframe for WaDEQA 2.0.
#Notes: 1) For 'SiteTypeCV', easier to label everything that is not a surface water first.
#       2) For 'CoordinateMethodCV', list out all Idaho specific CV values (should already be in WaDE Vocab).
#       3) Have to convert from epsg:8826 - to - epsg:4326 in order for lat and long to work in WaDE 2.0.
#       4) Transformer from pyproj is incredibly inefficient.  Did discover trick of preloading necessary coord systems.
#       5) Large files, better to use the '.apply() lambda row' method with a few custom functions, rather than a 'for' loop.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os
from pyproj import Transformer, transform

# Note: Idaho Transverse Mercator projection used by IDWR = epsg:8826.
# Note: WGS84 projection used by WaDE 2.0 = epsg:4326.
transformer = Transformer.from_proj(8826, 4326)  # A trick to drastically optimize the Transformer of pyproj.

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

# For converting IDWR projection latitude.
def assignLat(colrowValueLat, colrowValueLong):
    lat, long = transformer.transform(colrowValueLat, colrowValueLong)
    return lat

# For converting IDWR projection longitude.
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
    outstring = "ID_S" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf=pd.DataFrame(columns=columnslist)

print("CoordinateAccuracy")  # Hardcoded
outdf.CoordinateAccuracy = ""

print("CoordinateMethodCV")
outdf['CoordinateMethodCV'] = df.apply(lambda row: assignCoordinateMethodCV(row['DataSource_POD']), axis=1)

print("County")  # Hardcoded
outdf.County = ""

print("EPSGCodeCV")  # Hardcoded
outdf.EPSGCodeCV = 'EPSG:4326'

print("Geometry") # Hardcoded
outdf.Geometry = ""

print("GNISCodeCV")  # Hardcoded
outdf.GNISCodeCV = ""

print("HUC12")  # Hardcoded
outdf.HUC12 = ""

print("HUC8")  # Hardcoded
outdf.HUC8 = ""

print("Latitude")
outdf['Latitude'] = df.apply(lambda row: assignLat(row['X_POD'], row['Y_POD']), axis=1)

print("Longitude")
outdf['Longitude'] = df.apply(lambda row: assignLong(row['X_POD'], row['Y_POD']), axis=1)

print("NHDNetworkStatusCV")  # Hardcoded
outdf.NHDNetworkStatusCV = ""

print("NHDProductCV")  # Hardcoded
outdf.NHDProductCV = ""

print("SiteName")
outdf['SiteName'] = df.apply(lambda row: assignSiteName(row['DiversionName_POD']), axis=1)

print("SiteNativeID")
outdf['SiteNativeID'] = df['PointOfDiversionID_POD'].astype(str)

print("SitePoint")  # Hardcoded
outdf.SitePoint = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = df['inputSiteType']
# outdf['SiteTypeCV'] = df.apply(lambda row: assignSiteTypeCV(row['Source']), axis=1)

print("StateCV")  # Hardcoded
outdf.StateCV = "ID"

print("USGSSiteID")  # Hardcoded
outdf.USGSSiteID = ""

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of SiteNativeID, SiteName, SiteTypeCV
outdf = outdf.drop_duplicates(subset=['SiteNativeID', 'SiteName', 'SiteTypeCV'])
outdf = outdf.reset_index(drop=True)
outdfpurge = outdf.loc[(outdf['Longitude'].isnull()) | (outdf['Latitude'].isnull())]
######################################

print("SiteUUID") # has to be one of the last.
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['SiteUUID'] = dftemp.apply(lambda row: assignSiteUUID(row['Count']), axis=1)


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")  # Hardcoded
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

# Latitude_float_Yes
mask = outdf.loc[ (outdf["Latitude"].isnull()) | (outdf["Latitude"] == '') | (outdf["Latitude"] < 20) ].assign(ReasonRemoved='Bad Latitude').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ (outdf["Latitude"].isnull()) | (outdf["Latitude"] == '') | (outdf["Latitude"] < 20) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# Longitude_float_Yes
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