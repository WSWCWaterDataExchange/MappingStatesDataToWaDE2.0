#Date Created: 12/23/2020
#Author: Ryan James
#Purpose: To extract NM allocation use information and population dataframe WaDEQA 2.0.
#         1) Simple creation of working dataframe (df), with output dataframe (outdf).
#         2) Some data structure problems solved with pre-processes code.

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
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/NewMexico/WaterAllocation"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_NewMexicoMaster.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_M = pd.read_csv(M_fileInput)  # The State's Master input dataframe.

df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_watersources['WaterSourceNativeID'] = df_watersources['WaterSourceNativeID'].astype(int)
df_watersources['WaterSourceNativeID'] = df_watersources['WaterSourceNativeID'].astype(str)

df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe
df_sites['SiteNativeID'] = df_sites['SiteNativeID'].astype(int)
df_sites['SiteNativeID'] = df_sites['SiteNativeID'].astype(str)

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


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_M.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
outdf.MethodUUID = "NMOSE_Water Allocation"

print("OrganizationUUID")
outdf.OrganizationUUID = "NMOSE"

# ###########################################################################################
print("SiteUUID")

df_M['Latitude'] = df_M['Latitude']
df_M['Longitude'] = df_M['Longitude']
df_M['SiteName'] = df_M['SiteName']
df_M['SiteTypeCV'] = df_M['SiteTypeCV']

def assignSiteNativeID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        intvalue = int(colrowValue)
        strvalue = str(intvalue)
        outList = strvalue.strip()
    return outList
df_M['SiteNativeID'] = df_M.apply(lambda row: assignSiteNativeID(row['pod_nbr']), axis=1)


def retrieveSiteUUID(colrowValueA, colrowValueB, colrowValueC, colrowValueD, colrowValueE):
    ml = df_sites.loc[((df_sites['Latitude'] == colrowValueA) &
                                 (df_sites['Longitude'] == colrowValueB) &
                                 (df_sites['SiteName'] == colrowValueC) &
                                 (df_sites['SiteTypeCV'] == colrowValueD) &
                                 (df_sites['SiteNativeID'] == colrowValueE)), 'SiteUUID']
    if not(ml.empty):  # check if the series is empty
        outList = ml.iloc[0]
    else:
        outList = ''
    return outList


outdf['SiteUUID'] = df_M.apply(lambda row: retrieveSiteUUID(row['Latitude'], row['Longitude'], row['SiteName'], row['SiteTypeCV'], row['SiteNativeID']), axis=1)
###########################################################################################

print("VariableSpecificUUID")
outdf.VariableSpecificUUID = "NMOSE_Allocation All"

###########################################################################################
print("WaterSourceUUID")
# Need to recreate WaterSourceNativeID and WaterSourceTypeCV to correctly match up to WaterSourceUUID

# For creating WaterSourceNativeID
def assignWaterSourceNativeID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unspecified'
    else:
        strvalue = str(colrowValue)
        outList = strvalue.strip()
    return outList

# For creating WaterSourceTypeCV
def assignWaterSourceTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unspecified'
    else:
        strvalue = str(colrowValue)
        outList = strvalue.strip()
    return outList

df_M['WaterSourceName'] = df_M['WaterSourceName']
df_M['WaterSourceNativeID'] = df_M.apply(lambda row: assignWaterSourceNativeID(row['surface_co']), axis=1)
df_M['WaterSourceTypeCV'] = df_M.apply(lambda row: assignWaterSourceTypeCV(row['WaterSourceTypeCV']), axis=1)

def retrieveWaterSourceUUID(colrowValueA, colrowValueB, colrowValueC, df_watersources):
    ml = df_watersources.loc[((df_watersources['WaterSourceName'] == colrowValueA) &
                                 (df_watersources['WaterSourceNativeID'] == colrowValueB) &
                                 (df_watersources['WaterSourceTypeCV'] == colrowValueC)), 'WaterSourceUUID']
    if not(ml.empty):  # check if the series is empty
        outList = ml.iloc[0]
    else:
        outList = ''
    return outList

outdf['WaterSourceUUID'] = df_M.apply(lambda row: retrieveWaterSourceUUID(row['WaterSourceName'], row['WaterSourceNativeID'], row['WaterSourceTypeCV'], df_watersources), axis=1)

###########################################################################################

print("AllocationApplicationDate")
outdf.AllocationApplicationDate = ""
print("AllocationAssociatedConsumptiveUseSiteIDs")
outdf.AllocationAssociatedConsumptiveUseSiteIDs = ""

print("AllocationAssociatedWithdrawalSiteIDs")
outdf.AllocationAssociatedWithdrawalSiteIDs = ""

print("AllocationBasisCV")
outdf.AllocationBasisCV = "Unknown"

print("AllocationChangeApplicationIndicator")
outdf.AllocationChangeApplicationIndicator = ""

print("AllocationCommunityWaterSupplySystem")
outdf.AllocationCommunityWaterSupplySystem = ""

print("AllocationCropDutyAmount")
outdf.AllocationCropDutyAmount = ""

print("AllocationExpirationDate")
outdf.AllocationExpirationDate = ""

print("AllocationFlow_CFS")
outdf['AllocationFlow_CFS'] = ""

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_M['AllocationLegalStatusCV']

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_M['nbr'].astype(str) # Native dbtype is float. Need to return this value as a string

print("AllocationOwner")
outdf['AllocationOwner'] = df_M['AllocationOwner']

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_M['AllocationPriorityDate']

print("AllocationSDWISIdentifierCV")
outdf.AllocationSDWISIdentifierCV = ""

print("AllocationTimeframeEnd")
outdf.AllocationTimeframeEnd = "12/31"

print("AllocationTimeframeStart")
outdf.AllocationTimeframeStart = "01/01"

print("AllocationTypeCV") 
outdf.AllocationTypeCV = ""

print("AllocationVolume_AF")
outdf['AllocationVolume_AF'] = df_M['restrict']

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_M['BeneficialUseCategory']

print("CommunityWaterSupplySystem")
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")
outdf.CropTypeCV = ""

print("CustomerTypeCV")
outdf.CustomerTypeCV = ""

print("DataPublicationDate")
outdf.DataPublicationDate = "05/11/2020"

print("DataPublicationDOI")
outdf.DataPublicationDOI = ""

print("ExemptOfVolumeFlowPriority")
outdf['ExemptOfVolumeFlowPriority'] = "0"

print("GeneratedPowerCapacityMW")
outdf.GeneratedPowerCapacityMW = ""

print("IrrigatedAcreage")
outdf['IrrigatedAcreage'] = df_M['total_div']

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

# WaDE 2.0 does not allow for multiple items in the WaterSource column.  Only one entry.
# Temp Solutions: Going to remove those sites that have duplicates watersources ID


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


