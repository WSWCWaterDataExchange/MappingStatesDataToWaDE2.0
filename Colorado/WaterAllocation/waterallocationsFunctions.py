#!/usr/bin/env python
import pandas as pd
import numpy as np
import beneficialUseDictionary

def assignAllocAmountMax(in_decreedUnits, in_netAbsolute, in_netConditional):

    retVal = np.nan
    if ((in_netAbsolute != 0) and (in_netConditional != 0)):
        """
        For a single row, there should be only one value that is not zero in Net Absolute, or Net Conditional.
        If both of them have values that are not zero, then skip loading this row 
        (The data we have for now does not have this case, but just in case)
        """
        # ToDO save these rows for inspection?
        retVal = np.nan
    else:
        if ((in_decreedUnits == "A") and (in_netAbsolute != 0)):
            retVal = in_netAbsolute
        elif ((in_decreedUnits == "A") and (in_netConditional != 0)):
            retVal = in_netConditional
        else:
            ## TODO: check this is the case of units == 'A'
            retVal = np.nan
    return retVal


def assignAllocAmount(in_decreedUnits, in_netAbsolute, in_netConditional):

    retVal = np.nan
    if ((in_netAbsolute != 0) and (in_netConditional != 0)):
        """
        For a single row, there should be only one value that is not zero in Net Absolute, or Net Conditional.
        If both of them have values that are not zero, then skip loading this row 
        (The data we have for now does not have this case, but just in case)
        """
        # ToDO save these rows for inspection?
        retVal = np.nan
    else:
        if ((in_decreedUnits == "C") and (in_netAbsolute != 0)):
            retVal = in_netAbsolute
        elif ((in_decreedUnits == "C") and (in_netConditional != 0)):
            retVal = in_netConditional
        else:
            ## TODO: check this is the case of units == 'A'
            retVal = np.nan
    return retVal


def assignAllocatoinLegalStatusCV(in_netAbsolute, in_netConditional):

    if ((in_netAbsolute == 0) and (in_netConditional == 0)):
        return "Conditional Absolute"
    elif ((in_netAbsolute == 0) and (in_netConditional != 0)):
        return "Conditional"
    elif ((in_netAbsolute != 0) and (in_netConditional == 0)):
        return "Absolute"


def assignBenUseCategory_CO(colrowValue):
    # look up beneficial use
    # may need to modify capitalization in beneficialUseDictionary
    benUseDict = beneficialUseDictionary.beneficialUseDictionary_CO  ##modified key for Utah values
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