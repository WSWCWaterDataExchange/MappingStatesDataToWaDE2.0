#Date Created: 04/08/2020
#Author: Ryan James
#Purpose: To extract ND allocation use information and population dataframe WaDEQA 2.0.
#         1) Simple creation of working dataframe (df), with output dataframe (outdf).
#         2) Drop all nulls before combining duplicate rows on NativeID.


# Needed Libraries
############################################################################
import numpy as np
import pandas as pd
import os


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/NorthDakota/WaterAllocation"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_NorthDakotaMaster.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_DM = pd.read_csv(M_fileInput)  # The State's Master input dataframe.
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

#For creating SiteUUID
def retrieveSiteUUID(colrowValue, df_sites):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        sitl = df_sites.loc[df_sites['SiteNativeID'] == colrowValue, 'SiteUUID']
        if not(sitl.empty):  # check if the series is empty
            outList = ', '.join(str(inx) for inx in sitl)
        else:
            outList = ''
    return outList

# For creating WaterSourceUUID -----------------------------------------------------------
def assignWaterSourceName(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unknown'
    else:
        outList = colrowValue.strip()
    return outList

def assignWaterSourceTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unknown'
    else:
        outList = colrowValue.strip()
    return outList

def retrieveWaterSourceUUID(colrowValue11, colrowValue22, df_watersources):
    colrowValue1 = str(colrowValue11).strip()
    colrowValue2 = str(colrowValue22).strip()
    if ((colrowValue1 == '') | (pd.isnull(colrowValue1))):
        colrowValue1 = 'Unspecified'
    if ((colrowValue2 == '') | (pd.isnull(colrowValue2))):
        colrowValue2 = 'Unknown'

    ml = df_watersources.loc[(df_watersources['WaterSourceName'] == colrowValue1) &
                             (df_watersources['WaterSourceTypeCV'] == colrowValue2), 'WaterSourceUUID']
    if not (ml.empty):  # check if the series is empty
        outList = ml.iloc[0]
    else:
        outList = ''

    return outList
#-----------------------------------------------------------


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
outdf.MethodUUID = "NDSWC_Water Rights"

print("OrganizationUUID")
outdf.OrganizationUUID = "NDSWC"

print("SiteUUID")  # Using SiteNativeID to correctly identify SiteUUIDID
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['pod'], df_sites), axis=1)

print("VariableSpecificUUID")
outdf.VariableSpecificUUID = "NDSWC_Allocation All"

###########################################################################################
print("WaterSourceUUID")
# Need to recreate WaterSourceName and WaterSourceTypeCV to correctly match up to WaterSourceUUID
df_DM['WaterSourceName'] = df_DM.apply(lambda row: assignWaterSourceName(row['source_nam']), axis=1)
df_DM['WaterSourceTypeCV'] = df_DM.apply(lambda row: assignWaterSourceTypeCV(row['source']), axis=1)

outdf['WaterSourceUUID'] = df_DM.apply(lambda row: retrieveWaterSourceUUID(row['WaterSourceName'], row['WaterSourceTypeCV'], df_watersources), axis=1)
###########################################################################################

print("AllocationApplicationDate")
outdf['AllocationApplicationDate'] = df_DM['date_issue']

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
outdf['AllocationExpirationDate'] = df_DM['date_cance']

print("AllocationFlow_CFS")
outdf['AllocationFlow_CFS'] = df_DM['req_rate']

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_DM['status']

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_DM['permit_num'].astype(str) # Native dbtype is float. Need to return this value as a string

print("AllocationOwner")
outdf['AllocationOwner'] = df_DM['permit_hol']

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_DM['priority_d']

print("AllocationSDWISIdentifierCV")
outdf.AllocationSDWISIdentifierCV = ""

print("AllocationTimeframeEnd")
outdf['AllocationTimeframeEnd'] = df_DM['period_end']

print("AllocationTimeframeStart")
outdf['AllocationTimeframeStart'] = df_DM['period_sta']

print("AllocationTypeCV")  # temp fix
outdf.AllocationTypeCV = 'Unspecified'

print("AllocationVolume_AF")
outdf['AllocationVolume_AF'] = df_DM['req_acft']

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_DM['use_type']

print("CommunityWaterSupplySystem")
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")
outdf.CropTypeCV = ""

