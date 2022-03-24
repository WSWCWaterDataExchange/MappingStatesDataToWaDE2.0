# Last Update: 03/03/2022
# Purpose: To have a single function file to error check datatypes.
# Index:
#   WaterSources
#   Sites
#   ReportingUnits
#   AllocationsAmounts_facts
#   AggregatedAmounts_facts
#   SiteSpecificAmounts_fact
#   RegulatoryOverlay


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# WaterSources
########################################################################################################################
########################################################################################################################

# WaterSourceUUID_nvarchar(250)_-
def WaterSourceUUID_WS_Check(dfx, dfy):
    mask = dfx.loc[(dfx["WaterSourceUUID"].isnull()) |
                   (dfx["WaterSourceUUID"] == '') |
                   (dfx['WaterSourceUUID'].str.len() > 250)].assign(ReasonRemoved='Incomplete WaterSourceUUID').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['WaterSourceUUID']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[(dfx["WaterSourceUUID"].isnull()) |
                            (dfx["WaterSourceUUID"] == '') |
                            (dfx['WaterSourceUUID'].str.len() > 250)].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# Geometry_geometry_Yes
# ???? How to check for geometry datatype

# GNISFeatureNameCV_nvarchar(250)_Yes
def GNISFeatureNameCV_WS_Check(dfx, dfy):
    mask = dfx.loc[dfx["GNISFeatureNameCV"].str.len() > 250].assign(ReasonRemoved='Incomplete GNISFeatureNameCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['GNISFeatureNameCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[dfx["GNISFeatureNameCV"].str.len() > 250].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterQualityIndicatorCV_nvarchar(100)_-
def WaterQualityIndicatorCV_WS_Check(dfx, dfy):
    mask = dfx.loc[(dfx["WaterQualityIndicatorCV"].isnull()) |
                   (dfx["WaterQualityIndicatorCV"] == '') |
                   (dfx['WaterQualityIndicatorCV'].str.len() > 250)].assign(ReasonRemoved='Incomplete WaterQualityIndicatorCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['WaterQualityIndicatorCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[(dfx["WaterQualityIndicatorCV"].isnull()) |
                            (dfx["WaterQualityIndicatorCV"] == '') |
                            (dfx['WaterQualityIndicatorCV'].str.len() > 250)].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterSourceName_nvarchar(250)_Yes
def WaterSourceName_WS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["WaterSourceName"].astype(str).str.len() > 250 ].assign(ReasonRemoved='Incomplete WaterSourceName').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['WaterSourceName']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["WaterSourceName"].astype(str).str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterSourceNativeID_nvarchar(250)_Yes
def WaterSourceNativeID_WS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["WaterSourceNativeID"].astype(str).str.len() > 250 ].assign(ReasonRemoved='Incomplete WaterSourceNativeID').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['WaterSourceNativeID']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["WaterSourceNativeID"].astype(str).str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterSourceTypeCV_nvarchar(100)_-
def WaterSourceTypeCV_WS_Check(dfx, dfy):
    mask = dfx.loc[(dfx["WaterSourceTypeCV"].isnull()) |
                   (dfx["WaterSourceTypeCV"] == '') |
                   (dfx['WaterSourceTypeCV'].str.len() > 100)].assign(ReasonRemoved='Incomplete WaterSourceTypeCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['WaterSourceTypeCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[(dfx["WaterSourceTypeCV"].isnull()) |
                            (dfx["WaterSourceTypeCV"] == '') |
                            (dfx['WaterSourceTypeCV'].str.len() > 100)].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)


