# Date Created: 02/11/2022
# Author: Ryan James (WSWC)
# Purpose: To create CA agg variable use information and populate a dataframe for WaDE_QA 2.0.
# Notes: 1) No input csv to read, all values are more easily hardcoded into a list here and then exported to CSV.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/California/AggregatedAmounts"
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

outdf.VariableSpecificUUID = ["CAag_V1", "CAag_V2", "CAag_V3", "CAag_V4",
                              "CAag_V5", "CAag_V6", "CAag_V7", "CAag_V8",
                              "CAag_V9", "CAag_V10", "CAag_V11", "CAag_V12"]

outdf.AggregationInterval = ["1",
"1",
"1",
"1",
"1",
"1",
"1",
"1",
"1",
"1",
"1",
"1"]

outdf.AggregationIntervalUnitCV = ["Annual",
"Annual",
"Annual",
"Annual",
"Annual",
"Annual",
"Annual",
"Annual",
"Annual",
"Annual",
"Annual",
"Annual"]

outdf.AggregationStatisticCV = ["Cumulative",
"Cumulative",
"Cumulative",
"Cumulative",
"Cumulative",
"Cumulative",
"Cumulative",
"Cumulative",
"Cumulative",
"Cumulative",
"Cumulative",
"Cumulative"]

outdf.AmountUnitCV = ["AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY"]

outdf.MaximumAmountUnitCV = ["AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY",
"AFY"]

outdf.ReportYearStartMonth = ["1",
"1",
"1",
"1",
"1",
"1",
"1",
"1",
"1",
"1",
"1",
"1"]

outdf.ReportYearTypeCV = ["CalendarYear",
"CalendarYear",
"CalendarYear",
"CalendarYear",
"CalendarYear",
"CalendarYear",
"CalendarYear",
"CalendarYear",
"CalendarYear",
"CalendarYear",
"CalendarYear",
"CalendarYear"]

outdf.VariableCV = ["Applied Water Use",
"Applied Water Use",
"Applied Water Use",
"Applied Water Use",
"Applied Water Use",
"Applied Water Use",
"Depletion",
"Depletion",
"Depletion",
"Depletion",
"Depletion",
"Depletion"]

outdf.VariableSpecificCV = ["Applied Water Use_Annual_Agriculture_Surface Ground Water",
                            "Applied Water Use_Annual_Instream Flow Requirements_Surface Ground Water",
                            "Applied Water Use_Annual_Managed Wetlands_Surface Ground Water",
                            "Applied Water Use_Annual_Required Delta Outflow_Surface Ground Water",
                            "Applied Water Use_Annual_Urban_Surface Ground Water",
                            "Applied Water Use_Annual_Wild and Scenic River_Surface Ground Water",
                            "Depletion_Annual_Agriculture_Surface Ground Water",
                            "Depletion_Annual_Instream Flow Requirements_Surface Ground Water",
                            "Depletion_Annual_Managed Wetlands_Surface Ground Water",
                            "Depletion_Annual_Required Delta Outflow_Surface Ground Water",
                            "Depletion_Annual_Urban_Surface Ground Water",
                            "Depletion_Annual_Wild and Scenic River_Surface Ground Water"]


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
