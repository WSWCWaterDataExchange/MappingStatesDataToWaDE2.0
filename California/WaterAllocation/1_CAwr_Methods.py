# Date Update: 03/30/2023
# Purpose: To extract CA methods use information and populate dataframe for WaDE_QA 2.0.
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
workingDir = "G:/Shared drives/WaDE Data/California/WaterAllocation"
os.chdir(workingDir)

# WaDE columns
MethodsColumnsList = GetColumnsFile.GetMethodsColumnsFunction()


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=MethodsColumnsList)
outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.MethodUUID = "CAwr_M1"

outdf.ApplicableResourceTypeCV = "Surface Water and Groundwater"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = """A Water Right is a property right that is either conditional or absolute and conveys the right to use a particular amount of water, with a specified priority date as confirmed by the water court. The Net Amounts List contains the current status of a water right based on all of its court decreed actions."""

outdf.MethodName = "California Water Rights Method"

outdf.MethodNEMILink = "https://www.waterboards.ca.gov/waterrights/board_info/faqs.html#toc178761079"

outdf.MethodTypeCV = "Legal Processes"

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

# Report purged values.
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/methods_mandatoryFieldMissing.csv', index=False)

print("Done.")