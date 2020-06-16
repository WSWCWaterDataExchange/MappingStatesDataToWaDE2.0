#Date Created: 06/10/2020
#Author: Joseph Brewer
#Purpose: To extract TX allocation use information and population dataframe WaDEQA 2.0.
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
workingDir="/Users/augustus/Desktop/WSWC/WaDE/MappingStatesDataToWaDE2.0/Texas/WaterAllocation/"
os.chdir(workingDir)
TXM_fileInput = "RawInputData/Water Right Point.csv"  #Change this to fit state
method_fileInput = "ProcessedInputData/methods.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

use_fileInput = 'RawInputData/Water Use.csv'
owner_fileInput = 'RawInputData/Water Right Owner.csv'



df_TXM = pd.read_csv(TXM_fileInput)  # The Texas Master input dataframe.
df_method = pd.read_csv(method_fileInput)  # Method dataframe
df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

df_use=pd.read_csv(use_fileInput, usecols=['Water Right ID', 'Use'])
df_owner = pd.read_csv(owner_fileInput, usecols=['Water Right ID', 'Owner'])

#WaDE dataframe columns
columns = [
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
# For creating WaterSourceName
def assignWaterSourceName(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unknown"
    else:
        outList = colrowValue
    return outList

# For creating WaterSourceTypeCV
UnknownWSCVDict = {
"Ground Water" : "Ground Water",
"Spring" : "groundwater/spring",
"Waste Water" : "Reuse",
"Wasteway" : "Reuse",
"Wastewater" : "Reuse",
"Drain" : "Drain",
"Reservoir" : "reservoir"}
def WaterSourceTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = UnknownWSCVDict[String1]
        except:
            outList = "Surface Water"

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
        outList = 0
    else:
        String1 = colrowValue  # remove whitespace chars
        try:
            outList = SitUUIDdict[String1]
        except:
            outList = colrowValue
    return outList

# For creating AllocationAmount
def assignAllocationAmount(colrowValue):
    if colrowValue <= 0 or pd.isnull(colrowValue):
        outList = 0
    else:
        outList = colrowValue
    return outList

# For creating AllocationLegalStatusCV
def assignAllocationLegalStatusCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unknown"
    else:
        outList = "Active"
    return outList

# For creating AllocationLegalStatusCV
def assignBeneficialUseCategory(colrowValue):
    if colrowValue == "[]" or colrowValue == "" or pd.isnull(colrowValue):
        outList = "Unknown"
    else:
        outList = colrowValue.replace("[", "").replace("]", "").replace("'", "")
    return outList

# For creating AllocationAmount
def assignAllocationBasis(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unknown'
    else:
        outList = colrowValue
    return outList

def retrieveNames(df):
    ids = df['Water Right ID'].drop_duplicates()
    outdf = pd.DataFrame(ids)
    outdf.reset_index(drop=True, inplace=True)
    outdf['owners'] = ''
    outdf.set_index(outdf['Water Right ID'], inplace=True)

    for id in ids:
        vals = df.loc[df['Water Right ID'] == id]
        vals.reset_index(inplace=True)
        names=[]
        for i, row in vals.iterrows():
            names.append(row['Owner'])

        outdf.at[id,'owners'] = ','.join(names)

    return outdf

def retrieveUses(df):
    ids = df['Water Right ID'].drop_duplicates()
    outdf = pd.DataFrame(ids)
    outdf.reset_index(drop=True, inplace=True)
    outdf['uses'] = ''
    outdf.set_index(outdf['Water Right ID'], inplace=True)

    for id in ids:
        vals = df.loc[df['Water Right ID'] == id]
        vals.reset_index(inplace=True)
        uses = []
        for i, row in vals.iterrows():
            new_use = row['Use']

            if new_use not in uses:
                uses.append(new_use)

        outdf.at[id, 'uses'] = ','.join(uses)

    return outdf

# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe oudf...")
outdf = pd.DataFrame(index=df_TXM.index, columns=columns)  # The output dataframe

print("MethodUUID")  # Hardcoded
outdf.MethodUUID = "TCEQ_WaterRights"

print("OrganizationUUID")  # Hardcoded
outdf.OrganizationUUID = "TCEQ"

print("SiteUUID")
# outdf['SiteUUID'] = df_IDM.apply(lambda row: retrieveSiteUUID(row['WaterRightNumber'], df_sites), axis=1)
SitUUIDdict = pd.Series(df_sites.SiteNativeID.values, index = df_sites.SiteUUID).to_dict()
outdf['SiteUUID'] = df_sites.apply(lambda row: retrieveSiteUUID(row['SiteUUID']), axis=1)
outdf['SiteUUID'] = df_sites['SiteUUID']

print("VariableSpecificUUID")  # Hardcoded
outdf.VariableSpecificUUID = "TCEQ_Allocation All"

print("WaterSourceUUID")
#outdf['WaterSourceUUID'] = df_TXM.apply(lambda row: retrieveWaterSourceUUID(row['WaterSourceName'], row['WaterSourceTypeCV'], df_watersources), axis=1)
outdf['WaterSourceUUID'] = df_watersources.loc[0,'WaterSourceUUID']

##############################################################
# Need to recreate WSName and WStype for this to work... than match waterousrce.csv 'WaterSourceUUID' to the newly recreated WSName and WStype just to correctly  match the correct ID value.
# May need once TX supplies more water source info
"""
print("WaterSourceName")
df_IDM = df_TXM.assign(WaterSourceName = '')
df_IDM['WaterSourceName'] = df_TXM.apply(lambda row: assignWaterSourceName(row['TributaryOf']), axis=1)

print("WaterSourceTypeCV")
df_IDM = df_IDM.assign(WaterSourceTypeCV = '')
df_IDM['WaterSourceTypeCV'] = df_TXM.apply(lambda row: WaterSourceTypeCV(row['Source']), axis=1)

print("WaterSourceUUID")
outdf['WaterSourceUUID'] = df_TXM.apply(lambda row: retrieveWaterSourceUUID(row['WaterSourceName'], row['WaterSourceTypeCV'], df_watersources), axis=1)
"""
##############################################################

print("AllocationAmount")
#outdf['AllocationAmount'] = df_TXM.apply(lambda row: assignAllocationAmount(row['OverallMaxDiversionRate']), axis=1)
outdf['AllocationAmount'] = ""

print("AllocationApplicationDate")  # Hardcoded
outdf.AllocationApplicationDate = ""

print("AllocationAssociatedConsumptiveUseSiteIDs")  # Hardcoded
outdf.AllocationAssociatedConsumptiveUseSiteIDs = ""

print("AllocationAssociatedWithdrawalSiteIDs")  # Hardcoded
outdf.AllocationAssociatedWithdrawalSiteIDs = ""

print("AllocationBasisCV")
#outdf['AllocationBasisCV'] = df_TXM.apply(lambda row: assignAllocationBasis(row['Basis']), axis=1)
outdf['AllocationBasisCV'] = ""

print("AllocationChangeApplicationIndicator")  # Hardcoded
outdf.AllocationChangeApplicationIndicator = ""

print("AllocationCommunityWaterSupplySystem")  # Hardcoded
outdf['AllocationCommunityWaterSupplySystem'] = ''

print("AllocationCropDutyAmount")  # Hardcoded
outdf['AllocationCropDutyAmount'] = ""

print("AllocationExpirationDate")  # Hardcoded
outdf.AllocationExpirationDate = ""

print("AllocationLegalStatusCV")
#outdf['AllocationLegalStatusCV'] = df_TXM.apply(lambda row: assignAllocationLegalStatusCV(row['Status']), axis=1)
outdf['AllocationLegalStatusCV'] = ""

print("AllocationMaximum")  # Hardcoded
outdf['AllocationMaximum'] = ""

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_sites['SiteNativeID']

print("AllocationOwner")
df_owners = retrieveNames(df_owner)
for i, row in outdf.iterrows():
    try:
        x = row['AllocationNativeID']
        y = df_owners.loc[df_owners['Water Right ID'] == x]
        outdf.at[i, 'AllocationOwner'] = y.loc[x, 'owners']
    except:
        outdf.at[i, 'AllocationOwner'] = ''

print("AllocationPriorityDate")
#outdf['AllocationPriorityDate'] = df_TXM['PriorityDate']
outdf['AllocationPriorityDate'] = 'Unspecified'

print("AllocationTimeframeEnd")
#outdf['AllocationTimeframeEnd'] = df_IDM['AllocationTimeframeEnd']
outdf.AllocationTimeframeEnd = ""

print("AllocationTimeframeStart")
#outdf['AllocationTimeframeStart'] = df_IDM['AllocationTimeframeStart']
outdf.AllocationTimeframeStart = ""

print("AllocationTypeCV")  # Hardcoded
outdf['AllocationTypeCV'] = ''

print("BeneficialUseCategory")
df_uses = retrieveUses(df_use)
for i, row in outdf.iterrows():
    try:
        x = row['AllocationNativeID']
        y = df_uses.loc[df_uses['Water Right ID'] == x]
        outdf.at[i, 'BeneficialUseCategory'] = y.loc[x, 'uses']
    except:
        outdf.at[i, 'BeneficialUseCategory'] = ''


print("CommunityWaterSupplySystem")  # Hardcoded
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")  # Hardcoded
outdf.CropTypeCV = ""

print("CustomerTypeCV")  # Hardcoded
outdf.CustomerTypeCV = ""

print("DataPublicationDate")  # Hardcoded
outdf.DataPublicationDate = "06/16/20"

print("DataPublicationDOI")  # Hardcoded
outdf.DataPublicationDOI = ""

print("GeneratedPowerCapacityMW")  # Hardcoded
outdf.GeneratedPowerCapacityMW = ""

print("IrrigatedAcreage")
print("IrrigatedAcreage")
outdf.IrrigatedAcreage = ""

print("IrrigationMethodCV")
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
outdf["WaterAllocationNativeURL"] = ''


# Check required fields are not null
############################################################################
outdfpurge = pd.DataFrame(columns=columns)  # purge DataFrame holder

print("Checking required is not null...")
outdf_nullMand = outdf.loc[(outdf["MethodUUID"].isnull()) | (outdf["MethodUUID"] == '') |
                              (outdf["OrganizationUUID"].isnull()) | (outdf["OrganizationUUID"] == '') |
                              (outdf["SiteUUID"].isnull()) | (outdf["SiteUUID"] == '') |
                              (outdf["VariableSpecificUUID"].isnull()) | (outdf["VariableSpecificUUID"] == '') |
                              (outdf["WaterSourceUUID"].isnull()) | (outdf["WaterSourceUUID"] == '') |
                              (outdf["AllocationPriorityDate"].isnull()) | (outdf["AllocationPriorityDate"] == '') |
                              (outdf["BeneficialUseCategory"].isnull()) | (outdf["BeneficialUseCategory"] == '') |
                              (outdf["DataPublicationDate"].isnull()) | (outdf["DataPublicationDate"] == '')]

print("Dropping null AllocationsAmount...")
outdfpurgeAA = outdf.loc[(outdf["AllocationAmount"].isnull()) | (outdf["AllocationAmount"] == '') & ((outdf["AllocationMaximum"].isnull()) | (outdf["AllocationMaximum"] == ''))]
outdfpurge = outdfpurge.append(outdfpurgeAA)
if len(outdfpurgeAA.index) > 0:
    dropIndex = outdf.loc[(outdf["AllocationAmount"].isnull()) | (outdf["AllocationAmount"] == '') & ((outdf["AllocationMaximum"].isnull()) | (outdf["AllocationMaximum"] == ''))].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

print("Dropping null SiteUUIDs...")
outdfpurgeSUUID = outdf.loc[(outdf["SiteUUID"].isnull()) | (outdf["SiteUUID"]== '')]
outdfpurge = outdfpurge.append(outdfpurgeSUUID)
if len(outdfpurgeSUUID.index) > 0:
    dropIndex = outdf.loc[(outdf["SiteUUID"].isnull()) | (outdf["SiteUUID"]== '')].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

print("Dropping null PriorityDate...")
outdfpurgePD = outdf.loc[(outdf["AllocationPriorityDate"].isnull()) | (outdf["AllocationPriorityDate"] == '')]
outdfpurge = outdfpurge.append(outdfpurgePD)
if len(outdfpurgePD.index) > 0:
    dropIndex = outdf.loc[(outdf["AllocationPriorityDate"].isnull()) | (outdf["AllocationPriorityDate"] == '')].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

print("Dropping null WaterSourceUUID...")
outdfpurgeWSUUID = outdf.loc[(outdf["WaterSourceUUID"].isnull()) | (outdf["WaterSourceUUID"] == '')]
outdfpurge = outdfpurge.append(outdfpurgeWSUUID)
if len(outdfpurgeWSUUID.index) > 0:
    dropIndex = outdf.loc[(outdf["WaterSourceUUID"].isnull()) | (outdf["WaterSourceUUID"] == '')].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)


# Solving WaDE 2.0 Upload Issues
############################################################################
# Date Noted: 02/28/2020
# Note: Insure single 'AllocationNativeID' entry.
print("Joining outdf duplicates based on AllocationNativeID...")
outdf100 = pd.DataFrame(columns=columns)  # The output dataframe for CSV.
outdf100 = outdf.groupby('AllocationNativeID', sort=False).agg(lambda x: ','.join([str(elem) for elem in (list(set(x)))])).reset_index()

# Date Noted: 02/27/2020
# Note: Insure 'WaterSourceUUID' only has 1 entry. Error due to above merge / we don't allow multiple WSUUIDs.
print("temp fix WaterSourceUUID")
"""
def tempfixWSUUID(colrowValueA):
    #pass in text, split on 'sep', return first
    sep = ','
    result = colrowValueA.split(sep, 1)[0]
    return result
outdf100['WaterSourceUUID']  = outdf100.apply(lambda row: tempfixWSUUID(row['WaterSourceUUID']), axis=1)
"""

# Replace any blank cells within the output df with NaN.
############################################################################
# outdf100 = outdf100.replace('', np.nan)  # may not need to do this.... doesn't really work due to merge


# Checking Dataframe data types
############################################################################
print(outdf100.dtypes)


# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")
# The working output DataFrame for WaDE 2.0 input.
outdf100.to_csv('ProcessedInputData/waterallocations.csv', index=False)

# Report purged values.
if(len(outdfpurge.index) > 0):
    outdfpurge.to_csv('ProcessedInputData/waterallocations_missing.csv')  # index=False,

# Report missing values.
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/waterallocations_mandatoryFieldMissing.csv')  # index=False,



print("Done.")


# Code not using
############################################################################

# # For creating WaterSourceName
# UnknownWSNameDict = {
#     "Ground Water":"Unknown",
#     "Spring":"Unknown",
#     "Unnamed Stream":"Unknown",
#     "Unnamed Streams":"Unknown"}
# def assignWaterSourceName(colrowValue):
#     if colrowValue == '' or pd.isnull(colrowValue):
#         outList = "Unknown"
#     else:
#         String1 = colrowValue.strip()  # remove whitespace chars
#         try:
#             outList = UnknownWSNameDict[String1]
#         except:
#             outList = colrowValue
#
#     return outList


# ###################################################################################
# # Date Noted: 02/28/2020
# # Note: Priority date errors. date
# print("fix AllocationPriorityDate datatype")
# #changing data type of 'AllocationPriorityDate' to datatype, then changing format of 'Date' to yyyy-mm-dd
# outdf['AllocationPriorityDate'] = pd.to_datetime(outdf['AllocationPriorityDate'], errors = 'coerce')
# outdf['AllocationPriorityDate'] = pd.to_datetime(outdf['AllocationPriorityDate'].dt.strftime('%m/%d/%Ym'))
# ###################################################################################


# # Separate outdf to fix a few things
# ############################################################################
# print("Making outdf200temp to fix a few things...")
# outdf200 = pd.DataFrame(index=df_IDM.index, columns=columns)  # The output dataframe for CSV.
# outdf200 = outdf.groupby('AllocationNativeID', sort=False).agg(lambda x: list(set(x))).reset_index()
#
# # Aggregating IrrigatedAcreage from .groupby() into one value. Exporting to outdf100 for csv.
# print("summing IrrigatedAcreage.")
# for x, y in outdf200['IrrigatedAcreage'].iteritems():
#     newlist = []
#     for i in y:
#         newlist.append(i)
#     if ',' in newlist:
#         newlist.remove(',')
#     newlist = [float(i) for i in newlist]
#     outdf200['IrrigatedAcreage'][x] = sum(newlist)
#
# outdf100['IrrigatedAcreage'] = outdf200['IrrigatedAcreage']