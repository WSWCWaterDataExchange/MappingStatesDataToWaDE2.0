# Date Update: 05/06/2022
# Purpose: To extract AZ methods use information and populate dataframe for WaDE_QA 2.0.
# Notes: N/A


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Arizona/WaterAllocation"
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

outdf.MethodUUID = ["AZwr_M1", "AZwr_M2"]

outdf.ApplicableResourceTypeCV = ["Groundwater", "Surface Water"]

outdf.DataConfidenceValue = ""

outdf.DataQualityValueCV = ""

outdf.DataCoverageValue = ""

outdf.MethodDescription = [
"""The data on this website was developed by the Arizona Department of Water Resources (“Department”), for uses beneficial to the State of Arizona. The information is available to interested members of the public. While the Department believes the information to be reliable and made efforts to assure its reliability at the time the information was compiled, the information is provided “as is.” The Department is not responsible for the accuracy, completeness, quality or legal sufficiency of the information. Any expressed or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for the purpose ARE SPECIFICALLY DISCLAIMED. Neither the Department nor the State of Arizona shall be held liable for any direct, indirect, incidental, special, exemplary or consequential damages (including, but not limited to: procurement of substitute goods or services; loss of use, data or profits; or business interruption), however caused and on any theory of liability, whether in contract, strict liability or its aggregate use with other information, data or programs. The information contained in each of the basin descriptions at this site was obtained from information on file in the offices of the Department of Water Resources and limited additional information. Recent studies may contain additional, more up-to-date information. The State of Arizona and the Department of Water Resources hereby specifically retain any intellectual property interest, including copyright, that it may hold in the information provided, whether the information is in the form of data, files, text images, photography or maps.
The Department requests that persons receiving and using this information not make it available to others for their re-use. Instead, interested third parties should be encouraged to request copies directly from the Department, the source that developed the information, in order to provide the greatest degree of reliability.
The Groundwater Site Inventory (GWSI) is ADWR's main repository for state-wide groundwater data. The GWSI consists of field-verified data regarding wells and springs collected by personnel from ADWR's Hydrology Division's Field Services Section, the U.S. Geological Survey, and other co-operating agencies. The information in GWSI is constantly being updated by ongoing field investigations and through a state-wide network of water level and water quality monitoring sites."""
,
"""The data on this website was developed by the Arizona Department of Water Resources (“Department”), for uses beneficial to the State of Arizona. The information is available to interested members of the public. While the Department believes the information to be reliable and made efforts to assure its reliability at the time the information was compiled, the information is provided “as is.” The Department is not responsible for the accuracy, completeness, quality or legal sufficiency of the information. Any expressed or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for the purpose ARE SPECIFICALLY DISCLAIMED. Neither the Department nor the State of Arizona shall be held liable for any direct, indirect, incidental, special, exemplary or consequential damages (including, but not limited to: procurement of substitute goods or services; loss of use, data or profits; or business interruption), however caused and on any theory of liability, whether in contract, strict liability or its aggregate use with other information, data or programs. The information contained in each of the basin descriptions at this site was obtained from information on file in the offices of the Department of Water Resources and limited additional information. Recent studies may contain additional, more up-to-date information. The State of Arizona and the Department of Water Resources hereby specifically retain any intellectual property interest, including copyright, that it may hold in the information provided, whether the information is in the form of data, files, text images, photography or maps.
The Department requests that persons receiving and using this information not make it available to others for their re-use. Instead, interested third parties should be encouraged to request copies directly from the Department, the source that developed the information, in order to provide the greatest degree of reliability"""
]

outdf.MethodName = ["Arizona Water Rights Method", "Arizona Water Rights Method"]

outdf.MethodNEMILink = ["https://new.azwater.gov/sites/default/files/media/Arizona%20Groundwater_Code_1.pdf", "https://new.azwater.gov/surface-water"]

outdf.MethodTypeCV = ["Legal Processes", "Legal Processes"]

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
