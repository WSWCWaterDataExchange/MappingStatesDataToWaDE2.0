# Date Update: 04/26/2023
# Purpose: To create regulatory overlay information and populate dataframe for WaDE


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd
import re
from datetime import date
from datetime import timedelta


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
def CreateRegulatoryReportingUnitsInputFunction(workingDirString, mainInputFile):
    # Inputs
    ############################################################################
    print("Reading input csv...")
    workingDir = workingDirString
    os.chdir(workingDir)
    fileInput = "RawinputData/" + mainInputFile
    df = pd.read_csv(fileInput, compression='zip')

    # Input Data - 'WaDE Input' files.
    dfro = pd.read_csv("ProcessedInputData/regulatoryoverlays.csv").replace(np.nan, "")  # RegulatoryOverlays dataframe
    dfru = pd.read_csv("ProcessedInputData/reportingunits.csv").replace(np.nan, "")  # ReportingUnit dataframe

    # WaDE columns
    # no WaDEUUID column
    RegulatoryReportingUnitsColumnsList = GetColumnsFile.GetRegulatoryReportingUnitsColumnsFunction()


    # Custom Functions
    ############################################################################
    # For creating RegulatoryOverlayUUID
    RegulatoryOverlayUUIDdict = pd.Series(dfro.RegulatoryOverlayUUID.values, index = dfro.RegulatoryOverlayNativeID.astype(str)).to_dict()
    def retrieveRegulatoryOverlayUUID(colrowValue):
        if colrowValue == '' or pd.isnull(colrowValue):
            outList = ''
        else:
            String1 = str(colrowValue).strip()
            try:
                outList = RegulatoryOverlayUUIDdict[String1]
            except:
                outList = ''
        return outList

    # For creating ReportingUnitsUUID
    ReportingUnitUUIDdict = pd.Series(dfru.ReportingUnitUUID.values, index = dfru.ReportingUnitNativeID.astype(str)).to_dict()
    def retrieveReportingUnitsUUID(colrowValue):
        if colrowValue == '' or pd.isnull(colrowValue):
            outList = ''
        else:
            String1 = str(colrowValue).strip()
            try:
                outList = ReportingUnitUUIDdict[String1]
            except:
                outList = ''
        return outList

    # no custom UUID for RegulatoryReportingUnits


    # Creating output dataframe (outdf)
    ############################################################################
    print("Populating dataframe outdf...")
    outdf = pd.DataFrame(columns=RegulatoryReportingUnitsColumnsList, index=df.index)  # The output dataframe

    print("DataPublicationDate")
    outdf['DataPublicationDate'] = (date.today() - timedelta(days = 1)).strftime('%m/%d/%Y')

    print("OrganizationUUID")
    outdf['OrganizationUUID'] = df['in_OrganizationUUID']

    print("RegulatoryOverlayUUID")
    outdf['RegulatoryOverlayUUID'] = df.apply(lambda row: retrieveRegulatoryOverlayUUID(row['in_RegulatoryOverlayNativeID']), axis=1)

    print("ReportingUnitUUID")
    outdf['ReportingUnitUUID'] = df.apply(lambda row: retrieveReportingUnitsUUID(row['in_ReportingUnitNativeID']), axis=1)

    print("Resetting Index")
    outdf = outdf.drop_duplicates().reset_index(drop=True)


    # Solving WaDE 2.0 Upload Issues
    # ############################################################################
    print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to WaDE here.

    # None at the moment


    # Error Checking Each Field
    ############################################################################
    print("Error checking each field. Purging bad inputs.")
    dfpurge = pd.DataFrame(columns=RegulatoryReportingUnitsColumnsList)  # Purge DataFrame to hold removed elements
    dfpurge['ReasonRemoved'] = ""
    dfpurge['IncompleteField'] = ""
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.RegulatoryReportingUnitsErrorFunctions(outdf, dfpurge)
    print(f'Length of outdf DataFrame: ', len(outdf))
    print(f'Length of dfpurge DataFrame: ', len(dfpurge))


    # Assign UUID value
    ############################################################################
    # N/A
    # Not needed for RegulatoryReportingUnits


    # Export to new csv
    ############################################################################
    print("Exporting dataframe...")

    # The working output DataFrame for WaDE 2.0 input.
    outdf.to_csv('ProcessedInputData/regulatoryreportingunits.csv', index=False)

    # Report purged values.
    if(len(dfpurge.index) > 0): print(f'...', len(dfpurge),  ' records removed.')
    dfpurge.insert(0, 'ReasonRemoved', dfpurge.pop('ReasonRemoved'))
    dfpurge.to_csv('ProcessedInputData/regulatoryreportingunits_missing.csv', index=False)

    print("Done")
