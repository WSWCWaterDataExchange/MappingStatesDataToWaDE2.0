# Last Update: 12/09/2020
# Dependents: AllocationsAmounts_fact.py
# Purpose: To have a single function file to error check datatypes.


# WaterSources
########################################################################################################################
########################################################################################################################

# WaterSourceUUID_nvarchar(250)_-
def WaterSourceUUID_WS_Check(dfx, dfy):
    mask = dfx.loc[(dfx["WaterSourceUUID"].isnull()) |
                   (dfx["WaterSourceUUID"] == '') |
                   (dfx['WaterSourceUUID'].str.len() > 250)].assign(ReasonRemoved='Bad WaterSourceUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
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
    mask = dfx.loc[dfx["GNISFeatureNameCV"].str.len() > 250].assign(ReasonRemoved='Bad GNISFeatureNameCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[dfx["GNISFeatureNameCV"].str.len() > 250].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterQualityIndicatorCV_nvarchar(100)_-
def WaterQualityIndicatorCV_WS_Check(dfx, dfy):
    mask = dfx.loc[(dfx["WaterQualityIndicatorCV"].isnull()) |
                   (dfx["WaterQualityIndicatorCV"] == '') |
                   (dfx['WaterQualityIndicatorCV'].str.len() > 250)].assign(ReasonRemoved='Bad WaterQualityIndicatorCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[(dfx["WaterQualityIndicatorCV"].isnull()) |
                            (dfx["WaterQualityIndicatorCV"] == '') |
                            (dfx['WaterQualityIndicatorCV'].str.len() > 250)].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterSourceName_nvarchar(250)_Yes
def WaterSourceName_WS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["WaterSourceName"].astype(str).str.len() > 250 ].assign(ReasonRemoved='Bad WaterSourceName').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["WaterSourceName"].astype(str).str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterSourceNativeID_nvarchar(250)_Yes
def WaterSourceNativeID_WS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["WaterSourceNativeID"].astype(str).str.len() > 250 ].assign(ReasonRemoved='Bad WaterSourceNativeID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["WaterSourceNativeID"].astype(str).str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterSourceTypeCV_nvarchar(100)_-
def WaterSourceTypeCV_WS_Check(dfx, dfy):
    mask = dfx.loc[(dfx["WaterSourceTypeCV"].isnull()) |
                   (dfx["WaterSourceTypeCV"] == '') |
                   (dfx['WaterSourceTypeCV'].str.len() > 100)].assign(ReasonRemoved='Bad WaterSourceTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[(dfx["WaterSourceTypeCV"].isnull()) |
                            (dfx["WaterSourceTypeCV"] == '') |
                            (dfx['WaterSourceTypeCV'].str.len() > 100)].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)


# Sites
########################################################################################################################
########################################################################################################################

# SiteUUID_nvarchar(200)_
def SiteUUID_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["SiteUUID"].isnull()) |
                    (dfx["SiteUUID"] == '') |
                    (dfx['SiteUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad SiteUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["SiteUUID"].isnull()) |
                             (dfx["SiteUUID"] == '') |
                             (dfx['SiteUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CoordinateAccuracy_nvarchar(255)_Yes
def CoordinateAccuracy_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CoordinateAccuracy"].str.len() > 255 ].assign(ReasonRemoved='Bad CoordinateAccuracy').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CoordinateAccuracy"].str.len() > 255 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CoordinateMethodCV_nvarchar(100)_-
def CoordinateMethodCV_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["CoordinateMethodCV"].isnull()) |
                    (dfx["CoordinateMethodCV"] == '') |
                    (dfx['CoordinateMethodCV'].str.len() > 100) ].assign(ReasonRemoved='Bad CoordinateMethodCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["CoordinateMethodCV"].isnull()) |
                             (dfx["CoordinateMethodCV"] == '') |
                             (dfx['CoordinateMethodCV'].str.len() > 100) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# County_nvarchar(20)_Yes
def County_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["County"].str.len() > 20 ].assign(ReasonRemoved='Bad County').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["County"].str.len() > 20 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# EPSGCodeCV_nvarchar(50)_-
def EPSGCodeCV_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["EPSGCodeCV"].isnull()) |
                    (dfx["EPSGCodeCV"] == '') |
                    (dfx['EPSGCodeCV'].str.len() > 50) ].assign(ReasonRemoved='Bad EPSGCodeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
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
    mask = dfx.loc[ dfx["GNISCodeCV"].astype(str).str.len() > 250 ].assign(ReasonRemoved='Bad GNISCodeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["GNISCodeCV"].astype(str).str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# HUC12_nvarchar(20)_Yes
def HUC12_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["HUC12"].astype(str).str.len() > 20 ].assign(ReasonRemoved='Bad HUC12').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["HUC12"].astype(str).str.len() > 20 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# HUC8_nvarchar(20)_Yes
def HUC8_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["HUC8"].astype(str).str.len() > 20 ].assign(ReasonRemoved='Bad HUC8').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["HUC8"].astype(str).str.len() > 20 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# Latitude_float_-
def Latitude_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["Latitude"].isnull()) |
                    (dfx["Latitude"] == '') |
                    (dfx["Latitude"] < 20) ].assign(ReasonRemoved='Bad Latitude').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["Latitude"].isnull()) |
                             (dfx["Latitude"] == '') |
                             (dfx["Latitude"] < 20) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# Longitude_float_-
