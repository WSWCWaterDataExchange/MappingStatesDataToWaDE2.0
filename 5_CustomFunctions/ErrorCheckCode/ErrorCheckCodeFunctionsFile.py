# Last Update: 09/27/2023
# Purpose: To have a single function file to error check datatypes.
# Index:
#       WaterSources
#       Sites
#       ReportingUnits
#       AllocationsAmounts_facts
#       AggregatedAmounts_facts
#       SiteSpecificAmounts_fact
#       RegulatoryOverlay


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Global Functions
############################################################################
def removeMaskItemsFunc(dfx, dfy, mask, selectionVar):
    if len(mask.index) > 0:
        dfy = pd.concat([dfy, mask]).reset_index(drop=True)
        dropIndex = dfx.loc[selectionVar].index
        dfx = dfx.drop(dropIndex)
        dfx = dfx.reset_index(drop=True)
    return (dfx, dfy)


def WaterSourceTestErrorFunctions(outdf, dfpurge):
    # Geometry??? How to check for geometry datatype
    outdf, dfpurge = GNISFeatureNameCV_WS_Check(outdf, dfpurge)
    outdf, dfpurge = WaterQualityIndicatorCV_WS_Check(outdf, dfpurge)
    outdf, dfpurge = WaterSourceName_WS_Check(outdf, dfpurge)
    outdf, dfpurge = WaterSourceNativeID_WS_Check(outdf, dfpurge)
    outdf, dfpurge = WaterSourceTypeCV_WS_Check(outdf, dfpurge)
    return(outdf, dfpurge)


def SiteTestErrorFunctions(outdf, dfpurge):
    outdf, dfpurge = RegulatoryOverlayUUIDs_S_Check(outdf, dfpurge)
    outdf, dfpurge = WaterSourceUUIDs_S_Check(outdf, dfpurge)
    outdf, dfpurge = CoordinateAccuracy_S_Check(outdf, dfpurge)
    outdf, dfpurge = CoordinateMethodCV_S_Check(outdf, dfpurge)
    outdf, dfpurge = County_S_Check(outdf, dfpurge)
    outdf, dfpurge = EPSGCodeCV_S_Check(outdf, dfpurge)
    # Geometry ???? How to check for geometry datatype
    outdf, dfpurge = GNISCodeCV_S_Check(outdf, dfpurge)
    outdf, dfpurge = HUC12_S_Check(outdf, dfpurge)
    outdf, dfpurge = HUC8_S_Check(outdf, dfpurge)
    outdf, dfpurge = Latitude_S_Check(outdf, dfpurge)
    outdf, dfpurge = Longitude_S_Check(outdf, dfpurge)
    outdf, dfpurge = NHDNetworkStatusCV_S_Check(outdf, dfpurge)
    outdf, dfpurge = NHDProductCV_S_Check(outdf, dfpurge)
    outdf, dfpurge = PODorPOUSite_S_Check(outdf, dfpurge)
    outdf, dfpurge = SiteName_S_Check(outdf, dfpurge)
    outdf, dfpurge = SiteNativeID_S_Check(outdf, dfpurge)
    # SitePoint ???? How to check for geometry datatype
    outdf, dfpurge = SiteTypeCV_S_Check(outdf, dfpurge)
    outdf, dfpurge = StateCV_S_Check(outdf, dfpurge)
    outdf, dfpurge = USGSSiteID_S_Check(outdf, dfpurge)
    return(outdf, dfpurge)


def ReportingUnitTestErrorFunctions(outdf, dfpurge):
    outdf, dfpurge = EPSGCodeCV_RU_Check(outdf, dfpurge)
    # Geometry ???? How to check for geometry datatype
    outdf, dfpurge = ReportingUnitName_RU_Check(outdf, dfpurge)
    outdf, dfpurge = ReportingUnitNativeID_RU_Check(outdf, dfpurge)
    outdf, dfpurge = ReportingUnitProductVersion_RU_Check(outdf, dfpurge)
    outdf, dfpurge = ReportingUnitTypeCV_RU_Check(outdf, dfpurge)
    outdf, dfpurge = ReportingUnitUpdateDate_RU_Check(outdf, dfpurge)
    outdf, dfpurge = StateCV_RU_Check(outdf, dfpurge)
    return(outdf, dfpurge)


def AllocationAmountTestErrorFunctions(outdf, dfpurge):
    outdf, dfpurge = MethodUUID_AA_Check(outdf, dfpurge)
    outdf, dfpurge = OrganizationUUID_AA_Check(outdf, dfpurge)
    outdf, dfpurge = SiteUUID_AA_Check(outdf, dfpurge)
    outdf, dfpurge = VariableSpecificUUID_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationApplicationDate_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationAssociatedConsumptiveUseSiteIDs_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationAssociatedWithdrawalSiteIDs_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationBasisCV_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationChangeApplicationIndicator_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationCommunityWaterSupplySystem_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationCropDutyAmount_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationExpirationDate_AA_Check(outdf, dfpurge)
    # outdf, dfpurge = AllocationFlowVolume_CFSAF_float_Yes_AA_Check(outdf, dfpurge) # tring to check Flow and Vol separately.
    outdf, dfpurge = AllocationFlow_CFS_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationVolume_AF_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationLegalStatusCV_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationNativeID_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationOwner_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationPriorityDate_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationSDWISIdentifierCV_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationTimeframeEnd_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationTimeframeStart_AA_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationTypeCV_AA_Check(outdf, dfpurge)
    # outdf, dfpurge = BeneficialUseCategory_AA_Check(outdf, dfpurge)
    outdf, dfpurge = CommunityWaterSupplySystem_AA_Check(outdf, dfpurge)
    outdf, dfpurge = CropTypeCV_AA_Check(outdf, dfpurge)
    outdf, dfpurge = CustomerTypeCV_AA_Check(outdf, dfpurge)
    outdf, dfpurge = DataPublicationDate_AA_Check(outdf, dfpurge)
    outdf, dfpurge = DataPublicationDOI_AA_Check(outdf, dfpurge)
    # ExemptOfVolumeFlowPriority ??? outdf, dfpurge = ExemptOfVolumeFlowPriority_AA_Check(outdf, dfpurge)
    outdf, dfpurge = GeneratedPowerCapacityMW_AA_Check(outdf, dfpurge)
    outdf, dfpurge = IrrigatedAcreage_AA_Check(outdf, dfpurge)
    outdf, dfpurge = IrrigationMethodCV_AA_Check(outdf, dfpurge)
    outdf, dfpurge = LegacyAllocationIDs_AA_Check(outdf, dfpurge)
    outdf, dfpurge = OwnerClassificationCV_AA_Check(outdf, dfpurge)
    outdf, dfpurge = PopulationServed_AA_Check(outdf, dfpurge)
    outdf, dfpurge = PowerType_AA_Check(outdf, dfpurge)
    outdf, dfpurge = PrimaryBeneficialUseCategory_AA_Check(outdf, dfpurge)
    outdf, dfpurge = WaterAllocationNativeURL_AA_Check(outdf, dfpurge)
    return(outdf, dfpurge)


def SiteSpecificAmountsTestErrorFunctions(outdf, dfpurge):
    outdf, dfpurge = MethodUUID_SS_Check(outdf, dfpurge)
    outdf, dfpurge = VariableSpecificUUID_SS_Check(outdf, dfpurge)
    outdf, dfpurge = WaterSourceUUID_SS_Check(outdf, dfpurge)
    outdf, dfpurge = OrganizationUUID_SS_Check(outdf, dfpurge)
    outdf, dfpurge = SiteUUID_SS_Check(outdf, dfpurge)
    outdf, dfpurge = Amount_SS_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationCropDutyAmount_SS_Check(outdf, dfpurge)
    outdf, dfpurge = AssociatedNativeAllocationIDs_SS_Check(outdf, dfpurge)
    outdf, dfpurge = BeneficialUseCategory_SS_Check(outdf, dfpurge)
    outdf, dfpurge = CommunityWaterSupplySystem_SS_Check(outdf, dfpurge)
    outdf, dfpurge = CropTypeCV_SS_Check(outdf, dfpurge)
    outdf, dfpurge = CustomerTypeCV_SS_Check(outdf, dfpurge)
    outdf, dfpurge = DataPublicationDate_SS_Check(outdf, dfpurge)
    outdf, dfpurge = DataPublicationDOI_SS_Check(outdf, dfpurge)
    # Geometry ???? How to check for geometry datatype
    outdf, dfpurge = IrrigatedAcreage_SS_Check(outdf, dfpurge)
    outdf, dfpurge = IrrigationMethodCV_SS_Check(outdf, dfpurge)
    outdf, dfpurge = PopulationServed_SS_Check(outdf, dfpurge)
    outdf, dfpurge = PowerGeneratedGWh_SS_Check(outdf, dfpurge)
    outdf, dfpurge = PowerType_SS_Check(outdf, dfpurge)
    outdf, dfpurge = PrimaryUseCategory_SS_Check(outdf, dfpurge)
    outdf, dfpurge = ReportYearCV_SS_Check(outdf, dfpurge)
    outdf, dfpurge = SDWISIdentifier_SS_Check(outdf, dfpurge)
    # outdf, dfpurge = TimeframeEnd_SS_Check(outdf, dfpurge)
    # outdf, dfpurge = TimeframeStart_SS_Check(outdf, dfpurge)
    return(outdf, dfpurge)


