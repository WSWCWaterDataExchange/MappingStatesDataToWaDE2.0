#Date Updated: 08/08/2022
#Author(s): Joseph Brewer, Ryan James
#Purpose: To extract NV allocation use information and populate dataframe WaDEQA 2.0.
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
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "G:/Shared drives/WaDE Data/Nevada/WaterAllocation"
os.chdir(workingDir)
NVM_fileInput = "RawInputData/P_MastersNV.csv"  # Change this to fit state
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_NVM = pd.read_csv(NVM_fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

#WaDE dataframe columns
columnslist = [
    "WaDEUUID",
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


# Custom Site Functions
############################################################################

# For retrieving SiteUUID
SitUUIDdict = pd.Series(df_sites.SiteUUID.values, index = df_sites.SiteNativeID).to_dict()
def retrieveSiteUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()
        try:
            outList = SitUUIDdict[String1]
        except:
            outList = ''
    return outList

# For creating AllocationLegalStatusCV
LegalDict = {
"ABN" : "Abandoned",
"ABR" : "Abrogated",
"APP" : "Application",
"CAN" : "Canceled",
"CER" : "Certificate",
"CUR" : "Curtailed",
"DEC" : "Decreed",
"DEN": "Denied",
"EXP": "Expired",
"FOR": "Forfeited",
"PER": "Permit",
"REJ": "Rejected",
"REL": "Relinquished",
"RES": "Reserved",
"RFA": "Ready For Action",
"RFP": "Ready for Action (Protested)",
"RLP": "Relinquish a Portion",
"RSC": "Rescinded",
"RVK": "Revoked",
"RVP": "Revocable Permit",
"SUP": "Supersceded",
"SUS": "Suspended",
"VST": "Vested Rights",
"WDR": "Withdrawn"}
def assignAllocationLegalStatusCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue) == True :
        outList = "Unspecified"
    else:
        String1 = colrowValue.strip()
        try:
            outList = LegalDict[String1]
        except:
            outList = "Unspecified"
    return outList

# For creating AllocationOwner
def assignAllocationOwner(colrowValue):
    if colrowValue == '' or (pd.isnull(colrowValue)==True):
        outList = ""
    else:
        outList = colrowValue.strip()
    return outList

# For creating BeneficialUse
BeneficialUseDict = {
"COM" : "Commercial",
"CON" : "Construction",
"DEC" : "As Decreed",
"DOM" : "Domestic",
"DWR" : "Dewatering",
"ENV" : "Environmental",
"EVP" : "Evaporation",
"IND": "Industrial",
"IRC": "Irrigation-Carey Act",
"IRD": "Irrigation-DLE",
"IRR": "Irrigation",
"MM": "Mining and Milling",
"MMD": "Mining Milling and Dewatering",
"MUN": "Municipal",
"OTH": "Other",
"PWR": "Power",
"QM": "Quasi-Municipal",
"REC": "Recreational",
"STK": "Stockwatering",
"STO": "Storage",
"UKN": "Unknown",
"WLD": "Wildlife"}
def assignBeneficialUse(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unspecified'
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = BeneficialUseDict[String1]
        except:
            outList = "Unspecified"

    return outList

# For creating AllocationUUID
def assignAllocationUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "NVwr_WR" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe oudf...")

outdf = pd.DataFrame(index=df_NVM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
outdf['MethodUUID'] = "NVwr_M1"

print("OrganizationUUID")
outdf['OrganizationUUID'] = "NVwr_O1"

print("SiteUUID")
outdf['SiteUUID'] = df_NVM.apply(lambda row: retrieveSiteUUID(row['in_SiteNativeID']), axis=1)

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = "NVwr_V1"

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
outdf['AllocationCommunityWaterSupplySystem']= ''

print("AllocationCropDutyAmount")
outdf['AllocationCropDutyAmount'] = ""

print("AllocationExpirationDate")
outdf['AllocationExpirationDate'] = ""

print("AllocationFlow_CFS")
outdf['AllocationFlow_CFS'] = ""

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_NVM.apply(lambda row: assignAllocationLegalStatusCV(row['app_status']), axis=1)

print("AllocationNativeID")
outdf['AllocationNativeID'] = df_NVM['app']

print("AllocationOwner")
outdf['AllocationOwner'] = df_NVM.apply(lambda row: assignAllocationOwner(row['owner_name']), axis=1)

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_NVM['prior_dt']

print("AllocationTimeframeEnd")
outdf['AllocationTimeframeEnd'] = "12/31"

print("AllocationTimeframeStart")
outdf['AllocationTimeframeStart'] = "01/01"

print("AllocationTypeCV")
outdf['AllocationTypeCV'] = "Unspecified"

print("AllocationVolume_AF")
outdf['AllocationVolume_AF'] = df_NVM['duty_balance']

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_NVM.apply(lambda row: assignBeneficialUse(row['mou']), axis=1)

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySystem'] = ""

print("CropTypeCV")
outdf['CropTypeCV'] = ""

print("CustomerTypeCV")
outdf['CustomerTypeCV'] = ""

print("DataPublicationDate")
outdf['DataPublicationDate'] = "01/31/2022"

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

print("AllocationSDWISIdentifierCV")
outdf['AllocationSDWISIdentifierCV'] = ""

print("WaterAllocationNativeURL")
outdf["WaterAllocationNativeURL"] = df_NVM['permit_info']

print("Adding Data Assessment UUID")
outdf['WaDEUUID'] = df_NVM['WaDEUUID']

print("Resetting Index")
outdf.reset_index()

print("Joining outdf duplicates based on key fields...")
outdf = outdf.replace(np.nan, "")  # Replaces NaN values with blank.
groupbyList = ['AllocationNativeID', 'AllocationFlow_CFS', 'AllocationVolume_AF']
outdf = outdf.groupby(groupbyList).agg(lambda x: ','.join([str(elem) for elem in (list(set(x))) if elem!=''])).replace(np.nan, "").reset_index()
outdf = outdf[columnslist]  # reorder the dataframe's columns based on columnslist


# Solving WaDE 2.0 Upload Issues
############################################################################

# Note: OwnerClassificationCV can only accept 1 entry at this time. Error due to above merge / we don't allow multiple OwnerClassificationCV.
def tempfixOCSV(val):
    valList = val.split(",") # convert string to list
    valList.sort() # sort list alphabetically
    if ("In Review" in valList):
        valList.remove("In Review") # check if "In Review"  If true, remove.
        valList.append("In Review") # Append back in "In Review" to end of list.
    result = valList[0] # return only first value in list.
    return result
outdf['OwnerClassificationCV']  = outdf.apply(lambda row: tempfixOCSV(row['OwnerClassificationCV']), axis=1)

# Temp solution to populate PrimaryBeneficialUseCategory field.
# Use Custom import file
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/AssignPrimaryUseCategory")
import AssignPrimaryUseCategory
outdf['PrimaryBeneficialUseCategory'] = outdf.apply(lambda row: AssignPrimaryUseCategory.retrievePrimaryUseCategory(row['BeneficialUseCategory']), axis=1)


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")
purgecolumnslist = ["ReasonRemoved", "WaDEUUID", "RowIndex", "IncompleteField_1", "IncompleteField_2"]
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

# AllocationFlow_CFS_float_Yes & AllocationVolume_AF_float_Yes
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


# Remove WaDEUUID field from import file (only needed for purge info).
############################################################################
print("Drop Assessment WaDEUUID")
outdf = outdf.drop(['WaDEUUID'], axis=1)


# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/waterallocations.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_excel('ProcessedInputData/waterallocations_missing.xlsx', index=False)

print("Done.")
