#!/usr/bin/env python
import pandas as pd
import numpy as np
import beneficialUseDictionary
#from pyproj import CRS, Transformer
from decimal import Decimal
from datetime import datetime
from dateutil.parser import parse

def assignBenUseCategory(colrowValue):
    # look up beneficial use
    # may need to modify capitalization in beneficialUseDictionary
    benUseDict = beneficialUseDictionary.beneficialUseDictionary  ##modified key for Utah values
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        benUseListStr = colrowValue.strip()  # remove whitespace chars
        outList = ",".join(benUseDict[inx] for inx in list(str(benUseListStr)))

    return outList

def assignWaterSourceID(colrowValue, df400):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        ml = df400.loc[df400['WaterSourceName'] == colrowValue, 'WaterSourceUUID']
        #ml = df400.loc[df400['WaterSourceName'] == df100.loc[ix,"WREX_SOURCE"], 'WaterSourceUUID']
        #print(ml)
        #print(ml.empty)
        if not(ml.empty):            # check if the series is empty
            outList = ml.iloc[0]   # watersourceSer.append(ml.iloc[0])
        else:
            outList = ''
    return outList

def assignSiteID(colrowValue, df500):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        sitl = df500.loc[df500['SiteNativeID'] == colrowValue, 'SiteUUID']
        #print(sitl)
        #print(sitl.empty)
        if not(sitl.empty):            # check if the series is empty
            outList = ','.join(str(inx) for inx in sitl) #sil.iloc[0]
        else:
            outList = ''
    return outList

# find no-loop approach
def assignallocTypeCV(colrowValue):
    # look up allocation dictionary
    # may need to modify capitalization in beneficialUseDictionary
    AllocationTypeCVDict = beneficialUseDictionary.AllocationTypeCVDictionary  ##modified key for Utah values
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        benUseListStr = colrowValue.strip()  # remove whitespace chars
        try:
            outList = AllocationTypeCVDict[benUseListStr]
        except:
            outList = ''

    return outList

def assignownerName(colrowValue1, colrowValue2):
    if colrowValue1 == '' or pd.isnull(colrowValue1):
        outList1 = ''
    else:
        outList1 = colrowValue1.strip()  # remove whitespace chars
    if colrowValue2 == '' or pd.isnull(colrowValue2):
        outList2 = ''
    else:
        outList2 = colrowValue2.strip()  # remove whitespace chars

    if outList1 == '' and outList2 == '':
        outList = ''
    elif outList1 == '':
        outList = outList2
    elif outList2 == '':
        outList = outList1
    else:
        outList = ",".join(map(str, [colrowValue1, colrowValue2]))
    return outList

def assignallocLegalStatausCV(colrowValue):
    AllocationUseDict = beneficialUseDictionary.AllocationLegalStatusDictionary
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        benUseListStr = colrowValue.strip()  # remove whitespace chars
        try:
            outList = AllocationUseDict[benUseListStr]
        except:
            outList = ''

    return outList

# Get SiteTypeCV based on the field "POD_TYPE" and map Blank to “unknown”
def assignSiteTypeCV(colrowValue):
    # look up allocation dictionary
    # may need to modify capitalization in beneficialUseDictionary
    SiteTypeCVDict = beneficialUseDictionary.siteTypedict  ##modified key for Utah values
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = ''
    else:
        benUseListStr = colrowValue.strip()  # remove whitespace chars
        try:
            outList = SiteTypeCVDict[benUseListStr]
        except:
            outList = ''

    return outList

def strLiteralToDateString(inString):
    #print(inString)
    try:
        if inString == '' or pd.isnull(inString):
            valndf = ''
        else:
            inStringStr = str(int(inString))
            #print(inStringStr)
            xvs = inStringStr.strip()  # remove whitespace chars`
            #print(xvs)
            if len(xvs) == 8:
                xvstr = xvs
                yrstr = xvstr[0:4]
                mstr = xvstr[4:6]
                dstr = xvstr[6:8]
                valn = mstr + '/' + dstr + '/' + yrstr
                valD = datetime.strptime(valn, '%m/%d/%Y')
                # print(valD)
                valnDd = valD.date()
                # print(valnDd)
                valndf = valnDd.strftime('%m/%d/%Y')
                #print('date:', valndf)
            elif len(xvs) == 4:
                xvstr = xvs + '0101'
                yrstr = xvstr[0:4]
                mstr = xvstr[4:6]
                dstr = xvstr[6:8]
                valn = mstr + '/' + dstr + '/' + yrstr
                valD = datetime.strptime(valn, '%m/%d/%Y')
                # print(valD)
                valnDd = valD.date()
                # print(valnDd)
                valndf = valnDd.strftime('%m/%d/%Y')
                # print('date:', valndf)
            else:
                valndf = ''
            #print(valn)
    except:
        valndf = ''

    return valndf

"""
    try:
        valD = datetime.strptime(valn, '%m/%d/%Y')
        #print(valD)
        valnDd = valD.date()
        #print(valnDd)
        valndf = valnDd.strftime('%m/%d/%Y')
        print('date:', valndf)
        return valndf
    except:
        return valn
"""

# Project the x and y (UTM NAD 83) coordinates to WGS84 lat lon
def assignLatLon(x1, y1):

    # use pyproj to project to lat lon
    crs_to = CRS('EPSG:4326')  # CRS("WGS84")
    crs_from = CRS("EPSG:26912")
    transformer = Transformer.from_crs(crs_from, crs_to)
    """
    if x1 == '' or pd.isnull(x1) or y1 == '' or pd.isnull(y1):
        lon = ''
        lat = ''
    else:
    """
    try:
        lon, lat = transformer.transform(x1, y1)
    except:
        lon = np.nan
        lat = np.nan

    return lon, lat

# Project the x and y (UTM NAD 83) coordinates to WGS84 lat lon
def assignLon(x1, y1):

    # use pyproj to project to lat lon
    crs_to = CRS('EPSG:4326')  # CRS("WGS84")
    crs_from = CRS("EPSG:26912")
    transformer = Transformer.from_crs(crs_from, crs_to)
    """
    if x1 == '' or pd.isnull(x1) or y1 == '' or pd.isnull(y1):
        lon = np.nan
    else:
    """
    try:
        lon, lat = transformer.transform(float(x1), float(y1))
    except:
        lon = np.nan

    return lon

# Project the x and y (UTM NAD 83) coordinates to WGS84 lat lon
def assignLat(x1, y1):

    # use pyproj to project to lat lon
    crs_to = CRS('EPSG:4326')  # CRS("WGS84")
    crs_from = CRS("EPSG:26912")
    transformer = Transformer.from_crs(crs_from, crs_to)
    """
    if x1 == '' or pd.isnull(x1) or y1 == '' or pd.isnull(y1):
        lat = np.nan
    else:
    """
    try:
        lon, lat = transformer.transform(float(x1), float(y1))
    except:
        lat = np.nan

    return lat