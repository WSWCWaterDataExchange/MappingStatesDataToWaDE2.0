import numpy as np
import pandas as pd
import os
from pyproj import CRS, Transformer
import beneficialUseDictionary
from waterallocationsFunctions import *

# working directory
working_dir = "C:/tseg/jupyterWaDE"
os.chdir(working_dir)

### Read Utah input csv file
#(file must be already downloaded and stored in the working directory)

# input csv
input_csv = 'WRCHEX_WATER_MASTER.csv'
input_div = "WRCHEX_POINTS_OF_DIVERSION.csv"

# output file
output_sit = "sites.csv"

#column names
columns=['WaDESiteUUID', 'SiteNativeID', 'SiteName', 'USGSSiteID', 'SiteTypeCV', 'Longitude_x', 'Latitude_y',
          'SitePoint', 'SiteNativeURL', 'Geometry', 'CoordinateMethodCV', 'CoordinateAccuracy', 'GNISCodeCV',
          'EPSGCodeCV', 'NHDNetworkStatusCV', 'NHDProductCV', 'NHDUpdateDate', 'NHDReachCode', 'NHDMeasureNumber',
          'StateCV']

# These are not used currently. Data types inferred from the inputs
dtypesx = ['NVarChar(55)	NVarChar(50)	NVarChar(500)	NVarChar(250)	NVarChar(100)	Double	Double	Geometry',
           'NVarChar(250)	Geometry	NVarChar(100)	NVarChar(255)	NVarChar(50)	NVarChar(50)	NVarChar(50)',
           'NVarChar(50)	Date	NVarChar(50)	NVarChar(50)	NChar(5)']

# create target dataframe

#assumes dtypes inferred from CO file
outdf100=pd.DataFrame(columns=columns)

####### Read Inputs and merge tables
# We are joining 'on-left': keep all rows of first table (check if need to be refined)

"""
From design doc:
Add the site table (join the water right record into the point of diversions table based on the matching 
water right identifier.
Get the first diversion info (long, lat, site type) in case many exist.   
"""
# for now we just use the point of diversion table

print("Reading inputs...")
# water_master
input_columns = ['recordId', 'WRCHEX', 'POD_TYPE', 'X_UTM', 'Y_UTM']
dType_dict = {'recordId': np.int32, 'WRCHEX':str, 'POD_TYPE':str, 'X_UTM':np.float64, 'Y_UTM': np.float64}
df100 = pd.read_csv(input_div,encoding = "ISO-8859-1", usecols = input_columns) #, dtype=dType_dict) #, or alternatively encoding = "utf-8"
#df100
#print(len(df100_l.index))
df100.drop_duplicates(inplace=True)
#print (len(df100_l.index))

#df100 = df100.head(1000) #only runs first 10000 lines for testing.
#df100

df100 = df100.replace(np.nan, '')
#df100

# UT SiteTypeCV mapping

# Get SiteTypeCV based on the field "POD_TYPE" and map Blank to “unknown”

df100 = df100.assign(SiteTypeCV='')  #add new column and make it empty

# no-loop approach?
df100['SiteTypeCV'] = df100.apply(lambda row: assignSiteTypeCV(row['POD_TYPE']), axis=1)
#df100

print("Project to longitude/ latitude ")
# use pyproj to project to lat lon
crs_to = CRS('EPSG:4326')  # CRS("WGS84")
crs_from = CRS("EPSG:26912")
transformer = Transformer.from_crs(crs_from, crs_to)

df100 = df100.assign(Longitude_x='')
df100 = df100.assign(Latitude_y='')
# drop cells with no x or y coordinate
dropIndex = df100.loc[(df100['X_UTM'].isnull()) | (df100['X_UTM'] == '') |
                      (df100['Y_UTM'].isnull()) | (df100['Y_UTM'] == '')].index
if len(dropIndex) > 0:
    df100 = df100.drop(dropIndex)
    df100 = df100.reset_index(drop=True)

lonX = []
latY = []
print("total rows, ", len(df100.index))
for ix in range(len(df100.index)):
    print(ix)
    x1 = df100.loc[ix, 'X_UTM']
    y1 = df100.loc[ix, 'Y_UTM']
    try:
        lon, lat = transformer.transform(float(x1), float(y1))
        lonX.append(lon)
        latY.append(lat)
    except:
        lonX.append(np.nan)
        latY.append(np.nan)

df100['Longitude_x'] = lonX
df100['Latitude_y'] = latY

print("Copying all columns...")
#
# Utah directly mapped cells
destCols=['SiteNativeID', 'SiteTypeCV', 'Longitude_x', 'Latitude_y']
srsCols=['WRCHEX', 'SiteTypeCV', 'Longitude_x', 'Latitude_y']

outdf100[destCols] = df100[srsCols]

# replace NaN with blank cells
outdf100 = outdf100.replace(np.nan, '')

print("Dropping duplicates...")

#filter the whole table based on a unique combination of site ID, SiteName, SiteType
outdf100 = outdf100.drop_duplicates(subset=['SiteNativeID', 'SiteName', 'SiteTypeCV'])   #
outdf100 = outdf100.reset_index(drop=True)

print("Dropping empty lat/lon")

#drop the sites with no long and lat.
outdf100purge = outdf100.loc[(outdf100['Longitude_x'].isnull()) | (outdf100['Longitude_x'] == '') |
                             (outdf100['Latitude_y'].isnull()) | (outdf100['Latitude_y'] == '')]
if len(outdf100purge.index) > 0:
    outdf100purge.to_csv('sites_missing.csv')    #index=False,
    dropIndex = outdf100.loc[(outdf100['Longitude_x'].isnull()) | (outdf100['Longitude_x'] == '') |
                             (outdf100['Latitude_y'].isnull()) | (outdf100['Latitude_y'] == '')].index
    outdf100 = outdf100.drop(dropIndex)
    outdf100 = outdf100.reset_index(drop=True)

# hardcoded columns
#
outdf100.EPSGCodeCV = 'EPSG:4326'

print("Adding WaDESiteUUID...")
#append 'UT''
df100 = df100.assign(WaDESiteUUID='')  #add new empty column

# no-loop approach?
outdf100['WaDESiteUUID'] = outdf100.apply(lambda row: ('' if (str(row['SiteNativeID']) == '') else
                                                       ("_".join(["UT", str(row['SiteNativeID'])]))) , axis=1)

#df100

print("Checking required isnot null...")

# check if any cell of these columns is null
requiredCols = ['WaDESiteUUID', 'SiteName', 'CoordinateMethodCV', 'GNISCodeCV', 'EPSGCodeCV']

# replace NaN with blank cells
outdf100 = outdf100.replace(np.nan, '')

outdf100_nullMand = outdf100.loc[(outdf100["WaDESiteUUID"] == '') |
                                 (outdf100["SiteName"] == '') | (outdf100["CoordinateMethodCV"] == '') |
                                 (outdf100["GNISCodeCV"] == '') | (outdf100["EPSGCodeCV"] == '')]

if (len(outdf100_nullMand.index) > 0):
    outdf100_nullMand.to_csv('sites_mandatoryFieldMissing.csv')  # index=False,

# ToDO: purge these cells if there is any missing? #For now left to be inspected and reported

print("Writing out...")

#write out
outdf100.to_csv(output_sit, index=False, encoding = "utf-8")

print("Done sites")