# Author: Ryan James (WSWC)
# Date Created: 08/26/2021
# Purpose: To extract CA date use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) asdf


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/California/Regulatory"

os.chdir(workingDir)

#WaDE columns
columnslist = [
    "Date",
    "Year"]


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
inpVals = [
    "08/26/2021",
    "2021"]

outdf = pd.DataFrame([inpVals], columns=columnslist)

# Changing datatype of used date fields.
outdf['Date'] = pd.to_datetime(outdf['Date'], errors = 'coerce')
outdf['Date'] = pd.to_datetime(outdf["Date"].dt.strftime('%m/%d/%Y'))


# Check required fields are not null
############################################################################
print("Check required is not null...")
#Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan)
outdf_nullMand = outdf.loc[(outdf["Date"].isnull()) | (outdf["Date"] == '') |
                           (outdf["Year"].isnull()) | (outdf["Year"] == '')]


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/date.csv', index=False)

# Report purged values.
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/date_mandatoryFieldMissing.csv', index=False)

print("Done.")
