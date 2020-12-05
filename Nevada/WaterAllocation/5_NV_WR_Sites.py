#Date Created: 07/17/2020
#Purpose: To extract NV site use information and population dataframe for WaDEQA 2.0.
#Notes:


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os
# from pyproj import Transformer, transform


# Inputs
############################################################################
print("Reading input csv...")
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Nevada/WaterAllocation"
os.chdir(workingDir)
fileInput="RawInputData/P_MastersNV.csv"
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
def assignSiteName(colrowValue):
    colrowValuestr = str(colrowValue)
    colrowValuestr = colrowValuestr.strip()
    if ((colrowValuestr == "") or pd.isnull(colrowValuestr) or colrowValuestr == 'nan'):
        outList = "Unknown"
    else:
        outList = colrowValuestr
    return outList

# For creating SiteTypeCV
UnknownSTCVDict = {
    "EFF":"Effluent",
    "GEO":"Geothermal",
    "LAK":"lake",
    "OGW":"Other Ground Water",
    "OSW":"Other Surface Water",
    "RES":"Reservoir",
    "SPR":"Spring",
    "STO":"Storage",
    "STR":"stream",
    "UG":"Underground",
    "UKN":"unknown"}
def assignSiteTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = UnknownSTCVDict[String1]
        except:
            outList = "Unknown"
    return outList

# For creating County
CountyDict = {
    "HU" : "Humboldt",
    "CC" : "Carson City",
    "CH" : "Churchill",
    "CL" : "Clark",
    "DO" : "Douglas",
    "EL" : "Elko",
    "ES" : "Esmerelda",
    "EU" : "Eureka",
    "LA" : "Lander",
    "LI" : "Lincoln",
    "LY": "Lyon",
    "MI": "Mineral",
    "NY": "Nye",
    "PE": "Pershing",
    "ST": "Storey",
     "": "Unknown",
    "WA": "Washoe",
    "WP": "White Pine",
    "UK": "Unknown"}
def assignCounty(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = CountyDict[String1]
        except:
            outList = "Unknown"
    return outList


# For creating SiteUUID
def assignSiteUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "NVwr_S" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist, index=df.index)

print("CoordinateAccuracy")  # Hardcoded
outdf["CoordinateAccuracy"] = 'Unknown'

print("CoordinateMethodCV")
outdf['CoordinateMethodCV'] = 'Digitized'

print("County")  # Hardcoded
outdf.County = df.apply(lambda row: assignCounty(row['county_x']), axis=1)

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
outdf['Latitude'] = df['y']

print("Longitude")
outdf['Longitude'] = df['x']

print("NHDNetworkStatusCV")  # Hardcoded
outdf.NHDNetworkStatusCV = ""

print("NHDProductCV")  # Hardcoded
outdf.NHDProductCV = ""

print("SiteName")
outdf['SiteName'] = df.apply(lambda row: assignSiteName(row['site_name']), axis=1)

print("SiteNativeID")  # Hardcoded
outdf.SiteNativeID = ""

print("SitePoint")  # Hardcoded
outdf.SitePoint = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = df.apply(lambda row: assignSiteTypeCV(row['source']), axis=1)

print("StateCV")  # Hardcoded
outdf.StateCV = "NV"

print("USGSSiteID")  # Hardcoded
outdf.USGSSiteID = ""

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of SiteNativeID, SiteName, SiteTypeCV
outdf = outdf.drop_duplicates(subset=['SiteName', 'SiteTypeCV'])
outdf = outdf.reset_index(drop=True)
outdfpurge = outdf.loc[(outdf['Longitude'].isnull()) | (outdf['Latitude'].isnull())]
######################################

print("SiteUUID") # has to be one of the last.
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['SiteUUID'] = dftemp.apply(lambda row: assignSiteUUID(row['Count']), axis=1)


#Error Checking each Field
############################################################################
print("Error checking each field. Purging bad inputs.")
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
print("Exporting dataframe to csv...")
outdf.to_csv('ProcessedInputData/sites.csv', index=False)  # The output

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/sites_missing.csv')  # index=False,

print("Done")



#Code Not Used
# # Check required fields are not null
# ############################################################################
# print("Checking required is not null...")  # Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
# outdf = outdf.replace('', np.nan) #replace blank strings by NaN, if there are any
# # Dataframe to show mandatory fields that had a blank input form df.
# outdf_nullMand = outdf.loc[
#     (outdf["SiteUUID"].isnull()) | (outdf["SiteUUID"] == '') |
#     (outdf["SiteName"].isnull()) | (outdf["SiteName"] == '') |
#     (outdf["CoordinateMethodCV"].isnull()) | (outdf["CoordinateMethodCV"] == '') |
#     (outdf["EPSGCodeCV"].isnull()) | (outdf["EPSGCodeCV"] == '')]

#
# if(len(outdf_nullMand.index) > 0):
#     outdf_nullMand.to_csv('ProcessedInputData/sites_mandatoryFieldMissing.csv')  # index=False,