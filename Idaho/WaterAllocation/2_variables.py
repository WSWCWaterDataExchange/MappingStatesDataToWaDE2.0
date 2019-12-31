#Date Created: 12/06/2019
#Purpose: To extract ID variables use infromation and population dataframe for WaDE 2.0.
#Notes: 1) Single row of entires, inpVals, for Variable Table.



# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os



# Inputs
############################################################################
print("Reading input csv...")
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Idaho/WaterAllocation"
os.chdir(workingDir)
fileInput="RawinputData/ID_Water_Master.csv"
df = pd.read_csv(fileInput)



# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")

#WaDE columns
columns=['VariableSpecificUUID', 'VariableSpecificCV', 'VariableCV', 'AggregationStatisticCV', 'AggregationInterval',
         'AggregationIntervalUnitCV', 'ReportYearStartMonth', 'ReportYearTypeCV', 'AmountUnitCV', 'MaximumAmountUnitCV']

# #ry_comment: @dtypesx, his list isn't being used for anything...
dtypesx = []

inpVals = ['IDWR Allocation All', np.nan, np.nan, np.nan, np.nan, np.nan, '2019-1', 'Calender', 'CFS', 'AF']  # Hardcoded
outdf = pd.DataFrame([inpVals], columns=columns)



# Check required fields are not null
############################################################################
print("Check required is not null...")
# #Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
# #ry_comment: @requiredCols, this list isn't being used for anything...
# requiredCols=['VariableSpecificUUID','VariableSpecificCV', 'VariableCV', 'AggregationStatisticCV', 'AggregationInterval',
#               'AggregationIntervalUnitCV', 'ReportYearStartMonth', 'ReportYearTypeCV', 'AmountUnitCV']

outdf = outdf.replace('', np.nan) #replace blank strings by NaN, if there are any
outdf_nullMand = outdf.loc[(outdf["VariableSpecificUUID"].isnull()) | (outdf["VariableSpecificCV"].isnull()) |
                                (outdf["VariableCV"].isnull()) | (outdf["AggregationStatisticCV"].isnull()) |
                                (outdf["AggregationInterval"].isnull()) | (outdf["AggregationIntervalUnitCV"].isnull()) |
                                (outdf["ReportYearStartMonth"].isnull()) | (outdf["ReportYearTypeCV"].isnull()) |
                                (outdf["AmountUnitCV"].isnull()) | (outdf["MaximumAmountUnitCV"].isnull())]



# Export to new csv
############################################################################
print("Exporting dataframe to csv...")
outdf.to_csv('ProcessedInputData/variables.csv', index=False)

#Report missing values if need be to seperate csv
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/variables_mandatoryFieldMissing.csv')  # index=False,


print("Done.")