def RegulatoryOverlaysTestErrorFunctions(outdf, dfpurge):
    outdf, dfpurge = OversightAgency_RE_Check(outdf, dfpurge)
    outdf, dfpurge = RegulatoryDescription_RE_Check(outdf, dfpurge)
    outdf, dfpurge = RegulatoryName_RE_Check(outdf, dfpurge)
    outdf, dfpurge = RegulatoryOverlayNativeID_RE_Check(outdf, dfpurge)
    outdf, dfpurge = RegulatoryStatusCV_RE_Check(outdf, dfpurge)
    outdf, dfpurge = RegulatoryStatute_RE_Check(outdf, dfpurge)
    outdf, dfpurge = RegulatoryStatuteLink_RE_Check(outdf, dfpurge)
    outdf, dfpurge = StatutoryEffectiveDate_RE_Check(outdf, dfpurge)
    outdf, dfpurge = StatutoryEndDate_RE_Check(outdf, dfpurge)
    outdf, dfpurge = RegulatoryOverlayTypeCV_RE_Check(outdf, dfpurge)
    outdf, dfpurge = WaterSourceTypeCV_RE_Check(outdf, dfpurge)
    return(outdf, dfpurge)


def RegulatoryReportingUnitsErrorFunctions(outdf, dfpurge):
    # DataPublicationDate
    outdf, dfpurge = OrganizationUUID_SS_Check(outdf, dfpurge)
    outdf, dfpurge = ReportingUnitUUID_RU_Check(outdf, dfpurge)
    outdf, dfpurge = RegulatoryOverlayUUID_RE_Check(outdf, dfpurge)
    return(outdf, dfpurge)


def AggregatedAmountsErrorFunctions(outdf, dfpurge):
    outdf, dfpurge = MethodUUID_AG_Check(outdf, dfpurge)
    outdf, dfpurge = OrganizationUUID_AG_Check(outdf, dfpurge)
    outdf, dfpurge = ReportingUnitUUID_AG_Check(outdf, dfpurge)
    outdf, dfpurge = VariableSpecificUUID_AG_Check(outdf, dfpurge)
    outdf, dfpurge = WaterSourceUUID_AG_Check(outdf, dfpurge)
    outdf, dfpurge = AllocationCropDutyAmount_AG_Check(outdf, dfpurge)
    outdf, dfpurge = Amount_AG_Check(outdf, dfpurge)
    outdf, dfpurge = BeneficialUseCategory_AG_Check(outdf, dfpurge)
    outdf, dfpurge = CommunityWaterSupplySystem_AG_Check(outdf, dfpurge)
    outdf, dfpurge = CropTypeCV_AG_Check(outdf, dfpurge)
    outdf, dfpurge = CustomerTypeCV_AG_Check(outdf, dfpurge)
    outdf, dfpurge = DataPublicationDate_AG_Check(outdf, dfpurge)
    outdf, dfpurge = DataPublicationDOI_AG_Check(outdf, dfpurge)
    outdf, dfpurge = InterbasinTransferFromID_AG_Check(outdf, dfpurge)
    outdf, dfpurge = InterbasinTransferToID_AG_Check(outdf, dfpurge)
    outdf, dfpurge = IrrigatedAcreage_AG_Check(outdf, dfpurge)
    outdf, dfpurge = IrrigationMethodCV_AG_Check(outdf, dfpurge)
    outdf, dfpurge = PopulationServed_AG_Check(outdf, dfpurge)
    outdf, dfpurge = PowerGeneratedGWh_AG_Check(outdf, dfpurge)
    outdf, dfpurge = PowerType_AG_Check(outdf, dfpurge)
    outdf, dfpurge = PrimaryUseCategoryCV_AG_Check(outdf, dfpurge)
    outdf, dfpurge = ReportYearCV_AG_Check(outdf, dfpurge)
    outdf, dfpurge = SDWISIdentifierCV_AG_Check(outdf, dfpurge)
    outdf, dfpurge = TimeframeEnd_AG_Check(outdf, dfpurge)
    outdf, dfpurge = TimeframeStart_AG_Check(outdf, dfpurge)
    return (outdf, dfpurge)


# WaterSources
########################################################################################################################
########################################################################################################################

