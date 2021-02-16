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

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/ErrorCheckCode")
import TestErrorFunctions


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


# For creating SiteUUID
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

# For creating WaterSourceUUID
def retrieveWaterSourceUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = WaterSourceUUIDdict[String1]
        except:
            outList = ''
    return outList

# For creating AllocationFlow_CFS
def assignAllocationFlow_CFS(colrowValue):
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
        outList = 'Unspecified'
    else:
        benUseListStr = colrowValue.strip()  # remove whitespace chars
        outList = ",".join(benUseDict[inx] for inx in list(str(benUseListStr)))
    return outList

# For creating AllocationFlow_CFS
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

print("MethodUUID")
outdf.MethodUUID = "UT_Water Allocation"

print("OrganizationUUID")
outdf.OrganizationUUID = "UTDWRi"

print("SiteUUID")
SitUUIDdict = pd.Series(df_sites.SiteUUID.values, index = df_sites.SiteNativeID).to_dict()
outdf['SiteUUID'] = df_IDM.apply(lambda row: retrieveSiteUUID(row['SiteLocation']), axis=1)

print("VariableSpecificUUID")
outdf.VariableSpecificUUID = "UT_Allocation All"

print("WaterSourceUUID")
WaterSourceUUIDdict = pd.Series(df_watersources.WaterSourceUUID.values, index = df_watersources.WaterSourceName).to_dict()
outdf['WaterSourceUUID'] = df_IDM.apply(lambda row: retrieveWaterSourceUUID(row['WREX_SOURCE']), axis=1)
##############################################################

print("AllocationApplicationDate")
outdf['AllocationApplicationDate'] = df_IDM.apply(lambda row: strLiteralToDateString(row['DATE_FILED']), axis=1)

print("AllocationAssociatedConsumptiveUseSiteIDs")
outdf.AllocationAssociatedConsumptiveUseSiteIDs = ""

print("AllocationAssociatedWithdrawalSiteIDs")
outdf.AllocationAssociatedWithdrawalSiteIDs = ""

print("AllocationBasisCV")
outdf.AllocationBasisCV = "Unknown"

print("AllocationChangeApplicationIndicator")
outdf['AllocationChangeApplicationIndicator'] = ""

print("AllocationCommunityWaterSupplySystem")
outdf['AllocationCommunityWaterSupplySystem'] = df_IDM['MUNICIPALITY']

print("AllocationCropDutyAmount")
outdf['AllocationCropDutyAmount'] = df_IDM['IRRIGATION_DEPLETION']

print("AllocationExpirationDate")
outdf['AllocationExpirationDate'] = df_IDM['DATE_TERMINATED']

print("AllocationFlow_CFS")
outdf['AllocationFlow_CFS'] = df_IDM.apply(lambda row: assignAllocationFlow_CFS(row['WREX_CFS']), axis=1)

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_IDM.apply(lambda row: assignAllocationLegalStatusCV(row['WREX_STATUS']), axis=1)

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_IDM['WRNUM']

print("AllocationOwner")
outdf['AllocationOwner'] = df_IDM.apply(lambda row: assignownerName(row['OWNER_LAST_NAME'], row['OWNER_FIRST_NAME']), axis=1)

print("AllocationSDWISIdentifierCV")
outdf.AllocationSDWISIdentifierCV = ""

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_IDM['DATE_PRIORITY']

print("AllocationTimeframeEnd")
outdf['AllocationTimeframeEnd'] = df_IDM['AllocationTimeframeEnd']

print("AllocationTimeframeStart")
outdf['AllocationTimeframeStart'] = df_IDM['AllocationTimeframeStart']

print("AllocationTypeCV")
outdf['AllocationTypeCV'] = df_IDM.apply(lambda row: assignallocTypeCV(row['TYPE_OF_RIGHT']), axis=1)

print("AllocationVolume_AF")
outdf['AllocationVolume_AF'] = df_IDM['WREX_ACFT']

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_IDM.apply(lambda row: assignBenUseCategory(row['WATER_USES']), axis=1)

print("CommunityWaterSupplySystem")
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")
outdf.CropTypeCV = ""

print("CustomerTypeCV")
outdf.CustomerTypeCV = ""

print("DataPublicationDate")
outdf.DataPublicationDate = "03/16/2020"

print("DataPublicationDOI")
outdf.DataPublicationDOI = ""

print("ExemptOfVolumeFlowPriority")
outdf.ExemptOfVolumeFlowPriority = 0

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


#Error checking each field
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
