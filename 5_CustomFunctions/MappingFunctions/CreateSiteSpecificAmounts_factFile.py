# Date Update: 11/16/2023
# Purpose: To create site-specific amounts record information and populate dataframe for WaDE 2.0.


# Needed Libraries
############################################################################
import os
import sys
import numpy as np
import pandas as pd
from datetime import date


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
def CreateSiteSpecificAmounts_factsInputFunction(workingDirString, mainInputFile):

    # Inputs
    ############################################################################
    print("Reading input csv...")
    workingDir = workingDirString
    os.chdir(workingDir)
    fileInput = "RawinputData/" + mainInputFile
    df = pd.read_csv(fileInput, compression='zip')

    # Input Data - 'WaDE Input' files.
    dfv = pd.read_csv("ProcessedInputData/variables.csv").replace(np.nan, "")  # Variables dataframe
    dfws = pd.read_csv("ProcessedInputData/watersources.csv").replace(np.nan, "")  # WaterSources dataframe
    dfs = pd.read_csv("ProcessedInputData/sites.csv").replace(np.nan, "")

    # WaDE columns
    SiteSpecificAmountsColumnsList = GetColumnsFile.GetSiteSpecificAmountsColumnsFunction()


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

    # For creating SiteUUID
    SiteUUIDDdict = pd.Series(dfs.SiteUUID.values, index=dfs.SiteNativeID.astype(str)).to_dict()
    def retrieveSiteUUID(colrowValue):
        if colrowValue == '' or pd.isnull(colrowValue):
            outList = ''
        else:
            strVal = str(colrowValue).strip()
            try:
                outList = SiteUUIDDdict[strVal]
            except:
                outList = ''
        return outList


    # Creating output dataframe (outdf)
    ############################################################################
    print("Populating dataframe outdf...")
    outdf = pd.DataFrame(columns=SiteSpecificAmountsColumnsList, index=df.index)  # The output dataframe

    print("MethodUUID")
    outdf['MethodUUID'] = df['in_MethodUUID']

    print("VariableSpecificUUID")
    outdf['VariableSpecificUUID'] = df.apply(lambda row: retrieveVariableSpecificUUID(row['in_VariableSpecificCV']), axis=1)

    print("OrganizationUUID")
    outdf['OrganizationUUID'] = df['in_OrganizationUUID']

    print("WaterSourceUUID")
    outdf['WaterSourceUUID'] = df.apply(lambda row: retrieveWaterSourceUUID(row['in_WaterSourceNativeID']), axis=1)

    print("SiteUUID")  # Using SiteNativeID
    outdf['SiteUUID'] = df.apply(lambda row: retrieveSiteUUID(row['in_SiteNativeID']), axis=1)

    print("Amount")
    outdf['Amount'] = df['in_Amount']

    print('AllocationCropDutyAmount')
    outdf['AllocationCropDutyAmount'] = df['in_AllocationCropDutyAmount']

    print("AssociatedNativeAllocationIDs")
    outdf['AssociatedNativeAllocationIDs'] = df['in_AssociatedNativeAllocationIDs']

    print('BeneficialUseCategory')
    outdf['BeneficialUseCategory'] = df['in_BeneficialUseCategory']

    print("CommunityWaterSupplySystem")
    outdf['CommunityWaterSupplySystem'] = df['in_CommunityWaterSupplySystem']

    print("CropTypeCV")
    outdf['CropTypeCV'] = df['in_CropTypeCV']

    print("CustomerTypeCV")
    outdf['CustomerTypeCV'] = df['in_CustomerTypeCV']

    print("DataPublicationDate")
    outdf['DataPublicationDate'] = date.today().strftime('%m/%d/%Y')

    print("DataPublicationDOI")
    outdf['DataPublicationDOI'] = df['in_DataPublicationDOI']

    print("Geometry")
    outdf['Geometry'] = df['in_Geometry']

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
    outdf['PrimaryUseCategory'] = df['in_PrimaryUseCategory']

    print("ReportYearCV")
    outdf['ReportYearCV'] = df['in_ReportYearCV']

    print("SDWISIdentifier")
    outdf['SDWISIdentifier'] = df['in_SDWISIdentifier']

    print("TimeframeEnd")
    outdf['TimeframeEnd'] = df['in_TimeframeEnd']

    print("TimeframeStart")
    outdf['TimeframeStart'] = df['in_TimeframeStart']

    print("Adding Data Assessment UUID")
    outdf['WaDEUUID'] = ""

    print("Resetting Index")
    outdf = outdf.drop_duplicates().reset_index(drop=True).replace(np.nan, "")


    # Solving WaDE 2.0 Upload Issues
    ############################################################################
    # N/A


    # Error Checking Each Field
    ############################################################################
    print("Error checking each field. Purging bad inputs.")
    dfpurge = pd.DataFrame(columns=SiteSpecificAmountsColumnsList)  # Purge DataFrame to hold removed elements
    dfpurge['ReasonRemoved'] = ""
    dfpurge['IncompleteField'] = ""
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.SiteSpecificAmountsTestErrorFunctions(outdf, dfpurge)
    print(f'Length of outdf DataFrame: ', len(outdf))
    print(f'Length of dfpurge DataFrame: ', len(dfpurge))


    # Clean data & check data types before export
    ############################################################################
    print("Cleaning export for correct data types...")
    outdf = CleanDataCodeFunctionsFile.FixSiteSpecificAmountsInfoFunctions(outdf)


    # Export to new csv
    ############################################################################
    print("Exporting dataframe...")

    # The working output DataFrame for WaDE 2.0 input.
    outdf.to_csv('ProcessedInputData/sitespecificamounts.csv', index=False)

    # Report purged values.
    if(len(dfpurge.index) > 0): print(f'...', len(dfpurge),  ' records removed.')
    dfpurge.insert(0, 'ReasonRemoved', dfpurge.pop('ReasonRemoved'))
    dfpurge.to_csv('ProcessedInputData/sitespecificamounts_missing.csv', index=False)

    print("Done")