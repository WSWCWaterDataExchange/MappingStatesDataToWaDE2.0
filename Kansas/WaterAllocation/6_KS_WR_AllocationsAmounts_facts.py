#Date Created: 03/16/2020
#Author: Ryan James
#Purpose: To extract UT allocation use information and population dataframe WaDEQA 2.0.
#         1) Simple creation of working dataframe (df), with output dataframe (outdf).
#         2) Drop all nulls before combining duplicate rows on NativeID.


# Needed Libraries
############################################################################
import numpy as np
import pandas as pd
import os
from datetime import datetime


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/WaterAllocation"  # Specific to my machine, will need to change.
os.chdir(workingDir)
IDM_fileInput = "RawinputData/P_UtahMaster.csv"
method_fileInput = "ProcessedInputData/methods.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_IDM = pd.read_csv(IDM_fileInput)  # The State's Master input dataframe.
df_method = pd.read_csv(method_fileInput)  # Method dataframe
df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

#WaDE dataframe columns
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


# For creating SiteUUID
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

# For creating WaterSourceUUID
def retrieveWaterSourceUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue  # remove whitespace chars
        try:
            outList = WaterSourceUUIDdict[String1]
        except:
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
AllocationLegalStatusDictionary={
"ADEC":"Adjudication Decree",
"APP":"Approved",
"CERT":"Certificated",
"DIS":"Disallowed",
"EXP":"Expired",
"FORF":"Forfeited",
"LAP":"Lapsed",
"LAPD":"Lapsed(Destroyed), Currently NOT Used",
"NPR":"No Proof Required",
"NUSE":"Nonuse",
"PERF":"Perfected",
"REJ":"Rejected",
"REJD":"Rejected(Destroyed), Currently Not Used",
"RNUM":"Renumbered",
"TERM":"Terminated",
"UNAP":"Unapproved",
"WD":"Withdrawn",
"WDD":"Withdrawn(Destroyed), Currently Not Used",
"WUC":"Water User`s Claim"}
def assignAllocationLegalStatusCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unknown'
    else:
        colrowValueStr = colrowValue.strip()  # remove whitespace chars
        try:
            outList = AllocationLegalStatusDictionary[colrowValueStr]
        except:
            outList = 'Unknown'
    return outList


