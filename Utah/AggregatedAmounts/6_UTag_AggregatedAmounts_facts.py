#Date Created: 11/12/2020
#Author: Ryan James (WSWC)
#Purpose: To create UT agg aggregated information and populate a dataframe WaDEQA 2.0.
#         1) Simple creation of working dataframe (df), with output dataframe (outdf).
#         2) Drop all nulls before combining duplicate rows on NativeID.


# Needed Libraries
############################################################################
import numpy as np
import pandas as pd
import os

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/AggregatedAmounts"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_utAggMaster.csv"
method_fileInput = "ProcessedInputData/methods.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
reportingunits_fileInput = "ProcessedInputData/reportingunits.csv"

df_DM = pd.read_csv(M_fileInput)  # The State's Master input dataframe.
df_method = pd.read_csv(method_fileInput)  # Method dataframe
df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_reportingunits = pd.read_csv(reportingunits_fileInput)  # ReportingUnits dataframe

#WaDE dataframe columns
columnslist = [
    "MethodUUID",
    "OrganizationUUID",
    "ReportingUnitUUID",
    "VariableSpecificUUID",
    "WaterSourceUUID",
    "AllocationCropDutyAmount",
    "Amount",
    "BeneficialUseCategory",
    "CommunityWaterSupplySystem",
    "CropTypeCV",
    "CustomerTypeCV",
    "DataPublicationDate",
    "DataPublicationDOI",
    "InterbasinTransferFromID",
    "InterbasinTransferToID",
    "IrrigatedAcreage",
    "IrrigationMethodCV",
    "PopulationServed",
    "PowerGeneratedGWh",
    "PowerType",
    "PrimaryUseCategory",
    "ReportYearCV",
    "SDWISIdentifierCV",
    "TimeframeEnd",
    "TimeframeStart"]


# Custom Functions
############################################################################

# For creating MethodUUID
def retrieveMethodUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = MethodUUIDdict[String1]
        except:
            outList = ''
    return outList

