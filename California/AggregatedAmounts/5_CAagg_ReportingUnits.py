#Date Created: 11/04/2020
#Author: Ryan James (WSWC)
#Purpose: To create CA agg reporting unit information and populate a dataframe for WaDEQA 2.0.
#Notes:


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd

# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/California/AggregatedAmounts"
os.chdir(workingDir)
fileInput = "RawinputData/P_caAggMaster.csv"
fileInput_shape = "RawinputData/P_caGeometry.csv"
df = pd.read_csv(fileInput)
dfshape = pd.read_csv(fileInput_shape)

columnslist =[
    "ReportingUnitUUID",
    "EPSGCodeCV",
    "ReportingUnitName",
    "ReportingUnitNativeID",
    "ReportingUnitProductVersion",
    "ReportingUnitTypeCV",
    "ReportingUnitUpdateDate",
    "StateCV",
    "Geometry"]


# Custom Functions
############################################################################

# For Creating Geometry
Geometrydict = pd.Series(dfshape.geometry.values, index = dfshape.RU_ID).to_dict()
def retrieveGeometry(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()
        try:
            outList = Geometrydict[String1]
        except:
            outList = ''
    return outList


# For creating SiteUUID
def assignReportingUnitID(colrowValue):
    string1 = str(colrowValue)
    outstring = "CAag_RU" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist, index=df.index)

print("EPSGCodeCV")
outdf.EPSGCodeCV = 'EPSG:4326'

print("ReportingUnitName")
outdf['ReportingUnitName'] = df['inReportingUnitName']

print("ReportingUnitNativeID")
outdf['ReportingUnitNativeID'] = df['inReportingUnitNativeID']

print("ReportingUnitProductVersion")
outdf.ReportingUnitProductVersion = ''

print("ReportingUnitTypeCV")
outdf['ReportingUnitTypeCV'] = df['inReportingUnitTypeCV']

print("ReportingUnitUpdateDate")
outdf.ReportingUnitUpdateDate = ''

print("StateCV")
outdf.StateCV = "CA"

print("Geometry")
outdf['Geometry'] = df.apply(lambda row: retrieveGeometry(row['inReportingUnitNativeID']), axis=1)

print("Resetting Index")
outdf.reset_index()

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of ReportingUnitName, ReportingUnitNativeID & ReportingUnitTypeCV
outdf = outdf.drop_duplicates(subset=['ReportingUnitName', 'ReportingUnitNativeID', 'ReportingUnitTypeCV'])
outdf = outdf.reset_index(drop=True)
######################################

print("ReportingUnitUUID") # has to be one of the last.
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['ReportingUnitUUID'] = dftemp.apply(lambda row: assignReportingUnitID(row['Count']), axis=1)


#Error Checking each Field
############################################################################
print("Error checking each field. Purging bad inputs.")
dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# ReportingUnitUUID_nvarchar(200)_
mask = outdf.loc[ (outdf["ReportingUnitUUID"].isnull()) | (outdf["ReportingUnitUUID"] == '') | (outdf['ReportingUnitUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad ReportingUnitUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[ (outdf["ReportingUnitUUID"].isnull()) | (outdf["ReportingUnitUUID"] == '') | (outdf['ReportingUnitUUID'].str.len() > 200) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# EPSGCodeCV_nvarchar(50)_Yes
mask = outdf.loc[ (outdf['EPSGCodeCV'].str.len() > 50) ].assign(ReasonRemoved='Bad EPSGCodeCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[ (outdf["EPSGCodeCV"].isnull()) | (outdf["EPSGCodeCV"] == '') | (outdf['EPSGCodeCV'].str.len() > 50) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# Geometry_Geometry_Yes
# Not sure how to check for this...

# ReportingUnitName_nvarchar(250)_
mask = outdf.loc[ (outdf["ReportingUnitName"].isnull()) | (outdf["ReportingUnitName"] == '') | (outdf['ReportingUnitName'].str.len() > 250) ].assign(ReasonRemoved='Bad ReportingUnitName').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[ (outdf["ReportingUnitName"].isnull()) | (outdf["ReportingUnitName"] == '') | (outdf['ReportingUnitName'].str.len() > 250) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# ReportingUnitNativeID_nvarchar(250)_
mask = outdf.loc[ (outdf["ReportingUnitNativeID"].isnull()) | (outdf["ReportingUnitNativeID"] == '') | (outdf['ReportingUnitNativeID'].str.len() > 250) ].assign(ReasonRemoved='Bad ReportingUnitNativeID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[ (outdf["ReportingUnitNativeID"].isnull()) | (outdf["ReportingUnitNativeID"] == '') | (outdf['ReportingUnitNativeID'].str.len() > 250) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# ReportingUnitProductVersion_nvarchar(100)_Yes
mask = outdf.loc[ outdf["ReportingUnitProductVersion"].str.len() > 100 ].assign(ReasonRemoved='Bad ReportingUnitProductVersion').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ outdf["ReportingUnitProductVersion"].str.len() > 100 ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# this might allow 50 (not 20) double check on that
# ReportingUnitTypeCV_nvarchar(20)_
mask = outdf.loc[ (outdf["ReportingUnitTypeCV"].isnull()) | (outdf["ReportingUnitTypeCV"] == '') | (outdf['ReportingUnitTypeCV'].str.len() > 50) ].assign(ReasonRemoved='Bad ReportingUnitTypeCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[ (outdf["ReportingUnitTypeCV"].isnull()) | (outdf["ReportingUnitTypeCV"] == '') | (outdf['ReportingUnitTypeCV'].str.len() > 50) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# ReportingUnitUpdateDate_Date_Yes
mask = outdf.loc[ (outdf["ReportingUnitUpdateDate"].str.contains(',') == True) ].assign(ReasonRemoved='Bad ReportingUnitUpdateDate').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf.loc[ (outdf["ReportingUnitUpdateDate"].str.contains(',') == True) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

# StateCV_nvarchar(2)_
mask = outdf.loc[ (outdf["StateCV"].isnull()) | (outdf["StateCV"] == '') | (outdf['StateCV'].str.len() > 50) ].assign(ReasonRemoved='Bad StateCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf.loc[ (outdf["StateCV"].isnull()) | (outdf["StateCV"] == '') | (outdf['StateCV'].str.len() > 50) ].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)


# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")
# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/reportingunits.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/reportingunits_missing.csv')

print("Done.")