#!/usr/bin/env python
import pandas as pd
import numpy as np
from mpi4py import MPI
import os
import beneficialUseDictionary

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

workingDir = "C:/tseg/jupyterWaDE/"
os.chdir(workingDir)

# Inputs
fileInput="WRCHEX_WATER_MASTER.csv"
WSdimCSV="UTWaterSources.csv"
FileInput2="OWNERS.csv"
FileInput3= "IRRIGATION_MASTER.csv"

#output: water allocation
allocCSV="UTWaterAllocations.csv"    #output

######## WaDE columns  

#the followwing fields have difference between the table here (edited by DPL) and that on the schema website
#http://schema.westernstateswater.org/tables/Input_AllocationAmounts_fact.html
"""
BeneficialUseCategory, PrimaryUseCategory, AllocationTimeframeStart, AllocationTimeframeEnd, " "
BeneficialUseCategoryCV, PrimaryUseCategoryCV, TimeframeStartDate,	TimeframeEndDate,	Geometry	
"""
# UUIDs: 9.15.19: Adel commented "Add UUIDs for all dim tables"
# OrganizationUUID, SiteUUID, VariableSpecificUUID, WaterSourceUUID, MethodUUID
columns = ["OrganizationUUID", "SiteUUID", "VariableSpecificUUID", "WaterSourceUUID", "MethodUUID", "PrimaryUseCategoryCV",
           "BeneficialUseCategoryCV", "AllocationNativeID", "AllocationTypeCV", "AllocationOwner", 
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
# ToDO: We are joining 'on-left': keep all rows of mater table (check if need to be refined)
if rank == 0:

    # water_master
    input_columns = ['RECORD_ID', 'WREX_SOURCE', 'WATER_USES', 'WRNUM', 'TYPE_OF_RIGHT', 'DATE_FILED',
                   'DATE_PRIORITY', 'WREX_STATUS', 'IRRIGATION_DEPLETION','DATE_TERMINATED',
                   'WREX_CFS', 'WREX_ACFT']
    df100_l = pd.read_csv(fileInput,encoding = "ISO-8859-1", usecols = input_columns) #, or alternatively encoding = "utf-8"
    #df100
    print(len(df100_l.index))
    df100_l.drop_duplicates(inplace=True)
    print (len(df100_l.index))

    ###### Join tables

    # Allocation owner
    input_owner_cols = ['WRCHEX', 'OWNER_LAST_NAME', 'OWNER_FIRST_NAME']
    df200 = pd.read_csv(FileInput2,encoding = "ISO-8859-1", usecols =input_owner_cols)  #UtahOwners
    print(len(df200))
    df200.drop_duplicates(inplace=True)
    print(len(df200))
    df100_ll=pd.merge(df100_l, df200, left_on='WRNUM', right_on='WRCHEX', how='left') #joined Utahowners table into Master_Table
    #df100_ll
    #print (len(df100_ll.index))

    # Irrigation master
    input_irr_cols = ['WRNUM', 'IRRIGATION_ACREAGE', 'USE_BEG_DATE', 'USE_END_DATE']
    df300=pd.read_csv(FileInput3,encoding = "ISO-8859-1", usecols = input_irr_cols)
    print(len(df300))
    df300.drop_duplicates(inplace=True)
    print(len(df300))
    df100=pd.merge(df100_ll, df300, left_on='WRNUM', right_on='WRNUM', how='left') #joined Irrigation master table into Master_Table
    #df100
    #print (len(df100.index))

    df100.drop_duplicates(inplace=True)
    df100 = df100.reset_index(drop=True)
    print (len(df100.index))

    #df100 = df100.head(10000) #only runs first 10000 lines for testing.
    #df100

    df100 = df100.replace('', np.nan)
    #df100

    # water sources look up
    df400 = pd.read_csv(WSdimCSV,encoding = "ISO-8859-1")
    #drop duplicate rows ---this one is not necessary once the water sources table is refined to remove duplicates
    df400 = df400.drop_duplicates(subset=['WaterSourceName'])
    #df400
else:
    df100 = None
    df400 = None

df100 = comm.bcast(df100, root = 0)
comm.Barrier()
df400 = comm.bcast(df400, root = 0)
comm.Barrier()

# slice df among procs
numrows_per_proc = int(len(df100.index) / size)
extra_cells = int(len(df100.index) % size)
if rank == 0:
    lower_bound = 0
    upper_bound = numrows_per_proc + extra_cells + 1  # add extras to root # overlap cells at boundary
else:
    lower_bound = rank * numrows_per_proc + extra_cells - 1  # overlap cells at boundary
    upper_bound = (1 + rank) * numrows_per_proc + extra_cells + 1

comm.Barrier()
print("proc ", rank, "lower bound ", lower_bound, " upper bound ", upper_bound)

# divide data frame among procs.
df100 = df100.iloc[lower_bound:upper_bound]  # overlap cells at boundary
df100 = df100.reset_index(drop=True)
comm.Barrier()
#print("proc ", rank)  print(df100)  exit(0)
if rank == 0:
    print("Adding SiteUUID...")
#append 'UTDWRE'
df100 = df100.assign(SiteUUID=np.nan)  #add new column and make is nan

# no-loop approach?

df100['SiteUUID'] = df100.apply(lambda row: "_".join(["UTDWRE", str(row['RECORD_ID'])]), axis=1)

"""
%% timeit
for ix in range(len(df100.index)):
    #print(ix)
    df100.loc[ix, 'SiteUUID'] = "_".join(["UTDWRE",str(df100.loc[ix, 'RECORD_ID'])])
df100['SiteUUID']

%% timeit
siteuuidSer = []
for index, row in df100.iterrows():
    #print(ix)
    siteuuidSer.append("_".join(["UTDWRE", str(row['RECORD_ID'])]))
    # df100.loc[ix, 'SiteUUID'] = "_".join(["UTDWRE",str(df100.loc[ix, 'RECORD_ID'])])
df100['SiteUUID'] = siteuuidSer
df100['SiteUUID']

%% timeit
df100['SiteUUID'] = df100.apply(lambda row: "_".join(["UTDWRE", str(row['RECORD_ID'])]), axis=1)
df100['SiteUUID']

%% timeit
df100['SiteUUID'] = "_".join(["UTDWRE", str(df100['RECORD_ID'])])
df100['SiteUUID']

%% timeit
df100['SiteUUID'] = "_".join(["UTDWRE", str(df100['RECORD_ID'].values)])
df100['SiteUUID']
"""

#df100
if rank == 0:
    print("Beneficial uses...")
#look up beneficial use
# may need to modify capitalization in beneficialUseDictionary
benUseDict = beneficialUseDictionary.beneficialUseDictionary ##modified key for Utah values
#
df100 = df100.assign(BeneficialUseCategory=np.nan)
## df100 = df100.dropna(subset=['WATER_USES']) 10.15.19 not application here---there are empty cells 
##df100 = df100.reset_index(drop=True)
# find no-loop approach
for ix in range(len(df100.index)):
    if rank == 0:
        print(ix)
    if pd.notnull(df100.loc[ix, 'WATER_USES']):    #if not pd.isnull(df100.loc[ix, 'WATER_USES'])
        benUseListStrStr = df100.loc[ix, 'WATER_USES']
        benUseListStr = benUseListStrStr.strip() #remove whitespace chars
        df100.loc[ix, 'BeneficialUseCategory'] = ",".join(benUseDict[inx] for inx in list(str(benUseListStr)))         
        #map(lambda x: x, benUseListStr))
#df100
if rank == 0:
    print("Water sources...")
#look up WaterSources_dim
df100 = df100.assign(WaterSourceUUID=np.nan)
#df100['WaterSourceUUID'] = np.nan
for ix in range(len(df100.index)):
    if rank == 0:
        print(ix)
    ml = df400.loc[df400['WaterSourceName'] == df100.loc[ix,"WREX_SOURCE"], 'WaterSourceUUID']
    #ml = wsdim.loc[wsdim['WaterSourceName'] == outdf100.WaterSourceVar[ix],'WaterSourceNativeID']
    #print(ml)
    #print(ml.empty)
    if not(ml.empty):            # check if the series is empty
        df100.loc[ix, 'WaterSourceUUID'] = ml.iloc[0]

#df100
if rank == 0:
    print("Native allocation...")
# look up allocation dictionary
# may need to modify capitalization in beneficialUseDictionary
AllocationTypeCVDict = beneficialUseDictionary.AllocationTypeCVDictionary ##modified key for Utah values
#df100['BeneficialUseCategoryID'] = df100['Decreed Uses']
#df100['BeneficialUseID'] = np.nan
df100 = df100.assign(AllocationTypeCV=np.nan)
#
##df100 = df100.dropna(subset=['TYPE_OF_RIGHT']) #drop null values
##df100 = df100.reset_index(drop=True)

# find no-loop approach
for ix in range(len(df100.index)):
    if rank == 0:
        print(ix)
    if pd.notnull(df100.loc[ix, 'TYPE_OF_RIGHT']):
        benUseListStrStr = df100.loc[ix, 'TYPE_OF_RIGHT']
        benUseListStr = benUseListStrStr.strip() #remove whitespace chars
        df100.loc[ix, 'AllocationTypeCV'] = AllocationTypeCVDict[benUseListStr]
#df100
if rank == 0:
    print("AllocationOwner...")
df100 = df100.assign(AllocationOwner=np.nan)
# no-loop approach?
for ix in range(len(df100.index)):
    if rank == 0:
        print(ix)
    df100.loc[ix, 'AllocationOwner'] = ",".join(map(str, [df100["OWNER_LAST_NAME"].iloc[ix], df100["OWNER_FIRST_NAME"].iloc[ix]]))
#df100
if rank == 0:
    print("Allocation Legal Status...")
df100 = df100.assign(AllocationLegalStatusCV=np.nan)
#outdf100.AllocationLegalStatusCV = df100.AllocationLegalStatusC
AllocationUseDict = beneficialUseDictionary.AllocationLegalStatusDictionary ##modified key for Utah values. First part is file name, second part is dictionary name I created for Allocation.
##df100 = df100.dropna(subset=['WREX_STATUS']) #drop null values if there is a blank row
##df100 = df100.reset_index(drop=True)

# find no-loop approach
for ix in range(len(df100.index)):
    if rank == 0:
        print(ix)
    if pd.notnull(df100.loc[ix, 'WREX_STATUS']):    #if not pd.isnull(df100.loc[ix, 'WREX_STATUS'])
        benUseListStrStr = df100.loc[ix, 'WREX_STATUS']
        benUseListStr = benUseListStrStr.strip() #remove whitespace chars
        if benUseListStr in AllocationUseDict.keys():
            df100.loc[ix, 'AllocationLegalStatusCV'] = AllocationUseDict[benUseListStr]        #map(lambda x: x, benUseListStr))
#df100


if rank == 0:
    print("Copying all columns...")
#
destCols=["SiteUUID",
          "WaterSourceUUID",
          "BeneficialUseCategory", "AllocationNativeID",
          "AllocationOwner", 
          "AllocationApplicationDate", "AllocationPriorityDate",
          "AllocationLegalStatusCV","AllocationAmount", "AllocationMaximum", "AllocationCropDutyAmount",
          "AllocationExpirationDate", 
          "AllocationAcreage",
          "AllocationTimeframeStart", "AllocationTimeframeEnd"
         ]
#
sourCols=["SiteUUID",
          "WaterSourceUUID",
          "BeneficialUseCategory", "WRNUM", 
          "AllocationOwner",
          "DATE_FILED", "DATE_PRIORITY",
          "AllocationLegalStatusCV","WREX_CFS","WREX_ACFT", "IRRIGATION_DEPLETION",
          "DATE_TERMINATED",
          "IRRIGATION_ACREAGE",
          "USE_BEG_DATE", "USE_END_DATE"
         ]

outdf100[destCols] = df100[sourCols]
#outdf100

# hard coded
if rank == 0:
    print("Hard coded...")
#hard coded
outdf100.OrganizationUUID = "UTDWRE"
outdf100.VariableSpecificUUID = "Water Allocation_all"
outdf100.MethodUUID = "UT_WaterAllocation"
outdf100.AllocationBasisCV = "Unknown"
outdf100.TimeframeStart = "01/01"
outdf100.TimeframeEnd = "12/31"

#outdf100

if rank == 0:
    print("Droping null allocations...")
""" 
Comment from Adel
1) AllocationAmount/Allocation maximum empty cells -- one of them empty is acceptable but not both
==> find if both Allocation amount and Allocation maximum are empty -if they are, then:
==> delete row :drop
==> and save row to a Allocations_missing.csv
"""
#outdf100 = outdf100.replace('', np.nan) #replace blank strings by NaN
outdf100purge = outdf100.loc[(outdf100["AllocationAmount"].isnull()) & (outdf100["AllocationMaximum"].isnull())]
if len(outdf100purge.index) > 0:
    # outdf100purge.to_csv('waterallocations_missing.csv')    #index=False,
    dropIndex = outdf100.loc[(outdf100["AllocationAmount"].isnull()) & (outdf100["AllocationMaximum"].isnull())].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)