def Longitude_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["Longitude"].isnull()) |
                    (dfx["Longitude"] == '') |
                    (dfx["Longitude"] > -80) ].assign(ReasonRemoved='Bad Longitude').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["Longitude"].isnull()) |
                             (dfx["Longitude"] == '') |
                             (dfx["Longitude"] > -80) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# NHDNetworkStatusCV_nvarchar(50)_Yes
def NHDNetworkStatusCV_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["NHDNetworkStatusCV"].str.len() > 50 ].assign(ReasonRemoved='Bad NHDNetworkStatusCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["NHDNetworkStatusCV"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# NHDProductCV_nvarchar(50)_Yes
def NHDProductCV_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["NHDProductCV"].str.len() > 50 ].assign(ReasonRemoved='Bad NHDProductCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["NHDProductCV"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PODorPOUSite_nvarchar(50)_Yes
def PODorPOUSite_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PODorPOUSite"].str.len() > 50 ].assign(ReasonRemoved='Bad PODorPOUSite').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PODorPOUSite"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# RegulatoryOverlayUUIDs_nvarchar(200)_
def RegulatoryOverlayUUIDs_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx['RegulatoryOverlayUUIDs'].str.len() > 200) ].assign(ReasonRemoved='Bad ReportingUnitUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx['RegulatoryOverlayUUIDs'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SiteName_nvarchar(500)_
def SiteName_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["SiteName"].isnull()) |
                    (dfx["SiteName"] == '') |
                    (dfx['SiteName'].str.len() > 500) ].assign(ReasonRemoved='Bad SiteName').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)  # Append to purge DataFrame
        dropIndex = dfx.loc[ (dfx["SiteName"].isnull()) |
                             (dfx["SiteName"] == '') |
                             (dfx['SiteName'].str.len() > 500) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SiteNativeID_nvarchar(50)_Yes
def SiteNativeID_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["SiteNativeID"].astype(str).str.len() > 50 ].assign(ReasonRemoved='Bad SiteNativeID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["SiteNativeID"].astype(str).str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SitePoint_geometry_Yes
# ???? How to check for geometry datatype

# SiteTypeCV_nvarchar(100)_Yes
def SiteTypeCV_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["SiteTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Bad SiteTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["SiteTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# StateCV_nvarchar(2)_Yes
def StateCV_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["StateCV"].str.len() > 2 ].assign(ReasonRemoved='Bad StateCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["StateCV"].str.len() > 2 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# USGSSiteID_nvarchar(250)_Yes
def USGSSiteID_S_Check(dfx, dfy):
    mask = dfx.loc[ dfx["USGSSiteID"].str.len() > 250 ].assign(ReasonRemoved='Bad USGSSiteID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["USGSSiteID"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterSourceUUID_nvarchar(200)_-
def WaterSourceUUID_S_Check(dfx, dfy):
    mask = dfx.loc[ (dfx['WaterSourceUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad WaterSourceUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx['WaterSourceUUID'].str.len() > 200) ].index
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
                    (dfx['ReportingUnitUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad ReportingUnitUUID').reset_index()
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
                    (dfx['EPSGCodeCV'].str.len() > 50) ].assign(ReasonRemoved='Bad EPSGCodeCV').reset_index()
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
                    (dfx['ReportingUnitName'].astype(str).str.len() > 250) ].assign(ReasonRemoved='Bad ReportingUnitName').reset_index()
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
                    (dfx['ReportingUnitNativeID'].astype(str).str.len() > 250) ].assign(ReasonRemoved='Bad ReportingUnitNativeID').reset_index()
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
    mask = dfx.loc[ dfx["ReportingUnitProductVersion"].str.len() > 100 ].assign(ReasonRemoved='Bad ReportingUnitProductVersion').reset_index()
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
                    (dfx['ReportingUnitTypeCV'].str.len() > 50) ].assign(ReasonRemoved='Bad ReportingUnitTypeCV').reset_index()
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
    mask = dfx.loc[ (dfx["ReportingUnitUpdateDate"].str.contains(',')) ].assign(ReasonRemoved='Bad ReportingUnitUpdateDate').reset_index()
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
                    (dfx['StateCV'].str.len() > 2) ].assign(ReasonRemoved='Bad StateCV').reset_index()
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
                    (dfx['MethodUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad MethodUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
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
                    (dfx['VariableSpecificUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad VariableSpecificUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
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
                    (dfx['OrganizationUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad OrganizationUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["OrganizationUUID"].isnull()) |
                             (dfx["OrganizationUUID"] == '') |
                             (dfx['OrganizationUUID'].str.len() > 200) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SiteUUID_nvarchar(max)_-
def SiteUUID_AA_Check(dfx, dfy):
    mask = dfx.loc[(dfx["SiteUUID"].isnull()) |
                   (dfx["SiteUUID"] == '') ].assign(ReasonRemoved='Bad SiteUUID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[(dfx["SiteUUID"].isnull()) |
                            (dfx["SiteUUID"] == '') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationApplicationDate_date_Yes
def AllocationApplicationDate_AA_Check(dfx, dfy):
    mask = dfx.loc[dfx["AllocationApplicationDate"].str.contains(',') == True].assign(ReasonRemoved='Bad AllocationApplicationDate').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationApplicationDate"].str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationAssociatedConsumptiveUseSiteIDs_nvarchar(500)_Yes
def AllocationAssociatedConsumptiveUseSiteIDs_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationAssociatedConsumptiveUseSiteIDs"].str.len() > 500 ].assign(ReasonRemoved='Bad AllocationAssociatedConsumptiveUseSiteIDs').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationAssociatedConsumptiveUseSiteIDs"].str.len() > 500 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationAssociatedWithdrawalSiteIDs_nvarchar(500)_Yes
def AllocationAssociatedWithdrawalSiteIDs_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationAssociatedWithdrawalSiteIDs"].str.len() > 500 ].assign(ReasonRemoved='Bad AllocationAssociatedWithdrawalSiteIDs').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationAssociatedWithdrawalSiteIDs"].str.len() > 500 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationBasisCV_nvarchar(250)_Yes
def AllocationBasisCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationBasisCV"].str.len() > 250 ].assign(ReasonRemoved='Bad AllocationBasisCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationBasisCV"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationChangeApplicationIndicator_nvarchar(100)_Yes
def AllocationChangeApplicationIndicator_AA_Check(dfx, dfy):
    mask= dfx.loc[ dfx["AllocationChangeApplicationIndicator"].str.len() > 100 ].assign(ReasonRemoved='Bad AllocationChangeApplicationIndicator').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationChangeApplicationIndicator"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationCommunityWaterSupplySystem_nvarchar(250)_Yes
def AllocationCommunityWaterSupplySystem_AA_Check(dfx, dfy):
    mask= dfx.loc[ dfx["AllocationCommunityWaterSupplySystem"].str.len() > 250 ].assign(ReasonRemoved='Bad AllocationCommunityWaterSupplySystem').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationCommunityWaterSupplySystem"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationCropDutyAmount_float_Yes
def AllocationCropDutyAmount_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationCropDutyAmount"].str.contains(',') == True ].assign(ReasonRemoved='Bad AllocationCropDutyAmount').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationCropDutyAmount"].str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationExpirationDate_string_Yes
def AllocationExpirationDate_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationExpirationDate"].str.contains(',') == True ].assign(ReasonRemoved='Bad AllocationExpirationDate').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationExpirationDate"].str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)




# AllocationFlow_CFS_float_Yes & AllocationVolume_AF_float_Yes
# We have to have either a flow or a volume
def AllocationFlowVolume_CFSAF_float_Yes_AA_Check(dfx, dfy):

    # check if CFS or AF is a csv list. If true, sum values.
    for index, row in dfx.iterrows():
        flowNumbers = row['AllocationFlow_CFS'].split(",")
        volumeNumbers = row['AllocationVolume_AF'].split(",")

        # Flow
        flowTotal = 0
        for x in flowNumbers:
            if x == "" or "," in x:
                flowTotal = x
            else:
                try:
                    x = float(x)
                    flowTotal += x
                except:
                    flowTotal = x

        # Volume
        volumeTotal = 0
        for x in volumeNumbers:
            if x == "" or "," in x:
                flowTotal = x
            else:
                try:
                    x = float(x)
                    volumeTotal += x
                except:
                    volumeTotal = x

        row['AllocationFlow_CFS'] = flowTotal
        row['AllocationVolume_AF'] = volumeTotal

    # Search for non-numeric items to remove
    mask = dfx.loc[ (dfx['ExemptOfVolumeFlowPriority'] == "0") &
                    (((dfx["AllocationFlow_CFS"].isnull()) |
                      (dfx["AllocationFlow_CFS"] == "") |
                      (dfx['AllocationFlow_CFS'].astype(str).str.contains(','))) &
                     ((dfx["AllocationVolume_AF"].isnull()) |
                      (dfx["AllocationVolume_AF"] == "") |
                      (dfx['AllocationVolume_AF'].astype(str).str.contains(',')))) ].assign(ReasonRemoved='Bad Flow or Volume').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
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





# # AllocationFlow_CFS_float_Yes & AllocationVolume_AF_float_Yes
# # We have to have either a flow or a volume
# def AllocationFlowVolume_CFSAF_float_Yes_AA_Check(dfx, dfy):
#     mask = dfx.loc[ (dfx['ExemptOfVolumeFlowPriority'] == "0") &
#                     (((dfx["AllocationFlow_CFS"].isnull()) |
#                       (dfx["AllocationFlow_CFS"] == "") |
#                       (dfx['AllocationFlow_CFS'].astype(str).str.contains(','))) &
#                      ((dfx["AllocationVolume_AF"].isnull()) |
#                       (dfx["AllocationVolume_AF"] == "") |
#                       (dfx['AllocationVolume_AF'].astype(str).str.contains(',')))) ].assign(ReasonRemoved='Bad Flow or Volume').reset_index()
#     if len(mask.index) > 0:
#         dfy = dfy.append(mask)
#         dropIndex = dfx.loc[ (dfx['ExemptOfVolumeFlowPriority'] == "0") &
#                              (((dfx["AllocationFlow_CFS"].isnull()) |
#                                (dfx["AllocationFlow_CFS"] == "") |
#                                (dfx['AllocationFlow_CFS'].astype(str).str.contains(','))) &
#                               ((dfx["AllocationVolume_AF"].isnull()) |
#                                (dfx["AllocationVolume_AF"] == "") |
#                                (dfx['AllocationVolume_AF'].astype(str).str.contains(',')))) ].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)

# AllocationLegalStatusCV_nvarchar(250)_Yes
def AllocationLegalStatusCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["AllocationLegalStatusCV"].str.len() > 250) |
                    (dfx['AllocationLegalStatusCV'].str.contains(',')) ].assign(ReasonRemoved='Bad AllocationLegalStatusCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["AllocationLegalStatusCV"].str.len() > 250) |
                             (dfx['AllocationLegalStatusCV'].str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationNativeID_nvarchar(250)_Yes
def AllocationNativeID_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationNativeID"].str.len() > 250 ].assign(ReasonRemoved='Bad AllocationNativeID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationNativeID"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationOwner_nvarchar(500)_Yes
def AllocationOwner_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationOwner"].str.len() > 500 ].assign(ReasonRemoved='Bad AllocationOwner').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
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
                     (dfx["AllocationPriorityDate"].str.contains(','))) ].assign(ReasonRemoved='Bad AllocationPriorityDate').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
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
    mask = dfx.loc[ dfx["AllocationTimeframeEnd"].str.len() > 5 ].assign(ReasonRemoved='Bad AllocationTimeframeEnd').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationTimeframeEnd"].str.len() > 5 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationTimeframeStart_nvarchar(5)_Yes
def AllocationTimeframeStart_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationTimeframeStart"].str.len() > 5 ].assign(ReasonRemoved='Bad AllocationTimeframeStart').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationTimeframeStart"].str.len() > 5 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationTypeCV_nvarchar(250)_Yes
def AllocationTypeCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["AllocationTypeCV"].str.len() > 250) |
                    (dfx["AllocationTypeCV"].str.contains(',')) ].assign(ReasonRemoved='Bad AllocationTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["AllocationTypeCV"].str.len() > 250) |
                             (dfx["AllocationTypeCV"].str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# BeneficialUseCategory_nvarchar(100)_-
def BeneficialUseCategory_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["BeneficialUseCategory"].isnull()) |
                    (dfx["BeneficialUseCategory"] == '') |
                    (dfx["BeneficialUseCategory"].str.len() > 100) ].assign(ReasonRemoved='Bad BeneficialUseCategory').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["BeneficialUseCategory"].isnull()) |
                             (dfx["BeneficialUseCategory"] == '') |
                             (dfx["BeneficialUseCategory"].str.len() > 100) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# # CommunityWaterSupplySystem_nvarchar(250)_Yes
