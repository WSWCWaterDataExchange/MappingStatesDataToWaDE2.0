# Date Updated: 05/25/2021
# Purpose: To extract UT site POD and POU relation information and populate dataframe for WaDEQA 2.0.
# Notes: N/A


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/SiteSpecificAmounts"  # Specific to my machine, will need to change.
os.chdir(workingDir)

# Sites
siteColumns = ["SiteUUID", "PODorPOUSite"]
sitesInput = "ProcessedInputData/sites.csv"
dfsites = pd.read_csv(sitesInput, usecols=siteColumns)
dfPOD = dfsites[dfsites['PODorPOUSite'] == "POD"].reset_index(drop=True)
dfPOD['PODSiteUUID'] = dfPOD['SiteUUID']
dfPOU = dfsites[dfsites['PODorPOUSite'] == "POU"].reset_index(drop=True)
dfPOU['POUSiteUUID'] = dfPOU['SiteUUID']

# Sitespecificamounts
recordColumns = ["SiteUUID", "CommunityWaterSupplySystem"]
recordInput = "ProcessedInputData/sitespecificamounts.csv"
dfrecord = pd.read_csv(recordInput, usecols=recordColumns)


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")

# Explode allocation by SiteUUID
dfrecord = dfrecord.assign(SiteUUID=dfrecord['SiteUUID'].str.split(',')).explode('SiteUUID').reset_index(drop=True)

# Merging dataframes into one, using left-join.
dfrecord = pd.merge(dfrecord, dfPOD[['SiteUUID', 'PODSiteUUID', 'PODorPOUSite']], on='SiteUUID', how='left')
dfrecord = pd.merge(dfrecord, dfPOU[['SiteUUID', 'POUSiteUUID', 'PODorPOUSite']], on='SiteUUID', how='left')

# group by CommunityWaterSupplySystem
dfrecord = dfrecord.groupby(['CommunityWaterSupplySystem']).agg(lambda x: ",".join([str(elem) for elem in (list(set(x))) if elem!=""])).replace(np.nan, "").reset_index()

# explode by both PODSiteUUID, then by POUSiteUUID
dfrecord = dfrecord.assign(PODSiteUUID=dfrecord['PODSiteUUID'].str.split(',')).explode('PODSiteUUID').reset_index(drop=True)
dfrecord = dfrecord.assign(POUSiteUUID=dfrecord['POUSiteUUID'].str.split(',')).explode('POUSiteUUID').reset_index(drop=True)

# create out DataFrame
outdf = pd.DataFrame()
outdf['PODSiteUUID'] = dfrecord['PODSiteUUID']
outdf['POUSiteUUID'] = dfrecord['POUSiteUUID']

# drops 'nan rows'
outdf = outdf[outdf['PODSiteUUID'] != 'nan'].reset_index(drop=True)
outdf = outdf[outdf['POUSiteUUID'] != 'nan'].reset_index(drop=True)

# create StartDate & EndDate values.
outdf['StartDate'] = "01/01/2021"
outdf['EndDate'] = "12/31/2021"


# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")

# The working output DataFrame for WaDE 2.0 input.
# Check if dataframe is empty, fill in 1 row if true
if not outdf.empty:
    outdf.to_csv('ProcessedInputData/podsitetopousiterelationships.csv', index=False)

print("Done.")
