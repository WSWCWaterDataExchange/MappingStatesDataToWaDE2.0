# Date Created: 08/12/2021
# Purpose: To extract NM organization information and populate dataframe for WaDE_QA 2.0.
# Notes: asdf


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/NewMexico/Regulatory"
os.chdir(workingDir)

# Needed WaDE columns
columnslist = [
    "OrganizationUUID",
    "OrganizationContactEmail",
    "OrganizationContactName",
    "OrganizationDataMappingURL",
    "OrganizationName",
    "OrganizationPhoneNumber",
    "OrganizationPurview",
    "OrganizationWebsite",
    "State"]


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")

outdf = pd.DataFrame(columns=columnslist)
outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.OrganizationUUID = "NMOSE"

outdf.OrganizationContactEmail = "ose.webmaster@state.nm.us"

outdf.OrganizationContactName = "David Hatchner (GIS Manager)"

outdf.OrganizationDataMappingURL = "https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/NewMexico"

outdf.OrganizationName = "New Mexico Office of the State Engineer"

outdf.OrganizationPhoneNumber = "505-827-3846"

outdf.OrganizationPurview = "The New Mexico Office of the State Engineer (OSE) provides this geographic data and any associated metadata as is without warranty of any kind."

outdf.OrganizationWebsite = "https://www.ose.state.nm.us/"

outdf.State = "NM"


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
