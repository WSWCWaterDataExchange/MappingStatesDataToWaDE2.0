# Date Created: 06/23/2022
# Purpose: To extract WA wr allocation use information and population dataframe WaDEQA 2.0.
# Notes: N/A

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
workingDir = "G:/Shared drives/WaDE Data/Washington/WaterAllocation"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_WashingtonMaster.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_DM = pd.read_csv(M_fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

#WaDE dataframe columns
columnslist = [
    "AllocationUUID",
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
    "PrimaryBeneficialUseCategory",
    "WaterAllocationNativeURL"]


# Custom Functions
############################################################################

# For creating SiteUUID
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
benUseDict = {
    "508-14":"508-14",
    "AI":"Agricultural Irrigation",
    "CI":"Commercial & indust",
    "CM":"Commercial",
    "CO":"Cooling for indust proces",
    "DC":"Dust Control",
    "DG":"Domestic general",
    "DM":"Domestic multiple",
    "DS":"Domestic single",
    "DY":"Dairy",
    "EN":"Environmental quality",
    "FP":"Frost protection",
    "FR":"Fire protection",
    "FS":"Fish propagation",
    "GP":"Groundwater Preservation",
    "HE":"Heat Exchange",
    "HP":"Heat protection for crops",
    "HW":"Highway",
    "IFlow":"Instream Flow",
    "II":"Individual Irrigation",
    "IR":"Irrigation",
    "IT":"Municipal inter-tie system",
    "IU":"Irrigation Unknown",
    "MI":"Mining",
    "MT":"Mitigation",
    "MU":"Municipal",
    "NR":"No Purpose Identified",
    "OT":"Other",
    "PO":"Power",
    "PR":"Parks and Recreation",
    "RE":"Recreation - beautification",
    "RW":"Railway",
    "SA":"Stream augmentation",
    "SR":"Storage",
    "ST":"Stock water",
    "TS":"Test Well",
    "TW-P":"Trust water, Permanent",
    "TW-T":"Trust water, Temporary",
    "WL":"Wildlife refuge"}

def assignBenUseCategory(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        keyStr = colrowValue.strip()
        try:
            benUseListStr = keyStr.split()  # Need to split WA csv data
            outList = ", ".join(benUseDict[inx] for inx in benUseListStr)
        except:
            outList = ""
    return outList

# For creating AllocationAmount
def assignAllocationBasis(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ""
    else:
        outList = colrowValue
    return outList

# For creating LegalStatausCV
def assignallocLegalStatausCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        outList = colrowValue.strip()
    return outList

# For creating AllocationTypeCV
def assignAllocationTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ""
    else:
        outList = colrowValue.strip()
    return outList

# For creating AllocationUUID
def assignAllocationUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "WAwr_WR" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
outdf['MethodUUID'] = "WAwr_M1"

print("OrganizationUUID")
outdf['OrganizationUUID'] = "WAwr_O1"

print("SiteUUID")  # Using SiteNativeID
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['in_SiteNativeID']), axis=1)

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = "WAwr_V1"

print("AllocationApplicationDate")
outdf['AllocationApplicationDate'] = ""

print("AllocationAssociatedConsumptiveUseSiteIDs")
outdf['AllocationAssociatedConsumptiveUseSiteIDs'] = ""

print("AllocationAssociatedWithdrawalSiteIDs")
outdf['AllocationAssociatedWithdrawalSiteIDs'] = ""

print("AllocationBasisCV")
outdf['AllocationBasisCV'] = "Unspecified"

print("AllocationChangeApplicationIndicator")
outdf['AllocationChangeApplicationIndicator'] = ""

print("AllocationCommunityWaterSupplySystem")
outdf['AllocationCommunityWaterSupplySystem'] = ""

print("AllocationCropDutyAmount")
outdf['AllocationCropDutyAmount'] = ""

print("AllocationExpirationDate")
outdf['AllocationExpirationDate'] = ""

print("AllocationFlow_CFS")  # see preprocessing
outdf['AllocationFlow_CFS'] =  df_DM['in_AllocationFlow_CFS']

print("AllocationLegalStatusCV")  # see preprocessing
outdf['AllocationLegalStatusCV'] = df_DM['in_AllocationLegalStatusCV']

print("AllocationNativeID")  # see preprocessing
outdf['AllocationNativeID'] = df_DM['in_AllocationNativeID'].astype(str) # Native dbtype is float. Need to return this value as a string

print("AllocationOwner")  # see preprocessing
outdf['AllocationOwner'] = df_DM['in_AllocationOwner']

print("AllocationPriorityDate")  # see preprocessing
outdf['AllocationPriorityDate'] = df_DM['in_AllocationPriorityDate']

print("AllocationSDWISIdentifierCV")
outdf['AllocationSDWISIdentifierCV'] = ""

print("AllocationTimeframeEnd")
outdf['AllocationTimeframeEnd'] = "12/31"

print("AllocationTimeframeStart")
outdf['AllocationTimeframeStart'] = "01/01"

print("AllocationTypeCV")  # see preprocessing
outdf['AllocationTypeCV'] = df_DM.apply(lambda row: assignAllocationTypeCV(row['in_AllocationTypeCV']), axis=1)

print("AllocationVolume_AF")  # see preprocessing
outdf['AllocationVolume_AF'] = df_DM['in_AllocationVolume_AF']

print("BeneficialUseCategory")  # see preprocessing
outdf['BeneficialUseCategory'] = df_DM.apply(lambda row: assignBenUseCategory(row['in_BeneficialUseCategory']), axis=1)

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySystem'] = ""

print("CropTypeCV")
outdf['CropTypeCV'] = ""

print("CustomerTypeCV")
outdf['CustomerTypeCV'] = ""

print("DataPublicationDate")
outdf['DataPublicationDate'] = "03/30/2022"

print("DataPublicationDOI")
outdf['DataPublicationDOI'] = ""

print("ExemptOfVolumeFlowPriority")
outdf['ExemptOfVolumeFlowPriority'] = "0"

print("GeneratedPowerCapacityMW")
outdf['GeneratedPowerCapacityMW'] = ""

print("IrrigatedAcreage")  # see preprocessing
outdf['IrrigatedAcreage'] = df_DM['in_IrrigatedAcreage']

print("IrrigationMethodCV")
outdf['IrrigationMethodCV'] = ""

print("LegacyAllocationIDs")
outdf['LegacyAllocationIDs'] = ""

#####################################
print("OwnerClassificationCV")
# Temp solution to populate OwnerClassificationCV field.
# Use Custom import file
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/OwnerClassification")
import OwnerClassificationField
outdf['OwnerClassificationCV'] = outdf.apply(lambda row: OwnerClassificationField.CreateOwnerClassification(row['AllocationOwner']), axis=1)
#####################################

print("PopulationServed")
outdf['PopulationServed'] = ""

print("PowerType")
outdf['PowerType'] = ""

print("PrimaryBeneficialUseCategory")
outdf['PrimaryBeneficialUseCategory'] = "Unspecified"

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

# Temp solution to populate PrimaryBeneficialUseCategory field.
# Use Custom import file
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/AssignPrimaryUseCategory")
import AssignPrimaryUseCategory
outdf['PrimaryBeneficialUseCategory'] = outdf.apply(lambda row: AssignPrimaryUseCategory.retrievePrimaryUseCategory(row['BeneficialUseCategory']), axis=1)


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

# PrimaryBeneficialUseCategory
outdf, dfpurge = TestErrorFunctions.PrimaryBeneficialUseCategory_AA_Check(outdf, dfpurge)

# WaterAllocationNativeURL
outdf, dfpurge = TestErrorFunctions.WaterAllocationNativeURL_AA_Check(outdf, dfpurge)


############################################################################
print("Assign AllocationUUID") # has to be one of the last.
outdf = outdf.reset_index(drop=True)
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['AllocationUUID'] = dftemp.apply(lambda row: assignAllocationUUID(row['Count']), axis=1)

# Error check AllocationUUID
outdf, dfpurge = TestErrorFunctions.AllocationUUID_AA_Check(outdf, dfpurge)


# Export to new csv
############################################################################
print("Exporting outdf and dfpurge dataframes...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/waterallocations.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_excel('ProcessedInputData/waterallocations_missing.xlsx', index=False)

print("Done.")