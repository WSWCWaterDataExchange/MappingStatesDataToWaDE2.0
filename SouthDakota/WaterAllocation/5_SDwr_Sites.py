# Date Update: 03/29/2023
# Purpose: To extract SD site information and populate dataframe for WaDE_QA 2.0.
# Notes: N/A


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Custom Libraries
############################################################################
import sys
# columns
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/MappingFunctions")
import GetColumnsFile

# Test WaDE Data for any Errors
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/ErrorCheckCode")
import TestErrorFunctionsFile


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "G:/Shared drives/WaDE Data/SouthDakota/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/Pwr_SouthDakotaMain.zip"
df = pd.read_csv(fileInput, compression='zip')

watersources_fileInput = "ProcessedInputData/watersources.csv"
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe

try:
    fileInput_shape = "RawinputData/P_utGeometry.csv"
    dfshape = pd.read_csv(fileInput_shape)
    Geometrydict = pd.Series(dfshape.geometry.values, index=dfshape.in_SiteNativeID).to_dict()
except:
    print("no geometry data to worry about.")

# WaDE columns
SitesColumnsList = GetColumnsFile.GetSitesColumnsFunction()


# Custom Functions
############################################################################

# For creating WaterSourceUUID
WaterSourceUUIDdict = pd.Series(df_watersources.WaterSourceUUID.values, index = df_watersources.WaterSourceNativeID).to_dict()
def retrieveWaterSourceUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        strVal = str(colrowValue).strip()
        outList = WaterSourceUUIDdict[strVal]
    return outList

# For Creating Geometry
def retrieveGeometry(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = Geometrydict[String1]
        except:
            outList = ''
    return outList

# For creating SiteUUID
def assignSiteUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "SDwr_S" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(index=df.index, columns=SitesColumnsList)  # The output dataframe for CSV.

print("WaterSourceUUIDs")
outdf['WaterSourceUUIDs'] = df.apply(lambda row: retrieveWaterSourceUUID(row['in_WaterSourceNativeID']), axis=1)

print("RegulatoryOverlayUUIDs")
outdf['RegulatoryOverlayUUIDs'] = ""

print("CoordinateAccuracy")
outdf['CoordinateAccuracy'] = df['in_CoordinateAccuracy']

print("CoordinateMethodCV")
outdf['CoordinateMethodCV'] = df['in_CoordinateMethodCV']

print("County")
outdf['County'] = df['in_County']

print("EPSGCodeCV")
outdf['EPSGCodeCV'] = "4326"

print("Geometry")
try:
    outdf['Geometry'] = df.apply(lambda row: retrieveGeometry(row['in_SiteNativeID']), axis=1)
except:
    print("...no geometry data.")
    outdf['Geometry'] = ""

print("GNISCodeCV")
outdf['GNISCodeCV'] = ""

print("HUC12")
outdf['HUC12'] = df['in_HUC12']

print("HUC8")
outdf['HUC8'] = df['in_HUC8']

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
outdf['SiteNativeID'] = df['in_SiteNativeID']

print("SitePoint")
outdf['SitePoint'] = ""

print("SiteTypeCV")
outdf['SiteTypeCV'] = df['in_SiteTypeCV']

print("StateCV")
outdf['StateCV'] = df['in_StateCV']

print("USGSSiteID")
outdf['USGSSiteID'] = ""

print("Adding Data Assessment UUID")
outdf['WaDEUUID'] = df['WaDEUUID']

print("Resetting Index")
outdf.reset_index()

print("Joining outdf duplicates based on key fields...")
outdf = outdf.replace(np.nan, "")  # Replaces NaN values with blank.
groupbyList = ['PODorPOUSite', 'SiteNativeID', 'SiteName', 'SiteTypeCV', 'Longitude', 'Latitude']
outdf = outdf.groupby(groupbyList).agg(lambda x: ','.join([str(elem) for elem in (list(set(x))) if elem!=''])).replace(np.nan, "").reset_index()
outdf = outdf[SitesColumnsList]  # reorder the dataframe's columns based on columnslist


#Error Checking each Field
############################################################################
print("Error checking each field. Purging bad inputs.")
dfpurge = pd.DataFrame(columns=SitesColumnsList) # Purge DataFrame to hold removed elements
dfpurge['ReasonRemoved'] = ""
dfpurge['IncompleteField'] = ""
outdf, dfpurge = TestErrorFunctionsFile.SiteTestErrorFunctions(outdf, dfpurge)
print(f'Length of outdf DataFrame: ', len(outdf))
print(f'Length of dfpurge DataFrame: ', len(dfpurge))


############################################################################
print("Assign SiteUUID") # has to be one of the last.
outdf = outdf.reset_index(drop=True)
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['SiteUUID'] = dftemp.apply(lambda row: assignSiteUUID(row['Count']), axis=1)
#outdf['SiteUUID'] = outdf.apply(lambda row: assignSiteUUID(row['SiteNativeID']), axis=1)

# Error check SiteUUID
outdf, dfpurge = TestErrorFunctionsFile.SiteUUID_S_Check(outdf, dfpurge)


# Export to new csv
############################################################################
print("Exporting dataframe...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/sites.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0): print(f'...', len(dfpurge),  ' records removed.')
dfpurge.insert(0, 'ReasonRemoved', dfpurge.pop('ReasonRemoved'))
dfpurge.to_csv('ProcessedInputData/sites_missing.csv', index=False)

print("Done")