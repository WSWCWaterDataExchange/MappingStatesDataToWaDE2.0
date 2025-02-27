# Date Update: 03/22/2023
# Purpose: To create UT site specific reservoir and observation site organization use information and population dataframe for WaDE_QA 2.0.
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
workingDir = "G:/Shared drives/WaDE Data/Utah/SS_ReservoirsObservationSites"
os.chdir(workingDir)

# WaDE columns
OrganizationsColumnsList = GetColumnsFile.GetOrganizationsColumnsFunction()


# Creating output dataframe (outdf)
############################################################################
print("Populating DataFrame...")
outdf = pd.DataFrame(columns=OrganizationsColumnsList)
outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.OrganizationUUID = "UTssro_O1"

outdf.OrganizationContactEmail = "jamesgreer@utah.gov"

outdf.OrganizationContactName = "James Greer"

outdf.OrganizationDataMappingURL = "https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Utah"

outdf.OrganizationName = "Utah Division of Water Rights"

outdf.OrganizationPhoneNumber = "801-538-7280"

outdf.OrganizationPurview = "Water Planning"

outdf.OrganizationWebsite = "https://water.utah.gov/"

outdf.State = "UT"


# Check required fields are not null
############################################################################
print("Checking required is not null...")  # Check all 'required' (not NA) columns have value (not empty).
outdf = outdf.replace('', np.nan)  # Replace blank strings by NaN, if there are any.
outdf_nullMand = outdf.loc[(outdf["OrganizationUUID"].isnull()) | (outdf["OrganizationUUID"] == '') |
                           (outdf["OrganizationContactEmail"].isnull()) | (outdf["OrganizationContactEmail"] == '') |
                           (outdf["OrganizationContactName"].isnull()) | (outdf["OrganizationContactName"] == '') |
                           (outdf["OrganizationDataMappingURL"].isnull()) | (outdf["OrganizationDataMappingURL"] == '') |
                           (outdf["OrganizationName"].isnull()) | (outdf["OrganizationName"] == '') |
                           (outdf["OrganizationPhoneNumber"].isnull()) | (outdf["OrganizationPhoneNumber"] == '') |
                           (outdf["OrganizationWebsite"].isnull()) | (outdf["OrganizationWebsite"] == '') |
                           (outdf["State"].isnull()) | (outdf["State"] == '')]


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/organizations.csv', index=False)

# Report purged values.
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('organizations_mandatoryFieldMissing.csv', index=False)

print("Done.")