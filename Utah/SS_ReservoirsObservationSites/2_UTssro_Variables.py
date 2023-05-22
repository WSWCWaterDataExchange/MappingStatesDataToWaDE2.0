# Date Update: 03/22/2023
# Purpose: To create UT site specific reservoir and observation site variable use information and population dataframe for WaDE_QA 2.0.
# Notes: N/A


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd
######################################################
import sys

# columns
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/MappingFunctions")
import GetColumnsFile

# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Utah/SS_ReservoirsObservationSites"
os.chdir(workingDir)

# WaDE columns
VariablesColumnsList = GetColumnsFile.GetVariablesColumnsFunction()

# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=VariablesColumnsList)
# outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.VariableSpecificUUID = ["UTssro_V1", "UTssro_V2", "UTssro_V3", "UTssro_V4", "UTssro_V5",  "UTssro_V6"]

outdf.AggregationInterval = "1"

outdf.AggregationIntervalUnitCV = "Daily"

outdf.AggregationStatisticCV = "WaDE Unspecified"

outdf.AmountUnitCV = ["AF", "CFS", "CFS", "CFS", "FT", "AF"]

outdf.MaximumAmountUnitCV = ["AF", "CFS", "CFS", "CFS", "FT", "AF"]

outdf.ReportYearStartMonth = "1"

outdf.ReportYearTypeCV = "CalendarYear"

outdf.VariableCV = ["Discharge AF",
                    "Discharge",
                    "Diversion",
                    "Evaporation",
                    "Stage",
                    "Storage"]

outdf.VariableSpecificCV = ["Discharge AF_Daily_Discharge_Surface Water",
                            "Discharge_Daily_Discharge_Surface Water",
                            "Diversion_Daily_Diversion_Surface Water",
                            "Evaporation_Daily_Evaporation_Surface Water",
                            "Stage_Daily_Stage_Surface Water",
                            "Storage_Daily_Storage_Surface Water"]

# Check required fields are not null
############################################################################
print("Check required is not null...")
# #Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan)  # replace blank strings by NaN, if there are any
outdf_nullMand = outdf.loc[(outdf["VariableSpecificUUID"].isnull()) | (outdf["VariableSpecificUUID"] == '') |
                           (outdf["AggregationInterval"].isnull()) | (outdf["AggregationInterval"] == '') |
                           (outdf["AggregationIntervalUnitCV"].isnull()) | (outdf["AggregationIntervalUnitCV"] == '') |
                           (outdf["AggregationStatisticCV"].isnull()) | (outdf["AggregationStatisticCV"] == '') |
                           (outdf["AmountUnitCV"].isnull()) | (outdf["AmountUnitCV"] == '') |
                           (outdf["MaximumAmountUnitCV"].isnull()) | (outdf["MaximumAmountUnitCV"] == '') |
                           (outdf["ReportYearStartMonth"].isnull()) | (outdf["ReportYearStartMonth"] == '') |
                           (outdf["VariableCV"].isnull()) | (outdf["VariableCV"] == '') |
                           (outdf["VariableSpecificCV"].isnull()) | (outdf["VariableSpecificCV"] == '')]

# Export to new csv
############################################################################
print("Exporting dataframe to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/variables.csv', index=False)

# Report purged values.
if (len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/variables_mandatoryFieldMissing.csv', index=False)

print("Done.")
