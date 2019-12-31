#Date Created: 12/20/2019
#Purpose: To extract ID watersources use infromation and population dataframe for WaDE 2.0.
#Notes:


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading input csv...")
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Idaho/WaterAllocation"
os.chdir(workingDir)
fileInput="RawinputData/ID_Water_Master.csv"
df = pd.read_csv(fileInput)

#WaDE columns
columns=['WaterSourceUUID', 'WaterSourceNativeID',	'WaterSourceName', 'WaterSourceTypeCV',
         'WaterQualityIndicatorCV',	'GNISFeatureNameCV', 'Geometry']

#ry_comment: @dtypesx, list is not being used.
dtypesx = ['BigInt	NVarChar(250)	NVarChar(250)	NVarChar(250)	NVarChar(100)	NVarChar(100)',
           'NVarChar(250)	Geometry']



# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf=pd.DataFrame(columns=columns) #assumes dtypes inferred from CO file

print("WaterSourceName")
outdf['WaterSourceName'] = df['Source']
outdf = outdf.drop_duplicates(subset=['WaterSourceName'])   # dropping duplicates of WaterSourceName.
outdf = outdf.reset_index(drop=True)

print("WaterSourceTypeCV")
outdf['WaterSourceTypeCV'] = df['Source']

print("WaterQualityIndicatorCV") # Hardcoded
outdf.WaterQualityIndicatorCV = 'Fresh'

print("GNISFeatureNameCV") # Hardcoded
outdf.Geometry = ''

print("Geometry") # Hardcoded
outdf.Geometry = ''

print("WaterSourceNativeID")
# has to be one of the last, need length of created outdf
outdf['WaterSourceNativeID'] = range(1, len(outdf.index) + 1)

print("WaterSourceUUID") #native source identifier and the organization univeral id
# has to be one of the last, need WaterSourceNativeID to create
for ix in range(len(outdf.index)):
    outdf.loc[ix, 'WaterSourceUUID'] = "_".join(["IDWR",str(outdf.loc[ix, 'WaterSourceNativeID'])])

# Check required fields are not null
############################################################################
#Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
print("Checking required is not null...")
#ry_comment: @requiredCols, this list isn't being used for anything.
requiredCols=['WaterSourceUUID', 'WaterSourceTypeCV', 'WaterQualityIndicatorCV']

#replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan)
outdf100_nullMand = outdf.loc[(outdf["WaterSourceUUID"].isnull()) | (outdf["WaterSourceTypeCV"].isnull()) |
                                (outdf["WaterQualityIndicatorCV"].isnull())]


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")
outdf.to_csv('ProcessedInputData/watersources.csv', index=False)

#Report missing values if need be to seperate csv
if(len(outdf100_nullMand.index) > 0):
    outdf100_nullMand.to_csv('watersources_mandatoryFieldMissing.csv')  # index=False,

print("Done.")
