#Date Created: 11/23/2020
#Purpose: To extract MT water right use information and population dataframe for WaDE_QA 2.0.
#         1) Simple creation of working dataframe (df), with output dataframe (outdf).
#         2) Drop all nulls before combining duplicate rows on NativeID.

# Needed Libraries
############################################################################
import numpy as np
import pandas as pd
import os
from datetime import datetime

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/ErrorCheckCode")
import TestErrorFunctions

# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Montana/WaterAllocation"
os.chdir(workingDir)
DM_fileInput = "RawinputData/P_MontanaMaster.csv"
method_fileInput = "ProcessedInputData/methods.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_DM = pd.read_csv(DM_fileInput)  # The State's Master input dataframe.
df_method = pd.read_csv(method_fileInput)  # Method dataframe
df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

#WaDE dataframe columns
columnslist = [
    "AllocationApplicationDate",
    "AllocationAssociatedConsumptiveUseSiteIDs",
    "AllocationAssociatedWithdrawalSiteIDs",
    "AllocationBasisCV",
    "AllocationChangeApplicationIndicator",
    "AllocationCommunityWaterSupplySystem",
    "AllocationCropDutyAmount",
    "AllocationExpirationDate",
    "AllocationFlow_CFS",
    "AllocationLegalStatusCV",
    "AllocationNativeID",
    "AllocationOwner",
    "AllocationPriorityDate",
    "AllocationSDWISIdentifierCV",
    "AllocationTimeframeEnd",
    "AllocationTimeframeStart",
    "AllocationTypeCV",
    "AllocationVolume_AF",
    "BeneficialUseCategory",
    "CommunityWaterSupplySystem",
    "CropTypeCV",
    "CustomerTypeCV",
    "DataPublicationDate",
    "DataPublicationDOI",
    "ExemptOfVolumeFlowPriority",
    "GeneratedPowerCapacityMW",
    "IrrigatedAcreage",
    "IrrigationMethodCV",
    "LegacyAllocationIDs",
    "MethodUUID",
    "OrganizationUUID",
    "PopulationServed",
    "PowerType",
    "PrimaryUseCategory",
    "SiteUUID",
    "VariableSpecificUUID",
    "WaterAllocationNativeURL",
    "WaterSourceUUID"]

# Custom Functions
############################################################################

# For creating MethodUUID
MethodUUIDdict = pd.Series(df_method.MethodUUID.values, index = df_method.MethodTypeCV).to_dict()
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

# For creating SiteUUID
SiteUUIDDdict = pd.Series(df_sites.SiteUUID.values, index = df_sites.SiteNativeID).to_dict()
def retrieveSiteUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = SiteUUIDDdict[String1]
        except:
            outList = ''
    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
outdf['MethodUUID'] = df_DM.apply(lambda row: retrieveMethodUUID(row['inputMethodTypeCV']), axis=1)

print("OrganizationUUID")
outdf.OrganizationUUID = "MDNRC"

print("SiteUUID")
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['PODV_ID_SEQ']), axis=1)

print("VariableSpecificUUID")
outdf.VariableSpecificUUID = "MT_Consumptive Use"

##############################################################
print("WaterSourceUUID")

