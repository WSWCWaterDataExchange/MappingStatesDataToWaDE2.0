#Date Created: 06/25/2020
#Purpose: To extract NM agg reporting unit information and population dataframe for WaDEQA 2.0.
#Notes:


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os

# Custom Libraries
############################################################################
import sys
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/ErrorCheckCode")
import TestErrorFunctions


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/NewMexico/AggregatedAmounts"
os.chdir(workingDir)
fileInput = "RawinputData/P_NMagg.csv"
df = pd.read_csv(fileInput)

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

# For creating SiteUUID
def assignReportingUnitID(colrowValue):
    string1 = str(colrowValue)
    outstring = "NMag_RU" + string1
    return outstring


# For creating ReportingUnitNativeID
nameGEOIDDict = {
"Bernalillo" : "35001",
"Catron" : "35003",
"Chaves" : "35005",
"Cibola" : "35006",
"Colfax" : "35007",
"Curry" : "35009",
"De Baca" : "35011",
"Dona Ana" : "35013",
"Eddy" : "35015",
"Grant" : "35017",
"Guadalupe" : "35019",
"Harding" : "35021",
"Hidalgo" : "35023",
"Lea" : "35025",
"Lincoln" : "35027",
"Los Alamos" : "35028",
"Luna" : "35029",
"McKinley" : "35031",
"Mora" : "35033",
"Otero" : "35035",
"Quay" : "35037",
"Rio Arriba" : "35039",
"Roosevelt" : "35041",
"San Juan" : "35045",
"San Miguel" : "35047",
"Sandoval" : "35043",
"Santa Fe" : "35049",
"Sierra" : "35051",
"Socorro" : "35053",
"Taos" : "35055",
"Torrance" : "35057",
"Union" : "35059",
"Valencia" : "35061"}

def retrieveGEOID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = colrowValue
    else:
        String1 = colrowValue  # remove whitespace chars
        try:
            outList = nameGEOIDDict[String1]
        except:
            outList = colrowValue
    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist, index=df.index)

print("EPSGCodeCV")
outdf['EPSGCodeCV'] = 'EPSG:4326'

print("Geometry")
outdf['Geometry'] = df['Geometry']

print("ReportingUnitName")
outdf['ReportingUnitName'] = df['COUNTY']

print("ReportingUnitNativeID")
outdf['ReportingUnitNativeID'] = outdf.apply(lambda row: retrieveGEOID(row['ReportingUnitName']), axis=1)

print("ReportingUnitProductVersion")
outdf['ReportingUnitProductVersion'] = ''

print("ReportingUnitTypeCV")
outdf['ReportingUnitTypeCV'] = 'County'

print("ReportingUnitUpdateDate")
outdf['ReportingUnitUpdateDate'] = ''

print("StateCV")
outdf['StateCV'] = "NM"

print("Resetting Index")
outdf.reset_index()

#####################################
# Dropping duplicate
# filter the whole table based on a unique combination of ReportingUnitName
outdf = outdf.drop_duplicates(subset=['ReportingUnitName'])
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