def CommunityWaterSupplySystem_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CommunityWaterSupplySystem"].str.len() > 250 ].assign(ReasonRemoved='Bad CommunityWaterSupplySystem').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CommunityWaterSupplySystem"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CropTypeCV_nvarchar(100)_Yes
def CropTypeCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CommunityWaterSupplySystem"].str.len() > 250 ].assign(ReasonRemoved='Bad CommunityWaterSupplySystem').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CommunityWaterSupplySystem"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CustomerTypeCV_nvarchar(100)_Yes
def CustomerTypeCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Bad CustomerTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDate_string_-
def DataPublicationDate_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["DataPublicationDate"].isnull()) | (dfx["DataPublicationDate"] == '') | (dfx["DataPublicationDate"].str.contains(',') == True) ].assign(ReasonRemoved='Bad DataPublicationDate').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["DataPublicationDate"].isnull()) | (dfx["DataPublicationDate"] == '') | (dfx["DataPublicationDate"].str.contains(',') == True)  ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDOI_nvarchar(100)_Yes
def DataPublicationDOI_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["DataPublicationDOI"].str.len() > 100 ].assign(ReasonRemoved='Bad DataPublicationDOI').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["DataPublicationDOI"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# ExemptOfVolumeFlowPriority_bit_Yes
def ExemptOfVolumeFlowPriority_AA_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["ExemptOfVolumeFlowPriority"] > 1) ].assign(ReasonRemoved='Bad ExemptOfVolumeFlowPriority').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["ExemptOfVolumeFlowPriority"] > 1) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# GeneratedPowerCapacityMW_float_Yes
def GeneratedPowerCapacityMW_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["GeneratedPowerCapacityMW"].str.contains(',') == True ].assign(ReasonRemoved='Bad GeneratedPowerCapacityMW').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["GeneratedPowerCapacityMW"].str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# IrrigatedAcreage_float_Yes
def IrrigatedAcreage_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["IrrigatedAcreage"].str.contains(',') == True ].assign(ReasonRemoved='Bad IrrigatedAcreage').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["IrrigatedAcreage"].str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# IrrigationMethodCV_nvarchar(100)_Yes
def IrrigationMethodCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["IrrigationMethodCV"].str.len() > 100 ].assign(ReasonRemoved='Bad IrrigationMethodCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["IrrigationMethodCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# LegacyAllocationIDs_nvarchar(250)_Yes
def LegacyAllocationIDs_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["LegacyAllocationIDs"].str.len() > 250 ].assign(ReasonRemoved='Bad LegacyAllocationIDs').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["LegacyAllocationIDs"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# OwnerClassificationCV_nvarchar(200)_Yes  ??
def OwnerClassificationCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["OwnerClassificationCV"].str.len() > 50 ].assign(ReasonRemoved='Bad PowerType').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["OwnerClassificationCV"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PopulationServed_bigint_Yes
def PopulationServed_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PopulationServed"].str.contains(',') == True ].assign(ReasonRemoved='Bad PopulationServed').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PopulationServed"].str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PowerType_nvarchar(50)_Yes
def PowerType_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PowerType"].str.len() > 50 ].assign(ReasonRemoved='Bad PowerType').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PowerType"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PrimaryUseCategory_Nvarchar(100)_Yes
def PrimaryUseCategory_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PrimaryUseCategory"].str.len() > 100 ].assign(ReasonRemoved='Bad PrimaryUseCategory').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PrimaryUseCategory"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationSDWISIdentifierCV_nvarchar(100)_Yes
def AllocationSDWISIdentifierCV_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationSDWISIdentifierCV"].str.len() > 100 ].assign(ReasonRemoved='Bad AllocationSDWISIdentifierCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationSDWISIdentifierCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# WaterAllocationNativeURL_nvarchar(250)_Yes
def WaterAllocationNativeURL_AA_Check(dfx, dfy):
    mask = dfx.loc[ dfx["WaterAllocationNativeURL"].str.len() > 250 ].assign(ReasonRemoved='Bad WaterAllocationNativeURL').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
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
                    (dfx['MethodUUID'].str.len() > 250) ].assign(ReasonRemoved='Bad MethodUUID').reset_index()
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
                    (dfx['VariableSpecificUUID'].str.len() > 250) ].assign(ReasonRemoved='Bad VariableSpecificUUID').reset_index()
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
                    (dfx['WaterSourceUUID'].str.len() > 250) ].assign(ReasonRemoved='Bad WaterSourceUUID').reset_index()
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
                    (dfx['OrganizationUUID'].str.len() > 250) ].assign(ReasonRemoved='Bad OrganizationUUID').reset_index()
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
                    (dfx['ReportingUnitUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad ReportingUnitUUID').reset_index()
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
    mask = dfx.loc[ (dfx['AllocationCropDutyAmount'].astype(str).str.contains(',')) ].assign(ReasonRemoved='Bad AllocationCropDutyAmount').reset_index()
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
                    (dfx['Amount'].astype(str).str.contains(',')) ].assign(ReasonRemoved='Bad Amount').reset_index()
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
    mask = dfx.loc[ (dfx["BeneficialUseCategory"].str.len() > 250) ].assign(ReasonRemoved='Bad BeneficialUseCategory').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["BeneficialUseCategory"].str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CommunityWaterSupplySystem_nvarchar(250)_Yes
