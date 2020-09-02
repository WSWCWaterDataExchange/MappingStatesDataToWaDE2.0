#Date Created: 07/30/2020
#Author: Ryan James
#Purpose: To extract UT site specific site amount use information and population dataframe WaDEQA 2.0.
#Notes:


# Needed Libraries
############################################################################
import numpy as np
import pandas as pd
import os
from pyproj import Transformer, transform

# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/SiteSpecificAmounts"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_MasterUTSiteSpecific.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_DM = pd.read_csv(M_fileInput)  # The State's Master input dataframe.
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

transformer = Transformer.from_crs(4269, 4326)
# NAD83 projection = epsg:4269.
# WGS84 projection used by WaDE 2.0 = epsg:4326.

#WaDE dataframe columns
columnslist = [
    "MethodUUID",
    "OrganizationUUID",
    "SiteUUID",
    "VariableSpecificUUID",
    "WaterSourceUUID",
    "Amount",
    "AssociatedNativeAllocationIDs",
    "CommunityWaterSupplySystem",
    "CropTypeCV",
    "CustomerTypeCV",
    "DataPublicationDateID",
    "DataPublicationDOI",
    "Geometry",
    "IrrigatedAcreage",
    "IrrigationMethodCV",
    "PopulationServed",
    "PowerGeneratedGWh",
    "PrimaryUseCategoryCV",
    "ReportYearCV",
    "SDWISIdentifierCV",
    "TimeframeEndID",
    "TimeframeStartID"]


# Custom Functions
############################################################################

#########################################################
# For creating SiteUUID
def assignLat(colrowValLat, colrowValLong):
    lat, long = transformer.transform(colrowValLat, colrowValLong)
    return lat

def assignLong(colrowValLat, colrowValLong):
    lat, long = transformer.transform(colrowValLat, colrowValLong)
    return long

def retrieveSiteUUID(colrowValA, colrowValB, colrowValC, colrowValD, colrowValE, df_sites):
    if (colrowValA=='' and colrowValB=='' and colrowValC=='' and colrowValD=='' and colrowValE=='') or \
            (pd.isnull(colrowValA) and pd.isnull(colrowValB) and pd.isnull(colrowValC) and pd.isnull(colrowValD) and pd.isnull(colrowValE)):
        outList = ''
    else:
        ml = df_sites.loc[df_sites['Latitude'] == colrowValA &
                          df_sites['Longitude'] == colrowValB &
                          df_sites['SiteName'] == colrowValC &
                          df_sites['SiteNativeID'] == colrowValD &
                          df_sites['SiteTypeCV'] == colrowValE, 'SiteUUID']
        if not (ml.empty):  # check if the series is empty
            outList = ml.iloc[0]
        else:
            outList = ''
    return outList
#########################################################

#########################################################
# For creating WaterSourceUUID
def assignWaterSourceName(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unspecified'
    else:
        strval = str(colrowValue)
        outList = strval.strip()
    return outList

def assignWaterSourceNativeID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unspecified'
    else:
        strval = str(colrowValue)
        outList = strval.strip()
    return outList

WSTypeDict = {
"Spring": "groundwater/spring",
"Well" :"groundwater/well",
"Stream" : "Surface Water",
"Reservoir" : "Surface Water",
"Drain" : "Surface Water",
"Well/Spring" : "Groundwater/Mixed",
"Tunnel" : "Groundwater",
"Well Field" : "groundwater/well",
"Lake" : "Surface Water"
}
def assignWaterSourceTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unknown"
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = WSTypeDict[String1]
        except:
            outList = "Unknown"
    return outList

def retrieveWaterSourceUUID(colrowValA, colrowValB, colrowValC, df_watersources):
    if (colrowValA=='' and colrowValB=='' and colrowValC=='') or \
            (pd.isnull(colrowValA) and pd.isnull(colrowValB) and pd.isnull(colrowValC)):
        outList = ''
    else:
        ml = df_watersources.loc[df_watersources['WaterSourceName'] == colrowValA &
                                 df_watersources['WaterSourceNativeID'] == colrowValB &
                                 df_watersources['WaterSourceTypeCV'] == colrowValC, 'WaterSourceUUID']
        if not (ml.empty):  # check if the series is empty
            outList = ml.iloc[0]
        else:
            outList = ''
    return outList
#########################################################

# For creating BeneficialUseCategory
def assignBenUseCategory(colrowVal):
    if colrowVal == '' or pd.isnull(colrowVal):
        outList = 'Unknown'
    else:
        outList = colrowVal.strip()
    return outList

# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")  # Hardcoded
outdf.MethodUUID = "UDWR_Water Use Data"

print("OrganizationUUID")  # Hardcoded
outdf.OrganizationUUID = "UDWR"


########################################################################
print("SiteUUID")  # Using Lat, long, SiteName, SiteNativeID & SiteTypeCV to correctly identify SiteUUIDID

df_DM['Latitude'] = df_DM.apply(lambda row: assignLat(row['Lat NAD83'], row['Lon NAD83']), axis=1)
df_DM['Longitude'] = df_DM.apply(lambda row: assignLong(row['Lat NAD83'], row['Lon NAD83']), axis=1)

outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['Latitude'],
                                                             row['Longitude'],
                                                             row['System Name_x'],
                                                             row['System ID_x'],
                                                             row['Source Type'], df_sites), axis=1)
