#Last Updated: 09/15/2021
#Author: Ryan James (WSWC)
#Purpose: To create MT site POD and POU relation information and populate dataframe for WaDEQA 2.0.
# Notes:    1) data primary comes from records data.  We want the relationship based on a physical connection, temporal connection, and similar amount values.
#           2) read in records, remove unnecessary columns.
#           3) Attach PODorPOUSite value from sites.csv based on SiteUUID value.
#           4) Split into two dataframes: POD and POUs
#           5) look for matching rows / values between POD and POU dataframe.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Montana/SiteSpecificAmounts"  # Specific to my machine, will need to change.
os.chdir(workingDir)

# Sites
sitesInput = "ProcessedInputData/sites.csv"
dfsites = pd.read_csv(sitesInput)

# Sitespecificamounts
recordInput = "ProcessedInputData/sitespecificamounts.csv"
dfrecord = pd.read_csv(recordInput)


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")

neededColumnList = ["SiteUUID", "CommunityWaterSupplySystem", "TimeframeEnd", "TimeframeStart", "Amount"]
dfrecord_2 = pd.DataFrame(columns=neededColumnList, index=dfrecord.index)
dfrecord_2 = dfrecord[neededColumnList].drop_duplicates().reset_index(drop=True)

# Explode record data by SiteUUID
dfrecord_2 = dfrecord_2.assign(SiteUUID=dfrecord_2['SiteUUID'].str.split(',')).explode('SiteUUID').reset_index(drop=True)

# Merging dataframes into one, using left-join.
dfrecord_2 = pd.merge(dfrecord_2, dfsites[['SiteUUID', 'PODorPOUSite']], on='SiteUUID', how='left')

# Split into two dataframes: POD & POU sites
neededColumnList = ["SiteUUID", "CommunityWaterSupplySystem", "TimeframeEnd", "TimeframeStart", "Amount", "PODorPOUSite"]
dfPOD = pd.DataFrame(columns=neededColumnList)
dfPOD = dfrecord_2[dfrecord_2['PODorPOUSite'] == "POD"].reset_index(drop=True)

dfPOU = pd.DataFrame(columns=neededColumnList)
dfPOU = dfrecord_2[dfrecord_2['PODorPOUSite'] == "POU"].reset_index(drop=True)


# Create output DataFrame
# see if there are matching rows / records in dfPOD & dfPOU.
outdf = pd.DataFrame()
outdf = pd.merge(dfPOD, dfPOU, on=["CommunityWaterSupplySystem", "TimeframeEnd", "TimeframeStart", "Amount"], how='inner')

def retrievePODSiteUUID(pouX, siteX, siteY):
    # Check for POD
    if pouX == "POD":
        outString = siteX  # return POD SiteUUID
    else:
        outString = siteY  # return POU SiteUUID
    return outString
outdf['PODSiteUUID'] = outdf.apply(lambda row: retrievePODSiteUUID(row['PODorPOUSite_x'], row['SiteUUID_x'], row['SiteUUID_y']), axis=1)

def retrievePOUSiteUUID(pouX, siteX, siteY):
    # Check for POD
    if pouX == "POU":
        outString = siteX  # return POD SiteUUID
    else:
        outString = siteY  # return POU SiteUUID
    return outString
outdf['POUSiteUUID'] = outdf.apply(lambda row: retrievePOUSiteUUID(row['PODorPOUSite_x'], row['SiteUUID_x'], row['SiteUUID_y']), axis=1)


neededColumnList = ["PODSiteUUID", "POUSiteUUID", "StartDate", "EndDate"]
outdf_2 = pd.DataFrame()
outdf_2['PODSiteUUID'] = outdf['PODSiteUUID']
outdf_2['POUSiteUUID'] = outdf['POUSiteUUID']
outdf_2['StartDate'] = outdf['TimeframeStart']
outdf_2['EndDate'] = outdf['TimeframeEnd']


# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")

# The working output DataFrame for WaDE 2.0 input.
if not outdf_2.empty:
    outdf_2.to_csv('ProcessedInputData/podsitetopousiterelationships.csv', index=False)

print("Done.")
