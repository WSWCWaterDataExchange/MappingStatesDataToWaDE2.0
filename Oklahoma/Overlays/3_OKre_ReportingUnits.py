# Author: Ryan James (WSWC)
# Date Created: 09/21/2021
# Purpose: To extract OK regulatory reporting unit information and populate a dataframe for WaDEQA 2.0.
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
fileInput = "RawinputData/P_okRegMaster.csv"
fileInput_shape = "RawinputData/P_okRegGeometry.csv"
df = pd.read_csv(fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.
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
Geometrydict = pd.Series(dfshape.geometry.values, index = dfshape.OBJECTID).to_dict()
def retrieveGeometry(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue
        try:
            outList = Geometrydict[String1]
        except:
            outList = ''
    return outList

# For creating SiteUUID
def assignReportingUnitID(colrowValue):
    string1 = str(colrowValue)
    outstring = "OKre_RU" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist, index=df.index)

print("EPSGCodeCV")
outdf['EPSGCodeCV'] = "4326"

print("ReportingUnitName")
outdf['ReportingUnitName'] = df['NAME']

print("ReportingUnitNativeID")
outdf['ReportingUnitNativeID'] = df['OBJECTID']

print("ReportingUnitProductVersion")
outdf['ReportingUnitProductVersion'] = ""

print("ReportingUnitTypeCV")
outdf['ReportingUnitTypeCV'] = "Special Provision Watersheds"

print("ReportingUnitUpdateDate")
outdf['ReportingUnitUpdateDate'] = ""

print("StateCV")
outdf['StateCV'] = "OK"

print("Geometry")
outdf['Geometry'] = df.apply(lambda row: retrieveGeometry(row['OBJECTID']), axis=1)

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
print("Error checking each field.  Purging bad inputs.")

dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# ReportingUnitUUID
outdf, dfpurge = TestErrorFunctions.ReportingUnitUUID_RU_Check(outdf, dfpurge)

# EPSGCodeCV
outdf, dfpurge = TestErrorFunctions.EPSGCodeCV_RU_Check(outdf, dfpurge)

# ReportingUnitName
outdf, dfpurge = TestErrorFunctions.ReportingUnitName_RU_Check(outdf, dfpurge)

# ReportingUnitNativeID
outdf, dfpurge = TestErrorFunctions.ReportingUnitNativeID_RU_Check(outdf, dfpurge)

# ReportingUnitProductVersion
outdf, dfpurge = TestErrorFunctions.ReportingUnitProductVersion_RU_Check(outdf, dfpurge)

# ReportingUnitTypeCV
outdf, dfpurge = TestErrorFunctions.ReportingUnitTypeCV_RU_Check(outdf, dfpurge)

# ReportingUnitUpdateDate
outdf, dfpurge = TestErrorFunctions.ReportingUnitUpdateDate_RU_Check(outdf, dfpurge)

# StateCV
outdf, dfpurge = TestErrorFunctions.StateCV_RU_Check(outdf, dfpurge)

# Geometry
# ???? How to check for geometry datatype


# Export to new csv
############################################################################
print("Exporting dataframe outdf to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/reportingunits.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/reportingunits_missing.csv', index=False)

print("Done.")
