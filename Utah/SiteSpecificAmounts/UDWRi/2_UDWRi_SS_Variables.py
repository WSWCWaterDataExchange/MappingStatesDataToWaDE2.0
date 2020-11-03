#Last Updated: 09/08/2020
#Purpose: To create UT site specific variable use information and population dataframe for WaDE_QA 2.0.
#Notes: 1) Used a list approach.  Needed to have five rows for VaribleCVs.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/SiteSpecificAmounts/UDWRi"
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

outdf.VariableSpecificUUID = ["UDWRi_Site Specific Unspecified", "UDWRi_Site Specific Withdrawal",
                              "UDWRi_Site Specific Transfer In", "UDWRi_Site Specific Transfer Out",
                              "UDWRi_Site Specific Delivery", "UDWRi_Site Specific Return"]

outdf.AggregationInterval = ["1", "1", "1", "1", "1", "1"]

outdf.AggregationIntervalUnitCV = ["Year", "Year", "Year", "Year", "Year", "Year"]

outdf.AggregationStatisticCV = ["Cumulative", "Cumulative", "Cumulative", "Cumulative", "Cumulative", "Cumulative"]

outdf.AmountUnitCV = ["AF", "AF", "AF", "AF", "AF", "AF"]

outdf.MaximumAmountUnitCV = ["AF", "AF", "AF", "AF", "AF", "AF"]

outdf.ReportYearStartMonth = ["1", "1", "1", "1", "1", "1"]

outdf.ReportYearTypeCV = ["CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear", "CalendarYear"]

outdf.VariableCV = ["Unspecified", "Withdrawal", "Transfer In", "Transfer Out", "Delivery", "Return"]

outdf.VariableSpecificCV = ["Site Specific", "Site Specific", "Site Specific", "Site Specific", "Site Specific", "Site Specific"]


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
outdf.to_csv('ProcessedInputData/variables.csv', index=False)

#Report missing values if need be to separate csv
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/variables_missing.csv')  # index=False,


print("Done.")