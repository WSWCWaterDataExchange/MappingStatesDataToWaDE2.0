#Date Updated: 05/09/2022
#Purpose: To extract CA water right information and population dataframe for WaDE_QA 2.0.
#         1) Simple creation of working dataframe (df), with output dataframe (outdf).
#         2) Drop all nulls before combining duplicate rows on NativeID.


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
workingDir = "G:/Shared drives/WaDE Data/California/WaterAllocation"
os.chdir(workingDir)
DM_fileInput = "RawinputData/P_CaliforniaMaster.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_DM = pd.read_csv(DM_fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

#WaDE dataframe columns
columnslist = [
    "MethodUUID",
    "OrganizationUUID",
    "SiteUUID",
    "VariableSpecificUUID",
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
    "OwnerClassificationCV",
    "PopulationServed",
    "PowerType",
    "PrimaryUseCategory",
    "WaterAllocationNativeURL"]

# Custom Functions
############################################################################

# For Creating SiteUUID
SitUUIDdict = pd.Series(df_sites.SiteUUID.values, index = df_sites.SiteNativeID).to_dict()
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

# For creating BeneficialUseCategory
def assignBeneficialUseCategory(colrowValue):
    colrowValue = str(colrowValue).strip()
    if colrowValue == "" or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        try:
            outList = str(colrowValue).strip()
        except:
            outList = "Unspecified"
    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")

outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
outdf['MethodUUID'] = "CAwr_M1"

print("OrganizationUUID")
outdf['OrganizationUUID'] = "CAwr_O1"

#####################
print("SiteUUID")
def assignSiteNativeID(colrowValue):
    if colrowValue == "" or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        try:
            #outList = str(colrowValue).strip()
            outList = colrowValue
        except:
            outList = "Unspecified"
    return outList
df_DM['in_SiteNativeID'] = df_DM.apply(lambda row: assignSiteNativeID(row['POD_ID']), axis=1)
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['in_SiteNativeID']), axis=1)
#####################

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = "CAwr_V1"

print("AllocationApplicationDate")
outdf['AllocationApplicationDate'] = ""

print("AllocationAssociatedConsumptiveUseSiteIDs")
outdf['AllocationAssociatedConsumptiveUseSiteIDs'] = ""

print("AllocationAssociatedWithdrawalSiteIDs")
outdf['AllocationAssociatedWithdrawalSiteIDs'] = ""

print("AllocationBasisCV")
outdf['AllocationBasisCV'] = ""

print("AllocationChangeApplicationIndicator")
outdf['AllocationChangeApplicationIndicator'] = ""

print("AllocationCommunityWaterSupplySystem")
outdf['AllocationCommunityWaterSupplySystem'] = ""

print("AllocationCropDutyAmount")
outdf['AllocationCropDutyAmount'] = ""

print("AllocationExpirationDate")
outdf['AllocationExpirationDate'] = ""

print("AllocationFlow_CFS")
outdf['AllocationFlow_CFS'] = ""

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_DM['WR_STATUS']

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_DM['WR_WATER_RIGHT_ID'].astype(str)

print("AllocationOwner")
outdf['AllocationOwner'] = df_DM['in_WaDEOwner']

print("AllocationSDWISIdentifierCV")
outdf['AllocationSDWISIdentifierCV'] = ""

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_DM['in_AllocationPriorityDate']

print("AllocationTimeframeEnd")
outdf['AllocationTimeframeEnd'] = df_DM['in_AllocationTimeframeEnd']

print("AllocationTimeframeStart")
outdf['AllocationTimeframeStart'] = df_DM['in_AllocationTimeframeStart']

print("AllocationTypeCV")
outdf['AllocationTypeCV'] = df_DM['WR_TYPE']

print("AllocationVolume_AF")
outdf['AllocationVolume_AF'] = df_DM['FACE_VALUE_AMOUNT']

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_DM.apply(lambda row: assignBeneficialUseCategory(row['USE_CODE']), axis=1)

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySystem'] = ""

print("CropTypeCV")
outdf['CropTypeCV'] = ""

print("CustomerTypeCV")
outdf['CustomerTypeCV'] = ""

print("DataPublicationDate")
outdf['DataPublicationDate'] = "07/21/2021"

print("DataPublicationDOI")
outdf['DataPublicationDOI'] = ""

print("ExemptOfVolumeFlowPriority")
outdf['ExemptOfVolumeFlowPriority'] = "0"

