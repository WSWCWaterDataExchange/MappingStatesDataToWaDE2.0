

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
        "WaDEUUID",
        "WaterSourceUUID",
        "Geometry",
        "GNISFeatureNameCV",
        "WaterQualityIndicatorCV",
        "WaterSourceName",
        "WaterSourceNativeID",
        "WaterSourceTypeCV"]
    return (columnslist)

def GetSitesColumnsFunction():
    columnslist = [
        "WaDEUUID",
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
        "USGSSiteID"]
    return (columnslist)

def GetReportingUnitColumnsFunction():
    columnslist = [
        "WaDEUUID",
        "ReportingUnitUUID",
        "EPSGCodeCV",
        "ReportingUnitName",
        "ReportingUnitNativeID",
        "ReportingUnitProductVersion",
        "ReportingUnitTypeCV",
        "ReportingUnitUpdateDate",
        "StateCV",
        "Geometry"]
    return (columnslist)

def GetAllocationAmountsColumnsFunction():
    columnslist = [
        "WaDEUUID",
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
        "WaterAllocationNativeURL"]
    return (columnslist)

def GetSiteSpecificAmountsColumnsFunction():
    columnslist = [
        "WaDEUUID",
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
    return (columnslist)
