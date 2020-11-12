#Last Updated: 10/29/2020
#Author: Ryan James
#Purpose: To extract UT site specific site amount use information and population dataframe WaDEQA 2.0.
#Notes:


# Needed Libraries
############################################################################
import numpy as np
import pandas as pd
import os
from pyproj import Transformer, transform


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/SiteSpecificAmounts/UDWRi"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_MasterUTSiteSpecific.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
sites_fileInput = "ProcessedInputData/sites.csv"
shapefileInput = "RawinputData/P_Geometry.csv"

df_DM = pd.read_csv(M_fileInput)  # The State's Master input dataframe.
df_variables = pd.read_csv(variables_fileInput)  # Variable dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_sites = pd.read_csv(sites_fileInput)  # Sites dataframe
df_shape = pd.read_csv(shapefileInput)

transformer = Transformer.from_crs(4269, 4326)
# NAD83 projection = epsg:4269.
# WGS84 projection used by WaDE 2.0 = epsg:4326.

#WaDE dataframe columns
columnslist = [
    "MethodUUID",
    "OrganizationUUID",
    "SiteUUID",
    "VariableSpecificUUID",
    "WaterSourceUUID",
    "Amount",
    'AllocationCropDutyAmount',
    "AssociatedNativeAllocationIDs",
    'BeneficialUseCategory',
    "CommunityWaterSupplySystem",
    "CropTypeCV",
    "CustomerTypeCV",
    "DataPublicationDate",
    "DataPublicationDOI",
    "Geometry",
    "IrrigatedAcreage",
    "IrrigationMethodCV",
    "PopulationServed",
    "PowerGeneratedGWh",
    'PowerType',
    "PrimaryUseCategory",
    "ReportYearCV",
    "SDWISIdentifier",
    "TimeframeEnd",
    "TimeframeStart"]


# Custom Functions
############################################################################

