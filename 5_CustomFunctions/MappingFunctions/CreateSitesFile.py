# Date Update: 04/12/2023
# Purpose: To extract site information and populate dataframe for WaDE


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd
import re


# Custom Libraries
############################################################################
import sys
# columns
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/MappingFunctions")
import GetColumnsFile

# Test WaDE Data for any Errors
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/ErrorCheckCode")
import TestErrorFunctionsFile


# Create File Function
############################################################################
def CreateSitesInputFunction(varST, varSTName, varUUIDType, varWaDEDataType, mainInputFile):
    # Inputs
    ############################################################################
    print("Reading input csv...")
    workingDir = "G:/Shared drives/WaDE Data/" + varSTName + "/" + varWaDEDataType
    os.chdir(workingDir)
    fileInput = "RawinputData/" + mainInputFile
    df = pd.read_csv(fileInput, compression='zip')

    watersources_fileInput = "ProcessedInputData/watersources.csv"
    df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe

    try:
        fileInput_shape = "RawinputData/P_Geometry.zip"
        dfshape = pd.read_csv(fileInput_shape, compression='zip')
        Geometrydict = pd.Series(dfshape.geometry.values, index=dfshape.in_SiteNativeID.astype(str)).to_dict()
    except:
        print("no geometry data to worry about.")

    # WaDE columns
    SitesColumnsList = GetColumnsFile.GetSitesColumnsFunction()


    # Custom Functions
    ############################################################################

    # For creating WaterSourceUUID
    WaterSourceUUIDdict = pd.Series(df_watersources.WaterSourceUUID.values, index=df_watersources.WaterSourceNativeID.astype(str)).to_dict()
    def retrieveWaterSourceUUID(colrowValue):
        if colrowValue == '' or pd.isnull(colrowValue):
            outList = ''
        else:
            colrowValue = str(colrowValue).strip()
            outList = WaterSourceUUIDdict[colrowValue]
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
    def assignUUID(Val):
        Val = str(Val)
        Val = re.sub("[$@&.;,/\)(-]", "", Val).strip()
        Val = varST + varUUIDType + "_S" + Val
        return Val


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


    # Error Checking each Field
    ############################################################################
    print("Error checking each field. Purging bad inputs.")
    dfpurge = pd.DataFrame(columns=SitesColumnsList) # Purge DataFrame to hold removed elements
    dfpurge['ReasonRemoved'] = ""
    dfpurge['IncompleteField'] = ""
    outdf, dfpurge = TestErrorFunctionsFile.SiteTestErrorFunctions(outdf, dfpurge)
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