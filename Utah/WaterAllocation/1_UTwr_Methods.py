# Date Update: 03/10/2023
# Purpose: To extract UT methods use information and populate dataframe for WaDE_QA 2.0.
# Notes: N/A


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Custom Libraries
############################################################################
import sys
# columns
sys.path.append("C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/MappingFunctions")
import GetColumnsFile


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Utah/WaterAllocation"
os.chdir(workingDir)

# WaDE columns
MethodsColumnsList = GetColumnsFile.GetMethodsColumnsFunction()


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=MethodsColumnsList)
outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.MethodUUID = "UTwr_M1"

outdf.ApplicableResourceTypeCV = "Surface Water and Groundwater"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = """The Point of Diversion feature class is a complete record of point of diversion locations taken from the Division's day to day operating database. The database is a complete record with the following exceptions:1) The Division's point of diversion referencing policy includes a provision which allows some point of diversion locations to be described more as areas (Point-to-Point Filings) than discrete points. Point to point filings are usually limited to stock watering rights. They are represented  by a discrete point which is located within the area covered by the point to point description.2) Utah State Law required applications to divert surface water to be filed with the State Engineer after 1903 and groundwater after 1935. There may be existing diversions which began prior to those dates which are not included in the Division of Water Right records. The Division becomes aware of these rights and includes these rights in it's records when the user submits a statement of water user claim either pursuant to an adjudication or to establish there is a water right under which the State Engineer is to take action.3) Data in the Division of Water Rights database was entered over an eight year period from paper files maintained by the office. Data entered in the database has been subsequently verified by staff. However, errors are occasionally detected in the database as a result of entry operations either from current staff activities or the original entry project. The Division makes an ongoing effort to maintain the database free of errors and omissions, however users of the data are responsible to verify it is suitable for their purpose. The Division appreciates and encourages users to promptly disclose any inconsistencies detected in the data to Division staff who will make every effort to correct any errors discovered."""

outdf.MethodName = "Utah Water Rights Method"

outdf.MethodNEMILink = "https://waterrights.utah.gov/code_index.asp"

outdf.MethodTypeCV = "Legal Processes"

# Check required fields are not null
############################################################################
print("Check required is not null...")
#Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan)
outdf_nullMand = outdf.loc[(outdf["MethodUUID"].isnull()) | (outdf["MethodUUID"] == '') |
                           (outdf["MethodName"].isnull()) | (outdf["MethodName"] == '') |
                           (outdf["MethodDescription"].isnull()) | (outdf["MethodDescription"] == '') |
                           (outdf["ApplicableResourceTypeCV"].isnull()) | (outdf["ApplicableResourceTypeCV"] == '') |
                           (outdf["MethodTypeCV"].isnull()) | (outdf["MethodTypeCV"] == '')]


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/methods.csv', index=False)

# Report purged values.
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/methods_mandatoryFieldMissing.csv', index=False)

print("Done.")