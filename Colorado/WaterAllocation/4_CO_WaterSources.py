#Date Created: 02/28/2020
#Author: Ryan James WSWC
#Purpose: To extract CO water source use information and population dataframe for WaDE_QA 2.0.
#Notes: 1) For 'WaterSourceTypeCV', easier to label everything that is not a surface water first.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading input csv...")
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Colorado/WaterAllocation"
os.chdir(workingDir)
fileInput = "RawinputData/DWR_Water_Right_-_Net_Amounts.csv"
df = pd.read_csv(fileInput)

#WaDE columns
columnslist = [
    "WaterSourceUUID",
    "Geometry",
    "GNISFeatureNameCV",
    "WaterQualityIndicatorCV",
    "WaterSourceName",
    "WaterSourceNativeID",
    "WaterSourceTypeCV"]


# Custom Site Functions
############################################################################

# For creating WaterSourceName
def assignWaterSourceName(colrowValue):
    if colrowValue == '' or pd.isnull(colrowValue):
        outList = "Unknown"
    else:
        outList = colrowValue
    return outList

# For creating WaterSourceTypeCV
UnknownWSCVDict = {
"Ground Water" : "Ground Water",
"Spring" : "groundwater/spring",
"Waste Water" : "Reuse",
"Wasteway" : "Reuse",
"Wastewater" : "Reuse",
"Drain" : "Drain",
"Reservoir" : "reservoir"
}
def assignWaterSourceTypeCV(colrowValue):
    if colrowValue == "" or pd.isnull(colrowValue):
        outList = ""
    else:
        String1 = colrowValue.strip()  # remove whitespace chars
        try:
            outList = UnknownWSCVDict[String1]
        except:
            outList = "Surface Water"
    return outList

# For creating WaDESiteUUID
def assignWaterSourceUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "CODWR_WS_" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(index=df.index, columns=columnslist)  # The output dataframe for CSV.

print("Geometry")  # Hardcoded
outdf.Geometry = ""

print("GNISFeatureNameCV")  # Hardcoded
outdf.Geometry = ""

print("WaterQualityIndicatorCV")  # Hardcoded
outdf.WaterQualityIndicatorCV = "Unspecified"

print("WaterSourceName")
outdf['WaterSourceName'] = df.apply(lambda row: assignWaterSourceName(row['Water Source']), axis=1)

print("WaterSourceNativeID")  # has to be one of the last, need length of created outdf
outdf['WaterSourceNativeID'] = df['GNIS ID']

print("WaterSourceTypeCV")
outdf.WaterSourceTypeCV = "Unknown"

##############################
# Dropping duplicate
print("Dropping duplicates")
outdf = outdf.drop_duplicates(subset=['WaterSourceName']).reset_index(drop=True)
##############################

print("WaterSourceUUID") #native source identifier and the organization univeral id. has to be one of the last, need WaterSourceNativeID to create
df["Count"] = range(1, len(df.index) + 1)
outdf['WaterSourceUUID'] = df.apply(lambda row: assignWaterSourceUUID(row['Count']), axis=1)


# Check required fields are not null
############################################################################
#Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
print("Checking required is not null...")
outdf = outdf.replace('', np.nan)  # Replace blank strings by NaN, if there are any
outdf100_nullMand = outdf.loc[(outdf["WaterSourceUUID"].isnull()) | (outdf["WaterSourceUUID"] == '') |
                              (outdf["WaterSourceTypeCV"].isnull()) | (outdf["WaterSourceTypeCV"] == '') |
                              (outdf["WaterQualityIndicatorCV"].isnull()) | (outdf["WaterQualityIndicatorCV"] == '')]


# Checking Dataframe data types
############################################################################
print(outdf.dtypes)


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")
outdf.to_csv('ProcessedInputData/watersources.csv', index=False)

#Report missing values if need be to seperate csv
if(len(outdf100_nullMand.index) > 0):
    outdf100_nullMand.to_csv('watersources_mandatoryFieldMissing.csv')  # index=False,

print("Done.")
