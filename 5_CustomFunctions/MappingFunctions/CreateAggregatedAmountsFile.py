# Date Update: 09/24/2024
# Purpose: To extract aggregated water use amount timeseries record information and populate dataframe for WaDE.


# Needed Libraries
############################################################################
import os
import sys
import numpy as np
import pandas as pd
import re
from datetime import date
from datetime import timedelta



# Custom Libraries
############################################################################

# columns
sys.path.append("../../5_CustomFunctions/MappingFunctions")
import GetColumnsFile

# Assign Primary Use Category fix
sys.path.append("../../5_CustomFunctions/AssignPrimaryUseCategory")
import AssignPrimaryUseCategoryFile

# Test WaDE Data for any Errors
sys.path.append("../../5_CustomFunctions/ErrorCheckCode")
import ErrorCheckCodeFunctionsFile

# Clean data and data types
sys.path.append("../../5_CustomFunctions/CleanDataCode")
import CleanDataCodeFunctionsFile


# Create File Function
############################################################################
def CreateAggregatedAmountsInputFunction(workingDirString, df):

    # Inputs
    ############################################################################
    print("Setting inputs...")
    workingDir = workingDirString
    os.chdir(workingDir)

    # Input Data - 'WaDE Input' files.
    dfv = pd.read_csv("ProcessedInputData/variables.csv").replace(np.nan, "")  # Variables dataframe
    dfru = pd.read_csv("ProcessedInputData/reportingunits.csv").replace(np.nan, "")  # ReportingUnit dataframe
    dfws = pd.read_csv("ProcessedInputData/watersources.csv").replace(np.nan, "")  # WaterSources dataframe

    # WaDE columns
    AggregatedAmountsColumnsList = GetColumnsFile.GetAggregatedAmountsColumnsFunction()


    # Custom Functions
    ############################################################################

    # For creating VariableSpecificUUID
    VariableSpecificUUIDdict = pd.Series(dfv.VariableSpecificUUID.values, index=dfv.VariableSpecificCV.astype(str)).to_dict()
    def retrieveVariableSpecificUUID(colrowValue):
        if colrowValue == '' or pd.isnull(colrowValue):
            outString = ''
        else:
            colrowValue = str(colrowValue).strip()
            try:
                outString = VariableSpecificUUIDdict[colrowValue]
            except:
                outString = ''
        return outString

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


    # Creating output dataframe (outdf)
    ############################################################################
    print("Populating dataframe outdf...")
    outdf = pd.DataFrame(columns=AggregatedAmountsColumnsList, index=df.index)  # The output dataframe

    print("MethodUUID")
    outdf['MethodUUID'] = df['in_MethodUUID']

    print("OrganizationUUID")
    outdf['OrganizationUUID'] = df['in_OrganizationUUID']

    print("ReportingUnitUUID")  # Using SiteNativeID to identify ID
    outdf['ReportingUnitUUID'] = df.apply(lambda row: retrieveReportingUnitsUUID(row['in_ReportingUnitNativeID']), axis=1)

    print("VariableSpecificUUID")
    outdf['VariableSpecificUUID'] = df.apply(lambda row: retrieveVariableSpecificUUID(row['in_VariableSpecificCV']), axis=1)

    print("WaterSourceUUID")
    outdf['WaterSourceUUID'] = df.apply(lambda row: retrieveWaterSourceUUID(row['in_WaterSourceNativeID']), axis=1)

    print("Amount")
    outdf['Amount'] = df['in_Amount']

    print("BeneficialUseCategory")
    outdf['BeneficialUseCategory'] = df['in_BeneficialUseCategory']

    print("CommunityWaterSupplySystem")
    outdf['CommunityWaterSupplySystem'] = df['in_CommunityWaterSupplySystem']

    print("CropTypeCV")
    outdf['CropTypeCV'] = df['in_CropTypeCV']

    print("CustomerTypeCV")
    outdf['CustomerTypeCV'] = df['in_CustomerTypeCV']

    print("DataPublicationDate")
    outdf['DataPublicationDate'] = (date.today() - timedelta(days = 1)).strftime('%m/%d/%Y')

    print("DataPublicationDOI")
    outdf['DataPublicationDOI'] = df['in_DataPublicationDOI']

    print("InterbasinTransferFromID")
    outdf['InterbasinTransferFromID'] = df['in_InterbasinTransferFromID']

    print("InterbasinTransferToID")
    outdf['InterbasinTransferToID'] = df['in_InterbasinTransferToID']

    print("IrrigatedAcreage")
    outdf['IrrigatedAcreage'] = df['in_IrrigatedAcreage']

    print("IrrigationMethodCV")
    outdf['IrrigationMethodCV'] = df['in_IrrigationMethodCV']

    print("PopulationServed")
    outdf['PopulationServed'] = df['in_PopulationServed']

    print("PowerGeneratedGWh")
    outdf['PowerGeneratedGWh'] = df['in_PowerGeneratedGWh']

    print("PowerType")
    outdf['PowerType'] = df['in_PowerType']

    print("PrimaryUseCategory")
    outdf['PrimaryUseCategory'] = df['in_PrimaryUseCategoryCV']

    print("ReportYearCV")
    outdf['ReportYearCV'] = df['in_ReportYearCV']

    print("SDWISIdentifierCV")
    outdf['SDWISIdentifierCV'] = df['in_SDWISIdentifierCV']

    print("TimeframeEnd")
    outdf['TimeframeEnd'] = df['in_TimeframeEnd']

    print("TimeframeStart")
    outdf['TimeframeStart'] = df['in_TimeframeStart']

    print("Adding Data Assessment UUID")
    outdf['WaDEUUID'] = df['WaDEUUID']

    print("Resetting Index")
    outdf = outdf.drop_duplicates().reset_index(drop=True).replace(np.nan, "")

    # Solving WaDE 2.0 Upload Issues
    ############################################################################
    print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to WaDE here.

    # Temp solution to populate PrimaryBeneficialUseCategory field.
    # Use Custom import file
    outdf['PrimaryUseCategoryCV'] = outdf.apply(lambda row: AssignPrimaryUseCategoryFile.retrievePrimaryUseCategory(row['BeneficialUseCategory']), axis=1)


    # Error Checking Each Field
    ############################################################################
    print("Error checking each field. Purging bad inputs.")
    dfpurge = pd.DataFrame(columns=AggregatedAmountsColumnsList)  # Purge DataFrame to hold removed elements
    dfpurge['ReasonRemoved'] = ""
    dfpurge['IncompleteField'] = ""
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.AggregatedAmountsErrorFunctions(outdf, dfpurge)
    print(f'Length of outdf DataFrame: ', len(outdf))
    print(f'Length of dfpurge DataFrame: ', len(dfpurge))


    # Clean data & check data types before export
    ############################################################################
    print("Cleaning export for correct data types...")
    outdf = CleanDataCodeFunctionsFile.FixAggregatedAmountsInfoFunctions(outdf)


    # Export to new csv
    ############################################################################
    print("Exporting dataframe...")

    # The working output DataFrame for WaDE 2.0 input.
    outdf.to_csv('ProcessedInputData/aggregatedamounts.csv', index=False)

    # Report purged values.
    if(len(dfpurge.index) > 0): print(f'...', len(dfpurge),  ' records removed.')
    dfpurge.insert(0, 'ReasonRemoved', dfpurge.pop('ReasonRemoved'))
    dfpurge.to_csv('ProcessedInputData/aggregatedamounts_missing.csv', index=False)

    print("Done")

