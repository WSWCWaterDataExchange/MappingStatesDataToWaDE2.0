# Author: Ryan James (WSWC)
# Date Created: 09/21/2021
# Purpose: To extract OK regulatory overlay information and populate a dataframe WaDEQA 2.0.
# Notes: N/A


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
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Oklahoma/Regulatory"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_okRegMaster.csv"
reportingunits_fileInput = "ProcessedInputData/reportingunits.csv"
regulatoryoverlays_fileInput = "ProcessedInputData/regulatoryoverlays.csv"

df_DM = pd.read_csv(M_fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.
df_reportingunits = pd.read_csv(reportingunits_fileInput)  # ReportingUnits dataframe
df_regulatoryoverlays = pd.read_csv(regulatoryoverlays_fileInput)  # ReportingUnits dataframe

#WaDE dataframe columns
columnslist = [
    "DataPublicationDate",
    "OrganizationUUID",
    "RegulatoryOverlayUUID",
    "ReportingUnitUUID"]


# Custom Functions
############################################################################

# For creating RegulatoryOverlayUUID
RegulatoryOverlayUUIDdict = pd.Series(df_regulatoryoverlays.RegulatoryOverlayUUID.values, index = df_regulatoryoverlays.RegulatoryOverlayNativeID).to_dict()
def retrieveRegulatoryOverlayUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = RegulatoryOverlayUUIDdict[String1]
        except:
            outList = ''
    return outList

# For creating ReportingUnitsUUID
ReportingUnitUUIDdict = pd.Series(df_reportingunits.ReportingUnitUUID.values, index = df_reportingunits.ReportingUnitNativeID).to_dict()
def retrieveReportingUnitsUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = ReportingUnitUUIDdict[String1]
        except:
            outList = ''
    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("DataPublicationDate")  # Hard Coded
outdf['DataPublicationDate'] = "09/20/2020"
outdf['DataPublicationDate'] = pd.to_datetime(outdf['DataPublicationDate'], errors = 'coerce')
outdf['DataPublicationDate'] = pd.to_datetime(outdf["DataPublicationDate"].dt.strftime('%m/%d/%Y'))

print("OrganizationUUID")  # Hard Coded
outdf['OrganizationUUID'] = "OWRB"

print("RegulatoryOverlayUUID")  # Using RegulatoryOverlayNativeID to identify ID
outdf['RegulatoryOverlayUUID'] = df_DM.apply(lambda row: retrieveRegulatoryOverlayUUID(row['TYPE']), axis=1)

print("ReportingUnitUUID")  # Using RegulatoryOverlayNativeID to identify ID
outdf['ReportingUnitUUID'] = df_DM.apply(lambda row: retrieveReportingUnitsUUID(row['OBJECTID']), axis=1)

print("Resetting Index")
outdf = outdf.drop_duplicates().reset_index(drop=True)



# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# N/A


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")

dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# DataPublicationDate
# ???

# OrganizationUUID
# ???

# ReportingUnitUUID
outdf, dfpurge = TestErrorFunctions.ReportingUnitUUID_RU_Check(outdf, dfpurge)

# RegulatoryOverlayUUID
outdf, dfpurge = TestErrorFunctions.RegulatoryOverlayUUID_RE_Check(outdf, dfpurge)



# Export to new csv
############################################################################
print("Exporting dataframe outdf100 to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/regulatoryreportingunits.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/regulatoryreportingunits_missing.csv', index=False)

print("Done.")