def CommunityWaterSupplySystem_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CommunityWaterSupplySystem"].str.len() > 250 ].assign(ReasonRemoved='Bad CommunityWaterSupplySystem').reset_index()
    purge = dfx[mask]
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CommunityWaterSupplySystem"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CropTypeCV_nvarchar(250)_Yes
def CropTypeCV_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CropTypeCV"].str.len() > 250 ].assign(ReasonRemoved='Bad CropTypeCV').reset_index()
    purge = dfx[mask]
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CropTypeCV"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CustomerTypeCV_nvarchar((100)_Yes
def CustomerTypeCV_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Bad CustomerTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDate_bigint_Yes
def DataPublicationDate_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["DataPublicationDate"].str.contains(',') ].assign(ReasonRemoved='Bad DataPublicationDate').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["DataPublicationDate"].str.contains(',') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDOI_nvarchar(100)_Yes
def DataPublicationDOI_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["DataPublicationDOI"].str.len() > 100 ].assign(ReasonRemoved='Bad DataPublicationDOI').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["DataPublicationDOI"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# InterbasinTransferFromID_nvarchar(100)_Yes
def InterbasinTransferFromID_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["InterbasinTransferFromID"].str.len() > 100 ].assign(ReasonRemoved='Bad InterbasinTransferFromID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["InterbasinTransferFromID"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# InterbasinTransferToID_nvarchar(100)_Yes
def InterbasinTransferToID_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["InterbasinTransferToID"].str.len() > 100 ].assign(ReasonRemoved='Bad InterbasinTransferToID').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["InterbasinTransferToID"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# IrrigatedAcreage_float_Yes
def IrrigatedAcreage_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx['IrrigatedAcreage'].str.contains(',') ) ].assign(ReasonRemoved='Bad IrrigatedAcreage').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx['IrrigatedAcreage'].str.contains(',') ) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# IrrigationMethodCV_nvarchar(100)_Yes
def IrrigationMethodCV_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["IrrigationMethodCV"].str.len() > 100 ].assign(ReasonRemoved='Bad IrrigationMethodCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["IrrigationMethodCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PopulationServed_bigint_Yes
def PopulationServed_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PopulationServed"].astype(str).str.contains(',') == True ].assign(ReasonRemoved='Bad PopulationServed').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PopulationServed"].astype(str).str.contains(',') == True ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PowerGeneratedGWh_float_Yes
def PowerGeneratedGWh_AG_Check(dfx, dfy):
    mask = dfx.loc[ (dfx['PowerGeneratedGWh'].str.contains(',') == True) ].assign(ReasonRemoved='Bad PowerGeneratedGWh').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx['PowerGeneratedGWh'].str.contains(',') == True) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PowerType_nvarchar(50)_Yes
