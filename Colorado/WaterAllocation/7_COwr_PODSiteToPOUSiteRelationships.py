# Date Updated: 05/25/2021
# Purpose: To extract CO site POD and POU relation information and populate dataframe for WaDEQA 2.0.
# Notes: Uses allocations.csv as input.  Explodes() SiteUUID values, and then groups AllocationNativeID to find POD and POU relation.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/CustomFunctions/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Colorado/WaterAllocation"  # Specific to my machine, will need to change.
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


# Custom Functions
############################################################################
# N/A


# Creating output dataframe (outdf)
############################################################################
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
# drops 'nan rows'
outdf = pd.DataFrame()
outdf['PODSiteUUID'] = dfallo['PODSiteUUID']
outdf['POUSiteUUID'] = dfallo['POUSiteUUID']

outdf = outdf[outdf['PODSiteUUID'] != 'nan'].reset_index(drop=True)
outdf = outdf[outdf['POUSiteUUID'] != 'nan'].reset_index(drop=True)

# create StartDate & EndDate values.
outdf['StartDate'] = "01/01/2021"
outdf['EndDate'] = "12/31/2021"

# Check if dataframe is empty, fill in 1 row if true
if outdf.empty:
    outdf = outdf.append({'StartDate': "01/01/2021", 'EndDate': "12/31/2021"}, ignore_index=True)

#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")

# dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
# dfpurge = dfpurge.assign(ReasonRemoved='')



# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/podsitetopousiterelationships.csv', index=False)

# # Report purged values.
# if(len(dfpurge.index) > 0):
#     dfpurge.to_csv('ProcessedInputData/podsitetopousiterelationships_missing.csv', index=False)

print("Done.")
