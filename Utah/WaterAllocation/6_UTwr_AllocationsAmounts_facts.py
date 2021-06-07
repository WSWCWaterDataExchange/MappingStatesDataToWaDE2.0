# Date Updated: 05/17/2021
# Author: Ryan James
# Purpose: To extract UT allocation use information and population dataframe WaDEQA 2.0.
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
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/CustomFunctions/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/WaterAllocation"  # Specific to my machine, will need to change.
os.chdir(workingDir)
DM_fileInput = "RawinputData/P_UtahMaster.csv"
method_fileInput = "ProcessedInputData/methods.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_DM = pd.read_csv(DM_fileInput)  # The State's Master input dataframe.
df_method = pd.read_csv(method_fileInput)  # Method dataframe
df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe
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

# For creating SiteUUID
SitUUIDdict = pd.Series(df_sites.SiteUUID.values, index = df_sites.SiteNativeID).to_dict()
def retrieveSiteUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = int(colrowValue)
        try:
            outList = SitUUIDdict[String1]
        except:
            outList = ''
    return outList

# For creating BeneficialUseCategory
benUseDict = {
    "I" : "Irrigation",
    "S" : "Stockwatering",
    "D" : "Domestic",
    "M" : "Municipal",
    "X" : "Mining",
    "P" : "Power",
    "O" : "Other"}
def assignBenUseCategory(colrowValue):
    if colrowValue == "" or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        outList = ",".join(benUseDict[inx] for inx in list(str(colrowValue)))
    return outList

# For creating AllocationOwner
def assignAllocationOwner(colrowValue):
    if colrowValue == "" or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        outList = colrowValue.strip()
    return outList

# For creating GeneratedPowerCapacityMW
def assignGeneratedPowerCapacityMW(colrowValue):
    if colrowValue == "" or pd.isnull(colrowValue):
        outList = ""
    else:
        val = float(colrowValue)/1000
        outList = float(val)
    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")

outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
outdf['MethodUUID'] = "UT_Water Allocation"

print("OrganizationUUID")
outdf['OrganizationUUID'] = "UTDWRi"

print("SiteUUID")
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['OBJECTID']), axis=1)

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = "UT_Allocation"

print("AllocationApplicationDate")
outdf['AllocationApplicationDate'] = df_DM['DATE_FILED']

print("AllocationAssociatedConsumptiveUseSiteIDs")
outdf['AllocationAssociatedConsumptiveUseSiteIDs'] = ""

print("AllocationAssociatedWithdrawalSiteIDs")
outdf['AllocationAssociatedWithdrawalSiteIDs'] = ""

print("AllocationBasisCV")
outdf['AllocationBasisCV'] = "Unspecified"

print("AllocationChangeApplicationIndicator")
outdf['AllocationChangeApplicationIndicator'] = ""

print("AllocationCommunityWaterSupplySystem")
outdf['AllocationCommunityWaterSupplySystem'] = df_DM['MUNICIPALITY']

print("AllocationCropDutyAmount")
outdf['AllocationCropDutyAmount'] = df_DM['IRRIGATION_DEPLETION']

print("AllocationExpirationDate")
outdf['AllocationExpirationDate'] = df_DM['DATE_TERMINATED']

print("AllocationFlow_CFS")
outdf['AllocationFlow_CFS'] = df_DM['CFS']

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_DM['in_LegalStatus']

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_DM['WRNUM']

print("AllocationOwner")
outdf['AllocationOwner'] = df_DM.apply(lambda row: assignAllocationOwner(row['OWNER']), axis=1)

print("AllocationSDWISIdentifierCV")
outdf['AllocationSDWISIdentifierCV'] = ""

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_DM['PRIORITY']

print("AllocationTimeframeEnd")
outdf['AllocationTimeframeEnd'] = df_DM['in_AllocationTimeframeEnd']

print("AllocationTimeframeStart")
outdf['AllocationTimeframeStart'] = df_DM['in_AllocationTimeframeStart']

print("AllocationTypeCV")
outdf['AllocationTypeCV'] = "Unspecified"

print("AllocationVolume_AF")
outdf['AllocationVolume_AF'] = df_DM['ACFT']

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_DM.apply(lambda row: assignBenUseCategory(row['USES']), axis=1)

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySystem'] = ""

print("CropTypeCV")
outdf['CropTypeCV'] = ""

print("CustomerTypeCV")
outdf['CustomerTypeCV'] = ""

print("DataPublicationDate")
outdf['DataPublicationDate'] = "05/19/2021"

print("DataPublicationDOI")
outdf['DataPublicationDOI'] = ""

print("ExemptOfVolumeFlowPriority")
outdf['ExemptOfVolumeFlowPriority'] = "0"

print("GeneratedPowerCapacityMW")
# outdf['GeneratedPowerCapacityMW'] = df_DM.apply(lambda row: assignGeneratedPowerCapacityMW(row['POWER_CAPACITY']), axis=1)
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

print("Joining outdf duplicates based on AllocationNativeID...")
outdf = outdf.replace(np.nan, "")  # Replaces NaN values with blank.
outdf100 = pd.DataFrame(columns=columnslist)  # The output dataframe for CSV.
outdf100 = outdf.groupby(['AllocationNativeID']).agg(lambda x: ",".join([str(elem) for elem in (list(set(x))) if elem!=""])).replace(np.nan, "").reset_index()


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# Date Noted: 05/25/2021
# Note: OwnerClassificationCV can only accept 1 entry at this time. Error due to above merge / we don't allow multiple OwnerClassificationCV.
def tempfixOCSV(colrowValueA):
    result = colrowValueA.split(",", 1)[0]  # pass in text, split on "," & return first value.
    return result
outdf100['OwnerClassificationCV']  = outdf100.apply(lambda row: tempfixOCSV(row['OwnerClassificationCV']), axis=1)


#Error checking each field
############################################################################
print("Error checking each field.  Purging bad inputs.")

# Purge DataFrame to hold removed elements
dfpurge = pd.DataFrame(columns=columnslist)
dfpurge = dfpurge.assign(ReasonRemoved="")

# MethodUUID
outdf100, dfpurge = TestErrorFunctions.MethodUUID_AA_Check(outdf100, dfpurge)

# OrganizationUUID
outdf100, dfpurge = TestErrorFunctions.OrganizationUUID_AA_Check(outdf100, dfpurge)

# SiteUUID
outdf100, dfpurge = TestErrorFunctions.SiteUUID_AA_Check(outdf100, dfpurge)

# VariableSpecificUUID
outdf100, dfpurge = TestErrorFunctions.VariableSpecificUUID_AA_Check(outdf100, dfpurge)

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

# OwnerClassificationCV
outdf100, dfpurge = TestErrorFunctions.OwnerClassificationCV_AA_Check(outdf100, dfpurge)

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
    dfpurge.to_csv('ProcessedInputData/waterallocations_missing.csv', index=False)

print("Done.")
