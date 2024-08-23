# Date Created: 02/09/2022
# Author: Ryan James (WSWC)
# Purpose: To create UT agg variable use information and populate a dataframe for WaDE_QA 2.0.
# Notes: 1) No input csv to read, all values are more easily hardcoded into a list here and then exported to CSV.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir  = "G:/Shared drives/WaDE Data/Utah/AggregatedAmounts"
os.chdir(workingDir)

#WaDE columns
columnslist = [
    "VariableSpecificUUID",
    "AggregationInterval",
    "AggregationIntervalUnitCV",
    "AggregationStatisticCV",
    "AmountUnitCV",
    "MaximumAmountUnitCV",
    "ReportYearStartMonth",
    "ReportYearTypeCV",
    "VariableCV",
    "VariableSpecificCV"]


# Custom Functions
############################################################################

# N/A


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist)

outdf.VariableSpecificUUID = ["UTag_V1", "UTag_V2", "UTag_V3", "UTag_V4", "UTag_V5", "UTag_V6"]

outdf.AggregationInterval = ["1", "1", "1", "1", "1", "1"]

outdf.AggregationIntervalUnitCV = ["Annual", "Annual", "Annual", "Annual", "Annual", "Annual"]

outdf.AggregationStatisticCV = ["Average", "Average", "Average", "Average", "Average", "Average"]

outdf.AmountUnitCV = ["AFY", "AFY", "AFY", "AFY", "AFY", "AFY"]

outdf.MaximumAmountUnitCV = ["AFY", "AFY", "AFY", "AFY", "AFY", "AFY"]

outdf.ReportYearStartMonth = ["10", "10", "10", "10", "10", "10"]

outdf.ReportYearTypeCV = ["WaterYear", "WaterYear", "WaterYear", "WaterYear", "WaterYear", "WaterYear"]

outdf.VariableCV = ["Consumptive Use", "Consumptive Use", "Withdrawal", "Withdrawal", "Withdrawal", "Withdrawal"]

outdf.VariableSpecificCV = ["Consumptive Use_Annual_Agriculture_Surface and Groundwater",
                            "Consumptive Use_Annual_Agriculture_Surface Water",
                            "Withdrawal_Annual_Agriculture_Groundwater",
                            "Withdrawal_Annual_Agriculture_Surface Water",
                            "Withdrawal_Annual_Municipal/Industrial_Groundwater",
                            "Withdrawal_Annual_Municipal/Industrial_Surface Water"]


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
    outdf_nullMand.to_csv('ProcessedInputData/variables_missing.csv', index=False)

print("Done.")