print("CustomerTypeCV")
outdf.CustomerTypeCV = ""

print("DataPublicationDate")
outdf.DataPublicationDate = "04/08/2020"

print("DataPublicationDOI")
outdf.DataPublicationDOI = ""

print("ExemptOfVolumeFlowPriority")
outdf['ExemptOfVolumeFlowPriority'] = 0

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

# None at the moment


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")
dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# MethodUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["MethodUUID"].isnull()) | (outdf100["MethodUUID"] == '') | (outdf100['MethodUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad MethodUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["MethodUUID"].isnull()) | (outdf100["MethodUUID"] == '') | (outdf100['MethodUUID'].str.len() > 200) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# VariableSpecificUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["VariableSpecificUUID"].isnull()) | (outdf100["VariableSpecificUUID"] == '') | (outdf100['VariableSpecificUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad VariableSpecificUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["VariableSpecificUUID"].isnull()) | (outdf100["VariableSpecificUUID"] == '') | (outdf100['VariableSpecificUUID'].str.len() > 200) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# WaterSourceUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["WaterSourceUUID"].isnull()) |
                     (outdf100["WaterSourceUUID"] == '') |
                     (outdf100['WaterSourceUUID'].str.len() > 200) |
                     (outdf100["WaterSourceUUID"].str.contains(',')) ].assign(ReasonRemoved='Bad WaterSourceUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["WaterSourceUUID"].isnull()) |
                              (outdf100["WaterSourceUUID"] == '') |
                              (outdf100['WaterSourceUUID'].str.len() > 200) |
                              (outdf100["WaterSourceUUID"].str.contains(',')) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# OrganizationUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["OrganizationUUID"].isnull()) | (outdf100["OrganizationUUID"] == '') | (outdf100['OrganizationUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad OrganizationUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["OrganizationUUID"].isnull()) | (outdf100["OrganizationUUID"] == '') | (outdf100['OrganizationUUID'].str.len() > 200) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# SiteUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["SiteUUID"].isnull()) | (outdf100["SiteUUID"] == '') | (outdf100['SiteUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad SiteUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["SiteUUID"].isnull()) | (outdf100["SiteUUID"] == '') | (outdf100['SiteUUID'].str.len() > 200) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationApplicationDate_date_Yes
mask = outdf100.loc[outdf100["AllocationApplicationDate"].str.contains(',') == True].assign(ReasonRemoved='Bad AllocationApplicationDate').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationApplicationDate"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationAssociatedConsumptiveUseSiteIDs_nvarchar(500)_Yes
mask = outdf100.loc[ outdf100["AllocationAssociatedConsumptiveUseSiteIDs"].str.len() > 500 ].assign(ReasonRemoved='Bad AllocationAssociatedConsumptiveUseSiteIDs').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationAssociatedConsumptiveUseSiteIDs"].str.len() > 500 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationAssociatedWithdrawalSiteIDs_nvarchar(500)_Yes
mask = outdf100.loc[ outdf100["AllocationAssociatedWithdrawalSiteIDs"].str.len() > 500 ].assign(ReasonRemoved='Bad AllocationAssociatedWithdrawalSiteIDs').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationAssociatedWithdrawalSiteIDs"].str.len() > 500 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationBasisCV_nvarchar(250)_Yes
mask = outdf100.loc[ outdf100["AllocationBasisCV"].str.len() > 250 ].assign(ReasonRemoved='Bad AllocationBasisCV').reset_index()
purge = outdf100[mask]
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationBasisCV"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationChangeApplicationIndicator_nvarchar(100)_Yes
mask= outdf100.loc[ outdf100["AllocationChangeApplicationIndicator"].str.len() > 100 ].assign(ReasonRemoved='Bad AllocationChangeApplicationIndicator').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationChangeApplicationIndicator"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationCommunityWaterSupplySystem_nvarchar(250)_Yes
mask= outdf100.loc[ outdf100["AllocationCommunityWaterSupplySystem"].str.len() > 250 ].assign(ReasonRemoved='Bad AllocationCommunityWaterSupplySystem').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationCommunityWaterSupplySystem"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationCropDutyAmount_float_Yes
mask = outdf100.loc[ outdf100["AllocationCropDutyAmount"].str.contains(',') == True ].assign(ReasonRemoved='Bad AllocationCropDutyAmount').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationCropDutyAmount"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationExpirationDate_string_Yes
mask = outdf100.loc[ outdf100["AllocationExpirationDate"].str.contains(',') == True ].assign(ReasonRemoved='Bad AllocationExpirationDate').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationExpirationDate"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationFlow_CFS_float_Yes & AllocationVolume_AF_float_Yes
# We have to have either a flow or a volume
mask = outdf100.loc[ (outdf100['ExemptOfVolumeFlowPriority'] == "0") &
                     ((outdf100["AllocationFlow_CFS"].isnull()) |
                      (outdf100["AllocationFlow_CFS"] == "") |
                      (outdf100['AllocationFlow_CFS'].str.contains(','))) &
                     ((outdf100["AllocationVolume_AF"].isnull()) |
                      (outdf100["AllocationVolume_AF"] == '') |
                      (outdf100['AllocationVolume_AF'].str.contains(','))) ].assign(ReasonRemoved='Bad Flow or Volume').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100['ExemptOfVolumeFlowPriority'] == "0") &
                              ((outdf100["AllocationFlow_CFS"].isnull()) |
                               (outdf100["AllocationFlow_CFS"] == "") |
                               (outdf100['AllocationFlow_CFS'].str.contains(','))) &
                              ((outdf100["AllocationVolume_AF"].isnull()) |
                               (outdf100["AllocationVolume_AF"] == '') |
                               (outdf100['AllocationVolume_AF'].str.contains(','))) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationLegalStatusCV_nvarchar(250)_Yes
