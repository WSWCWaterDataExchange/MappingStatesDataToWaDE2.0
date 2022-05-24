# Last Updated: 05/17/2022
# Purpose: To create NJ site specific organization use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) No input csv to read, all values are more easily hardcoded into a list here and then exported to CSV.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/NewJersey/SiteSpecificAmounts"
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

outdf.OrganizationUUID = "NJss_O1"

outdf.OrganizationContactEmail = "Steven.Domber@dep.nj.gov, Kent.Barr@dep.nj.gov"

outdf.OrganizationContactName = "Steven Domber, Kent Barr"

outdf.OrganizationDataMappingURL = "https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/NewJersey"

outdf.OrganizationName = "New Jersey Division of Water Supply and Geoscience"

outdf.OrganizationPhoneNumber = "(609) 984-6587"

outdf.OrganizationPurview = "Unspecified"

outdf.OrganizationWebsite = "https://www.nj.gov/dep/watersupply/"

outdf.State = "NJ"


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
