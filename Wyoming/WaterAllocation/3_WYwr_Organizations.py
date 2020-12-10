#Date Created: 12/01/2020
#Purpose: To extract AZ organization information and population dataframe for WaDE_QA 2.0.
#Notes: asdf


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Arizona/WaterAllocation"
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
inpVals = [
    "ADWR",
    "lmwilliams@azwater.gov",
    "Lisa Williams",
    "https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Arizona",
    "Arizona Department of Water Resources",
    "602-771-8500",
    "The Arizona Department of Water Resources is the steward of Arizona’s water future and ensures long-term, reliable water supplies to support the continued economic prosperity of the State.",
    "http://gisdata-azwater.opendata.arcgis.com/",
    "AZ"]

outdf = pd.DataFrame([inpVals], columns=columnslist)


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

if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('organizations_mandatoryFieldMissing.csv')  # index=False,


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")
# save to output
outdf.to_csv('ProcessedInputData/organizations.csv', index=False)


print("Done.")