print("GeneratedPowerCapacityMW")
outdf['GeneratedPowerCapacityMW'] = ""

print("IrrigatedAcreage")
outdf['IrrigatedAcreage'] = ""

print("IrrigationMethodCV")
outdf['IrrigationMethodCV'] = ""

print("LegacyAllocationIDs")
outdf['LegacyAllocationIDs'] = ""

#####################################
print("OwnerClassificationCV")
# Temp solution to populate OwnerClassificationCV field.
# Use Custom import file
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/CustomFunctions/OwnerClassification")
import OwnerClassificationField
outdf['OwnerClassificationCV'] = outdf.apply(lambda row: OwnerClassificationField.CreateOwnerClassification(row['AllocationOwner']), axis=1)
#####################################

print("PopulationServed")
outdf['PopulationServed'] = ""

print("PowerType")
outdf['PowerType'] = ""

print("PrimaryUseCategory")
outdf['PrimaryUseCategory'] = "Unspecified"

print("WaterAllocationNativeURL")
outdf['WaterAllocationNativeURL'] = ""

print("Resetting Index")
outdf.reset_index()

print("Joining outdf duplicates based on key fields...")
outdf = outdf.replace(np.nan, "")  # Replaces NaN values with blank.
groupbyList = ['AllocationNativeID', 'AllocationFlow_CFS', 'AllocationVolume_AF']
outdf = outdf.groupby(groupbyList).agg(lambda x: ','.join([str(elem) for elem in (list(set(x))) if elem!=''])).replace(np.nan, "").reset_index()
outdf = outdf[columnslist]  # reorder the dataframe's columns based on columnslist


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# Date Noted: 05/25/2021
# Note: OwnerClassificationCV can only accept 1 entry at this time. Error due to above merge / we don't allow multiple OwnerClassificationCV.
def tempfixOCSV(colrowValueA):
    result = colrowValueA.split(",", 1)[0]  # pass in text, split on "," & return first value.
    return result
outdf['OwnerClassificationCV']  = outdf.apply(lambda row: tempfixOCSV(row['OwnerClassificationCV']), axis=1)

# Temp solution to populate PrimaryUseCategory field.
# Use Custom import file
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/CustomFunctions/AssignPrimaryUserCategory")
import AssignPrimaryUserCategory
outdf['PrimaryUseCategory'] = outdf.apply(lambda row: AssignPrimaryUserCategory.retrievePrimaryUseCategory(row['BeneficialUseCategory']), axis=1)


#Error checking each field
############################################################################
print("Error checking each field.  Purging bad inputs.")
purgecolumnslist = ["ReasonRemoved", "RowIndex", "IncompleteField_1", "IncompleteField_2"]
dfpurge = pd.DataFrame(columns=purgecolumnslist) # Purge DataFrame to hold removed elements

# MethodUUID
outdf, dfpurge = TestErrorFunctions.MethodUUID_AA_Check(outdf, dfpurge)

# OrganizationUUID
outdf, dfpurge = TestErrorFunctions.OrganizationUUID_AA_Check(outdf, dfpurge)

# SiteUUID
outdf, dfpurge = TestErrorFunctions.SiteUUID_AA_Check(outdf, dfpurge)

# VariableSpecificUUID
outdf, dfpurge = TestErrorFunctions.VariableSpecificUUID_AA_Check(outdf, dfpurge)

# AllocationApplicationDateID
outdf, dfpurge = TestErrorFunctions.AllocationApplicationDate_AA_Check(outdf, dfpurge)

# AllocationAssociatedConsumptiveUseSiteIDs
outdf, dfpurge = TestErrorFunctions.AllocationAssociatedConsumptiveUseSiteIDs_AA_Check(outdf, dfpurge)

# AllocationAssociatedWithdrawalSiteIDs
outdf, dfpurge = TestErrorFunctions.AllocationAssociatedWithdrawalSiteIDs_AA_Check(outdf, dfpurge)

# AllocationBasisCV
outdf, dfpurge = TestErrorFunctions.AllocationBasisCV_AA_Check(outdf, dfpurge)

# AllocationChangeApplicationIndicator
outdf, dfpurge = TestErrorFunctions.AllocationChangeApplicationIndicator_AA_Check(outdf, dfpurge)

# AllocationCommunityWaterSupplySystem
outdf, dfpurge = TestErrorFunctions.AllocationCommunityWaterSupplySystem_AA_Check(outdf, dfpurge)

