# Date Created: 08/12/2021
# Author: Ryan James (WSWC)
# Purpose: To create NM regulatory overlay bridge to site information and populate a dataframe WaDEQA 2.0.
# Notes: 1) Have to upload regulatory overlay and reporting units to QA first
#        2) export data with sites info to ArcGIS Pro
#        3) perform spatial join of sites with areas.
#        4) re-upload new sites.csv


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/CustomFunctions/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/NewMexico/Regulatory"
os.chdir(workingDir)

M_fileInput = "RawinputData/NM_Sites_RegulatoryOverlay_Bridge_input.csv"  # ArcGIS Pro generated input file.
df_DM = pd.read_csv(M_fileInput).replace(np.nan, "")

#WaDE dataframe columns
columnslist = [
    "RegulatoryOverlayUUID",
    "SiteUUID"]


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("RegulatoryOverlayUUID")
outdf['RegulatoryOverlayUUID'] = df_DM['Reportin_1']

print("SiteUUID")
outdf['SiteUUID'] = df_DM['SiteUUID']

print("Resetting Index")
outdf = outdf.drop_duplicates().reset_index(drop=True)


# Bridge to Sites.csv for Water Rights
############################################################################
sites_fileInput = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/NewMexico/WaterAllocation/ProcessedInputData/sites.csv"  # ArcGIS Pro generated input file.
df_sites = pd.read_csv(sites_fileInput).replace(np.nan, "")


# # For creating RegulatoryOverlayUUID
# RegulatoryOverlayUUIDdict = pd.Series(outdf.RegulatoryOverlayUUID.values, index = outdf.SiteUUID).to_dict()
# def retrieveRegulatoryOverlayUUID(colrowValue):
#     if colrowValue == '' or pd.isnull(colrowValue):
#         outList = ''
#     else:
#         String1 = colrowValue.strip()
#         try:
#             outList = RegulatoryOverlayUUIDdict[String1]
#         except:
#             outList = ''
#     return outList
# print("Sites RegulatoryOverlayUUIDs")
# df_sites['RegulatoryOverlayUUIDs'] = df_sites.apply(lambda row: retrieveRegulatoryOverlayUUID(row['SiteUUID']), axis=1)


print("Merging Files")
df_sites = pd.merge(df_sites, outdf[['SiteUUID', 'RegulatoryOverlayUUID']], left_on='SiteUUID', right_on='SiteUUID', how='left')





# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# N/A


# #Error Checking each Field
# ############################################################################
# print("Error checking each field.  Purging bad inputs.")
#
# dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
# dfpurge = dfpurge.assign(ReasonRemoved='')
#
# # RegulatoryOverlayUUID
# outdf, dfpurge = TestErrorFunctions.RegulatoryOverlayUUID_RE_Check(outdf, dfpurge)
#
# # SiteUUID
# # ???


# Export to new csv
############################################################################
print("Exporting WaterAllocation Sites...")
# WaterAllocation Sites
# The working output DataFrame for WaDE 2.0 input.
df_sites.to_csv('C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/NewMexico/WaterAllocation/ProcessedInputData/sites_withReg.csv', index=False)
