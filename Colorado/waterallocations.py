#!/usr/bin/env python
import pandas as pd
import numpy as np
from sodapy import Socrata
import os
import beneficialUseDictionary

workingDir = "C:/tseg/testData/full/"
os.chdir(workingDir)

fileInput="DWR_Water_Right_-_Net_Amounts.csv"
allocCSV="waterallocations.csv"
siteCSV="sites.csv"
WSdimCSV="watersources.csv"
MethodsCSV="Methods_dim.csv"
varCSV="Variables.csv"

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
df100 = pd.read_csv(fileInput)
#df100 = df.head(10000)

#WaDE columns #'WaDESiteUUID'  # to be assigned by Wade
#UUIDs: 9.15.19: Adel commented "Add UUIDs for all dim tables"
# OrganizationUUID, SiteUUID, VariableSpecificUUID, WaterSourceUUID, MethodUUID
columns=["OrganizationUUID","SiteUUID","VariableSpecificUUID","WaterSourceUUID","MethodUUID","BeneficialUseID",
         "NativeAllocationID","WaterAllocationTypeCV","AllocationOwner","AllocationApplicationDate",
         "AllocationPriorityDate","AllocationLegalStatusCV","AllocationCropDutyAmount","AllocationExpirationDate",
         "AllocationChangeApplicationIndicator","LegacyAllocationIDs","AllocationBasisCV","AllocationAcreage",
         "TimeframeStart","TimeframeEnd","AllocationAmount","AllocationMaximum"]
dtypesx = ['']

#TODO: assumes dtypes inferred from CO file
outdf100=pd.DataFrame(columns=columns)

df100 = df100.replace('', np.nan)

print("Adding SiteUUIDvar...")
#ToDO: append 'CODWR'
#outdf100.SiteUUIDVar = df100.WDID
df100 = df100.assign(SiteUUIDVar=np.nan)  #add new column and make is nan
# no-loop approach?
for ix in range(len(df100.index)):
    df100.loc[ix, 'SiteUUIDVar'] = "_".join(["CODWR",str(df100.loc[ix, 'WDID'])])
#outdf100.SiteUUID = df100['SiteUUIDVar']

print("Beneficial uses...")
#ToDO: look up beneficial use
# may need to modify capitalization in beneficialUseDictionary
benUseDict = beneficialUseDictionary.beneficialUseDictionary
#df100['BeneficialUseCategoryID'] = df100['Decreed Uses']
#df100['BeneficialUseID'] = np.nan
df100 = df100.assign(BeneficialUseID=np.nan)
#
df100 = df100.dropna(subset=['Decreed Uses'])
df100 = df100.reset_index(drop=True)
# find no-loop approach
for ix in range(len(df100.index)):
    print(ix)
    benUseListStrStr = df100.loc[ix, 'Decreed Uses']
    benUseListStr = benUseListStrStr.strip() #remove whitespace chars
    df100.loc[ix, 'BeneficialUseID'] = ",".join(benUseDict[inx] for inx in list(str(benUseListStr)))         #map(lambda x: x, benUseListStr))
#outdf100.BeneficialUseID = df100['BeneficialUseID']

print("Water sources...")
#ToDO: look up WaterSources_dim
wsdim = pd.read_csv(WSdimCSV)
#df100['WaterSourceUUID'] = np.nan
df100 = df100.assign(WaterSourceUUID=np.nan)
for ix in range(len(df100.index)):
     print(ix)
     ml = wsdim.loc[wsdim['WaterSourceName'] == df100.loc[ix,"Water Source"], 'WaterSourceUUID']
     #ml = wsdim.loc[wsdim['WaterSourceName'] == outdf100.WaterSourceVar[ix],'WaterSourceNativeID']
     df100.loc[ix, 'WaterSourceUUID'] = ml.iloc[0]
#outdf100.WaterSourceUUID = df100['WaterSourceUUID']

print("Native allocation...")
#ToDO check logic
#Concentrate the three values of these fields with a - between them (Admin No, Order No, Decreed Units)
#df100['NativeAllocationID'] = np.nan
df100 = df100.assign(NativeAllocationID=np.nan)
# no-loop approach?
for ix in range(len(df100.index)):
    print(ix)
    df100.loc[ix, 'NativeAllocationID'] = "-".join(map(str, [df100["Admin No"].iloc[ix], df100["Order No"].iloc[ix], df100["Decreed Units"].iloc[ix]]))         #map(lambda x: x, benUseListStr))
