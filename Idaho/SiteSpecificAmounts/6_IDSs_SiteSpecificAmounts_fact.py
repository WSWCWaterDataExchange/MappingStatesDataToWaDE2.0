#Last Updated: 03/16/2021
#Author: Ryan James (WSWC)
#Purpose: To create ID site specific site amount use information and population dataframe WaDE_QA 2.0.
#Notes:

# Needed Libraries
############################################################################
import numpy as np
import pandas as pd
import os

# Site lat and long already converted.
# from pyproj import Transformer, transform
# transformer = Transformer.from_crs(4269, 4326)
# # NAD83 projection = epsg:4269.
# # WGS84 projection used by WaDE 2.0 = epsg:4326.

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Idaho/SiteSpecificAmounts"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_idSSMaster.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_DM = pd.read_csv(M_fileInput)  # The State's Master input dataframe.
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

# For creating WaterSourceUUID
# ID has a very simple ss watersource at this time.
# WaterSourceUUIDdict = pd.Series(df_watersources.WaterSourceUUID.values, index=df_watersources.WaterSourceNativeID).to_dict()
# def retrieveWaterSourceUUID(colrowValue):
#     if colrowValue == '' or pd.isnull(colrowValue):
#         outList = ''
#     else:
#         String1 = colrowValue
#         try:
#             outList = WaterSourceUUIDdict[String1]
#         except:
#             outList = ''
#     return outList

# For creating SiteUUID
SitUUIDdict = pd.Series(df_sites.SiteUUID.values, index=df_sites.SiteNativeID).to_dict()
def retrieveSiteUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = str(colrowValue).strip()
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
outdf['MethodUUID'] = "IDWR_AquaInfo"

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = "IDWR_Site Specific"

print("OrganizationUUID")
outdf['OrganizationUUID'] = "IDWR"

print("WaterSourceUUID")
outdf['WaterSourceUUID'] = "IDss_WS1"

print("SiteUUID") # Using SiteNativeID
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['identifier']), axis=1)

print("Amount")
outdf['Amount'] = df_DM['numericValue1'].astype(float)

print('AllocationCropDutyAmount')
outdf['AllocationCropDutyAmount'] = ""

print("AssociatedNativeAllocationIDs")
outdf['AssociatedNativeAllocationIDs'] = ""

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySystem'] = ""

print('BeneficialUseCategory')
outdf['BeneficialUseCategory'] = "Unspecified"

print("CropTypeCV")
outdf['CropTypeCV'] = ""

print("CustomerTypeCV")
outdf['CustomerTypeCV'] = ""

print("DataPublicationDate")
outdf['DataPublicationDate'] = "03/16/2021"

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
outdf['PrimaryUseCategory'] = "Unspecified"

print("ReportYearCV")
outdf['ReportYearCV'] = df_DM['in_ReportYear'].astype(int)

print("SDWISIdentifier")
outdf['SDWISIdentifier'] = ""

print("TimeframeEnd")
outdf['TimeframeEnd'] = df_DM['timeStamp']

print("TimeframeStart")
outdf['TimeframeStart'] = df_DM['timeStamp']

print("Resetting Index")
outdf.reset_index()


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

print("Joining outdf duplicates based on AllocationNativeID...")
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

# TimeframeEnd
outdf100, dfpurge = TestErrorFunctions.TimeframeEnd_SS_Check(outdf100, dfpurge)

# TimeframeStart
outdf100, dfpurge = TestErrorFunctions.TimeframeStart_SS_Check(outdf100, dfpurge)


# Export to new csv
############################################################################
print("Exporting dataframe outdf100 to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf100.to_csv('ProcessedInputData/sitespecificamounts.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/sitespecificamounts_missing.csv', index=False)

print("Done.")