# # Sites
# ########################################################################################################################
# ########################################################################################################################
#
# # SiteUUID_nvarchar(200)_
# def SiteUUID_S_Check(dfx, dfy):
#     mask = dfx.loc[ (dfx["SiteUUID"].isnull()) |
#                     (dfx["SiteUUID"] == '') |
#                     (dfx['SiteUUID'].str.len() > 200) ].assign(ReasonRemoved='Incomplete SiteUUID').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['SiteUUID']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ (dfx["SiteUUID"].isnull()) |
#                              (dfx["SiteUUID"] == '') |
#                              (dfx['SiteUUID'].str.len() > 200) ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # CoordinateAccuracy_nvarchar(255)_Yes
# def CoordinateAccuracy_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["CoordinateAccuracy"].str.len() > 255 ].assign(ReasonRemoved='Incomplete CoordinateAccuracy').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['CoordinateAccuracy']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["CoordinateAccuracy"].str.len() > 255 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # CoordinateMethodCV_nvarchar(100)_-
# def CoordinateMethodCV_S_Check(dfx, dfy):
#     mask = dfx.loc[ (dfx["CoordinateMethodCV"].isnull()) |
#                     (dfx["CoordinateMethodCV"] == '') |
#                     (dfx['CoordinateMethodCV'].str.len() > 100) ].assign(ReasonRemoved='Incomplete CoordinateMethodCV').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['CoordinateMethodCV']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ (dfx["CoordinateMethodCV"].isnull()) |
#                              (dfx["CoordinateMethodCV"] == '') |
#                              (dfx['CoordinateMethodCV'].str.len() > 100) ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # County_nvarchar(20)_Yes
# def County_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["County"].str.len() > 20 ].assign(ReasonRemoved='Incomplete County').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['County']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["County"].str.len() > 20 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # EPSGCodeCV_nvarchar(50)_-
# def EPSGCodeCV_S_Check(dfx, dfy):
#     mask = dfx.loc[ (dfx["EPSGCodeCV"].isnull()) |
#                     (dfx["EPSGCodeCV"] == '') |
#                     (dfx['EPSGCodeCV'].str.len() > 50) ].assign(ReasonRemoved='Incomplete EPSGCodeCV').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['EPSGCodeCV']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ (dfx["EPSGCodeCV"].isnull()) |
#                              (dfx["EPSGCodeCV"] == '') |
#                              (dfx['EPSGCodeCV'].str.len() > 50) ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # Geometry_geometry_Yes
# # ???? How to check for geometry datatype
#
# # GNISCodeCV_nvarchar(250)_Yes
# def GNISCodeCV_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["GNISCodeCV"].astype(str).str.len() > 250 ].assign(ReasonRemoved='Incomplete GNISCodeCV').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['GNISCodeCV']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["GNISCodeCV"].astype(str).str.len() > 250 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # HUC12_nvarchar(20)_Yes
# def HUC12_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["HUC12"].astype(str).str.len() > 20 ].assign(ReasonRemoved='Incomplete HUC12').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['HUC12']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["HUC12"].astype(str).str.len() > 20 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # HUC8_nvarchar(20)_Yes
# def HUC8_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["HUC8"].astype(str).str.len() > 20 ].assign(ReasonRemoved='Incomplete HUC8').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['HUC8']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["HUC8"].astype(str).str.len() > 20 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # Latitude_float_-
# # (dfx["Latitude"] < 20.0)
# def Latitude_S_Check(dfx, dfy):
#     mask = dfx.loc[ (dfx["Latitude"].isnull()) |
#                     (dfx["Latitude"] == "")].assign(ReasonRemoved='Incomplete Latitude').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['Latitude']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ (dfx["Latitude"].isnull()) |
#                              (dfx["Latitude"] == "")].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # Longitude_float_-
# # (dfx["Longitude"] > -80)
# def Longitude_S_Check(dfx, dfy):
#     mask = dfx.loc[ (dfx["Longitude"].isnull()) |
#                     (dfx["Longitude"] == "")].assign(ReasonRemoved='Incomplete Longitude').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['Longitude']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ (dfx["Longitude"].isnull()) |
#                              (dfx["Longitude"] == "")].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # NHDNetworkStatusCV_nvarchar(50)_Yes
# def NHDNetworkStatusCV_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["NHDNetworkStatusCV"].str.len() > 50 ].assign(ReasonRemoved='Incomplete NHDNetworkStatusCV').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['NHDNetworkStatusCV']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["NHDNetworkStatusCV"].str.len() > 50 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # NHDProductCV_nvarchar(50)_Yes
# def NHDProductCV_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["NHDProductCV"].str.len() > 50 ].assign(ReasonRemoved='Incomplete NHDProductCV').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['NHDProductCV']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["NHDProductCV"].str.len() > 50 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # PODorPOUSite_nvarchar(50)_Yes
# def PODorPOUSite_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["PODorPOUSite"].str.len() > 50 ].assign(ReasonRemoved='Incomplete PODorPOUSite').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['PODorPOUSite']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["PODorPOUSite"].str.len() > 50 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # RegulatoryOverlayUUIDs_nvarchar(200)_
# def RegulatoryOverlayUUIDs_S_Check(dfx, dfy):
#     mask = dfx.loc[ (dfx['RegulatoryOverlayUUIDs'].str.len() > 200) ].assign(ReasonRemoved='Incomplete ReportingUnitUUID').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['RegulatoryOverlayUUIDs']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ (dfx['RegulatoryOverlayUUIDs'].str.len() > 200) ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # SiteName_nvarchar(500)_
# def SiteName_S_Check(dfx, dfy):
#     mask = dfx.loc[ (dfx["SiteName"].isnull()) |
#                     (dfx["SiteName"] == '') |
#                     (dfx['SiteName'].str.len() > 500) ].assign(ReasonRemoved='Incomplete SiteName').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['SiteName']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ (dfx["SiteName"].isnull()) |
#                              (dfx["SiteName"] == '') |
#                              (dfx['SiteName'].str.len() > 500) ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # SiteNativeID_nvarchar(50)_Yes
# def SiteNativeID_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["SiteNativeID"].astype(str).str.len() > 50 ].assign(ReasonRemoved='Incomplete SiteNativeID').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['SiteNativeID']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["SiteNativeID"].astype(str).str.len() > 50 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # SitePoint_geometry_Yes
# # ???? How to check for geometry datatype
#
# # SiteTypeCV_nvarchar(100)_Yes
# def SiteTypeCV_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["SiteTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete SiteTypeCV').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['SiteTypeCV']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["SiteTypeCV"].str.len() > 100 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # StateCV_nvarchar(2)_Yes
# def StateCV_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["StateCV"].str.len() > 2 ].assign(ReasonRemoved='Incomplete StateCV').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['StateCV']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["StateCV"].str.len() > 2 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # USGSSiteID_nvarchar(250)_Yes
# def USGSSiteID_S_Check(dfx, dfy):
#     mask = dfx.loc[ dfx["USGSSiteID"].str.len() > 250 ].assign(ReasonRemoved='Incomplete USGSSiteID').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['USGSSiteID']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ dfx["USGSSiteID"].str.len() > 250 ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)
#
# # WaterSourceUUIDs_nvarchar(200)_-
# def WaterSourceUUIDs_S_Check(dfx, dfy):
#     mask = dfx.loc[ (dfx['WaterSourceUUIDs'].str.len() > 200) ].assign(ReasonRemoved='Incomplete WaterSourceUUIDs').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['UUID'] = mask['UUID']
#         outmaskdf['IncompleteField_1'] = mask['WaterSourceUUIDs']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[ (dfx['WaterSourceUUIDs'].str.len() > 200) ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)


# Sites
########################################################################################################################
########################################################################################################################

# SiteUUID_nvarchar(200)_
def SiteUUID_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["SiteUUID"].isnull()) |
                    (dfx["SiteUUID"] == '') |
                    (dfx['SiteUUID'].str.len() > 200) ].assign(ReasonRemoved='Incomplete SiteUUID').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['SiteUUID']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["SiteUUID"].isnull()) |
                             (dfx["SiteUUID"] == '') |
                             (dfx['SiteUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CoordinateAccuracy_nvarchar(255)_Yes
def CoordinateAccuracy_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CoordinateAccuracy"].str.len() > 255 ].assign(ReasonRemoved='Incomplete CoordinateAccuracy').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['CoordinateAccuracy']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["CoordinateAccuracy"].str.len() > 255 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CoordinateMethodCV_nvarchar(100)_-
def CoordinateMethodCV_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["CoordinateMethodCV"].isnull()) |
                    (dfx["CoordinateMethodCV"] == '') |
                    (dfx['CoordinateMethodCV'].str.len() > 100) ].assign(ReasonRemoved='Incomplete CoordinateMethodCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['CoordinateMethodCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["CoordinateMethodCV"].isnull()) |
                             (dfx["CoordinateMethodCV"] == '') |
                             (dfx['CoordinateMethodCV'].str.len() > 100) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# County_nvarchar(20)_Yes
def County_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["County"].str.len() > 20) |
                    (dfx["County"].str.contains(',') == True) ].assign(ReasonRemoved='Incomplete County').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['County']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["County"].str.len() > 20) |
                             (dfx["County"].str.contains(',') == True) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# EPSGCodeCV_nvarchar(50)_-
def EPSGCodeCV_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["EPSGCodeCV"].isnull()) |
                    (dfx["EPSGCodeCV"] == '') |
                    (dfx['EPSGCodeCV'].str.len() > 50) ].assign(ReasonRemoved='Incomplete EPSGCodeCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['EPSGCodeCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["EPSGCodeCV"].isnull()) |
                             (dfx["EPSGCodeCV"] == '') |
                             (dfx['EPSGCodeCV'].str.len() > 50) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# Geometry_geometry_Yes
# ???? How to check for geometry datatype

