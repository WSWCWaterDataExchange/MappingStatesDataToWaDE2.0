# Date Updated: 05/03/2022
# Purpose: To create NM agg variable use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) No input csv to read, all values are more easily hardcoded into a list here and then exported to CSV.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/NewMexico/AggregatedAmounts"
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
#outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.VariableSpecificUUID = ["NMag_V1",
"NMag_V2",
"NMag_V3",
"NMag_V4",
"NMag_V5",
"NMag_V6",
"NMag_V7",
"NMag_V8",
"NMag_V9",
"NMag_V10",
"NMag_V11",
"NMag_V12",
"NMag_V13",
"NMag_V14",
"NMag_V15",
"NMag_V16",
"NMag_V17",
"NMag_V18"]

outdf.VariableSpecificCV = ["Withdrawal_Annual_Commercial_Groundwater",
"Withdrawal_Annual_Domestic_Groundwater",
"Withdrawal_Annual_Industrial_Groundwater",
"Withdrawal_Annual_Irrigated Agriculture_Groundwater",
"Withdrawal_Annual_Livestock_Groundwater",
"Withdrawal_Annual_Mining_Groundwater",
"Withdrawal_Annual_Power_Groundwater",
"Withdrawal_Annual_Public Supply_Groundwater",
"Withdrawal_Annual_Reservoir Evaporation_Groundwater",
"Withdrawal_Annual_Commercial_Surface Water",
"Withdrawal_Annual_Domestic_Surface Water",
"Withdrawal_Annual_Industrial_Surface Water",
"Withdrawal_Annual_Irrigated Agriculture_Surface Water",
"Withdrawal_Annual_Livestock_Surface Water",
"Withdrawal_Annual_Mining_Surface Water",
"Withdrawal_Annual_Power_Surface Water",
"Withdrawal_Annual_Public Supply_Surface Water",
"Withdrawal_Annual_Reservoir Evaporation_Surface Water"]

outdf.AggregationInterval = "1"

outdf.AggregationIntervalUnitCV = "Annual"

outdf.AggregationStatisticCV = "Cumulative"

outdf.AmountUnitCV = "AF"

outdf.MaximumAmountUnitCV = "AF"

outdf.ReportYearStartMonth = "10"

outdf.ReportYearTypeCV = "WaterYear"

outdf.VariableCV = "Withdrawal"


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
