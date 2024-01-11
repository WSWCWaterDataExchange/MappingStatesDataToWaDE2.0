# Last Update: 10/20/2023
# Purpose: To have a single function file to create OwnerClassificationCV field.


# Needed Libraries
############################################################################
import re
import pandas as pd


# Create Dictionary
############################################################################
# read in Notes_OwnerClassification.xlsx, skip first row, save as dataframe
# create dictionary. key = column name, value = data, remove 'nan' values

datadf = pd.read_excel("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/OwnerClassification/Notes_OwnerClassification.xlsx",
                  sheet_name ="TrackWordsByGroup", skiprows=1)

listDictionary = {} # create list dictioarny.

for (columnName, columnData) in datadf.items():
    columnList = columnData.tolist()
    columnList = [x for x in columnList if str(x) != 'nan']
    listDictionary[columnName] = columnList


# Assign OwnerClassification value.
############################################################################
# Uses the re library, but requires for loop.
# Order that the lists are inputed into dictoinary is important, want to overide generic search with a more specific search.

def CreateOwnerClassification(val):
    val = str(val).strip()
    if val == '' or pd.isnull(val):
        outString = "Unspecified" # if value is blank or unknown
    else:
        outString = "Private"  # Default Value

        # Cleaning text / simple search format
        val = re.sub("[$@&.`;',/\)(-]", "", val).strip()
        val = val.lower().strip()
        val = " " + val + " "

        for x in listDictionary:
            valueList = listDictionary[x]
            for words in valueList:
                if re.search(" " + words + " ", val): outString = x

    return outString