# Date Created: 05/13/2021
# Author: Ryan James (WSWC)
# Purpose: To create NV agg aggregated information and populate a dataframe WaDEQA 2.0.
#          1) Simple creation of working dataframe (df), with output dataframe (outdf).
#          2) Drop all nulls before combining duplicate rows on NativeID.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/CustomFunctions/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Nevada/AggregatedAmounts"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_nvAggMaster.csv"
method_fileInput = "ProcessedInputData/methods.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
reportingunits_fileInput = "ProcessedInputData/reportingunits.csv"

df_DM = pd.read_csv(M_fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.
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

# For creating ReportingUnitsUUID
ReportingUnitUUIDdict = pd.Series(df_reportingunits.ReportingUnitUUID.values, index = df_reportingunits.ReportingUnitNativeID).to_dict()
def retrieveReportingUnits(colrowValue):
    if colrowValue == "" or pd.isnull(colrowValue):
        outList = ""
    else:
        String1 = colrowValue
        try:
            outList = ReportingUnitUUIDdict[String1]
        except:
            outList = ""
    return outList

# For creating BeneficialUse
BeneficialUseDict = {
    "COM" : "Commercial",
    "CON" : "Construction",
    "DOM" : "Domestic",
    "ENV" : "Environmental",
    "IND" : "Industrial",
    "IRR" : "Irrigation",
    "MM" : "Mining and Milling",
    "MUN" : "Municipal",
    "PWR" : "Power",
    "QM" : "Quasi-Municipal",
    "REC" : "Recreational",
    "STK" : "Stockwater",
    "WLD" : "Wildlife"}
def assignBeneficialUse(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        String1 = colrowValue.strip()
        try:
            outList = BeneficialUseDict[String1]
        except:
            outList = "Unspecified"

    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
outdf['MethodUUID'] = "NVDWR_Water Use"

print("OrganizationUUID")
outdf['OrganizationUUID'] = "NVDWR"

print("ReportingUnitUUID")
outdf['ReportingUnitUUID'] = df_DM.apply(lambda row: retrieveReportingUnits(row['in_ReportingUnitNativeID']), axis=1)

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = "NVDWR_Withdrawal"

print("WaterSourceUUID")
outdf['WaterSourceUUID'] = "NVag_WS1"  # only the one to report at this time

print("Amount")
outdf['Amount'] = df_DM['in_Amount']

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_DM.apply(lambda row: assignBeneficialUse(row['NV_BenUse']), axis=1)

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySyste'] = ""

print("CropTypeCV")
outdf['CropTypeCV'] = ""

print("CustomerTypeCV")
outdf['CustomerTypeCV'] = ""

print("DataPublicationDate")
outdf['DataPublicationDate'] = "05/13/2021"

print("DataPublicationDOI")
outdf['DataPublicationDOI'] = ""

print("InterbasinTransferFromID")
outdf['InterbasinTransferFromID'] = ""

print("InterbasinTransferToID")
outdf['InterbasinTransferToID'] = ""

print("IrrigatedAcreage")
outdf['IrrigatedAcreage'] = ""

print("IrrigationMethodCV")
outdf['IrrigationMethodCV'] = ""

print("PopulationServed")
outdf['PopulationServed'] = ""

print("PowerGeneratedGWh")
outdf['PowerGeneratedGWh'] = ""

print("PowerType")
outdf['PowerType'] = ""

print("PrimaryUseCategory")
outdf['PrimaryUseCategory'] = "Unspecified"

print("ReportYearCV")
outdf['ReportYearCV'] = df_DM['Year']

print("SDWISIdentifierCV")
outdf['SDWISIdentifierCV'] = ""

print("TimeframeEnd")
outdf['TimeframeEnd'] = df_DM['in_TimeframeEnd']

print("TimeframeStart")
outdf['TimeframeStart'] = df_DM['in_TimeframeStart']

print("Resetting Index")
outdf.reset_index()

print("out df updates...")
outdf = outdf.replace(np.nan, '')  # Replaces NaN values with blank.
outdf100 = outdf


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# None at the moment


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
