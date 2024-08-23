# Date Created: 05/02/2022
# Author: Ryan James (WSWC)
# Purpose: To create NE ag variable use information and populate a dataframe for WaDE_QA 2.0.
# Notes: 1) No input csv to read, all values are more easily hardcoded into a list here and then exported to CSV.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Nebraska/AggregatedAmounts"
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
# outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.VariableSpecificUUID = ["NEag_V1",
                              "NEag_V2",
                              "NEag_V3",
                              "NEag_V4",
                              "NEag_V5",
                              "NEag_V6",
                              "NEag_V7"]

outdf.VariableCV = ["Depletion",
                    "Depletion",
                    "Consumptive Use",
                    "Consumptive Use",
                    "Consumptive Use",
                    "Consumptive Use",
                    "Demand"]

outdf.VariableSpecificCV = ["Depletion_Annual_Total_Surface Water",
                            "Depletion_Annual_Total_Groundwater",
                            "Consumptive Use_Annual_Total_Groundwater",
                            "Consumptive Use_Annual_Irrigation_Groundwater",
                            "Consumptive Use_Annual_Municipal_Groundwater",
                            "Consumptive Use_Annual_Industrial_Groundwater",
                            "Demand_Annual_Total_Surface Water"]

outdf.AggregationInterval = "1"

outdf.AggregationIntervalUnitCV = "Annual"

outdf.AggregationStatisticCV = "Cumulative"

outdf.AmountUnitCV = "AFY"

outdf.MaximumAmountUnitCV = "AFY"

outdf.ReportYearStartMonth = "10"

outdf.ReportYearTypeCV = "CalendarYear"


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