# GNISCodeCV_nvarchar(250)_Yes
def GNISCodeCV_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["GNISCodeCV"].astype(str).str.len() > 250 ].assign(ReasonRemoved='Incomplete GNISCodeCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['GNISCodeCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["GNISCodeCV"].astype(str).str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# HUC12_nvarchar(20)_Yes
def HUC12_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["HUC12"].astype(str).str.len() > 20 ].assign(ReasonRemoved='Incomplete HUC12').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['HUC12']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["HUC12"].astype(str).str.len() > 20 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# HUC8_nvarchar(20)_Yes
def HUC8_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["HUC8"].astype(str).str.len() > 20 ].assign(ReasonRemoved='Incomplete HUC8').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['HUC8']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["HUC8"].astype(str).str.len() > 20 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# Latitude_float_-
def Latitude_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["Latitude"].isnull()) |
                    (dfx["Latitude"] == "")].assign(ReasonRemoved='Incomplete Latitude').reset_index()
    if len(mask.index) > 0:
        mask = mask.assign(ReasonRemoved='Incomplete Latitude')
        mask = mask.assign(UUID=mask['UUID'])
        mask = mask.assign(IncompleteField_1=mask['Latitude'])
        dfy = dfy.append(mask)

        dropIndex = dfx.loc[ (dfx["Latitude"].isnull()) |
                             (dfx["Latitude"] == "")].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# Longitude_float_-
def Longitude_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["Longitude"].isnull()) |
                    (dfx["Longitude"] == "")].assign(ReasonRemoved='Incomplete Longitude').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['Longitude']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["Longitude"].isnull()) |
                             (dfx["Longitude"] == "")].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# NHDNetworkStatusCV_nvarchar(50)_Yes
def NHDNetworkStatusCV_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["NHDNetworkStatusCV"].str.len() > 50 ].assign(ReasonRemoved='Incomplete NHDNetworkStatusCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['NHDNetworkStatusCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["NHDNetworkStatusCV"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# NHDProductCV_nvarchar(50)_Yes
def NHDProductCV_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["NHDProductCV"].str.len() > 50 ].assign(ReasonRemoved='Incomplete NHDProductCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['NHDProductCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["NHDProductCV"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PODorPOUSite_nvarchar(50)_Yes
def PODorPOUSite_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PODorPOUSite"].str.len() > 50 ].assign(ReasonRemoved='Incomplete PODorPOUSite').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['PODorPOUSite']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["PODorPOUSite"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# RegulatoryOverlayUUIDs_nvarchar(200)_
def RegulatoryOverlayUUIDs_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx['RegulatoryOverlayUUIDs'].str.len() > 200) ].assign(ReasonRemoved='Incomplete ReportingUnitUUID').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['RegulatoryOverlayUUIDs']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx['RegulatoryOverlayUUIDs'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SiteName_nvarchar(500)_
def SiteName_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["SiteName"].isnull()) |
                    (dfx["SiteName"] == '') |
                    (dfx['SiteName'].str.len() > 500) ].assign(ReasonRemoved='Incomplete SiteName').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['SiteName']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["SiteName"].isnull()) |
                             (dfx["SiteName"] == '') |
                             (dfx['SiteName'].str.len() > 500) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SiteNativeID_nvarchar(50)_Yes
def SiteNativeID_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["SiteNativeID"].astype(str).str.len() > 50 ].assign(ReasonRemoved='Incomplete SiteNativeID').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['SiteNativeID']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["SiteNativeID"].astype(str).str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SitePoint_geometry_Yes
# ???? How to check for geometry datatype

# SiteTypeCV_nvarchar(100)_Yes
def SiteTypeCV_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["SiteTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete SiteTypeCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['SiteTypeCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["SiteTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# StateCV_nvarchar(2)_Yes
def StateCV_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["StateCV"].str.len() > 2 ].assign(ReasonRemoved='Incomplete StateCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['StateCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["StateCV"].str.len() > 2 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# USGSSiteID_nvarchar(250)_Yes
def USGSSiteID_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["USGSSiteID"].str.len() > 250 ].assign(ReasonRemoved='Incomplete USGSSiteID').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['USGSSiteID']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["USGSSiteID"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterSourceUUIDs_nvarchar(200)_-
def WaterSourceUUIDs_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx['WaterSourceUUIDs'].str.len() > 200) ].assign(ReasonRemoved='Incomplete WaterSourceUUIDs').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['WaterSourceUUIDs']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx['WaterSourceUUIDs'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)


# ReportingUnits
########################################################################################################################
########################################################################################################################

# ReportingUnitUUID_nvarchar(200)_
def ReportingUnitUUID_RU_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["ReportingUnitUUID"].isnull()) |
                    (dfx["ReportingUnitUUID"] == '') |
                    (dfx['ReportingUnitUUID'].str.len() > 200) ].assign(ReasonRemoved='Incomplete ReportingUnitUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["ReportingUnitUUID"].isnull()) |
                             (dfx["ReportingUnitUUID"] == '') |
                             (dfx['ReportingUnitUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# EPSGCodeCV_nvarchar(50)_Yes
def EPSGCodeCV_RU_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["EPSGCodeCV"].isnull()) |
                    (dfx["EPSGCodeCV"] == '') |
                    (dfx['EPSGCodeCV'].str.len() > 50) ].assign(ReasonRemoved='Incomplete EPSGCodeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["EPSGCodeCV"].isnull()) |
                             (dfx["EPSGCodeCV"] == '') |
                             (dfx['EPSGCodeCV'].str.len() > 50) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# Geometry_Geometry_Yes
# Not sure how to check for this...

# ReportingUnitName_nvarchar(250)_
def ReportingUnitName_RU_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["ReportingUnitName"].isnull()) |
                    (dfx["ReportingUnitName"] == '') |
                    (dfx['ReportingUnitName'].astype(str).str.len() > 250) ].assign(ReasonRemoved='Incomplete ReportingUnitName').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["ReportingUnitName"].isnull()) |
                             (dfx["ReportingUnitName"] == '') |
                             (dfx['ReportingUnitName'].astype(str).str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# ReportingUnitNativeID_nvarchar(250)_
def ReportingUnitNativeID_RU_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["ReportingUnitNativeID"].isnull()) |
                    (dfx["ReportingUnitNativeID"] == '') |
                    (dfx['ReportingUnitNativeID'].astype(str).str.len() > 250) ].assign(ReasonRemoved='Incomplete ReportingUnitNativeID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["ReportingUnitNativeID"].isnull()) |
                             (dfx["ReportingUnitNativeID"] == '') |
                             (dfx['ReportingUnitNativeID'].astype(str).str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# ReportingUnitProductVersion_nvarchar(100)_Yes
def ReportingUnitProductVersion_RU_Check(dfx, dfy):
    mask = dfx.loc[ dfx["ReportingUnitProductVersion"].str.len() > 100 ].assign(ReasonRemoved='Incomplete ReportingUnitProductVersion').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["ReportingUnitProductVersion"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)


# ReportingUnitTypeCV_nvarchar(20)_
def ReportingUnitTypeCV_RU_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["ReportingUnitTypeCV"].isnull()) |
                    (dfx["ReportingUnitTypeCV"] == '') |
                    (dfx['ReportingUnitTypeCV'].str.len() > 50) ].assign(ReasonRemoved='Incomplete ReportingUnitTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["ReportingUnitTypeCV"].isnull()) |
                             (dfx["ReportingUnitTypeCV"] == '') |
                             (dfx['ReportingUnitTypeCV'].str.len() > 50) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# ReportingUnitUpdateDate_Date_Yes
def ReportingUnitUpdateDate_RU_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["ReportingUnitUpdateDate"].str.contains(',')) ].assign(ReasonRemoved='Incomplete ReportingUnitUpdateDate').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["ReportingUnitUpdateDate"].str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# StateCV_nvarchar(2)_
def StateCV_RU_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["StateCV"].isnull()) |
                    (dfx["StateCV"] == '') |
                    (dfx['StateCV'].str.len() > 2) ].assign(ReasonRemoved='Incomplete StateCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["StateCV"].isnull()) |
                             (dfx["StateCV"] == '') |
                             (dfx['StateCV'].str.len() > 2) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)



