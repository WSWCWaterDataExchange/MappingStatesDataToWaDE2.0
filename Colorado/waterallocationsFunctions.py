#!/usr/bin/env python
import pandas as pd
import numpy as np
import beneficialUseDictionary

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