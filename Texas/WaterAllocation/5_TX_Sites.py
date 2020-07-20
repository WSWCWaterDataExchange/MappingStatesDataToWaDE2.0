#Date Created: 06/12/2020
#Purpose: To extract ID site use information and population dataframe for WaDEQA 2.0.
#Notes: 1) For 'SiteTypeCV', easier to label everything that is not a surface water first.
#       2) For 'CoordinateMethodCV', list out all Idaho specific CV values (should already be in WaDE Vocab).
#       3) Transformer from pyproj is incredibly inefficient.  Did discover trick of preloading necessary coord systems.
#       4) Issue of Transformer from pyproj not working with Anoconda interpretor, had to swap to pip.
#       4) Large files, better to use the '.apply() lambda row' method with a few custom functions, rather than a 'for' loop.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os
from pyproj import Transformer
transformer = Transformer.from_crs(4269, 4326)
# Texas NAD83 projection used by TCEQ = epsg:4269.
# WGS84 projection used by WaDE 2.0 = epsg:4326.


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Texas\WaterAllocation"
os.chdir(workingDir)
fileInput = "RawInputData/P_TexasWRP.csv"
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
def assignSiteName(colrowValue1, colrowValue2):
    if colrowValue1 == '' or pd.isnull(colrowValue1):
        outList = ''
    else:
        colrowValue1 = str(colrowValue1)
        colrowValue2 = str(colrowValue2)
        String1 = colrowValue1.strip()  # remove whitespace chars
        String2 = colrowValue2.strip()  # remove whitespace chars
        try:
            outList = String1 +'_'+ String2 # concatenate Water Right ID and TCEQ ID to give unique ID for each site
        except:
            outList = colrowValue1

    return outList


# For creating SiteTypeCV
UnknownSTCVDict = {
    "Ground Water":"Ground Water",
    "Spring":"spring",
    "Lake":"lake",
    "Pond":"pond",
    "Canal":"Canal",
    "Fork":"Surface Water",
    "Waste":"waste water",
    "Drain":"drain",
    "Reservoir":"reservoir",
    "Ditch":"ditch"}
def assignSiteTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = String1 #Changed from UnknownSTCVDict since TCEQ data includes site type
        except:
            outList = "Surface Water"

    return outList


# For creating CoordinateMethodCV
UnknownCMCVDict = {
    "GPS" : "GPS",
    "Digitized" : "Digitized",
    "Survey" : "Surveyed",
    "Parcel" : "ID parcel by map",
    "Geocoded" : "ID Geocoded",
    "Q" : "ID Q",
    "QQ" : "ID QQ",
    "QQQ" : "ID QQQ",
    "WMIS QQ Crossover" : "ID QQ",
    "WMIS QQQ Crossover" : "ID QQQ",
    "Online Claim" : "ID Online Claim"}
def assignCoordinateMethodCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = UnknownCMCVDict[String1]
        except:
            outList = "Unspecified"

    return outList


# For creating SiteUUID
def assignSiteUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "TX_" + string1
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

###################################
 # Lat and Long have to process first as you cannot assign a constant value to a df without an index.
print("Latitude")
outdf['Latitude'] = df.apply(lambda row: assignLat(row['LAT_DD'], row['LONG_DD']), axis=1)

print("Longitude")
outdf['Longitude'] = df.apply(lambda row: assignLong(row['LAT_DD'], row['LONG_DD']), axis=1)
###################################

print("CoordinateAccuracy")  # Hardcoded
outdf["CoordinateAccuracy"] = 'Unknown'

outdf['CoordinateMethodCV'] = 'Digitized'

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

print("NHDNetworkStatusCV")  # Hardcoded
outdf.NHDNetworkStatusCV = ""

print("NHDProductCV")  # Hardcoded
outdf.NHDProductCV = ""

print("SiteName")
outdf['SiteName'] = df.apply(lambda row: assignSiteName(row['WR_ID'], row['TCEQ_ID']), axis=1)

print("SiteNativeID")
outdf['SiteNativeID'] = df['WR_ID']

print("SitePoint")  # Hardcoded
outdf.SitePoint = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = df.apply(lambda row: assignSiteTypeCV(row['TYPE']), axis=1)

print("StateCV")  #
outdf.StateCV = "TX"

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