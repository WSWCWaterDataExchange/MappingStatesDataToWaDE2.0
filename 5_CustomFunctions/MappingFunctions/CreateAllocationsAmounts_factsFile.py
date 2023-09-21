# Date Update: 08/09/2023
# Purpose: To extract water right record information and populate dataframe for WaDE 2.0.


# Needed Libraries
############################################################################
import os
import sys
import numpy as np
import pandas as pd
import re
from datetime import date
from datetime import timedelta



# Custom Libraries
############################################################################

# columns
sys.path.append("../../5_CustomFunctions/MappingFunctions")
import GetColumnsFile

# Owner Classification Fix
sys.path.append("../../5_CustomFunctions/OwnerClassification")
import OwnerClassificationField

# Assign Primary Use Category fix
sys.path.append("../../5_CustomFunctions/AssignPrimaryUseCategory")
import AssignPrimaryUseCategoryFile

# Test WaDE Data for any Errors
sys.path.append("../../5_CustomFunctions/ErrorCheckCode")
import ErrorCheckCodeFunctionsFile

# Clean data and data types
sys.path.append("../../5_CustomFunctions/CleanDataCode")
import CleanDataCodeFunctionsFile


# Create File Function
############################################################################
def CreateAllocationsAmounts_factsInputFunction(workingDirString, varST, varUUIDType, mainInputFile):

    # Inputs
    ############################################################################
    print("Reading input csv...")
    workingDir = workingDirString
    os.chdir(workingDir)
    fileInput = "RawinputData/" + mainInputFile
    df = pd.read_csv(fileInput, compression='zip')

    # Input Data - 'WaDE Input' files.
    dfv = pd.read_csv("ProcessedInputData/variables.csv").replace(np.nan, "")
    dfs = pd.read_csv("ProcessedInputData/sites.csv").replace(np.nan, "")

    # WaDE columns
    AllocationAmountsColumnsList = GetColumnsFile.GetAllocationAmountsColumnsFunction()


    # Custom Functions
    ############################################################################
    # For creating SiteUUID
    SiteUUIDDdict = pd.Series(dfs.SiteUUID.values, index=dfs.SiteNativeID.astype(str)).to_dict()
    def retrieveSiteUUID(colrowValue):
        if colrowValue == '' or pd.isnull(colrowValue):
            outList = ''
        else:
            strVal = str(colrowValue).strip()
            try:
                outList = SiteUUIDDdict[strVal]
            except:
                outList = ''
        return outList

    # For creating UUID
    def assignUUID(Val):
        Val = str(Val)
        Val = re.sub("[$@&.;,/\)(-]", "", Val).strip().replace(" ", "")
        Val = varST + varUUIDType + "_WR" + Val
        return Val


    # Creating output dataframe (outdf)
    ############################################################################
    print("Populating dataframe outdf...")
    outdf = pd.DataFrame(columns=AllocationAmountsColumnsList, index=df.index)  # The output dataframe

    print("MethodUUID")
    outdf['MethodUUID'] = df['in_MethodUUID']

    print("OrganizationUUID")
    outdf['OrganizationUUID'] = df['in_OrganizationUUID']

    print("SiteUUID")
    outdf['SiteUUID'] = df.apply(lambda row: retrieveSiteUUID(row['in_SiteNativeID']), axis=1)

    print("VariableSpecificUUID")
    outdf['VariableSpecificUUID'] = df['in_VariableSpecificUUID']

    print("AllocationApplicationDate")
    outdf['AllocationApplicationDate'] = df['in_AllocationApplicationDate']

    print("AllocationAssociatedConsumptiveUseSiteIDs")
    outdf['AllocationAssociatedConsumptiveUseSiteIDs'] = df['in_AllocationAssociatedConsumptiveUseSiteIDs']

    print("AllocationAssociatedWithdrawalSiteIDs")
    outdf['AllocationAssociatedWithdrawalSiteIDs'] = df['in_AllocationAssociatedWithdrawalSiteIDs']

    print("AllocationBasisCV")
    outdf['AllocationBasisCV'] = df['in_AllocationBasisCV']

    print("AllocationChangeApplicationIndicator")
    outdf['AllocationChangeApplicationIndicator'] = df['in_AllocationChangeApplicationIndicator']

    print("AllocationCommunityWaterSupplySystem")
    outdf['AllocationCommunityWaterSupplySystem'] = df['in_AllocationCommunityWaterSupplySystem']

    print("AllocationCropDutyAmount")
    outdf['AllocationCropDutyAmount'] = df['in_AllocationCropDutyAmount']

    print("AllocationExpirationDate")
    outdf['AllocationExpirationDate'] = df['in_AllocationExpirationDate']

    print("AllocationFlow_CFS")
    outdf['AllocationFlow_CFS'] = df['in_AllocationFlow_CFS']

    print("AllocationLegalStatusCV")
    outdf['AllocationLegalStatusCV'] = df['in_AllocationLegalStatusCV']

    print("AllocationNativeID")  # Will use this with a .groupby() statement towards the ends.
    outdf['AllocationNativeID'] = df['in_AllocationNativeID'].astype(str)

    print("AllocationOwner")
    outdf['AllocationOwner'] = df['in_AllocationOwner']

    print("AllocationPriorityDate")
    outdf['AllocationPriorityDate'] = df['in_AllocationPriorityDate']

    print("AllocationSDWISIdentifierCV")
    outdf['AllocationSDWISIdentifierCV'] = df['in_AllocationSDWISIdentifierCV']

    print("AllocationTimeframeEnd")
    outdf['AllocationTimeframeEnd'] = df['in_AllocationTimeframeEnd']

    print("AllocationTimeframeStart")
    outdf['AllocationTimeframeStart'] = df['in_AllocationTimeframeStart']

    print("AllocationTypeCV")
    outdf['AllocationTypeCV'] = df['in_AllocationTypeCV']

    print("AllocationVolume_AF")
    outdf['AllocationVolume_AF'] = df['in_AllocationVolume_AF']

    print("BeneficialUseCategory")
    outdf['BeneficialUseCategory'] = df['in_BeneficialUseCategory']

    print("CommunityWaterSupplySystem")
    outdf['CommunityWaterSupplySystem'] = df['in_CommunityWaterSupplySystem']

    print("CropTypeCV")
    outdf['CropTypeCV'] = df['in_CropTypeCV']

    print("CustomerTypeCV")
    outdf['CustomerTypeCV'] = df['in_CustomerTypeCV']

    print("DataPublicationDate")
    outdf['DataPublicationDate'] = (date.today() - timedelta(days = 1)).strftime('%m/%d/%Y')

    print("DataPublicationDOI")
    outdf['DataPublicationDOI'] = df['in_DataPublicationDOI']

    print("ExemptOfVolumeFlowPriority")
    outdf['ExemptOfVolumeFlowPriority'] = df['in_ExemptOfVolumeFlowPriority']

    print("GeneratedPowerCapacityMW")
    outdf['GeneratedPowerCapacityMW'] = df['in_GeneratedPowerCapacityMW']

    print("IrrigatedAcreage")
    outdf['IrrigatedAcreage'] = df['in_IrrigatedAcreage']

    print("IrrigationMethodCV")
    outdf['IrrigationMethodCV'] = df['in_IrrigationMethodCV']

    print("LegacyAllocationIDs")
    outdf['LegacyAllocationIDs'] = df['in_LegacyAllocationIDs']

    #####################################
    print("OwnerClassificationCV")
    # Temp solution to populate OwnerClassificationCV field.
    outdf['OwnerClassificationCV'] = outdf.apply(lambda row: OwnerClassificationField.CreateOwnerClassification(row['AllocationOwner']), axis=1)
    #####################################

    print("PopulationServed")
    outdf['PopulationServed'] = df['in_PopulationServed']

    print("PowerType")
    outdf['PowerType'] = df['in_PowerType']

    print("PrimaryBeneficialUseCategory")
    outdf['PrimaryBeneficialUseCategory'] = df['in_PrimaryBeneficialUseCategory']

    print("WaterAllocationNativeURL")
    outdf['WaterAllocationNativeURL'] = df['in_WaterAllocationNativeURL']

    print("Adding Data Assessment UUID")
    outdf['WaDEUUID'] = df['WaDEUUID']

    print("Resetting Index")
    outdf = outdf.drop_duplicates().reset_index(drop=True).replace(np.nan, "")

    print("GroupBy outdf duplicates based on key fields...")
    outdf = outdf.groupby('AllocationNativeID').agg(lambda x: ','.join([str(elem) for elem in (list(set(x))) if elem != ""])).replace(np.nan, "").reset_index()
    outdf = outdf[AllocationAmountsColumnsList]  # reorder the dataframe's columns based on ColumnsList


    # Solving WaDE 2.0 Upload Issues
    ############################################################################
    print("Solving WaDE 2.0 upload issues")  # List all temp fixes required to upload data to WaDE here.
    # Note: OwnerClassificationCV can only accept 1 entry at this time. Error due to above merge / we don't allow multiple OwnerClassificationCV.
    def tempfixOCSV(val):
        valList = val.split(",") # convert string to list
        valList.sort() # sort list alphabetically
        if ("WaDE Blank" in valList):
            valList.remove("WaDE Blank") # check if "In Review"  If true, remove.
            valList.append("WaDE Blank") # Append back in "In Review" to end of list.
        result = valList[0] # return only first value in list.
        return result
    outdf['OwnerClassificationCV'] = outdf.apply(lambda row: tempfixOCSV(row['OwnerClassificationCV']), axis=1)

    # Temp solution to populate PrimaryBeneficialUseCategory field.
    # Use Custom import file
    outdf['PrimaryBeneficialUseCategory'] = outdf.apply(lambda row: AssignPrimaryUseCategoryFile.retrievePrimaryUseCategory(row['BeneficialUseCategory']), axis=1)


    # Error Checking Each Field
    ############################################################################
    print("Error checking each field. Purging bad inputs.")
    dfpurge = pd.DataFrame(columns=AllocationAmountsColumnsList)  # Purge DataFrame to hold removed elements
    dfpurge['ReasonRemoved'] = ""
    dfpurge['IncompleteField'] = ""
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.AllocationAmountTestErrorFunctions(outdf, dfpurge)
    print(f'Length of outdf DataFrame: ', len(outdf))
    print(f'Length of dfpurge DataFrame: ', len(dfpurge))


    # Assign UUID value
    ############################################################################
    print("Assign AllocationUUID")  # has to be one of the last.
    outdf = outdf.reset_index(drop=True)
    outdf['AllocationUUID'] = outdf.apply(lambda row: assignUUID(row['AllocationNativeID']), axis=1)  # assign based on native ID
    outdf['AllocationUUID'] = np.where(outdf['AllocationUUID'].duplicated(keep=False),
                                       outdf['AllocationUUID'].astype(str).str.cat(outdf.groupby('AllocationUUID').cumcount().add(1).astype(str), sep='_'),
                                       outdf['AllocationUUID'])

    # Error check AllocationUUID
    outdf, dfpurge = ErrorCheckCodeFunctionsFile.AllocationUUID_AA_Check(outdf, dfpurge)


    # Clean data & check data types before export
    ############################################################################
    print("Cleaning export for correct data types...")
    outdf = CleanDataCodeFunctionsFile.FixAllocationAmountInfoFunctions(outdf)


    # Export to new csv
    ############################################################################
    print("Exporting dataframe...")

    # The working output DataFrame for WaDE 2.0 input.
    outdf.to_csv('ProcessedInputData/waterallocations.csv', index=False)

    # Report purged values.
    if(len(dfpurge.index) > 0): print(f'...', len(dfpurge),  ' records removed.')
    dfpurge.insert(0, 'ReasonRemoved', dfpurge.pop('ReasonRemoved'))
    dfpurge.to_csv('ProcessedInputData/waterallocations_missing.csv', index=False)

    print("Done")