# AllocationsAmounts_facts
########################################################################################################################
########################################################################################################################

# MethodUUID_nvarchar(200)_-
def MethodUUID_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["MethodUUID"].isnull()) |
                    (dfx["MethodUUID"] == '') |
                    (dfx['MethodUUID'].str.len() > 200) ].assign(ReasonRemoved='Incomplete MethodUUID').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['MethodUUID']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["MethodUUID"].isnull()) |
                             (dfx["MethodUUID"] == '') |
                             (dfx['MethodUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# VariableSpecificUUID_nvarchar(200)_-
def VariableSpecificUUID_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["VariableSpecificUUID"].isnull()) |
                    (dfx["VariableSpecificUUID"] == '') |
                    (dfx['VariableSpecificUUID'].str.len() > 200) ].assign(ReasonRemoved='Incomplete VariableSpecificUUID').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['VariableSpecificUUID']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["VariableSpecificUUID"].isnull()) |
                             (dfx["VariableSpecificUUID"] == '') |
                             (dfx['VariableSpecificUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# OrganizationUUID_nvarchar(200)_-
def OrganizationUUID_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["OrganizationUUID"].isnull()) |
                    (dfx["OrganizationUUID"] == '') |
                    (dfx['OrganizationUUID'].str.len() > 200) ].assign(ReasonRemoved='Incomplete OrganizationUUID').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['OrganizationUUID']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["OrganizationUUID"].isnull()) |
                             (dfx["OrganizationUUID"] == '') |
                             (dfx['OrganizationUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SiteUUID_nvarchar(max)_-
def SiteUUID_AA_Check(dfx, dfy):
    mask = dfx.loc[(dfx["SiteUUID"].isnull()) |
                   (dfx["SiteUUID"] == '') ].assign(ReasonRemoved='Incomplete SiteUUID').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['SiteUUID']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[(dfx["SiteUUID"].isnull()) |
                            (dfx["SiteUUID"] == '') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationApplicationDate_date_Yes
def AllocationApplicationDate_AA_Check(dfx, dfy):
    mask = dfx.loc[dfx["AllocationApplicationDate"].str.contains(',') == True].assign(ReasonRemoved='Incomplete AllocationApplicationDate').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationApplicationDate']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationApplicationDate"].str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationAssociatedConsumptiveUseSiteIDs_nvarchar(500)_Yes
def AllocationAssociatedConsumptiveUseSiteIDs_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationAssociatedConsumptiveUseSiteIDs"].str.len() > 500 ].assign(ReasonRemoved='Incomplete AllocationAssociatedConsumptiveUseSiteIDs').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationAssociatedConsumptiveUseSiteIDs']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationAssociatedConsumptiveUseSiteIDs"].str.len() > 500 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationAssociatedWithdrawalSiteIDs_nvarchar(500)_Yes
def AllocationAssociatedWithdrawalSiteIDs_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationAssociatedWithdrawalSiteIDs"].str.len() > 500 ].assign(ReasonRemoved='Incomplete AllocationAssociatedWithdrawalSiteIDs').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationAssociatedWithdrawalSiteIDs']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationAssociatedWithdrawalSiteIDs"].str.len() > 500 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationBasisCV_nvarchar(250)_Yes
def AllocationBasisCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationBasisCV"].str.len() > 250 ].assign(ReasonRemoved='Incomplete AllocationBasisCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationBasisCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationBasisCV"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationChangeApplicationIndicator_nvarchar(100)_Yes
def AllocationChangeApplicationIndicator_AA_Check(dfx, dfy):
    mask= dfx.loc[ dfx["AllocationChangeApplicationIndicator"].str.len() > 100 ].assign(ReasonRemoved='Incomplete AllocationChangeApplicationIndicator').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationChangeApplicationIndicator']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationChangeApplicationIndicator"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationCommunityWaterSupplySystem_nvarchar(250)_Yes
def AllocationCommunityWaterSupplySystem_AA_Check(dfx, dfy):
    mask= dfx.loc[ dfx["AllocationCommunityWaterSupplySystem"].str.len() > 250 ].assign(ReasonRemoved='Incomplete AllocationCommunityWaterSupplySystem').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationCommunityWaterSupplySystem']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationCommunityWaterSupplySystem"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationCropDutyAmount_float_Yes
def AllocationCropDutyAmount_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationCropDutyAmount"].str.contains(',') == True ].assign(ReasonRemoved='Incomplete AllocationCropDutyAmount').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationCropDutyAmount']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationCropDutyAmount"].str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationExpirationDate_string_Yes
def AllocationExpirationDate_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationExpirationDate"].str.contains(',') == True ].assign(ReasonRemoved='Incomplete AllocationExpirationDate').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationExpirationDate']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationExpirationDate"].str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationFlow_CFS_float_Yes & AllocationVolume_AF_float_Yes
# We have to have either a flow or a volume
def AllocationFlowVolume_CFSAF_float_Yes_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx['ExemptOfVolumeFlowPriority'] == "0") &
                    (((dfx["AllocationFlow_CFS"].isnull()) |
                      (dfx["AllocationFlow_CFS"] == "") |
                      (dfx['AllocationFlow_CFS'].astype(str).str.contains(','))) &
                     ((dfx["AllocationVolume_AF"].isnull()) |
                      (dfx["AllocationVolume_AF"] == "") |
                      (dfx['AllocationVolume_AF'].astype(str).str.contains(',')))) ].assign(ReasonRemoved='Incomplete Flow or Volume').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1", "IncompleteField_2"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationFlow_CFS']
        outmaskdf['IncompleteField_2'] = mask['AllocationVolume_AF']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx['ExemptOfVolumeFlowPriority'] == "0") &
                             (((dfx["AllocationFlow_CFS"].isnull()) |
                               (dfx["AllocationFlow_CFS"] == "") |
                               (dfx['AllocationFlow_CFS'].astype(str).str.contains(','))) &
                              ((dfx["AllocationVolume_AF"].isnull()) |
                               (dfx["AllocationVolume_AF"] == "") |
                               (dfx['AllocationVolume_AF'].astype(str).str.contains(',')))) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)


