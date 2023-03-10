# Date Update: 03/02/2023
# Purpose: To extract CA water right information and populate dataframe for WaDE_QA 2.0.
#         1) Simple creation of working dataframe (df), with output dataframe (outdf).
#         2) Drop all nulls before combining duplicate rows on NativeID.
#         3) Remove unused sites and watersource records.
#         4) Remove WaDEUUID field (for purge files only).


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd

# Custom Libraries
############################################################################
import sys
# columns
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/MappingFunctions")
import GetColumnsFile

# Owner Classification Fix
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/OwnerClassification")
import OwnerClassificationField

# Assign Primary Use Category fix
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/AssignPrimaryUseCategory")
import AssignPrimaryUseCategory

# Test WaDE Data for any Errors
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/ErrorCheckCode")
import TestErrorFunctionsFile


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "G:/Shared drives/WaDE Data/California/WaterAllocation"
os.chdir(workingDir)
DM_fileInput = "RawinputData/Pwr_CAMain.csv"
df_DM = pd.read_csv(DM_fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.

# method_fileInput = "ProcessedInputData/methods.csv"
# variables_fileInput = "ProcessedInputData/variables.csv"
# df_method = pd.read_csv(method_fileInput)  # Method dataframe
# df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe

# Input Data - 'WaDE Input' files & 'missing.xlsx' files.
dfws = pd.read_csv("ProcessedInputData/watersources.csv").replace(np.nan, "")
dfwspurge = pd.read_excel("ProcessedInputData/watersources_missing.xlsx").replace(np.nan, "")
dfs = pd.read_csv("ProcessedInputData/sites.csv" ).replace(np.nan, "")
dfspurge = pd.read_excel("ProcessedInputData/sites_missing.xlsx").replace(np.nan, "")

# WaDE columns
AllocationAmountsColumnsList = GetColumnsFile.GetAllocationAmountsColumnsFunction()

# Custom Functions
############################################################################

# For creating SiteUUID
SitUUIDdict = pd.Series(dfs.SiteUUID.values, index=dfs.SiteNativeID).to_dict()
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

# For creating AllocationUUID
def assignAllocationUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "CAwr_WR" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(columns=AllocationAmountsColumnsList, index=df_DM.index)  # The output dataframe

print("MethodUUID")
outdf['MethodUUID'] = "CAwr_M1"

print("OrganizationUUID")
outdf['OrganizationUUID'] = "CAwr_O1"

print("SiteUUID")
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['in_SiteNativeID']), axis=1)

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = df_DM['in_VariableSpecificUUID']

print("AllocationApplicationDate")
outdf['AllocationApplicationDate'] = df_DM['in_AllocationApplicationDate']

print("AllocationAssociatedConsumptiveUseSiteIDs")
outdf['AllocationAssociatedConsumptiveUseSiteIDs'] = ""

print("AllocationAssociatedWithdrawalSiteIDs")
outdf['AllocationAssociatedWithdrawalSiteIDs'] = ""

print("AllocationBasisCV")
outdf['AllocationBasisCV'] = ""

print("AllocationChangeApplicationIndicator")
outdf['AllocationChangeApplicationIndicator'] = ""

print("AllocationCommunityWaterSupplySystem")
outdf['AllocationCommunityWaterSupplySystem'] = ""

print("AllocationCropDutyAmount")
outdf['AllocationCropDutyAmount'] = ""

print("AllocationExpirationDate")
outdf['AllocationExpirationDate'] = ""

print("AllocationFlow_CFS")
outdf['AllocationFlow_CFS'] = df_DM['in_AllocationFlow_CFS'].astype(float)

print("AllocationLegalStatusCV")
outdf['AllocationLegalStatusCV'] = df_DM['in_AllocationLegalStatusCV']

print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
outdf['AllocationNativeID'] = df_DM['in_AllocationNativeID'].astype(str)

print("AllocationOwner")
outdf['AllocationOwner'] =  df_DM['in_AllocationOwner']

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df_DM['in_AllocationPriorityDate']

print("AllocationSDWISIdentifierCV")
outdf['AllocationSDWISIdentifierCV'] = ""

print("AllocationTimeframeEnd")
outdf['AllocationTimeframeEnd'] = df_DM['in_AllocationTimeframeEnd']