def PowerType_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PowerType"].str.len() > 50 ].assign(ReasonRemoved='Bad PowerType').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PowerType"].str.len() > 50 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PrimaryUseCategory_nvarchar(100)_Yes
def PrimaryUseCategory_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PrimaryUseCategory"].str.len() > 100 ].assign(ReasonRemoved='Bad PrimaryUseCategory').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PrimaryUseCategory"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# ReportYearCV_nchar(4)_Yes
def ReportYearCV_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["ReportYearCV"].astype(str).str.len() > 4 ].assign(ReasonRemoved='Bad ReportYearCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["ReportYearCV"].astype(str).str.len() > 4 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SDWISIdentifierCV_nvarchar(100)_Yes
def SDWISIdentifierCV_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["SDWISIdentifierCV"].str.len() > 100 ].assign(ReasonRemoved='Bad SDWISIdentifierCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["SDWISIdentifierCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# TimeframeEnd_bigint_Yes
def TimeframeEnd_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["TimeframeEnd"].str.contains(',') ].assign(ReasonRemoved='Bad TimeframeEnd').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["TimeframeEnd"].str.contains(',') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# TimeframeStart_bigint_Yes
def TimeframeStart_AG_Check(dfx, dfy):
    mask = dfx.loc[ dfx["TimeframeStart"].str.contains(',') == True ].assign(ReasonRemoved='Bad TimeframeStart').reset_index()
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
                    (dfx['MethodUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad MethodUUID').reset_index()
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
                    (dfx['VariableSpecificUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad VariableSpecificUUID').reset_index()
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
                    (dfx["WaterSourceUUID"].str.contains(',')) ].assign(ReasonRemoved='Bad WaterSourceUUID').reset_index()
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
                    (dfx['OrganizationUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad OrganizationUUID').reset_index()
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
                    (dfx['SiteUUID'].str.len() > 200) ].assign(ReasonRemoved='Bad SiteUUID').reset_index()
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
                    (dfx["Amount"] == '') ].assign(ReasonRemoved='Bad Amount').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["Amount"].isnull()) |
                             (dfx["Amount"] == '') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AllocationCropDutyAmount_float_Yes
