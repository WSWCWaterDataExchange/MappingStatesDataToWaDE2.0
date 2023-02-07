#Date Created: 06/21/2022
#Purpose: To extract NV methods use information and populate dataframe for WaDE_QA 2.0.
#Notes:   1) Single row of entries for Methods Table.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Nevada/WaterAllocation"
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

outdf.MethodUUID = "NVwr_M1"

outdf.ApplicableResourceTypeCV = "Surface Ground"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = """The Nevada Division of Water Resources makes no warranties or guarantees, either expressed or implied as to the completeness, accuracy, or correctness of the data portrayed in this product nor accepts any liability, arising from any incorrect, incomplete or misleading information contained therein. All information, data and databases are provided “as is” with no warranty, expressed or implied, including but not limited to, fitness for a particular purpose. Users should also note that property boundaries included in any product do not represent an on- the-ground survey suitable for legal, engineering, or surveying purposes. They represent only the approximate relative locations. By accessing this website and/or data contained within the databases, you hereby release the Nevada Division of Water Resources, its employees, agents, contractors, and suppliers from any and all responsibility and liability associated with its use. In no event shall the Nevada Division of Water Resources or its officers or employees be liable for any damages arising in any way from the use of the website, or use of the information contained in the databases herein."""

outdf.MethodName = "Nevada Water Rights Method"

outdf.MethodNEMILink = "http://water.nv.gov/waterlaw.aspx"

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
