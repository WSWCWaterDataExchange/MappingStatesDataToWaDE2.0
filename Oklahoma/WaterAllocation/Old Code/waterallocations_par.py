#!/usr/bin/env python
import pandas as pd
import numpy as np
from mpi4py import MPI
from sodapy import Socrata
import os
import beneficialUseDictionary

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

workingDir = "C:/tseg/testData/fullPar2/"
os.chdir(workingDir)

fileInput = "DWR_Water_Right_-_Net_Amounts.csv"
allocCSV = "waterallocations.csv"
siteCSV = "sites.csv"
WSdimCSV = "watersources.csv"
MethodsCSV = "Methods_dim.csv"
varCSV = "Variables.csv"

# WaDE columns #'WaDESiteUUID'  # to be assigned by Wade
# UUIDs: 9.15.19: Adel commented "Add UUIDs for all dim tables"
# OrganizationUUID, SiteUUID, VariableSpecificUUID, WaterSourceUUID, MethodUUID
columns = ["OrganizationUUID", "SiteUUID", "VariableSpecificUUID", "WaterSourceUUID", "MethodUUID", "PrimaryUseCategory",
           "BeneficialUseCategory", "AllocationNativeID", "AllocationTypeCV", "AllocationOwner", "AllocationApplicationDate",
           "AllocationPriorityDate", "AllocationLegalStatusCV", "AllocationCropDutyAmount", "AllocationExpirationDate",
           "AllocationChangeApplicationIndicator", "LegacyAllocationIDs", "AllocationBasisCV", "AllocationTimeframeStart",
           "AllocationTimeframeEnd", "AllocationAmount", "AllocationMaximum", "PopulationServed", "PowerGeneratedGWh",
           "IrrigatedAcreage", "AllocationCommunityWaterSupplySystem", "AllocationSDWISIdentifierCV",
           "AllocationAssociatedWithdrawalSiteIDs", "AllocationAssociatedConsumptiveUseSiteIDs", "WaterAllocationNativeURL",
           "CustomerTypeCV", "IrrigationMethodCV", "CropTypeCV", "CommunityWaterSupplySystem", "DataPublicationDate", "DataPublicationDOI"]

dtypesx = ['']

# TODO: assumes dtypes inferred from CO file
outdf100 = pd.DataFrame(columns=columns)

##from https://dev.socrata.com/foundry/data.colorado.gov/a8zw-bjth
# client = Socrata("data.colorado.gov", None)
## authenticated client (needed for non-public datasets):
# client = Socrata(data.colorado.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")
# top100 = client.get("a8zw-bjth", limit=100)
## Convert to pandas DataFrame
# df = pd.DataFrame.from_records(top100)
##OR read csv
if rank == 0:
    df100 = pd.read_csv(fileInput)
    #df100 = df.head(103)
    df100 = df100.replace('', np.nan)
    # WaterSources_dim lookup
    wsdim = pd.read_csv(WSdimCSV)
else:
    df100 = None
    wsdim = None

df100 = comm.bcast(df100, root = 0)
comm.Barrier()
wsdim = comm.bcast(wsdim, root = 0)
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
    print("Adding SiteUUIDvar...")
# ToDO: append 'CODWR'
# outdf100.SiteUUIDVar = df100.WDID
df100 = df100.assign(SiteUUIDVar=np.nan)  # add new column and make is nan
# no-loop approach?
for ix in range(len(df100.index)):
    df100.loc[ix, 'SiteUUIDVar'] = "_".join(["CODWR", str(df100.loc[ix, 'WDID'])])
# outdf100.SiteUUID = df100['SiteUUIDVar']

if rank == 0:
    print("Beneficial uses...")
# ToDO: look up beneficial use
# may need to modify capitalization in beneficialUseDictionary
benUseDict = beneficialUseDictionary.beneficialUseDictionary
# df100['BeneficialUseCategoryID'] = df100['Decreed Uses']
# df100['BeneficialUseCategory'] = np.nan
df100 = df100.assign(BeneficialUseCategory=np.nan)
#
df100 = df100.dropna(subset=['Decreed Uses'])
df100 = df100.reset_index(drop=True)
# find no-loop approach
for ix in range(len(df100.index)):
    if rank == 0:
        print(ix)
    benUseListStrStr = df100.loc[ix, 'Decreed Uses']
    benUseListStr = benUseListStrStr.strip()  # remove whitespace chars
    df100.loc[ix, 'BeneficialUseCategory'] = ",".join(
        benUseDict[inx] for inx in list(str(benUseListStr)))  # map(lambda x: x, benUseListStr))
# outdf100.BeneficialUseCategory = df100['BeneficialUseCategory']

if rank == 0:
    print("Water sources...")
