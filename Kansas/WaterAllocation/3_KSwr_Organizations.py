#Date Created: 01/06/2021
#Purpose: To extract KS organization information and population dataframe for WaDE_QA 2.0.
#Notes:


# Needed Libraries
############################################################################
import pandas as pd
import numpy as np
import os


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Kansas/WaterAllocation"
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
    "KDADWR",
    "Ginger.Pugh@ks.gov",
    "Ginger Pugh",
    "https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/tree/master/Kansas",
    "The Kansas Department of Agriculture, Division of Water Resources",
    "785-564-6677",
    "The Division of Water Resources within the Kansas Department of Agriculture governs the use and allocation of the state's water resources.",
    "https://agriculture.ks.gov/home",
    "KS"]

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


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")
outdf.to_csv('ProcessedInputData/organizations.csv', index=False)

#Report missing values if need be to separate csv
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('organizations_mandatoryFieldMissing.csv', index=False)


print("Done.")