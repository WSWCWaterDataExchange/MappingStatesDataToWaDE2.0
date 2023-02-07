# Date Updated: 03/20/2022
# Author: Ryan James
# Purpose: To create OK methods use information and populate dataframe for WaDE_QA 2.0.
# Notes:


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Oklahoma/WaterAllocation"
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

outdf.MethodUUID = "OKwr_M1"

outdf.ApplicableResourceTypeCV = "Surface Ground Water"

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = """The map layers displayed in this map service or viewer were produced from various sources at varying degrees of accuracy and precision. Therefore these maps should only be used for general reference information. Metadata documents are provided for each geographic layer. These documents describe the layer’s purpose and limitations. The data represent the results of data collection and/or processing for the specific Oklahoma Water Resources Board (OWRB) activity or purpose described above. As such, the data are valid only for their use, content, time, and accuracy specifications determined or intended by, or acceptable to, the OWRB. These data are not guaranteed to be useable, timely, accurate, or complete. The user is responsible for any use of these data other than their use by the OWRB, and for the results of any application of the data for other than the purpose intended by the OWRB. Although these data have been processed successfully on a computer system at the OWRB, NEITHER THE STATE OF OKLAHOMA NOR THE OWRB NOR ANY OTHER AGENCY THEREOF, NOR ANY OF THEIR EMPLOYEES, CONTRACTORS, OR SUBCONTRACTORS, MAKE ANY WARRANTY, EXPRESS OR IMPLIED, NOR ASSUME ANY LEGAL LIABILITY OR RESPONSIBILITY FOR OR AS TO THE ACCURACY, COMPLETENESS, USEFULNESS OR MERCHANTABILITY OF ANY DATUM, SOFTWARE, INFORMATION, APPARATUS, PRODUCT, OR PROCESS DISCLOSED, NOR REPRESENT THAT ITS USE WOULD NOT INFRINGE ON PRIVATELY OWNED RIGHTS. NOR SHALL THE ACT OF DISTRIBUTION CONSTITUTE ANY SUCH WARRANTY. THIS DISCLAIMER APPLIES BOTH TO INDIVIDUAL USE OF THE DATA AND AGGREGATE USE WITH OTHER DATA. Conclusions drawn from, or actions undertaken on the basis of, such data and information are the sole responsibility of the user. Users are cautioned to consider carefully the provisional nature of these data and information before using them for decisions that concern personal or public safety or the conduct of business that involves substantial monetary or operational consequences."""

outdf.MethodName = "Oklahoma Water Rights Method"

outdf.MethodNEMILink = "https://www.owrb.ok.gov/wateruse/index.php"

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
    outdf_nullMand.to_csv('ProcessedInputData/methods_missing.csv', index=False)

print("Done.")