def AllocationCropDutyAmount_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AllocationCropDutyAmount"].str.contains(',')].assign(ReasonRemoved='Bad AllocationCropDutyAmount').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AllocationCropDutyAmount"].str.contains(',')].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# AssociatedNativeAllocationIDs_nvarchar(500)_Yes
def AssociatedNativeAllocationIDs_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["AssociatedNativeAllocationIDs"].str.len() > 500 ].assign(ReasonRemoved='Bad AssociatedNativeAllocationIDs').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["AssociatedNativeAllocationIDs"].str.len() > 500 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# BeneficialUseCategory_nvarchar(250)_Yes
def BeneficialUseCategory_SS_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["BeneficialUseCategory"].str.len() > 250) ].assign(ReasonRemoved='Bad BeneficialUseCategory').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["BeneficialUseCategory"].str.len() > 250) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CommunityWaterSupplySystem_nvarchar(250)_Yes
def CommunityWaterSupplySystem_SS_Check(dfx, dfy):
    mask = dfx.loc[dfx["CommunityWaterSupplySystem"].str.len() > 250].assign(ReasonRemoved='Bad CommunityWaterSupplySystem').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[dfx["CommunityWaterSupplySystem"].str.len() > 250].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CropTypeCV_nvarchar(100)_Yes
