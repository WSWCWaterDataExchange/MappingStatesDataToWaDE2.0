# Date Created: 09/24/2024
# Purpose: To create reporting unit information and populate a dataframe for WaDE


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


# Create File Function
############################################################################
def CreateReportingUnitInputFunction(workingDirString, varST, varUUIDType, mainInputFile):
    # Inputs
    ############################################################################
    print("Reading input csv...")
    workingDir = workingDirString
    os.chdir(workingDir)
    fileInput = "RawInputData/" + mainInputFile
    df = pd.read_csv(fileInput, compression='zip')

    # geometry data mandatory for reporting unit information
    fileInput_shape = "RawinputData/P_Geometry.zip"
    dfshape = pd.read_csv(fileInput_shape, compression='zip')
    Geometrydict = pd.Series(dfshape.geometry.values, index=dfshape.in_ReportingUnitNativeID.astype(str)).to_dict()

    # WaDE columns
    ReportingUnitColumnsList = GetColumnsFile.GetReportingUnitColumnsFunction()

    # Custom Functions
    ############################################################################
    # For Creating Geometry
    def retrieveGeometry(colrowValue):
        String1 = colrowValue
        try:
            outString = Geometrydict[String1]
            outString = wkt.loads(outString)
            outString = make_valid(outString)
        except:
            outString = ""
            print(f'...could not pair/find "{colrowValue}" id geometry.')
        return outString


    # For creating UUID
    def assignUUID(Val):
        Val = str(Val)
        Val = re.sub("[$@&.;,/\)(-]", "", Val).strip().replace(" ", "")
        Val = varST + varUUIDType + "_RU" + Val
        return Val


    # Creating output dataframe (outdf)
    ############################################################################
    print("Populating dataframe...")
    outdf = pd.DataFrame(columns=ReportingUnitColumnsList, index=df.index)

    print("EPSGCodeCV")
    outdf['EPSGCodeCV'] = "4326"

    print("ReportingUnitName")
    outdf['ReportingUnitName'] = df['in_ReportingUnitName']

    print("ReportingUnitNativeID")
    outdf['ReportingUnitNativeID'] = df['in_ReportingUnitNativeID']

    print("ReportingUnitProductVersion")
    outdf['ReportingUnitProductVersion'] = df['in_ReportingUnitProductVersion']

    print("ReportingUnitTypeCV")
    outdf['ReportingUnitTypeCV'] = df['in_ReportingUnitTypeCV']

    print("ReportingUnitUpdateDate")
    outdf['ReportingUnitUpdateDate'] = df['in_ReportingUnitUpdateDate']

    print("StateCV")
    outdf['StateCV'] = df['in_StateCV']

    print("Geometry")
    outdf['Geometry'] = df.apply(lambda row: retrieveGeometry(row['in_ReportingUnitNativeID']), axis=1)  # See pre-processing.

    print("Adding Data Assessment UUID")
    outdf['WaDEUUID'] = df['WaDEUUID']

    print("Resetting Index")
    outdf = outdf.drop_duplicates().reset_index(drop=True).replace(np.nan, "")

    print("GroupBy outdf duplicates based on key fields...")
    outdf = outdf.groupby('ReportingUnitNativeID').agg(lambda x: ','.join([str(elem) for elem in (list(set(x))) if elem != ""])).replace(np.nan, "").reset_index()
    outdf = outdf[ReportingUnitColumnsList]  # reorder the dataframe's columns based on Columnslist


    # Error Checking each Field
    ############################################################################
    print("Error checking each field. Purging bad inputs.")
    dfpurge = pd.DataFrame(columns=ReportingUnitColumnsList) # Purge DataFrame to hold removed elements
    dfpurge['ReasonRemoved'] = ""
    dfpurge['IncompleteField'] = ""
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.ReportingUnitTestErrorFunctions(outdf, dfpurge)
    print(f'Length of outdf DataFrame: ', len(outdf))
    print(f'Length of dfpurge DataFrame: ', len(dfpurge))


    # Assign UUID value
    ############################################################################
    print("Assign ReportingUnitUUID") # has to be one of the last.
    outdf = outdf.reset_index(drop=True)
    outdf['ReportingUnitUUID'] = outdf.apply(lambda row: assignUUID(row['ReportingUnitNativeID']), axis=1) # assign based on native ID
    outdf['ReportingUnitUUID'] = np.where(outdf['ReportingUnitUUID'].duplicated(keep=False),
                                          outdf['ReportingUnitUUID'].astype(str).str.cat(outdf.groupby('ReportingUnitUUID').cumcount().add(1).astype(str), sep='_'),
                                          outdf['ReportingUnitUUID'])

    # Error check SiteUUID
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.ReportingUnitUUID_RU_Check(outdf, dfpurge)


    # Export to new csv
    ############################################################################
    print("Exporting dataframe...")

    # The working output DataFrame for WaDE 2.0 input.
    outdf.to_csv('ProcessedInputData/reportingunits.csv', index=False)

    # Report purged values.
    if(len(dfpurge.index) > 0): print(f'...', len(dfpurge),  ' records removed.')
    dfpurge.insert(0, 'ReasonRemoved', dfpurge.pop('ReasonRemoved'))
    dfpurge.to_csv('ProcessedInputData/reportingunits_missing.csv', index=False)

    print("Done")