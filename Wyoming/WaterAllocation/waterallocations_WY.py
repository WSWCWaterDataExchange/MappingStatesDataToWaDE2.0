#!/usr/bin/env python
import pandas as pd
import numpy as np
from sodapy import Socrata
import os
import Dictionaries_WY

workingDir = "/Users/augustus/Desktop/WSWC/WaDE/Data/WY"
os.chdir(workingDir)

#fileInput="WyoPOUMaster.csv"
fileInput = "WyoPODSample.csv"


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



#ToDO: SiteUUIDVar Status: DONE
print("Adding SiteUUIDvar...")
#ToDO: append 'CODWR'
#outdf100.SiteUUIDVar = df100.WDID

# remove '.' from site names.  I.e. 'Main No. 1 Canal' is same as 'Main No 1 Canal'
# this was done in sites.csv, so replicate process here
df100['FacilityName'] = df100['FacilityName'].str.replace('.', '')
sitesdim = pd.read_csv(siteCSV)
df100 = df100.assign(SiteUUID=np.nan)
for ix in range(len(df100.index)):
     print(ix)
     ml = sitesdim.loc[sitesdim['SiteName'] == df100.loc[ix,"FacilityName"], 'WaDESiteUUID']
     print(ml)
     x = ml.iloc[0]
     #ml = wsdim.loc[wsdim['WaterSourceName'] == outdf100.WaterSourceVar[ix],'WaterSourceNativeID']
     df100.loc[ix, 'SiteUUID'] = x
#outdf100.WaterSourceUUID = df100['WaterSourceUUID']

#add new column and make is nan
# no-loop approach?
#for ix in range(len(df100.index)):
#    df100.loc[ix, 'SiteUUIDVar'] = "_".join(["CODWR",str(df100.loc[ix, 'WDID'])])
#outdf100.SiteUUID = df100['SiteUUIDVar']



#ToDO: Beneficial Use Status: DONE
print("Beneficial uses...")
# may need to modify capitalization in beneficialUseDictionary
benUseDict = Dictionaries_WY.beneficialUseDictionary
#df100['BeneficialUseCategoryID'] = df100['Decreed Uses']
#df100['BeneficialUseID'] = np.nan
df100 = df100.assign(BeneficialUseID=np.nan)

# Change 'Decreed Uses' from CO code to 'Uses' for WY code
#df100 = df100.dropna(subset=['Uses'])
#df100 = df100.reset_index(drop=True)
# find no-loop approach
# Can't strip white space with np.nan present.  Convert np.nan to '-'
df100['Uses']= df100['Uses'].fillna('-')
for ix in range(len(df100.index)):
    print(ix)
    benUseListStrStr = df100.loc[ix, 'Uses']
    benUseListStr = benUseListStrStr.replace(" ", "")
    benUseList = benUseListStr.split(';')

    df100.loc[ix, 'BeneficialUseID'] = ",".join(benUseDict[inx] for inx in benUseList).upper()         #map(lambda x: x, benUseListStr))
#outdf100.BeneficialUseID = df100['BeneficialUseID']


#ToDO: Water Sources Status: DONE
print("Water sources...")
wsdim = pd.read_csv(WSdimCSV)
#df100['WaterSourceUUID'] = np.nan
df100 = df100.assign(WaterSourceUUID=np.nan)
df100['Stream Source'] = df100['Stream Source'].fillna('Unknown')
df100['Stream Source'] = df100['Stream Source'].str.upper()
for ix in range(len(df100.index)):
     print(ix)
     ml = wsdim.loc[wsdim['WaterSourceName'] == df100.loc[ix, "Stream Source"], 'WaterSourceUUID']
     # ml = wsdim.loc[wsdim['WaterSourceName'] == outdf100.WaterSourceVar[ix],'WaterSourceNativeID']
     df100.loc[ix, 'WaterSourceUUID'] = ml.iloc[0]

#outdf100.WaterSourceUUID = df100['WaterSourceUUID']

#ToDO:  Allocation Owner Status:  DONE
print("Allocation Owner...")
df100 = df100.assign(AllocationOwner=np.nan).astype(str)
df100['Company'] = df100['Company'].fillna('-')
for i, row in df100.iterrows():
    x = row['Company']
    y = row['FirstName']
    z = row['LastName']
    zz = y +'_'+ z
    if x == 'nan':
        df100.at[i, 'AllocationOwner'] = zz
    else:
        df100.at[i, 'AllocationOwner'] = x
    print('done')

# Can just copy columns from Total Flow and Total Capacity, check with logic for dual blanks,
# if both NaN, drop row.

print("Allocation Amount...")
df100['AllocationAmount'] = df100['Total Flow(CFS)/ Appropriation(GPM)']

print("Allocation maximum...")
df100['AllocationMaximum'] = df100['Total Capacity (AF/Yr)']

print("Allocation Legal Status...")
df100['AllocationLegalStatusCV'] = df100['SummaryWRStatus']

print("Allocation Priority Date...")
df100['AllocationPriorityDate'] = df100['PriorityDate']



#direct copy

outdf100.NativeAllocationID = df100['WR Number']
outdf100.SiteUUID = df100['SiteUUID']
outdf100.WaterSourceUUID = df100['WaterSourceUUID']
outdf100.BeneficialUseID = df100['BeneficialUseID']
#outdf100.NativeAllocationID = df100.NativeAllocationID
outdf100.AllocationOwner =	df100['AllocationOwner']
#outdf100.AllocationApplicationDate = df100['Appropriation Date']
outdf100.AllocationPriorityDate = df100['AllocationPriorityDate']
outdf100.AllocationLegalStatusCV = df100.AllocationLegalStatusCV
outdf100.AllocationAmount = df100.AllocationAmount
outdf100.AllocationMaximum = df100.AllocationMaximum


print("Copying all columns...")
#destCols=["SiteUUID","WaterSourceUUID","BeneficialUseID","NativeAllocationID","AllocationOwner","AllocationApplicationDate",
#             "AllocationPriorityDate","AllocationLegalStatusCV","AllocationAmount","AllocationMaximum"]
#sourCols=["SiteUUIDVar","WaterSourceUUID","BeneficialUseID","NativeAllocationID","Structure Name","Appropriation Date",
#             "Appropriation Date","AllocationLegalStatusCV","AllocationAmount","AllocationMaximum"]
#outdf100[destCols] = df100[sourCols]

#hard coded
print("Hard coded...")
outdf100.OrganizationUUID = "WWDO"
#outdf100.VariableSpecificUUID = "CODWR Allocation All"
#outdf100.MethodUUID = "CODWR-DiversionTracking"
#outdf100.AllocationBasisCV = "Unknown"
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
outdf100 = outdf100.replace('nan', np.nan) #replace blank strings by NaN
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