# AllocationLegalStatusCV_nvarchar(250)_Yes
def AllocationLegalStatusCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["AllocationLegalStatusCV"].str.len() > 250) |
                    (dfx['AllocationLegalStatusCV'].str.contains(',')) ].assign(ReasonRemoved='Incomplete AllocationLegalStatusCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationLegalStatusCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["AllocationLegalStatusCV"].str.len() > 250) |
                             (dfx['AllocationLegalStatusCV'].str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationNativeID_nvarchar(250)_Yes
def AllocationNativeID_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationNativeID"].str.len() > 250 ].assign(ReasonRemoved='Incomplete AllocationNativeID').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationNativeID']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationNativeID"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationOwner_nvarchar(500)_Yes
def AllocationOwner_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationOwner"].str.len() > 500 ].assign(ReasonRemoved='Incomplete AllocationOwner').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationOwner']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationOwner"].str.len() > 500 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationPriorityDate_string_-
def AllocationPriorityDate_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx['ExemptOfVolumeFlowPriority'] == "0") &
                    ((dfx["AllocationPriorityDate"].isnull()) |
                     (dfx["AllocationPriorityDate"] == "") |
                     (dfx["AllocationPriorityDate"] == " ") |
                     (dfx["AllocationPriorityDate"].str.contains(','))) ].assign(ReasonRemoved='Incomplete AllocationPriorityDate').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationPriorityDate']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx['ExemptOfVolumeFlowPriority'] == "0") &
                             ((dfx["AllocationPriorityDate"].isnull()) |
                              (dfx["AllocationPriorityDate"] == "") |
                              (dfx["AllocationPriorityDate"] == " ") |
                              (dfx["AllocationPriorityDate"].str.contains(','))) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationTimeframeEnd_nvarchar(5)_Yes
def AllocationTimeframeEnd_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationTimeframeEnd"].str.len() > 5 ].assign(ReasonRemoved='Incomplete AllocationTimeframeEnd').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationTimeframeEnd']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationTimeframeEnd"].str.len() > 5 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationTimeframeStart_nvarchar(5)_Yes
def AllocationTimeframeStart_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationTimeframeStart"].str.len() > 5 ].assign(ReasonRemoved='Incomplete AllocationTimeframeStart').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationTimeframeStart']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationTimeframeStart"].str.len() > 5 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationTypeCV_nvarchar(250)_Yes
def AllocationTypeCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["AllocationTypeCV"].str.len() > 250) |
                    (dfx["AllocationTypeCV"].str.contains(',')) ].assign(ReasonRemoved='Incomplete AllocationTypeCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationTypeCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["AllocationTypeCV"].str.len() > 250) |
                             (dfx["AllocationTypeCV"].str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# BeneficialUseCategory_nvarchar(100)_-
# We are ignoring nvarchar length in the check at this time
def BeneficialUseCategory_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["BeneficialUseCategory"].isnull()) |
                    (dfx["BeneficialUseCategory"] == '') ].assign(ReasonRemoved='Incomplete BeneficialUseCategory').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['BeneficialUseCategory']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["BeneficialUseCategory"].isnull()) |
                             (dfx["BeneficialUseCategory"] == '') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# # CommunityWaterSupplySystem_nvarchar(250)_Yes
def CommunityWaterSupplySystem_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CommunityWaterSupplySystem"].str.len() > 250 ].assign(ReasonRemoved='Incomplete CommunityWaterSupplySystem').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['CommunityWaterSupplySystem']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["CommunityWaterSupplySystem"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CropTypeCV_nvarchar(100)_Yes
def CropTypeCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CropTypeCV"].str.len() > 250 ].assign(ReasonRemoved='Incomplete CropTypeCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['CropTypeCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["CropTypeCV"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CustomerTypeCV_nvarchar(100)_Yes
def CustomerTypeCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete CustomerTypeCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['CustomerTypeCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDate_string_-
def DataPublicationDate_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["DataPublicationDate"].isnull()) | (dfx["DataPublicationDate"] == '') | (dfx["DataPublicationDate"].str.contains(',') == True) ].assign(ReasonRemoved='Incomplete DataPublicationDate').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['DataPublicationDate']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["DataPublicationDate"].isnull()) | (dfx["DataPublicationDate"] == '') | (dfx["DataPublicationDate"].str.contains(',') == True)  ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDOI_nvarchar(100)_Yes
def DataPublicationDOI_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["DataPublicationDOI"].str.len() > 100 ].assign(ReasonRemoved='Incomplete DataPublicationDOI').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['DataPublicationDOI']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["DataPublicationDOI"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# ExemptOfVolumeFlowPriority_bit_Yes
def ExemptOfVolumeFlowPriority_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["ExemptOfVolumeFlowPriority"] > 1) ].assign(ReasonRemoved='Incomplete ExemptOfVolumeFlowPriority').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['ExemptOfVolumeFlowPriority']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ (dfx["ExemptOfVolumeFlowPriority"] > 1) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# GeneratedPowerCapacityMW_float_Yes
def GeneratedPowerCapacityMW_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["GeneratedPowerCapacityMW"].astype(str).str.contains(',') == True ].assign(ReasonRemoved='Incomplete GeneratedPowerCapacityMW').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['GeneratedPowerCapacityMW']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["GeneratedPowerCapacityMW"].astype(str).str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# IrrigatedAcreage_float_Yes
def IrrigatedAcreage_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["IrrigatedAcreage"].astype(str).str.contains(',') == True ].assign(ReasonRemoved='Incomplete IrrigatedAcreage').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['IrrigatedAcreage']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["IrrigatedAcreage"].astype(str).str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# IrrigationMethodCV_nvarchar(100)_Yes
def IrrigationMethodCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["IrrigationMethodCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete IrrigationMethodCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['IrrigationMethodCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["IrrigationMethodCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# LegacyAllocationIDs_nvarchar(250)_Yes
def LegacyAllocationIDs_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["LegacyAllocationIDs"].str.len() > 250 ].assign(ReasonRemoved='Incomplete LegacyAllocationIDs').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['LegacyAllocationIDs']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["LegacyAllocationIDs"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# OwnerClassificationCV_nvarchar(200)_Yes  ??
def OwnerClassificationCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["OwnerClassificationCV"].str.len() > 50 ].assign(ReasonRemoved='Incomplete OwnerClassificationCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['OwnerClassificationCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["OwnerClassificationCV"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PopulationServed_bigint_Yes
def PopulationServed_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PopulationServed"].str.contains(',') == True ].assign(ReasonRemoved='Incomplete PopulationServed').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['PopulationServed']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["PopulationServed"].str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PowerType_nvarchar(50)_Yes
def PowerType_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PowerType"].str.len() > 50 ].assign(ReasonRemoved='Incomplete PowerType').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['PowerType']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["PowerType"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PrimaryUseCategory_Nvarchar(100)_Yes
def PrimaryUseCategory_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PrimaryUseCategory"].str.len() > 100 ].assign(ReasonRemoved='Incomplete PrimaryUseCategory').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['PrimaryUseCategory']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["PrimaryUseCategory"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationSDWISIdentifierCV_nvarchar(100)_Yes
def AllocationSDWISIdentifierCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationSDWISIdentifierCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete AllocationSDWISIdentifierCV').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['AllocationSDWISIdentifierCV']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["AllocationSDWISIdentifierCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterAllocationNativeURL_nvarchar(250)_Yes
def WaterAllocationNativeURL_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["WaterAllocationNativeURL"].str.len() > 250 ].assign(ReasonRemoved='Incomplete WaterAllocationNativeURL').reset_index()
    if len(mask.index) > 0:
        outmaskColumn = ["ReasonRemoved", "UUID", "IncompleteField_1"]
        outmaskdf = pd.DataFrame(columns=outmaskColumn)
        outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
        outmaskdf['UUID'] = mask['UUID']
        outmaskdf['IncompleteField_1'] = mask['WaterAllocationNativeURL']
        dfy = dfy.append(outmaskdf)

        dropIndex = dfx.loc[ dfx["WaterAllocationNativeURL"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)



# AggregatedAmounts_facts
########################################################################################################################
########################################################################################################################

# MethodUUID_nvarchar(250)_-
def MethodUUID_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["MethodUUID"].isnull()) |
                    (dfx["MethodUUID"] == '') |
                    (dfx['MethodUUID'].str.len() > 250) ].assign(ReasonRemoved='Incomplete MethodUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)  # Append to purge DataFrame
        dropIndex = dfx.loc[ (dfx["MethodUUID"].isnull()) |
                             (dfx["MethodUUID"] == '') |
                             (dfx['MethodUUID'].str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# VariableSpecificUUID_nvarchar(250)_-
def VariableSpecificUUID_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["VariableSpecificUUID"].isnull()) |
                    (dfx["VariableSpecificUUID"] == '') |
                    (dfx['VariableSpecificUUID'].str.len() > 250) ].assign(ReasonRemoved='Incomplete VariableSpecificUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["VariableSpecificUUID"].isnull()) |
                             (dfx["VariableSpecificUUID"] == '') |
                             (dfx['VariableSpecificUUID'].str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterSourceUUID_nvarchar(250)_-
def WaterSourceUUID_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["WaterSourceUUID"].isnull()) |
                    (dfx["WaterSourceUUID"] == '') |
                    (dfx['WaterSourceUUID'].str.len() > 250) ].assign(ReasonRemoved='Incomplete WaterSourceUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["WaterSourceUUID"].isnull()) |
                             (dfx["WaterSourceUUID"] == '') |
                             (dfx['WaterSourceUUID'].str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# OrganizationUUID_nvarchar(250)_-
def OrganizationUUID_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["OrganizationUUID"].isnull()) |
                    (dfx["OrganizationUUID"] == '') |
                    (dfx['OrganizationUUID'].str.len() > 250) ].assign(ReasonRemoved='Incomplete OrganizationUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["OrganizationUUID"].isnull()) |
                             (dfx["OrganizationUUID"] == '') |
                             (dfx['OrganizationUUID'].str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# ReportingUnitUUID_nvarchar(200)_-
def ReportingUnitUUID_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["ReportingUnitUUID"].isnull()) |
                    (dfx["ReportingUnitUUID"] == '') |
                    (dfx['ReportingUnitUUID'].str.len() > 200) ].assign(ReasonRemoved='Incomplete ReportingUnitUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["ReportingUnitUUID"].isnull()) |
                             (dfx["ReportingUnitUUID"] == '') |
                             (dfx['ReportingUnitUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationCropDutyAmount_float_Yes
def AllocationCropDutyAmount_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx['AllocationCropDutyAmount'].astype(str).str.contains(',')) ].assign(ReasonRemoved='Incomplete AllocationCropDutyAmount').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx['AllocationCropDutyAmount'].astype(str).str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# Amount_float_-
def Amount_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["Amount"].isnull()) |
                    (dfx["Amount"] == "") |
                    (dfx['Amount'].astype(str).str.contains(',')) ].assign(ReasonRemoved='Incomplete Amount').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["Amount"].isnull()) |
                             (dfx["Amount"] == "") |
                             (dfx['Amount'].astype(str).str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)