outdf100.NativeAllocationID = df100.NativeAllocationID
#outdf100.drop(columns='NativeAllocationIDVar', inplace=True)

print("Net absolute net conditional...")
#ToDO: check logic
# If Net Absolute and Net Conditional are both zeros, then value = "Conditional Absolute"
# If the "Net Absolute" is zero and the "Net Conditional" is not zero. Then value="Conditional"
# If the "Net Absolute" is not zero and the "Net Conditional" = zero. Then value="Absolute"
#ToDO: for loop for now
#df100['AllocationLegalStatusCV'] = np.nan
df100 = df100.assign(AllocationLegalStatusCV=np.nan)
for ix in range(len(df100.index)):
    print(ix)
    if((df100["Net Absolute"].iloc[ix] == 0) and (df100["Net Conditional"].iloc[ix] == 0)):
        df100.loc[ix, 'AllocationLegalStatusCV'] = "Conditional Absolute"
    elif ((df100["Net Absolute"].iloc[ix] == 0) and (df100["Net Conditional"].iloc[ix] != 0)):
        df100.loc[ix, 'AllocationLegalStatusCV'] = "Conditional"
    elif ((df100["Net Absolute"].iloc[ix] != 0) and (df100["Net Conditional"].iloc[ix] == 0)):
        df100.loc[ix, 'AllocationLegalStatusCV'] = "Absolute"
#outdf100.AllocationLegalStatusCV = df100.AllocationLegalStatusCV

print("Decreed units...")
#ToDO: check the logic
#If the Decreed Units value="C", then either of Net Absolute,
# or Net Conditional that has value not equal to zero goes into here*
#df100['AllocationAmount'] = np.nan
df100 = df100.assign(AllocationAmount=np.nan)
#stripping any leading/trailing space characters for 'C'/'A'
ACstr=pd.Series([])
ACstr=df100["Decreed Units"].str.strip()
df100["Decreed Units"]=ACstr
for ix in range(len(df100.index)):
    print(ix)
    if((df100["Net Absolute"].iloc[ix] != 0) and (df100["Net Conditional"].iloc[ix] != 0)):
        """
        For a single row, there should be only one value that is not zero in Net Absolute, or Net Conditional.
        If both of them have values that are not zero, then skip loading this row 
        (The data we have for now does not have this case, but just in case)
        """
        #ToDO save these rows for inspection?
        pass
    else:
        if((df100["Decreed Units"].iloc[ix] == "C") and (df100["Net Absolute"].iloc[ix] != 0)):
            df100.loc[ix, 'AllocationAmount'] = df100["Net Absolute"].iloc[ix]
        elif ((df100["Decreed Units"].iloc[ix] == "C") and (df100["Net Conditional"].iloc[ix] != 0)):
            df100.loc[ix, 'AllocationAmount'] = df100["Net Conditional"].iloc[ix]
        else:
            ## TODO: check this is the case of units == 'A'
            pass
#outdf100.AllocationAmount = df100.AllocationAmount
#ToDO: check the logic
# If the Decreed Units value="A", then either of Net Absolute,
# or Net Conditional that has value not equal to zero goes into here*
#df100['AllocationMaximum'] = np.nan
df100 = df100.assign(AllocationMaximum=np.nan)
#stripping any leading/trailing space characters for 'C'/'A' --done above
for ix in range(len(df100.index)):
    print(ix)
    if((df100["Net Absolute"].iloc[ix] != 0) and (df100["Net Conditional"].iloc[ix] != 0)):
        """
        For a single row, there should be only one value that is not zero in Net Absolute, or Net Conditional.
        If both of them have values that are not zero, then skip loading this row 
        (The data we have for now does not have this case, but just in case)
        """
        # ToDO save these rows for inspection?
        pass
    else:
        if((df100["Decreed Units"].iloc[ix] == "A") and (df100["Net Absolute"].iloc[ix] != 0)):
            df100.loc[ix, 'AllocationMaximum'] = df100["Net Absolute"].iloc[ix]
        elif ((df100["Decreed Units"].iloc[ix] == "C") and (df100["Net Conditional"].iloc[ix] != 0)):
            df100.loc[ix, 'AllocationMaximum'] = df100["Net Conditional"].iloc[ix]
        else:
            ## TODO: Check this is the case of units='C'
            pass