# For creating ReportingUnitsUUID
def retrieveReportingUnits(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = ReportingUnitUUIDdict[String1]
        except:
            outList = ''
    return outList

# For creating VariableSpecificUUID
def retrieveVariableSpecificUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = VariableSpecificUUIDdict[String1]
        except:
            outList = ''
    return outList

# For creating WaterSourceUUID
def retrieveWaterSourceUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = WaterSourceUUIDUUIDdict[String1]
        except:
            outList = ''
    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
MethodUUIDdict = pd.Series(df_method.MethodUUID.values, index = df_method.MethodName).to_dict()
outdf['MethodUUID'] = df_DM.apply(lambda row: retrieveMethodUUID(row['MethodUUID']), axis=1)

print("OrganizationUUID")
outdf.OrganizationUUID = "UDWRe"

print("ReportingUnitUUID")  # Using SiteNativeID to identify ID
ReportingUnitUUIDdict = pd.Series(df_reportingunits.ReportingUnitUUID.values, index = df_reportingunits.ReportingUnitNativeID).to_dict()
outdf['ReportingUnitUUID'] = df_DM.apply(lambda row: retrieveReportingUnits(row['ReportingUnitNativeID']), axis=1)

print("VariableSpecificUUID")
VariableSpecificUUIDdict = pd.Series(df_variables.VariableSpecificUUID.values, index = df_variables.VariableSpecificCV).to_dict()
outdf['VariableSpecificUUID'] = df_DM.apply(lambda row: retrieveVariableSpecificUUID(row['UT_VariableSpecificCV']), axis=1)

print("WaterSourceUUID")
WaterSourceUUIDUUIDdict = pd.Series(df_watersources.WaterSourceUUID.values, index = df_watersources.WaterSourceTypeCV).to_dict()
outdf['WaterSourceUUID'] = df_DM.apply(lambda row: retrieveWaterSourceUUID(row['inputWaterSourceTypeCV']), axis=1)

print("Amount")
outdf['Amount'] = df_DM['Amount']

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_DM['BeneficialUseCategory']

print("CommunityWaterSupplySystem")
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")
outdf.CropTypeCV = ""

print("CustomerTypeCV")
outdf.CustomerTypeCV = ""

print("DataPublicationDate")
outdf.DataPublicationDate = "11/03/2020"

print("DataPublicationDOI")
outdf.DataPublicationDOI = ""

print("InterbasinTransferFromID")
outdf.InterbasinTransferFromID = ""

print("InterbasinTransferToID")
outdf.InterbasinTransferToID = ""

print("IrrigatedAcreage")
outdf.IrrigatedAcreage = ""

print("IrrigationMethodCV")
outdf.IrrigationMethodCV = ""

print("PopulationServed")
outdf.PopulationServed = ""

print("PowerGeneratedGWh")
outdf.PowerGeneratedGWh = ""

print("PowerType")
outdf.PowerType = ""

print("PrimaryUseCategory")
outdf["PrimaryUseCategory"] =  df_DM['USGSCategoryCV']

print("ReportYearCV")
outdf['ReportYearCV'] = df_DM['ReportYearCV']

print("SDWISIdentifierCV")
outdf.SDWISIdentifierCV = ""

print("TimeframeEnd")
outdf["TimeframeEnd"] =  df_DM['TimeframeEnd']

print("TimeframeStart")
outdf["TimeframeStart"] =  df_DM['TimeframeStart']

print("Resetting Index")
outdf.reset_index()

print("out df updates...")
outdf = outdf.replace(np.nan, '')  # Replaces NaN values with blank.
outdf100 = outdf


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# issue of input file having too many duplicate rows of information
outdf100 = outdf100.drop_duplicates()


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")
dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# MethodUUID
outdf, dfpurge = TestErrorFunctions.MethodUUID_AG_Check(outdf, dfpurge)

# OrganizationUUID
outdf, dfpurge = TestErrorFunctions.OrganizationUUID_AG_Check(outdf, dfpurge)

# ReportingUnitUUID
outdf, dfpurge = TestErrorFunctions.ReportingUnitUUID_AG_Check(outdf, dfpurge)

# VariableSpecificUUID
outdf, dfpurge = TestErrorFunctions.VariableSpecificUUID_AG_Check(outdf, dfpurge)

# WaterSourceUUID
outdf, dfpurge = TestErrorFunctions.WaterSourceUUID_AG_Check(outdf, dfpurge)

# AllocationCropDutyAmount
outdf, dfpurge = TestErrorFunctions.AllocationCropDutyAmount_AG_Check(outdf, dfpurge)

# Amount
outdf, dfpurge = TestErrorFunctions.Amount_AG_Check(outdf, dfpurge)

# BeneficialUseCategory
outdf, dfpurge = TestErrorFunctions.BeneficialUseCategory_AG_Check(outdf, dfpurge)

# CommunityWaterSupplySystem
outdf, dfpurge = TestErrorFunctions.CommunityWaterSupplySystem_AG_Check(outdf, dfpurge)

# CropTypeCV
outdf, dfpurge = TestErrorFunctions.CropTypeCV_AG_Check(outdf, dfpurge)

# CustomerTypeCV
outdf, dfpurge = TestErrorFunctions.CustomerTypeCV_AG_Check(outdf, dfpurge)

# DataPublicationDate
outdf, dfpurge = TestErrorFunctions.DataPublicationDate_AG_Check(outdf, dfpurge)

# DataPublicationDOI
outdf, dfpurge = TestErrorFunctions.DataPublicationDOI_AG_Check(outdf, dfpurge)

# InterbasinTransferFromID
outdf, dfpurge = TestErrorFunctions.InterbasinTransferFromID_AG_Check(outdf, dfpurge)

# InterbasinTransferToID
outdf, dfpurge = TestErrorFunctions.InterbasinTransferToID_AG_Check(outdf, dfpurge)

# IrrigatedAcreage
outdf, dfpurge = TestErrorFunctions.IrrigatedAcreage_AG_Check(outdf, dfpurge)

# IrrigationMethodCV
outdf, dfpurge = TestErrorFunctions.IrrigationMethodCV_AG_Check(outdf, dfpurge)

# PopulationServed
outdf, dfpurge = TestErrorFunctions.PopulationServed_AG_Check(outdf, dfpurge)

# PowerGeneratedGWh
outdf, dfpurge = TestErrorFunctions.PowerGeneratedGWh_AG_Check(outdf, dfpurge)

# PowerType
outdf, dfpurge = TestErrorFunctions.PowerType_AG_Check(outdf, dfpurge)

# PrimaryUseCategory
outdf, dfpurge = TestErrorFunctions.PrimaryUseCategory_AG_Check(outdf, dfpurge)

# ReportYearCV
outdf, dfpurge = TestErrorFunctions.ReportYearCV_AG_Check(outdf, dfpurge)

# SDWISIdentifierCV
outdf, dfpurge = TestErrorFunctions.SDWISIdentifierCV_AG_Check(outdf, dfpurge)

# TimeframeEnd
outdf, dfpurge = TestErrorFunctions.TimeframeEnd_AG_Check(outdf, dfpurge)

# TimeframeStart
outdf, dfpurge = TestErrorFunctions.TimeframeStart_AG_Check(outdf, dfpurge)


# Export to new csv
############################################################################
print("Exporting dataframe outdf100 to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/aggregatedamounts.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/aggregatedamounts_missing.csv', index=False)

print("Done.")