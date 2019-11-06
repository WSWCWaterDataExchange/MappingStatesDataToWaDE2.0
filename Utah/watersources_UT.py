#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
import beneficialUseDictionary

# working directory
working_dir = "C:/Users/gdg12/Desktop/WaDE2.0/UtahCSVs"
os.chdir(working_dir)

# Input files
fileInput = "Water_Master.csv" #"Water_Master.csv"
FileInput2 = "PointofDiversionTable.csv" # Points of diversion

# output water sources
WSdimCSV = "UTWaterSources.csv" ##this UTWaterSources file output is waterallocation input

##### WaDE columns

columns=['WaterSourceUUID', 'WaterSourceNativeID',	'WaterSourceName', 'WaterSourceTypeCV',
         'WaterQualityIndicatorCV',	'GNISFeatureNameCV', 'Geometry']

dtypesx = ['BigInt	NVarChar(250)	NVarChar(250)	NVarChar(250)	NVarChar(100)	NVarChar(100)',
           'NVarChar(250)	Geometry']

#assumes dtypes inferred from CO file
outdf100=pd.DataFrame(columns=columns)

## read input csv

# Read Inputs and merge tables
# ToDO: We are joining 'on-left': keep all rows of mater table (check if need to be refined)

# water_master
df100_l = pd.read_csv(fileInput,encoding = "ISO-8859-1") #, or alternatively encoding = "utf-8"
#df100_l
print (len(df100_l.index))

#### Join tables

# Points of diversion
df200 = pd.read_csv(FileInput2,encoding = "ISO-8859-1")
df100=pd.merge(df100_l, df200, left_on='WRNUM', right_on='WRCHEX', how='left') #joined Points of diversiont table into Master_Table
#df100
print (len(df100.index))

#df100 = df100.head(10000) #only runs first 100 lines for testing.
df100 = df100.replace('', np.nan)
#df100

print("Water source type...")

benUseDict = beneficialUseDictionary.WaterSourceTypeCVDictionary ##modified key for Utah values

df100 = df100.assign(BeneficialUseCategory=np.nan)
## df100 = df100.dropna(subset=['POD_TYPE']) 10.15.19 not application here---there are empty cells
##df100 = df100.reset_index(drop=True)
# find no-loop approach
for ix in range(len(df100.index)):
    print(ix)
    if pd.notnull(df100.loc[ix, 'POD_TYPE']):    #if not pd.isnull(df100.loc[ix, 'POD_TYPE'])
        benUseListStrStr = df100.loc[ix, 'POD_TYPE']
        benUseListStr = benUseListStrStr.strip() #remove whitespace chars
        df100.loc[ix, 'WaterSourceTypeCV'] = ",".join(benUseDict[inx] for inx in list(str(benUseListStr)))
    else:  # blank to unknown
        df100.loc[ix, 'WaterSourceTypeCV'] = "unknown"
#df100

print("Direct mapping Water source name; water source type ...")
#existing corresponding fields

destCols=['WaterSourceName','WaterSourceTypeCV']
srsCols=['WREX_SOURCE', 'WaterSourceTypeCV']

outdf100[destCols] = df100[srsCols]

print("dropping duplicates...")
#filter the whole table based on a unique combination of site ID, SiteName, #'WaterSourceNativeID',
outdf100 = outdf100.drop_duplicates(subset=['WaterSourceName'])

print("WaterSourceNativeID...")
#9.12.19 Adel: For water sources table, how about we do an incremental ID? like 1, 2, 3 etc?
outdf100 = outdf100.reset_index(drop=True)
outdf100['WaterSourceNativeID'] = range(1, len(outdf100.index) + 1)

print("Adding UUID...")
#9.10.19 add UUID for dim tables
# no-loop approach?
for ix in range(len(outdf100.index)):
    outdf100.loc[ix, 'WaterSourceUUID'] = "_".join(["UT",str(outdf100.loc[ix, 'WaterSourceNativeID'])])
#outdf100

print("Hard coded values...")
#hardcode
outdf100.WaterQualityIndicatorCV = "Fresh"
#outdf100.GNISFeatureNameCV
#outdf100.Geometry

print("Checking required is not null...")
#9.9.19: Adel: check all 'required' (not NA) columns have value (not empty)
#'WaterSourceNativeID',
requiredCols=['WaterSourceUUID', 'WaterSourceTypeCV', 'WaterQualityIndicatorCV']
#replace blank strings by NaN, if there are any
outdf100 = outdf100.replace('', np.nan)
#outdf100_nullMand = outdf100.loc[outdf100.isnull().any(axis=1)] --for all cols#any cell of these columns is null
#(outdf100["WaterSourceNativeID"].isnull()) |
outdf100_nullMand = outdf100.loc[(outdf100["WaterSourceUUID"].isnull()) | (outdf100["WaterSourceTypeCV"].isnull()) |
                                (outdf100["WaterQualityIndicatorCV"].isnull())]
#outdf100_nullMand = outdf100.loc[[False | (outdf100[varName].isnull()) for varName in requiredCols]]
if(len(outdf100_nullMand.index) > 0):
    outdf100_nullMand.to_csv('watersources_mandatoryFieldMissing.csv')  # index=False,
###ToDO: purge these cells if there is any missing? #For now left to be inspected

#outdf100_nullMand

#write out
outdf100.to_csv(WSdimCSV, index=False, encoding = "utf-8")

print("Done watersources")