mask = outdf100.loc[ outdf100["AllocationLegalStatusCV"].str.len() > 250 ].assign(ReasonRemoved='Bad AllocationLegalStatusCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationLegalStatusCV"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationNativeID_nvarchar(250)_Yes
mask = outdf100.loc[ outdf100["AllocationNativeID"].str.len() > 250 ].assign(ReasonRemoved='Bad AllocationNativeID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationNativeID"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationOwner_nvarchar(500)_Yes
mask = outdf100.loc[ outdf100["AllocationOwner"].str.len() > 500 ].assign(ReasonRemoved='Bad AllocationOwner').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationOwner"].str.len() > 500 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationPriorityDate_string_-
mask = outdf100.loc[ (outdf100['ExemptOfVolumeFlowPriority'] == "0") &
                     ((outdf100["AllocationPriorityDate"].isnull()) |
                      (outdf100["AllocationPriorityDate"] == '') |
                      (outdf100["AllocationPriorityDate"].str.contains(','))) ].assign(ReasonRemoved='Bad AllocationPriorityDate').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100['ExemptOfVolumeFlowPriority'] == "0") &
                              ((outdf100["AllocationPriorityDate"].isnull()) |
                               (outdf100["AllocationPriorityDate"] == '') |
                               (outdf100["AllocationPriorityDate"].str.contains(','))) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationTimeframeEnd_nvarchar(5)_Yes
mask = outdf100.loc[ outdf100["AllocationTimeframeEnd"].str.len() > 5 ].assign(ReasonRemoved='Bad AllocationTimeframeEnd').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationTimeframeEnd"].str.len() > 5 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationTimeframeStart_nvarchar(5)_Yes
mask = outdf100.loc[ outdf100["AllocationTimeframeStart"].str.len() > 5 ].assign(ReasonRemoved='Bad AllocationTimeframeStart').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationTimeframeStart"].str.len() > 5 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationTypeCV_nvarchar(250)_Yes
mask = outdf100.loc[ outdf100["AllocationTypeCV"].str.len() > 250 ].assign(ReasonRemoved='Bad AllocationTypeCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationTypeCV"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# BeneficialUseCategory_nvarchar(250)_-
mask = outdf100.loc[ (outdf100["BeneficialUseCategory"].isnull()) | (outdf100["BeneficialUseCategory"] == '') | (outdf100["BeneficialUseCategory"].str.len() > 250) ].assign(ReasonRemoved='Bad BeneficialUseCategory').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["BeneficialUseCategory"].isnull()) | (outdf100["BeneficialUseCategory"] == '') | (outdf100["BeneficialUseCategory"].str.len() > 250) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# CommunityWaterSupplySystem_nvarchar(250)_Yes
mask = outdf100.loc[ outdf100["CommunityWaterSupplySystem"].str.len() > 250 ].assign(ReasonRemoved='Bad CommunityWaterSupplySystem').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["CommunityWaterSupplySystem"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# CropTypeCV_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["CommunityWaterSupplySystem"].str.len() > 250 ].assign(ReasonRemoved='Bad CommunityWaterSupplySystem').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["CommunityWaterSupplySystem"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# CustomerTypeCV_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["CustomerTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Bad CustomerTypeCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["CustomerTypeCV"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# DataPublicationDate_string_-
mask = outdf100.loc[ (outdf100["DataPublicationDate"].isnull()) | (outdf100["DataPublicationDate"] == '') | (outdf100["DataPublicationDate"].str.contains(',') == True) ].assign(ReasonRemoved='Bad DataPublicationDate').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["DataPublicationDate"].isnull()) | (outdf100["DataPublicationDate"] == '') | (outdf100["DataPublicationDate"].str.contains(',') == True)  ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# DataPublicationDOI_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["DataPublicationDOI"].str.len() > 100 ].assign(ReasonRemoved='Bad DataPublicationDOI').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["DataPublicationDOI"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# ExemptOfVolumeFlowPriority_bit_Yes
# mask = outdf100.loc[ (outdf100["ExemptOfVolumeFlowPriority"] > 1) ].assign(ReasonRemoved='Bad ExemptOfVolumeFlowPriority').reset_index()
# if len(mask.index) > 0:
#     dfpurge = dfpurge.append(mask)
#     dropIndex = outdf100.loc[ (outdf100["ExemptOfVolumeFlowPriority"] > 1) ].index
#     outdf100 = outdf100.drop(dropIndex)
#     outdf100 = outdf100.reset_index(drop=True)

# GeneratedPowerCapacityMW_float_Yes
mask = outdf100.loc[ outdf100["GeneratedPowerCapacityMW"].str.contains(',') == True ].assign(ReasonRemoved='Bad GeneratedPowerCapacityMW').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["GeneratedPowerCapacityMW"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# IrrigatedAcreage_float_Yes
mask = outdf100.loc[ outdf100["IrrigatedAcreage"].str.contains(',') == True ].assign(ReasonRemoved='Bad IrrigatedAcreage').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["IrrigatedAcreage"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# IrrigationMethodCV_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["IrrigationMethodCV"].str.len() > 100 ].assign(ReasonRemoved='Bad IrrigationMethodCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["IrrigationMethodCV"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# LegacyAllocationIDs_nvarchar(250)_Yes
mask = outdf100.loc[ outdf100["LegacyAllocationIDs"].str.len() > 250 ].assign(ReasonRemoved='Bad LegacyAllocationIDs').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["LegacyAllocationIDs"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# PopulationServed_bigint_Yes
mask = outdf100.loc[ outdf100["PopulationServed"].str.contains(',') == True ].assign(ReasonRemoved='Bad PopulationServed').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["PopulationServed"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# PowerType_nvarchar(50)_Yes
mask = outdf100.loc[ outdf100["PowerType"].str.len() > 50 ].assign(ReasonRemoved='Bad PowerType').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["PowerType"].str.len() > 50 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# PrimaryUseCategory_Nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["PrimaryUseCategory"].str.len() > 100 ].assign(ReasonRemoved='Bad PrimaryUseCategory').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["PrimaryUseCategory"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationSDWISIdentifierCV_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["AllocationSDWISIdentifierCV"].str.len() > 100 ].assign(ReasonRemoved='Bad AllocationSDWISIdentifierCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationSDWISIdentifierCV"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# WaterAllocationNativeURL_nvarchar(250)_Yes
mask = outdf100.loc[ outdf100["WaterAllocationNativeURL"].str.len() > 250 ].assign(ReasonRemoved='Bad WaterAllocationNativeURL').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["WaterAllocationNativeURL"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)



# Export to new csv
############################################################################
print("Exporting dataframe outdf100 to csv...")
# The working output DataFrame for WaDE 2.0 input.
outdf100.to_csv('ProcessedInputData/waterallocations.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/waterallocations_missing.csv', index=False)


print("Done.")


