#Last Updated: 01/06/2022
#Author: Ryan James (WSWC)
#Purpose: To create CA site specific variable use information and population dataframe for WaDE_QA 2.0.
#Notes: 1) Used a list approach.  Needed to have five rows for VaribleCVs.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/California/SiteSpecificAmounts"
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

outdf.VariableSpecificUUID = ["CAss_V1", "CAss_V2", "CAss_V3", "CAss_V4", "CAss_V5", "CAss_V6", "CAss_V7", "CAss_V8", "CAss_V9", "CAss_V10", "CAss_V11"]

outdf.AggregationInterval = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]

outdf.AggregationIntervalUnitCV = ["Monthly", "Monthly", "Monthly", "Monthly", "Monthly", "Monthly", "Monthly", "Monthly", "Monthly", "Monthly", "Monthly"]

outdf.AggregationStatisticCV = ["Unspecified", "Unspecified", "Unspecified", "Unspecified", "Unspecified", "Unspecified", "Unspecified", "Unspecified", "Unspecified", "Unspecified", "Unspecified"]

outdf.AmountUnitCV = ["G",	"G",	"G",	"G",	"G",	"G",	"G",	"G",	"G",	"G",	"G"]

outdf.MaximumAmountUnitCV = ["G",	"G",	"G",	"G",	"G",	"G",	"G",	"G",	"G",	"G",	"G"]

outdf.ReportYearStartMonth = ["1",	"1",	"1",	"1",	"1",	"1",	"1",	"1",	"1",	"1",	"1"]

outdf.ReportYearTypeCV = ["CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear"]

outdf.VariableCV = ["Delivered", "Delivered", "Delivered", "Delivered", "Delivered", "Delivered", "Delivered", "Delivered", "Produced", "Produced", "Produced"]

outdf.VariableSpecificCV = ["Cumulative Delivered_Monthly_Single Family Residential_Unspecified",
                            "Cumulative Delivered_Monthly_Multi Family Residential_Unspecified",
                            "Cumulative Delivered_Monthly_Commercial Institutional_Unspecified",
                            "Cumulative Delivered_Monthly_Industrial_Unspecified",
                            "Cumulative Delivered_Monthly_Landscape Irrigation_Unspecified",
                            "Cumulative Delivered_Monthly_Other_Unspecified",
                            "Cumulative Delivered_Monthly_Agricultural_Unspecified",
                            "Cumulative Delivered_Monthly_Other PWS_Unspecified",
                            "Cumulative Produced_Monthly_Total_Groundwater",
                            "Cumulative Produced_Monthly_Total_Surface Water",
                            "Cumulative Produced_Monthly_Total_Purchased"]


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
