# Date Update: 04/26/2023
# Purpose: To extract regulatory record information and populate dataframe for WaDE


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd
import re
from datetime import date


# Custom Libraries
############################################################################
import sys
# columns
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/MappingFunctions")
import GetColumnsFile

# Test WaDE Data for any Errors
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/ErrorCheckCode")
import ErrorCheckCodeFunctionsFile


# Create File Function
############################################################################
def CreateOverlaysInputFunction(workingDirString, varST, varUUIDType, mainInputFile):
    # Inputs
    ############################################################################
    print("Reading input csv...")
    workingDir = workingDirString
    os.chdir(workingDir)
    fileInput = "RawinputData/" + mainInputFile
    df = pd.read_csv(fileInput, compression='zip')

    # WaDE columns
    OverlaysColumnsList = GetColumnsFile.GetOverlaysColumnsFunction()


    # Custom Functions
    ############################################################################
    # For creating UUID
    def assignUUID(Val):
        Val = str(Val)
        Val = re.sub("[$@&.;,/\)(-]", "", Val).strip().replace(" ", "")
        Val = varST + varUUIDType + "_RO" + Val
        return Val


    # Creating output dataframe (outdf)
    ############################################################################
    print("Populating dataframe outdf...")
    outdf = pd.DataFrame(columns=OverlaysColumnsList, index=df.index)  # The output dataframe

    print("OversightAgency")
    outdf['OversightAgency'] = df['in_OversightAgency']

    print("OverlayDescription")
    outdf['OverlayDescription'] = df['in_OverlayDescription']

    print("OverlayName")
    outdf['OverlayName'] = df['in_OverlayName']

    print("OverlayNativeID")
    outdf['OverlayNativeID'] = df['in_OverlayNativeID'].astype(str)

    print("OverlayStatusCV")
    outdf['OverlayStatusCV'] = df['in_OverlayStatusCV']

    print("Statute")
    outdf['Statute'] = df['in_Statute']

    print("StatuteLink")
    outdf['StatuteLink'] = df['in_StatuteLink']

    print("StatutoryEffectiveDate")
    outdf['StatutoryEffectiveDate'] = df['in_StatutoryEffectiveDate']

    print("StatutoryEndDate")
    outdf['StatutoryEndDate'] = df['in_StatutoryEndDate']

    print("OverlayTypeCV")
    outdf['OverlayTypeCV'] = df['in_OverlayTypeCV']

    print("WaterSourceTypeCV")
    outdf['WaterSourceTypeCV'] = df['in_WaterSourceTypeCV']

    print("Adding Data Assessment UUID")
    outdf['WaDEUUID'] = df['WaDEUUID']

    print("Resetting Index")
    outdf.reset_index()

    print("Joining outdf duplicates based on key fields...")
    outdf = outdf.replace(np.nan, "")  # Replaces NaN values with blank.
    groupbyList = ['OverlayName', 'OverlayNativeID', 'OverlayStatusCV', 'OverlayTypeCV', 'WaterSourceTypeCV']
    outdf = outdf.groupby(groupbyList).agg(lambda x: ','.join([str(elem) for elem in (list(set(x))) if elem!=''])).replace(np.nan, "").reset_index()
    outdf = outdf[OverlaysColumnsList]  # reorder the dataframe's columns based on ColumnsList


    # Solving WaDE 2.0 Upload Issues
    # ############################################################################
    print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to WaDE here.

    # None at the moment


    # Error Checking Each Field
    ############################################################################
    print("Error checking each field. Purging bad inputs.")
    dfpurge = pd.DataFrame(columns=OverlaysColumnsList)  # Purge DataFrame to hold removed elements
    dfpurge['ReasonRemoved'] = ""
    dfpurge['IncompleteField'] = ""
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.OverlaysTestErrorFunctions(outdf, dfpurge)
    print(f'Length of outdf DataFrame: ', len(outdf))
    print(f'Length of dfpurge DataFrame: ', len(dfpurge))


    # Assign UUID value
    ############################################################################
    print("Assign OverlayUUID")  # has to be one of the last.
    outdf = outdf.reset_index(drop=True)
    outdf['OverlayUUID'] = outdf.apply(lambda row: assignUUID(row['OverlayNativeID']), axis=1)  # assign based on native ID
    outdf['OverlayUUID'] = np.where(outdf['OverlayUUID'].duplicated(keep=False),
                                              outdf['OverlayUUID'].astype(str).str.cat(outdf.groupby('OverlayUUID').cumcount().add(1).astype(str), sep='_'),
                                              outdf['OverlayUUID'])

    # Error check OverlayUUID
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.OverlayUUID_RE_Check(outdf, dfpurge)


    # Export to new csv
    ############################################################################
    print("Exporting dataframe...")

    # The working output DataFrame for WaDE 2.0 input.
    outdf.to_csv('ProcessedInputData/overlays.csv', index=False)

    # Report purged values.
    if(len(dfpurge.index) > 0): print(f'...', len(dfpurge),  ' records removed.')
    dfpurge.insert(0, 'ReasonRemoved', dfpurge.pop('ReasonRemoved'))
    dfpurge.to_csv('ProcessedInputData/overlays_missing.csv', index=False)

    print("Done")
