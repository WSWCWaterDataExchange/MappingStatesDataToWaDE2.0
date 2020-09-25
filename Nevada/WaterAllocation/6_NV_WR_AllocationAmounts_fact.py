#Date Created: 07/20/2020
#Author: Joseph Brewer
#Purpose: To extract NV allocation use information and population dataframe WaDEQA 2.0.
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
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Nevada/WaterAllocation"
os.chdir(workingDir)
NVM_fileInput = "RawInputData/P_MastersNV.csv"  #Change this to fit state
method_fileInput = "ProcessedInputData/methods.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"


df_NVM = pd.read_csv(NVM_fileInput)  # The Texas Master input dataframe.
df_method = pd.read_csv(method_fileInput)  # Method dataframe
df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe


#WaDE dataframe columnslist
columnslist = [
    "MethodUUID",
    "OrganizationUUID",
    "SiteUUID",
    "VariableSpecificUUID",
    "WaterSourceUUID",
    "AllocationAmount",
    "AllocationApplicationDate",
    "AllocationAssociatedConsumptiveUseSiteIDs",
    "AllocationAssociatedWithdrawalSiteIDs",
    "AllocationBasisCV",
    "AllocationChangeApplicationIndicator",
    "AllocationCommunityWaterSupplySystem",
    "AllocationCropDutyAmount",
    "AllocationExpirationDate",
    "AllocationLegalStatusCV",
    "AllocationMaximum",
    "AllocationNativeID",
    "AllocationOwner",
    "AllocationPriorityDate",
    "AllocationTimeframeEnd",
    "AllocationTimeframeStart",
    "AllocationTypeCV",
    "BeneficialUseCategory",
    "CommunityWaterSupplySystem",
    "CropTypeCV",
    "CustomerTypeCV",
    "DataPublicationDate",
    "DataPublicationDOI",
    "GeneratedPowerCapacityMW",
    "IrrigatedAcreage",
    "IrrigationMethodCV",
    "LegacyAllocationIDs",
    "PopulationServed",
    "PowerType",
    "PrimaryUseCategory",
    "AllocationSDWISIdentifierCV",
    "WaterAllocationNativeURL"]


# Custom Site Functions
############################################################################

# For retrieving WaterSourceUUID
def retrieveWaterSourceUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()
        try:
            outList = WSUUIDdict[String1]
        except:
            outList = colrowValue
    return outList

# For retrieving SiteUUID
def retrieveSiteUUID(colrowValueA, colrowValueB):
    ml = df_sites.loc[(df_sites['SiteName'] == colrowValueA) & (df_sites['SiteTypeCV'] == colrowValueB), 'SiteUUID']
    if not(ml.empty):  # check if the series is empty
        outList = ml.iloc[0]
    else:
        outList = ''
    return outList

# For creating AllocationAmount
def assignAllocationAmount(colrowValue):
    if colrowValue <= 0 or pd.isnull(colrowValue):
        outList = 0
    else:
        outList = colrowValue
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
        outList = ''
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = LegalDict[String1]
        except:
            outList = "Unknown"
    return outList

