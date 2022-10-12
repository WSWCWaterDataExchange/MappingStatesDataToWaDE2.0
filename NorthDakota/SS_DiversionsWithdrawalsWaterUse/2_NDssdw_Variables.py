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
workingDir = "G:/Shared drives/WaDE Data/NorthDakota/SS_DiversionsWithdrawalsWaterUse"
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

outdf.VariableSpecificUUID = [
"NDssdw_V1",
"NDssdw_V2",
"NDssdw_V3",
"NDssdw_V4",
"NDssdw_V5",
"NDssdw_V6",
"NDssdw_V7",
"NDssdw_V8",
"NDssdw_V9",
"NDssdw_V10",
"NDssdw_V11",
"NDssdw_V12",
"NDssdw_V13",
"NDssdw_V14",
"NDssdw_V15",
"NDssdw_V16",
"NDssdw_V17",
"NDssdw_V18",
"NDssdw_V19",
"NDssdw_V20",
"NDssdw_V21",
"NDssdw_V22",
"NDssdw_V23",
"NDssdw_V24",
"NDssdw_V25",
"NDssdw_V26",
"NDssdw_V27",
"NDssdw_V28",
"NDssdw_V29",
"NDssdw_V30",
"NDssdw_V31",
"NDssdw_V32",
"NDssdw_V33"]

outdf.AggregationInterval = "1"

outdf.AggregationIntervalUnitCV = "Annual"

outdf.AggregationStatisticCV = "Unspecified"

outdf.AmountUnitCV = "MG"

outdf.MaximumAmountUnitCV = "MG"

outdf.ReportYearStartMonth = "1"

outdf.ReportYearTypeCV = "CalendarYear"

outdf.VariableCV = "Withdrawal"

outdf.VariableSpecificCV = [
"Withdrawal_Annual_Commercial_Groundwater",
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