def CropTypeCV_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CropTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Bad CropTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CropTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# CustomerTypeCV_nvarchar((100)_Yes
def CustomerTypeCV_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].assign(ReasonRemoved='Bad CustomerTypeCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["CustomerTypeCV"].str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDate_date_Yes
def DataPublicationDate_SS_Check(dfx, dfy):
    mask = dfx.loc[dfx["DataPublicationDate"].str.contains(',')].assign(ReasonRemoved='Bad DataPublicationDate').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["DataPublicationDate"].str.contains(',')].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# DataPublicationDOI_nvarchar(100)_Yes
def DataPublicationDOI_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["DataPublicationDOI"].str.len() > 100 ].assign(ReasonRemoved='Bad DataPublicationDOI').reset_index()
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
    mask = dfx.loc[ dfx["IrrigatedAcreage"].str.contains(',')].assign(ReasonRemoved='Bad IrrigatedAcreage').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["IrrigatedAcreage"].str.contains(',')].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# IrrigationMethodCV_nvarchar(100)_Yes
def IrrigationMethodCV_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["IrrigationMethodCV"].astype(str).str.len() > 100 ].assign(ReasonRemoved='Bad IrrigationMethodCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["IrrigationMethodCV"].astype(str).str.len() > 100 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PopulationServed_float_Yes
def PopulationServed_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PopulationServed"].astype(str).str.contains(',') ].assign(ReasonRemoved='Bad PopulationServed').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PopulationServed"].astype(str).str.contains(',') ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PowerGeneratedGWh_float_Yes
def PowerGeneratedGWh_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PowerGeneratedGWh"].astype(str).str.contains(',') ].assign(ReasonRemoved='Bad PowerGeneratedGWh').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["PowerGeneratedGWh"].astype(str).str.contains(',')].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# PowerType_nvarchar(50)_Yes
def PowerType_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["PowerType"].str.len() > 50 ].assign(ReasonRemoved='Bad PowerType').reset_index()
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
                    (dfx["PrimaryUseCategory"] == '') ].assign(ReasonRemoved='Bad PrimaryUseCategory').reset_index()
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
    mask = dfx.loc[ dfx["ReportYearCV"].astype(str).str.len() > 4 ].assign(ReasonRemoved='Bad ReportYearCV').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["ReportYearCV"].astype(str).str.len() > 4 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# SDWISIdentifier_nvarchar(100)_Yes
