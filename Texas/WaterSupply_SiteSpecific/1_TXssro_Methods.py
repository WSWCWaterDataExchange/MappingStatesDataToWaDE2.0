# Date Update: 03/17/2023
# Purpose: To create TX site specific reservoir and observation site methods use information and population dataframe for WaDE_QA 2.0.
# Notes: N/A


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Custom Libraries
############################################################################
import sys
# columns
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/MappingFunctions")
import GetColumnsFile

# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Texas/SS_ReservoirsObservationSites"
os.chdir(workingDir)

# WaDE columns
MethodsColumnsList = GetColumnsFile.GetMethodsColumnsFunction()


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=MethodsColumnsList)
outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.MethodUUID = "TXssro_M1"

outdf.ApplicableResourceTypeCV = "Surface Water"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = "The reservoir data contained in this file are best estimates generated by the Texas Water Development Board (TWDB) using data collected by various data providers as well as by TWDB. For a detailed explanation of the methodology used please visit: http://waterdatafortexas.org/reservoirs/methodology. TWDB makes no warranties (including no warranties as to merchantability or fitness) either expressed or implied with respect to the data or its fitness for any specific application."

outdf.MethodName = "Reservoir Data"

outdf.MethodNEMILink = "https://www.waterdatafortexas.org/reservoirs/download"

outdf.MethodTypeCV = "Measured"


# Check required fields are not null
############################################################################
print("Check required is not null...")
#Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan)
outdf_nullMand = outdf.loc[(outdf["MethodUUID"].isnull()) | (outdf["MethodUUID"] == '') |
                           (outdf["MethodName"].isnull()) | (outdf["MethodName"] == '') |
                           (outdf["MethodDescription"].isnull()) | (outdf["MethodDescription"] == '') |
                           (outdf["ApplicableResourceTypeCV"].isnull()) | (outdf["ApplicableResourceTypeCV"] == '') |
                           (outdf["MethodTypeCV"].isnull()) | (outdf["MethodTypeCV"] == '')]


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/methods.csv', index=False)

#Report missing values if need be to separate csv
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/methods_missing.csv', index=False)

print("Done.")