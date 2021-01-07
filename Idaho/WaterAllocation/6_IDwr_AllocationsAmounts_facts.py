#Date Created: 10/22/2020
#Author: Ryan James
#Purpose: To extract ID allocation use information and population dataframe WaDEQA 2.0.
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
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Idaho/WaterAllocation"  # Specific to my machine, will need to change.
os.chdir(workingDir)
M_fileInput = "RawinputData/P_IdahoMaster.csv"
method_fileInput = "ProcessedInputData/methods.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_M = pd.read_csv(M_fileInput)  # The Idaho Master input dataframe.
df_method = pd.read_csv(method_fileInput)  # Method dataframe
df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

# WaDE dataframe columns
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


# Custom Site Functions
############################################################################
# For creating WaterSourceName
def assignWaterSourceName(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        outList = colrowValue
    return outList

# For creating WaterSourceUUID
def retrieveWaterSourceUUID(colrowValueA, colrowValueB, df_watersources):
    if (colrowValueA == '' and colrowValueB == '') or (pd.isnull(colrowValueA) and pd.isnull(colrowValueB)):
        outList = ''
    else:
        ml = df_watersources.loc[(df_watersources['WaterSourceName'] == colrowValueA) & (df_watersources['WaterSourceTypeCV'] == colrowValueB), 'WaterSourceUUID']
        if not(ml.empty):  # check if the series is empty
            outList = ml.iloc[0]
        else:
            outList = ''
    return outList

def retrieveSiteUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue  # remove whitespace chars
        try:
            outList = SitUUIDdict[String1]
        except:
            outList = colrowValue
    return outList

# For creating AllocationLegalStatusCV
def assignAllocationLegalStatusCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unknown"
    else:
        outList = colrowValue.strip()
    return outList

# For creating AllocationLegalStatusCV
def assignAllocationTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unknown"
    else:
        outList = colrowValue.strip()
    return outList

# For creating AllocationLegalStatusCV
def assignBeneficialUse(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unspecified"
    else:
        outList = colrowValue.strip()
    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe oudf...")
outdf = pd.DataFrame(index=df_M.index, columns=columnslist)  # The output dataframe

print("MethodUUID")  
outdf.MethodUUID = "IDWR_Diversion Tracking"

print("OrganizationUUID")  
outdf.OrganizationUUID = "IDWR"

print("SiteUUID")
SitUUIDdict = pd.Series(df_sites.SiteUUID.values, index = df_sites.SiteNativeID).to_dict()
outdf['SiteUUID'] = df_M.apply(lambda row: retrieveSiteUUID(row['PointOfDiversionID_POD']), axis=1)

print("VariableSpecificUUID")  
outdf.VariableSpecificUUID = "IDWR_Allocation All"

##############################################################
# Need to recreate WSName.
print("WaterSourceName")
df_M = df_M.assign(WaterSourceName = '')
df_M['WaterSourceName'] = df_M.apply(lambda row: assignWaterSourceName(row['Source_POD']), axis=1)

print("WaterSourceUUID")
outdf['WaterSourceUUID'] = df_M.apply(lambda row: retrieveWaterSourceUUID(row['WaterSourceName'], row['inputWaterSourceType'], df_watersources), axis=1)
##############################################################

print("AllocationApplicationDate")
outdf.AllocationApplicationDate = ""

print("AllocationAssociatedConsumptiveUseSiteIDs")  
outdf.AllocationAssociatedConsumptiveUseSiteIDs = ""

print("AllocationAssociatedWithdrawalSiteIDs")  
outdf.AllocationAssociatedWithdrawalSiteIDs = ""

print("AllocationBasisCV")
outdf.AllocationBasisCV = ""

print("AllocationChangeApplicationIndicator")  
outdf.AllocationChangeApplicationIndicator = ""

print("AllocationCommunityWaterSupplySystem")  
outdf['AllocationCommunityWaterSupplySystem'] = ''

print("AllocationCropDutyAmount")  
outdf['AllocationCropDutyAmount'] = ""

print("AllocationExpirationDate")  
outdf.AllocationExpirationDate = ""

print("AllocationFlow_CFS")
outdf['AllocationFlow_CFS'] = df_M['OverallMaxDiversionRate_POD']

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_M.apply(lambda row: assignAllocationLegalStatusCV(row['Basis_POD']), axis=1)

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
def assignNativeID(colrowValue):
    outList = str(colrowValue)
    outList = outList.strip()
    return outList
outdf['AllocationNativeID'] = df_M.apply(lambda row: assignNativeID(row['RightID_POD']), axis=1)

print("AllocationOwner")
outdf['AllocationOwner'] = df_M['Owner_Update']

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_M['PriorityDate_POD']

print("AllocationTimeframeEnd") 
outdf.AllocationTimeframeEnd = ""

print("AllocationTimeframeStart") 
outdf.AllocationTimeframeStart = ""

print("AllocationTypeCV")  
outdf['AllocationTypeCV'] = df_M.apply(lambda row: assignAllocationTypeCV(row['Status_POD']), axis=1)

print("AllocationVolume_AF")
outdf['AllocationVolume_AF'] = ""

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_M.apply(lambda row: assignBeneficialUse(row['WaterUse_PoU']), axis=1)

print("CommunityWaterSupplySystem")  
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")  
outdf.CropTypeCV = ""

print("CustomerTypeCV")  
outdf.CustomerTypeCV = ""

print("DataPublicationDate")  
outdf.DataPublicationDate = "10/21/2020"

print("DataPublicationDOI")  
outdf.DataPublicationDOI = ""

print("ExemptOfVolumeFlowPriority")
outdf['ExemptOfVolumeFlowPriority'] = "0"

print("GeneratedPowerCapacityMW")  
outdf.GeneratedPowerCapacityMW = ""

print("IrrigatedAcreage") 
outdf.IrrigatedAcreage = ""

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

print("AllocationSDWISIdentifierCV")  
outdf.AllocationSDWISIdentifierCV = ""

print("WaterAllocationNativeURL")
outdf["WaterAllocationNativeURL"] = df_M['WRDocs_POD']

print("Resetting Index")
outdf.reset_index()

print("Joining outdf duplicates based on AllocationNativeID...")
outdf = outdf.replace(np.nan, '')  # Replaces NaN values with blank.
outdf100 = pd.DataFrame(columns=columnslist)  # The output dataframe for CSV.
outdf100 = outdf.groupby('AllocationNativeID').agg(lambda x: ','.join([str(elem) for elem in (list(set(x)))])).replace(np.nan, '').reset_index()

# Solving WaDE 2.0 Upload Issues
############################################################################
# Date Noted: 02/27/2020
# Note: Insure 'WaterSourceUUID' only has 1 entry. Error due to above merge / we don't allow multiple WSUUIDs.
print("temp fix WaterSourceUUID")
outdf100.to_csv('ProcessedInputData/oldWSUUID_waterallocations.csv', index=False)
def tempfixWSUUID(colrowValueA):
    #pass in text, split on 'sep', return first
    sep = ','
    result = colrowValueA.split(sep, 1)[0]
    return result
outdf100['WaterSourceUUID']  = outdf100.apply(lambda row: tempfixWSUUID(row['WaterSourceUUID']), axis=1)


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")
# Purge DataFrame to hold removed elements
dfpurge = pd.DataFrame(columns=columnslist)
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
    dfpurge.to_csv('ProcessedInputData/waterallocations_missing.csv', index=False)

print("Done.")