def assignWaterSourceName(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        outList = colrowValue
    return outList
df_DM['WaterSourceName'] = df_DM.apply(lambda row: assignWaterSourceName(row['SOURCE_NAME']), axis=1)

def assignWaterSourceTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        outList = colrowValue
    return outList
df_DM['WaterSourceTypeCV'] = df_DM.apply(lambda row: assignWaterSourceTypeCV(row['SOURCE_TYPE']), axis=1)

WaterSourceUUIDDict = df_watersources.set_index(['WaterSourceName', 'WaterSourceTypeCV']).to_dict(orient='dict')['WaterSourceUUID']
def retrieveWaterSourceUUID(A, B):
    try:
        outList = WaterSourceUUIDDict[(A, B)]
    except:
        outList = ''
    return outList

outdf['WaterSourceUUID'] = df_DM.apply(lambda row: retrieveWaterSourceUUID(row['WaterSourceName'], row['WaterSourceTypeCV']), axis=1)
##############################################################

print("AllocationApplicationDate")
outdf['AllocationApplicationDate'] = ""

print("AllocationAssociatedConsumptiveUseSiteIDs")
outdf.AllocationAssociatedConsumptiveUseSiteIDs = ""

print("AllocationAssociatedWithdrawalSiteIDs")
outdf.AllocationAssociatedWithdrawalSiteIDs = ""

print("AllocationBasisCV")
outdf.AllocationBasisCV = "Unknown"

print("AllocationChangeApplicationIndicator")
outdf['AllocationChangeApplicationIndicator'] = ""

print("AllocationCommunityWaterSupplySystem")
outdf['AllocationCommunityWaterSupplySystem'] = ""

print("AllocationCropDutyAmount")
outdf['AllocationCropDutyAmount'] = ""

print("AllocationExpirationDate")
outdf['AllocationExpirationDate'] = ""

print("AllocationFlow_CFS")
outdf['AllocationFlow_CFS'] = df_DM['FLW_RT_CFS']

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_DM['WR_STATUS']

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_DM['WR_NUMBER']

print("AllocationOwner")
outdf['AllocationOwner'] = df_DM['ALL_OWNERS']

print("AllocationSDWISIdentifierCV")
outdf.AllocationSDWISIdentifierCV = ""

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_DM['ENF_PRIORITY_DATE']

print("AllocationTimeframeEnd")
outdf['AllocationTimeframeEnd'] = df_DM['inputTimeframeEnd']

print("AllocationTimeframeStart")
outdf['AllocationTimeframeStart'] = df_DM['inputTimeframeStart']

print("AllocationTypeCV")
outdf['AllocationTypeCV'] = df_DM['WR_TYPE']

print("AllocationVolume_AF")
outdf['AllocationVolume_AF'] = df_DM['VOLUME']

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_DM['PURPOSES']

print("CommunityWaterSupplySystem")
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")
outdf.CropTypeCV = ""

print("CustomerTypeCV")
outdf.CustomerTypeCV = ""

print("DataPublicationDate")
outdf.DataPublicationDate = "11/20/2020"

print("DataPublicationDOI")
outdf['DataPublicationDOI'] = df_DM['ABST_LINK']

print("ExemptOfVolumeFlowPriority")
outdf['ExemptOfVolumeFlowPriority'] = "0"

print("GeneratedPowerCapacityMW")
outdf.GeneratedPowerCapacityMW = ""

print("IrrigatedAcreage")
outdf['IrrigatedAcreage'] = df_DM['MAX_ACRES']

print("IrrigationMethodCV")
outdf.IrrigationMethodCV = ""

print("LegacyAllocationIDs")
outdf.LegacyAllocationIDs = ""

print("PopulationServed")
outdf.PopulationServed = ""

print("PowerType")
outdf.PowerType = ""

print("PrimaryUseCategory")
outdf.PrimaryUseCategory = "Irrigation"

print("WaterAllocationNativeURL")
outdf.WaterAllocationNativeURL = ""

print("Resetting Index")
outdf.reset_index()

print("Joining outdf duplicates based on AllocationNativeID...")
outdf = outdf.replace(np.nan, '')  # Replaces NaN values with blank.
outdf100 = pd.DataFrame(columns=columnslist)  # The output dataframe for CSV.
outdf100 = outdf.groupby('AllocationNativeID').agg(lambda x: ','.join([str(elem) for elem in (list(set(x)))])).replace(np.nan, '').reset_index()


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")
dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# MethodUUID
outdf100, dfpurge = TestErrorFunctions.MethodUUID_AA_Check(outdf100, dfpurge)

# OrganizationUUID
outdf100, dfpurge = TestErrorFunctions.OrganizationUUID_AA_Check(outdf100, dfpurge)

# SiteUUID
outdf100, dfpurge = TestErrorFunctions.SiteUUID_AA_Check(outdf100, dfpurge)

# VariableSpecificUUID
outdf100, dfpurge = TestErrorFunctions.VariableSpecificUUID_AA_Check(outdf100, dfpurge)

# WaterSourceUUID
outdf100, dfpurge = TestErrorFunctions.WaterSourceUUID_AA_Check(outdf100, dfpurge)

# AllocationApplicationDateID
outdf100, dfpurge = TestErrorFunctions.AllocationApplicationDate_AA_Check(outdf100, dfpurge)

# AllocationAssociatedConsumptiveUseSiteIDs
outdf100, dfpurge = TestErrorFunctions.AllocationAssociatedConsumptiveUseSiteIDs_AA_Check(outdf100, dfpurge)

# AllocationAssociatedWithdrawalSiteIDs
outdf100, dfpurge = TestErrorFunctions.AllocationAssociatedWithdrawalSiteIDs_AA_Check(outdf100, dfpurge)

# AllocationBasisCV
outdf100, dfpurge = TestErrorFunctions.AllocationBasisCV_AA_Check(outdf100, dfpurge)

# AllocationChangeApplicationIndicator
outdf100, dfpurge = TestErrorFunctions.AllocationChangeApplicationIndicator_AA_Check(outdf100, dfpurge)

# AllocationCommunityWaterSupplySystem
outdf100, dfpurge = TestErrorFunctions.AllocationCommunityWaterSupplySystem_AA_Check(outdf100, dfpurge)

# AllocationCropDutyAmount
outdf100, dfpurge = TestErrorFunctions.AllocationCropDutyAmount_AA_Check(outdf100, dfpurge)

# AllocationExpirationDate
outdf100, dfpurge = TestErrorFunctions.AllocationExpirationDate_AA_Check(outdf100, dfpurge)

# # AllocationFlow_CFS_float_Yes & AllocationVolume_AF_float_Yes
outdf100, dfpurge = TestErrorFunctions.AllocationFlowVolume_CFSAF_float_Yes_AA_Check(outdf100, dfpurge)

# AllocationLegalStatusCV
outdf100, dfpurge = TestErrorFunctions.AllocationLegalStatusCV_AA_Check(outdf100, dfpurge)

# AllocationNativeID
outdf100, dfpurge = TestErrorFunctions.AllocationNativeID_AA_Check(outdf100, dfpurge)

# AllocationOwner
outdf100, dfpurge = TestErrorFunctions.AllocationOwner_AA_Check(outdf100, dfpurge)

# AllocationPriorityDate
outdf100, dfpurge = TestErrorFunctions.AllocationPriorityDate_AA_Check(outdf100, dfpurge)

# AllocationSDWISIdentifierCV
outdf100, dfpurge = TestErrorFunctions.AllocationSDWISIdentifierCV_AA_Check(outdf100, dfpurge)

# AllocationTimeframeEnd
outdf100, dfpurge = TestErrorFunctions.AllocationTimeframeEnd_AA_Check(outdf100, dfpurge)

# AllocationTimeframeStart
outdf100, dfpurge = TestErrorFunctions.AllocationTimeframeStart_AA_Check(outdf100, dfpurge)

# AllocationTypeCV
outdf100, dfpurge = TestErrorFunctions.AllocationTypeCV_AA_Check(outdf100, dfpurge)

# BeneficialUseCategory
outdf100, dfpurge = TestErrorFunctions.BeneficialUseCategory_AA_Check(outdf100, dfpurge)

# CommunityWaterSupplySystem
outdf100, dfpurge = TestErrorFunctions.CommunityWaterSupplySystem_AA_Check(outdf100, dfpurge)

# CropTypeCV
outdf100, dfpurge = TestErrorFunctions.CropTypeCV_AA_Check(outdf100, dfpurge)

# CustomerTypeCV
outdf100, dfpurge = TestErrorFunctions.CustomerTypeCV_AA_Check(outdf100, dfpurge)

# DataPublicationDate
outdf100, dfpurge = TestErrorFunctions.DataPublicationDate_AA_Check(outdf100, dfpurge)

# DataPublicationDOI
outdf100, dfpurge = TestErrorFunctions.DataPublicationDOI_AA_Check(outdf100, dfpurge)

# # ExemptOfVolumeFlowPriority
# outdf100, dfpurge = TestErrorFunctions.ExemptOfVolumeFlowPriority_AA_Check(outdf100, dfpurge)

# GeneratedPowerCapacityMW
outdf100, dfpurge = TestErrorFunctions.GeneratedPowerCapacityMW_AA_Check(outdf100, dfpurge)

# IrrigatedAcreage
outdf100, dfpurge = TestErrorFunctions.IrrigatedAcreage_AA_Check(outdf100, dfpurge)

# IrrigationMethodCV
outdf100, dfpurge = TestErrorFunctions.IrrigationMethodCV_AA_Check(outdf100, dfpurge)

# LegacyAllocationIDs
outdf100, dfpurge = TestErrorFunctions.LegacyAllocationIDs_AA_Check(outdf100, dfpurge)

# PopulationServed
outdf100, dfpurge = TestErrorFunctions.PopulationServed_AA_Check(outdf100, dfpurge)

# PowerType
outdf100, dfpurge = TestErrorFunctions.PowerType_AA_Check(outdf100, dfpurge)

# PrimaryUseCategory
outdf100, dfpurge = TestErrorFunctions.PrimaryUseCategory_AA_Check(outdf100, dfpurge)

# WaterAllocationNativeURL
outdf100, dfpurge = TestErrorFunctions.WaterAllocationNativeURL_AA_Check(outdf100, dfpurge)


# Export to new csv
############################################################################
print("Exporting dataframe outdf100 to csv...")
# The working output DataFrame for WaDE 2.0 input.
outdf100.to_csv('ProcessedInputData/waterallocations.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/waterallocations_missing.csv')  # index=False,

print("Done.")