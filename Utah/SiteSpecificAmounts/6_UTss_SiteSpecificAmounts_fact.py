# Last Updated: 12/14/2020
# Author: Ryan James
# Purpose: To extract UT site specific site amount use information and populate dataframe WaDE_QA 2.0.
# Notes: N/A

# Needed Libraries
############################################################################
import numpy as np
import pandas as pd
import os

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/CustomFunctions/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/SiteSpecificAmounts"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_MasterUTSiteSpecific.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_DM = pd.read_csv(M_fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.
df_variables = pd.read_csv(variables_fileInput)  # Variable dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

#WaDE dataframe columns
columnslist = [
    "MethodUUID",
    "OrganizationUUID",
    "SiteUUID",
    "VariableSpecificUUID",
    "WaterSourceUUID",
    "Amount",
    'AllocationCropDutyAmount',
    "AssociatedNativeAllocationIDs",
    'BeneficialUseCategory',
    "CommunityWaterSupplySystem",
    "CropTypeCV",
    "CustomerTypeCV",
    "DataPublicationDate",
    "DataPublicationDOI",
    "Geometry",
    "IrrigatedAcreage",
    "IrrigationMethodCV",
    "PopulationServed",
    "PowerGeneratedGWh",
    'PowerType',
    "PrimaryUseCategory",
    "ReportYearCV",
    "SDWISIdentifier",
    "TimeframeEnd",
    "TimeframeStart"]


# Custom Functions
############################################################################

# For creating VariableSpecificUUID
VariableSpecificUUIDdict = pd.Series(df_variables.VariableSpecificUUID.values, index = df_variables.VariableSpecificCV).to_dict()
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
WaterSourceUUIDdict = pd.Series(df_watersources.WaterSourceUUID.values, index = df_watersources.WaterSourceNativeID).to_dict()
def retrieveWaterSourceUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = WaterSourceUUIDdict[String1]
        except:
            outList = ''
    return outList

# For creating SiteUUID
df_sites['WaDEKey'] = df_sites['SiteNativeID'].astype(str) + df_sites['Latitude'].astype(str)
SitUUIDdict = pd.Series(df_sites.SiteUUID.values, index=df_sites.WaDEKey).to_dict()
def retrieveSiteUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = SitUUIDdict[String1]
        except:
            outList = ''
    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
outdf['MethodUUID'] = "UDWRi_Water Use Data"

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = df_DM.apply(lambda row: retrieveVariableSpecificUUID(row['in_VariableSpecificCV']), axis=1)

print("OrganizationUUID")
outdf['OrganizationUUID'] = "UDWRi"

print("WaterSourceUUID")
outdf['WaterSourceUUID'] = df_DM.apply(lambda row: retrieveWaterSourceUUID(row['in_WaterSourceNativeID']), axis=1)

print("SiteUUID")
df_DM['WaDEKey'] = df_DM['in_SiteNativeID'].astype(str) + df_DM['in_Latitude'].astype(str)
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['WaDEKey']), axis=1)

print("Amount")
outdf['Amount'] = df_DM['WaterUse']

print('AllocationCropDutyAmount')
outdf['AllocationCropDutyAmount'] = ""

print("AssociatedNativeAllocationIDs")
outdf['AssociatedNativeAllocationIDs'] = ""

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySystem'] = df_DM['System Name']

print('BeneficialUseCategory')
outdf['BeneficialUseCategory'] = df_DM['BenUse']

print("CropTypeCV")
outdf['CropTypeCV'] = ""

print("CustomerTypeCV")
outdf['CustomerTypeCV'] = df_DM['in_CustomerTypeCV']  # see preprocessing

print("DataPublicationDate")
outdf['DataPublicationDate'] = "06/14/2021"

print("DataPublicationDOI")
outdf['DataPublicationDOI'] = ""

print("Geometry")
outdf['Geometry'] = ""

print("IrrigatedAcreage")
outdf['IrrigatedAcreage'] = ""

print("IrrigationMethodCV")
outdf['IrrigationMethodCV'] = ""

print("PopulationServed")
outdf['PopulationServed'] = df_DM['Population']

print("PowerGeneratedGWh")
outdf['PowerGeneratedGWh'] = ""

print("PowerType")
outdf['PowerType'] = ""

print("PrimaryUseCategory")
outdf['PrimaryUseCategory'] = "Unspecified"

print("ReportYearCV")
outdf['ReportYearCV'] = df_DM['History Year']

print("SDWISIdentifier")
outdf['SDWISIdentifier'] = ""