# WaterSourceUUID_nvarchar(250)_-
def WaterSourceUUID_WS_Check(dfx, dfy):
    selectionVar = (dfx["WaterSourceUUID"].isnull()) | (dfx["WaterSourceUUID"] == '') | (dfx['WaterSourceUUID'].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for WaterSourceUUID').reset_index()
    mask['IncompleteField'] = mask['WaterSourceUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# Geometry_geometry_Yes
# ???? How to check for geometry datatype

# GNISFeatureNameCV_nvarchar(250)_Yes
def GNISFeatureNameCV_WS_Check(dfx, dfy):
    selectionVar = (dfx["GNISFeatureNameCV"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for GNISFeatureNameCV').reset_index()
    mask['IncompleteField'] = mask['GNISFeatureNameCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# WaterQualityIndicatorCV_nvarchar(100)_-
def WaterQualityIndicatorCV_WS_Check(dfx, dfy):
    selectionVar = (dfx["WaterQualityIndicatorCV"].isnull()) | (dfx["WaterQualityIndicatorCV"] == '') | (dfx['WaterQualityIndicatorCV'].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for WaterQualityIndicatorCV').reset_index()
    mask['IncompleteField'] = mask['WaterQualityIndicatorCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# WaterSourceName_nvarchar(250)_Yes
def WaterSourceName_WS_Check(dfx, dfy):
    selectionVar = (dfx["WaterSourceName"].astype(str).str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for WaterSourceName').reset_index()
    mask['IncompleteField'] = mask['WaterSourceName']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# WaterSourceNativeID_nvarchar(250)_Yes
def WaterSourceNativeID_WS_Check(dfx, dfy):
    selectionVar = (dfx["WaterSourceNativeID"].astype(str).str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for WaterSourceNativeID').reset_index()
    mask['IncompleteField'] = mask['WaterSourceNativeID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# WaterSourceTypeCV_nvarchar(100)_-
def WaterSourceTypeCV_WS_Check(dfx, dfy):
    selectionVar = (dfx['WaterSourceTypeCV'].str.len() > 100) | (dfx["WaterSourceTypeCV"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for WaterSourceTypeCV').reset_index()
    mask['IncompleteField'] = mask['WaterSourceTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# Sites
########################################################################################################################
########################################################################################################################

# SiteUUID_nvarchar(200)_
def SiteUUID_S_Check(dfx, dfy):
    selectionVar = (dfx["SiteUUID"].isnull()) | (dfx["SiteUUID"] == '') | (dfx['SiteUUID'].str.len() > 200)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for SiteUUID').reset_index()
    mask['IncompleteField'] = mask['SiteUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# WaterSourceUUIDs_nvarchar(200)_-
def WaterSourceUUIDs_S_Check(dfx, dfy):
    selectionVar = (dfx["WaterSourceUUIDs"].isnull()) | (dfx["WaterSourceUUIDs"] == '') | (dfx['WaterSourceUUIDs'].str.len() > 200)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for WaterSourceUUIDs').reset_index()
    mask['IncompleteField'] = mask['WaterSourceUUIDs']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# CoordinateAccuracy_nvarchar(255)_Yes
def CoordinateAccuracy_S_Check(dfx, dfy):
    selectionVar = (dfx["CoordinateAccuracy"].astype(str).str.len() > 255)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for CoordinateAccuracy').reset_index()
    mask['IncompleteField'] = mask['CoordinateAccuracy']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# CoordinateMethodCV_nvarchar(100)_-
def CoordinateMethodCV_S_Check(dfx, dfy):
    selectionVar = (dfx['CoordinateMethodCV'].astype(str).str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for CoordinateMethodCV').reset_index()
    mask['IncompleteField'] = mask['CoordinateMethodCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# County_nvarchar(20)_Yes
def County_S_Check(dfx, dfy):
    selectionVar= ((dfx["County"].astype(str).str.len() > 20) | (dfx["County"].astype(str).str.contains(',') == True))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for County').reset_index()
    mask['IncompleteField'] = mask['County']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# EPSGCodeCV_nvarchar(50)_-
def EPSGCodeCV_S_Check(dfx, dfy):
    selectionVar= (dfx["EPSGCodeCV"].isnull()) | (dfx["EPSGCodeCV"] == '') | (dfx['EPSGCodeCV'].str.len() > 50)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for EPSGCodeCV').reset_index()
    mask['IncompleteField'] = mask['EPSGCodeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# Geometry_geometry_Yes
# ???? How to check for geometry datatype
# this doesn't work, need some kind of boolean check in the mask
# from shapely.wkt import loads
#
# def validGeoFunc(geo):
#     try:
#         return loads(geo)
#     except:
#         return geo
#
# def Geometry_S_Check(dfx, dfy):
#     mask = dfx.loc[dfx["Geometry"].apply(validGeoFunc)].assign(ReasonRemoved='Incomplete or bad entry for Geometry').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "WaDEUUID", "RowIndex", "IncompleteField", "IncompleteField_2"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['WaDEUUID'] = mask['WaDEUUID']
#         outmaskdf['RowIndex'] = mask['index']
#         outmaskdf['IncompleteField'] = mask['Geometry']
#         dfy = dfy.append(outmaskdf)
#
#         dropIndex = dfx.loc[dfx["Geometry"].apply(validGeoFunc)].index
#         dfx = dfx.drop(dropIndex)
#         dfx = dfx.reset_index(drop=True)
#     return (dfx, dfy)


# GNISCodeCV_nvarchar(250)_Yes
def GNISCodeCV_S_Check(dfx, dfy):
    selectionVar = (dfx["GNISCodeCV"].astype(str).str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for GNISCodeCV').reset_index()
    mask['IncompleteField'] = mask['GNISCodeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# HUC12_nvarchar(20)_Yes
def HUC12_S_Check(dfx, dfy):
    selectionVar = (dfx["HUC12"].astype(str).str.len() > 20)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for HUC12').reset_index()
    mask['IncompleteField'] = mask['HUC12']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# HUC8_nvarchar(20)_Yes
def HUC8_S_Check(dfx, dfy):
    selectionVar = (dfx["HUC8"].astype(str).str.len() > 20)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for HUC8').reset_index()
    mask['IncompleteField'] = mask['HUC8']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# Latitude_float_-
def Latitude_S_Check(dfx, dfy):
    # check for string values with a ','
    selectionVar = (dfx["Latitude"].isnull()) | (dfx["Latitude"].astype(str) == "") | (dfx["Latitude"].astype(str).str.contains(","))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Latitude').reset_index()
    mask['IncompleteField'] = mask['Latitude']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)

    # check for bad float values
    selectionVar = (dfx["Latitude"].replace("",0).fillna(0).astype(float) == 0.0) | (dfx["Latitude"].replace("",0).fillna(0).astype(float) < -91) | (dfx["Latitude"].replace("",0).fillna(0).astype(float) > 91)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Latitude').reset_index()
    mask['IncompleteField'] = mask['Latitude']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)

    # return results
    return (dfx, dfy)


# Longitude_float_-
def Longitude_S_Check(dfx, dfy):
    # check for string values with a ','
    selectionVar = (dfx["Longitude"].isnull()) | (dfx["Longitude"].astype(str) == "") | (dfx["Longitude"].astype(str).str.contains(","))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Longitude').reset_index()
    mask['IncompleteField'] = mask['Longitude']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)

    # check for bad float values
    selectionVar = (dfx["Longitude"].replace("",0).fillna(0).astype(float) == 0.0 ) | (dfx["Longitude"].replace("",0).fillna(0).astype(float) < -181) | (dfx["Longitude"].replace("",0).fillna(0).astype(float) > 181)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Longitude').reset_index()
    mask['IncompleteField'] = mask['Longitude']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)

    # return results
    return (dfx, dfy)


# NHDNetworkStatusCV_nvarchar(50)_Yes
def NHDNetworkStatusCV_S_Check(dfx, dfy):
    selectionVar = dfx["NHDNetworkStatusCV"].str.len() > 50
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for NHDNetworkStatusCV').reset_index()
    mask['IncompleteField'] = mask['NHDNetworkStatusCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# NHDProductCV_nvarchar(50)_Yes
def NHDProductCV_S_Check(dfx, dfy):
    selectionVar = dfx["NHDProductCV"].str.len() > 50
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for NHDProductCV').reset_index()
    mask['IncompleteField'] = mask['NHDProductCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PODorPOUSite_nvarchar(50)_Yes
def PODorPOUSite_S_Check(dfx, dfy):
    selectionVar = (dfx["PODorPOUSite"].str.len() > 50) | (dfx["PODorPOUSite"].astype(str).str.contains(","))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PODorPOUSite').reset_index()
    mask['IncompleteField'] = mask['PODorPOUSite']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# RegulatoryOverlayUUIDs_nvarchar(200)_
def RegulatoryOverlayUUIDs_S_Check(dfx, dfy):
    selectionVar = (dfx['RegulatoryOverlayUUIDs'].str.len() > 200)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for ReportingUnitUUID').reset_index()
    mask['IncompleteField'] = mask['RegulatoryOverlayUUIDs']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# SiteName_nvarchar(500)_
def SiteName_S_Check(dfx, dfy):
    selectionVar = (dfx['SiteName'].str.len() > 500) | (dfx["SiteName"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for SiteName').reset_index()
    mask['IncompleteField'] = mask['SiteName']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# SiteNativeID_nvarchar(50)_Yes
def SiteNativeID_S_Check(dfx, dfy):
    selectionVar = (dfx["SiteNativeID"].astype(str).str.len() > 50)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for SiteNativeID').reset_index()
    mask['IncompleteField'] = mask['SiteNativeID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# SitePoint_geometry_Yes
# ???? How to check for geometry datatype

# SiteTypeCV_nvarchar(100)_Yes
def SiteTypeCV_S_Check(dfx, dfy):
    selectionVar = (dfx["SiteTypeCV"].str.len() > 100) | (dfx["SiteTypeCV"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for SiteTypeCV').reset_index()
    mask['IncompleteField'] = mask['SiteTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# StateCV_nvarchar(2)_Yes
def StateCV_S_Check(dfx, dfy):
    selectionVar = (dfx["StateCV"].str.len() > 2)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for StateCV').reset_index()
    mask['IncompleteField'] = mask['StateCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# USGSSiteID_nvarchar(250)_Yes
def USGSSiteID_S_Check(dfx, dfy):
    selectionVar = (dfx["USGSSiteID"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for USGSSiteID').reset_index()
    mask['IncompleteField'] = mask['USGSSiteID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# ReportingUnits
########################################################################################################################
########################################################################################################################

# ReportingUnitUUID_nvarchar(200)_
def ReportingUnitUUID_RU_Check(dfx, dfy):
    selectionVar = (dfx["ReportingUnitUUID"].isnull()) | (dfx["ReportingUnitUUID"] == '') | (dfx['ReportingUnitUUID'].str.len() > 200)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for ReportingUnitUUID').reset_index()
    mask['IncompleteField'] = mask['ReportingUnitUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# EPSGCodeCV_nvarchar(50)_Yes
def EPSGCodeCV_RU_Check(dfx, dfy):
    selectionVar = (dfx["EPSGCodeCV"].isnull()) | (dfx["EPSGCodeCV"] == '') |  (dfx['EPSGCodeCV'].str.len() > 50)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for EPSGCodeCV').reset_index()
    mask['IncompleteField'] = mask['EPSGCodeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# Geometry_Geometry_Yes
# Not sure how to check for this...

# ReportingUnitName_nvarchar(250)_
def ReportingUnitName_RU_Check(dfx, dfy):
    selectionVar = (dfx["ReportingUnitName"].isnull()) | (dfx["ReportingUnitName"] == '') | (dfx['ReportingUnitName'].astype(str).str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for ReportingUnitName').reset_index()
    mask['IncompleteField'] = mask['ReportingUnitName']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# ReportingUnitNativeID_nvarchar(250)_
def ReportingUnitNativeID_RU_Check(dfx, dfy):
    selectionVar = (dfx["ReportingUnitNativeID"].isnull()) | (dfx["ReportingUnitNativeID"] == '') | (dfx['ReportingUnitNativeID'].astype(str).str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for ReportingUnitNativeID').reset_index()
    mask['IncompleteField'] = mask['ReportingUnitNativeID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# ReportingUnitProductVersion_nvarchar(100)_Yes
def ReportingUnitProductVersion_RU_Check(dfx, dfy):
    selectionVar = (dfx["ReportingUnitProductVersion"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for ReportingUnitProductVersion').reset_index()
    mask['IncompleteField'] = mask['ReportingUnitProductVersion']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# ReportingUnitTypeCV_nvarchar(20)_
def ReportingUnitTypeCV_RU_Check(dfx, dfy):
    selectionVar = (dfx['ReportingUnitTypeCV'].str.len() > 50) | (dfx["ReportingUnitTypeCV"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for ReportingUnitTypeCV').reset_index()
    mask['IncompleteField'] = mask['ReportingUnitTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# ReportingUnitUpdateDate_Date_Yes
def ReportingUnitUpdateDate_RU_Check(dfx, dfy):
    selectionVar = (dfx["ReportingUnitUpdateDate"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for ReportingUnitUpdateDate').reset_index()
    mask['IncompleteField'] = mask['ReportingUnitUpdateDate']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# StateCV_nvarchar(2)_
def StateCV_RU_Check(dfx, dfy):
    selectionVar = (dfx["StateCV"].isnull()) | (dfx["StateCV"] == '') | (dfx['StateCV'].str.len() > 2)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for StateCV').reset_index()
    mask['IncompleteField'] = mask['StateCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationsAmounts_facts
########################################################################################################################
########################################################################################################################

# AllocationUUID_nvarchar(250)_-
def AllocationUUID_AA_Check(dfx, dfy):
    selectionVar = ((dfx["AllocationUUID"].isnull()) | (dfx["AllocationUUID"] == '') | (dfx['AllocationUUID'].str.len() > 250))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationUUID').reset_index()
    mask['IncompleteField'] = mask['AllocationUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# MethodUUID_nvarchar(200)_-
def MethodUUID_AA_Check(dfx, dfy):
    selectionVar = ((dfx["MethodUUID"].isnull()) | (dfx["MethodUUID"] == '') | (dfx['MethodUUID'].str.len() > 200) | (dfx["MethodUUID"].str.contains(',') == True))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for MethodUUID').reset_index()
    mask['IncompleteField'] = mask['MethodUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# VariableSpecificUUID_nvarchar(200)_-
def VariableSpecificUUID_AA_Check(dfx, dfy):
    selectionVar = ((dfx["VariableSpecificUUID"].isnull()) | (dfx["VariableSpecificUUID"] == '') | (dfx['VariableSpecificUUID'].str.len() > 200) | (dfx["VariableSpecificUUID"].str.contains(',') == True))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for VariableSpecificUUID').reset_index()
    mask['IncompleteField'] = mask['VariableSpecificUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# OrganizationUUID_nvarchar(200)_-
def OrganizationUUID_AA_Check(dfx, dfy):
    selectionVar = ((dfx["OrganizationUUID"].isnull()) | (dfx["OrganizationUUID"] == '') | (dfx['OrganizationUUID'].str.len() > 200) | (dfx["OrganizationUUID"].str.contains(',') == True))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for OrganizationUUID').reset_index()
    mask['IncompleteField'] = mask['OrganizationUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# SiteUUID_nvarchar(max)_-
def SiteUUID_AA_Check(dfx, dfy):
    selectionVar = (dfx["SiteUUID"].isnull()) | (dfx["SiteUUID"] == '')
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for SiteUUID').reset_index()
    mask['IncompleteField'] = mask['SiteUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationApplicationDate_date_Yes
def AllocationApplicationDate_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationApplicationDate"].str.contains(',') == True)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationApplicationDate').reset_index()
    mask['IncompleteField'] = mask['AllocationApplicationDate']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationAssociatedConsumptiveUseSiteIDs_nvarchar(500)_Yes
def AllocationAssociatedConsumptiveUseSiteIDs_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationAssociatedConsumptiveUseSiteIDs"].str.len() > 500)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationAssociatedConsumptiveUseSiteIDs').reset_index()
    mask['IncompleteField'] = mask['AllocationAssociatedConsumptiveUseSiteIDs']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationAssociatedWithdrawalSiteIDs_nvarchar(500)_Yes
def AllocationAssociatedWithdrawalSiteIDs_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationAssociatedWithdrawalSiteIDs"].str.len() > 500)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationAssociatedWithdrawalSiteIDs').reset_index()
    mask['IncompleteField'] = mask['AllocationAssociatedWithdrawalSiteIDs']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationBasisCV_nvarchar(250)_Yes
def AllocationBasisCV_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationBasisCV"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationBasisCV').reset_index()
    mask['IncompleteField'] = mask['AllocationBasisCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationChangeApplicationIndicator_nvarchar(100)_Yes
def AllocationChangeApplicationIndicator_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationChangeApplicationIndicator"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationChangeApplicationIndicator').reset_index()
    mask['IncompleteField'] = mask['AllocationChangeApplicationIndicator']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationCommunityWaterSupplySystem_nvarchar(250)_Yes
def AllocationCommunityWaterSupplySystem_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationCommunityWaterSupplySystem"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationCommunityWaterSupplySystem').reset_index()
    mask['IncompleteField'] = mask['AllocationCommunityWaterSupplySystem']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationCropDutyAmount_float_Yes
def AllocationCropDutyAmount_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationCropDutyAmount"].str.contains(',') == True)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationCropDutyAmount').reset_index()
    mask['IncompleteField'] = mask['AllocationCropDutyAmount']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationExpirationDate_string_Yes
def AllocationExpirationDate_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationExpirationDate"].str.contains(',') == True)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationExpirationDate').reset_index()
    mask['IncompleteField'] = mask['AllocationExpirationDate']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# # AllocationFlow_CFS_float_Yes & AllocationVolume_AF_float_Yes
# # We have to have either a flow or a volume
# # We are summing multiple entries into one
# def AllocationFlowVolume_CFSAF_float_Yes_AA_Check(dfx, dfy):
#
#     # check if CFS or AF is a csv list. If true, sum values.
#     for index, row in dfx.iterrows():
#         flowNumbers = row['AllocationFlow_CFS'].split(",")
#         volumeNumbers = row['AllocationVolume_AF'].split(",")
#
#         # Flow
#         for x in flowNumbers:
#             if x == '' or x is None:
#                 x = x
#             else:
#                 x = float(x)
#                 x += x
#
#         # Volume
#         for y in volumeNumbers:
#             if y == '' or y is None:
#                 y = y
#             else:
#                 y = float(y)
#                 y += y
#
#         row['AllocationFlow_CFS'] = x
#         row['AllocationVolume_AF'] = y
#
#     # Search for non-numeric items to remove
#     mask = dfx.loc[ (dfx['ExemptOfVolumeFlowPriority'] == "0") &
#                     (((dfx["AllocationFlow_CFS"].isnull()) |
#                       (dfx["AllocationFlow_CFS"] == "") |
#                       (dfx['AllocationFlow_CFS'].astype(str).str.contains(','))) &
#                      ((dfx["AllocationVolume_AF"].isnull()) |
#                       (dfx["AllocationVolume_AF"] == "") |
#                       (dfx['AllocationVolume_AF'].astype(str).str.contains(',')))) ].assign(ReasonRemoved='Incomplete or bad entry for Flow or Volume').reset_index()
#     if len(mask.index) > 0:
#         outmaskColumn = ["ReasonRemoved", "RowIndex", "IncompleteField", "IncompleteField_2"]
#         outmaskdf = pd.DataFrame(columns=outmaskColumn)
#         outmaskdf['ReasonRemoved'] = mask['ReasonRemoved']
#         outmaskdf['RowIndex'] = mask['index']
#         outmaskdf['IncompleteField'] = mask['AllocationFlow_CFS']
#         outmaskdf['IncompleteField_2'] = mask['AllocationVolume_AF']
#         dfy = dfy.append(outmaskdf)
#
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


# # AllocationFlow_CFS_float_Yes & AllocationVolume_AF_float_Yes
# # We have to have either a flow or a volume
# def AllocationFlowVolume_CFSAF_float_Yes_AA_Check(dfx, dfy):
#     selectionVar = ((dfx['ExemptOfVolumeFlowPriority'] == "0") & (((dfx["AllocationFlow_CFS"].isnull()) |
#                                                                    (dfx["AllocationFlow_CFS"] == "") |
#                                                                    (dfx['AllocationFlow_CFS'].astype(str).str.contains(',')) |
#                                                                    (dfx["AllocationFlow_CFS"].replace("", 0).fillna(0).astype(float) < 0.0)) &
#                                                                   ((dfx["AllocationVolume_AF"].isnull()) |
#                                                                    (dfx["AllocationVolume_AF"] == "") |
#                                                                    (dfx['AllocationVolume_AF'].astype(str).str.contains(',')) |
#                                                                    (dfx["AllocationVolume_AF"].replace("", 0).fillna(0).astype(float) < 0.0))))
#     mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Flow or Volume').reset_index()
#     mask['IncompleteField'] = str(mask['AllocationExpirationDate']) + ", " + str(mask['AllocationVolume_AF'])
#     dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
#     return (dfx, dfy)


# # AllocationFlow_CFS_float_Yes
# def AllocationFlow_CFS_AA_Check(dfx, dfy):
#     selectionVar = (dfx['ExemptOfVolumeFlowPriority'] == "0") & (dfx['AllocationFlow_CFS'].astype(str).str.contains(','))
#     mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Flow').reset_index()
#     mask['IncompleteField'] = mask['AllocationFlow_CFS']
#     dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
#     return (dfx, dfy)
#
#
# # AllocationVolume_AF_float_Yes
# def AllocationVolume_AF_AA_Check(dfx, dfy):
#     selectionVar = (dfx['ExemptOfVolumeFlowPriority'] == "0") & ((dfx['AllocationVolume_AF'].astype(str).str.contains(',')) | (dfx['AllocationVolume_AF'].replace("",0).fillna(0).astype(float) < 0.0))
#     mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Volume').reset_index()
#     mask['IncompleteField'] = mask['AllocationVolume_AF']
#     dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
#     return (dfx, dfy)


# AllocationFlow_CFS_float_Yes
def AllocationFlow_CFS_AA_Check(dfx, dfy):
    # check for string values with a ','
    selectionVar = (dfx['ExemptOfVolumeFlowPriority'] == "0") & (dfx['AllocationFlow_CFS'].astype(str).str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Flow').reset_index()
    mask['IncompleteField'] = mask['AllocationFlow_CFS']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)

    # check for bad float values
    selectionVar = (dfx['ExemptOfVolumeFlowPriority'] == "0") & (dfx['AllocationFlow_CFS'].replace("", 0).fillna(0).astype(float) < 0.0)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Flow').reset_index()
    mask['IncompleteField'] = mask['AllocationFlow_CFS']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)

    # return results
    return (dfx, dfy)


# AllocationVolume_AF_float_Yes
def AllocationVolume_AF_AA_Check(dfx, dfy):
    # check for string values with a ','
    selectionVar = (dfx['ExemptOfVolumeFlowPriority'] == "0") & (dfx['AllocationVolume_AF'].astype(str).str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Volume').reset_index()
    mask['IncompleteField'] = mask['AllocationVolume_AF']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)

    # check for bad float values
    selectionVar = (dfx['ExemptOfVolumeFlowPriority'] == "0") & (dfx['AllocationVolume_AF'].replace("", 0).fillna(0).astype(float) < 0.0)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Volume').reset_index()
    mask['IncompleteField'] = mask['AllocationVolume_AF']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)

    # return results
    return (dfx, dfy)


# AllocationLegalStatusCV_nvarchar(250)_Yes
def AllocationLegalStatusCV_AA_Check(dfx, dfy):
    selectionVar = ((dfx["AllocationLegalStatusCV"].str.len() > 250) | (dfx['AllocationLegalStatusCV'].str.contains(',')))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationLegalStatusCV').reset_index()
    mask['IncompleteField'] = mask['AllocationLegalStatusCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationNativeID_nvarchar(250)_Yes
def AllocationNativeID_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationNativeID"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationNativeID').reset_index()
    mask['IncompleteField'] = mask['AllocationNativeID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationOwner_nvarchar(500)_Yes
def AllocationOwner_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationOwner"].str.len() > 500)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationOwner').reset_index()
    mask['IncompleteField'] = mask['AllocationOwner']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationPriorityDate_string_-
def AllocationPriorityDate_AA_Check(dfx, dfy):
    selectionVar = ((dfx['ExemptOfVolumeFlowPriority'] == "0") & ((dfx["AllocationPriorityDate"].isnull()) |
                                                                  (dfx["AllocationPriorityDate"] == "") |
                                                                  (dfx["AllocationPriorityDate"] == " ") |
                                                                  (dfx["AllocationPriorityDate"].astype(str).str.contains(','))))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationPriorityDate').reset_index()
    mask['IncompleteField'] = mask['AllocationPriorityDate']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationTimeframeEnd_Yes
def AllocationTimeframeEnd_AA_Check(dfx, dfy):
    selectionVar = ((dfx["AllocationTimeframeEnd"].astype(str).str.len() > 6))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationTimeframeEnd').reset_index()
    mask['IncompleteField'] = mask['AllocationTimeframeEnd']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationTimeframeStart_Yes
def AllocationTimeframeStart_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationTimeframeStart"].astype(str).str.len() > 6)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationTimeframeStart').reset_index()
    mask['IncompleteField'] = mask['AllocationTimeframeStart']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationTypeCV_nvarchar(250)_Yes
def AllocationTypeCV_AA_Check(dfx, dfy):
    selectionVar = ((dfx["AllocationTypeCV"].str.len() > 250) | (dfx["AllocationTypeCV"].str.contains(',')))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationTypeCV').reset_index()
    mask['IncompleteField'] = mask['AllocationTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# # BeneficialUseCategory_nvarchar(100)_-
# # We are ignoring nvarchar length in the check at this time
# # we are solving these issues with clean code files
# def BeneficialUseCategory_AA_Check(dfx, dfy):
#     selectionVar = (dfx["BeneficialUseCategory"].isnull()) | (dfx["BeneficialUseCategory"] == ''))
#     mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for BeneficialUseCategory').reset_index()
#     mask['IncompleteField'] = mask['BeneficialUseCategory']
#     dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
#     return (dfx, dfy)


# # CommunityWaterSupplySystem_nvarchar(250)_Yes
def CommunityWaterSupplySystem_AA_Check(dfx, dfy):
    selectionVar =  (dfx["CommunityWaterSupplySystem"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for CommunityWaterSupplySystem').reset_index()
    mask['IncompleteField'] = mask['CommunityWaterSupplySystem']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# CropTypeCV_nvarchar(100)_Yes
def CropTypeCV_AA_Check(dfx, dfy):
    selectionVar = (dfx["CropTypeCV"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for CropTypeCV').reset_index()
    mask['IncompleteField'] = mask['CropTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# CustomerTypeCV_nvarchar(100)_Yes
def CustomerTypeCV_AA_Check(dfx, dfy):
    selectionVar = (dfx["CustomerTypeCV"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for CustomerTypeCV').reset_index()
    mask['IncompleteField'] = mask['CustomerTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# DataPublicationDate_string_-
def DataPublicationDate_AA_Check(dfx, dfy):
    selectionVar = ((dfx["DataPublicationDate"].isnull()) | (dfx["DataPublicationDate"] == '') | (dfx["DataPublicationDate"].str.contains(',') == True))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for DataPublicationDate').reset_index()
    mask['IncompleteField'] = mask['DataPublicationDate']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# DataPublicationDOI_nvarchar(100)_Yes
def DataPublicationDOI_AA_Check(dfx, dfy):
    selectionVar = (dfx["DataPublicationDOI"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for DataPublicationDOI').reset_index()
    mask['IncompleteField'] = mask['DataPublicationDOI']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# ExemptOfVolumeFlowPriority_bit_Yes
def ExemptOfVolumeFlowPriority_AA_Check(dfx, dfy):
    selectionVar = (dfx["ExemptOfVolumeFlowPriority"] > 1)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for ExemptOfVolumeFlowPriority').reset_index()
    mask['IncompleteField'] = mask['ExemptOfVolumeFlowPriority']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# GeneratedPowerCapacityMW_float_Yes
def GeneratedPowerCapacityMW_AA_Check(dfx, dfy):
    selectionVar = (dfx["GeneratedPowerCapacityMW"].astype(str).str.contains(',') == True)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for GeneratedPowerCapacityMW').reset_index()
    mask['IncompleteField'] = mask['GeneratedPowerCapacityMW']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# IrrigatedAcreage_float_Yes
def IrrigatedAcreage_AA_Check(dfx, dfy):
    selectionVar = (dfx['IrrigatedAcreage'].astype(str).str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for IrrigatedAcreage').reset_index()
    mask['IncompleteField'] = mask['IrrigatedAcreage']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# IrrigationMethodCV_nvarchar(100)_Yes
def IrrigationMethodCV_AA_Check(dfx, dfy):
    selectionVar = (dfx["IrrigationMethodCV"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for IrrigationMethodCV').reset_index()
    mask['IncompleteField'] = mask['IrrigationMethodCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# LegacyAllocationIDs_nvarchar(250)_Yes
def LegacyAllocationIDs_AA_Check(dfx, dfy):
    selectionVar = (dfx["LegacyAllocationIDs"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for LegacyAllocationIDs').reset_index()
    mask['IncompleteField'] = mask['LegacyAllocationIDs']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# OwnerClassificationCV_nvarchar(200)_Yes  ??
def OwnerClassificationCV_AA_Check(dfx, dfy):
    selectionVar = (dfx["OwnerClassificationCV"].str.len() > 50)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for OwnerClassificationCV').reset_index()
    mask['IncompleteField'] = mask['OwnerClassificationCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PopulationServed_bigint_Yes
def PopulationServed_AA_Check(dfx, dfy):
    selectionVar = (dfx["PopulationServed"].astype(str).str.contains(',') == True)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PopulationServed').reset_index()
    mask['IncompleteField'] = mask['PopulationServed']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PowerType_nvarchar(50)_Yes
def PowerType_AA_Check(dfx, dfy):
    selectionVar = (dfx["PowerType"].str.len() > 50)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PowerType').reset_index()
    mask['IncompleteField'] = mask['PowerType']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PrimaryBeneficialUseCategory_Nvarchar(150)_Yes
def PrimaryBeneficialUseCategory_AA_Check(dfx, dfy):
    selectionVar = (dfx["PrimaryBeneficialUseCategory"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PrimaryBeneficialUseCategory').reset_index()
    mask['IncompleteField'] = mask['PrimaryBeneficialUseCategory']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationSDWISIdentifierCV_nvarchar(100)_Yes
def AllocationSDWISIdentifierCV_AA_Check(dfx, dfy):
    selectionVar = (dfx["AllocationSDWISIdentifierCV"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationSDWISIdentifierCV').reset_index()
    mask['IncompleteField'] = mask['AllocationSDWISIdentifierCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# WaterAllocationNativeURL_nvarchar(250)_Yes
def WaterAllocationNativeURL_AA_Check(dfx, dfy):
    selectionVar = (dfx["WaterAllocationNativeURL"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for WaterAllocationNativeURL').reset_index()
    mask['IncompleteField'] = mask['WaterAllocationNativeURL']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)



# AggregatedAmounts_facts
########################################################################################################################
########################################################################################################################

# MethodUUID_nvarchar(250)_-
def MethodUUID_AG_Check(dfx, dfy):
    selectionVar = (dfx["MethodUUID"].isnull()) | (dfx["MethodUUID"] == '') | (dfx['MethodUUID'].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for MethodUUID').reset_index()
    mask['IncompleteField'] = mask['MethodUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# VariableSpecificUUID_nvarchar(250)_-
def VariableSpecificUUID_AG_Check(dfx, dfy):
    selectionVar = (dfx["VariableSpecificUUID"].isnull()) | (dfx["VariableSpecificUUID"] == '') | (dfx['VariableSpecificUUID'].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for VariableSpecificUUID').reset_index()
    mask['IncompleteField'] = mask['VariableSpecificUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# WaterSourceUUID_nvarchar(250)_-
def WaterSourceUUID_AG_Check(dfx, dfy):
    selectionVar = (dfx["WaterSourceUUID"].isnull()) | (dfx["WaterSourceUUID"] == '') | (dfx['WaterSourceUUID'].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for WaterSourceUUID').reset_index()
    mask['IncompleteField'] = mask['WaterSourceUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# OrganizationUUID_nvarchar(250)_-
def OrganizationUUID_AG_Check(dfx, dfy):
    selectionVar = (dfx["OrganizationUUID"].isnull()) | (dfx["OrganizationUUID"] == '') | (dfx['OrganizationUUID'].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for OrganizationUUID').reset_index()
    mask['IncompleteField'] = mask['OrganizationUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# ReportingUnitUUID_nvarchar(200)_-
def ReportingUnitUUID_AG_Check(dfx, dfy):
    selectionVar = (dfx["ReportingUnitUUID"].isnull()) | (dfx["ReportingUnitUUID"] == '') | (dfx['ReportingUnitUUID'].str.len() > 200)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for ReportingUnitUUID').reset_index()
    mask['IncompleteField'] = mask['ReportingUnitUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationCropDutyAmount_float_Yes
def AllocationCropDutyAmount_AG_Check(dfx, dfy):
    selectionVar = (dfx['AllocationCropDutyAmount'].astype(str).str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationCropDutyAmount').reset_index()
    mask['IncompleteField'] = mask['AllocationCropDutyAmount']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# Amount_float_-
def Amount_AG_Check(dfx, dfy):
    selectionVar = (dfx['Amount'].astype(str).str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Amount').reset_index()
    mask['IncompleteField'] = mask['Amount']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# BeneficialUseCategory_nvarchar(250)_Yes
def BeneficialUseCategory_AG_Check(dfx, dfy):
    selectionVar = (dfx["BeneficialUseCategory"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for BeneficialUseCategory').reset_index()
    mask['IncompleteField'] = mask['BeneficialUseCategory']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# CommunityWaterSupplySystem_nvarchar(250)_Yes
def CommunityWaterSupplySystem_AG_Check(dfx, dfy):
    selectionVar = (dfx["CommunityWaterSupplySystem"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for CommunityWaterSupplySystem').reset_index()
    mask['IncompleteField'] = mask['CommunityWaterSupplySystem']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# CropTypeCV_nvarchar(250)_Yes
def CropTypeCV_AG_Check(dfx, dfy):
    selectionVar = (dfx["CropTypeCV"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for CropTypeCV').reset_index()
    mask['IncompleteField'] = mask['CropTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# CustomerTypeCV_nvarchar((100)_Yes
def CustomerTypeCV_AG_Check(dfx, dfy):
    selectionVar = (dfx["CustomerTypeCV"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for CustomerTypeCV').reset_index()
    mask['IncompleteField'] = mask['CustomerTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# DataPublicationDate_bigint_Yes
def DataPublicationDate_AG_Check(dfx, dfy):
    selectionVar = (dfx["DataPublicationDate"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for DataPublicationDate').reset_index()
    mask['IncompleteField'] = mask['DataPublicationDate']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# DataPublicationDOI_nvarchar(100)_Yes
def DataPublicationDOI_AG_Check(dfx, dfy):
    selectionVar = (dfx["DataPublicationDOI"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for DataPublicationDOI').reset_index()
    mask['IncompleteField'] = mask['DataPublicationDOI']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# InterbasinTransferFromID_nvarchar(100)_Yes
def InterbasinTransferFromID_AG_Check(dfx, dfy):
    selectionVar = (dfx["InterbasinTransferFromID"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for InterbasinTransferFromID').reset_index()
    mask['IncompleteField'] = mask['InterbasinTransferFromID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# InterbasinTransferToID_nvarchar(100)_Yes
def InterbasinTransferToID_AG_Check(dfx, dfy):
    selectionVar = (dfx["InterbasinTransferToID"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for InterbasinTransferToID').reset_index()
    mask['IncompleteField'] = mask['InterbasinTransferToID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# IrrigatedAcreage_float_Yes
def IrrigatedAcreage_AG_Check(dfx, dfy):
    selectionVar = (dfx['IrrigatedAcreage'].astype(str).str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for IrrigatedAcreage').reset_index()
    mask['IncompleteField'] = mask['IrrigatedAcreage']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# IrrigationMethodCV_nvarchar(100)_Yes
def IrrigationMethodCV_AG_Check(dfx, dfy):
    selectionVar = (dfx["IrrigationMethodCV"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for IrrigationMethodCV').reset_index()
    mask['IncompleteField'] = mask['IrrigationMethodCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PopulationServed_bigint_Yes
def PopulationServed_AG_Check(dfx, dfy):
    selectionVar = (dfx["PopulationServed"].astype(str).str.contains(',') == True)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PopulationServed').reset_index()
    mask['IncompleteField'] = mask['PopulationServed']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PowerGeneratedGWh_float_Yes
def PowerGeneratedGWh_AG_Check(dfx, dfy):
    selectionVar = (dfx['PowerGeneratedGWh'].str.contains(',') == True)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PowerGeneratedGWh').reset_index()
    mask['IncompleteField'] = mask['PowerGeneratedGWh']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PowerType_nvarchar(50)_Yes
def PowerType_AG_Check(dfx, dfy):
    selectionVar = (dfx["PowerType"].str.len() > 50)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PowerType').reset_index()
    mask['IncompleteField'] = mask['PowerType']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PrimaryUseCategoryCV_nvarchar(100)_Yes
def PrimaryUseCategoryCV_AG_Check(dfx, dfy):
    selectionVar = (dfx["PrimaryUseCategoryCV"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PrimaryUseCategoryCV').reset_index()
    mask['IncompleteField'] = mask['PrimaryUseCategoryCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# ReportYearCV_nchar(4)_Yes
def ReportYearCV_AG_Check(dfx, dfy):
    selectionVar = (dfx["ReportYearCV"].astype(str).str.len() > 4)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for ReportYearCV').reset_index()
    mask['IncompleteField'] = mask['ReportYearCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# SDWISIdentifierCV_nvarchar(100)_Yes
def SDWISIdentifierCV_AG_Check(dfx, dfy):
    selectionVar = (dfx["SDWISIdentifierCV"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for SDWISIdentifierCV').reset_index()
    mask['IncompleteField'] = mask['SDWISIdentifierCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# TimeframeEnd_bigint_Yes
def TimeframeEnd_AG_Check(dfx, dfy):
    selectionVar = (dfx["TimeframeEnd"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for TimeframeEnd').reset_index()
    mask['IncompleteField'] = mask['TimeframeEnd']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# TimeframeStart_bigint_Yes
def TimeframeStart_AG_Check(dfx, dfy):
    selectionVar = (dfx["TimeframeStart"].str.contains(',') == True)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for TimeframeStart').reset_index()
    mask['IncompleteField'] = mask['TimeframeStart']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# SiteSpecificAmounts_fact
########################################################################################################################
########################################################################################################################

# MethodUUID_nvarchar(200)_-
def MethodUUID_SS_Check(dfx, dfy):
    selectionVar = (dfx["MethodUUID"].isnull()) | (dfx["MethodUUID"] == '') | (dfx['MethodUUID'].str.len() > 200)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for MethodUUID').reset_index()
    mask['IncompleteField'] = mask['MethodUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# VariableSpecificUUID_nvarchar(200)_-
def VariableSpecificUUID_SS_Check(dfx, dfy):
    selectionVar = (dfx["VariableSpecificUUID"].isnull()) | (dfx["VariableSpecificUUID"] == '') | (dfx['VariableSpecificUUID'].str.len() > 200)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for VariableSpecificUUID').reset_index()
    mask['IncompleteField'] = mask['VariableSpecificUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# WaterSourceUUID_nvarchar(200)_-
def WaterSourceUUID_SS_Check(dfx, dfy):
    selectionVar = (dfx["WaterSourceUUID"].isnull()) | (dfx["WaterSourceUUID"] == '') | (dfx['WaterSourceUUID'].str.len() > 200) | (dfx["WaterSourceUUID"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for WaterSourceUUID').reset_index()
    mask['IncompleteField'] = mask['WaterSourceUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# OrganizationUUID_nvarchar(200)_-
def OrganizationUUID_SS_Check(dfx, dfy):
    selectionVar = (dfx["OrganizationUUID"].isnull()) | (dfx["OrganizationUUID"] == '') | (dfx['OrganizationUUID'].str.len() > 200)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for OrganizationUUID').reset_index()
    mask['IncompleteField'] = mask['OrganizationUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# SiteUUID_nvarchar(200)_-
def SiteUUID_SS_Check(dfx, dfy):
    selectionVar = (dfx["SiteUUID"].isnull()) | (dfx["SiteUUID"] == '') | (dfx['SiteUUID'].str.len() > 200)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for SiteUUID').reset_index()
    mask['IncompleteField'] = mask['SiteUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# Amount_float_-
def Amount_SS_Check(dfx, dfy):
    selectionVar = (dfx["Amount"].astype(str).str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for Amount').reset_index()
    mask['IncompleteField'] = mask['Amount']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AllocationCropDutyAmount_float_Yes
def AllocationCropDutyAmount_SS_Check(dfx, dfy):
    selectionVar = dfx["AllocationCropDutyAmount"].astype(str).str.contains(',')
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AllocationCropDutyAmount').reset_index()
    mask['IncompleteField'] = mask['AllocationCropDutyAmount']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# AssociatedNativeAllocationIDs_nvarchar(500)_Yes
def AssociatedNativeAllocationIDs_SS_Check(dfx, dfy):
    selectionVar = dfx["AssociatedNativeAllocationIDs"].str.len() > 500
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for AssociatedNativeAllocationIDs').reset_index()
    mask['IncompleteField'] = mask['AssociatedNativeAllocationIDs']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# BeneficialUseCategory_nvarchar(250)_Yes
def BeneficialUseCategory_SS_Check(dfx, dfy):
    selectionVar = (dfx["BeneficialUseCategory"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for BeneficialUseCategory').reset_index()
    mask['IncompleteField'] = mask['BeneficialUseCategory']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# CommunityWaterSupplySystem_nvarchar(250)_Yes
def CommunityWaterSupplySystem_SS_Check(dfx, dfy):
    selectionVar = (dfx["CommunityWaterSupplySystem"].str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for CommunityWaterSupplySystem').reset_index()
    mask['IncompleteField'] = mask['CommunityWaterSupplySystem']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# CropTypeCV_nvarchar(100)_Yes
def CropTypeCV_SS_Check(dfx, dfy):
    selectionVar = (dfx["CropTypeCV"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for CropTypeCV').reset_index()
    mask['IncompleteField'] = mask['CropTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# CustomerTypeCV_nvarchar((100)_Yes
def CustomerTypeCV_SS_Check(dfx, dfy):
    selectionVar = (dfx["CustomerTypeCV"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for CustomerTypeCV').reset_index()
    mask['IncompleteField'] = mask['CustomerTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# DataPublicationDate_date_Yes
def DataPublicationDate_SS_Check(dfx, dfy):
    selectionVar = (dfx["DataPublicationDate"].astype(str).str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for DataPublicationDate').reset_index()
    mask['IncompleteField'] = mask['DataPublicationDate']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# DataPublicationDOI_nvarchar(100)_Yes
def DataPublicationDOI_SS_Check(dfx, dfy):
    selectionVar = (dfx["DataPublicationDOI"].astype(str).str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for DataPublicationDOI').reset_index()
    mask['IncompleteField'] = mask['DataPublicationDOI']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# Geometry_geometry_Yes
# ???? How to check for geometry datatype

# IrrigatedAcreage_float_Yes
def IrrigatedAcreage_SS_Check(dfx, dfy):
    selectionVar = (dfx["IrrigatedAcreage"].astype(str).str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for IrrigatedAcreage').reset_index()
    mask['IncompleteField'] = mask['IrrigatedAcreage']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# IrrigationMethodCV_nvarchar(100)_Yes
def IrrigationMethodCV_SS_Check(dfx, dfy):
    selectionVar = (dfx["IrrigationMethodCV"].astype(str).str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for IrrigationMethodCV').reset_index()
    mask['IncompleteField'] = mask['IrrigationMethodCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PopulationServed_int_Yes
def PopulationServed_SS_Check(dfx, dfy):
    selectionVar = (dfx["PopulationServed"].astype(str).str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PopulationServed').reset_index()
    mask['IncompleteField'] = mask['PopulationServed']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PowerGeneratedGWh_float_Yes
def PowerGeneratedGWh_SS_Check(dfx, dfy):
    selectionVar = (dfx["PowerGeneratedGWh"].astype(str).str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PowerGeneratedGWh').reset_index()
    mask['IncompleteField'] = mask['PowerGeneratedGWh']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PowerType_nvarchar(50)_Yes
def PowerType_SS_Check(dfx, dfy):
    selectionVar = (dfx["PowerType"].str.len() > 50)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PowerType').reset_index()
    mask['IncompleteField'] = mask['PowerType']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# PrimaryUseCategory_nvarchar(250)_Yes
# This might be bugged.  Issue of must have PrimaryUseCategory for Beneficial Use to be uploaded.
def PrimaryUseCategory_SS_Check(dfx, dfy):
    selectionVar = (dfx["PrimaryUseCategory"].str.len() > 250) | (dfx["PrimaryUseCategory"].isnull()) | (dfx["PrimaryUseCategory"] == '')
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for PrimaryUseCategory').reset_index()
    mask['IncompleteField'] = mask['PrimaryUseCategory']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# ReportYearCV_nchar(4)_Yes
def ReportYearCV_SS_Check(dfx, dfy):
    selectionVar = (dfx["ReportYearCV"].astype(str).str.len() > 4) | (dfx["ReportYearCV"].isnull()) | (dfx["ReportYearCV"] == '') | (dfx["ReportYearCV"] == 0)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for ReportYearCV').reset_index()
    mask['IncompleteField'] = mask['ReportYearCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# SDWISIdentifier_nvarchar(100)_Yes
def SDWISIdentifier_SS_Check(dfx, dfy):
    selectionVar = (dfx["SDWISIdentifier"].str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for SDWISIdentifier').reset_index()
    mask['IncompleteField'] = mask['SDWISIdentifier']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# TimeframeEnd_BigInt_-
def TimeframeEnd_SS_Check(dfx, dfy):
    selectionVar = (dfx["TimeframeEnd"].isnull()) | (dfx["TimeframeEnd"] == "") | (dfx["TimeframeEnd"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for TimeframeEnd').reset_index()
    mask['IncompleteField'] = mask['TimeframeEnd']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# TimeframeStart_BigInt_-
def TimeframeStart_SS_Check(dfx, dfy):
    selectionVar = (dfx["TimeframeStart"].isnull()) |  (dfx["TimeframeStart"] == "") |  (dfx["TimeframeStart"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for TimeframeStart').reset_index()
    mask['IncompleteField'] = mask['TimeframeStart']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# RegulatoryOverlay
########################################################################################################################
########################################################################################################################

# RegulatoryOverlayUUID_nvarchar(250)_-
def RegulatoryOverlayUUID_RE_Check(dfx, dfy):
    selectionVar = (dfx["RegulatoryOverlayUUID"].isnull()) |(dfx["RegulatoryOverlayUUID"] == "") |(dfx['RegulatoryOverlayUUID'].astype(str).str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for RegulatoryOverlayUUID').reset_index()
    mask['IncompleteField'] = mask['RegulatoryOverlayUUID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# OversightAgency_nvarchar(250)_-
def OversightAgency_RE_Check(dfx, dfy):
    selectionVar = (dfx["OversightAgency"].isnull()) | (dfx["OversightAgency"] == "") |(dfx['OversightAgency'].astype(str).str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for OversightAgency').reset_index()
    mask['IncompleteField'] = mask['OversightAgency']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# RegulatoryDescription_nvarchar(MAX)_-
def RegulatoryDescription_RE_Check(dfx, dfy):
    selectionVar = (dfx["RegulatoryDescription"].isnull()) | (dfx["RegulatoryDescription"] == "")
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for RegulatoryDescription').reset_index()
    mask['IncompleteField'] = mask['RegulatoryDescription']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# RegulatoryName_nvarchar(50)_-
def RegulatoryName_RE_Check(dfx, dfy):
    selectionVar = (dfx["RegulatoryName"].isnull()) | (dfx["RegulatoryName"] == "") | (dfx['RegulatoryName'].astype(str).str.len() > 50)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for RegulatoryName').reset_index()
    mask['IncompleteField'] = mask['RegulatoryName']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# RegulatoryOverlayNativeID_nvarchar(250)_Yes
def RegulatoryOverlayNativeID_RE_Check(dfx, dfy):
    selectionVar = (dfx["RegulatoryOverlayNativeID"].astype(str).str.len() > 250)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for RegulatoryOverlayNativeID').reset_index()
    mask['IncompleteField'] = mask['RegulatoryOverlayNativeID']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# RegulatoryStatusCV_nvarchar(50)_-
def RegulatoryStatusCV_RE_Check(dfx, dfy):
    selectionVar = (dfx["RegulatoryStatusCV"].isnull()) | (dfx["RegulatoryStatusCV"] == "") | (dfx['RegulatoryStatusCV'].astype(str).str.len() > 50)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for RegulatoryStatusCV').reset_index()
    mask['IncompleteField'] = mask['RegulatoryStatusCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# RegulatoryStatute_nvarchar(500)_Yes
def RegulatoryStatute_RE_Check(dfx, dfy):
    selectionVar = (dfx["RegulatoryStatute"].astype(str).str.len() > 500)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for RegulatoryStatute').reset_index()
    mask['IncompleteField'] = mask['RegulatoryStatute']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# RegulatoryStatuteLink_nvarchar(500)_Yes
def RegulatoryStatuteLink_RE_Check(dfx, dfy):
    selectionVar = (dfx["RegulatoryStatuteLink"].astype(str).str.len() > 500)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for RegulatoryStatuteLink').reset_index()
    mask['IncompleteField'] = mask['RegulatoryStatuteLink']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# StatutoryEffectiveDate_BigInt_-
def StatutoryEffectiveDate_RE_Check(dfx, dfy):
    selectionVar = (dfx["StatutoryEffectiveDate"].isnull()) | (dfx["StatutoryEffectiveDate"] == "") | (dfx["StatutoryEffectiveDate"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for StatutoryEffectiveDate').reset_index()
    mask['IncompleteField'] = mask['StatutoryEffectiveDate']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# StatutoryEndDate_BigInt_Yes
def StatutoryEndDate_RE_Check(dfx, dfy):
    selectionVar = (dfx["StatutoryEndDate"].str.contains(','))
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for StatutoryEndDate').reset_index()
    mask['IncompleteField'] = mask['StatutoryEndDate']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# RegulatoryOverlayTypeCV_nvarchar(100)_Yes
def RegulatoryOverlayTypeCV_RE_Check(dfx, dfy):
    selectionVar = (dfx["RegulatoryOverlayTypeCV"].astype(str).str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for RegulatoryOverlayTypeCV').reset_index()
    mask['IncompleteField'] = mask['RegulatoryOverlayTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)


# WaterSourceTypeCV_nvarchar(100)_Yes
def WaterSourceTypeCV_RE_Check(dfx, dfy):
    selectionVar = (dfx["WaterSourceTypeCV"].astype(str).str.len() > 100)
    mask = dfx.loc[selectionVar].assign(ReasonRemoved='Incomplete or bad entry for WaterSourceTypeCV').reset_index()
    mask['IncompleteField'] = mask['WaterSourceTypeCV']
    dfx, dfy = removeMaskItemsFunc(dfx, dfy, mask, selectionVar)
    return (dfx, dfy)