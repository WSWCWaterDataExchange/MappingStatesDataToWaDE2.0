#Date Created: 02/28/2020
#Author: Ryan James WSWC
#Purpose: To extract CO site use information and population DataFrame for local WaDEQA 2.0.
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

transformer = Transformer.from_proj(8826, 4326)  # A trick to drastically optimize the Transformer of pyproj.
# Idaho Transverse Mercator projection used by IDWR = epsg:8826.
# WGS84 projection used by WaDE 2.0 = epsg:4326.

# Inputs
############################################################################
print("Reading input csv...")
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Colorado/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/DWR_Water_Right_-_Net_Amounts.csv"
df = pd.read_csv(fileInput)

columns = [
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
# UnknownSNameDict = {
#     "Ground Water":"Unnamed",
#     "Spring":"Unnamed",
#     "Unnamed Stream":"Unnamed",
#     "Unnamed Streams":"Unnamed"}
# def assignSiteName(colrowValue):
#     if colrowValue == '' or pd.isnull(colrowValue):
#         outList = ''
#     else:
#         String1 = colrowValue.strip()  # remove whitespace chars
#         try:
#             outList = UnknownSNameDict[String1]
#         except:
#             outList = colrowValue
#
#     return outList


# For creating SiteTypeCV
def assignSiteTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unknown'
    else:
        outList = colrowValue.strip()  # remove whitespace chars
    return outList

# For creating SiteTypeCV
def assignCoordinateMethodCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unspecified'
    elif colrowValue == 'Unable to spot':
        outList = 'Unspecified'
    else:
        outList = colrowValue  # remove whitespace chars
    return outList

# For creating SiteUUID
def assignSiteUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "CO_" + string1
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
outdf=pd.DataFrame(columns=columns)

print("CoordinateAccuracy")  # Hardcoded
outdf.CoordinateAccuracy = "Unknown"

print("CoordinateMethodCV")
outdf['CoordinateMethodCV'] = df.apply(lambda row: assignCoordinateMethodCV(row['Location Accuracy']), axis=1)

print("County")  # Hardcoded
outdf.County = ""

print("EPSGCodeCV")  # Hardcoded
outdf.EPSGCodeCV = 'EPSG:4326'

print("Geometry") # Hardcoded
outdf.Geometry = ""

print("GNISCodeCV")  # Hardcoded
#outdf['GNISCodeCV'] = df['GNIS ID']
outdf.GNISCodeCV = ''

print("HUC12")  # Hardcoded
outdf.HUC12 = ""

print("HUC8")  # Hardcoded
outdf.HUC8 = ""

print("Latitude")
#outdf['Latitude'] = df.apply(lambda row: assignLat(row['X'], row['Y']), axis=1)
outdf['Latitude'] = df['Latitude']

print("Longitude")
#outdf['Longitude'] = df.apply(lambda row: assignLong(row['X'], row['Y']), axis=1)
outdf['Longitude'] = df['Longitude']

print("NHDNetworkStatusCV")  # Hardcoded
outdf.NHDNetworkStatusCV = ""

print("NHDProductCV")  # Hardcoded
outdf.NHDProductCV = ""

print("SiteName")
#outdf['SiteName'] = df.apply(lambda row: assignSiteName(row['Source']), axis=1)
outdf['SiteName'] = df['Structure Name']

print("SiteNativeID")
outdf['SiteNativeID'] = df['WDID']

print("SitePoint")  # Hardcoded
outdf.SitePoint = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = df.apply(lambda row: assignSiteTypeCV(row['Structure Type']), axis=1)

print("StateCV")  #
outdf.StateCV = "CO"

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


# Check required fields are not null
############################################################################
print("Checking required is not null...")  # Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan) #replace blank strings by NaN, if there are any
# Dataframe to show mandatory fields that had a blank input form df.
outdf_nullMand = outdf.loc[
    (outdf["SiteUUID"].isnull()) | (outdf["SiteUUID"] == '') |
    (outdf["SiteName"].isnull()) | (outdf["SiteName"] == '') |
    (outdf["CoordinateMethodCV"].isnull()) | (outdf["CoordinateMethodCV"] == '') |
    (outdf["EPSGCodeCV"].isnull()) | (outdf["EPSGCodeCV"] == '')]



# Checking Dataframe data types
############################################################################
print(outdf.dtypes)


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")
outdf.to_csv('ProcessedInputData/sites.csv', index=False)  # The output


#Report missing values if need be to separate csv
if len(outdfpurge.index) > 0:
    outdfpurge.to_csv('ProcessedInputData/sites_missing.csv')    #index=False,
    dropIndex = outdf.loc[(outdf['Longitude'].isnull()) | (outdf['Latitude'].isnull())].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/sites_mandatoryFieldMissing.csv')  # index=False,

print("Done")