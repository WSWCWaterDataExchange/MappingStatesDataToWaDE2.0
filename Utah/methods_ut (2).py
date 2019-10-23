#!/usr/bin/env python
import pandas as pd
import numpy as np
import os

workingDir = "C:/tseg/jupyterWaDE/"
os.chdir(workingDir)

"""
This code copies the following table 
https://github.com/WSWCWaterDataExchange/WaDE2.0/blob/master/Design_docs/SampleInputData/Methods_dim.csv
"""
# input csv: make sure to copy "Methods_dim.csv" to working directory
fileInput='Methods_dim.csv'
inpdf = pd.read_csv(fileInput)

#WaDE columns
columns=['MethodUUID', 'MethodName', 'MethodDescription', 'MethodNEMILink', 'ApplicableResourceTypeCV',
         'MethodTypeCV', 'DataCoverageValue', 'DataQualityValueCV',	'DataConfidenceValue']

#assumes dtypes inferred from CO file
# mapping code for Utah
outdf = pd.DataFrame(columns=columns)

outdf[columns] = inpdf[columns]

print("Check required is not null...")
#9.9.19: Adel: check all 'required' (not NA) columns have value (not empty)
requiredCols=['MethodUUID', 'MethodName', 'MethodDescription','ApplicableResourceTypeCV','MethodTypeCV']
#replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan)
#any cell of these columns is null
#outdf_nullMand = outdf.loc[outdf.isnull().any(axis=1)] --for all cols
outdf_nullMand = outdf.loc[(outdf["MethodUUID"].isnull()) | (outdf["MethodName"].isnull()) |
                                (outdf["MethodDescription"].isnull()) | (outdf["ApplicableResourceTypeCV"].isnull()) |
                                (outdf["MethodTypeCV"].isnull())]
#outdf_nullMand = outdf.loc[[False | (outdf[varName].isnull()) for varName in requiredCols]]
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('methods_mandatoryFieldMissing.csv')  # index=False,
#ToDO: purge these cells if there is any missing? #For now left to be inspected

print("Write out...")
#write out
MethodsCSV="methods.csv"
outdf.to_csv(MethodsCSV, index=False)

print("Done methods")