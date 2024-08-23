# Date Updated: 05/03/2022
# Purpose: To extract NM agg reporting unit information and population dataframe for WaDEQA 2.0.
# Notes: N/A


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "G:/Shared drives/WaDE Data/NewMexico/AggregatedAmounts"
os.chdir(workingDir)
fileInput = "RawinputData/P_nmAgMaster.csv"
df = pd.read_csv(fileInput).replace(np.nan, "")  # The State's Master input dataframe. Remove any nulls.
fileInput_shape = "RawinputData/P_nmAgGeometry.csv"
dfshape = pd.read_csv(fileInput_shape)

columnslist =[
    "ReportingUnitUUID",
    "EPSGCodeCV",
    "Geometry",
    "ReportingUnitName",
    "ReportingUnitNativeID",
    "ReportingUnitProductVersion",
    "ReportingUnitTypeCV",
    "ReportingUnitUpdateDate",
    "StateCV"]


# Custom Functions
############################################################################

# For Creating Geometry
# using reporting unit name instead of native ID for NM
Geometrydict = pd.Series(dfshape.in_Geomerty.values, index = dfshape.in_ReportingUnitName).to_dict()
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
    outstring = "NMag_RU" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist, index=df.index)

print("EPSGCodeCV")
outdf['EPSGCodeCV'] = "4326"

print("ReportingUnitName")
outdf['ReportingUnitName'] = df['in_ReportingUnitName']  # See pre-processing.

print("ReportingUnitNativeID")
outdf['ReportingUnitNativeID'] = df['in_ReportingUnitNativeID']  # See pre-processing.

print("ReportingUnitProductVersion")
outdf['ReportingUnitProductVersion'] = ""

print("ReportingUnitTypeCV")
outdf['ReportingUnitTypeCV'] = df['in_ReportingUnitTypeCV']  # See pre-processing.

print("ReportingUnitUpdateDate")
outdf['ReportingUnitUpdateDate'] = ""

print("StateCV")
outdf['StateCV'] = "NM"

print("Geometry")
outdf['Geometry'] = df.apply(lambda row: retrieveGeometry(row['in_ReportingUnitName']), axis=1)  # See pre-processing.

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of ReportingUnitName, ReportingUnitNativeID & ReportingUnitTypeCV
outdf = outdf.drop_duplicates(subset=['ReportingUnitName', 'ReportingUnitNativeID', 'ReportingUnitTypeCV'])
outdf = outdf.reset_index(drop=True)
######################################

print("Resetting Index")
outdf.reset_index()


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")
purgecolumnslist = ["ReasonRemoved", "RowIndex", "IncompleteField_1", "IncompleteField_2"]
dfpurge = pd.DataFrame(columns=purgecolumnslist) # Purge DataFrame to hold removed elements

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


############################################################################
print("Assign ReportingUnitUUID") # has to be one of the last.
outdf = outdf.reset_index(drop=True)
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['ReportingUnitUUID'] = dftemp.apply(lambda row: assignReportingUnitID(row['Count']), axis=1)

# Error Check ReportingUnitUUID
outdf, dfpurge = TestErrorFunctions.ReportingUnitUUID_RU_Check(outdf, dfpurge)


# Export to new csv
############################################################################
print("Exporting outdf and dfpurge dataframes...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/reportingunits.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_excel('ProcessedInputData/reportingunits_missing.xlsx', index=False)

print("Done.")
