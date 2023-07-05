

def GetMethodsColumnsFunction():
    columnslist = [
        "MethodUUID",
        "ApplicableResourceTypeCV",
        "DataConfidenceValue",
        "DataCoverageValue",
        "DataQualityValueCV",
        "MethodDescription",
        "MethodName",
        "MethodNEMILink",
        "MethodTypeCV"]
    return (columnslist)

def GetVariablesColumnsFunction():
    columnslist = [
        "VariableSpecificUUID",
        "AggregationInterval",
        "AggregationIntervalUnitCV",
        "AggregationStatisticCV",
        "AmountUnitCV",
        "MaximumAmountUnitCV",
        "ReportYearStartMonth",
        "ReportYearTypeCV",
        "VariableCV",
        "VariableSpecificCV"]
    return (columnslist)

def GetOrganizationsColumnsFunction():
    columnslist = [
        "OrganizationUUID",
        "OrganizationContactEmail",
        "OrganizationContactName",
        "OrganizationDataMappingURL",
        "OrganizationName",
        "OrganizationPhoneNumber",
        "OrganizationPurview",
        "OrganizationWebsite",
        "State"]
    return (columnslist)

def GetWaterSourcesColumnsFunction():
    columnslist = [
        "WaterSourceUUID",
        "Geometry",
        "GNISFeatureNameCV",
        "WaterQualityIndicatorCV",
        "WaterSourceName",
        "WaterSourceNativeID",
        "WaterSourceTypeCV",
        "WaDEUUID"]
    return (columnslist)

def GetSitesColumnsFunction():
    columnslist = [
        "SiteUUID",
        "RegulatoryOverlayUUIDs",
        "WaterSourceUUIDs",
        "CoordinateAccuracy",
        "CoordinateMethodCV",
        "County",
        "EPSGCodeCV",
        "Geometry",
        "GNISCodeCV",
        "HUC12",
        "HUC8",
        "Latitude",
        "Longitude",
        "NHDNetworkStatusCV",
        "NHDProductCV",
        "PODorPOUSite",
        "SiteName",
        "SiteNativeID",
        "SitePoint",
        "SiteTypeCV",
        "StateCV",
        "USGSSiteID",
        "WaDEUUID"]
    return (columnslist)

def GetReportingUnitColumnsFunction():
    columnslist = [
        "ReportingUnitUUID",
        "EPSGCodeCV",
        "ReportingUnitName",
        "ReportingUnitNativeID",
        "ReportingUnitProductVersion",
        "ReportingUnitTypeCV",
        "ReportingUnitUpdateDate",
        "StateCV",
        "Geometry",
        "WaDEUUID"]
    return (columnslist)

def GetAllocationAmountsColumnsFunction():
    columnslist = [
        "AllocationUUID",
        "MethodUUID",
        "OrganizationUUID",
        "SiteUUID",
        "VariableSpecificUUID",
        "AllocationApplicationDate",
        "AllocationAssociatedConsumptiveUseSiteIDs",
        "AllocationAssociatedWithdrawalSiteIDs",
        "AllocationBasisCV",
        "AllocationChangeApplicationIndicator",
        "AllocationCommunityWaterSupplySystem",
        "AllocationCropDutyAmount",
        "AllocationExpirationDate",
        "AllocationFlow_CFS",
        "AllocationLegalStatusCV",
        "AllocationNativeID",
        "AllocationOwner",
        "AllocationPriorityDate",
        "AllocationSDWISIdentifierCV",
        "AllocationTimeframeEnd",
        "AllocationTimeframeStart",
        "AllocationTypeCV",
        "AllocationVolume_AF",
        "BeneficialUseCategory",
        "CommunityWaterSupplySystem",
        "CropTypeCV",
        "CustomerTypeCV",
        "DataPublicationDate",
        "DataPublicationDOI",
        "ExemptOfVolumeFlowPriority",
        "GeneratedPowerCapacityMW",
        "IrrigatedAcreage",
        "IrrigationMethodCV",
        "LegacyAllocationIDs",
        "OwnerClassificationCV",
        "PopulationServed",
        "PowerType",
        "PrimaryBeneficialUseCategory",
        "WaterAllocationNativeURL",
        "WaDEUUID"]
    return (columnslist)

def GetSiteSpecificAmountsColumnsFunction():
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
        "TimeframeStart",
        "WaDEUUID"]
    return (columnslist)

def GetRegulatoryOverlaysColumnsFunction():
    columnslist = [
        "RegulatoryOverlayUUID",
        "OversightAgency",
        "RegulatoryDescription",
        "RegulatoryName",
        "RegulatoryOverlayNativeID",
        "RegulatoryStatusCV",
        "RegulatoryStatute",
        "RegulatoryStatuteLink",
        "StatutoryEffectiveDate",
        "StatutoryEndDate",
        "RegulatoryOverlayTypeCV",
        "WaterSourceTypeCV",
        "WaDEUUID"]
    return (columnslist)

def GetRegulatoryReportingUnitsColumnsFunction():
    columnslist = [
        "DataPublicationDate",
        "OrganizationUUID",
        "RegulatoryOverlayUUID",
        "ReportingUnitUUID"]
    return (columnslist)

def GetAggregatedAmountsColumnsFunction():
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
        "PrimaryUseCategoryCV",
        "ReportYearCV",
        "SDWISIdentifierCV",
        "TimeframeEnd",
        "TimeframeStart"]
    return (columnslist)
