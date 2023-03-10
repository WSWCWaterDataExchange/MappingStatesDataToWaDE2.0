# Date Update: 03/02/2023
# Purpose: To extract AZ variable information and populate dataframe for WaDE_QA 2.0.
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
workingDir = "G:/Shared drives/WaDE Data/Arizona/WaterAllocation"
os.chdir(workingDir)

# WaDE columns
VariablesColumnsList = GetColumnsFile.GetVariablesColumnsFunction()


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=VariablesColumnsList)

outdf.VariableSpecificUUID = ['AZwr_V1', 'AZwr_V2']

outdf.AggregationInterval = "1"

outdf.AggregationIntervalUnitCV = "Year"

outdf.AggregationStatisticCV = "Average"

outdf.AmountUnitCV = ['CFS', 'AFY']

outdf.MaximumAmountUnitCV = ['CFS', 'AFY']

outdf.ReportYearStartMonth = "11"

outdf.ReportYearTypeCV = "WaterYear"

outdf.VariableCV = "Allocation"

outdf.VariableSpecificCV = "Allocation"


# Check required fields are not null
############################################################################
print("Check required is not null...")
# #Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan) #replace blank strings by NaN, if there are any
outdf_nullMand = outdf.loc[(outdf["VariableSpecificUUID"].isnull()) | (outdf["VariableSpecificUUID"] == '') |
                           (outdf["AggregationInterval"].isnull()) | (outdf["AggregationInterval"] == '') |
                           (outdf["AggregationIntervalUnitCV"].isnull()) | (outdf["AggregationIntervalUnitCV"] == '') |
                           (outdf["AggregationStatisticCV"].isnull()) | (outdf["AggregationStatisticCV"] == '') |
                           (outdf["AmountUnitCV"].isnull()) | (outdf["AmountUnitCV"] == '') |
                           (outdf["MaximumAmountUnitCV"].isnull()) | (outdf["MaximumAmountUnitCV"] == '') |
                           (outdf["ReportYearStartMonth"].isnull()) | (outdf["ReportYearStartMonth"] == '') |
                           (outdf["ReportYearTypeCV"].isnull()) | (outdf["ReportYearTypeCV"] == '') |
                           (outdf["VariableCV"].isnull()) | (outdf["VariableCV"] == '') |
                           (outdf["VariableSpecificCV"].isnull()) | (outdf["VariableSpecificCV"] == '')]


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/variables.csv', index=False)

# Report purged values.
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/variables_mandatoryFieldMissing.csv', index=False)

print("Done.")
