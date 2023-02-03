#Date Created: 04/08/2020
#Purpose: To create ND methods use information and populate dataframe for WaDE_QA 2.0.
#Notes:


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/NorthDakota/WaterAllocation"
os.chdir(workingDir)

#WaDE columns
columnslist = [
    "MethodUUID",
    "ApplicableResourceTypeCV",
    "DataConfidenceValue",
    "DataCoverageValue",
    "DataQualityValueCV",
    "MethodDescription",
    "MethodName",
    "MethodNEMILink",
    "MethodTypeCV"]


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist)
outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.MethodUUID = "NDwr_M1"

outdf.ApplicableResourceTypeCV = "Surface Ground"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = """This data is provided by the ND Department of Water Resources for your convenience. This data is provisional. This service is provided "AS IS" and without warranty of any kind, either express or implied. No warranty, either expressed or implied, is made regarding the accuracy or utility of the data or information presented at this site. The ND Department of Water Resources is not responsible for any errors or damages that may occur resulting from the use or mis-use of the data that is provided at this site. If you have any questions regarding the data, generation methods, or errors, please direct any these comments to Chris Bader at ND Department of Water Resources. Phone: (701) 328-4771 E-Mail: cbader@nd.gov"""

outdf.MethodName = "North Dakota Water Rights Method"

outdf.MethodNEMILink = "https://www.swc.nd.gov/reg_approp/waterpermits/"

outdf.MethodTypeCV =  "Legal Processes"


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
    outdf_nullMand.to_csv('ProcessedInputData/methods_missing.csv', index=False)

print("Done.")
