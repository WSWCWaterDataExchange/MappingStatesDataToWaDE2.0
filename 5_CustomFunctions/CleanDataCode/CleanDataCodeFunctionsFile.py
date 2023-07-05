# Last Update: 04/27/2023
# Purpose: To clean the data and ensure proper data types are being used for WaDE inputs.
# review cv terminology and assign 'WaDE Blank' values to comma separated values. Temp fix for some CV terms.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Function
############################################################################


def fixEmptyStringFunc(val):
    val = str(val).strip()
    if val == "" or val == " " or val == "nan" or val == "nan,nan" or pd.isnull(val):
        outString = "WaDE Blank"
    else:
        outString = val
    return outString


def FixWaterSourceInfoFunctions(outdf):
    # ---- Fix Empty Strings ----
    outdf['WaterSourceName'] = outdf.apply(lambda row: fixEmptyStringFunc(row['WaterSourceName']), axis=1)
    outdf['WaterSourceTypeCV'] = outdf.apply(lambda row: fixEmptyStringFunc(row['WaterSourceTypeCV']), axis=1)
    return (outdf)


def FixSiteInfoFunctions(outdf):
    # ---- Fix Empty Strings ----
    outdf['CoordinateAccuracy'] = outdf.apply(lambda row: fixEmptyStringFunc(row['CoordinateAccuracy']), axis=1)
    outdf['CoordinateMethodCV'] = outdf.apply(lambda row: fixEmptyStringFunc(row['CoordinateMethodCV']), axis=1)
    outdf['County'] = outdf.apply(lambda row: fixEmptyStringFunc(row['County']), axis=1)
    outdf['SiteName'] = outdf.apply(lambda row: fixEmptyStringFunc(row['SiteName']), axis=1)
    outdf['SiteTypeCV'] = outdf.apply(lambda row: fixEmptyStringFunc(row['SiteTypeCV']), axis=1)
    # ---- Fix Lat and Long Values ----
    outdf['Latitude'] = pd.to_numeric(outdf['Latitude'], errors='coerce').fillna(0)
    outdf['Longitude'] = pd.to_numeric(outdf['Longitude'], errors='coerce').fillna(0)
    return (outdf)


def FixAllocationAmountInfoFunctions(outdf):
    # ---- Fix Empty Strings ----
    outdf['AllocationBasisCV'] = outdf.apply(lambda row: fixEmptyStringFunc(row['AllocationBasisCV']), axis=1)
    outdf['AllocationLegalStatusCV'] = outdf.apply(lambda row: fixEmptyStringFunc(row['AllocationLegalStatusCV']), axis=1)
    outdf['AllocationOwner'] = outdf.apply(lambda row: fixEmptyStringFunc(row['AllocationOwner']), axis=1)
    outdf['AllocationTypeCV'] = outdf.apply(lambda row: fixEmptyStringFunc(row['AllocationTypeCV']), axis=1)
    outdf['BeneficialUseCategory'] = outdf.apply(lambda row: fixEmptyStringFunc(row['BeneficialUseCategory']), axis=1)
    # ---- Fix Priority Date Value ----
    outdf['AllocationPriorityDate'] = pd.to_datetime(outdf['AllocationPriorityDate'], errors='coerce')
    outdf['AllocationPriorityDate'] = pd.to_datetime(outdf['AllocationPriorityDate'].dt.strftime('%m/%d/%Y'))
    # ---- Fix Float Values ----
    outdf['AllocationFlow_CFS'] = pd.to_numeric(outdf['AllocationFlow_CFS'], errors='coerce').fillna(0)
    outdf['AllocationVolume_AF'] = pd.to_numeric(outdf['AllocationVolume_AF'], errors='coerce').fillna(0)
    outdf['IrrigatedAcreage'] = pd.to_numeric(outdf['IrrigatedAcreage'], errors='coerce').fillna(0)
    return (outdf)


def FixAggregatedAmountsInfoFunctions(outdf):
    # ---- Fix Empty Strings ----
    outdf['BeneficialUseCategory'] = outdf.apply(lambda row: fixEmptyStringFunc(row['BeneficialUseCategory']), axis=1)
    # ---- Fix Date Value ----
    outdf['TimeframeEnd'] = pd.to_datetime(outdf['TimeframeEnd'], errors='coerce')
    outdf['TimeframeStart'] = pd.to_datetime(outdf['TimeframeStart'], errors='coerce')
    # ---- Fix Float Values ----
    outdf['Amount'] = pd.to_numeric(outdf['Amount'], errors='coerce').fillna(0)
    return (outdf)


def FixSiteSpecificAmountsInfoFunctions(outdf):
    # ---- Fix Empty Strings ----
    outdf['BeneficialUseCategory'] = outdf.apply(lambda row: fixEmptyStringFunc(row['BeneficialUseCategory']), axis=1)
    # ---- Fix Date Value ----
    outdf['TimeframeEnd'] = pd.to_datetime(outdf['TimeframeEnd'], errors='coerce')
    outdf['TimeframeStart'] = pd.to_datetime(outdf['TimeframeStart'], errors='coerce')
    # ---- Fix Float Values ----
    outdf['Amount'] = pd.to_numeric(outdf['Amount'], errors='coerce').fillna(0)
    return (outdf)