#Date Created: 03/02/2020
#Author: Ryan James WSWC
#Purpose: To extract CO allocation use information and population DataFrame WaDEQA 2.0.
#         1) Simple creation of working DataFrame (df), with output DataFrame (outdf).
#         2) Drop all nulls before combining duplicate rows on AllocationNativeID.


# Needed Libraries
############################################################################
import numpy as np
import pandas as pd
import os
import beneficialUseDictionary #Custom .py file containing dictionaries.


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Colorado/WaterAllocation"  # Specific to my machine, will need to change.
os.chdir(workingDir)
CODM_fileInput = "RawinputData/DWR_Water_Right_-_Net_Amounts.csv"
method_fileInput = "ProcessedInputData/methods.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"

df_CODM = pd.read_csv(CODM_fileInput)  # The Idaho Master input dataframe.
df_method = pd.read_csv(method_fileInput)  # Method dataframe
df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe

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
# For creating WaterSourceUUID
#WaterSourceUUIDdict = pd.Series(df_watersources.WaterSourceNativeID.values, index = df_watersources.WaterSourceUUID).to_dict()
WaterSourceUUIDdict = pd.Series(df_watersources.WaterSourceUUID.values, index = df_watersources.WaterSourceName).to_dict()
def retrieveWaterSourceUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        outList = WaterSourceUUIDdict[colrowValue]
    return outList

# For creating SiteUUID
#SitUUIDdict = pd.Series(df_sites.SiteNativeID.values, index = df_sites.SiteUUID).to_dict()
SitUUIDdict = pd.Series(df_sites.SiteUUID.values, index = df_sites.SiteNativeID).to_dict()
def retrieveSiteUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        outList = SitUUIDdict[colrowValue]
    return outList

# For creating AllocationAmount
def assignAllocationAmount(colrowValueA, colrowValueB, colrowValueC):
    colrowValueA = str(colrowValueA)
    colrowValueA = colrowValueA.strip()
    if (colrowValueB != 0) and (colrowValueC != 0):
        outList = 0
    else:
        if (colrowValueA == "C") and (colrowValueB != 0):
            outList = colrowValueB
        elif (colrowValueA  == "C") and (colrowValueC != 0):
            outList = colrowValueC
        else:
            outList = 0
    return outList

# For creating assignAllocationMaximum
def assignAllocationMaximum(colrowValueA, colrowValueB, colrowValueC):
    colrowValueA = str(colrowValueA)
    colrowValueA = colrowValueA.strip()
    if (colrowValueB != 0) and (colrowValueC != 0): \
        outList = 0
    else:
        if (colrowValueA == "A") and (colrowValueB != 0):
            outList = colrowValueB
        elif (colrowValueA  == "A") and (colrowValueC != 0):
            outList = colrowValueC
        else:
            outList = 0
    return outList

# For creating AllocationLegalStatusCV
def assignAllocationLegalStatusCV(colrowValueA, colrowValueB):
    if (colrowValueA == 0) and (colrowValueB == 0):
        outlist = "Conditional Absolute"
    elif (colrowValueA == 0) and (colrowValueB != 0):
        outlist = "Conditional"
    # elif (colrowValueA != 0) and (colrowValueB == 0):
    #     outlist = "Absolute"
    else:
        outlist = "Absolute"
    return outlist

