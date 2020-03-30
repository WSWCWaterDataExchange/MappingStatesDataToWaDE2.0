#Date Created: 03/13/2020
#Purpose: To extract UT organization use information and population dataframe for WaDE_QA 2.0.
#Notes: 1) No input csv to read, all values are more easily hardcoded into a list here and then exported to CSV.


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading inputs...")
workingDir="C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Utah/WaterAllocation"
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
    "UTDWRE",
    "craigmiller@utah.gov",
    "Craig Miller",
    "https://github.com/WSWCWaterDataExchange/WaDE2.0",
    "Utah Division of Water Resources",
    "801-538-7280",
    "Water Planning",
    "https://water.utah.gov/",
    "UT"]

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