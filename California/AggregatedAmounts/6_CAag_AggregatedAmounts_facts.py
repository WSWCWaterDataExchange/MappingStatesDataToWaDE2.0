#Date Created: 11/04/2020
#Author: Ryan James (WSWC)
#Purpose: To create CA agg aggregated information and populate a dataframe WaDEQA 2.0.
#         1) Simple creation of working dataframe (df), with output dataframe (outdf).
#         2) Drop all nulls before combining duplicate rows on NativeID.


# Needed Libraries
############################################################################
import numpy as np
import pandas as pd
import os


# Inputs
############################################################################
print("Reading input csv...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/California/AggregatedAmounts"
os.chdir(workingDir)
M_fileInput = "RawinputData/P_caAggMaster.csv"
method_fileInput = "ProcessedInputData/methods.csv"
variables_fileInput = "ProcessedInputData/variables.csv"
watersources_fileInput = "ProcessedInputData/watersources.csv"
reportingunits_fileInput = "ProcessedInputData/reportingunits.csv"

df_DM = pd.read_csv(M_fileInput)  # The State's Master input dataframe.
df_method = pd.read_csv(method_fileInput)  # Method dataframe
df_variables = pd.read_csv(variables_fileInput)  # Variables dataframe
df_watersources = pd.read_csv(watersources_fileInput)  # WaterSources dataframe
df_reportingunits = pd.read_csv(reportingunits_fileInput)  # ReportingUnits dataframe

#WaDE dataframe columns
columnslist = [
    "MethodUUID",
    "OrganizationUUID",
    "ReportingUnitUUID",
    "VariableSpecificUUID",
    "WaterSourceUUID",
    "AllocationCropDutyAmount",
    "Amount",
    "BeneficialUseCategory",
    "CommunityWaterSupplySystem",
    "CropTypeCV",
    "CustomerTypeCV",
    "DataPublicationDate",
    "DataPublicationDOI",
    "InterbasinTransferFromID",
    "InterbasinTransferToID",
    "IrrigatedAcreage",
    "IrrigationMethodCV",
    "PopulationServed",
    "PowerGeneratedGWh",
    "PowerType",
    "PrimaryUseCategory",
    "ReportYearCV",
    "SDWISIdentifierCV",
    "TimeframeEnd",
    "TimeframeStart"]


# Custom Functions
############################################################################

# For creating ReportingUnitsUUID
def retrieveReportingUnits(colrowValue):
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

print("MethodUUID")
outdf.MethodUUID = "CDWR_Water Use"

print("OrganizationUUID")
outdf.OrganizationUUID = "CDWR"

print("ReportingUnitUUID")  # Using SiteNativeID to identify ID
ReportingUnitUUIDdict = pd.Series(df_reportingunits.ReportingUnitUUID.values, index = df_reportingunits.ReportingUnitNativeID).to_dict()
outdf['ReportingUnitUUID'] = df_DM.apply(lambda row: retrieveReportingUnits(row['inReportingUnitNativeID']), axis=1)

print("VariableSpecificUUID")
outdf.VariableSpecificUUID = 'CA_Consumptive Use'

print("WaterSourceUUID")
outdf.WaterSourceUUID = 'CAag_WS1'

print("Amount")
outdf['Amount'] = df_DM['inAmount']

print("BeneficialUseCategory")
outdf['BeneficialUseCategory'] = df_DM['inBenUse']

print("CommunityWaterSupplySystem")
outdf.CommunityWaterSupplySystem = ""

print("CropTypeCV")
outdf.CropTypeCV = ""

print("CustomerTypeCV")
outdf.CustomerTypeCV = ""

print("DataPublicationDate")
outdf.DataPublicationDate = "11/03/2020"

print("DataPublicationDOI")
outdf.DataPublicationDOI = ""

print("InterbasinTransferFromID")
outdf.InterbasinTransferFromID = ""

print("InterbasinTransferToID")
outdf.InterbasinTransferToID = ""

print("IrrigatedAcreage")
outdf.IrrigatedAcreage = ""

print("IrrigationMethodCV")
outdf.IrrigationMethodCV = ""

print("PopulationServed")
outdf.PopulationServed = ""

print("PowerGeneratedGWh")
outdf.PowerGeneratedGWh = ""

print("PowerType")
outdf.PowerType = ""

print("PrimaryUseCategory")
outdf.PrimaryUseCategory = ""

print("ReportYearCV")
outdf['ReportYearCV'] = df_DM['inYear']

print("SDWISIdentifierCV")
outdf.SDWISIdentifierCV = ""

print("TimeframeEnd")
outdf.TimeframeEnd = ""

print("TimeframeStart")
outdf.TimeframeStart = ""

print("Resetting Index")
outdf.reset_index()

print("out df updates...")
outdf = outdf.replace(np.nan, '')  # Replaces NaN values with blank.
outdf100 = outdf


# Solving WaDE 2.0 Upload Issues
# ############################################################################
print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to QA here.

# None at the moment


#Error Checking each Field
############################################################################
print("Error checking each field.  Purging bad inputs.")  # Hardcoded
dfpurge = pd.DataFrame(columns=columnslist)  # purge DataFrame
dfpurge = dfpurge.assign(ReasonRemoved='')

# MethodUUID_nvarchar(250)_-
mask = outdf100.loc[ (outdf100["MethodUUID"].isnull()) | (outdf100["MethodUUID"] == '') | (outdf100['MethodUUID'].str.len() > 250) ].assign(ReasonRemoved='Bad MethodUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)  # Append to purge DataFrame
    dropIndex = outdf100.loc[ (outdf100["MethodUUID"].isnull()) | (outdf100["MethodUUID"] == '') | (outdf100['MethodUUID'].str.len() > 250) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# VariableSpecificUUID_nvarchar(250)_-
mask = outdf100.loc[ (outdf100["VariableSpecificUUID"].isnull()) | (outdf100["VariableSpecificUUID"] == '') | (outdf100['VariableSpecificUUID'].str.len() > 250) ].assign(ReasonRemoved='Bad VariableSpecificUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["VariableSpecificUUID"].isnull()) | (outdf100["VariableSpecificUUID"] == '') | (outdf100['VariableSpecificUUID'].str.len() > 250) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# WaterSourceUUID_nvarchar(250)_-
mask = outdf100.loc[ (outdf100["WaterSourceUUID"].isnull()) | (outdf100["WaterSourceUUID"] == '') | (outdf100['WaterSourceUUID'].str.len() > 250) ].assign(ReasonRemoved='Bad WaterSourceUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["WaterSourceUUID"].isnull()) | (outdf100["WaterSourceUUID"] == '') | (outdf100['WaterSourceUUID'].str.len() > 250) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# OrganizationUUID_nvarchar(250)_-
mask = outdf100.loc[ (outdf100["OrganizationUUID"].isnull()) | (outdf100["OrganizationUUID"] == '') | (outdf100['OrganizationUUID'].str.len() > 250) ].assign(ReasonRemoved='Bad OrganizationUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["OrganizationUUID"].isnull()) | (outdf100["OrganizationUUID"] == '') | (outdf100['OrganizationUUID'].str.len() > 250) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# ReportingUnitUUID_nvarchar(200)_-
mask = outdf100.loc[ (outdf100["ReportingUnitUUID"].isnull()) | (outdf100["ReportingUnitUUID"] == '') | (outdf100['ReportingUnitUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad ReportingUnitUUID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["ReportingUnitUUID"].isnull()) | (outdf100["ReportingUnitUUID"] == '') | (outdf100['ReportingUnitUUID'].str.len() > 200) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# AllocationCropDutyAmount_float_Yes
mask = outdf100.loc[ (outdf100['AllocationCropDutyAmount'].str.contains(',') == True) ].assign(ReasonRemoved='Bad AllocationCropDutyAmount').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100['AllocationCropDutyAmount'].str.contains(',') == True) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# Amount_float_-
mask = outdf100.loc[ (outdf100["Amount"].isnull()) | (outdf100["Amount"] == '') ].assign(ReasonRemoved='Bad Amount').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100["Amount"].isnull()) | (outdf100["Amount"] == '') ].index
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
mask = outdf100.loc[ outdf100["CommunityWaterSupplySystem"].str.len() > 250 ].assign(ReasonRemoved='Bad CommunityWaterSupplySystem').reset_index()
purge = outdf100[mask]
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["CommunityWaterSupplySystem"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# CropTypeCV_nvarchar(250)_Yes
mask = outdf100.loc[ outdf100["CropTypeCV"].str.len() > 250 ].assign(ReasonRemoved='Bad CropTypeCV').reset_index()
purge = outdf100[mask]
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["CropTypeCV"].str.len() > 250 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# DataPublicationDate_bigint_Yes
mask = outdf100.loc[ outdf100["DataPublicationDate"].str.contains(',') == True ].assign(ReasonRemoved='Bad DataPublicationDate').reset_index()
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

# InterbasinTransferFromID_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["InterbasinTransferFromID"].str.len() > 100 ].assign(ReasonRemoved='Bad InterbasinTransferFromID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["InterbasinTransferFromID"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# InterbasinTransferToID_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["InterbasinTransferToID"].str.len() > 100 ].assign(ReasonRemoved='Bad InterbasinTransferToID').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["InterbasinTransferToID"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# IrrigatedAcreage_float_Yes
mask = outdf100.loc[ (outdf100['IrrigatedAcreage'].str.contains(',') == True) ].assign(ReasonRemoved='Bad IrrigatedAcreage').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100['IrrigatedAcreage'].str.contains(',') == True) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# IrrigationMethodCV_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["IrrigationMethodCV"].str.len() > 100 ].assign(ReasonRemoved='Bad IrrigationMethodCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["IrrigationMethodCV"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# PopulationServed_bigint_Yes
mask = outdf100.loc[ outdf100["PopulationServed"].str.contains(',') == True ].assign(ReasonRemoved='Bad PopulationServed').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["PopulationServed"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# PowerGeneratedGWh_float_Yes
mask = outdf100.loc[ (outdf100['PowerGeneratedGWh'].str.contains(',') == True) ].assign(ReasonRemoved='Bad PowerGeneratedGWh').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ (outdf100['PowerGeneratedGWh'].str.contains(',') == True) ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# PowerType_nvarchar(50)_Yes
mask = outdf100.loc[ outdf100["PowerType"].str.len() > 50 ].assign(ReasonRemoved='Bad PowerType').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["PowerType"].str.len() > 50 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# PrimaryUseCategory_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["PrimaryUseCategory"].str.len() > 100 ].assign(ReasonRemoved='Bad PrimaryUseCategory').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["PrimaryUseCategory"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# year data we loaded in came in as an int.  That still works...
# # ReportYearCV_nchar(4)_Yes
# mask = outdf100.loc[ outdf100["ReportYearCV"].str.len() > 4 ].assign(ReasonRemoved='Bad ReportYearCV').reset_index()
# if len(mask.index) > 0:
#     dfpurge = dfpurge.append(mask)
#     dropIndex = outdf100.loc[ outdf100["ReportYearCV"].str.len() > 4 ].index
#     outdf100 = outdf100.drop(dropIndex)
#     outdf100 = outdf100.reset_index(drop=True)

# SDWISIdentifierCV_nvarchar(100)_Yes
mask = outdf100.loc[ outdf100["SDWISIdentifierCV"].str.len() > 100 ].assign(ReasonRemoved='Bad SDWISIdentifierCV').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["SDWISIdentifierCV"].str.len() > 100 ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# TimeframeEnd_bigint_Yes
mask = outdf100.loc[ outdf100["TimeframeEnd"].str.contains(',') == True ].assign(ReasonRemoved='Bad TimeframeEnd').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["TimeframeEnd"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# TimeframeStart_bigint_Yes
mask = outdf100.loc[ outdf100["TimeframeStart"].str.contains(',') == True ].assign(ReasonRemoved='Bad TimeframeStart').reset_index()
if len(mask.index) > 0:
    dfpurge = dfpurge.append(mask)
    dropIndex = outdf100.loc[ outdf100["TimeframeStart"].str.contains(',') == True ].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)


# Export to new csv
############################################################################
print("Exporting dataframe outdf100 to csv...")
# The working output DataFrame for WaDE 2.0 input.
outdf100.to_csv('ProcessedInputData/aggregatedamounts.csv', index=False)

# Report purged values.
if(len(dfpurge.index) > 0):
    dfpurge.to_csv('ProcessedInputData/aggregatedamounts_missing.csv')  # index=False,

print("Done.")


