# Last Updated: 05/17/2022
# Purpose: To create NJ site specific variable use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) Used a list approach.  Needed to have five rows for VaribleCVs.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/NewJersey/SiteSpecificAmounts"
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

outdf.VariableSpecificUUID = ["NJss_V1",
"NJss_V2",
"NJss_V3",
"NJss_V4",
"NJss_V5",
"NJss_V6",
"NJss_V7",
"NJss_V8",
"NJss_V9",
"NJss_V10",
"NJss_V11",
"NJss_V12",
"NJss_V13",
"NJss_V14",
"NJss_V15",
"NJss_V16",
"NJss_V17",
"NJss_V18",
"NJss_V19",
"NJss_V20",
"NJss_V21",
"NJss_V22",
"NJss_V23",
"NJss_V24",
"NJss_V25",
"NJss_V26",
"NJss_V27",
"NJss_V28",
"NJss_V29",
"NJss_V30"]

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
