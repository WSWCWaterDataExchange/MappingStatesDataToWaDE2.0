# Last Updated: 10/12/2022
# Purpose: To create UT site specific public supply variable use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) Used a list approach.  Needed to have five rows for VaribleCVs.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Utah/SS_PublicSupplyWaterUse"
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

outdf.VariableSpecificUUID = ["UTssps_V1",
                              "UTssps_V2",
                              "UTssps_V3",
                              "UTssps_V4",
                              "UTssps_V5",
                              "UTssps_V6",
                              "UTssps_V7",
                              "UTssps_V8",
                              "UTssps_V9",
                              "UTssps_V10",
                              "UTssps_V11"]

outdf.AggregationInterval = "1"

outdf.AggregationIntervalUnitCV = "Year"

outdf.AggregationStatisticCV = "Cumulative"

outdf.AmountUnitCV = "G"

outdf.MaximumAmountUnitCV = "G"

outdf.ReportYearStartMonth = "1"

outdf.ReportYearTypeCV = "CalendarYear"

outdf.VariableCV = ["Delivered Water Use",
                    "Delivered Water Use",
                    "Delivered Water Use",
                    "Delivered Water Use",
                    "Delivered Water Use",
                    "Withdrawal",
                    "Withdrawal",
                    "Withdrawal",
                    "Withdrawal",
                    "Withdrawal",
                    "Withdrawal"]


outdf.VariableSpecificCV = ["Delivered Water Use_Annual_Domestic_Unspecified",
"Delivered Water Use_Annual_Commercial_Unspecified",
"Delivered Water Use_Annual_Industrial_Unspecified",
"Delivered Water Use_Annual_Institutional_Unspecified",
"Delivered Water Use_Annual_DCII_Unspecified",
"Withdrawal_Annual_DCII_Surface Water",
"Withdrawal_Annual_DCII_Groundwater",
"Withdrawal_Annual_DCII_Unspecified",
"Withdrawal_Monthly_DCII_Surface Water",
"Withdrawal_Monthly_DCII_Groundwater",
"Withdrawal_Monthly_DCII_Unspecified"]


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