# For creating AllocationLegalStatusCV
benUseDict = beneficialUseDictionary.beneficialUseDictionary_CO
def assignBeneficialUseCategory(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = benUseDict[String1]
        except:
            outList = "Unknown"

    return outList

# For creating AllocationAmount
def assignAllocationNativeID(colrowValueA, colrowValueB, colrowValueC, colrowValueD):
    outList = "-".join(map(str, [colrowValueA, colrowValueB, colrowValueC, colrowValueD]))
    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe oudf...")
outdf = pd.DataFrame(index=df_CODM.index, columns=columns)  # The output dataframe

print("MethodUUID")  # Hardcoded
outdf.MethodUUID = "CODWR_Diversion Tracking"

print("OrganizationUUID")  # Hardcoded
outdf.OrganizationUUID = "CODWR"

print("SiteUUID")
outdf['SiteUUID'] = df_CODM.apply(lambda row: retrieveSiteUUID(row['WDID']), axis=1)

print("VariableSpecificUUID")  # Hardcoded
outdf.VariableSpecificUUID = "CODWR_Allocation All"

print("WaterSourceUUID")
outdf['WaterSourceUUID'] = df_CODM.apply(lambda row: retrieveWaterSourceUUID(row['Water Source']), axis=1)

print("AllocationAmount")
outdf['AllocationAmount'] = df_CODM.apply(lambda row: assignAllocationAmount(row["Decreed Units"], row["Net Absolute"], row["Net Conditional"]), axis=1)

print("AllocationApplicationDate")  # Hardcoded
outdf['AllocationApplicationDate'] = df_CODM['Appropriation Date']

print("AllocationAssociatedConsumptiveUseSiteIDs")  # Hardcoded
outdf.AllocationAssociatedConsumptiveUseSiteIDs = ""

print("AllocationAssociatedWithdrawalSiteIDs")  # Hardcoded
outdf.AllocationAssociatedWithdrawalSiteIDs = ""

print("AllocationBasisCV")  # Hardcoded
outdf.AllocationBasisCV = "Unknown"

print("AllocationChangeApplicationIndicator")  # Hardcoded
outdf.AllocationChangeApplicationIndicator = ""

print("AllocationCommunityWaterSupplySystem")  # Hardcoded
outdf['AllocationCommunityWaterSupplySystem'] = ''

print("AllocationCropDutyAmount")  # Hardcoded
outdf['AllocationCropDutyAmount'] = ""

print("AllocationExpirationDate")  # Hardcoded
outdf.AllocationExpirationDate = ""

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_CODM.apply(lambda row: assignAllocationLegalStatusCV(row['Net Absolute'], row['Net Conditional']), axis=1)

print("AllocationMaximum")
outdf['AllocationMaximum'] = df_CODM.apply(lambda row: assignAllocationMaximum(row["Decreed Units"], row["Net Absolute"], row["Net Conditional"]), axis=1)

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_CODM.apply(lambda row: assignAllocationNativeID(row['Admin No'], row['Order No'], row['Decreed Units'], row['WDID']), axis=1)

print("AllocationOwner")
outdf['AllocationOwner'] = df_CODM['Structure Name']

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_CODM['Appropriation Date']

print("AllocationTimeframeEnd")  # Hardcoded
outdf.AllocationTimeframeEnd = "12/31"

print("AllocationTimeframeStart")  # Hardcoded
outdf.AllocationTimeframeStart = "01/01"

print("AllocationTypeCV")  # Hardcoded
outdf['AllocationTypeCV'] = ''

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_CODM.apply(lambda row: assignBeneficialUseCategory(row['Decreed Uses']), axis=1)

print("CommunityWaterSupplySystem")  # Hardcoded
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")  # Hardcoded
outdf.CropTypeCV = ""

print("CustomerTypeCV")  # Hardcoded
outdf.CustomerTypeCV = ""

print("DataPublicationDate")  # Hardcoded
outdf.DataPublicationDate = "03/02/2020"

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

print("AllocationSDWISIdentifierCV")  # Hardcoded
outdf.AllocationSDWISIdentifierCV = ""

print("WaterAllocationNativeURL")  # Hardcoded
outdf.WaterAllocationNativeURL = ""


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
# Date Noted: 03/02/2020
# Note: Insure single 'AllocationNativeID' entry.
print("Joining outdf duplicates based on AllocationNativeID...")
outdf100 = pd.DataFrame(columns=columns)  # The output dataframe for CSV.
outdf100 = outdf.groupby('AllocationNativeID', sort=False).agg(lambda x: ','.join([str(elem) for elem in (list(set(x)))])).reset_index()


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