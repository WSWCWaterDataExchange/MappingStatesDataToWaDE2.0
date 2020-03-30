#Date Created: 03/13/2020
#Purpose: To extract ID site use information and population dataframe for WaDEQA 2.0.
#Notes: 1) Have to convert from epsg:26912 - to - epsg:4326 in order for lat and long to work in WaDE 2.0.
#       2) Transformer from pyproj is incredibly inefficient.  Did discover trick of preloading necessary coord systems.
#       3) Large files, better to use the '.apply() lambda row' method with a few custom functions, rather than a 'for' loop.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os
from pyproj import Transformer, transform

transformer = Transformer.from_proj(26912, 4326)  # A trick to drastically optimize the Transformer of pyproj.
# Utah projection = EPSG:26912.  WGS84 projection used by WaDE 2.0 = epsg:4326.

# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/P_UtahMaster.csv"
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
# For creating SiteName
UnknownSNameDict = {
    "Ground Water":"Unnamed",
    "Spring":"Unnamed",
    "Unnamed Stream":"Unnamed",
    "Unnamed Streams":"Unnamed"}
def assignSiteName(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = UnknownSNameDict[String1]
        except:
            outList = colrowValue

    return outList

# For creating SiteTypeCV
UnknownSTCVDict = {
    "A": "Abandoned",
    "D": "Drain",
    "C": "Sewage",
    "F": "Sewage",
    "N": "Sewage",
    "P": "Sewage",
    "G": "Spring",
    "R": "Point of Rediversion",
    "S": "Surface",
    "T": "Point of Return",
    "U": "Underground"
}
def assignSiteTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = UnknownSTCVDict[String1]
        except:
            outList = ""

    return outList

# For creating SiteUUID
def assignSiteUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "UT_" + string1
    return outstring

# For converting IDWR projection latitude.
def assignLat(colrowValueLat, colrowValueLong):
    lat, long = transformer.transform(colrowValueLat, colrowValueLong)
    return lat


# For converting IDWR projection longitude.
def assignLong(colrowValueLat, colrowValueLong):
    lat, long = transformer.transform(colrowValueLat, colrowValueLong)
    return long


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist, index=df.index)

print("againCoordinateAccuracy")  # Hardcoded
outdf.CoordinateAccuracy = 'Unknown'

print("againCoordinateMethodCV")
outdf.CoordinateMethodCV = 'Unspecified'

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
outdf['Latitude'] = df.apply(lambda row: assignLat(row['X_UTM'], row['Y_UTM']), axis=1)

print("Longitude")
outdf['Longitude'] = df.apply(lambda row: assignLong(row['X_UTM'], row['Y_UTM']), axis=1)

print("NHDNetworkStatusCV")  # Hardcoded
outdf.NHDNetworkStatusCV = ""

print("NHDProductCV")  # Hardcoded
outdf.NHDProductCV = ""

print("SiteName")
outdf.SiteName = 'Not Provided'

print("SiteNativeID")
outdf['SiteNativeID'] = df['SiteLocation']

print("SitePoint")  # Hardcoded
outdf.SitePoint = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = df.apply(lambda row: assignSiteTypeCV(row['POD_TYPE']), axis=1)

print("StateCV")  # Hardcoded
outdf.StateCV = "UT"

print("USGSSiteID")  # Hardcoded
outdf.USGSSiteID = ""

print("Resetting Index")  # Hardcoded
outdf.reset_index()

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of SiteNativeID, SiteName, SiteTypeCV
outdf = outdf.drop_duplicates(subset=['SiteNativeID', 'SiteName', 'SiteTypeCV', 'Longitude', 'Latitude'])
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
# ???? Don't we consider null lat values bad?

# Longitude_float_Yes
# ???? Don't we consider null long values bad?

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
    dfpurge.to_csv('ProcessedInputData/sites.csv')  # index=False,

print("Done.")