# BeneficialUseCategory_nvarchar(250)_Yes
def BeneficialUseCategory_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["BeneficialUseCategory"].str.len() > 250) ].assign(ReasonRemoved='Incomplete BeneficialUseCategory').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["BeneficialUseCategory"].str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CommunityWaterSupplySystem_nvarchar(250)_Yes
def CommunityWaterSupplySystem_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CommunityWaterSupplySystem"].str.len() > 250 ].assign(ReasonRemoved='Incomplete CommunityWaterSupplySystem').reset_index()
    purge = dfx[mask]
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CommunityWaterSupplySystem"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CropTypeCV_nvarchar(250)_Yes
def CropTypeCV_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CropTypeCV"].str.len() > 250 ].assign(ReasonRemoved='Incomplete CropTypeCV').reset_index()
    purge = dfx[mask]
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CropTypeCV"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CustomerTypeCV_nvarchar((100)_Yes
def CustomerTypeCV_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete CustomerTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDate_bigint_Yes
def DataPublicationDate_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["DataPublicationDate"].str.contains(',') ].assign(ReasonRemoved='Incomplete DataPublicationDate').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["DataPublicationDate"].str.contains(',') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDOI_nvarchar(100)_Yes
def DataPublicationDOI_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["DataPublicationDOI"].str.len() > 100 ].assign(ReasonRemoved='Incomplete DataPublicationDOI').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["DataPublicationDOI"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# InterbasinTransferFromID_nvarchar(100)_Yes
def InterbasinTransferFromID_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["InterbasinTransferFromID"].str.len() > 100 ].assign(ReasonRemoved='Incomplete InterbasinTransferFromID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["InterbasinTransferFromID"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# InterbasinTransferToID_nvarchar(100)_Yes
def InterbasinTransferToID_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["InterbasinTransferToID"].str.len() > 100 ].assign(ReasonRemoved='Incomplete InterbasinTransferToID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["InterbasinTransferToID"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# IrrigatedAcreage_float_Yes
def IrrigatedAcreage_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx['IrrigatedAcreage'].str.contains(',') ) ].assign(ReasonRemoved='Incomplete IrrigatedAcreage').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx['IrrigatedAcreage'].str.contains(',') ) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# IrrigationMethodCV_nvarchar(100)_Yes
def IrrigationMethodCV_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["IrrigationMethodCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete IrrigationMethodCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["IrrigationMethodCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PopulationServed_bigint_Yes
def PopulationServed_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PopulationServed"].astype(str).str.contains(',') == True ].assign(ReasonRemoved='Incomplete PopulationServed').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PopulationServed"].astype(str).str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PowerGeneratedGWh_float_Yes
def PowerGeneratedGWh_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx['PowerGeneratedGWh'].str.contains(',') == True) ].assign(ReasonRemoved='Incomplete PowerGeneratedGWh').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx['PowerGeneratedGWh'].str.contains(',') == True) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PowerType_nvarchar(50)_Yes
def PowerType_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PowerType"].str.len() > 50 ].assign(ReasonRemoved='Incomplete PowerType').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PowerType"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PrimaryUseCategory_nvarchar(100)_Yes
def PrimaryUseCategory_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PrimaryUseCategory"].str.len() > 100 ].assign(ReasonRemoved='Incomplete PrimaryUseCategory').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PrimaryUseCategory"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# ReportYearCV_nchar(4)_Yes
def ReportYearCV_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["ReportYearCV"].astype(str).str.len() > 4 ].assign(ReasonRemoved='Incomplete ReportYearCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["ReportYearCV"].astype(str).str.len() > 4 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SDWISIdentifierCV_nvarchar(100)_Yes
def SDWISIdentifierCV_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["SDWISIdentifierCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete SDWISIdentifierCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["SDWISIdentifierCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# TimeframeEnd_bigint_Yes
def TimeframeEnd_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["TimeframeEnd"].str.contains(',') ].assign(ReasonRemoved='Incomplete TimeframeEnd').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["TimeframeEnd"].str.contains(',') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# TimeframeStart_bigint_Yes
def TimeframeStart_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["TimeframeStart"].str.contains(',') == True ].assign(ReasonRemoved='Incomplete TimeframeStart').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["TimeframeStart"].str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)



