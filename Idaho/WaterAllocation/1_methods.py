#Date Created: 12/06/2019
#Purpose: To extract ID methods use information and population dataframe for WaDE 2.0.
#Notes:   1) Single row of entires, inpVals, for Methods Table.


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
columns=['MethodUUID', 'MethodName', 'MethodDescription', 'MethodNEMILink', 'MethodDOI', 'ApplicableResourceTypeCV',
         'MethodTypeCV', 'DataCoverageValue', 'DataQualityValueCV', 'DataConfidenceValue']

#ry_comment: @dtypesx, this list isn't being used for anything.
dtypesx = ['BigInt	NVarChar(250)	NVarChar(50)	Text	NVarChar(100)	NVarChar(100)	NVarChar(50)',
           'NVarChar(100)	NVarChar(50)	NVarChar(50)']



# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
inpVals = ['IDWR_DiversionTracking', np.nan, np.nan, np.nan, np.nan,
           np.nan, np.nan, np.nan, np.nan, np.nan]  # Hardcoded
outdf = pd.DataFrame([inpVals], columns=columns)



# Check required fields are not null
############################################################################
print("Check required is not null...")
#Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan)
outdf_nullMand = outdf.loc[(outdf["MethodUUID"].isnull()) | (outdf["MethodName"].isnull()) |
                                (outdf["MethodDescription"].isnull()) | (outdf["ApplicableResourceTypeCV"].isnull()) |
                                (outdf["MethodTypeCV"].isnull())]



# Export to new csv
############################################################################
print("Exporting dataframe to csv...")

outdf.to_csv('ProcessedInputData/methods.csv', index=False)

#Report missing values if need be to seperate csv
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/methods_mandatoryFieldMissing.csv')  # index=False,


print("Done.")