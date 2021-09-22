# Author: Ryan James (WSWC)
# Date Created: 09/21/2021
# Purpose: To extract OK regulatory overlay bridge to site information and populate a dataframe WaDEQA 2.0.
# Notes: 1) asdf


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
print("Reading Regulatory input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Oklahoma/Regulatory"
os.chdir(workingDir)

M_fileInput = "RawinputData/OK_Sites_RegulatoryOverlay_Bridge_input.csv"  # ArcGIS Pro generated input file.
df_DM = pd.read_csv(M_fileInput).replace(np.nan, "")

regover_fileInput = "ProcessedInputData/regulatoryoverlays.csv"
dr_regover = pd.read_csv(regover_fileInput)  # Regulatory Overlays dataframe.

print("Reading Water Right Site input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Oklahoma/WaterAllocation"
os.chdir(workingDir)

sites_fileInput = "ProcessedInputData/sites.csv"  # Water rights sites.csv.
df_sites = pd.read_csv(sites_fileInput).replace(np.nan, "")

#WaDE dataframe columns
columnslist = [
    "RegulatoryOverlayUUIDs",
    "SiteUUID"]


# Custom Functions
############################################################################

# For creating RegulatoryOverlayUUID
RegulatoryOverlayUUIDdict = pd.Series(dr_regover.RegulatoryOverlayUUID.values, index = dr_regover.RegulatoryOverlayNativeID).to_dict()
def retrieveRegulatoryOverlayUUID(colrowValue):
    if colrowValue == "" or pd.isnull(colrowValue):
        outList = ""
    else:
        String1 = colrowValue
        try:
            outList = RegulatoryOverlayUUIDdict[String1]
        except:
            outList = ""
    return outList


# Creating Sites_RegulatoryOverlay_Bridge Table
############################################################################
print("Populating dataframe outdf...")
df_regToSite = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("RegulatoryOverlayUUIDs")  # Using RegulatoryOverlayNativeID to identify ID
df_regToSite['RegulatoryOverlayUUIDs'] = df_DM.apply(lambda row: retrieveRegulatoryOverlayUUID(row['TYPE']), axis=1)

print("SiteUUID")
df_regToSite['SiteUUID'] = df_DM['SiteUUID']

print("Resetting Index")
df_regToSite = df_regToSite.drop_duplicates().reset_index(drop=True)

# Bridge to Sites.csv for Water Rights
print("Updating sites.csv file.")
df_sites = pd.merge(df_sites, df_regToSite[['SiteUUID', 'RegulatoryOverlayUUIDs']], left_on='SiteUUID', right_on='SiteUUID', how='left')


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# N/A


# #Error Checking each Field
# ############################################################################
print("Error checking each field.  Purging bad inputs.")

# N/A


# Export to new csv
############################################################################
print("Exporting WaterAllocation Sites...")
# WaterAllocation Sites
# The working sites DataFrame for WaDE 2.0 input.
df_sites.to_csv('ProcessedInputData/sites_withReg.csv', index=False)





############################################################################

# # For creating RegulatoryOverlayUUID
# RegoverToSitesDict = pd.Series(df_regToSite.RegulatoryOverlayUUID.values, index = df_regToSite.SiteUUID).to_dict()
# def RegoverToStiesFunction(colrowValue):
#     if colrowValue == "" or pd.isnull(colrowValue):
#         outList = ""
#     else:
#         String1 = colrowValue.strip()
#         try:
#             outList = RegoverToSitesDict[String1]
#         except:
#             outList = ""
#     return outList
# print("Sites RegulatoryOverlayUUIDs")
# df_sites['RegulatoryOverlayUUIDs'] = df_sites.apply(lambda row: RegoverToStiesFunction(row['SiteUUID']), axis=1)