#outdf100

if rank == 0:
    print("Droping duplicates...")
#drop duplicate rows; just make sure
outdf100Duplicated=outdf100.loc[outdf100.duplicated()]
if len(outdf100Duplicated.index) > 0:
    # outdf100Duplicated.to_csv("waterallocations_duplicaterows.csv")  # index=False,
    outdf100.drop_duplicates(inplace=True)   #
    outdf100 = outdf100.reset_index(drop=True)
#outdf100
if rank == 0:
    print("Checking required is not null...")
#9.9.19: Adel: check all 'required' (not NA) columns have value (not empty)
requiredCols = ["OrganizationUUID", "VariableSpecificUUID", "WaterSourceUUID", "MethodUUID", "AllocationPriorityDate"] #SiteUUID
outdf100 = outdf100.replace('', np.nan) #replace blank strings by NaN,

# check if any cell of these columns is null
# outdf100_nullMand = outdf100.loc[outdf100.isnull().any(axis=1)] --for all cols
#(outdf100["SiteUUID"].isnull()) |
outdf100_nullMand = outdf100.loc[(outdf100["OrganizationUUID"].isnull()) |
                                (outdf100["VariableSpecificUUID"].isnull()) | (outdf100["WaterSourceUUID"].isnull()) |
                                (outdf100["MethodUUID"].isnull()) | (outdf100["AllocationPriorityDate"].isnull())]
