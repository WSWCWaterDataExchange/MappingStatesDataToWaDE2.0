# Date Update: 04/12/2023
# Purpose: To extract site information and populate dataframe for WaDE


# Needed Libraries
############################################################################
import os
import sys
import numpy as np
import pandas as pd
from shapely import wkt
from shapely.validation import make_valid
import re


# Custom Libraries
############################################################################

# columns
sys.path.append("../../5_CustomFunctions/MappingFunctions")
import GetColumnsFile

# Test WaDE Data for any Errors
sys.path.append("../../5_CustomFunctions/ErrorCheckCode")
import ErrorCheckCodeFunctionsFile

# Clean data and data types
sys.path.append("../../5_CustomFunctions/CleanDataCode")
import CleanDataCodeFunctionsFile


# Create File Function
############################################################################
def CreateSitesInputFunction(workingDirString, varST, varUUIDType, mainInputFile):
    # Inputs
    ############################################################################
    print("Reading input csv...")
    workingDir = workingDirString
    os.chdir(workingDir)
    fileInput = "RawinputData/" + mainInputFile
    df = pd.read_csv(fileInput, compression='zip')

    # Input Data - 'WaDE Input' files.
    dfws = pd.read_csv("ProcessedInputData/watersources.csv").replace(np.nan, "")  # WaterSources dataframe
    try:
        fileInput_shape = "RawinputData/P_Geometry.zip"
        dfshape = pd.read_csv(fileInput_shape, compression='zip')
        Geometrydict = pd.Series(dfshape.geometry.values, index=dfshape.in_SiteNativeID.astype(str)).to_dict()
    except:
        print("...no geometry data to worry about.")

    # WaDE columns
    SitesColumnsList = GetColumnsFile.GetSitesColumnsFunction()


    # Custom Functions
    ############################################################################

    # For creating WaterSourceUUID
    WaterSourceUUIDdict = pd.Series(dfws.WaterSourceUUID.values, index=dfws.WaterSourceNativeID.astype(str)).to_dict()
    def retrieveWaterSourceUUID(colrowValue):
        if colrowValue == '' or pd.isnull(colrowValue):
            outList = ''
        else:
            colrowValue = str(colrowValue).strip()
            try:
                outList = WaterSourceUUIDdict[colrowValue]
            except:
                outList = ''
        return outList

    # For Creating Geometry
    def retrieveGeometry(colrowValue):
        if colrowValue == "" or pd.isnull(colrowValue):
            outString = ""
        else:
            String1 = colrowValue
            try:
                outString = Geometrydict[String1]
                outString = wkt.loads(outString)
                outString = make_valid(outString)
            except:
                outString = ""
        return outString

    # For creating UUID
    def assignUUID(Val):
        Val = str(Val)
        Val = re.sub("[$@&.;,/\)(-]", "", Val).strip().replace(" ", "")
        Val = varST + varUUIDType + "_S" + Val
        return Val


    # Creating output dataframe (outdf)
    ############################################################################
    print("Populating dataframe...")
    outdf = pd.DataFrame(index=df.index, columns=SitesColumnsList)  # The output dataframe for CSV.

    print("WaterSourceUUIDs")
    outdf['WaterSourceUUIDs'] = df.apply(lambda row: retrieveWaterSourceUUID(row['in_WaterSourceNativeID']), axis=1)

    print("OverlayUUIDs")
    outdf['OverlayUUIDs'] = "" # Use custom JoinOverlayToSiteFile instead

    print("CoordinateAccuracy")
    outdf['CoordinateAccuracy'] = df['in_CoordinateAccuracy']

    print("CoordinateMethodCV")
    outdf['CoordinateMethodCV'] = df['in_CoordinateMethodCV']

    print("County")
    outdf['County'] = df['in_County']

    print("EPSGCodeCV")
    outdf['EPSGCodeCV'] = df['in_EPSGCodeCV']

    print("Geometry")
    outdf['Geometry'] = df.apply(lambda row: retrieveGeometry(row['in_SiteNativeID']), axis=1)

    print("GNISCodeCV")
    outdf['GNISCodeCV'] = df['in_GNISCodeCV']

    print("HUC12")
    outdf['HUC12'] = df['in_HUC12']

    print("HUC8")
    outdf['HUC8'] = df['in_HUC8']

    print("Latitude")
    outdf['Latitude'] = df['in_Latitude']

    print("Longitude")
    outdf['Longitude'] = df['in_Longitude']

    print("NHDNetworkStatusCV")
    outdf['NHDNetworkStatusCV'] = df['in_NHDNetworkStatusCV']

    print("NHDProductCV")
    outdf['NHDProductCV'] = df['in_NHDProductCV']

    print("PODorPOUSite")
    outdf['PODorPOUSite'] = df['in_PODorPOUSite']

    print("SiteName")
    outdf['SiteName'] = df['in_SiteName']

    print("SiteNativeID")
    outdf['SiteNativeID'] = df['in_SiteNativeID']

    print("SitePoint")
    outdf['SitePoint'] = df['in_SitePoint']

    print("SiteTypeCV")
    outdf['SiteTypeCV'] = df['in_SiteTypeCV']

    print("StateCV")
    outdf['StateCV'] = df['in_StateCV']

    print("USGSSiteID")
    outdf['USGSSiteID'] = df['in_USGSSiteID']

    print("Adding Data Assessment UUID")
    outdf['WaDEUUID'] = df['WaDEUUID']

    print("Resetting Index")
    outdf = outdf.drop_duplicates().reset_index(drop=True).replace(np.nan, "")

    print("GroupBy outdf duplicates based on key fields...")
    outdf = outdf.groupby('SiteNativeID').agg(lambda x: ','.join([str(elem) for elem in (list(set(x))) if elem!=''])).replace(np.nan, "").reset_index()
    outdf = outdf[SitesColumnsList]  # reorder the dataframe's columns based on ColumnsList


    # Error Checking each Field
    ############################################################################
    print("Error checking each field. Purging bad inputs.")
    dfpurge = pd.DataFrame(columns=SitesColumnsList) # Purge DataFrame to hold removed elements
    dfpurge['ReasonRemoved'] = ""
    dfpurge['IncompleteField'] = ""
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.SiteTestErrorFunctions(outdf, dfpurge)
    print(f'Length of outdf DataFrame: ', len(outdf))
    print(f'Length of dfpurge DataFrame: ', len(dfpurge))


    # Assign UUID value
    ############################################################################
    print("Assign SiteUUID") # has to be one of the last.
    outdf = outdf.reset_index(drop=True)
    outdf['SiteUUID'] = outdf.apply(lambda row: assignUUID(row['SiteNativeID']), axis=1) # assign based on native ID
    outdf['SiteUUID'] = np.where(outdf['SiteUUID'].duplicated(keep=False),
                                 outdf['SiteUUID'].astype(str).str.cat(outdf.groupby('SiteUUID').cumcount().add(1).astype(str), sep='_'),
                                 outdf['SiteUUID'])

    # Error check SiteUUID
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.SiteUUID_S_Check(outdf, dfpurge)


    # Clean data & check data types before export
    ############################################################################
    print("Cleaning export for correct data types...")
    outdf = CleanDataCodeFunctionsFile.FixSiteInfoFunctions(outdf)


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