########################################################################

print("VariableSpecificUUID")  # Hardcoded
outdf.VariableSpecificUUID = "UDWR_Site Specific"

########################################################################
print("WaterSourceUUID")  # Everything is considered fresh, groundwater

df_DM['WaterSourceName'] = df_DM.apply(lambda row: assignWaterSourceName(row['Source Name']), axis=1)
df_DM['WaterSourceNativeID'] = df_DM.apply(lambda row: assignWaterSourceNativeID(row['Source ID']), axis=1)
df_DM['WaterSourceTypeCV'] = df_DM.apply(lambda row: assignWaterSourceTypeCV(row['Source Type']), axis=1)

outdf['WaterSourceUUID'] = df_DM.apply(lambda row: retrieveWaterSourceUUID(row['WaterSourceName'],
                                                                           row['WaterSourceNativeID'],
                                                                           row['WaterSourceTypeCV'], df_watersources), axis=1)
########################################################################

print("Amount")
outdf['Amount'] = df_DM['PUMPRATE']

print("AllocationApplicationDate")  # Hardcoded
outdf.AllocationApplicationDate = ""

print("AllocationAssociatedConsumptiveUseSiteIDs")  # Hardcoded
outdf.AllocationAssociatedConsumptiveUseSiteIDs = ""

print("AllocationAssociatedWithdrawalSiteIDs")  # Hardcoded
outdf.AllocationAssociatedWithdrawalSiteIDs = ""

print("AllocationBasisCV")  # Hardcoded
outdf.AllocationBasisCV = "Unknown"

print("AllocationChangeApplicationIndicator")  # Hardcoded
outdf.AllocationChangeApplicationIndicator = ""

print("AllocationCommunityWaterSupplySystem")  # Hardcoded
outdf.AllocationCommunityWaterSupplySystem = ""

print("AllocationCropDutyAmount")  # Hardcoded
outdf.AllocationCropDutyAmount = ""

print("AllocationExpirationDate")  # Hardcoded
outdf.AllocationExpirationDate = ""

print("AllocationLegalStatusCV")
outdf.AllocationLegalStatusCV = ""

print("AllocationMaximum")  # Hardcoded
outdf['AllocationMaximum'] = df_DM['TESTEDRATE']

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_DM['REGISTRY_ID'].astype(str) # Native dbtype is float. Need to return this value as a string

print("AllocationOwner")  # Pre-process code
outdf['AllocationOwner'] = df_DM['OWNER_NAME']

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_DM['APPLICATION_DATE']

print("AllocationSDWISIdentifierCV")  # Hardcoded
outdf.AllocationSDWISIdentifierCV = ""

print("AllocationTimeframeEnd")  # Pre-process code
outdf.AllocationTimeframeEnd = "12/31"

print("AllocationTimeframeStart")  # Pre-process code
outdf.AllocationTimeframeStart = "01/01"