def SDWISIdentifier_SS_Check(dfx, dfy):
    mask = dfx.loc[ dfx["SDWISIdentifier"].str.len() > 250 ].assign(ReasonRemoved='Bad SDWISIdentifier').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ dfx["SDWISIdentifier"].str.len() > 250 ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# TimeframeEnd_BigInt_-
def TimeframeEnd_SS_Check(dfx, dfy):
    mask = dfx.loc[ (dfx["TimeframeEnd"].isnull()) |
                    (dfx["TimeframeEnd"] == '') |
                    (dfx["TimeframeEnd"].str.contains(',')) ].assign(ReasonRemoved='Bad TimeframeEnd').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[ (dfx["TimeframeEnd"].isnull()) |
                             (dfx["TimeframeEnd"] == '') |
                             (dfx["TimeframeEnd"].str.contains(',')) ].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)

# TimeframeStart_BigInt_-
def TimeframeStart_SS_Check(dfx, dfy):
    mask = dfx.loc[(dfx["TimeframeStart"].isnull()) |
                   (dfx["TimeframeStart"] == '') |
                   (dfx["TimeframeStart"].str.contains(','))].assign(ReasonRemoved='Bad TimeframeStart').reset_index()
    if len(mask.index) > 0:
        dfy = dfy.append(mask)
        dropIndex = dfx.loc[(dfx["TimeframeStart"].isnull()) |
                            (dfx["TimeframeStart"] == '') |
                            (dfx["TimeframeStart"].str.contains(','))].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)