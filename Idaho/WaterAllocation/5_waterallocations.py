#Date Created: 12/20/2019
#Purpose: To extract ID water allocation information and population dataframe for WaDE 2.0.
#Notes:


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os
from waterallocationsFunctions import *  # a custom funciton package made by Tsega.  Looks like these were mostly relevenat for UT data files only.



# Inputs
############################################################################
print("Reading input csv...")
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Idaho/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/ID_Water_Master.csv"
WaterSourcesdimCSV = "ProcessedInputData/watersources.csv"
SitesdimCSV = "ProcessedInputData/sites.csv"
# MethodsdimCSV = "ProcessedInputData/methods.csv"    #ry_comment: @MethodsdimCSV, might not be using this
# VariablesdimCSV = "ProcessedInputData/variables.csv"  #ry_comment: @VariablesdimCSV, might not be using this
df = pd.read_csv(fileInput)  # The working dataframe.


#WaDE columns
columns=["OrganizationUUID", "SiteUUID", "WaterSourceUUID", "MethodUUID", "VariableSpecificUUID",
        "AllocationNativeID", "AllocationAmount", "AllocationBasisCV", "AllocationChangeApplicationIndicator",
        "AllocationCommunityWaterSupplySystem", "AllocationCropDutyAmount", "AllocationExpirationDate", "AllocationLegalStatusCV",
        "AllocationMaximum", "AllocationOwner", "AllocationPriorityDate", "AllocationSDWISIdentifierCV", "AllocationTypeCV",
        "BeneficialUseCategoryCV", "CustomerTypeCV", "DataPublicationDOI", "Geometry", "IrrigatedAcreage", "LegacyAllocationIDs",
        "PopulationServed", "PowerGeneratedGWh", "PrimaryUseCategoryCV", "TimeframeEndDate", "TimeframeStartDate"]

dtypesx = ['']  #ry_comment: @dtypesx, list is not being used by anything.

outdf = pd.DataFrame(index=df.index, columns=columns)  # The output dataframe for CSV.

# Creating output dataframe (outdf)
############################################################################
print("Populating dataframes...")

print("OrganizationUUID")  # Hardcoded
outdf.OrganizationUUID = "IDWR"

print("SiteUUID")
sdim = pd.read_csv(SitesdimCSV) # sites.csv
df['SiteNativeID'] = sdim['SiteNativeID']
outdf['SiteUUID'] = "IDWR_" + df['SiteNativeID']
# df500 = pd.read_csv(SitesdimCSV, encoding = "ISO-8859-1")
# df = df.assign(SiteUUID='')
# df['SiteUUID'] = df.apply(lambda row: assignSiteID(row['WaterRightNumber'], df500), axis=1)
# outdf['SiteUUID'] = df['SiteUUID']

print("WaterSourceUUID")
df400 = pd.read_csv(WaterSourcesdimCSV, encoding = "ISO-8859-1")
df400 = df400.drop_duplicates(subset=['WaterSourceName'])  # Drop duplicate rows ---this one is not necessary once the water sources table is refined to remove duplicates
df = df.assign(WaterSourceUUID='')
df['WaterSourceUUID'] = df.apply(lambda row: assignWaterSourceID(row['Source'], df400), axis=1)  # This uses the waterallocationsFunciton.py.
outdf['WaterSourceUUID'] = df['WaterSourceUUID']

print("MethodUUID")
outdf['MethodUUID'] = "IDWR_DiversionTracking"

print("VariableSpecificUUID")
outdf['VariableSpecificUUID'] = "Water Allocation_all"

print("AllocationNativeID")
outdf['AllocationNativeID'] = df['RightID']

print("AllocationAmount")  # Hardcoded
df['AllocationAmount'] = "CFS"

print("AllocationBasisCV")
outdf['AllocationBasisCV'] = df['Basis']

print("AllocationChangeApplicationIndicator")  #ry_comment: @AllocationChangeApplicationIndicator, what are we doing for this?
outdf['AllocationChangeApplicationIndicator'] = ''

print("AllocationCommunityWaterSupplySystem")  #ry_comment: @AllocationCommunityWaterSupplySystem, what are we doing for this?
outdf['AllocationCommunityWaterSupplySystem'] = ''

print("AllocationCropDutyAmount")  #ry_comment: @AllocationCropDutyAmount, what are we doing for this?
outdf['AllocationCropDutyAmount'] = ''

