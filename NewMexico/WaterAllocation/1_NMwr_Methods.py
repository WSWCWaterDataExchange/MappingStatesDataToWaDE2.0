# Date Update: 03/28/2023
# Purpose: To extract NM methods use information and populate dataframe for WaDE_QA 2.0.
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
workingDir = "G:/Shared drives/WaDE Data/NewMexico/WaterAllocation"
os.chdir(workingDir)

# WaDE columns
MethodsColumnsList = GetColumnsFile.GetMethodsColumnsFunction()


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=MethodsColumnsList)
outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.MethodUUID = "NMwr_M1"

outdf.ApplicableResourceTypeCV = "Surface Water and Groundwater"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = """This data represents the locations of points of diversion within the State of New Mexico administered by the NM OSE as of December 2022. This dataset has a data dictionary that can be downloaded here.  The NM Office of the State Engineer (OSE) "Point of Diversions" (POD) layer includes well locations, surface declarations, or surface permits. These data were extracted from the OSE W.A.T.E.R.S. (Water Administration Technical Engineering Resource System) database and geo-located (mapped). These data have varying degrees of accuracy and have not been validated. This message is to alert users of this data to various changes regarding how this POD data is generated and maintained by the NM Office of the State Engineer. In addition, all attribute fields are fully described in the metadata, including descriptions of field codes. Please read the metadata accompanying this GIS data layer for further information. Any questions regarding this GIS data should be directed NM OSE Information Technology Systems Bureau GIS at the contact information given below. Stephen N. Hayes NMOSE ITSB GIS Data Manager(505) 827-6321 PO Box 25102 Santa Fe, NM 87504 stephen.hayes@state.nm.us"""

outdf.MethodName = "New Mexico Water Rights Method"

outdf.MethodNEMILink = "https://www.ose.state.nm.us/WR/WRindex.php"

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