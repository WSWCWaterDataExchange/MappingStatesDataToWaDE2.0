# Date Created: 06/17/2022
# Purpose: To create CO ag variable use information and populate a dataframe for WaDE_QA 2.0.
# Notes: 1) No input csv to read, all values are more easily hardcoded into a list here and then exported to CSV.
#        2) Special case of VariableCV and VariableSpecificCV.
#        3) Using a temp df to count out number for rows for outbound df for VariableSpecificUUID.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Colorado/AggregatedAmounts"
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

# For creating VariableSpecificUUID
def assignVariableSpecificUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "COag_V" + string1
    return outstring


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")

outdf = pd.DataFrame(columns=columnslist)
# outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.VariableSpecificCV = ["ReservoirStorage_Monthly_Unspecified_Surface Water",
                            "ForecastedRunoff_Monthly_Unspecified_Surface Water",
                            "PrevMoStreamflow_Monthly_Unspecified_Surface Water"]

outdf.VariableCV = ["ReservoirStorage", "ForecastedRunoff", "PrevMoStreamflow"]

outdf.AggregationInterval = "1"

outdf.AggregationIntervalUnitCV = "Year"

outdf.AggregationStatisticCV = "Cumulative"

outdf.AmountUnitCV = "AFY"

outdf.MaximumAmountUnitCV = "AFY"

outdf.ReportYearStartMonth = "1"

outdf.ReportYearTypeCV = "CalendarYear"

print("VariableSpecificUUID")
#using temp df to count out number of rows for outdf
tempdf = pd.DataFrame(columns=columnslist)
tempdf['VariableCV'] = outdf['VariableCV']
tempdf["Count"] = range(1, len(tempdf.index) + 1)
outdf['VariableSpecificUUID'] = tempdf.apply(lambda row: assignVariableSpecificUUID(row['Count']), axis=1)


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
