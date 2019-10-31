#!/usr/bin/env python
import pandas as pd
import numpy as np
import os

workingDir="C:/Users/gdg12/Desktop/Mapping"
os.chdir(workingDir)

# input csv: make sure to copy "Methods_dim.csv" to working directory
fileInput='Methods_dim.csv'
inpdf = pd.read_csv(fileInput)
###input table for methods is not the Water_Master CSV, but the Methods_dim.csv
#WaDE columns
columns=['MethodUUID', 'MethodName', 'MethodDescription', 'MethodNEMILink', 'ApplicableResourceTypeCV',
         'MethodTypeCV', 'DataCoverageValue', 'DataQualityValueCV',	'DataConfidenceValue']

#assumes dtypes inferred from CO file
# mapping code for Utah
outdf = pd.DataFrame(columns=columns)

outdf[columns] = inpdf[columns] ###copies the columns fron input data frame to output data frame at once-you can specify the columns

print("Check required is not null...")
#9.9.19: Adel: check all 'required' (not NA) columns have value (not empty)
requiredCols=['MethodUUID', 'MethodName', 'MethodDescription','ApplicableResourceTypeCV','MethodTypeCV'] ##can't be empty
#replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan) ##convert every blank space to np.nan
#any cell of these columns is null
#outdf_nullMand = outdf.loc[outdf.isnull().any(axis=1)] --for all cols
outdf_nullMand = outdf.loc[(outdf["MethodUUID"].isnull()) | (outdf["MethodName"].isnull()) |
                                (outdf["MethodDescription"].isnull()) | (outdf["ApplicableResourceTypeCV"].isnull()) |
                                (outdf["MethodTypeCV"].isnull())]

###This above checks to see if any rows have null values
if(len(outdf_nullMand.index) > 0): ##Writes out the rows where there is a null value
    outdf_nullMand.to_csv('methods_mandatoryFieldMissing.csv')  # index=False,
#ToDO: purge these cells if there is any missing? #For now left to be inspected

print("Write out...")
#write out
MethodsCSV="methods.csv"
outdf.to_csv(MethodsCSV, index=False)

print("Done methods")