# For retrieving VariableSpecificUUID.
VariableUUIDDict = pd.Series(df_variables.VariableSpecificUUID.values, index=df_variables.VariableCV).to_dict()
def retrieveVariableUUID(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = VariableUUIDDict[String1]
        except:
            outList = ''
    return outList


#-------------------------------------
# For creating SiteUUID
def assignLat(colrowValLat, colrowValLong):
    lat, long = transformer.transform(colrowValLat, colrowValLong)
    return lat

def assignLong(colrowValLat, colrowValLong):
    lat, long = transformer.transform(colrowValLat, colrowValLong)
    return long

def retrieveSiteUUID(colrowValA, colrowValB, colrowValC, colrowValD, colrowValE):
    if (colrowValA=='' and colrowValB=='' and colrowValC=='' and colrowValD=='' and colrowValE=='') or (pd.isnull(colrowValA) and pd.isnull(colrowValB) and pd.isnull(colrowValC) and pd.isnull(colrowValD) and pd.isnull(colrowValE)):
        outList = ''
    else:
        ml = df_sites.loc[(df_sites['Latitude'] == colrowValA) &
                          (df_sites['Longitude'] == colrowValB) &
                          (df_sites['SiteName'] == colrowValC) &
                          (df_sites['SiteNativeID'] == colrowValD) &
                          (df_sites['SiteTypeCV'] == colrowValE), 'SiteUUID']
        if not (ml.empty):  # check if the series is empty
            outList = ml.iloc[0]
        else:
            outList = ''
    return outList

#-------------------------------------

#-------------------------------------
# For creating WaterSourceUUID
def assignWaterSourceName(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = 'Unspecified'
    else:
        strval = str(colrowValue)
        outList = strval.strip()
    return outList

WSTypeDict = {
"Spring": "groundwater/spring",
"Well" :"groundwater/well",
"Stream" : "Surface Water",
"Reservoir" : "Surface Water",
"Drain" : "Surface Water",
"Well/Spring" : "Groundwater/Mixed",
"Tunnel" : "Groundwater",
"Well Field" : "groundwater/well",
"Lake" : "Surface Water"
}
def assignWaterSourceTypeCV(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unknown"
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = WSTypeDict[String1]
        except:
            outList = "Unknown"
    return outList

def retrieveWaterSourceUUID(colrowValA, colrowValC):
    ml = df_watersources.loc[(df_watersources['WaterSourceName'] == colrowValA) &
                             (df_watersources['WaterSourceTypeCV'] == colrowValC), 'WaterSourceUUID']
    outList = ml.iloc[0]
    return outList

#-------------------------------------
# For creating BeneficialUseCategory
def assignBenUseCategory(colrowVal):
    if colrowVal == '' or pd.isnull(colrowVal):
        outList = 'Unknown'
    else:
        outList = colrowVal.strip()
    return outList

# For retrieving Geometry
GeometryDict = pd.Series(df_shape.culGeometry.values, index=df_shape.WRID).to_dict()
def retrieveGeometry(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        String1 = colrowValue  # remove whitespace chars
        try:
            outList = GeometryDict[String1]
        except:
            outList = ''
    return outList


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe outdf...")
outdf = pd.DataFrame(index=df_DM.index, columns=columnslist)  # The output dataframe

print("MethodUUID")
outdf.MethodUUID = "UDWRi_Water Use Data"

print("OrganizationUUID")
outdf.OrganizationUUID = "UDWRi"

#-------------------------------------
print("SiteUUID")  # Using Lat, long, SiteName, SiteNativeID & SiteTypeCV to correctly identify SiteUUIDID
df_DM['Latitude'] = df_DM.apply(lambda row: assignLat(row['Lat NAD83_Sour'], row['Lon NAD83_Sour']), axis=1)
df_DM['Longitude'] = df_DM.apply(lambda row: assignLong(row['Lat NAD83_Sour'], row['Lon NAD83_Sour']), axis=1)
outdf['SiteUUID'] = df_DM.apply(lambda row: retrieveSiteUUID(row['Latitude'],
                                                             row['Longitude'],
                                                             row['Source Name_Sour'],
                                                             row['Source ID_Sour'],
                                                             row['Source Type_Sour']), axis=1)
#-------------------------------------

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = df_DM.apply(lambda row: retrieveVariableUUID(row['Diversion Type_Sour']), axis=1)

#-------------------------------------
print("WaterSourceUUID")  # Using Lat, long, SiteName, SiteNativeID & SiteTypeCV to correctly identify SiteUUIDID
df_DM['WaterSourceName'] = df_DM.apply(lambda row: assignWaterSourceName(row['Source Name_Sour']), axis=1)
df_DM['WaterSourceTypeCV'] = df_DM.apply(lambda row: assignWaterSourceTypeCV(row['Source Type_Sour']), axis=1)
outdf['WaterSourceUUID'] = df_DM.apply(lambda row: retrieveWaterSourceUUID(row['WaterSourceName'], row['WaterSourceTypeCV']), axis=1)
#-------------------------------------

print("Amount")
outdf['Amount'] = df_DM['Total Use_Sys']

print('AllocationCropDutyAmount')
outdf.AllocationCropDutyAmount = ''

print("AssociatedNativeAllocationIDs")
outdf.AssociatedNativeAllocationIDs = ''

print("CommunityWaterSupplySystem")
outdf['CommunityWaterSupplySystem'] = df_DM['System Name_Sys'].astype(str)

print('BeneficialUseCategory')
outdf['BeneficialUseCategory'] = df_DM['Use Type_Sour'].astype(str)

print("CropTypeCV")
outdf.CropTypeCV = ''

# Issue of CustomerTypeCV of being converted from nvarchar to float
print("CustomerTypeCV")
outdf['CustomerTypeCV'] = df_DM['System Type_Sys']

print("DataPublicationDate")
outdf.DataPublicationDate = '11/02/2020'

print("DataPublicationDOI")
outdf.DataPublicationDOI = ''

print("Geometry")
outdf['Geometry'] = df_DM.apply(lambda row: retrieveGeometry(row['System ID_Sys']), axis=1)

print("IrrigatedAcreage")
outdf.IrrigatedAcreage = ''

print("IrrigationMethodCV")
outdf.IrrigationMethodCV = ''

# Issue of PopulationServed of being converted from nvarchar to float
print("PopulationServed")
outdf['PopulationServed'] = df_DM['Population_Sys']

print("PowerGeneratedGWh")
outdf.PowerGeneratedGWh = ''

print("PowerType")
outdf.PowerType = ''

print("PrimaryUseCategory")
outdf['PrimaryUseCategory'] = df_DM['Use Type_Sour']

print("ReportYearCV")
outdf['ReportYearCV'] = df_DM['History Year_Sys'].astype(str)

print("SDWISIdentifier")
outdf.SDWISIdentifier = ''

print("TimeframeEnd")
outdf['TimeframeEnd'] = df_DM['TimeframeEnd']

print("TimeframeStart")
outdf['TimeframeStart'] = df_DM['TimeframeStart']

print("Resetting Index")
outdf.reset_index()

print("Joining outdf duplicates based on AllocationNativeID...")
outdf100 = outdf.replace(np.nan, '')  # Replaces NaN values with blank.


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# None at the moment


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")  
dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# MethodUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["MethodUUID"].isnull()) | (outdf100["MethodUUID"] == '') | (outdf100['MethodUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad MethodUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf100.loc[ (outdf100["MethodUUID"].isnull()) | (outdf100["MethodUUID"] == '') | (outdf100['MethodUUID'].str.len() > 200) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# VariableSpecificUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["VariableSpecificUUID"].isnull()) | (outdf100["VariableSpecificUUID"] == '') | (outdf100['VariableSpecificUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad VariableSpecificUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["VariableSpecificUUID"].isnull()) | (outdf100["VariableSpecificUUID"] == '') | (outdf100['VariableSpecificUUID'].str.len() > 200) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# WaterSourceUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["WaterSourceUUID"].isnull()) | (outdf100["WaterSourceUUID"] == '') | (outdf100['WaterSourceUUID'].str.len() > 200) | (outdf100["WaterSourceUUID"].str.contains(',') == True) ].assign(ReasonRemoved='Bad WaterSourceUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["WaterSourceUUID"].isnull()) | (outdf100["WaterSourceUUID"] == '') | (outdf100['WaterSourceUUID'].str.len() > 200) | (outdf100["WaterSourceUUID"].str.contains(',') == True) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# OrganizationUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["OrganizationUUID"].isnull()) | (outdf100["OrganizationUUID"] == '') | (outdf100['OrganizationUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad OrganizationUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["OrganizationUUID"].isnull()) | (outdf100["OrganizationUUID"] == '') | (outdf100['OrganizationUUID'].str.len() > 200) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# SiteUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["SiteUUID"].isnull()) | (outdf100["SiteUUID"] == '') | (outdf100['SiteUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad SiteUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["SiteUUID"].isnull()) | (outdf100["SiteUUID"] == '') | (outdf100['SiteUUID'].str.len() > 200) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# Amount_float_Yes
mask = outdf100.loc[ (outdf100["Amount"].isnull()) | (outdf100["Amount"] == '') ].assign(ReasonRemoved='Bad Amount').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["Amount"].isnull()) | (outdf100["Amount"] == '') ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# this should be a float with no commas in it...
# # AllocationCropDutyAmount_float_Yes
# mask = outdf100.loc[ outdf100["AllocationCropDutyAmount"].str.contains(',') == True ].assign(ReasonRemoved='Bad AllocationCropDutyAmount').reset_index()
# if len(mask.index) > 0:
#     dfpurge = dfpurge.append(mask)
#     dropIndex = outdf100.loc[ outdf100["AllocationCropDutyAmount"].str.contains(',') == True ].index
#     outdf100 = outdf100.drop(dropIndex)
#     outdf100 = outdf100.reset_index(drop=True)

# AssociatedNativeAllocationIDs_nvarchar(500)_Yes
mask = outdf100.loc[ outdf100["AssociatedNativeAllocationIDs"].str.len() > 500 ].assign(ReasonRemoved='Bad AssociatedNativeAllocationIDs').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["AssociatedNativeAllocationIDs"].str.len() > 500 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# BeneficialUseCategory_nvarchar(250)_Yes
mask = outdf100.loc[ (outdf100["BeneficialUseCategory"].str.len() > 250) ].assign(ReasonRemoved='Bad BeneficialUseCategory').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["BeneficialUseCategory"].str.len() > 250) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# CommunityWaterSupplySystem_nvarchar(250)_Yes
mask = outdf100.loc[outdf100["CommunityWaterSupplySystem"].str.len() > 250].assign(ReasonRemoved='Bad CommunityWaterSupplySystem').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[outdf100["CommunityWaterSupplySystem"].str.len() > 250].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# CropTypeCV_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["CropTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Bad CropTypeCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["CropTypeCV"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# CustomerTypeCV(100)_Yes
mask = outdf100.loc[ outdf100["CustomerTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Bad CustomerTypeCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["CustomerTypeCV"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# DataPublicationDate_date_Yes
mask = outdf100.loc[outdf100["DataPublicationDate"].str.contains(',') == True].assign(ReasonRemoved='Bad DataPublicationDate').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["DataPublicationDate"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# DataPublicationDOI_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["DataPublicationDOI"].str.len() > 100 ].assign(ReasonRemoved='Bad DataPublicationDOI').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["DataPublicationDOI"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# Geometry_geometry_Yes
# ???? How to check for geometry datatype

# IrrigatedAcreage_float_Yes
mask = outdf100.loc[ outdf100["IrrigatedAcreage"].str.contains(',') == True ].assign(ReasonRemoved='Bad IrrigatedAcreage').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["IrrigatedAcreage"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# IrrigationMethodCV_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["IrrigationMethodCV"].str.len() > 100 ].assign(ReasonRemoved='Bad IrrigationMethodCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["IrrigationMethodCV"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# # PopulationServed_float_Yes
# mask = outdf100.loc[ outdf100["PopulationServed"].str.contains(',') == True ].assign(ReasonRemoved='Bad PopulationServed').reset_index()
# if len(mask.index) > 0:
#     dfpurge = dfpurge.append(mask)
#     dropIndex = outdf100.loc[ outdf100["PopulationServed"].str.contains(',') == True ].index
#     outdf100 = outdf100.drop(dropIndex)
#     outdf100 = outdf100.reset_index(drop=True)

# PowerGeneratedGWh_float_Yes
mask = outdf100.loc[ outdf100["PowerGeneratedGWh"].str.contains(',') == True ].assign(ReasonRemoved='Bad PowerGeneratedGWh').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["PowerGeneratedGWh"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# PowerType_nvarchar(50)_Yes
mask = outdf100.loc[ outdf100["PowerType"].str.len() > 50 ].assign(ReasonRemoved='Bad PowerType').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["PowerType"].str.len() > 50 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# PrimaryUseCategory_nvarchar(250)_Yes
# This might be bugged.  Issue of must have Primaryuse Category for Beneficial Use to work.
mask = outdf100.loc[ outdf100["PrimaryUseCategory"].str.len() > 250 ].assign(ReasonRemoved='Bad PrimaryUseCategory').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["PrimaryUseCategory"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# ReportYearCV_nchar(4)_Yes
mask = outdf100.loc[ outdf100["ReportYearCV"].str.len() > 4 ].assign(ReasonRemoved='Bad ReportYearCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["ReportYearCV"].str.len() > 4 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# SDWISIdentifier_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["SDWISIdentifier"].str.len() > 250 ].assign(ReasonRemoved='Bad SDWISIdentifier').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["SDWISIdentifier"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# # TimeframeEnd_BigInt_-
# mask = outdf100.loc[ outdf100["TimeframeEnd"].str.len() > 5 ].assign(ReasonRemoved='Bad TimeframeEnd').reset_index()
# if len(mask.index) > 0:
#     dfpurge = dfpurge.append(mask)
#     dropIndex = outdf100.loc[ outdf100["TimeframeEnd"].str.contains(',') == True ].index
#     outdf100 = outdf100.drop(dropIndex)
#     outdf100 = outdf100.reset_index(drop=True)

# # TimeframeStart_BigInt_-
# mask = outdf100.loc[ outdf100["TimeframeStart"].str.len() > 5 ].assign(ReasonRemoved='Bad TimeframeStart').reset_index()
# if len(mask.index) > 0:
#     dfpurge = dfpurge.append(mask)
#     dropIndex = outdf100.loc[ outdf100["TimeframeStart"].str.contains(',') == True ].index
#     outdf100 = outdf100.drop(dropIndex)
#     outdf100 = outdf100.reset_index(drop=True)


# Export to new csv
############################################################################
print("Exporting dataframe outdf100 to csv...")
# The working output DataFrame for WaDE 2.0 input.
outdf100.to_csv('ProcessedInputData/sitespecificamounts.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/sitespecificamounts_missing.csv', index=False)

print("Done.")
outdf100.to_excel('ProcessedInputData/temp_sitespecificamounts.xlsx', index=False)