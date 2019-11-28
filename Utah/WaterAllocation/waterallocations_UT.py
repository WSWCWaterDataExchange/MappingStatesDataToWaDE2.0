#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
from waterallocationsFunctions import *

workingDir = "C:/Users/gdg12/Desktop/WaDE2.0/UtahCSVs/Test"
os.chdir(workingDir)

# Inputs
fileInput="Water_Master.csv"
FileInput2="UtahOwners.csv"
FileInput3= "Irrigation_Master.csv"
# municipal and power capacity
FielInput4 = 'WTRUSE_Municipal.csv' # WRNUM MUNICIPALITY AllocationCommunityWaterSupplySystem 	
FileInput5 = 'WTRUSE_Power.csv '# WRNUM POWER_CAPACITY/PowerGeneratedGWh, POWER_UNITS/div by M
# water sources look up
inp_wtrsrs="watersources.csv"
# sites look up
inpt_sitdim = 'sites.csv'

#output: water allocation
out_alloc = "waterallocations.csv"    #output

######## WaDE columns

#the followwing fields have difference between the table here (edited by DPL) and that on the schema website
#http://schema.westernstateswater.org/tables/Input_AllocationAmounts_fact.html
"""
BeneficialUseCategory, PrimaryUseCategory, AllocationTimeframeStart, AllocationTimeframeEnd, " "
BeneficialUseCategoryCV, PrimaryUseCategoryCV, TimeframeStartDate,	TimeframeEndDate,	Geometry	
"""
# UUIDs: Add UUIDs for all dim tables
# OrganizationUUID, SiteUUID, VariableSpecificUUID, WaterSourceUUID, MethodUUID
columns = ["OrganizationUUID", "SiteUUID", "VariableSpecificUUID", "WaterSourceUUID", "MethodUUID", "PrimaryUseCategory",
           "BeneficialUseCategory", "AllocationNativeID", "AllocationTypeCV", "AllocationOwner",
           "AllocationApplicationDate", "AllocationPriorityDate", "AllocationLegalStatusCV", "AllocationCropDutyAmount",
           "AllocationExpirationDate",
           "AllocationChangeApplicationIndicator", "LegacyAllocationIDs", "AllocationBasisCV", "AllocationTimeframeStart",
           "AllocationTimeframeEnd", "AllocationAmount", "AllocationMaximum", "PopulationServed", "PowerGeneratedGWh",
           "IrrigatedAcreage", "AllocationCommunityWaterSupplySystem", "AllocationSDWISIdentifierCV",
           "AllocationAssociatedWithdrawalSiteIDs", "AllocationAssociatedConsumptiveUseSiteIDs", "WaterAllocationNativeURL",
           "CustomerTypeCV", "IrrigationMethodCV", "CropTypeCV", "CommunityWaterSupplySystem", "DataPublicationDate",
           "DataPublicationDOI"]

dtypesx = [''] #here we could theoretically specify data types for each column name, but we didn't need to do that

### target dataFrame
# TODO: assumes dtypes inferred from CO file
outdf100=pd.DataFrame(columns=columns)

####### Read Inputs and merge tables
# We are joining 'on-left': keep all rows of mater table (check if need to be refined)

print("Reading inputs...")
# water_master
input_columns = ['RECORD_ID', 'WREX_SOURCE', 'WATER_USES', 'WRNUM', 'TYPE_OF_RIGHT', 'DATE_FILED',
               'DATE_PRIORITY', 'WREX_STATUS', 'IRRIGATION_DEPLETION','DATE_TERMINATED',
               'WREX_CFS', 'WREX_ACFT']
df100_l = pd.read_csv(fileInput,encoding = "ISO-8859-1", usecols = input_columns) #, or alternatively encoding = "utf-8"
#df100
#print(len(df100_l.index))
df100_l.drop_duplicates(inplace=True)
#print (len(df100_l.index))

###### Join tables

