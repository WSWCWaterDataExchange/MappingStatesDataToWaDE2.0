#Date Created: 02/06/2020
#Purpose: To extract ID allocation use information and population dataframe WaDEQA 2.0.
#       2) Simple creation of working dataframe (df), with output dataframe (outdf).


# Needed Libraries
############################################################################
import numpy as np
import pandas as pd
import os


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Idaho/WaterAllocation"  # Specific to my machine, will need to change.
os.chdir(workingDir)
IDM_fileInput = "RawinputData/P_IdahoMaster.csv"
method_fileInput = "ProcessedInputData/methods.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_IDM = pd.read_csv(IDM_fileInput)  # The Idaho Master input dataframe.
df_method = pd.read_csv(method_fileInput)  # Method dataframe
df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

#WaDE dataframe columns
columns = [
    # "MethodID",  # Think the WaDE 2.0 database creates these.  Should only need to link UUID.
    # "OrganizationID",
    # "SiteID",
    # "VariableSpecificID",
    # "WaterSourceID",
    "MethodUUID",
    "OrganizationUUID",
    "SiteUUID",
    "VariableSpecificUUID",
    "WaterSourceUUID",
    "AllocationAmount",
    #"AllocationApplicationDateID",
    "AllocationApplicationDate",
    "AllocationAssociatedConsumptiveUseSiteIDs",
    "AllocationAssociatedWithdrawalSiteIDs",
    "AllocationBasisCV",
    "AllocationChangeApplicationIndicator",
    "AllocationCommunityWaterSupplySystem",
    "AllocationCropDutyAmount",
    #"AllocationExpirationDateID",
    "AllocationExpirationDate",
    "AllocationLegalStatusCV",
    "AllocationMaximum",
    "AllocationNativeID",
    "AllocationOwner",
    #"AllocationPriorityDateID",
    "AllocationPriorityDate",
    "AllocationTimeframeEnd",
    "AllocationTimeframeStart",
    "AllocationTypeCV",
    #"BeneficialUseCategoryCV",
    "BeneficialUseCategory",
    "CommunityWaterSupplySystem",
    "CropTypeCV",
    "CustomerTypeCV",
    #"DataPublicationDateID",
    "DataPublicationDate",
    "DataPublicationDOI",
    "GeneratedPowerCapacityMW",
    "IrrigatedAcreage",
    "IrrigationMethodCV",
    "LegacyAllocationIDs",
    "PopulationServed",
    "PowerType",
    #"PrimaryUseCategoryCV",
    "PrimaryUseCategory",
    #"SDWISIdentifierCV",
    "AllocationSDWISIdentifierCV",
    "WaterAllocationNativeURL"]


# Custom Site Functions
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

# For creating SiteUUID
# def retrieveSiteUUID(colrowValue, df_sites):
    # if colrowValue == '' or pd.isnull(colrowValue):
    #     outList = ''
    # else:
    #     ml = df_sites.loc[df_sites['SiteNativeID'] == colrowValue, 'SiteUUID']  #think we use WaDESiteUUID instead of SiteUUID, for now.
    #     if not(ml.empty):  # check if the series is empty
    #         outList = ml.iloc[0]
    #     else:
    #         outList = ''
    # return outList

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


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe oudf...")
outdf = pd.DataFrame(index=df_IDM.index, columns=columns)  # The output dataframe

print("MethodUUID")  # Hardcoded
outdf.MethodUUID = "IDWR_DiversionTracking"

print("OrganizationUUID")  # Hardcoded
outdf.OrganizationUUID = "IDWR"

print("SiteUUID")
# outdf['SiteUUID'] = df_IDM.apply(lambda row: retrieveSiteUUID(row['WaterRightNumber'], df_sites), axis=1)
SitUUIDdict = pd.Series(df_sites.SiteNativeID.values, index = df_sites.SiteUUID).to_dict()
outdf['SiteUUID'] = df_IDM.apply(lambda row: retrieveSiteUUID(row['WaterRightNumber']), axis=1)

print("VariableSpecificUUID")  # Hardcoded
outdf.VariableSpecificUUID = "IDWR Allocation All"

##############################################################
# Need to recreate WSName and WStype for this to work... than match waterousrce.csv 'WaterSourceUUID' to the newly recreated WSName and WStype just to correctly  match the correct ID value.
print("WaterSourceName")
df_IDM = df_IDM.assign(WaterSourceName = '')
#df_IDM['WaterSourceName'] = df_IDM.apply(lambda row: assignWaterSourceName(row['TributaryOf']), axis=1)
df_IDM['WaterSourceName'] = df_IDM.apply(lambda row: assignWaterSourceName(row['TributaryOf']), axis=1)

print("WaterSourceTypeCV")
df_IDM = df_IDM.assign(WaterSourceTypeCV = '')
df_IDM['WaterSourceTypeCV'] = df_IDM.apply(lambda row: WaterSourceTypeCV(row['Source']), axis=1)

print("WaterSourceUUID")
outdf['WaterSourceUUID'] = df_IDM.apply(lambda row: retrieveWaterSourceUUID(row['WaterSourceName'], row['WaterSourceTypeCV'], df_watersources), axis=1)
##############################################################

print("AllocationAmount")
outdf['AllocationAmount'] = df_IDM.apply(lambda row: assignAllocationAmount(row['OverallMaxDiversionRate']), axis=1)

print("AllocationApplicationDate")  # Hardcoded
outdf.AllocationApplicationDate = ""

