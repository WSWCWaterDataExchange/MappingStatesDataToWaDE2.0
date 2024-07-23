# Date Update: 06/24/2024
# Purpose: Add missing County, HUC8, HUC12 information for sites.csv file.
# Notes:
#   shp files too large to store on GitHub, will have to use absolute paths on local machine.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd
import geopandas as gpd


# Custom Libraries
############################################################################
# N/A


# File Function
############################################################################
def AddCountyHUC8HUC12Function(workingDirString):
    workingDir = workingDirString
    os.chdir(workingDir)

    # Check for Regulatory data
    ############################################################################
    print("Checking for available shapefiles data / project...")
    try:
        # Inputs
        ############################################################################
        print("Reading input files(s)...")
        # Water right site csv.
        dfs = pd.read_csv('ProcessedInputData/sites.csv')
        # County, HUC8, and HUC12 shapefiles.
        gdfCounty = gpd.read_file("C:/Users/rjame/Documents/WSWC Documents/Generic Shapefiles/cb_2018_us_county.zip")
        gdfHuc8 = gpd.read_file("C:/Users/rjame/Documents/WSWC Documents/Generic Shapefiles/HUC8_US.zip")
        gdfHuc12West = gpd.read_file("C:/Users/rjame/Documents/WSWC Documents/Generic Shapefiles/HUC12_US_WEST.zip")

        # Missing County Data
        ############################################################################
        print("Checking for missing County information....")
        def AddMissingCountyFunc(originalVal, newVal):
            originalVal = str(originalVal).strip()
            if originalVal == "" or originalVal == "WaDE Blank" or originalVal == "nan" or pd.isnull(originalVal):
                outString = newVal
            else:
                outString = originalVal
            return outString

        gdfs = gpd.GeoDataFrame(dfs, geometry=gpd.points_from_xy(dfs.Longitude.astype(float), dfs.Latitude.astype(float)), crs="EPSG:4326")
        gdfs_gdfCounty = gpd.sjoin(left_df=gdfs, right_df=gdfCounty[['COUNTYNAME', 'geometry']], op='within').replace(np.nan, "")
        gdfs_gdfCounty['County'] = gdfs_gdfCounty.apply(lambda row: AddMissingCountyFunc(row['County'], row['COUNTYNAME']), axis=1)
        dfs = gdfs_gdfCounty.drop(['COUNTYNAME', 'geometry', 'index_right'], axis=1)

        # Missing HUC8 Data
        ############################################################################
        print("Checking for missing HUC8 information....")
        def AddMissingHUC8Func(originalVal, newVal):
            originalVal = str(originalVal).strip()
            if originalVal == "" or originalVal == "WaDE Blank" or originalVal == "nan" or pd.isnull(originalVal):
                outString = newVal
            else:
                outString = originalVal
            return outString

        gdfs = gpd.GeoDataFrame(dfs, geometry=gpd.points_from_xy(dfs.Longitude.astype(float), dfs.Latitude.astype(float)), crs="EPSG:4326")
        gdfs_gdfHuc8 = gpd.sjoin(left_df=gdfs, right_df=gdfHuc8[['HUC8NAME', 'geometry']], op='within').replace(np.nan, "")
        gdfs_gdfHuc8['HUC8'] = gdfs_gdfHuc8.apply(lambda row: AddMissingHUC8Func(row['HUC8'], row['HUC8NAME']), axis=1)
        dfs = gdfs_gdfHuc8.drop(['HUC8NAME', 'geometry', 'index_right'], axis=1)

        # Missing HUC12 Data
        ############################################################################
        print("Checking for missing HUC12 information....")
        def AddMissingHUC12Func(originalVal, newVal):
            originalVal = str(originalVal).strip()
            if originalVal == "" or originalVal == "WaDE Blank" or originalVal == "nan" or pd.isnull(originalVal):
                outString = newVal
            else:
                outString = originalVal
            return outString

        gdfs = gpd.GeoDataFrame(dfs, geometry=gpd.points_from_xy(dfs.Longitude.astype(float), dfs.Latitude.astype(float)), crs="EPSG:4326")
        gdfs_gdfHuc12west = gpd.sjoin(left_df=gdfs, right_df=gdfHuc12West[['HUC12NAME', 'geometry']], op='within').replace(np.nan, "")
        gdfs_gdfHuc12west['HUC12'] = gdfs_gdfHuc12west.apply(lambda row: AddMissingHUC12Func(row['HUC12'], row['HUC12NAME']), axis=1)
        dfs = gdfs_gdfHuc12west.drop(['HUC12NAME', 'geometry', 'index_right'], axis=1)

        # Export out to CSV.
        dfs = dfs.drop_duplicates().reset_index(drop=True)
        dfs.to_csv('ProcessedInputData/sites.csv', index=False)  # this is in the Regulatory data folder

    except:
        print("- WARNING: shp not found. Consult WaDE Team for more details on used shp flies.")
        print("- Exiting function with no change made.")

    print("Done")