# Allocation owner
input_owner_cols = ['WRCHEX', 'OWNER_LAST_NAME', 'OWNER_FIRST_NAME']
df200 = pd.read_csv(FileInput2,encoding = "ISO-8859-1", usecols =input_owner_cols)  #UtahOwners
#print(len(df200))
df200.drop_duplicates(inplace=True)
#print(len(df200))
df100_ll=pd.merge(df100_l, df200, left_on='WRNUM', right_on='WRCHEX', how='left') #joined Utahowners table into Master_Table
#df100_ll
#print (len(df100_ll.index))

# Irrigation master
input_irr_cols = ['WRNUM', 'IRRIGATION_ACREAGE', 'USE_BEG_DATE', 'USE_END_DATE']
df300=pd.read_csv(FileInput3,encoding = "ISO-8859-1", usecols = input_irr_cols)
#print(len(df300))
df300.drop_duplicates(inplace=True)
#print(len(df300))
df100_3=pd.merge(df100_ll, df300, left_on='WRNUM', right_on='WRNUM', how='left') #joined Irrigation master table into Master_Table
#df100
#print (len(df100.index))

# municipal 
df350=pd.read_csv(FileInput4,encoding = "ISO-8859-1", usecols = ['WRNUM', 'MUNICIPALITY'])
#print(len(df300))
df350.drop_duplicates(inplace=True)
#print(len(df300))
df100_4=pd.merge(df100_3, df350, left_on='WRNUM', right_on='WRNUM', how='left') 
#df100
#print (len(df100_4.index))

# power capacity
df360=pd.read_csv(FileInput5,encoding = "ISO-8859-1", usecols = ['WRNUM', 'POWER_CAPACITY'])
#print(len(df300))
df360.drop_duplicates(inplace=True)
#print(len(df300))
df100=pd.merge(df100_4, df360, left_on='WRNUM', right_on='WRNUM', how='left')
#df100
#print (len(df100_4.index))
df100.drop_duplicates(inplace=True)
df100 = df100.reset_index(drop=True)
#print (len(df100.index))

#Change number of rows to run
#df100 = df100.head(100000) #only runs first X lines for testing.
#df100

df100 = df100.replace(np.nan, '')
#df100

# water sources look up
df400 = pd.read_csv(inp_wtrsrs,encoding = "ISO-8859-1")
#drop duplicate rows ---this one is not necessary once the water sources table is refined to remove duplicates
df400 = df400.drop_duplicates(subset=['WaterSourceName'])
#df400

# sites look up
df500 = pd.read_csv(inpt_sitdim,encoding = "ISO-8859-1")
#df500
print("Adding SiteUUID...")
#append 'UTDWRE'
df100 = df100.assign(SiteUUID='')  #add new column and make is nan
# 10.24.19 from sites table based on WRNUM maching SiteNativeID / WRCHEX
df100['SiteUUID'] = df100.apply(lambda row: assignSiteID(row['WRNUM'], df500), axis=1)
#df100['SiteUUID'] = df100.apply(lambda row: ('' if (str(row['RECORD_ID']) == '') else ("_".join(["UTDWRE", str(row['RECORD_ID'])]))) , axis=1)
#df100

print("Beneficial uses...")
#
df100 = df100.assign(BeneficialUseCategory='')
## df100 = df100.dropna(subset=['WATER_USES']) 10.15.19 not application here---there are empty cells
##df100 = df100.reset_index(drop=True)
df100['BeneficialUseCategory'] = df100.apply(lambda row: assignBenUseCategory(row['WATER_USES']), axis=1)
#df100

print("Water sources...")
df100 = df100.assign(WaterSourceUUID='')
df100['WaterSourceUUID'] = df100.apply(lambda row: assignWaterSourceID(row['WREX_SOURCE'], df400), axis=1)
#df100

print("AllocationTypeCV...")
df100 = df100.assign(AllocationTypeCV='')
#
df100['AllocationTypeCV'] = df100.apply(lambda row: assignallocTypeCV(row['TYPE_OF_RIGHT']), axis=1)
#df100