# df100['WaterSourceUUID'] = np.nan
df100 = df100.assign(WaterSourceUUID=np.nan)
for ix in range(len(df100.index)):
    if rank == 0:
        print(ix)
    ml = wsdim.loc[wsdim['WaterSourceName'] == df100.loc[ix, "Water Source"], 'WaterSourceUUID']
    # ml = wsdim.loc[wsdim['WaterSourceName'] == outdf100.WaterSourceVar[ix],'WaterSourceNativeID']
    df100.loc[ix, 'WaterSourceUUID'] = ml.iloc[0]
# outdf100.WaterSourceUUID = df100['WaterSourceUUID']

if rank == 0:
    print("Native allocation...")
# ToDO check logic
# Concentrate the three values of these fields with a - between them (Admin No, Order No, Decreed Units)
# df100['AllocationNativeID'] = np.nan
df100 = df100.assign(AllocationNativeID=np.nan)
# no-loop approach?
for ix in range(len(df100.index)):
    if rank == 0:
        print(ix)
    df100.loc[ix, 'AllocationNativeID'] = "-".join(map(str, [df100["Admin No"].iloc[ix], df100["Order No"].iloc[ix],
                                                             df100["Decreed Units"].iloc[
                                                                 ix]]))  # map(lambda x: x, benUseListStr))
outdf100.AllocationNativeID = df100.AllocationNativeID
# outdf100.drop(columns='AllocationNativeIDVar', inplace=True)

if rank == 0:
    print("Net absolute / net conditional...")
# ToDO: check logic
# If Net Absolute and Net Conditional are both zeros, then value = "Conditional Absolute"
# If the "Net Absolute" is zero and the "Net Conditional" is not zero. Then value="Conditional"
# If the "Net Absolute" is not zero and the "Net Conditional" = zero. Then value="Absolute"
# ToDO: for loop for now
# df100['AllocationLegalStatusCV'] = np.nan
df100 = df100.assign(AllocationLegalStatusCV=np.nan)
for ix in range(len(df100.index)):
    if rank == 0:
        print(ix)
    if ((df100["Net Absolute"].iloc[ix] == 0) and (df100["Net Conditional"].iloc[ix] == 0)):
        df100.loc[ix, 'AllocationLegalStatusCV'] = "Conditional Absolute"
    elif ((df100["Net Absolute"].iloc[ix] == 0) and (df100["Net Conditional"].iloc[ix] != 0)):
        df100.loc[ix, 'AllocationLegalStatusCV'] = "Conditional"
    elif ((df100["Net Absolute"].iloc[ix] != 0) and (df100["Net Conditional"].iloc[ix] == 0)):
        df100.loc[ix, 'AllocationLegalStatusCV'] = "Absolute"
# outdf100.AllocationLegalStatusCV = df100.AllocationLegalStatusCV

if rank == 0:
    print("Decreed units...")
# ToDO: check the logic
# If the Decreed Units value="C", then either of Net Absolute,
# or Net Conditional that has value not equal to zero goes into here*
# df100['AllocationAmount'] = np.nan
df100 = df100.assign(AllocationAmount=np.nan)
# stripping any leading/trailing space characters for 'C'/'A'
ACstr = pd.Series([])
ACstr = df100["Decreed Units"].str.strip()
df100["Decreed Units"] = ACstr
for ix in range(len(df100.index)):
    if rank == 0:
        print(ix)
    if ((df100["Net Absolute"].iloc[ix] != 0) and (df100["Net Conditional"].iloc[ix] != 0)):
        """
        For a single row, there should be only one value that is not zero in Net Absolute, or Net Conditional.
        If both of them have values that are not zero, then skip loading this row 
        (The data we have for now does not have this case, but just in case)
        """
        # ToDO save these rows for inspection?
        pass
    else:
        if ((df100["Decreed Units"].iloc[ix] == "C") and (df100["Net Absolute"].iloc[ix] != 0)):
            df100.loc[ix, 'AllocationAmount'] = df100["Net Absolute"].iloc[ix]
        elif ((df100["Decreed Units"].iloc[ix] == "C") and (df100["Net Conditional"].iloc[ix] != 0)):
            df100.loc[ix, 'AllocationAmount'] = df100["Net Conditional"].iloc[ix]
        else:
            ## TODO: check this is the case of units == 'A'
            pass
# outdf100.AllocationAmount = df100.AllocationAmount

if rank == 0:
    print("Allocation maximum...")
