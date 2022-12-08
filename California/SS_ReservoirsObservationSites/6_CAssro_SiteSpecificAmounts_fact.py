#Last Updated: 03/24/2022
#Author: Ryan James (WSWC)
#Purpose: To create CA site specific site amount use information and population dataframe WaDE_QA 2.0.
#Notes:  1) Because of the unique site situation with duplicate SiteNativeID's, we need a way to create a unique key for dictionary look up values.

# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/ErrorCheckCode")
import TestErrorFunctions



# Inputs
############################################################################
print("Reading input csv...")
workingDir = "G:/Shared drives/WaDE Data/California/SS_ReservoirsObservationSites"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_caObsRecords.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_DM = pd.read_csv(M_fileInput)
df_variables = pd.read_csv(variables_fileInput)  # Variable dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

#WaDE dataframe columns
columnslist = [
    "WaDEUUID",
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
SitUUIDdict = pd.Series(df_sites.SiteUUID.values, index=df_sites.SiteNativeID).to_dict()
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
outdf['MethodUUID'] = "CAssro_M1"

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = df_DM.apply(lambda row: retrieveVariableSpecificUUID(row['in_VariableSpecificCV']), axis=1)

print("OrganizationUUID")
outdf['OrganizationUUID'] = "CAssro_O1"

print("WaterSourceUUID") # Using WaterSourceType
outdf['WaterSourceUUID'] = df_DM.apply(lambda row: retrieveWaterSourceUUID(row['in_WaterSourceNativeID']), axis=1)

print("SiteUUID") # Using SiteNativeID
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['in_SiteNativeID']), axis=1)

print("Amount")
outdf['Amount'] = df_DM['in_Amount'].astype(float)  # See pre-processing.

print('AllocationCropDutyAmount')
outdf['AllocationCropDutyAmount'] = ""

print("AssociatedNativeAllocationIDs")
outdf['AssociatedNativeAllocationIDs'] = ""

print('BeneficialUseCategory')
outdf['BeneficialUseCategory'] = df_DM['in_BenUse']  # See pre-processing.

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySystem'] = df_DM['in_CommunityWaterSupplySystem']  # See pre-processing.

print("CropTypeCV")
outdf['CropTypeCV'] = ""

print("CustomerTypeCV")
outdf['CustomerTypeCV'] = ""

print("DataPublicationDate")
outdf['DataPublicationDate'] = "03/24/2022"

print("DataPublicationDOI")
outdf['DataPublicationDOI'] = ""

print("Geometry")
outdf['Geometry'] = ""

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
outdf['PrimaryUseCategory'] = df_DM['in_BenUse']  # See pre-processing.

print("ReportYearCV")
outdf['ReportYearCV'] = df_DM['in_ReportYearCV'].astype(int)

print("SDWISIdentifier")
outdf['SDWISIdentifier'] = ""

print("TimeframeEnd")
outdf['TimeframeEnd'] = df_DM['in_date']  # See pre-processing.

print("TimeframeStart")
outdf['TimeframeStart'] = df_DM['in_date']  # See pre-processing.

print("Adding Data Assessment UUID")
outdf['WaDEUUID'] = ""

print("Resetting Index")
outdf.reset_index()


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

outdf = outdf.replace(np.nan, "").drop_duplicates().reset_index(drop=True)


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")
purgecolumnslist = ["ReasonRemoved", "WaDEUUID", "RowIndex", "IncompleteField_1", "IncompleteField_2"]
dfpurge = pd.DataFrame(columns=purgecolumnslist) # Purge DataFrame to hold removed elements

# MethodUUID
outdf, dfpurge = TestErrorFunctions.MethodUUID_SS_Check(outdf, dfpurge)

# VariableSpecificUUID
outdf, dfpurge = TestErrorFunctions.VariableSpecificUUID_SS_Check(outdf, dfpurge)

# WaterSourceUUID
outdf, dfpurge = TestErrorFunctions.WaterSourceUUID_SS_Check(outdf, dfpurge)

# OrganizationUUID
outdf, dfpurge = TestErrorFunctions.OrganizationUUID_SS_Check(outdf, dfpurge)

# SiteUUID
outdf, dfpurge = TestErrorFunctions.SiteUUID_SS_Check(outdf, dfpurge)

# Amount
outdf, dfpurge = TestErrorFunctions.Amount_SS_Check(outdf, dfpurge)

# AllocationCropDutyAmount
outdf, dfpurge = TestErrorFunctions.AllocationCropDutyAmount_SS_Check(outdf, dfpurge)

# AssociatedNativeAllocationIDs
outdf, dfpurge = TestErrorFunctions.AssociatedNativeAllocationIDs_SS_Check(outdf, dfpurge)

# BeneficialUseCategory
outdf, dfpurge = TestErrorFunctions.BeneficialUseCategory_SS_Check(outdf, dfpurge)

# CommunityWaterSupplySystem
outdf, dfpurge = TestErrorFunctions.CommunityWaterSupplySystem_SS_Check(outdf, dfpurge)

# CropTypeCV
outdf, dfpurge = TestErrorFunctions.CropTypeCV_SS_Check(outdf, dfpurge)

# CustomerTypeCV
outdf, dfpurge = TestErrorFunctions.CustomerTypeCV_SS_Check(outdf, dfpurge)

# DataPublicationDate_
outdf, dfpurge = TestErrorFunctions.DataPublicationDate_SS_Check(outdf, dfpurge)

# DataPublicationDOI
outdf, dfpurge = TestErrorFunctions.DataPublicationDOI_SS_Check(outdf, dfpurge)

# Geometry
# ???? How to check for geometry datatype

# IrrigatedAcreage
outdf, dfpurge = TestErrorFunctions.IrrigatedAcreage_SS_Check(outdf, dfpurge)

# IrrigationMethodCV
outdf, dfpurge = TestErrorFunctions.IrrigationMethodCV_SS_Check(outdf, dfpurge)

# PopulationServed
outdf, dfpurge = TestErrorFunctions.PopulationServed_SS_Check(outdf, dfpurge)

# PowerGeneratedGWh
outdf, dfpurge = TestErrorFunctions.PowerGeneratedGWh_SS_Check(outdf, dfpurge)

# PowerType
outdf, dfpurge = TestErrorFunctions.PowerType_SS_Check(outdf, dfpurge)

# PrimaryUseCategory_
outdf, dfpurge = TestErrorFunctions.PrimaryUseCategory_SS_Check(outdf, dfpurge)

# ReportYearCV_
outdf, dfpurge = TestErrorFunctions.ReportYearCV_SS_Check(outdf, dfpurge)

# SDWISIdentifier
outdf, dfpurge = TestErrorFunctions.SDWISIdentifier_SS_Check(outdf, dfpurge)

# # TimeframeEnd
# outdf, dfpurge = TestErrorFunctions.TimeframeEnd_SS_Check(outdf, dfpurge)
#
# # TimeframeStart
# outdf, dfpurge = TestErrorFunctions.TimeframeStart_SS_Check(outdf, dfpurge)


# Remove WaDEUUID field from import file (only needed for purge info).
############################################################################
print("Drop Assessment WaDEUUID")
outdf = outdf.drop(['WaDEUUID'], axis=1)


# Export to new csv
############################################################################
print("Exporting outdf and dfpurge dataframes...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/sitespecificamounts.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_excel('ProcessedInputData/sitespecificamounts_missing.xlsx', index=False)

print("Done.")
