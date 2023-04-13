# Date Update: 04/12/2023
# Purpose: To remove unused water sources and site records not found within the allocationamounts input file. Saves on database space.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Create File Function
############################################################################
def RemoveUnusedRecordsFileFunction(varSTName):
    # Inputs
    ############################################################################
    print("Reading input csv...")
    workingDir = "G:/Shared drives/WaDE Data/" + varSTName + "/WaterAllocation"
    os.chdir(workingDir)

    # Input Data - 'WaDE Input' files & 'missing.xlsx' files.
    dfws = pd.read_csv("ProcessedInputData/watersources.csv").replace(np.nan, "")
    dfwspurge = pd.read_csv("ProcessedInputData/watersources_missing.csv").replace(np.nan, "")
    dfs = pd.read_csv("ProcessedInputData/sites.csv").replace(np.nan, "")
    dfspurge = pd.read_csv("ProcessedInputData/sites_missing.csv").replace(np.nan, "")
    dfaa = pd.read_csv("ProcessedInputData/waterallocations.csv").replace(np.nan, "")


    # check length of dfaa
    ############################################################################
    if len(dfaa) == 0:
        print("!!!dfaa IS EMPTY, STOPPING SCRIPT!!!")
        exit()


    # Remove unused sites from sites.csv based on waterallocations.csv information
    ############################################################################
    print(f'Length of dfs before removing sites: ', len(dfs))
    # explode copy of waterallocations.csv on SiteUUID
    dfaaTemp = dfaa.copy()
    dfaaTemp = dfaaTemp.assign(SiteUUID=dfaaTemp['SiteUUID'].str.split(',')).explode('SiteUUID').reset_index(drop=True)

    # create list of & SiteUUIDs from copy of waterallocations.csv
    dfaaSiteUUID_List = dfaaTemp['SiteUUID'].drop_duplicates().to_list()
    dfaaSiteUUID_List.sort()

    # use list to add unused records to purge dataframe
    dftemp = dfs[~dfs['SiteUUID'].isin(dfaaSiteUUID_List)].reset_index(drop=True).assign(ReasonRemoved='Unused Site Record').reset_index()
    frames = [dfspurge, dftemp]  # add dataframes here
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
    frames = [dfwspurge, dftemp]  # add dataframes here
    dfwspurge = pd.concat(frames).reset_index(drop=True)

    # use list to only save used SiteUUID records in site.csv
    dfws = dfws[dfws['WaterSourceUUID'].isin(dfsWaterSourceUUID_List)].reset_index(drop=True)
    print(f'Length of dfws after removing water sources: ', len(dfws))


    # Remove WaDEUUID field WaDE input file (only needed for purge info).
    ############################################################################
    try:
        dfws = dfws.drop(['WaDEUUID'], axis=1)
    except:
        print('no ws WaDEUUID')

    try:
        dfs = dfs.drop(['WaDEUUID'], axis=1)
    except:
        print('no s WaDEUUID')

    try:
        dfaa = dfaa.drop(['WaDEUUID'], axis=1)
    except:
        print('no aa WaDEUUID')


    # Export to new csv
    ############################################################################
    print("Export Files - watersource.csv, watersource_missing.csv, sites.csv, sites_missing.csv, waterallocations.csv, waterallocations_missing.csv")

    # watersources info
    dfws.to_csv('ProcessedInputData/watersources.csv', index=False)
    dfwspurge.to_csv('ProcessedInputData/watersources_missing.csv', index=False)

    # sites info
    dfs.to_csv('ProcessedInputData/sites.csv', index=False)
    dfspurge.to_csv('ProcessedInputData/sites_missing.csv', index=False)

    # waterallocations info
    dfaa.to_csv('ProcessedInputData/waterallocations.csv', index=False)

    print("Done")

