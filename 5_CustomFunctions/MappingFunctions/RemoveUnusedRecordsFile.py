# Date Update: 06/13/2023
# Purpose: To remove unused water sources, site, and reporting unit records not found within the main input file. Saves on database space.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Removed Unused records in AllocationsAmount
##################################################################################
##################################################################################
def RemoveUnusedAllocationsAmountRecordsFileFunction(workingDirString):
    # Inputs
    #---------------------------------------------------------------------------------
    print("Reading input csv...")
    workingDir = workingDirString
    os.chdir(workingDir)

    # Input Data - 'WaDE Input' files & 'missing.xlsx' files.
    dfws = pd.read_csv("ProcessedInputData/watersources.csv").replace(np.nan, "")
    dfwspurge = pd.read_csv("ProcessedInputData/watersources_missing.csv").replace(np.nan, "")
    dfs = pd.read_csv("ProcessedInputData/sites.csv").replace(np.nan, "")
    dfspurge = pd.read_csv("ProcessedInputData/sites_missing.csv").replace(np.nan, "")
    dfaa = pd.read_csv("ProcessedInputData/waterallocations.csv").replace(np.nan, "")


    # check length of dfaa
    #---------------------------------------------------------------------------------
    if len(dfaa) == 0:
        print("!!!dfaa IS EMPTY, STOPPING SCRIPT!!!")
        exit()


    # Remove unused sites from sites.csv based on waterallocations.csv information
    #---------------------------------------------------------------------------------
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
    #---------------------------------------------------------------------------------
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
    #---------------------------------------------------------------------------------
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
    #---------------------------------------------------------------------------------
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




# Removed Unused records in Aggregated Amounts
##################################################################################
##################################################################################
def RemoveUnusedAggregatedAmountRecordsFileFunction(workingDirString):
    # Inputs
    # ---------------------------------------------------------------------------------
    print("Reading input csv...")
    workingDir = workingDirString
    os.chdir(workingDir)

    # Input Data - 'WaDE Input' files & 'missing.xlsx' files.
    dfws = pd.read_csv("ProcessedInputData/watersources.csv").replace(np.nan, "")
    dfwspurge = pd.read_csv("ProcessedInputData/watersources_missing.csv").replace(np.nan, "")
    dfru = pd.read_csv("ProcessedInputData/reportingunits.csv").replace(np.nan, "")
    dfrupurge = pd.read_csv("ProcessedInputData/reportingunits_missing.csv").replace(np.nan, "")
    dfag = pd.read_csv("ProcessedInputData/aggregatedamounts.csv").replace(np.nan, "")

    # check length of dfaa
    # ---------------------------------------------------------------------------------
    if len(dfag) == 0:
        print("!!!dfag IS EMPTY, STOPPING SCRIPT!!!")
        exit()

    # Remove unused reporting units from reportingunits.csv based on aggregatedamounts.csv information
    # ---------------------------------------------------------------------------------
    print(f'Length of dfru before removing reporting units: ', len(dfru))
    # explode copy of aggregatedamounts.csv on ReportingUnitUUID
    dfagTemp = dfag.copy()
    dfagTemp = dfagTemp.assign(ReportingUnitUUID=dfagTemp['ReportingUnitUUID'].str.split(',')).explode('ReportingUnitUUID').reset_index(drop=True)

    # create list of & ReportingUnitUUIDs from copy of aggregatedamounts.csv
    dfagReportingUnitUUID_List = dfagTemp['ReportingUnitUUID'].drop_duplicates().to_list()
    dfagReportingUnitUUID_List.sort()

    # use list to add unused records to purge dataframe
    dftemp = dfru[~dfru['ReportingUnitUUID'].isin(dfagReportingUnitUUID_List)].reset_index(drop=True).assign(ReasonRemoved='Unused Reporting Unit Record').reset_index()
    frames = [dfrupurge, dftemp]  # add dataframes here
    dfrupurge = pd.concat(frames).reset_index(drop=True)

    # use list to only save used ReportingUnitUUID records in reportingunits.csv
    dfru = dfru[dfru['ReportingUnitUUID'].isin(dfagReportingUnitUUID_List)].reset_index(drop=True)
    print(f'Length of dfru after removing reporting units: ', len(dfru))

    # Remove unused water source records from aggregatedamounts.csv information
    # ---------------------------------------------------------------------------------
    print(f'Length of dfws before removing reporting units: ', len(dfws))
    # explode copy of aggregatedamounts.csv on ReportingUnitUUID
    dfagTemp = dfag.copy()
    dfagTemp = dfagTemp.assign(WaterSourceUUID=dfagTemp['WaterSourceUUID'].str.split(',')).explode('WaterSourceUUID').reset_index(drop=True)

    # create list of & WaterSourceUUIDs from copy of aggregatedamounts.csv
    dfagWaterSourceUUID_List = dfagTemp['WaterSourceUUID'].drop_duplicates().to_list()
    dfagWaterSourceUUID_List.sort()

    # use list to add unused records to purge dataframe
    dftemp = dfws[~dfws['WaterSourceUUID'].isin(dfagWaterSourceUUID_List)].reset_index(drop=True).assign(ReasonRemoved='Unused Water Source Record').reset_index()
    frames = [dfwspurge, dftemp]  # add dataframes here
    dfwspurge = pd.concat(frames).reset_index(drop=True)

    # use list to only save used WaterSourceUUID records in watersources.csv
    dfws = dfws[dfws['WaterSourceUUID'].isin(dfagWaterSourceUUID_List)].reset_index(drop=True)
    print(f'Length of dfws after removing reporting units: ', len(dfws))

    # Remove WaDEUUID field WaDE input file (only needed for purge info).
    # ---------------------------------------------------------------------------------
    try:
        dfws = dfws.drop(['WaDEUUID'], axis=1)
    except:
        print('no ws WaDEUUID')

    try:
        dfru = dfru.drop(['WaDEUUID'], axis=1)
    except:
        print('no ru WaDEUUID')

    try:
        dfag = dfag.drop(['WaDEUUID'], axis=1)
    except:
        print('no ag WaDEUUID')

    # Export to new csv
    # ---------------------------------------------------------------------------------
    print(
        "Export Files - watersource.csv, watersource_missing.csv, reportingunits.csv, reportingunits_missing.csv, aggregatedamounts.csv, aggregatedamounts_missing.csv")

    # watersources info
    dfws.to_csv('ProcessedInputData/watersources.csv', index=False)
    dfwspurge.to_csv('ProcessedInputData/watersources_missing.csv', index=False)

    # reportingunits info
    dfru.to_csv('ProcessedInputData/reportingunits.csv', index=False)
    dfrupurge.to_csv('ProcessedInputData/reportingunits_missing.csv', index=False)

    # aggregatedamounts info
    dfag.to_csv('ProcessedInputData/aggregatedamounts.csv', index=False)

    print("Done")




