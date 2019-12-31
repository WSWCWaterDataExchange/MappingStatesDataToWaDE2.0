#Date Created: 12/06/2019
#Purpose: To extract CO site infromation and population dataframe for WaDE 2.0.
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
columns=['SiteUUID', 'SiteNativeID', 'SiteName', 'SiteTypeCV', 'Longitude', 'Latitude', 'EPSGCodeCV', 'Geometry', 'SiteNativeURL',
         'StateCV', 'CoordinateMethodCV', 'CoordinateAccuracy', 'GNISCodeCV', 'NHDNetworkStatusCV', 'NHDProductCV', 'NHDUpdateDate',
         'NHDReachCode', 'NHDMeasureNumber']

#ry_comment: @dtypesx, list is not being used.
dtypesx = ['NVarChar(55)	NVarChar(50)	NVarChar(500)	NVarChar(250)	NVarChar(100)	Double	Double	Geometry',
           'NVarChar(250)	Geometry	NVarChar(100)	NVarChar(255)	NVarChar(50)	NVarChar(50)	NVarChar(50)',
           'NVarChar(50)	Date	NVarChar(50)	NVarChar(50)	NChar(5)']



# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf=pd.DataFrame(columns=columns)

print("SiteNativeID")
outdf['SiteNativeID'] = df['WaterRightNumber']

print("SiteName")
outdf['SiteName'] = df['Source']

print("Longitude")
outdf['Longitude'] = df['X']

print("Latitude")
outdf['Latitude'] = df['Y']

print("SiteNativeURL")
outdf['SiteNativeURL'] = df['WRMap']

print("CoordinateMethodCV")
outdf['CoordinateMethodCV'] = df['DataSource']

print("SiteTypeCV") # Hardcoded
outdf.loc[outdf['SiteTypeCV'].isnull(),'SiteTypeCV'] = 'Fill in at later date'

print("Geometry") # Hardcoded
outdf.loc[outdf['Geometry'].isnull(),'Geometry'] = 'Unknown'

print("EPSGCodeCV") # Hardcoded
outdf.EPSGCodeCV = 'EPSG:4326'

print("ID") # Hardcoded  #ry_comment: @ID, what is this one?
outdf.ID = 'EPSG:ID'

print("CoordinateAccuracy") # Hardcoded
outdf.loc[outdf['CoordinateAccuracy'].isnull(),'CoordinateAccuracy'] ='Unknown'

print("GNISCodeCV") # Hardcoded
outdf.GNISCodeCV = np.nan

print("NHDNetworkStatusCV") # Hardcoded
outdf.NHDNetworkStatusCV = np.nan

print("NHDProductCV") # Hardcoded
outdf.NHDProductCV = np.nan

print("NHDUpdateDate") # Hardcoded
outdf.NHDUpdateDate = np.nan

print("NHDReachCode") # Hardcoded
outdf.NHDReachCode = np.nan

print("NHDMeasureNumber") # Hardcoded
outdf.NHDMeasureNumber = np.nan

print("SiteUUID")
# has to be one of the last, need SiteNativeID to create
for ix in range(len(outdf.index)):
    outdf.loc[ix, 'SiteUUID'] = "_".join(["IDWR",str(outdf.loc[ix, 'SiteNativeID'])])


# Dropping duplicate
#filter the whole table based on a unique combination of site ID, SiteName, SiteType
outdf = outdf.drop_duplicates(subset=['SiteNativeID', 'SiteName', 'SiteTypeCV'])
outdf = outdf.reset_index(drop=True)
outdfpurge = outdf.loc[(outdf['Longitude'].isnull()) | (outdf['Latitude'].isnull())]



# Check required fields are not null
############################################################################
print("Checking required is not null...")
#Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
#ry_comment: @requiredCols, this list isn't being used for anything...
requiredCols=['WaDESiteUUID', 'SiteName', 'CoordinateMethodCV', 'EPSGCodeCV']

#replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan)
outdf_nullMand = outdf.loc[(outdf["SiteUUID"].isnull()) |
                                 (outdf["SiteName"].isnull()) | (outdf["CoordinateMethodCV"].isnull()) |
                                 (outdf["EPSGCodeCV"].isnull())]



# Export to new csv
############################################################################
print("Exporting dataframe to csv...")
outdf.to_csv('ProcessedInputData/sites.csv', index=False)


#Report missing values if need be to seperate csv
if len(outdfpurge.index) > 0:
    outdfpurge.to_csv('ProcessedInputData/sites_missing.csv')    #index=False,
    dropIndex = outdf.loc[(outdf['Longitude'].isnull()) | (outdf['Latitude'].isnull())].index
    outdf = outdf.drop(dropIndex)
    outdf = outdf.reset_index(drop=True)

if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/sites_mandatoryFieldMissing.csv')  # index=False,

print("Done.")