# For creating BeneficialUseCategory
benUseDict = {
    "I":"Irrigation",
    "S":"Stockwatering",
    "D":"Domestic",
    "M":"Municipal",
    "X":"Mining",
    "P":"Power",
    "O":"Other"
}
def assignBenUseCategory(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unknown'
    else:
        benUseListStr = colrowValue.strip()  # remove whitespace chars
        outList = ",".join(benUseDict[inx] for inx in list(str(benUseListStr)))
    return outList

# For creating AllocationAmount
def assignAllocationBasis(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unknown'
    else:
        outList = colrowValue.strip()
    return outList

# For creating AllocationTypeCV
AllocationTypeCVDictionary={
"ADEC":"Adjudication Decree",
"ADV":"Adverse Use",
"APPL":"Application to Appropriate",
"DEC":"Decree",
"DIL":"Diligence Claim",
"FEDR": "Federal Reserved Water Right",
"FIXD":"Fixed-Time Application",
"PAC":"Pending Adjudication Claim",
"SHAR":"Water Company Shares",
"TEMP":"Temporary Application",
"UGWC":"Underground Water Claim"
}
def assignallocTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        benUseListStr = colrowValue.strip()  # remove whitespace chars
        try:
            outList = AllocationTypeCVDictionary[benUseListStr]
        except:
            outList = ''
    return outList

# For creating Owner
def assignownerName(colrowValue1, colrowValue2):
    if colrowValue1 == '' or pd.isnull(colrowValue1):
        outList1 = ''
    else:
        outList1 = colrowValue1.strip()  # remove whitespace chars
    if colrowValue2 == '' or pd.isnull(colrowValue2):
        outList2 = ''
    else:
        outList2 = colrowValue2.strip()  # remove whitespace chars

    if outList1 == '' and outList2 == '':
        outList = ''
    elif outList1 == '':
        outList = outList2
    elif outList2 == '':
        outList = outList1
    else:
        outList = ",".join(map(str, [colrowValue1, colrowValue2]))
    return outList

# For creating LegalStatausCV
AllocationLegalStatusDictionary={
"ADEC":"Adjudication Decree",
"APP":"Approved",
"CERT":"Certificated",
"DIS":"Disallowed",
"EXP":"Expired",
"FORF":"Forfeited",
"LAP":"Lapsed",
"LAPD":"Lapsed(Destroyed), Currently NOT Used",
"NPR":"No Proof Required",
"NUSE":"Nonuse",
"PERF":"Perfected",
"REJ":"Rejected",
"REJD":"Rejected(Destroyed), Currently Not Used",
"RNUM":"Renumbered",
"TERM":"Terminated",
"UNAP":"Unapproved",
"WD":"Withdrawn",
"WDD":"Withdrawn(Destroyed), Currently Not Used",
"WUC":"Water User`s Claim"
}
def assignallocLegalStatausCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        benUseListStr = colrowValue.strip()  # remove whitespace chars
        try:
            outList = AllocationLegalStatusDictionary[benUseListStr]
        except:
            outList = ''
    return outList

# For creating AllocationApplicationDate, AllocationPriorityDate
def strLiteralToDateString(inString):
    try:
        if inString == '' or pd.isnull(inString):
            valndf = ''
        else:
            inStringStr = str(int(inString))
            xvs = inStringStr.strip()  # remove whitespace chars`
            if len(xvs) == 8:
                xvstr = xvs
                yrstr = xvstr[0:4]
                mstr = xvstr[4:6]
                dstr = xvstr[6:8]
                valn = mstr + '/' + dstr + '/' + yrstr
                valD = datetime.strptime(valn, '%m/%d/%Y')
                valnDd = valD.date()
                valndf = valnDd.strftime('%m/%d/%Y')
            elif len(xvs) == 4:
                xvstr = xvs + '0101'
                yrstr = xvstr[0:4]
                mstr = xvstr[4:6]
                dstr = xvstr[6:8]
                valn = mstr + '/' + dstr + '/' + yrstr
                valD = datetime.strptime(valn, '%m/%d/%Y')
                valnDd = valD.date()
                valndf = valnDd.strftime('%m/%d/%Y')
            else:
                valndf = ''
    except:
        valndf = ''

    return valndf


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_IDM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")  # Hardcoded
outdf.MethodUUID = "UT_Water Allocation"

print("OrganizationUUID")  # Hardcoded
outdf.OrganizationUUID = "UTDWRE"

print("SiteUUID")
SitUUIDdict = pd.Series(df_sites.SiteUUID.values, index = df_sites.SiteNativeID).to_dict()
outdf['SiteUUID'] = df_IDM.apply(lambda row: retrieveSiteUUID(row['SiteLocation']), axis=1)

print("VariableSpecificUUID")  # Hardcoded
outdf.VariableSpecificUUID = "UT_Allocation All"

print("WaterSourceUUID")
WaterSourceUUIDdict = pd.Series(df_watersources.WaterSourceUUID.values, index = df_watersources.WaterSourceName).to_dict()
outdf['WaterSourceUUID'] = df_IDM.apply(lambda row: retrieveWaterSourceUUID(row['WREX_SOURCE']), axis=1)
##############################################################

print("AllocationAmount")
outdf['AllocationAmount'] = df_IDM.apply(lambda row: assignAllocationAmount(row['WREX_CFS']), axis=1)

print("AllocationApplicationDate")  # Hardcoded
outdf['AllocationApplicationDate'] = df_IDM.apply(lambda row: strLiteralToDateString(row['DATE_FILED']), axis=1)

print("AllocationAssociatedConsumptiveUseSiteIDs")  # Hardcoded
outdf.AllocationAssociatedConsumptiveUseSiteIDs = ""

print("AllocationAssociatedWithdrawalSiteIDs")  # Hardcoded
outdf.AllocationAssociatedWithdrawalSiteIDs = ""

print("AllocationBasisCV")
outdf.AllocationBasisCV = "Unknown"

print("AllocationChangeApplicationIndicator")  # Hardcoded
outdf['AllocationChangeApplicationIndicator'] = ""

print("AllocationCommunityWaterSupplySystem")
outdf['AllocationCommunityWaterSupplySystem'] = df_IDM['MUNICIPALITY']

print("AllocationCropDutyAmount")  # Hardcoded
outdf['AllocationCropDutyAmount'] = df_IDM['IRRIGATION_DEPLETION']

print("AllocationExpirationDate")  # Hardcoded
outdf['AllocationExpirationDate'] = df_IDM['DATE_TERMINATED']

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_IDM.apply(lambda row: assignAllocationLegalStatusCV(row['WREX_STATUS']), axis=1)

print("AllocationMaximum")  # Hardcoded
outdf['AllocationMaximum'] = df_IDM['WREX_ACFT']

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_IDM['WRNUM']

print("AllocationOwner")
outdf['AllocationOwner'] = df_IDM.apply(lambda row: assignownerName(row['OWNER_LAST_NAME'], row['OWNER_FIRST_NAME']), axis=1)

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_IDM['DATE_PRIORITY']

print("AllocationTimeframeEnd")
outdf['AllocationTimeframeEnd'] = df_IDM['AllocationTimeframeEnd']

print("AllocationTimeframeStart")
outdf['AllocationTimeframeStart'] = df_IDM['AllocationTimeframeStart']

print("AllocationTypeCV")  # Hardcoded
outdf['AllocationTypeCV'] = df_IDM.apply(lambda row: assignallocTypeCV(row['TYPE_OF_RIGHT']), axis=1)

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_IDM.apply(lambda row: assignBenUseCategory(row['WATER_USES']), axis=1)

print("CommunityWaterSupplySystem")  # Hardcoded
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")  # Hardcoded
outdf.CropTypeCV = ""

print("CustomerTypeCV")  # Hardcoded
outdf.CustomerTypeCV = ""

print("DataPublicationDate")  # Hardcoded
outdf.DataPublicationDate = "03/16/2020"

print("DataPublicationDOI")  # Hardcoded
outdf.DataPublicationDOI = ""

print("GeneratedPowerCapacityMW")  # Temp Fix
outdf.GeneratedPowerCapacityMW = ""
#outdf['GeneratedPowerCapacityMW'] = df_IDM.apply(lambda row: row['POWER_CAPACITY']/1000000, axis=1)

print("IrrigatedAcreage")
outdf['IrrigatedAcreage'] = df_IDM['IRRIGATION_ACREAGE']

print("IrrigationMethodCV")
#outdf.IrrigationMethodCV = ""

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


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")  # Hardcoded
dfpurge = pd.DataFrame(index=outdf100.index, columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')
# dfpurge = dfpurge.insert(0, 'ReasonRemoved')

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
mask = outdf100.loc[ (outdf100["AllocationAmount"].isnull()) | (outdf100["AllocationAmount"] == '') ].assign(ReasonRemoved='Bad AllocationAmount').reset_index()
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


