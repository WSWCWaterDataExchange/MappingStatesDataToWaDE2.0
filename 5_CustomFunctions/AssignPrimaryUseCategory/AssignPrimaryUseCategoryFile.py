# Last Update: 08/01/2022
# Dependents: AllocationsAmounts_fact.py
# Purpose: To assign a single value to the PrimaryUseCategory field for water rights.
# Notes 1) The BUtoWBUDict dictionary for converting Native Beneficial Use -> WaDE Beneficial Use will have to be updated everytime there is a native new benefical use added to the QA.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Dictionaries
############################################################################
# Native Beneficial Use -to- WaDE Beneficial Use Dictionary
# read in input file, create temp dataframe, make adjustments, convert to dictionary.
fileInput = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/AssignPrimaryUseCategory/PrimaryBenUseInput.xlsx"
df_pbu = pd.read_excel(fileInput).replace(np.nan, "")
df_pbu['Name'] = df_pbu['Name'].str.lower().str.strip()
BUtoWBUDict = pd.Series(df_pbu.WaDEname.values, index=df_pbu.Name.astype(str)).to_dict()


# WaDE Convert Multi-Beneficial Use to Single Primary Use Dictionary
# This has been pre-built looking for unique items of only length == 2 (last updated: 05/10/2022).
WaDEBenUseDict = {
"Agriculture Irrigation,Aquaculture" : "Agriculture Irrigation",
"Agriculture Irrigation,Commercial/Industrial" : "Agriculture Irrigation",
"Agriculture Irrigation,Domestic" : "Agriculture Irrigation",
"Agriculture Irrigation,Livestock" : "Agriculture Irrigation",
"Agriculture Irrigation,Other" : "Agriculture Irrigation",
"Agriculture Irrigation,Public Supply" : "Agriculture Irrigation",
"Agriculture Irrigation,Recreation" : "Agriculture Irrigation",
"Agriculture Irrigation,Unspecified" : "Agriculture Irrigation",
"Aquaculture,Recreation" : "Recreation",
"Commercial/Industrial,Domestic" : "Commercial/Industrial",
"Commercial/Industrial,Livestock" : "Commercial/Industrial",
"Domestic,Fire" : "Domestic",
"Domestic,Livestock" : "Livestock",
"Domestic,Municipal Irrigation" : "Municipal Irrigation",
"Domestic,Other" : "Domestic",
"Domestic,Public Supply" : "Public Supply",
"Domestic,Unspecified" : "Domestic",
"Fire,Livestock" : "Livestock",
"In-stream Flow,Unspecified" : "In-stream Flow",
"Livestock,Municipal Irrigation" : "Municipal Irrigation",
"Livestock,Other" : "Livestock",
"Livestock,Unspecified" : "Livestock",
"Public Supply,Unspecified" : "Public Supply",
"Reservoir Storage,Unspecified" : "Reservoir Storage"}



# Function
############################################################################
def retrievePrimaryUseCategory(val):
    # Clean val & create list.
    valList = val.split(",")
    valList = sorted(list(map(lambda x: str(x).strip().lower(), valList)))

    # Temp converting native ben use to WaDE terminology ben use
    wbuList = sorted(list(map(lambda x: BUtoWBUDict[x], valList)))

    # Assign PrimaryUse
    # if len == 2, use dictionary
    # if not, return first item in list as string
    if len(wbuList) == 2:
        try:
            outString = WaDEBenUseDict[",".join(str(x) for x in wbuList)]
        except:
            outString = wbuList[0]
            outString = str(outString).strip()
    else:
        outString = wbuList[0]
        outString = str(outString).strip()

    return outString