print("AllocationAssociatedConsumptiveUseSiteIDs")  # Hardcoded
outdf.AllocationAssociatedConsumptiveUseSiteIDs = ""

print("AllocationAssociatedWithdrawalSiteIDs")  # Hardcoded
outdf.AllocationAssociatedWithdrawalSiteIDs = ""

print("AllocationBasisCV")
outdf['AllocationBasisCV'] =df_IDM['Basis']

print("AllocationChangeApplicationIndicator")  # Hardcoded
outdf.AllocationChangeApplicationIndicator = ""

print("AllocationCommunityWaterSupplySystem")  # Hardcoded
outdf['AllocationCommunityWaterSupplySystem'] = ''

print("AllocationCropDutyAmount")  # Hardcoded
outdf['AllocationCropDutyAmount'] = ""

print("AllocationExpirationDate")  # Hardcoded
outdf.AllocationExpirationDate = ""

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_IDM.apply(lambda row: assignAllocationLegalStatusCV(row['Status']), axis=1)

print("AllocationMaximum")  # Hardcoded
outdf['AllocationMaximum'] = ""

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_IDM['RightID']

print("AllocationOwner")
outdf['AllocationOwner'] = df_IDM['Owner']

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_IDM['PriorityDate']

print("AllocationTimeframeEnd")
#outdf['AllocationTimeframeEnd'] = df_IDM['AllocationTimeframeEnd']
outdf.AllocationTimeframeEnd = ""

print("AllocationTimeframeStart")
#outdf['AllocationTimeframeStart'] = df_IDM['AllocationTimeframeStart']
outdf.AllocationTimeframeStart = ""

print("AllocationTypeCV")  # Hardcoded
outdf['AllocationTypeCV'] = ''

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_IDM.apply(lambda row: assignBeneficialUseCategory(row['BeneficialUseCategoryCV']), axis=1)

print("CommunityWaterSupplySystem")  # Hardcoded
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")  # Hardcoded
outdf.CropTypeCV = ""

print("CustomerTypeCV")  # Hardcoded
outdf.CustomerTypeCV = ""

print("DataPublicationDate")  # Hardcoded
outdf.DataPublicationDate = "02/13/2020"

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
outdf["WaterAllocationNativeURL"] = df_IDM['WRReport']


# Combining Duplicates
############################################################################
outdf100 = pd.DataFrame(index=df_IDM.index, columns=columns)  # The output dataframe for CSV.
print("Joining outdf duplicates based on AllocationNativeID...")
outdf100 = pd.DataFrame(index=df_IDM.index, columns=columns)  # The output dataframe for CSV.
outdf100 = outdf.groupby('AllocationNativeID', sort=False).agg(lambda x: ','.join([str(elem) for elem in (list(set(x)))])).reset_index()


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


# Check required fields are not null
############################################################################
# print("Dropping null AllocationsAmount...")
# outdfpurge = outdf100.loc[(outdf100["AllocationAmount"] == '') & (outdf100["AllocationMaximum"] == '')]
# if len(outdfpurge.index) > 0:
#     outdfpurge.to_csv('waterallocations_missing.csv')    #index=False,
#     dropIndex = outdf100.loc[(outdf["AllocationAmount"] == '') & (outdf100["AllocationMaximum"] == '')].index
#     outdf100 = outdf100.drop(dropIndex)
#     outdf100 = outdf100.reset_index(drop=True)

# print("Dropping null SiteUUIDs...")
# outdfnullID = outdf100.loc[outdf100["SiteUUID"] == '']
# if len(outdfnullID.index) > 0:
#     dropIndex = outdf100.loc[outdf100["SiteUUID"] == ''].index
#     outdf100 = outdf100.drop(dropIndex)
#     outdf100 = outdf100.reset_index(drop=True)
#
# print("Dropping null Priority date...")
# outdfnullPR = outdf100.loc[outdf100["AllocationPriorityDate"] == '']
# if len(outdfnullPR.index) > 0:
#     dropIndex = outdf100.loc[outdf100["AllocationPriorityDate"] == ''].index
#     outdf100 = outdf100.drop(dropIndex)
#     outdf100 = outdf100.reset_index(drop=True)
#
# print("Dropping null WaterSourceUUID...")
# outdfnullPR = outdf100.loc[outdf100["WaterSourceUUID"] == '']
# if len(outdfnullPR.index) > 0:
#     dropIndex = outdf100.loc[outdf100["WaterSourceUUID"] == ''].index
#     outdf100 = outdf100.drop(dropIndex)
#     outdf100 = outdf100.reset_index(drop=True)


print("Checking required is not null...")
outdf100 = outdf100.replace('', np.nan)  # Replace any blank cells with NaN.
outdf_nullMand = outdf100.loc[(outdf100["MethodUUID"].isnull())      | (outdf100["OrganizationUUID"].isnull()) |
                              (outdf100["SiteUUID"].isnull())        | (outdf100["VariableSpecificUUID"].isnull()) |
                              (outdf100["WaterSourceUUID"].isnull()) | (outdf100["AllocationPriorityDate"].isnull()) |
                              (outdf100["BeneficialUseCategory"].isnull()) | (outdf100["DataPublicationDate"].isnull())]


# Checking Dataframe data types
############################################################################
print(outdf.dtypes)


# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")
outdf100.to_csv('ProcessedInputData/waterallocations.csv', index=False)

#Report missing values if need be to separate csv
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/waterallocations_mandatoryFieldMissing.csv')  # index=False,


print("Done.")
