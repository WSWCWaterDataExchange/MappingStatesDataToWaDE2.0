# Date Update: 02/01/2024
# Purpose: To assign RegulatoryOverlayUUIDs values to state water right sites.csv file.
# Notes:
#   N/A


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
def JoinOverlayToSiteFunction(workingDirString):
    workingDir = workingDirString
    os.chdir(workingDir)

    # Check for Regulatory data
    ############################################################################
    print("Checking for available Overlays data / project...")
    checkDir = os.path.isdir('../Overlays/ProcessedInputData')
    if checkDir == True:
        print("- Overlays directory exists")

        # Inputs
        ############################################################################
        print("Reading input csv(s)...")
        # Water right Input Data
        dfws = pd.read_csv('ProcessedInputData/watersources.csv')
        dfs = pd.read_csv('ProcessedInputData/sites.csv')
        # Regulatory Input Data
        dfro = pd.read_csv("../Overlays/ProcessedInputData/regulatoryoverlays.csv")
        dfru = pd.read_csv("../Overlays/ProcessedInputData/reportingunits.csv")
        dfrru = pd.read_csv("../Overlays/ProcessedInputData/regulatoryreportingunits.csv")

        #### water right watersource info with site info
        # explode site.csv on WaterSourceUUIDs
        dfs = dfs.assign(WaterSourceUUIDs=dfs['WaterSourceUUIDs'].str.split(',')).explode('WaterSourceUUIDs').reset_index(drop=True)
        # merge watersources to dfs via WaterSourceUUIDs -to -WaterSourceUUID
        dfs = pd.merge(dfs, dfws[['WaterSourceUUID', 'WaterSourceTypeCV']],
                       left_on='WaterSourceUUIDs', right_on='WaterSourceUUID', how='left')

        #### Overlay watersource info with reporting unit info
        # merge regulatoryoverlays -to- regulatoryreportingunits -to- reportingunits
        dfro = pd.merge(dfro[['RegulatoryOverlayUUID', 'WaterSourceTypeCV']],
                        dfrru[['RegulatoryOverlayUUID', 'ReportingUnitUUID']],
                        left_on='RegulatoryOverlayUUID', right_on='RegulatoryOverlayUUID', how='left')
        dfru = pd.merge(dfru, dfro, left_on='ReportingUnitUUID', right_on='ReportingUnitUUID', how='left')
        ruRUTList = dfru['ReportingUnitTypeCV'].unique().tolist()
        print(f'- Reporting Unit Type(s) in ru: {ruRUTList}')

        for x in ruRUTList:
            print(f'For Reporting Unit Type = "{x}"...')
            dfru1 = dfru.copy()
            dfru1 = dfru1[dfru1['ReportingUnitTypeCV'] == x]
            ruWSTList = dfru1['WaterSourceTypeCV'].unique().tolist()
            print(f'- Water Source Type(s) for {x}: {ruWSTList}...')

            # Convert dataframe -to- geodataframe
            dfru1 = dfru1[dfru1['Geometry'] != ""].reset_index(drop=True)
            dfru1['Geometry'] = gpd.GeoSeries.from_wkt(dfru1['Geometry'], crs="EPSG:4326")
            gdfru1 = gpd.GeoDataFrame(dfru1, geometry=dfru1['Geometry'], crs="EPSG:4326")

            # Create copy of sites-wst dataframe
            # Extract out WaterSourceTypeCV and match to that of above reportingunits dataframe
            for y in ruWSTList:
                try:
                    print(f'-- Extracting Water Source Type "{y}" from sites.csv')
                    dfs1 = dfs.copy()
                    dfs1 = dfs1[dfs1['PODorPOUSite'] == 'POD']
                    dfs1 = dfs1[dfs1['WaterSourceTypeCV'] != y]

                    # convert copy sites dataframe -to- geodataframe
                    gdfs1 = gpd.GeoDataFrame(dfs1, geometry=gpd.points_from_xy(dfs1.Longitude.astype(float), dfs1.Latitude.astype(float)), crs="EPSG:4326")

                    # Select copy geodataframe sites within geodataframe reporting unit polygons.
                    print(f'-- Selecting sites within reporting unit polygon')
                    gdfs1_ru1 = gpd.sjoin(left_df=gdfs1, right_df=gdfru1[['ReportingUnitUUID', 'RegulatoryOverlayUUID', 'geometry']], op='within').replace(np.nan, "")

                    # set RegulatoryOverlayUUIDs in copy geodataframe sites
                    # drop geodataframe and WST elements from copy geodataframe sites
                    print(f'-- Setting RegulatoryOverlayUUIDs in sites.csv.')
                    gdfs1_ru1['RegulatoryOverlayUUIDs'] = gdfs1_ru1['RegulatoryOverlayUUID']
                    gdfs1_ru1 = gdfs1_ru1.drop(['RegulatoryOverlayUUID', 'geometry', 'index_right', 'ReportingUnitUUID', 'WaterSourceUUID', 'WaterSourceTypeCV'], axis=1)

                    # Concatenate existing sites and copy geodataframe sites into single output
                    print(f'-- Concatenate updated sites.csv to existing file')
                    dfs = pd.concat([dfs, gdfs1_ru1])
                    dfs = dfs.drop_duplicates().reset_index(drop=True).replace(np.nan, "")
                    dfs = dfs.drop(['WaterSourceUUID', 'WaterSourceTypeCV'], axis=1)
                    dfs = dfs.groupby('SiteUUID').agg(lambda x: ','.join([str(elem) for elem in (list(set(x))) if elem != ""])).replace(np.nan, "").reset_index()

                except:
                    print(f'-- WARNING: No matching Water Source Type(s) in sites.csv')

        # Export out to CSV.
        dfs.to_csv('ProcessedInputData/sites.csv', index=False)  # this is in the Regulatory data folder

    else:
        print("- WARNING: No Overlays data / project to work from")

    print("Done")