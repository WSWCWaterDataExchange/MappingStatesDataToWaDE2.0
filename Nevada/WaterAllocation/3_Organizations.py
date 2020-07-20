#Date Created: 07/17/2020
#Purpose: To extract NV organization use information and population dataframe for WaDE_QA 2.0.
#Notes: 1) No input csv to read, all values are more easily hardcoded into a list here and then exported to CSV.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading inputs...")
workingDir="/Users/augustus/Desktop/WSWC/WaDE/MappingStatesDataToWaDE2.0/Nevada/WaterAllocation/"
os.chdir(workingDir)

# Needed WaDE columns
columns = [
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
    "NVDWR",
    "bmcmenamy@nv.water.gov",
    "Brian McMenamy",
    "https://ndwr.maps.arcgis.com/home/item.html?id=0d050f7b79724404b80bf29589f67363",
    "Nevada Division of Water Resources",
    "(775) 684-2800",
    "The Nevada Division of Water Resources manages Nevada's water resources for the state.",
    "http://water.nv.gov/index.aspx",
    "NV"]

outdf = pd.DataFrame([inpVals], columns=columns)


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