print("AllocationOwner...")
df100 = df100.assign(AllocationOwner='')
df100['AllocationOwner'] = df100.apply(lambda row: assignownerName(row['OWNER_LAST_NAME'], row['OWNER_FIRST_NAME']), axis=1)
#df100

print("Allocation Legal Status...")
df100 = df100.assign(AllocationLegalStatusCV='')
df100['AllocationLegalStatusCV'] = df100.apply(lambda row: assignallocLegalStatausCV(row['WREX_STATUS']), axis=1)
#df100

print("Allocation application date...")
df100 = df100.assign(AllocationApplicationDate='')
df100['AllocationApplicationDate'] = df100.apply(lambda row: strLiteralToDateString(row['DATE_FILED']), axis=1)
#df100

print("Allocation priority date...")
df100 = df100.assign(AllocationPriorityDate='')
df100['AllocationPriorityDate'] = df100.apply(lambda row: strLiteralToDateString(row['DATE_PRIORITY']), axis=1)
#df100

print("Power capacity")
df100 = df100.assign(PowerGeneratedGWh='')
# input POWER_UNITS KW; target GW /div by 10000
# TODO: note the target name needs to change to GW
df100['PowerGeneratedGWh'] = df100.apply(lambda row: row['POWER_CAPACITY']/1000000, axis=1)
#df100['PowerGeneratedGWh'] = df100['POWER_CAPACITY'].apply(lambda cp: cp/1000000, axis=1)

print("Copying all columns...")
#
destCols=["SiteUUID",
          "WaterSourceUUID",
          "BeneficialUseCategory", "AllocationNativeID",
          "AllocationTypeCV",
          "AllocationOwner", 
          "AllocationApplicationDate", "AllocationPriorityDate",
          "AllocationLegalStatusCV","AllocationAmount", "AllocationMaximum", "AllocationCropDutyAmount",
          "AllocationExpirationDate", 
          "IrrigatedAcreage",
          "AllocationTimeframeStart", "AllocationTimeframeEnd",
          'AllocationCommunityWaterSupplySystem',
          'PowerGeneratedGWh'
         ]
#
sourCols=["SiteUUID",
          "WaterSourceUUID",
          "BeneficialUseCategory", "WRNUM",
          "AllocationTypeCV",
          "AllocationOwner",
          "AllocationApplicationDate", "AllocationPriorityDate",
          "AllocationLegalStatusCV","WREX_CFS","WREX_ACFT", "IRRIGATION_DEPLETION",
          "DATE_TERMINATED",
          "IRRIGATION_ACREAGE",
          "USE_BEG_DATE", "USE_END_DATE",
          'MUNICIPALITY',
          'PowerGeneratedGWh'
         ]

outdf100[destCols] = df100[sourCols]
#outdf100

# hard coded
print("Hard coded...")
#hard coded
outdf100.OrganizationUUID = "UTDWRE"
outdf100.VariableSpecificUUID = "UTDWRE Allocation All"
outdf100.MethodUUID = "UT_WaterAllocation"
outdf100.AllocationBasisCV = "Unknown"
# check this later
outdf100.PrimaryUseCategory = "Irrigation"
outdf100.DataPublicationDate = datetime.now().strftime('%m/%d/%Y')    #"10/31/2019" # edit this to the code run date

#outdf100

print("Droping null allocations...")
# if both Allocation amount and Allocation maximum are empty drop row and save it to a Allocations_missing.csv
#outdf100 = outdf100.replace('', np.nan) #replace blank strings by NaN,
outdf100purge = outdf100.loc[(outdf100["AllocationAmount"] == '') & (outdf100["AllocationMaximum"] == '')]
if len(outdf100purge.index) > 0:
    outdf100purge.to_csv('waterallocations_missing.csv')    #index=False,
    dropIndex = outdf100.loc[(outdf100["AllocationAmount"] == '') & (outdf100["AllocationMaximum"] == '')].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)