# SiteSpecificAmounts_fact
########################################################################################################################
########################################################################################################################

# MethodUUID_nvarchar(200)_-
def MethodUUID_SS_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["MethodUUID"].isnull()) |
                    (dfx["MethodUUID"] == '') |
                    (dfx['MethodUUID'].str.len() > 200) ].assign(ReasonRemoved='Incomplete MethodUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["MethodUUID"].isnull()) |
                             (dfx["MethodUUID"] == '') |
                             (dfx['MethodUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# VariableSpecificUUID_nvarchar(200)_-
def VariableSpecificUUID_SS_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["VariableSpecificUUID"].isnull()) |
                    (dfx["VariableSpecificUUID"] == '') |
                    (dfx['VariableSpecificUUID'].str.len() > 200) ].assign(ReasonRemoved='Incomplete VariableSpecificUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["VariableSpecificUUID"].isnull()) |
                             (dfx["VariableSpecificUUID"] == '') |
                             (dfx['VariableSpecificUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterSourceUUID_nvarchar(200)_-
def WaterSourceUUID_SS_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["WaterSourceUUID"].isnull()) |
                    (dfx["WaterSourceUUID"] == '') |
                    (dfx['WaterSourceUUID'].str.len() > 200) |
                    (dfx["WaterSourceUUID"].str.contains(',')) ].assign(ReasonRemoved='Incomplete WaterSourceUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["WaterSourceUUID"].isnull()) |
                             (dfx["WaterSourceUUID"] == '') |
                             (dfx['WaterSourceUUID'].str.len() > 200) |
                             (dfx["WaterSourceUUID"].str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# OrganizationUUID_nvarchar(200)_-
def OrganizationUUID_SS_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["OrganizationUUID"].isnull()) |
                    (dfx["OrganizationUUID"] == '') |
                    (dfx['OrganizationUUID'].str.len() > 200) ].assign(ReasonRemoved='Incomplete OrganizationUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["OrganizationUUID"].isnull()) |
                             (dfx["OrganizationUUID"] == '') |
                             (dfx['OrganizationUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SiteUUID_nvarchar(200)_-
def SiteUUID_SS_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["SiteUUID"].isnull()) |
                    (dfx["SiteUUID"] == '') |
                    (dfx['SiteUUID'].str.len() > 200) ].assign(ReasonRemoved='Incomplete SiteUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["SiteUUID"].isnull()) |
                             (dfx["SiteUUID"] == '') |
                             (dfx['SiteUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# Amount_float_-
def Amount_SS_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["Amount"].isnull()) |
                    (dfx["Amount"] == '') ].assign(ReasonRemoved='Incomplete Amount').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["Amount"].isnull()) |
                             (dfx["Amount"] == '') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationCropDutyAmount_float_Yes
def AllocationCropDutyAmount_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationCropDutyAmount"].str.contains(',')].assign(ReasonRemoved='Incomplete AllocationCropDutyAmount').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationCropDutyAmount"].str.contains(',')].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AssociatedNativeAllocationIDs_nvarchar(500)_Yes
def AssociatedNativeAllocationIDs_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AssociatedNativeAllocationIDs"].str.len() > 500 ].assign(ReasonRemoved='Incomplete AssociatedNativeAllocationIDs').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AssociatedNativeAllocationIDs"].str.len() > 500 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# BeneficialUseCategory_nvarchar(250)_Yes
def BeneficialUseCategory_SS_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["BeneficialUseCategory"].str.len() > 250) ].assign(ReasonRemoved='Incomplete BeneficialUseCategory').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["BeneficialUseCategory"].str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CommunityWaterSupplySystem_nvarchar(250)_Yes
def CommunityWaterSupplySystem_SS_Check(dfx, dfy):
    mask = dfx.loc[dfx["CommunityWaterSupplySystem"].str.len() > 250].assign(ReasonRemoved='Incomplete CommunityWaterSupplySystem').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[dfx["CommunityWaterSupplySystem"].str.len() > 250].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CropTypeCV_nvarchar(100)_Yes
def CropTypeCV_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CropTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete CropTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CropTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CustomerTypeCV_nvarchar((100)_Yes
def CustomerTypeCV_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete CustomerTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDate_date_Yes
def DataPublicationDate_SS_Check(dfx, dfy):
    mask = dfx.loc[dfx["DataPublicationDate"].str.contains(',')].assign(ReasonRemoved='Incomplete DataPublicationDate').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["DataPublicationDate"].str.contains(',')].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDOI_nvarchar(100)_Yes
def DataPublicationDOI_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["DataPublicationDOI"].str.len() > 100 ].assign(ReasonRemoved='Incomplete DataPublicationDOI').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["DataPublicationDOI"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# Geometry_geometry_Yes
# ???? How to check for geometry datatype

# IrrigatedAcreage_float_Yes
def IrrigatedAcreage_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["IrrigatedAcreage"].str.contains(',')].assign(ReasonRemoved='Incomplete IrrigatedAcreage').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["IrrigatedAcreage"].str.contains(',')].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# IrrigationMethodCV_nvarchar(100)_Yes
def IrrigationMethodCV_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["IrrigationMethodCV"].astype(str).str.len() > 100 ].assign(ReasonRemoved='Incomplete IrrigationMethodCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["IrrigationMethodCV"].astype(str).str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PopulationServed_int_Yes
def PopulationServed_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PopulationServed"].astype(str).str.contains(',') ].assign(ReasonRemoved='Incomplete PopulationServed').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PopulationServed"].astype(str).str.contains(',') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PowerGeneratedGWh_float_Yes
def PowerGeneratedGWh_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PowerGeneratedGWh"].astype(str).str.contains(',') ].assign(ReasonRemoved='Incomplete PowerGeneratedGWh').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PowerGeneratedGWh"].astype(str).str.contains(',')].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PowerType_nvarchar(50)_Yes
def PowerType_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PowerType"].str.len() > 50 ].assign(ReasonRemoved='Incomplete PowerType').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PowerType"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PrimaryUseCategory_nvarchar(250)_Yes
# This might be bugged.  Issue of must have PrimaryUseCategory for Beneficial Use to be uploaded.
def PrimaryUseCategory_SS_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["PrimaryUseCategory"].str.len() > 250) |
                    (dfx["PrimaryUseCategory"].isnull()) |
                    (dfx["PrimaryUseCategory"] == '') ].assign(ReasonRemoved='Incomplete PrimaryUseCategory').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["PrimaryUseCategory"].str.len() > 250) |
                             (dfx["PrimaryUseCategory"].isnull()) |
                             (dfx["PrimaryUseCategory"] == '') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# ReportYearCV_nchar(4)_Yes
