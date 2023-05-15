# Date Update: 03/30/2023
# Purpose: To create water source information and populate dataframe for WaDE_QA 2.0.


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
import ErrorCheckCodeFunctionsFile

# Clean data and data types
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/CleanDataCode")
import CleanDataCodeFunctionsFile


# Create File Function
############################################################################
def CreateWaterSourcesInputFunction(varST, varSTName, varUUIDType, varWaDEDataType, mainInputFile):

    # Inputs
    ############################################################################
    print("Reading input csv...")
    workingDir = "G:/Shared drives/WaDE Data/" + varSTName + "/" + varWaDEDataType
    os.chdir(workingDir)
    fileInput = "RawinputData/" + mainInputFile
    df = pd.read_csv(fileInput, compression='zip')

    # WaDE columns
    WaterSourcseColumnsList = GetColumnsFile.GetWaterSourcesColumnsFunction()


    # Custom Site Functions
    ############################################################################

    # For creating WaterSourceUUID
    def assignUUID(Val):
        Val = str(Val)
        Val = re.sub("[$@&.;,/\)(-]", "", Val).strip().replace(" ", "")
        Val = varST + varUUIDType + "_WS" + Val
        return Val


    # Creating output dataframe (outdf)
    ############################################################################
    print("Populating dataframe...")
    outdf = pd.DataFrame(index=df.index, columns=WaterSourcseColumnsList)  # The output dataframe for CSV.

    print("Geometry")
    outdf['Geometry'] = ""

    print("GNISFeatureNameCV")
    outdf['GNISFeatureNameCV'] = ""

    print("WaterQualityIndicatorCV")
    outdf['WaterQualityIndicatorCV'] = "Fresh"

    print("WaterSourceName")
    outdf['WaterSourceName'] = df['in_WaterSourceName']

    print("WaterSourceNativeID")
    outdf["WaterSourceNativeID"] = df['in_WaterSourceNativeID']

    print("WaterSourceTypeCV")
    outdf['WaterSourceTypeCV'] = df['in_WaterSourceTypeCV']

    print("Adding Data Assessment UUID")
    outdf['WaDEUUID'] = df['WaDEUUID']

    print("Resetting Index")
    outdf = outdf.drop_duplicates().reset_index(drop=True).replace(np.nan, "")

    print("GroupBy outdf duplicates based on key fields...")
    outdf = outdf.groupby('WaterSourceNativeID').agg(lambda x: ','.join([str(elem) for elem in (list(set(x))) if elem != ""])).replace(np.nan, "").reset_index()
    outdf = outdf[WaterSourcseColumnsList]  # reorder the dataframe's columns based on ColumnsList


    #Error Checking each Field
    ############################################################################
    print("Error checking each field. Purging bad inputs.")
    dfpurge = pd.DataFrame(columns=WaterSourcseColumnsList) # Purge DataFrame to hold removed elements
    dfpurge['ReasonRemoved'] = ""
    dfpurge['IncompleteField'] = ""
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.WaterSourceTestErrorFunctions(outdf, dfpurge)
    print(f'Length of outdf DataFrame: ', len(outdf))
    print(f'Length of dfpurge DataFrame: ', len(dfpurge))


    ############################################################################
    print("Assign WaterSourceUUID") # has to be one of the last.
    outdf = outdf.reset_index(drop=True)
    outdf['WaterSourceUUID'] = outdf.apply(lambda row: assignUUID(row['WaterSourceNativeID']), axis=1) # assign based on native ID
    outdf['WaterSourceUUID'] = np.where(outdf['WaterSourceUUID'].duplicated(keep=False),
                                        outdf['WaterSourceUUID'].astype(str).str.cat(outdf.groupby('WaterSourceUUID').cumcount().add(1).astype(str), sep='_'),
                                        outdf['WaterSourceUUID'])

    # Error check WaterSourceUUID
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.WaterSourceUUID_WS_Check(outdf, dfpurge)


    # Clean data & check data types before export
    ############################################################################
    print("Cleaning export for correct data types...")
    outdf = CleanDataCodeFunctionsFile.FixWaterSourceInfoFunctions(outdf)


    # Export to new csv
    ############################################################################
    print("Exporting dataframe...")

    # The working output DataFrame for WaDE 2.0 input.
    outdf.to_csv('ProcessedInputData/watersources.csv', index=False)

    # Report purged values.
    if(len(dfpurge.index) > 0): print(f'...', len(dfpurge),  ' records removed.')
    dfpurge.insert(0, 'ReasonRemoved', dfpurge.pop('ReasonRemoved'))
    dfpurge.to_csv('ProcessedInputData/watersources_missing.csv', index=False)

    print("Done")