#outdf100

print("Droping null SiteUUIDs...")
outdf100nullID = outdf100.loc[outdf100["SiteUUID"] == '']
if len(outdf100nullID.index) > 0:
    dropIndex = outdf100.loc[outdf100["SiteUUID"] == ''].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)
#outdf100

print("Droping null Priority date...")
outdf100nullPR = outdf100.loc[outdf100["AllocationPriorityDate"] == '']
if len(outdf100nullPR.index) > 0:
    dropIndex = outdf100.loc[outdf100["AllocationPriorityDate"] == ''].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)
#outdf100

print("Droping null WaterSourceUUID...")
outdf100nullPR = outdf100.loc[outdf100["WaterSourceUUID"] == '']
if len(outdf100nullPR.index) > 0:
    dropIndex = outdf100.loc[outdf100["WaterSourceUUID"] == ''].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)
#outdf100

print("Droping duplicate rows...")
#drop duplicate rows; just make sure
outdf100Duplicated=outdf100.loc[outdf100.duplicated()]
if len(outdf100Duplicated.index) > 0:
    outdf100Duplicated.to_csv("waterallocations_duplicaterows.csv")  # index=False,
    outdf100.drop_duplicates(inplace=True)   #
    outdf100 = outdf100.reset_index(drop=True)
#outdf100

print("Droping duplicate key IDs...")
"""from merge statement of stored procedure for waterallocations import:
	MERGE INTO Core.AllocationAmounts_fact AS Target
	USING q1 AS Source ON
		ISNULL(Target.OrganizationID, '') = ISNULL(Source.OrganizationID, '')
		AND ISNULL(Target.AllocationNativeID, '') = ISNULL(Source.AllocationNativeID, '')
		AND ISNULL(Target.VariableSpecificID, '') = ISNULL(Source.VariableSpecificID, '')
		AND ISNULL(Target.PrimaryUseCategoryCV, '') = ISNULL(Source.PrimaryUseCategory, '')
"""

dupColumns = ["OrganizationUUID", "AllocationNativeID", "VariableSpecificUUID", "PrimaryUseCategory"]

outdf100Duplicated=outdf100.loc[outdf100.duplicated(subset=dupColumns)]
if len(outdf100Duplicated.index) > 0:
    print("There are duplicate key IDs")
    outdf100Duplicated.to_csv("waterallocations_duplicateKeyID_rows.csv")  # index=False,
    outdf100.drop_duplicates(subset=dupColumns, inplace=True)   #
    outdf100 = outdf100.reset_index(drop=True)
#outdf100

#outdf100Duplicated

print("Checking required is not null...")
# check if any cell of these columns is null
requiredCols = ["OrganizationUUID", "VariableSpecificUUID", "WaterSourceUUID", "MethodUUID", "AllocationPriorityDate"] #SiteUUID
# outdf100_nullMand = outdf100.loc[outdf100.isnull().any(axis=1)] --for all cols
# outdf100_nullMand = outdf100.loc[outdf100[requiredCols].isnull().any(axis=1)]
#(outdf100["SiteUUID"].isnull()) |
outdf100_nullMand = outdf100.loc[(outdf100["OrganizationUUID"] == '') |
                                (outdf100["VariableSpecificUUID"] == '') |
                                (outdf100["WaterSourceUUID"] == '') |
                                (outdf100["MethodUUID"] == '') |
                                (outdf100["AllocationPriorityDate"] == '')]
#outdf100_nullMand = outdf100.loc[[False | (outdf100[varName].isnull()) for varName in requiredCols]]
if(len(outdf100_nullMand.index) > 0):
    outdf100_nullMand.to_csv('waterallocations_mandatoryFieldMissing.csv')  # index=False,
#ToDO: purge these cells if there is any missing? #For now left to be inspected

#outdf100_nullMand

print("Writing outputs...")
#write out
outdf100.to_csv(out_alloc, index=False, encoding = "utf-8")

print("Done Water Allocation")