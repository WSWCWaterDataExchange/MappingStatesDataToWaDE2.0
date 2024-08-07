# Date Created: 04/18//2023
# Purpose: To extract site POD and POU relation information and populate dataframe for WaDE


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd
import sys
import re


# Create POD to POU relationship within AllocationsAmount
############################################################################
def PODToPOUWaterRightRelationshipsFunction(workingDirString):
    # Inputs
    ############################################################################
    print("Reading input csv...")
    workingDir = workingDirString
    os.chdir(workingDir)

    # Sites
    siteColumns = ["SiteUUID", "PODorPOUSite"]
    sitesInput = "ProcessedInputData/sites.csv"
    dfsites = pd.read_csv(sitesInput, usecols=siteColumns)
    dfPOD = dfsites[dfsites['PODorPOUSite'] == "POD"].reset_index(drop=True)
    dfPOD['PODSiteUUID'] = dfPOD['SiteUUID']
    dfPOU = dfsites[dfsites['PODorPOUSite'] == "POU"].reset_index(drop=True)
    dfPOU['POUSiteUUID'] = dfPOU['SiteUUID']

    # AllocationAmounts_facts
    alocationColumns = ["SiteUUID", "AllocationNativeID"]
    allocationInput = "ProcessedInputData/waterallocations.csv"
    dfallo = pd.read_csv(allocationInput, usecols=alocationColumns)

    print("Populating dataframe...")

    # Explode allocation by SiteUUID
    dfallo = dfallo.assign(SiteUUID=dfallo['SiteUUID'].str.split(',')).explode('SiteUUID').reset_index(drop=True)

    # Merging dataframes into one, using left-join.
    dfallo = pd.merge(dfallo, dfPOD[['SiteUUID', 'PODSiteUUID', 'PODorPOUSite']], on='SiteUUID', how='left')
    dfallo = pd.merge(dfallo, dfPOU[['SiteUUID', 'POUSiteUUID', 'PODorPOUSite']], on='SiteUUID', how='left')

    # group by AllocationNativeID
    dfallo = dfallo.groupby(['AllocationNativeID']).agg(lambda x: ",".join([str(elem) for elem in (list(set(x))) if elem!=""])).replace(np.nan, "").reset_index()

    # explode by both PODSiteUUID, then by POUSiteUUID
    dfallo = dfallo.assign(PODSiteUUID=dfallo['PODSiteUUID'].str.split(',')).explode('PODSiteUUID').reset_index(drop=True)
    dfallo = dfallo.assign(POUSiteUUID=dfallo['POUSiteUUID'].str.split(',')).explode('POUSiteUUID').reset_index(drop=True)

    # create out DataFrame
    outdf = pd.DataFrame()
    outdf['PODSiteUUID'] = dfallo['PODSiteUUID']
    outdf['POUSiteUUID'] = dfallo['POUSiteUUID']

    # drops 'nan rows'
    outdf = outdf[outdf['PODSiteUUID'] != 'nan'].reset_index(drop=True)
    outdf = outdf[outdf['POUSiteUUID'] != 'nan'].reset_index(drop=True)

    # create StartDate & EndDate values.
    outdf['StartDate'] = "01/01/2023"
    outdf['EndDate'] = "12/31/2023"


    # Export to new csv
    ############################################################################
    print("Exporting dataframe outdf to csv...")

    # The working output DataFrame for WaDE 2.0 input.
    # Check if dataframe is empty, print if false.
    if not outdf.empty:
        outdf.to_csv('ProcessedInputData/podsitetopousiterelationships.csv', index=False)

    print("Done")




# Create POD to POU relationship within SiteSpecificAmounts
############################################################################
def PODToPOUSiteSpecificRelationshipsFunction(workingDirString):
    # Inputs
    ############################################################################
    print("Reading input csv...")
    workingDir = workingDirString
    os.chdir(workingDir)

    # Sites
    siteColumns = ["SiteUUID", "PODorPOUSite"]
    sitesInput = "ProcessedInputData/sites.csv"
    dfsites = pd.read_csv(sitesInput, usecols=siteColumns)
    dfPOD = dfsites[dfsites['PODorPOUSite'] == "POD"].reset_index(drop=True)
    dfPOD['PODSiteUUID'] = dfPOD['SiteUUID']
    dfPOU = dfsites[dfsites['PODorPOUSite'] == "POU"].reset_index(drop=True)
    dfPOU['POUSiteUUID'] = dfPOU['SiteUUID']

    # SiteSpecificAmounts
    siteSpecificColumns = ["SiteUUID", "CommunityWaterSupplySystem"]
    siteSpecificnput = "ProcessedInputData/sitespecificamounts.csv"
    dfsa = pd.read_csv(siteSpecificnput, usecols=siteSpecificColumns)

    print("Populating dataframe...")

    # Explode SiteSpecificAmounts by SiteUUID
    dfsa = dfsa.assign(SiteUUID=dfsa['SiteUUID'].str.split(',')).explode('SiteUUID').reset_index(drop=True)

    # Merging dataframes into one, using left-join.
    dfsa = pd.merge(dfsa, dfPOD[['SiteUUID', 'PODSiteUUID', 'PODorPOUSite']], on='SiteUUID', how='left')
    dfsa = pd.merge(dfsa, dfPOU[['SiteUUID', 'POUSiteUUID', 'PODorPOUSite']], on='SiteUUID', how='left')

    # group by CommunityWaterSupplySystem
    dfsa = dfsa.groupby(['CommunityWaterSupplySystem']).agg(lambda x: ",".join([str(elem) for elem in (list(set(x))) if elem!=""])).replace(np.nan, "").reset_index()

    # explode by both PODSiteUUID, then by POUSiteUUID
    dfsa = dfsa.assign(PODSiteUUID=dfsa['PODSiteUUID'].str.split(',')).explode('PODSiteUUID').reset_index(drop=True)
    dfsa = dfsa.assign(POUSiteUUID=dfsa['POUSiteUUID'].str.split(',')).explode('POUSiteUUID').reset_index(drop=True)

    # create out DataFrame
    outdf = pd.DataFrame()
    outdf['PODSiteUUID'] = dfsa['PODSiteUUID']
    outdf['POUSiteUUID'] = dfsa['POUSiteUUID']

    # drops 'nan rows'
    outdf = outdf[outdf['PODSiteUUID'] != 'nan'].reset_index(drop=True)
    outdf = outdf[outdf['POUSiteUUID'] != 'nan'].reset_index(drop=True)

    # create StartDate & EndDate values.
    outdf['StartDate'] = "01/01/2024"
    outdf['EndDate'] = "12/31/2024"


    # Export to new csv
    ############################################################################
    print("Exporting dataframe outdf to csv...")

    # The working output DataFrame for WaDE 2.0 input.
    # Check if dataframe is empty, print if false.
    if not outdf.empty:
        outdf.to_csv('ProcessedInputData/podsitetopousiterelationships.csv', index=False)

    print("Done")