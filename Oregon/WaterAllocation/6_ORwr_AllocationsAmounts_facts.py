#Date Created: 12/23/2020
#Author: Ryan James
#Purpose: To extract OR allocation use information and population dataframe WaDEQA 2.0.
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
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Oregon/WaterAllocation"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_OregonMaster.csv"
#method_fileInput = "ProcessedInputData/methods.csv"
#variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_DM = pd.read_csv(M_fileInput)  # The State's Master input dataframe.
#df_method = pd.read_csv(method_fileInput)  # Method dataframe
#df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe
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

# For creating SiteUUID
def retrieveSiteUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        # String1 = str(colrowValue).strip()
        # outList = SitUUIDdict[String1]
        outList = SitUUIDdict[colrowValue]
    return outList

# For creating WaterSourceUUID -----------------------------------------------------------
def assignWaterSourceName(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unknown"
    else:
        outList = colrowValue.strip()
    return outList

WSTypeDict = {
    "ST": "storage",
    "GW": "groundwater",
    "SW": "surface water"
}
def assignWaterSourceTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unknown'
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = WSTypeDict[String1]
        except:
            outList = 'Unknown'
    return outList

def retrieveWaterSourceUUID(colrowValueA, colrowValueB):
    if (colrowValueA == '' and colrowValueB == '') or (pd.isnull(colrowValueA) and pd.isnull(colrowValueB)):
        outList = ''
    else:
        ml = df_watersources.loc[(df_watersources['WaterSourceName'] == colrowValueA) & (df_watersources['WaterSourceTypeCV'] == colrowValueB), 'WaterSourceUUID']
        if not(ml.empty):  # check if the series is empty
            outList = ml.iloc[0]
        else:
            outList = ''
    return outList
#-----------------------------------------------------------

# For creating AllocationTypeCV
AllowTypeDict = {
"GR": "groundwater registrations",
"PC": "power claim",
"SW": "surface water registrations",
"KL": "Klamath Adjudication claim",
"KA": "Klamath Adjudication"
}
def assignAllocationTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unspecified'
    else:
        String1 = colrowValue.strip()
        try:
            outList = AllowTypeDict[String1]
        except:
            outList = 'Unspecified'
    return outList

# For creating BeneficialUseCategory
def assignBenUseCategory(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unknown'
    else:
        outList = colrowValue.strip()
    return outList

# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
outdf['MethodUUID'] = "OWRD_Water Rights"

print("OrganizationUUID")
outdf['OrganizationUUID'] = "OWRD"

print("SiteUUID")  # Using SiteNativeID to correctly identify SiteUUIDID
SitUUIDdict = pd.Series(df_sites.SiteUUID.values, index = df_sites.SiteNativeID).to_dict()
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['pod_location_id']), axis=1)

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = "OWRD_Allocation All"

###########################################################################################
print("WaterSourceUUID")
# Need to recreate WSName and WSType to correctly match up to WaterSourceUUID

df_DM['WaterSourceName'] = df_DM.apply(lambda row: assignWaterSourceName(row['source']), axis=1)
df_DM['WaterSourceTypeCV'] = df_DM.apply(lambda row: assignWaterSourceTypeCV(row['wr_type']), axis=1)

outdf['WaterSourceUUID'] = df_DM.apply(lambda row: retrieveWaterSourceUUID(row['WaterSourceName'], row['WaterSourceTypeCV']), axis=1)
###########################################################################################

print("AllocationApplicationDate")
outdf['AllocationApplicationDate'] = ""

print("AllocationAssociatedConsumptiveUseSiteIDs")
outdf['AllocationAssociatedConsumptiveUseSiteIDs'] = ""

print("AllocationAssociatedWithdrawalSiteIDs")
outdf['AllocationAssociatedWithdrawalSiteIDs'] = ""

print("AllocationBasisCV")
outdf['AllocationBasisCV'] = "Unknown"

print("AllocationChangeApplicationIndicator")
outdf['AllocationChangeApplicationIndicator'] = ""

print("AllocationCommunityWaterSupplySystem")
outdf['AllocationCommunityWaterSupplySystem'] = ""

print("AllocationCropDutyAmount")
outdf['AllocationCropDutyAmount'] = ""

print("AllocationExpirationDate")
outdf['AllocationExpirationDate'] = ""

print("AllocationFlow_CFS")
outdf['AllocationFlow_CFS'] = df_DM['rate_cfs'].astype(float)

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = ""

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_DM['snp_id'].astype(str) # Native dbtype is float. Need to return this value as a string

print("AllocationOwner")  # Pre-process code
outdf['AllocationOwner'] = df_DM['Owner']

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_DM['priority_date']

print("AllocationSDWISIdentifierCV")
outdf['AllocationSDWISIdentifierCV'] = ""

print("AllocationTimeframeEnd")  # Pre-process code
outdf['AllocationTimeframeEnd'] = df_DM['AllocationTimeframeEnd']

print("AllocationTimeframeStart")  # Pre-process code
outdf['AllocationTimeframeStart'] = df_DM['AllocationTimeframeStart']

print("AllocationTypeCV")
outdf['AllocationTypeCV'] = df_DM.apply(lambda row: assignAllocationTypeCV(row['claim_char']), axis=1)

print("AllocationVolume_AF")
outdf['AllocationVolume_AF'] = df_DM['max_rate_acre_feet'].astype(float)

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_DM.apply(lambda row: assignBenUseCategory(row['use_code_description']), axis=1)

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySystem'] = ""

print("CropTypeCV")
outdf['CropTypeCV'] = ""

print("CustomerTypeCV")
outdf['CustomerTypeCV']= ""

print("DataPublicationDate")
outdf['DataPublicationDate'] = "04/03/2020"

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

print("PopulationServed")
outdf['PopulationServed'] = ""

print("PowerType")
outdf['PowerType'] = ""

print("PrimaryUseCategory")
outdf['PrimaryUseCategory'] = "Irrigation"

print("WaterAllocationNativeURL")
outdf['WaterAllocationNativeURL'] = df_DM['wris_link']

print("Resetting Index")
outdf.reset_index()

print("Joining outdf duplicates based on AllocationNativeID...")
outdf = outdf.replace(np.nan, "")  # Replaces NaN values with blank.
outdf100 = pd.DataFrame(columns=columnslist)  # The output dataframe for CSV.
outdf100 = outdf.groupby('AllocationNativeID').agg(lambda x: ",".join([str(elem) for elem in (list(set(x)))])).replace(np.nan, "").reset_index()


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# None at the moment


#Error Checking Each Field
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

