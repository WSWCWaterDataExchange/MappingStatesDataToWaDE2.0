# Last Updated: 10/12/2022
# Purpose: To create NJ site specific public supply variable use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) Used a list approach.  Needed to have five rows for VaribleCVs.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/NewJersey/SS_PublicSupplyWaterUse"
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

outdf.VariableSpecificUUID = ["NJssps_V1",
"NJssps_V2",
"NJssps_V3",
"NJssps_V4",
"NJssps_V5",
"NJssps_V6",
"NJssps_V7",
"NJssps_V8",
"NJssps_V9",
"NJssps_V10",
"NJssps_V11",
"NJssps_V12",
"NJssps_V13",
"NJssps_V14",
"NJssps_V15",
"NJssps_V16",
"NJssps_V17",
"NJssps_V18",
"NJssps_V19",
"NJssps_V20",
"NJssps_V21",
"NJssps_V22",
"NJssps_V23",
"NJssps_V24",
"NJssps_V25",
"NJssps_V26",
"NJssps_V27",
"NJssps_V28",
"NJssps_V29",
"NJssps_V30"]

outdf.AggregationInterval = "1"

outdf.AggregationIntervalUnitCV = "Monthly"

outdf.AggregationStatisticCV = "Unspecified"

outdf.AmountUnitCV = "MG"

outdf.MaximumAmountUnitCV = "MG"

outdf.ReportYearStartMonth = "1"

outdf.ReportYearTypeCV = "CalendarYear"

outdf.VariableCV = ["Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal"]


outdf.VariableSpecificCV = ["Return_Monthly_Irrigation_Unspecified",
"Return_Monthly_Not Classified_Groundwater",
"Return_Monthly_Not Classified_Surface Water",
"Return_Monthly_Not Classified_Unspecified",
"Return_Monthly_Potable Supply_Groundwater",
"Return_Monthly_Potable Supply_Surface Water",
"Return_Monthly_Potable Supply_Unspecified",
"Withdrawal_Monthly_Agricultural_Groundwater",
"Withdrawal_Monthly_Agricultural_Surface Water",
"Withdrawal_Monthly_Commercial_Groundwater",
"Withdrawal_Monthly_Commercial_Surface Groundwater",
"Withdrawal_Monthly_Commercial_Surface Water",
"Withdrawal_Monthly_Industrial_Groundwater",
"Withdrawal_Monthly_Industrial_Surface Groundwater",
"Withdrawal_Monthly_Industrial_Surface Water",
"Withdrawal_Monthly_Industrial_Unspecified",
"Withdrawal_Monthly_Irrigation_Groundwater",
"Withdrawal_Monthly_Irrigation_Surface Groundwater",
"Withdrawal_Monthly_Irrigation_Surface Water",
"Withdrawal_Monthly_Irrigation_Unspecified",
"Withdrawal_Monthly_Mining_Groundwater",
"Withdrawal_Monthly_Mining_Surface Groundwater",
"Withdrawal_Monthly_Mining_Surface Water",
"Withdrawal_Monthly_Mining_Unspecified",
"Withdrawal_Monthly_Potable Supply_Groundwater",
"Withdrawal_Monthly_Potable Supply_Surface Groundwater",
"Withdrawal_Monthly_Potable Supply_Surface Water",
"Withdrawal_Monthly_Potable Supply_Unspecified",
"Withdrawal_Monthly_Power Generation_Groundwater",
"Withdrawal_Monthly_Power Generation_Surface Water"]


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
