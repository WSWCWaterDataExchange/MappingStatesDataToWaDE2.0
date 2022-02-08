# Date Created: 02/07/2022
# Purpose: To create AZ agg variable use information and populate a dataframe for WaDE_QA 2.0.
# Notes: 1) No input csv to read, all values are more easily hardcoded into a list here and then exported to CSV.
#        2) Special case of VariableCV and VariableSpecificCV.
#        3) Using a temp df to count out number for rows for outbound df for VariableSpecificUUID.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Arizona/AggregatedAmounts"
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


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist)
# outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.VariableSpecificUUID = ["AZag_V1", "AZag_V2", "AZag_V3", "AZag_V4", "AZag_V5", "AZag_V6", "AZag_V7", "AZag_V8", "AZag_V9", "AZag_V10",
                              "AZag_V11", "AZag_V12", "AZag_V13", "AZag_V14", "AZag_V15", "AZag_V16", "AZag_V17", "AZag_V18", "AZag_V19", "AZag_V20"]

outdf.AggregationInterval = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1",
                             "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]

outdf.AggregationIntervalUnitCV = ["Annual", "Annual", "Annual", "Annual", "Annual", "Annual", "Annual", "Annual", "Annual", "Annual",
                                   "Annual", "Annual", "Annual", "Annual", "Annual", "Annual", "Annual", "Annual", "Annual", "Annual"]

outdf.AggregationStatisticCV = ["Cumulative", "Cumulative", "Cumulative", "Cumulative", "Cumulative",
                                "Cumulative", "Cumulative", "Cumulative", "Cumulative", "Cumulative",
                                "Cumulative", "Cumulative",  "Cumulative", "Cumulative", "Cumulative",
                                "Cumulative", "Cumulative", "Cumulative", "Cumulative", "Cumulative"]

outdf.AmountUnitCV = ["CFS", "CFS", "CFS", "CFS", "CFS", "CFS", "CFS", "CFS", "CFS", "CFS",
                      "CFS", "CFS", "CFS", "CFS", "CFS", "CFS", "CFS", "CFS", "CFS", "CFS"]

outdf.MaximumAmountUnitCV = ["AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY",
                             "AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY"]

outdf.ReportYearStartMonth = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1",
                              "1", "1", "1", "1", "1", "1", "1", "1", "1", "1",]

outdf.ReportYearTypeCV = ["CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear",
                          "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear",
                          "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear",
                          "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear"]

outdf.VariableCV = ["Demand", "Demand", "Demand", "Demand",
                    "Supply", "Supply", "Supply", "Supply", "Supply", "Supply", "Supply", "Supply",
                    "Supply", "Supply", "Supply", "Supply", "Supply", "Supply", "Supply", "Supply"]

outdf.VariableSpecificCV = ["Demand_Annual_Agricultural_Unspecified",
                            "Demand_Annual_Indian_Unspecified",
                            "Demand_Annual_Industrial_Unspecified",
                            "Demand_Annual_Municipal_Unspecified",
                            "Supply_Annual_Agricultural_Effluent",
                            "Supply_Annual_Agricultural_Groundwater",
                            "Supply_Annual_Agricultural_Surface Water",
                            "Supply_Annual_Agricultural_Unspecified",
                            "Supply_Annual_Indian_Effluent",
                            "Supply_Annual_Indian_Groundwater",
                            "Supply_Annual_Indian_Surface Water",
                            "Supply_Annual_Indian_Unspecified",
                            "Supply_Annual_Industrial_Effluent",
                            "Supply_Annual_Industrial_Groundwater",
                            "Supply_Annual_Industrial_Surface Water",
                            "Supply_Annual_Industrial_Unspecified",
                            "Supply_Annual_Municipal_Effluent",
                            "Supply_Annual_Municipal_Groundwater",
                            "Supply_Annual_Municipal_Surface Water",
                            "Supply_Annual_Municipal_Unspecified"]


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

#Report missing values if need be to separate csv
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/variables_missing.csv', index=False)

print("Done.")