print("AllocationTimeframeStart")
outdf['AllocationTimeframeStart'] = df_DM['in_AllocationTimeframeStart']

print("AllocationTypeCV")
outdf['AllocationTypeCV'] = df_DM['in_AllocationTypeCV']

print("AllocationVolume_AF")
outdf['AllocationVolume_AF'] = df_DM['in_AllocationVolume_AF'].astype(float)

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_DM['in_BeneficialUseCategory']

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySystem'] = ""

print("CropTypeCV")
outdf['CropTypeCV'] = ""

print("CustomerTypeCV")
outdf['CustomerTypeCV'] = ""

print("DataPublicationDate")
outdf['DataPublicationDate'] = "03/02/2023"

print("DataPublicationDOI")
outdf['DataPublicationDOI'] = ""

print("ExemptOfVolumeFlowPriority")
outdf['ExemptOfVolumeFlowPriority'] = df_DM['in_ExemptOfVolumeFlowPriority']

print("GeneratedPowerCapacityMW")
outdf['GeneratedPowerCapacityMW'] = ""

print("IrrigatedAcreage")
outdf['IrrigatedAcreage'] = ""

print("IrrigationMethodCV")
outdf['IrrigationMethodCV'] = ""

print("LegacyAllocationIDs")
outdf['LegacyAllocationIDs'] = ""

#####################################
print("OwnerClassificationCV")
# Temp solution to populate OwnerClassificationCV field.
outdf['OwnerClassificationCV'] = outdf.apply(lambda row: OwnerClassificationField.CreateOwnerClassification(row['AllocationOwner']), axis=1)
#####################################

print("PopulationServed")
outdf['PopulationServed'] = ""

print("PowerType")
outdf['PowerType'] = ""

print("PrimaryBeneficialUseCategory")
outdf['PrimaryBeneficialUseCategory'] = ""

print("WaterAllocationNativeURL")
#outdf['WaterAllocationNativeURL'] = df_DM['in_WaterAllocationNativeURL']  #too long of entry

print("Adding Data Assessment UUID")
outdf['WaDEUUID'] = df_DM['WaDEUUID']

print("Resetting Index")
outdf.reset_index()

print("Joining outdf duplicates based on key fields...")
outdf = outdf.replace(np.nan, "")  # Replaces NaN values with blank.
groupbyList = ['AllocationNativeID', 'AllocationFlow_CFS', 'AllocationVolume_AF']
outdf = outdf.groupby(groupbyList).agg(lambda x: ','.join([str(elem) for elem in (list(set(x))) if elem!=''])).replace(np.nan, "").reset_index()
outdf = outdf[AllocationAmountsColumnsList]  # reorder the dataframe's columns based on columnslist


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# Note: OwnerClassificationCV can only accept 1 entry at this time. Error due to above merge / we don't allow multiple OwnerClassificationCV.
def tempfixOCSV(val):
    valList = val.split(",") # convert string to list
    valList.sort() # sort list alphabetically
    if ("In Review" in valList):
        valList.remove("In Review") # check if "In Review"  If true, remove.
        valList.append("In Review") # Append back in "In Review" to end of list.
    result = valList[0] # return only first value in list.
    return result
outdf['OwnerClassificationCV']  = outdf.apply(lambda row: tempfixOCSV(row['OwnerClassificationCV']), axis=1)

# Temp solution to populate PrimaryBeneficialUseCategory field.
# Use Custom import file
outdf['PrimaryBeneficialUseCategory'] = outdf.apply(lambda row: AssignPrimaryUseCategory.retrievePrimaryUseCategory(row['BeneficialUseCategory']), axis=1)


#Error Checking Each Field
############################################################################
print("Error checking each field. Purging bad inputs.")
dfpurge = pd.DataFrame(columns=AllocationAmountsColumnsList) # Purge DataFrame to hold removed elements
dfpurge['ReasonRemoved'] = ""
dfpurge['IncompleteField'] = ""
outdf, dfpurge = TestErrorFunctionsFile.AllocationAmountTestErrorFunctions(outdf, dfpurge)
print(f'Length of outdf DataFrame: ', len(outdf))
print(f'Length of dfpurge DataFrame: ', len(dfpurge))


# Assign AllocationUUID value
############################################################################
print("Assign AllocationUUID") # has to be one of the last.
outdf = outdf.reset_index(drop=True)
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['AllocationUUID'] = dftemp.apply(lambda row: assignAllocationUUID(row['Count']), axis=1)

