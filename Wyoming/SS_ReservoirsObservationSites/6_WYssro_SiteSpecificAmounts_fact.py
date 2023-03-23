# Date Update: 03/22/2023
# Purpose: To create WY site specific reservoir and observation site amount use information and population dataframe WaDE_QA 2.0.
# Notes:  N/A


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

# Test WaDE Data for any Errors
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/ErrorCheckCode")
import TestErrorFunctionsFile


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "G:/Shared drives/WaDE Data/Wyoming/SS_ReservoirsObservationSites"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_wySSROMain.zip"
df_DM = pd.read_csv(M_fileInput, compression='zip') # use zip file

# Input Data - 'WaDE Input' files & 'missing.xlsx' files.
dfv = pd.read_csv("ProcessedInputData/variables.csv").replace(np.nan, "")
dfws = pd.read_csv("ProcessedInputData/watersources.csv").replace(np.nan, "")
dfwspurge = pd.read_csv("ProcessedInputData/watersources_missing.csv").replace(np.nan, "")
dfs = pd.read_csv("ProcessedInputData/sites.csv").replace(np.nan, "")
dfspurge = pd.read_csv("ProcessedInputData/sites_missing.csv").replace(np.nan, "")

# WaDE columns
SpecificAmountsColumnsList = GetColumnsFile.GetSiteSpecificAmountsColumnsFunction()


# Custom Functions
############################################################################

# For creating VariableSpecificUUID
VariableSpecificUUIDdict = pd.Series(dfv.VariableSpecificUUID.values, index=dfv.VariableCV).to_dict()
def retrieveVariableSpecificUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = VariableSpecificUUIDdict[String1]
        except:
            outList = ''
    return outList

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


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=SpecificAmountsColumnsList)  # The output dataframe

print("MethodUUID")
outdf['MethodUUID'] = "WYssro_M1"

print("VariableSpecificUUID") # pass in a VariableCV value
outdf['VariableSpecificUUID'] = df_DM.apply(lambda row: retrieveVariableSpecificUUID(row['in_VariableCV']), axis=1)

print("OrganizationUUID")
outdf['OrganizationUUID'] = "WYssro_O1"

print("WaterSourceUUID")
outdf['WaterSourceUUID'] = "WYssro_WS1"

print("SiteUUID") # Using SiteNativeID
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['in_SiteNativeID']), axis=1)

print("Amount")
outdf['Amount'] = df_DM['in_Amount'].astype(float)  # See pre-processing.

print('AllocationCropDutyAmount')
outdf['AllocationCropDutyAmount'] = ""

print("AssociatedNativeAllocationIDs")
outdf['AssociatedNativeAllocationIDs'] = ""

print('BeneficialUseCategory')
outdf['BeneficialUseCategory'] = df_DM['in_BeneficialUseCategory']  # See pre-processing.

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySystem'] = ""

print("CropTypeCV")
outdf['CropTypeCV'] = ""

print("CustomerTypeCV")
outdf['CustomerTypeCV'] = ""

print("DataPublicationDate")
outdf['DataPublicationDate'] = "03/22/2023"

print("DataPublicationDOI")
outdf['DataPublicationDOI'] = ""

print("Geometry")
outdf['Geometry'] = ""

print("IrrigatedAcreage")
outdf['IrrigatedAcreage'] = ""

print("IrrigationMethodCV")
outdf['IrrigationMethodCV'] = ""

print("PopulationServed")
outdf['PopulationServed'] = ""

print("PowerGeneratedGWh")
outdf['PowerGeneratedGWh'] = ""

print("PowerType")
outdf['PowerType'] = ""

print("PrimaryUseCategory")
outdf['PrimaryUseCategory'] = df_DM['in_BeneficialUseCategory']  # See pre-processing.

print("ReportYearCV")
outdf['ReportYearCV'] = df_DM['in_ReportYearCV'].astype(int)

print("SDWISIdentifier")
outdf['SDWISIdentifier'] = ""

print("TimeframeEnd")
outdf['TimeframeEnd'] = df_DM['in_TimeframeEnd']  # See pre-processing.

print("TimeframeStart")
outdf['TimeframeStart'] = df_DM['in_TimeframeStart']  # See pre-processing.

print("Adding Data Assessment UUID")
outdf['WaDEUUID'] = df_DM['WaDEUUID']

print("Resetting Index")
outdf.reset_index()


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

outdf = outdf.replace(np.nan, "").drop_duplicates().reset_index(drop=True)


# Error Checking Each Field
############################################################################
print("Error checking each field. Purging bad inputs.")
dfpurge = pd.DataFrame(columns=SpecificAmountsColumnsList) # Purge DataFrame to hold removed elements
dfpurge['ReasonRemoved'] = ""
dfpurge['IncompleteField'] = ""
outdf, dfpurge = TestErrorFunctionsFile.SiteSpecificAmountsTestErrorFunctions(outdf, dfpurge)
print(f'Length of outdf DataFrame: ', len(outdf))
print(f'Length of dfpurge DataFrame: ', len(dfpurge))


# Remove unused sites from sites.csv based on waterallocations.csv information
############################################################################
print(f'Length of dfs before removing sites: ', len(dfs))
# explode copy of waterallocations.csv on SiteUUID
outdfTemp = outdf.copy()
outdfTemp = outdfTemp.assign(SiteUUID=outdfTemp['SiteUUID'].str.split(',')).explode('SiteUUID').reset_index(drop=True)

# create list of & SiteUUIDs from copy of waterallocations.csv
dfaaSiteUUID_List = outdfTemp['SiteUUID'].drop_duplicates().to_list()
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
print("Export Files - watersource.csv, watersource_missing.csv, sites.csv, sites_missing.csv, sitespecificamounts.csv, sitespecificamounts_missing.csv")

# watersources info
dfws.to_csv('ProcessedInputData/watersources.csv', index=False)
dfwspurge.to_csv('ProcessedInputData/watersources_missing.csv', index=False)

# sites info
dfs.to_csv('ProcessedInputData/sites.csv', index=False)
dfspurge.to_csv('ProcessedInputData/sites_missing.csv', index=False)

# sitespecificamounts info
outdf.to_csv('ProcessedInputData/sitespecificamounts.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0): print(f'...', len(dfpurge),  ' records removed.')
dfpurge.insert(0, 'ReasonRemoved', dfpurge.pop('ReasonRemoved'))
dfpurge.to_csv('ProcessedInputData/sitespecificamounts_missing.csv', index=False)

print("Done")