print("AllocationTypeCV")  # temp fix
outdf['AllocationTypeCV'] = df_DM.apply(lambda row: assignAllocationTypeCV(row['WELLTYPE']), axis=1)

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_DM.apply(lambda row: assignBenUseCategory(row['WATER_USE']), axis=1)

print("CommunityWaterSupplySystem")  # Hardcoded
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")  # Hardcoded
outdf.CropTypeCV = ""

print("CustomerTypeCV")  # Hardcoded
outdf.CustomerTypeCV = ""

print("DataPublicationDate")  # Hardcoded
outdf.DataPublicationDate = "04/06/2020"

print("DataPublicationDOI")  # Hardcoded
outdf.DataPublicationDOI = ""

print("GeneratedPowerCapacityMW")  # Hardcoded
outdf.GeneratedPowerCapacityMW = ""

print("IrrigatedAcreage")  # Hardcoded
outdf.IrrigatedAcreage = ""

print("IrrigationMethodCV")  # Hardcoded
outdf.IrrigationMethodCV = ""

print("LegacyAllocationIDs")  # Hardcoded
outdf.LegacyAllocationIDs = ""

print("PopulationServed")  # Hardcoded
outdf.PopulationServed = ""

print("PowerType")  # Hardcoded
outdf.PowerType = ""

print("PrimaryUseCategory")  # Hardcoded
outdf.PrimaryUseCategory = "Irrigation"

print("WaterAllocationNativeURL")  # Hardcoded
outdf.WaterAllocationNativeURL = ""

print("Resetting Index")  # Hardcoded
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
mask = outdf100.loc[ (outdf100["WaterSourceUUID"].isnull()) | (outdf100["WaterSourceUUID"] == '') | (outdf100['WaterSourceUUID'].str.len() > 200) | (outdf100["WaterSourceUUID"].str.contains(',') == True) ].assign(ReasonRemoved='Bad WaterSourceUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["WaterSourceUUID"].isnull()) | (outdf100["WaterSourceUUID"] == '') | (outdf100['WaterSourceUUID'].str.len() > 200) | (outdf100["WaterSourceUUID"].str.contains(',') == True) ].index
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
mask = outdf100.loc[ (outdf100["AllocationAmount"].isnull()) | (outdf100["AllocationAmount"] == '') | (outdf100['AllocationAmount'].str.contains(',') == True) ].assign(ReasonRemoved='Bad AllocationAmount').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["AllocationAmount"].isnull()) | (outdf100["AllocationAmount"] == '') | (outdf100['AllocationAmount'].str.contains(',') == True) ].index
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

# AllocationMaximum_float_Yes
mask = outdf100.loc[ (outdf100["AllocationMaximum"].isnull()) | (outdf100["AllocationMaximum"] == '') | (outdf100['AllocationMaximum'].str.contains(',') == True) ].assign(ReasonRemoved='Bad AllocationMaximum').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["AllocationMaximum"].isnull()) | (outdf100["AllocationMaximum"] == '') | (outdf100['AllocationMaximum'].str.contains(',') == True) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

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
mask = outdf100.loc[ (outdf100["AllocationPriorityDate"].isnull()) | (outdf100["AllocationPriorityDate"] == '') | (outdf100["AllocationPriorityDate"].str.contains(',') == True) ].assign(ReasonRemoved='Bad AllocationPriorityDate').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["AllocationPriorityDate"].isnull()) | (outdf100["AllocationPriorityDate"] == '') | (outdf100["AllocationPriorityDate"].str.contains(',') == True) ].index
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
mask = outdf100.loc[ (outdf100["AllocationTypeCV"].isnull()) |
                     (outdf100["AllocationTypeCV"] == '') |
                     (outdf100["AllocationPriorityDate"].str.contains(',') == True) |
                     (outdf100["AllocationTypeCV"].str.len() > 250) ].assign(ReasonRemoved='Bad AllocationTypeCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["AllocationTypeCV"].isnull()) |
                     (outdf100["AllocationTypeCV"] == '') |
                     (outdf100["AllocationPriorityDate"].str.contains(',') == True) |
                     (outdf100["AllocationTypeCV"].str.len() > 250) ].index
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
    dfpurge.to_csv('ProcessedInputData/waterallocations_missing.csv', index=False)


print("Done.")