# Error check AllocationUUID
outdf, dfpurge = TestErrorFunctionsFile.AllocationUUID_AA_Check(outdf, dfpurge)


# Remove unused sites from sites.csv based on waterallocations.csv information
############################################################################
print(f'Length of dfs before removing sites: ', len(dfs))
# explode copy of waterallocations.csv on SiteUUID
dfaaTemp = outdf.copy()
dfaaTemp = dfaaTemp.assign(SiteUUID=dfaaTemp['SiteUUID'].str.split(',')).explode('SiteUUID').reset_index(drop=True)

# create list of & SiteUUIDs from copy of waterallocations.csv
dfaaSiteUUID_List = dfaaTemp['SiteUUID'].drop_duplicates().to_list()
dfaaSiteUUID_List.sort()

# use lit to add unused records to purge dataframe
dftemp = dfs[~dfs['SiteUUID'].isin(dfaaSiteUUID_List)].reset_index(drop=True).assign(ReasonRemoved='Unused Site Record').reset_index()
frames = [dfspurge, dftemp] # add dataframes here
dfspurge = pd.concat(frames).reset_index(drop=True)

# use list to only save used SiteUUID records in site.csv
dfs = dfs[dfs['SiteUUID'].isin(dfaaSiteUUID_List)].reset_index(drop=True)

print(f'Length of dfs after removing sites: ', len(dfs))


# Remove unused water source records from sites.csv information
############################################################################
print(f'Length of dfws before removing water sources: ', len(dfws))
# explode copy of sites.csv on WaterSourceUUID
dfsTemp = dfs.copy()
dfsTemp = dfsTemp.assign(WaterSourceUUIDs=dfsTemp['WaterSourceUUIDs'].str.split(',')).explode('WaterSourceUUIDs').reset_index(drop=True)

# create list of & WaterSourceUUID from copy of sites.csv
dfsWaterSourceUUID_List = dfsTemp['WaterSourceUUIDs'].drop_duplicates().to_list()
dfsWaterSourceUUID_List.sort()

# use lit to add unused records to purge dataframe
dftemp = dfws[~dfws['WaterSourceUUID'].isin(dfsWaterSourceUUID_List)].reset_index(drop=True).assign(ReasonRemoved='Unused WaterSource Record').reset_index()
frames = [dfwspurge, dftemp] # add dataframes here
dfwspurge = pd.concat(frames).reset_index(drop=True)

# use list to only save used SiteUUID records in site.csv
dfws = dfws[dfws['WaterSourceUUID'].isin(dfsWaterSourceUUID_List)].reset_index(drop=True)

print(f'Length of dfws after removing water sources: ', len(dfws))


# Remove WaDEUUID field WaDE input file (only needed for purge info).
############################################################################
try: dfws = dfws.drop(['WaDEUUID'], axis=1)
except: print('no ws WaDEUUID')

try: dfs = dfs.drop(['WaDEUUID'], axis=1)
except: print('no s WaDEUUID')

try: outdf = outdf.drop(['WaDEUUID'], axis=1)
except: print('no aa WaDEUUID')


# Export to new csv
############################################################################
print("Export Files - watersource.csv, watersource_missing.xlsx, sites.csv, sites_missing.xlsx, waterallocations.csv, waterallocations_missing.xlsx")

# watersources info
dfws.to_csv('ProcessedInputData/watersources.csv', index=False)
dfwspurge.to_excel('ProcessedInputData/watersources_missing.xlsx', index=False, freeze_panes=(1,1))

# sites info
dfs.to_csv('ProcessedInputData/sites.csv', index=False)
dfspurge.to_excel('ProcessedInputData/sites_missing.xlsx', index=False, freeze_panes=(1,1))

# waterallocations info
outdf.to_csv('ProcessedInputData/waterallocations.csv', index=False)
# Report purged values.
if(len(dfpurge.index) > 0): print(f'...', len(dfpurge),  ' records removed.')
dfpurge.insert(0, 'ReasonRemoved', dfpurge.pop('ReasonRemoved'))
dfpurge.to_excel('ProcessedInputData/waterallocations_missing.xlsx', index=False, freeze_panes=(1,1))

print("Done")