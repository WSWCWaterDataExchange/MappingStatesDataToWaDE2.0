#Date Created: 04/08/2020
#Purpose: To extract ND site use information and population dataframe for WaDEQA 2.0.
#Notes:


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/NorthDakota/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/P_NorthDakotaMaster.csv"
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

# For creating SiteNativeID
def assignSiteNativeID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        outList = colrowValue.strip()
    return outList

# For creating WaterSourceTypeCV
def assignSiteTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        outList = colrowValue.strip()
    return outList

# For creating SiteUUID
def assignSiteUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "NDwr_S" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist, index=df.index)

print("CoordinateAccuracy")
outdf['CoordinateAccuracy'] = ''

print("CoordinateMethodCV")
outdf['CoordinateMethodCV'] = 'Unspecified'

print("County")
outdf['County'] = df['county']

print("EPSGCodeCV")
outdf['EPSGCodeCV'] = 'EPSG:4326'

print("Geometry")
outdf['Geometry'] = ""

print("GNISCodeCV")
outdf['GNISCodeCV'] = ""

print("HUC12")
outdf['HUC12'] = ""

print("HUC8")
outdf['HUC8'] = ""

print("Latitude")
outdf['Latitude'] = df['latitude']

print("Longitude")
outdf['Longitude'] = df['longitude']

print("NHDNetworkStatusCV")
outdf['NHDNetworkStatusCV'] = ""

print("NHDProductCV")
outdf['NHDProductCV'] = ""

print("PODorPOUSite")
outdf['PODorPOUSite'] = "POD"

print("SiteName")
outdf['SiteName'] = "Unspecified"

print("SiteNativeID")
outdf['SiteNativeID'] = df.apply(lambda row: assignSiteNativeID(row['pod']), axis=1)

print("SitePoint")
outdf['SitePoint'] = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = df.apply(lambda row: assignSiteTypeCV(row['source']), axis=1)

print("StateCV")
outdf['StateCV'] = "ND"

print("USGSSiteID")
outdf['USGSSiteID'] = ""

print("Resetting Index")
outdf.reset_index()
outdf = outdf.replace(np.nan, '')

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of SiteNativeID, SiteName, SiteTypeCV, Longitude, and Latitude
outdf = outdf.drop_duplicates(subset=['SiteNativeID', 'SiteName', 'SiteTypeCV', 'Longitude', 'Latitude']).reset_index()
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