#outdf100.AllocationMaximum = df100.AllocationMaximum
#direct copy
"""
outdf100.SiteUUID = df100['SiteUUIDVar']
outdf100.WaterSourceUUID = df100['WaterSourceUUID']
outdf100.BeneficialUseID = df100['BeneficialUseID']
outdf100.NativeAllocationID = df100.NativeAllocationID
outdf100.AllocationOwner =	df100['Structure Name']
outdf100.AllocationApplicationDate = df100['Appropriation Date']
outdf100.AllocationPriorityDate = df100['Appropriation Date']
outdf100.AllocationLegalStatusCV = df100.AllocationLegalStatusCV
outdf100.AllocationAmount = df100.AllocationAmount
outdf100.AllocationMaximum = df100.AllocationMaximum
"""
print("Copying all columns...")
destCols=["SiteUUID","WaterSourceUUID","BeneficialUseID","NativeAllocationID","AllocationOwner","AllocationApplicationDate",
             "AllocationPriorityDate","AllocationLegalStatusCV","AllocationAmount","AllocationMaximum"]
sourCols=["SiteUUIDVar","WaterSourceUUID","BeneficialUseID","NativeAllocationID","Structure Name","Appropriation Date",
             "Appropriation Date","AllocationLegalStatusCV","AllocationAmount","AllocationMaximum"]
outdf100[destCols] = df100[sourCols]

#hard coded
print("Hard coded...")
outdf100.OrganizationUUID = "CODWR"
outdf100.VariableSpecificUUID = "CODWR Allocation All"
outdf100.MethodUUID = "CODWR-DiversionTracking"
outdf100.AllocationBasisCV = "Unknown"
outdf100.TimeframeStart = "01/01"
outdf100.TimeframeEnd = "12/31"
""" 
Comment from Adel
1) AllocationAmount/Allocation maximum empty cells -- one of them empty is acceptable but not both
==> find if both Allocation amount and Allocation maximum are empty 
==> and delete row :drop
==> save row to a Allocations_missing.csv
"""
print("Droping null allocations...")
#outdf100 = outdf100.replace('', np.nan) #replace blank strings by NaN
outdf100purge = outdf100.loc[(outdf100["AllocationAmount"].isnull()) & (outdf100["AllocationMaximum"].isnull())]
if len(outdf100purge.index) > 0:
    outdf100purge.to_csv('waterallocations_missing.csv')    #index=False,
    dropIndex = outdf100.loc[(outdf100["AllocationAmount"].isnull()) & (outdf100["AllocationMaximum"].isnull())].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

print("Droping duplicates...")
#drop duplicate rows; just make sure
outdf100Duplicated=outdf100.loc[outdf100.duplicated()]
if len(outdf100Duplicated.index) > 0:
    outdf100Duplicated.to_csv("waterallocations_duplicaterows.csv")  # index=False,
    outdf100.drop_duplicates(inplace=True)   #
    outdf100 = outdf100.reset_index(drop=True)
#remove duplicate index
#outdf100[~outdf100.index.duplicated()]

print("Checking required is not null...")
#9.9.19: Adel: check all 'required' (not NA) columns have value (not empty)
#"SiteUUID",
requiredCols=["OrganizationUUID","VariableSpecificUUID","WaterSourceUUID","MethodUUID", "AllocationPriorityDate"]
outdf100 = outdf100.replace('', np.nan) #replace blank strings by NaN, if there are any
#any cell of these columns is null
#outdf100_nullMand = outdf100.loc[outdf100.isnull().any(axis=1)] --for all cols
#(outdf100["SiteUUID"].isnull()) |
outdf100_nullMand = outdf100.loc[(outdf100["OrganizationUUID"].isnull()) |
                                (outdf100["VariableSpecificUUID"].isnull()) | (outdf100["WaterSourceUUID"].isnull()) |
                                (outdf100["MethodUUID"].isnull()) | (outdf100["AllocationPriorityDate"].isnull())]
#outdf100_nullMand = outdf100.loc[[False | (outdf100[varName].isnull()) for varName in requiredCols]]
if(len(outdf100_nullMand.index) > 0):
    outdf100_nullMand.to_csv('waterallocations_mandatoryFieldMissing.csv')  # index=False,
#ToDO: purge these cells if there is any missing? #For now left to be inspected

print("Writing outputs...")
#write out
outdf100.to_csv(allocCSV, index=False)

print("done Water Allocation")