def ReportYearCV_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["ReportYearCV"].astype(str).str.len() > 4 ].assign(ReasonRemoved='Incomplete ReportYearCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["ReportYearCV"].astype(str).str.len() > 4 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SDWISIdentifier_nvarchar(100)_Yes
def SDWISIdentifier_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["SDWISIdentifier"].str.len() > 100 ].assign(ReasonRemoved='Incomplete SDWISIdentifier').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["SDWISIdentifier"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# TimeframeEnd_BigInt_-
def TimeframeEnd_SS_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["TimeframeEnd"].isnull()) |
                    (dfx["TimeframeEnd"] == "") |
                    (dfx["TimeframeEnd"].str.contains(',')) ].assign(ReasonRemoved='Incomplete TimeframeEnd').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["TimeframeEnd"].isnull()) |
                             (dfx["TimeframeEnd"] == "") |
                             (dfx["TimeframeEnd"].str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# TimeframeStart_BigInt_-
def TimeframeStart_SS_Check(dfx, dfy):
    mask = dfx.loc[(dfx["TimeframeStart"].isnull()) |
                   (dfx["TimeframeStart"] == "") |
                   (dfx["TimeframeStart"].str.contains(','))].assign(ReasonRemoved='Incomplete TimeframeStart').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[(dfx["TimeframeStart"].isnull()) |
                            (dfx["TimeframeStart"] == "") |
                            (dfx["TimeframeStart"].str.contains(','))].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)


# RegulatoryOverlay
########################################################################################################################
########################################################################################################################

# RegulatoryOverlayUUID_nvarchar(250)_-
def RegulatoryOverlayUUID_RE_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["RegulatoryOverlayUUID"].isnull()) |
                    (dfx["RegulatoryOverlayUUID"] == "") |
                    (dfx['RegulatoryOverlayUUID'].str.len() > 250) ].assign(ReasonRemoved='Incomplete RegulatoryOverlayUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["RegulatoryOverlayUUID"].isnull()) |
                             (dfx["RegulatoryOverlayUUID"] == "") |
                             (dfx['RegulatoryOverlayUUID'].str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# OversightAgency_nvarchar(250)_-
def OversightAgency_RE_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["OversightAgency"].isnull()) |
                    (dfx["OversightAgency"] == "") |
                    (dfx['OversightAgency'].str.len() > 250) ].assign(ReasonRemoved='Incomplete OversightAgency').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["OversightAgency"].isnull()) |
                             (dfx["OversightAgency"] == "") |
                             (dfx['OversightAgency'].str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# RegulatoryDescription_nvarchar(MAX)_-
def RegulatoryDescription_RE_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["RegulatoryDescription"].isnull()) |
                    (dfx["RegulatoryDescription"] == "") ].assign(ReasonRemoved='Incomplete RegulatoryDescription').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["RegulatoryDescription"].isnull()) |
                             (dfx["RegulatoryDescription"] == "")  ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# RegulatoryName_nvarchar(50)_-
def RegulatoryName_RE_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["RegulatoryName"].isnull()) |
                    (dfx["RegulatoryName"] == "") |
                    (dfx['RegulatoryName'].str.len() > 50) ].assign(ReasonRemoved='Incomplete RegulatoryName').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["RegulatoryName"].isnull()) |
                             (dfx["RegulatoryName"] == "") |
                             (dfx['RegulatoryName'].str.len() > 50) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# RegulatoryOverlayNativeID_nvarchar(250)_Yes
def RegulatoryOverlayNativeID_RE_Check(dfx, dfy):
    mask = dfx.loc[ dfx["RegulatoryOverlayNativeID"].astype(str).str.len() > 250 ].assign(ReasonRemoved='Incomplete RegulatoryOverlayNativeID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["RegulatoryOverlayNativeID"].astype(str).str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# RegulatoryStatusCV_nvarchar(50)_-
def RegulatoryStatusCV_RE_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["RegulatoryStatusCV"].isnull()) |
                    (dfx["RegulatoryStatusCV"] == "") |
                    (dfx['RegulatoryStatusCV'].str.len() > 50) ].assign(ReasonRemoved='Incomplete RegulatoryStatusCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["RegulatoryStatusCV"].isnull()) |
                             (dfx["RegulatoryStatusCV"] == "") |
                             (dfx['RegulatoryName'].str.len() > 50) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# RegulatoryStatute_nvarchar(500)_Yes
def RegulatoryStatute_RE_Check(dfx, dfy):
    mask = dfx.loc[ dfx["RegulatoryStatute"].str.len() > 500 ].assign(ReasonRemoved='Incomplete RegulatoryStatute').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["RegulatoryStatute"].str.len() > 500 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# RegulatoryStatuteLink_nvarchar(500)_Yes
def RegulatoryStatuteLink_RE_Check(dfx, dfy):
    mask = dfx.loc[ dfx["RegulatoryStatuteLink"].str.len() > 500 ].assign(ReasonRemoved='Incomplete RegulatoryStatuteLink').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["RegulatoryStatuteLink"].str.len() > 500 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# StatutoryEffectiveDate_BigInt_-
def StatutoryEffectiveDate_RE_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["StatutoryEffectiveDate"].isnull()) |
                    (dfx["StatutoryEffectiveDate"] == "") |
                    (dfx["StatutoryEffectiveDate"].str.contains(',')) ].assign(ReasonRemoved='Incomplete StatutoryEffectiveDate').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["StatutoryEffectiveDate"].isnull()) |
                             (dfx["StatutoryEffectiveDate"] == "") |
                             (dfx["StatutoryEffectiveDate"].str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# StatutoryEndDate_BigInt_Yes
def StatutoryEndDate_RE_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["StatutoryEndDate"].str.contains(',')) ].assign(ReasonRemoved='Incomplete StatutoryEndDate').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["StatutoryEndDate"].str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# RegulatoryOverlayTypeCV_nvarchar(100)_Yes
def RegulatoryOverlayTypeCV_RE_Check(dfx, dfy):
    mask = dfx.loc[ dfx["RegulatoryOverlayTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete RegulatoryOverlayTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["RegulatoryOverlayTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterSourceTypeCV_nvarchar(100)_Yes
def WaterSourceTypeCV_RE_Check(dfx, dfy):
    mask = dfx.loc[ dfx["WaterSourceTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Incomplete WaterSourceTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["WaterSourceTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)