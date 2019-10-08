#!/usr/bin/env python
import pandas as pd
from sodapy import Socrata
import numpy as np
import os

workingDir="C:/Tseganeh/0WaDE/Data/TestOutputs/"
os.chdir(workingDir)

fileInput="DWR_Water_Right_-_Net_Amounts.csv"
allocCSV="waterallocations.csv"

MethodsCSV="methods.csv"

##from https://dev.socrata.com/foundry/data.colorado.gov/a8zw-bjth
# client = Socrata("data.colorado.gov", None)
## authenticated client (needed for non-public datasets):
# client = Socrata(data.colorado.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")
# top100 = client.get("a8zw-bjth", limit=100)
## Convert to pandas DataFrame
# df = pd.DataFrame.from_records(top100)

##OR read csv
df100 = pd.read_csv(fileInput)
#df100 = df.head(100)

#WaDE columns
columns=['MethodUUID', 'MethodName', 'MethodDescription', 'MethodNEMILink', 'ApplicableResourceTypeCV',
         'MethodTypeCV', 'DataCoverageValue', 'DataQualityValueCV',	'DataConfidenceValue']
dtypesx = ['BigInt	NVarChar(250)	NVarChar(50)	Text	NVarChar(100)	NVarChar(100)	NVarChar(50)',
           'NVarChar(100)	NVarChar(50)	NVarChar(50)']
#assumes dtypes inferred from CO file

"""
#9.10.19 add UUID for dim tables
#OrgID and the method name
for ix in range(len(outdf100.index)):
    outdf100.loc[ix, 'MethodUUID'] = "_".join(["CODWR",str(outdf100.loc[ix, 'MethodName'])])
"""
print("Columns...")
inpVals = ['CODWR_DiversionTracking','DiversionTracking', 'Methodology used for tracking diversions in the state of Colorado',
           np.nan, 'Allocation', 'Water withdrawals', np.nan, np.nan, np.nan]
outdf100 = pd.DataFrame([inpVals], columns=columns)
"""
outdf100=pd.DataFrame(columns=columns)
#existing corresponding fields
outdf100.MethodName = 'DiversionTracking'
outdf100.MethodDescription = 'Methodology used for tracking diversions in the state of Colorado'
#outdf100.MethodNEMILink
outdf100.ApplicableResourceTypeCV = 'Allocation'
outdf100.MethodTypeCV = 'Water withdrawals'
#outdf100.DataCoverageValue
#outdf100.DataQualityValueCV
#outdf100.DataConfidenceValue
"""

print("Check required is not null...")
#9.9.19: Adel: check all 'required' (not NA) columns have value (not empty)
requiredCols=['MethodUUID', 'MethodName', 'MethodDescription','ApplicableResourceTypeCV','MethodTypeCV']
#replace blank strings by NaN, if there are any
outdf100 = outdf100.replace('', np.nan)
#any cell of these columns is null
#outdf100_nullMand = outdf100.loc[outdf100.isnull().any(axis=1)] --for all cols
outdf100_nullMand = outdf100.loc[(outdf100["MethodUUID"].isnull()) | (outdf100["MethodName"].isnull()) |
                                (outdf100["MethodDescription"].isnull()) | (outdf100["ApplicableResourceTypeCV"].isnull()) |
                                (outdf100["MethodTypeCV"].isnull())]
#outdf100_nullMand = outdf100.loc[[False | (outdf100[varName].isnull()) for varName in requiredCols]]
if(len(outdf100_nullMand.index) > 0):
    outdf100_nullMand.to_csv('methods_mandatoryFieldMissing.csv')  # index=False,
#ToDO: purge these cells if there is any missing? #For now left to be inspected

print("Write out...")
#write out
outdf100.to_csv(MethodsCSV, index=False)

print("Done methods")