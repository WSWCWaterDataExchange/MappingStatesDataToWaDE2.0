# Last Updated: 03/04/2022
# Purpose: To create TX site specific variable use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) Used a list approach.  Needed to have five rows for VaribleCVs.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Texas/SS_PublicSupplyWaterUse"
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
#outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.VariableSpecificUUID = ["TXssps_V1", "TXssps_V2", "TXssps_V3", "TXssps_V4", "TXssps_V5", "TXssps_V6",
                              "TXssps_V7", "TXssps_V8", "TXssps_V9", "TXssps_V10", "TXssps_V11", "TXssps_V12", "TXssps_V13", "TXssps_V14", "TXssps_V15"]

outdf.AggregationInterval = [1,	1, 1, 1, 1, 1,
                             1, 1, 1, 1, 1, 1, 1, 1, 1]

outdf.AggregationIntervalUnitCV = ["Annual",	"Annual",	"Annual",	"Monthly",	"Monthly",	"Monthly",
                                   "Annual", "Annual", "Annual", "Annual", "Annual", "Annual", "Annual", "Annual","Annual"]

outdf.AggregationStatisticCV = ["Unspecified",	"Unspecified",	"Unspecified",	"Unspecified",	"Unspecified",	"Unspecified",
                                "Unspecified", "Unspecified", "Unspecified", "Unspecified", "Unspecified","Unspecified", "Unspecified", "Unspecified", "Unspecified"]

outdf.AmountUnitCV = ["G",	"G",	"G",	"G",	"G",	"G",
                      "G", "G", "G", "G", "G", "G", "G", "G", "G"]

outdf.MaximumAmountUnitCV = ["G",	"G",	"G",	"G",	"G",	"G",
                             "G", "G", "G", "G", "G", "G", "G", "G", "G"]

outdf.ReportYearStartMonth = [1, 1, 1, 1, 1, 1,
                              1, 1, 1, 1, 1, 1, 1, 1, 1]

outdf.ReportYearTypeCV = ["CalendarYear",	"CalendarYear",	"CalendarYear",	"CalendarYear",	"CalendarYear",	"CalendarYear",
                          "CalendarYear",	"CalendarYear",	"CalendarYear",	"CalendarYear",	"CalendarYear",	"CalendarYear",	"CalendarYear",	"CalendarYear",	"CalendarYear"]

outdf.VariableCV = ["Intake",	"Intake",	"Intake",	"Intake",	"Intake",	"Intake",
                    "Water Use", "Water Use", "Water Use", "Water Use",	"Water Use",	"Water Use",	"Water Use",	"Water Use",	"Water Use"]


outdf.VariableSpecificCV = ["Intake_Annual_MI_Groundwater",	"Intake_Annual_MI_Surface Water",	"Intake_Annual_MI_Reuse",	"Intake_Monthly_MI_Groundwater",	"Intake_Monthly_MI_Surface Water",	"Intake_Monthly_MI_Reuse",
                            "Water Use_Annual_SingleFamily_Unspecified",	"Water Use_Annual_MultiFamily_Unspecified",	"Water Use_Annual_Commercial_Unspecified",	"Water Use_Annual_Industrial_Unspecified",	"Water Use_Annual_Institutional_Unspecified",	"Water Use_Annual_Agriculture_Unspecified",	"Water Use_Annual_Reuse_Unspecified",	"Water Use_Annual_TotalMetered_Unspecified",	"Water Use_Annual_TotalUnmetered_Unspecified"]


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