#outdf100_nullMand = outdf100.loc[[False | (outdf100[varName].isnull()) for varName in requiredCols]]
# if(len(outdf100_nullMand.index) > 0):
#    outdf100_nullMand.to_csv('waterallocations_mandatoryFieldMissing.csv')  # index=False,
# ToDO: purge these cells if there is any missing? #For now left to be inspected
if rank == 0:
    print("Gathering...")
# copy tables
outdf100_list = comm.gather(outdf100, root=0)
if rank == 0:
    outdf100 = pd.concat(outdf100_list)
#
outdf100purge_list = comm.gather(outdf100purge, root=0)
if rank == 0:
    outdf100purge = pd.concat(outdf100purge_list)
#
outdf100Duplicated_list = comm.gather(outdf100Duplicated, root=0)
if rank == 0:
    outdf100Duplicated = pd.concat(outdf100Duplicated_list)
#
outdf100_nullMand_list = comm.gather(outdf100_nullMand, root=0)
if rank == 0:
    outdf100_nullMand = pd.concat(outdf100_nullMand_list)
#
if rank == 0:
    print("Droping duplicates in combined table..")
    # drop duplicate rows; just make sure
    outdf100.drop_duplicates(inplace=True)  #
    outdf100 = outdf100.reset_index(drop=True)
    #
    outdf100purge.drop_duplicates(inplace=True)  #
    outdf100purge = outdf100purge.reset_index(drop=True)
    outdf100Duplicated.drop_duplicates(inplace=True)  #
    outdf100Duplicated = outdf100Duplicated.reset_index(drop=True)
    outdf100_nullMand.drop_duplicates(inplace=True)  #
    outdf100_nullMand = outdf100_nullMand.reset_index(drop=True)

    print("Writing outputs...")
    # null allocations
    outdf100purge.to_csv('waterallocations_missing.csv')  # index=False,
    # duplicates
    outdf100Duplicated.to_csv("waterallocations_duplicaterows.csv")  # index=False,
    # mandatory fields mising
    outdf100_nullMand.to_csv('waterallocations_mandatoryFieldMissing.csv')  # index=False,
   
    # combined table
    outdf100.to_csv(allocCSV, index=False, encoding = "utf-8")

    print("done Water Allocation")