# AllocationCropDutyAmount
outdf, dfpurge = TestErrorFunctions.AllocationCropDutyAmount_AA_Check(outdf, dfpurge)

# AllocationExpirationDate
outdf, dfpurge = TestErrorFunctions.AllocationExpirationDate_AA_Check(outdf, dfpurge)

# # AllocationFlow_CFS_float_Yes & AllocationVolume_AF_float_Yes
outdf, dfpurge = TestErrorFunctions.AllocationFlowVolume_CFSAF_float_Yes_AA_Check(outdf, dfpurge)

# AllocationLegalStatusCV
outdf, dfpurge = TestErrorFunctions.AllocationLegalStatusCV_AA_Check(outdf, dfpurge)

# AllocationNativeID
outdf, dfpurge = TestErrorFunctions.AllocationNativeID_AA_Check(outdf, dfpurge)

# AllocationOwner
outdf, dfpurge = TestErrorFunctions.AllocationOwner_AA_Check(outdf, dfpurge)

# AllocationPriorityDate
outdf, dfpurge = TestErrorFunctions.AllocationPriorityDate_AA_Check(outdf, dfpurge)

# AllocationSDWISIdentifierCV
outdf, dfpurge = TestErrorFunctions.AllocationSDWISIdentifierCV_AA_Check(outdf, dfpurge)

# AllocationTimeframeEnd
outdf, dfpurge = TestErrorFunctions.AllocationTimeframeEnd_AA_Check(outdf, dfpurge)

# AllocationTimeframeStart
outdf, dfpurge = TestErrorFunctions.AllocationTimeframeStart_AA_Check(outdf, dfpurge)

# AllocationTypeCV
outdf, dfpurge = TestErrorFunctions.AllocationTypeCV_AA_Check(outdf, dfpurge)

# BeneficialUseCategory
outdf, dfpurge = TestErrorFunctions.BeneficialUseCategory_AA_Check(outdf, dfpurge)

# CommunityWaterSupplySystem
outdf, dfpurge = TestErrorFunctions.CommunityWaterSupplySystem_AA_Check(outdf, dfpurge)

# CropTypeCV
outdf, dfpurge = TestErrorFunctions.CropTypeCV_AA_Check(outdf, dfpurge)

# CustomerTypeCV
outdf, dfpurge = TestErrorFunctions.CustomerTypeCV_AA_Check(outdf, dfpurge)

# DataPublicationDate
outdf, dfpurge = TestErrorFunctions.DataPublicationDate_AA_Check(outdf, dfpurge)

# DataPublicationDOI
outdf, dfpurge = TestErrorFunctions.DataPublicationDOI_AA_Check(outdf, dfpurge)

# # ExemptOfVolumeFlowPriority
# outdf, dfpurge = TestErrorFunctions.ExemptOfVolumeFlowPriority_AA_Check(outdf, dfpurge)

# GeneratedPowerCapacityMW
outdf, dfpurge = TestErrorFunctions.GeneratedPowerCapacityMW_AA_Check(outdf, dfpurge)

# IrrigatedAcreage
outdf, dfpurge = TestErrorFunctions.IrrigatedAcreage_AA_Check(outdf, dfpurge)

# IrrigationMethodCV
outdf, dfpurge = TestErrorFunctions.IrrigationMethodCV_AA_Check(outdf, dfpurge)

# LegacyAllocationIDs
outdf, dfpurge = TestErrorFunctions.LegacyAllocationIDs_AA_Check(outdf, dfpurge)

# OwnerClassificationCV
outdf, dfpurge = TestErrorFunctions.OwnerClassificationCV_AA_Check(outdf, dfpurge)

# PopulationServed
outdf, dfpurge = TestErrorFunctions.PopulationServed_AA_Check(outdf, dfpurge)

# PowerType
outdf, dfpurge = TestErrorFunctions.PowerType_AA_Check(outdf, dfpurge)

# PrimaryUseCategory
outdf, dfpurge = TestErrorFunctions.PrimaryUseCategory_AA_Check(outdf, dfpurge)

# WaterAllocationNativeURL
outdf, dfpurge = TestErrorFunctions.WaterAllocationNativeURL_AA_Check(outdf, dfpurge)


# Export to new csv
############################################################################
print("Exporting outdf and dfpurge dataframes...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/waterallocations.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_excel('ProcessedInputData/waterallocations_missing.xlsx', index=False)

print("Done.")