# ToDO: check the logic
# If the Decreed Units value="A", then either of Net Absolute,
# or Net Conditional that has value not equal to zero goes into here*
# df100['AllocationMaximum'] = np.nan
df100 = df100.assign(AllocationMaximum=np.nan)
# stripping any leading/trailing space characters for 'C'/'A' --done above
for ix in range(len(df100.index)):
    if rank == 0:
        print(ix)
    if ((df100["Net Absolute"].iloc[ix] != 0) and (df100["Net Conditional"].iloc[ix] != 0)):
        """
        For a single row, there should be only one value that is not zero in Net Absolute, or Net Conditional.
        If both of them have values that are not zero, then skip loading this row 
        (The data we have for now does not have this case, but just in case)
        """
        # ToDO save these rows for inspection?
        pass
    else:
        if ((df100["Decreed Units"].iloc[ix] == "A") and (df100["Net Absolute"].iloc[ix] != 0)):
            df100.loc[ix, 'AllocationMaximum'] = df100["Net Absolute"].iloc[ix]
        elif ((df100["Decreed Units"].iloc[ix] == "A") and (df100["Net Conditional"].iloc[ix] != 0)):
            df100.loc[ix, 'AllocationMaximum'] = df100["Net Conditional"].iloc[ix]
        else:
            ## TODO: Check this is the case of units='C'
            pass
# outdf100.AllocationMaximum = df100.AllocationMaximum

# copy
if rank == 0:
    print("Copying all columns...")
destCols = ["SiteUUID", "WaterSourceUUID", "BeneficialUseCategory", "AllocationNativeID", "AllocationOwner",
            "AllocationApplicationDate",
            "AllocationPriorityDate", "AllocationLegalStatusCV", "AllocationAmount", "AllocationMaximum"]
sourCols = ["SiteUUIDVar", "WaterSourceUUID", "BeneficialUseCategory", "AllocationNativeID", "Structure Name",
            "Appropriation Date",
            "Appropriation Date", "AllocationLegalStatusCV", "AllocationAmount", "AllocationMaximum"]
outdf100[destCols] = df100[sourCols]

# hard coded
if rank == 0:
    print("Hard coded...")
outdf100.OrganizationUUID = "CODWR"
outdf100.VariableSpecificUUID = "Allocation All"
outdf100.MethodUUID = "CODWR-DiversionTracking"
outdf100.PrimaryUseCategory = "Irrigation"
outdf100.AllocationBasisCV = "Unknown"
outdf100.AllocationTimeframeStart = "01/01"
outdf100.AllocationTimeframeEnd = "12/31"
outdf100.DataPublicationDate = "4/24/2019"

""" 
Comment from Adel
1) AllocationAmount/Allocation maximum empty cells -- one of them empty is acceptable but not both
==> find if both Allocation amount and Allocation maximum are empty 
==> and delete row :drop
==> save row to a Allocations_missing.csv
"""
if rank == 0:
    print("Droping null allocations...")
# outdf100 = outdf100.replace('', np.nan) #replace blank strings by NaN
outdf100purge = outdf100.loc[(outdf100["AllocationAmount"].isnull()) & (outdf100["AllocationMaximum"].isnull())]
if len(outdf100purge.index) > 0:
    # outdf100purge.to_csv('waterallocations_missing.csv')    #index=False,
    dropIndex = outdf100.loc[(outdf100["AllocationAmount"].isnull()) & (outdf100["AllocationMaximum"].isnull())].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

if rank == 0:
    print("Droping duplicates...")
# drop duplicate rows; just make sure
outdf100Duplicated = outdf100.loc[outdf100.duplicated()]
if len(outdf100Duplicated.index) > 0:
    # outdf100Duplicated.to_csv("waterallocations_duplicaterows.csv")  # index=False,
    outdf100.drop_duplicates(inplace=True)  #
    outdf100 = outdf100.reset_index(drop=True)
# remove duplicate index
# outdf100[~outdf100.index.duplicated()]

if rank == 0:
    print("Checking required is not null...")
# 9.9.19: Adel: check all 'required' (not NA) columns have value (not empty)
# "SiteUUID",
requiredCols = ["OrganizationUUID", "VariableSpecificUUID", "WaterSourceUUID", "MethodUUID", "AllocationPriorityDate"]
outdf100 = outdf100.replace('', np.nan)  # replace blank strings by NaN, if there are any
# any cell of these columns is null
# outdf100_nullMand = outdf100.loc[outdf100.isnull().any(axis=1)] --for all cols
# (outdf100["SiteUUID"].isnull()) |
outdf100_nullMand = outdf100.loc[(outdf100["OrganizationUUID"].isnull()) |
                                 (outdf100["VariableSpecificUUID"].isnull()) | (outdf100["WaterSourceUUID"].isnull()) |
                                 (outdf100["MethodUUID"].isnull()) | (outdf100["AllocationPriorityDate"].isnull())]
# outdf100_nullMand = outdf100.loc[[False | (outdf100[varName].isnull()) for varName in requiredCols]]
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
    outdf100.to_csv(allocCSV, index=False)

    print("done Water Allocation")