print("AllocationExpirationDate")  #ry_comment: leave blank for now.
outdf['AllocationExpirationDate'] = ''

print("AllocationLegalStatusCV")  #ry_comment: leave blank for now.
outdf['AllocationLegalStatusCV'] = ''

print("AllocationMaximum")  # Hardcoded
outdf['AllocationMaximum'] = "AF"

print("AllocationOwner")
outdf['AllocationOwner'] = df['Owner']

print("AllocationPriorityDate")
outdf['AllocationPriorityDate'] = df['PriorityDate']

print("AllocationSDWISIdentifierCV")  #ry_comment: @AllocationSDWISIdentifierCV, what are we doing for this?
outdf['AllocationSDWISIdentifierCV'] = ''

print("AllocationTypeCV")  #ry_comment: leave blank for now.
outdf['AllocationTypeCV'] = ''

print("BeneficialUseCategoryCV")
# df = df.assign(BeneficialUseCategory='')
# df['BeneficialUseCategory'] = df.apply(lambda row: assignBenUseCategory(row['WaterUse']), axis=1)
# outdf['BeneficialUseCategoryCV'] = df['BeneficialUseCategory']
outdf['BeneficialUseCategoryCV'] = df['WaterUse']

print("CustomerTypeCV")  #ry_comment: leave blank for now.
outdf['CustomerTypeCV'] = ''

print("DataPublicationDOI")
outdf['DataPublicationDOI'] = df['WRReport']

print("Geometry")  #ry_comment: leave blank for now.
outdf['CustomerTypeCV'] = ''

print("IrrigatedAcreage")
outdf['DataPublicationDOI'] = df['TotalAcres']

print("LegacyAllocationIDs")  #ry_comment: @LegacyAllocationIDs, what are we doing for this?
outdf['LegacyAllocationIDs'] = ''

print("PopulationServed")  #ry_comment: @PopulationServed, what are we doing for this?
outdf['PopulationServed'] = ''

print("PowerGeneratedGWh")  #ry_comment: @PowerGeneratedGWh, what are we doing for this?
outdf['PowerGeneratedGWh'] = ''

print("PrimaryUseCategoryCV")  #ry_comment: leave blank for now.
outdf['PrimaryUseCategoryCV'] = ''

print("TimeframeEndDate")  #ry_comment: @TimeframeEndDate, what are we doing for this?
outdf['TimeframeEndDate'] = ''

print("TimeframeStartDate")  #ry_comment: @TimeframeStartDate, what are we doing for this?
outdf['TimeframeStartDate'] = ''


print("Dropping null allocations...")
outdf100purge = outdf.loc[(outdf["AllocationAmount"].isnull()) & (outdf["AllocationMaximum"].isnull())]
if len(outdf100purge.index) > 0:
    outdf100purge.to_csv('waterallocations_missing.csv')    #index=False,
    dropIndex = outdf.loc[(outdf["AllocationAmount"].isnull()) & (outdf["AllocationMaximum"].isnull())].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

print("Dropping duplicates...")
outdf100Duplicated=outdf.loc[outdf.duplicated()]
if len(outdf100Duplicated.index) > 0:
    outdf100Duplicated.to_csv("waterallocations_duplicaterows.csv")  # index=False,
    outdf.drop_duplicates(inplace=True)
    outdf = outdf.reset_index(drop=True)



# Check required fields are not null
############################################################################
print("Checking required is not null...")
requiredCols=["OrganizationUUID","VariableSpecificUUID","WaterSourceUUID","MethodUUID", "AllocationPriorityDate"]  #ry_comment: @requiredCols, list is not being used.
outdf = outdf.replace('', np.nan) #replace blank strings by NaN, if there are any
outdf100_nullMand = outdf.loc[(outdf["OrganizationUUID"].isnull()) |
                                (outdf["VariableSpecificUUID"].isnull()) | (outdf["WaterSourceUUID"].isnull()) |
                                (outdf["MethodUUID"].isnull()) | (outdf["AllocationPriorityDate"].isnull())]



# Export to new csv
############################################################################
print("Exporting dataframe to csv...")
outdf.to_csv('ProcessedInputData/waterallocations.csv', index=False)

#Report missing values if need be to seperate csv
if(len(outdf100_nullMand.index) > 0):
    outdf100_nullMand.to_csv('ProcessedInputData/waterallocations_mandatoryFieldMissing.csv')  # index=False,


print("Done.")