# Removed Unused records in SiteSpecificAmounts
##################################################################################
##################################################################################
def RemoveUnusedSiteSpecificAmountsRecordsFileFunction(workingDirString):
    # Inputs
    #---------------------------------------------------------------------------------
    print("Reading input csv...")
    workingDir = workingDirString
    os.chdir(workingDir)

    # Input Data - 'WaDE Input' files & 'missing.xlsx' files.
    dfws = pd.read_csv("ProcessedInputData/watersources.csv").replace(np.nan, "")
    dfwspurge = pd.read_csv("ProcessedInputData/watersources_missing.csv").replace(np.nan, "")
    dfs = pd.read_csv("ProcessedInputData/sites.csv").replace(np.nan, "")
    dfspurge = pd.read_csv("ProcessedInputData/sites_missing.csv").replace(np.nan, "")
    dfsa = pd.read_csv("ProcessedInputData/sitespecificamounts.csv").replace(np.nan, "")


    # check length of dfaa
    #---------------------------------------------------------------------------------
    if len(dfsa) == 0:
        print("!!!dfsa IS EMPTY, STOPPING SCRIPT!!!")
        exit()


    # Remove unused sites from sites.csv based on waterallocations.csv information
    #---------------------------------------------------------------------------------
    print(f'Length of dfs before removing sites: ', len(dfs))
    # explode copy of waterallocations.csv on SiteUUID
    dfsaTemp = dfsa.copy()
    dfsaTemp = dfsaTemp.assign(SiteUUID=dfsaTemp['SiteUUID'].str.split(',')).explode('SiteUUID').reset_index(drop=True)

    # create list of & SiteUUIDs from copy of waterallocations.csv
    dfsaSiteUUID_List = dfsaTemp['SiteUUID'].drop_duplicates().to_list()
    dfsaSiteUUID_List.sort()

    # use list to add unused records to purge dataframe
    dftemp = dfs[~dfs['SiteUUID'].isin(dfsaSiteUUID_List)].reset_index(drop=True).assign(ReasonRemoved='Unused Site Record').reset_index()
    frames = [dfspurge, dftemp]  # add dataframes here
    dfspurge = pd.concat(frames).reset_index(drop=True)

    # use list to only save used SiteUUID records in site.csv
    dfs = dfs[dfs['SiteUUID'].isin(dfsaSiteUUID_List)].reset_index(drop=True)
    print(f'Length of dfs after removing sites: ', len(dfs))


    # Remove unused water source records from sites.csv information
    #---------------------------------------------------------------------------------
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
    #---------------------------------------------------------------------------------
    try:
        dfws = dfws.drop(['WaDEUUID'], axis=1)
    except:
        print('no ws WaDEUUID')

    try:
        dfs = dfs.drop(['WaDEUUID'], axis=1)
    except:
        print('no s WaDEUUID')

    try:
        dfsa = dfsa.drop(['WaDEUUID'], axis=1)
    except:
        print('no aa WaDEUUID')


    # Export to new csv
    #---------------------------------------------------------------------------------
    print("Export Files - watersource.csv, watersource_missing.csv, sites.csv, sites_missing.csv, sitespecificamounts.csv, sitespecificamounts_missing.csv")

    # watersources info
    dfws.to_csv('ProcessedInputData/watersources.csv', index=False)
    dfwspurge.to_csv('ProcessedInputData/watersources_missing.csv', index=False)

    # sites info
    dfs.to_csv('ProcessedInputData/sites.csv', index=False)
    dfspurge.to_csv('ProcessedInputData/sites_missing.csv', index=False)

    # sitespecificamounts info
    dfsa.to_csv('ProcessedInputData/sitespecificamounts.csv', index=False)

    print("Done")