print("TimeframeEnd")
outdf['TimeframeEnd'] = df_DM['in_TimeframeEnd']  # see preprocessing.

print("TimeframeStart")
outdf['TimeframeStart'] = df_DM['in_TimeframeStart']  # see preprocessing.

print("Resetting Index")
outdf.reset_index()


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# Dropping duplicate
# filter the whole table based on a unique combination of SiteNativeID, SiteName, SiteTypeCV, Longitude & Latitude
outdf = outdf.drop_duplicates().reset_index(drop=True)
outdf100 = outdf.replace(np.nan, '')  # Replaces NaN values with blank.


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")

dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# MethodUUID
outdf100, dfpurge = TestErrorFunctions.MethodUUID_SS_Check(outdf100, dfpurge)

# VariableSpecificUUID
outdf100, dfpurge = TestErrorFunctions.VariableSpecificUUID_SS_Check(outdf100, dfpurge)

# WaterSourceUUID
outdf100, dfpurge = TestErrorFunctions.WaterSourceUUID_SS_Check(outdf100, dfpurge)

# OrganizationUUID
outdf100, dfpurge = TestErrorFunctions.OrganizationUUID_SS_Check(outdf100, dfpurge)

# SiteUUID
outdf100, dfpurge = TestErrorFunctions.SiteUUID_SS_Check(outdf100, dfpurge)

# Amount
outdf100, dfpurge = TestErrorFunctions.Amount_SS_Check(outdf100, dfpurge)

# AllocationCropDutyAmount
outdf100, dfpurge = TestErrorFunctions.AllocationCropDutyAmount_SS_Check(outdf100, dfpurge)

# AssociatedNativeAllocationIDs
outdf100, dfpurge = TestErrorFunctions.AssociatedNativeAllocationIDs_SS_Check(outdf100, dfpurge)

# BeneficialUseCategory
outdf100, dfpurge = TestErrorFunctions.BeneficialUseCategory_SS_Check(outdf100, dfpurge)

# CommunityWaterSupplySystem
outdf100, dfpurge = TestErrorFunctions.CommunityWaterSupplySystem_SS_Check(outdf100, dfpurge)

# CropTypeCV
outdf100, dfpurge = TestErrorFunctions.CropTypeCV_SS_Check(outdf100, dfpurge)

# CustomerTypeCV
outdf100, dfpurge = TestErrorFunctions.CustomerTypeCV_SS_Check(outdf100, dfpurge)

# DataPublicationDate_
outdf100, dfpurge = TestErrorFunctions.DataPublicationDate_SS_Check(outdf100, dfpurge)

# DataPublicationDOI
outdf100, dfpurge = TestErrorFunctions.DataPublicationDOI_SS_Check(outdf100, dfpurge)

# Geometry
# ???? How to check for geometry datatype

# IrrigatedAcreage
outdf100, dfpurge = TestErrorFunctions.IrrigatedAcreage_SS_Check(outdf100, dfpurge)

# IrrigationMethodCV
outdf100, dfpurge = TestErrorFunctions.IrrigationMethodCV_SS_Check(outdf100, dfpurge)

# PopulationServed
outdf100, dfpurge = TestErrorFunctions.PopulationServed_SS_Check(outdf100, dfpurge)

# PowerGeneratedGWh
outdf100, dfpurge = TestErrorFunctions.PowerGeneratedGWh_SS_Check(outdf100, dfpurge)

# PowerType
outdf100, dfpurge = TestErrorFunctions.PowerType_SS_Check(outdf100, dfpurge)

# PrimaryUseCategory_
outdf100, dfpurge = TestErrorFunctions.PrimaryUseCategory_SS_Check(outdf100, dfpurge)

# ReportYearCV_
outdf100, dfpurge = TestErrorFunctions.ReportYearCV_SS_Check(outdf100, dfpurge)

# SDWISIdentifier
outdf100, dfpurge = TestErrorFunctions.SDWISIdentifier_SS_Check(outdf100, dfpurge)

# # TimeframeEnd
# outdf100, dfpurge = TestErrorFunctions.TimeframeEnd_SS_Check(outdf100, dfpurge)
#
# # TimeframeStart
# outdf100, dfpurge = TestErrorFunctions.TimeframeStart_SS_Check(outdf100, dfpurge)


# Export to new csv
############################################################################
print("Exporting dataframe outdf100 to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf100.to_csv('ProcessedInputData/sitespecificamounts.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/sitespecificamounts_missing.csv', index=False)

print("Done.")
