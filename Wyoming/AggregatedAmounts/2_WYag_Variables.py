# Date Updated: 02/08/2022
# Author: Ryan James (WSWC)
# Purpose: To create WY agg variable use information and populate a dataframe for WaDE_QA 2.0.
# Notes: 1) No input csv to read, all values are more easily hardcoded into a list here and then exported to CSV.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Wyoming/AggregatedAmounts"
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

outdf.VariableSpecificUUID = ["WYag_V1", "WYag_V2", "WYag_V3", "WYag_V4",
                              "WYag_V5", "WYag_V6", "WYag_V7", "WYag_V8",
                              "WYag_V9"]

outdf.AggregationInterval = ["1", "1", "1", "1", "1", "1", "1", "1", "1"]

outdf.AggregationIntervalUnitCV = ["Annual", "Annual", "Annual", "Annual",
                                   "Annual", "Annual", "Annual", "Annual",
                                   "Annual"]

outdf.AggregationStatisticCV = ["Cumulative", "Cumulative", "Cumulative", "Cumulative",
                                "Cumulative", "Cumulative", "Cumulative", "Cumulative",
                                "Cumulative"]

outdf.AmountUnitCV = ["AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY"]

outdf.MaximumAmountUnitCV = ["AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY", "AFY"]

outdf.ReportYearStartMonth = ["1", "1", "1", "1", "1", "1", "1", "1", "1"]

outdf.ReportYearTypeCV = ["WaterYear", "WaterYear", "WaterYear", "WaterYear",
                          "WaterYear", "WaterYear", "WaterYear", "WaterYear",
                          "WaterYear"]

outdf.VariableCV = ["Reservoirs and Gages", "Reservoirs and Gages", "Reservoirs and Gages", "Reservoirs and Gages",
                    "Reservoirs and Gages", "Reservoirs and Gages", "Reservoirs and Gages", "Reservoirs and Gages",
                    "Reservoirs and Gages"]

outdf.VariableSpecificCV = ["Consumptive Use_Annual_Agricultural Consumptive Use_Groundwater",
                            "Consumptive Use_Annual_Agricultural Consumptive Use_Surface Water",
                            "Consumptive Use_Annual_Domestic Use_Groundwater",
                            "Consumptive Use_Annual_Domestic Use_Surface Water",
                            "Consumptive Use_Annual_Industrial Use_Groundwater",
                            "Consumptive Use_Annual_Industrial Use_Surface Water",
                            "Consumptive Use_Annual_Municipal Use_Cross Basin Diversion",
                            "Consumptive Use_Annual_Municipal Use_Groundwater",
                            "Consumptive Use_Annual_Municipal Use_Surface Water"]


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

