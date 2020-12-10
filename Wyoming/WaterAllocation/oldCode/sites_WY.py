#!/usr/bin/env python
import pandas as pd
import numpy as np
from sodapy import Socrata
import os
import Dictionaries_WY
import sys



"""
Comments from Adel
1) we want to get the unique sites here. so could you filter the whole table based on a unique combination of site ID, SiteName, and SiteType?
2) We probably need to drop the sites with no long and lat. (could you add a code for that and we'll decide to keep it or comment it out later)?
3) hard code "Unknown" for SiteTypeCV value if it is missing
"""

workingDir="/Users/augustus/Desktop/WSWC/WaDE/Data/WY"
os.chdir(workingDir)

#fileInput="WyoPOUMaster.csv"
fileInput = "WyoPODSample.csv"

allocCSV="waterallocations.csv"
siteCSV="sites.csv"
WSdimCSV="watersources.csv"
MethodsCSV="methods.csv"
varCSV="variables.csv"

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

#WaDE columns
columns=['WaDESiteUUID', 'SiteNativeID', 'SiteName', 'USGSSiteID', 'SiteTypeCV', 'Longitude_x', 'Latitude_y',
          'SitePoint', 'SiteNativeURL', 'Geometry', 'CoordinateMethodCV', 'CoordinateAccuracy', 'GNISCodeCV',
          'EPSGCodeCV', 'NHDNetworkStatusCV', 'NHDProductCV', 'NHDUpdateDate', 'NHDReachCode', 'NHDMeasureNumber',
          'StateCV']
dtypesx = ['NVarChar(55)	NVarChar(50)	NVarChar(500)	NVarChar(250)	NVarChar(100)	Double	Double	Geometry',
           'NVarChar(250)	Geometry	NVarChar(100)	NVarChar(255)	NVarChar(50)	NVarChar(50)	NVarChar(50)',
           'NVarChar(50)	Date	NVarChar(50)	NVarChar(50)	NChar(5)']

#assumes dtypes inferred from CO file
outdf100=pd.DataFrame(columns=columns)
#

"""
#existing corresponding fields
outdf100.SiteNativeID =
outdf100.SiteName = df100['FacilityName']
#outdf100.USGSSiteID =
outdf100.SiteTypeCV = df100['PermitSuffix']
outdf100.Longitude_x = df100['Longitude']
outdf100.Latitude_y = df100['Latitude']
#outdf100.Geometry = 
outdf100.CoordinateMethodCV =
#outdf100.CoordinateAccuracy
outdf100.GNISCodeCV =
outdf100.EPSGCodeCV = 
"""
print("Copy columns...")
destCols=['SiteName', 'SiteTypeCV', 'Longitude_x', 'Latitude_y']
sourCols=['FacilityName', 'PermitSuffix', 'Longitude', 'Latitude']
outdf100[destCols] = df100[sourCols]

# remove '.' from site names.  I.e. 'Main No. 1 Canal' is same as 'Main No 1 Canal'
outdf100['SiteName'] = outdf100['SiteName'].str.replace('.', '')

print("Dropping duplicates...")
#ToDO: formatting of some sites prevents them from being dropped, need way to solve this problem
#filter the whole table based on a unique combination of site ID, SiteName, SiteType
outdf100 = outdf100.drop_duplicates(subset=['SiteName'])
#outdf100 = outdf100.drop_duplicates(subset=['SiteName', 'PermitSuffix'])   #
outdf100 = outdf100.reset_index(drop=True)


print('Site type...')
perSufDict = Dictionaries_WY.permitSuffixDictionary
outdf100 = outdf100.assign(sitetype = np.nan)

for ix in range(len(outdf100.index)):
    print(ix)
    perSufList = outdf100.loc[ix, 'SiteTypeCV']
    perSufList = perSufList.strip()
    outdf100.loc[ix, 'sitetype'] = ','.join(perSufDict[inx] for inx in list(str(perSufList)))

outdf100['SiteTypeCV'] = outdf100['sitetype']
outdf100 = outdf100.drop(['sitetype'], axis = 1)

print("Hard code...")
#hard code "Unknown" for SiteTypeCV value if it is missing
#outdf100 = outdf100.replace('', np.nan) #replace blank strings by NaN
outdf100.loc[outdf100['SiteTypeCV'].isnull(),'SiteTypeCV']='Unknown'

print("Dropping empty lat/lon...")
#drop the sites with no long and lat.
outdf100 = outdf100.replace('', np.nan) #replace blank strings by NaN
outdf100purge = outdf100.loc[(outdf100['Longitude_x'].isnull()) | (outdf100['Latitude_y'].isnull())]
if len(outdf100purge.index) > 0:
    outdf100purge.to_csv('sites_missing.csv')    #index=False,
    dropIndex = outdf100.loc[(outdf100['Longitude_x'].isnull()) | (outdf100['Latitude_y'].isnull())].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)


#hardcoded
#outdf100.EPSGCodeCV = 'EPSG:4326'

# Generate SiteNativeID
for ix in range(len(outdf100.index)):
    id = 100000 + ix
    outdf100.loc[ix, 'SiteNativeID'] = id

outdf100.SiteNativeID = outdf100.SiteNativeID.astype(int)
outdf100.SiteNativeID = outdf100.SiteNativeID.astype(str)


print("Adding UUID...")
#9.10.19 add UUID for dim tables
# no-loop approach?
for ix in range(len(outdf100.index)):
    outdf100.loc[ix, 'WaDESiteUUID'] = "_".join(["WWDO",str(outdf100.loc[ix, 'SiteNativeID'])])


print("Checking required isnot null...")
#9.9.19: Adel: check all 'required' (not NA) columns have value (not empty)
#'SiteNativeID',
#requiredCols=['SiteUUID', 'SiteName', 'CoordinateMethodCV', 'EPSGCodeCV']
#replace blank strings by NaN, if there are any
#outdf100 = outdf100.replace('', np.nan)
#any cell of these columns is null
#outdf100_nullMand = outdf100.loc[outdf100.isnull().any(axis=1)] --for all cols
#(outdf100["SiteNativeID"].isnull()) |
#outdf100_nullMand = outdf100.loc[(outdf100["SiteUUID"].isnull()) |
#                                (outdf100["SiteName"].isnull()) | (outdf100["CoordinateMethodCV"].isnull()) |
#                                (outdf100["EPSGCodeCV"].isnull())]
#outdf100_nullMand = outdf100.loc[[False | (outdf100[varName].isnull()) for varName in requiredCols]]
#if(len(outdf100_nullMand.index) > 0):
#    outdf100_nullMand.to_csv('sites_mandatoryFieldMissing.csv')  # index=False,
#ToDO: purge these cells if there is any missing? #For now left to be inspected

print("Writing out...")
#write out
outdf100.to_csv(siteCSV, index=False)

print("Done sites")