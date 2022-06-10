# Last Updated: 06/01/2022
# Purpose: To create ND site specific variable use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) Used a list approach.  Needed to have five rows for VaribleCVs.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/NorthDakota/SiteSpecificAmounts"
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

outdf.VariableSpecificUUID = ["NDss_V1",
"NDss_V2",
"NDss_V3",
"NDss_V4",
"NDss_V5",
"NDss_V6",
"NDss_V7",
"NDss_V8",
"NDss_V9",
"NDss_V10",
"NDss_V11",
"NDss_V12",
"NDss_V13",
"NDss_V14",
"NDss_V15",
"NDss_V16",
"NDss_V17",
"NDss_V18",
"NDss_V19",
"NDss_V20",
"NDss_V21",
"NDss_V22",
"NDss_V23",
"NDss_V24",
"NDss_V25",
"NDss_V26",
"NDss_V27",
"NDss_V28",
"NDss_V29",
"NDss_V30",
"NDss_V31",
"NDss_V32",
"NDss_V33"]

outdf.AggregationInterval = "1"

outdf.AggregationIntervalUnitCV = "Annual"

outdf.AggregationStatisticCV = "Unspecified"

outdf.AmountUnitCV = "MG"

outdf.MaximumAmountUnitCV = "MG"

outdf.ReportYearStartMonth = "1"

outdf.ReportYearTypeCV = "CalendarYear"

outdf.VariableCV = "Withdrawal"

outdf.VariableSpecificCV = ["Withdrawal_Annual_Commercial_Groundwater",
"Withdrawal_Annual_Commercial_Surface Water",
"Withdrawal_Annual_Domestic_Groundwater",
"Withdrawal_Annual_Domestic_Surface Water",
"Withdrawal_Annual_Fish And Wildlife_Groundwater",
"Withdrawal_Annual_Fish And Wildlife_Surface Water",
"Withdrawal_Annual_Fish And Wildlife_Unspecified",
"Withdrawal_Annual_Flood Control_Surface Water",
"Withdrawal_Annual_Industrial_Groundwater",
"Withdrawal_Annual_Industrial_Surface Water",
"Withdrawal_Annual_Industrial_Unspecified",
"Withdrawal_Annual_Irrigation_Groundwater",
"Withdrawal_Annual_Irrigation_Surface Water",
"Withdrawal_Annual_Irrigation_Unspecified",
"Withdrawal_Annual_Multiple Use_Groundwater",
"Withdrawal_Annual_Multiple Use_Surface Water",
"Withdrawal_Annual_Multiple Use_Unspecified",
"Withdrawal_Annual_Municipal_Groundwater",
"Withdrawal_Annual_Municipal_Surface Water",
"Withdrawal_Annual_Municipal_Unspecified",
"Withdrawal_Annual_Power Generation_Groundwater",
"Withdrawal_Annual_Power Generation_Surface Water",
"Withdrawal_Annual_Power Generation_Unspecified",
"Withdrawal_Annual_Recreation_Groundwater",
"Withdrawal_Annual_Recreation_Surface Water",
"Withdrawal_Annual_Rural Water_Groundwater",
"Withdrawal_Annual_Rural Water_Surface Water",
"Withdrawal_Annual_Rural Water_Unspecified",
"Withdrawal_Annual_Stock_Groundwater",
"Withdrawal_Annual_Stock_Surface Water",
"Withdrawal_Annual_Unspecified_Groundwater",
"Withdrawal_Annual_Unspecified_Surface Water",
"Withdrawal_Annual_Unspecified_Unspecified"]


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
