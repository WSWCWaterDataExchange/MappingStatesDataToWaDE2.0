#!/usr/bin/env python
import pandas as pd
import numpy as np
from sodapy import Socrata
import os

workingDir="C:/Tseganeh/0WaDE/Data/TestOutputs"
os.chdir(workingDir)

fileInput="DWR_Water_Right_-_Net_Amounts.csv"
allocCSV="waterallocations.csv"

varCSV="variables.csv"

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

print("Columns...")
#WaDE columns
columns=['VariableSpecificUUID', 'VariableSpecificCV', 'VariableCV', 'AggregationStatisticCV', 'AggregationInterval',
         'AggregationIntervalUnitCV', 'ReportYearStartMonth', 'ReportYearTypeCV', 'AmountUnitCV', 'MaximumAmountUnitCV']
dtypesx = ['']
#assumes dtypes inferred from CO file

"""
#9.10.19 add UUID for dim tables
#OrgID and the varspec cv
for ix in range(len(outdf100.index)):
    outdf100.loc[ix, 'VariableSpecificUUID'] = " ".join(["CODWR",str(outdf100.loc[ix, 'VariableSpecificCV'])])
"""
inpVals = ['CODWR Allocation All','Allocation All', 'Allocation', 'Average', '1', 'Day', '11', 'Irrigation', 'CFS', 'AFY']
outdf100 = pd.DataFrame([inpVals], columns=columns)
"""
outdf100=pd.DataFrame(columns=columns)
# #hardcodedZZ
outdf100.VariableSpecificCV = 'Allocation All'
outdf100.VariableCV = 'Allocation'
outdf100.AggregationStatisticCV = 'Average'
outdf100.AggregationInterval = '1'
outdf100.AggregationIntervalUnitCV = 'Day'
outdf100.ReportYearStartMonth = '11'
outdf100.ReportYearTypeCV = 'Irrigation'
outdf100.AmountUnitCV = 'CFS'
outdf100.MaximumAmountUnitCV = 'AFY'
"""

print("Check required is not null...")
#9.9.19: Adel: check all 'required' (not NA) columns have value (not empty)
requiredCols=['VariableSpecificUUID','VariableSpecificCV', 'VariableCV', 'AggregationStatisticCV', 'AggregationInterval',
              'AggregationIntervalUnitCV', 'ReportYearStartMonth', 'ReportYearTypeCV', 'AmountUnitCV']
#replace blank strings by NaN, if there are any
outdf100 = outdf100.replace('', np.nan)
#any cell of these columns is null
#outdf100_nullMand = outdf100.loc[outdf100.isnull().any(axis=1)] --for all cols
outdf100_nullMand = outdf100.loc[(outdf100["VariableSpecificUUID"].isnull()) | (outdf100["VariableSpecificCV"].isnull()) |
                                (outdf100["VariableCV"].isnull()) | (outdf100["AggregationStatisticCV"].isnull()) |
                                (outdf100["AggregationInterval"].isnull()) | (outdf100["AggregationIntervalUnitCV"].isnull()) |
                                (outdf100["ReportYearStartMonth"].isnull()) | (outdf100["ReportYearTypeCV"].isnull()) |
                                (outdf100["AmountUnitCV"].isnull())]
#outdf100_nullMand = outdf100.loc[[False | (outdf100[varName].isnull()) for varName in requiredCols]]
if(len(outdf100_nullMand.index) > 0):
    outdf100_nullMand.to_csv('variables_mandatoryFieldMissing.csv')  # index=False,
#ToDO: purge these cells if there is any missing? #For now left to be inspected

print("Write out...")
# save to output
outdf100.to_csv(varCSV, index=False)

print("Done variables")