# For creating AllocationOwner
def assignAllocationOwner(colrowValue):
    if colrowValue == '' or (pd.isnull(colrowValue)==True):
        outList = ''
    else:
        outList = colrowValue.strip()  # remove whitespace chars
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
"MMD": "Mining, Milling, and Dewatering",
"MUN": "Municipal",
"OTH": "Other",
"PWR": "Power",
"QM": "Quasi-Municipal",
"REC": "Recreational",
"STK": "Stockwatering",
"STO": "Storage",
"UKN": "Unknown",
"WLD": "Wildlife"}
# For creating AllocationLegalStatusCV
def assignBeneficialUse(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = BeneficialUseDict[String1]
        except:
            outList = "Unknown"

    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe oudf...")
outdf = pd.DataFrame(index=df_NVM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")  # Hardcoded
outdf.MethodUUID = "NVDWR_Diversion Tracking"

print("OrganizationUUID")  # Hardcoded
outdf.OrganizationUUID = "NVDWR"

######################################
print("SiteUUID")

def assignSiteName(colrowValue):
    colrowValuestr = str(colrowValue)
    colrowValuestr = colrowValuestr.strip()
    if ((colrowValuestr == "") or pd.isnull(colrowValuestr) or colrowValuestr == 'nan'):
        outList = "Unknown"
    else:
        outList = colrowValuestr
    return outList

UnknownSTCVDict = {
    "EFF":"Effluent",
    "GEO":"Geothermal",
    "LAK":"lake",
    "OGW":"Other Ground Water",
    "OSW":"Other Surface Water",
    "RES":"Reservoir",
    "SPR":"Spring",
    "STO":"Storage",
    "STR":"stream",
    "UG":"Underground",
    "UKN":"Unknown"}
def assignSiteTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = UnknownSTCVDict[String1]
        except:
            outList = "Unknown"
    return outList

df_NVM['SiteName'] = df_NVM.apply(lambda row: assignSiteName(row['site_name']), axis=1)
df_NVM['SiteTypeCV'] = df_NVM.apply(lambda row: assignSiteTypeCV(row['source']), axis=1)

outdf['SiteUUID'] = df_NVM.apply(lambda row: retrieveSiteUUID(row['SiteName'], row['SiteTypeCV']), axis=1)
#######################################################

print("VariableSpecificUUID")  # Hardcoded
outdf.VariableSpecificUUID = "NVDWR_Allocation All"

#######################################################
print("WaterSourceUUID")

UnknownWSCVDict = {
"EFF" : "Reuse",
"GEO" : "Groundwater",
"LAK" : "Surface Water",
"OGW" : "Groundwater",
"OSW" : "Surface Water",
"RES" : "Reservoir",
"SPR" : "Surface Water",
"STO" : "Storage",
"STR" : "Surface Water",
"UG" : "Groundwater",
"UKN" : "Unknown"}
def assignWaterSourceTypeCV(colrowValue):
    if colrowValue == "" or pd.isnull(colrowValue):
        outList = ""
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = UnknownWSCVDict[String1]
        except:
            outList = "Unknown"
    return outList


df_NVM['WaterSourceTypeCV'] = df_NVM.apply(lambda row: assignWaterSourceTypeCV(row['source']), axis=1)
WSUUIDdict = pd.Series(df_watersources.WaterSourceUUID.values, index = df_watersources.WaterSourceTypeCV).to_dict()

outdf['WaterSourceUUID'] = df_NVM.apply(lambda row: retrieveWaterSourceUUID(row['WaterSourceTypeCV']), axis=1)
#######################################################

print("AllocationAmount")
outdf['AllocationAmount'] = df_NVM.apply(lambda row: assignAllocationAmount(row['duty_balance']), axis=1)

print("AllocationApplicationDate")  # Hardcoded
outdf.AllocationApplicationDate = ""

print("AllocationAssociatedConsumptiveUseSiteIDs")  # Hardcoded
outdf.AllocationAssociatedConsumptiveUseSiteIDs = ""

print("AllocationAssociatedWithdrawalSiteIDs")  # Hardcoded
outdf.AllocationAssociatedWithdrawalSiteIDs = ""

print("AllocationBasisCV")
outdf.AllocationBasisCV = ""

print("AllocationChangeApplicationIndicator")  # Hardcoded
outdf.AllocationChangeApplicationIndicator = ""

print("AllocationCommunityWaterSupplySystem")  # Hardcoded
outdf.AllocationCommunityWaterSupplySystem = ''

print("AllocationCropDutyAmount")  # Hardcoded
outdf.AllocationCropDutyAmount = ""

print("AllocationExpirationDate")  # Hardcoded
outdf.AllocationExpirationDate = ""

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_NVM.apply(lambda row: assignAllocationLegalStatusCV(row['app_status']), axis=1)

print("AllocationMaximum")  # Hardcoded
outdf.AllocationMaximum = ""

print("AllocationNativeID")
outdf['AllocationNativeID'] = df_NVM['app']

print("AllocationOwner")
outdf['AllocationOwner'] = df_NVM.apply(lambda row: assignAllocationOwner(row['owner_name']), axis=1)

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_NVM['prior_dt']

print("AllocationTimeframeEnd")
outdf.AllocationTimeframeEnd = "12/31"

print("AllocationTimeframeStart")
outdf.AllocationTimeframeStart = "01/01"

print("AllocationTypeCV")  # Hardcoded
outdf.AllocationTypeCV = ""

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_NVM.apply(lambda row: assignBeneficialUse(row['mou']), axis=1)

print("CommunityWaterSupplySystem")  # Hardcoded
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")  # Hardcoded
outdf.CropTypeCV = ""

print("CustomerTypeCV")  # Hardcoded
outdf.CustomerTypeCV = ""

print("DataPublicationDate")  # Hardcoded
outdf.DataPublicationDate = "08/03/2020"

print("DataPublicationDOI")  # Hardcoded
outdf.DataPublicationDOI = ""

print("GeneratedPowerCapacityMW")  # Hardcoded
outdf.GeneratedPowerCapacityMW = ""

print("IrrigatedAcreage") # Hardcoded
outdf.IrrigatedAcreage = ""

print("IrrigationMethodCV") # Hardcoded
outdf.IrrigationMethodCV = ""

print("LegacyAllocationIDs")  # Hardcoded
outdf.LegacyAllocationIDs = ""

print("PopulationServed")  # Hardcoded
outdf.PopulationServed = ""

print("PowerType")  # Hardcoded
outdf.PowerType = ""

print("PrimaryUseCategory")  # Hardcoded
outdf.PrimaryUseCategory = "Irrigation"

print("AllocationSDWISIdentifierCV")  # Hardcoded
outdf.AllocationSDWISIdentifierCV = ""

print("WaterAllocationNativeURL")  # Hardcoded
outdf["WaterAllocationNativeURL"] = df_NVM['permit_info']


# Solving WaDE 2.0 Upload Issues
############################################################################
# Date Noted: 02/28/2020
# Note: Insure single 'AllocationNativeID' entry.
print("Joining outdf duplicates based on AllocationNativeID...")
outdf100 = pd.DataFrame(columns=columnslist)  # The output dataframe for CSV.
outdf100 = outdf.groupby('AllocationNativeID', sort=False).agg(lambda x: ','.join([str(elem) for elem in (list(set(x)))])).reset_index()


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")  # Hardcoded
dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# MethodUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["MethodUUID"].isnull()) | (outdf100["MethodUUID"] == '') | (outdf100['MethodUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad MethodUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
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
mask = outdf100.loc[ (outdf100["WaterSourceUUID"].isnull()) | (outdf100["WaterSourceUUID"] == '') | (outdf100['WaterSourceUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad WaterSourceUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["WaterSourceUUID"].isnull()) | (outdf100["WaterSourceUUID"] == '') | (outdf100['WaterSourceUUID'].str.len() > 200) ].index
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

# AllocationAmount_float_Yes
mask = outdf100.loc[ (outdf100["AllocationAmount"].isnull()) | (outdf100["AllocationAmount"] == '')  ].assign(ReasonRemoved='Bad AllocationAmount').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["AllocationAmount"].isnull()) | (outdf100["AllocationAmount"] == '') ].index
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

# AllocationLegalStatusCV_nvarchar(250)_Yes
mask = outdf100.loc[ outdf100["AllocationLegalStatusCV"].str.len() > 250 ].assign(ReasonRemoved='Bad AllocationLegalStatusCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationLegalStatusCV"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# We are using allowcation amount for nv so we can ignore this check
# # AllocationMaximum_float_Yes
# mask = outdf100.loc[ (outdf100["AllocationMaximum"].isnull()) | (outdf100["AllocationMaximum"] == '') | (outdf100['AllocationMaximum'].str.contains(',') == True) ].assign(ReasonRemoved='Bad AllocationMaximum').reset_index()
# if len(mask.index) > 0:
#     dfpurge = dfpurge.append(mask)
#     dropIndex = outdf100.loc[ (outdf100["AllocationMaximum"].isnull()) | (outdf100["AllocationMaximum"] == '') | (outdf100['AllocationMaximum'].str.contains(',') == True) ].index
#     outdf100 = outdf100.drop(dropIndex)
#     outdf100 = outdf100.reset_index(drop=True)

# AllocationNativeID_nvarchar(250)_Yes
mask = outdf100.loc[ outdf100["AllocationNativeID"].str.len() > 250 ].assign(ReasonRemoved='Bad AllocationNativeID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationNativeID"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationOwner_nvarchar(250)_Yes
mask = outdf100.loc[ outdf100["AllocationOwner"].str.len() > 250 ].assign(ReasonRemoved='Bad AllocationOwner').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AllocationOwner"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationPriorityDate_string_-
mask = outdf100.loc[ (outdf100["AllocationPriorityDate"].isnull() == True) | (outdf100["AllocationPriorityDate"] == '') | (outdf100["AllocationPriorityDate"].str.contains(',') == True) ].assign(ReasonRemoved='Bad AllocationPriorityDate').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["AllocationPriorityDate"].isnull() == True) | (outdf100["AllocationPriorityDate"] == '') | (outdf100["AllocationPriorityDate"].str.contains(',') == True) ].index
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
    dfpurge.to_csv('ProcessedInputData/waterallocations_missing.csv')  # index=False,

print("Done.")