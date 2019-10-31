#!/usr/bin/env python
import pandas as pd
import numpy as np
import os

workingDir="C:/Users/gdg12/Desktop/WaDE2.0/UtahCSVs/Test"
os.chdir(workingDir)

fileInput="Water_Master.csv"
allocCSV="UTWaterAllocations.csv"

varCSV="UtahOrganizations.csv"

##OR read csv
df100 = pd.read_csv(fileInput)
#df100 = df.head(100)

print("Columns...")
#WaDE columns
columns=['OrganizationUUID', 'OrganizationName', 'OrganizationPurview', 'OrganizationWebsite',
         'OrganizationPhoneNumber', 'OrganizationContactName', 'OrganizationContactEmail', 'DataMappingURL']
dtypesx = ['']
#assumes dtypes inferred from CO file

inpVals = ['UTDWRE', 'Utah Division of Water Resources', 'Water Planning', 'Water Planning', '8015387280', 'Craig Miller', 'craigmiller@utah.gov', 'https://github.com/WSWCWaterDataExchange/WaDE2.0']
outdf100 = pd.DataFrame([inpVals], columns=columns)

"""
outdf100=pd.DataFrame(columns=columns)

# #hardcoded
outdf100.OrganizationUUID = 'UTDWRE'
outdf100.OrganizationName = 'Utah Division of Water Resources'
outdf100.OrganizationPurview = 'Water Planning'
outdf100.OrganizationWebsite = 'Water Planning'
outdf100.OrganizationPhoneNumber = '8015387280'
outdf100.OrganizationContactName = 'Craig Miller'
outdf100.OrganizationContactEmail = 'craigmiller@utah.gov'
outdf100.DataMappingURL = 'https://github.com/WSWCWaterDataExchange/WaDE2.0'
"""

print("Check required is not null...")
#9.9.19: Adel: check all 'required' (not NA) columns have value (not empty)
requiredCols=['OrganizationUUID', 'OrganizationName', 'OrganizationPurview', 'OrganizationWebsite',
         'OrganizationPhoneNumber', 'OrganizationContactName', 'OrganizationContactEmail', 'DataMappingURL']
#replace blank strings by NaN, if there are any
outdf100 = outdf100.replace('', np.nan)
#any cell of these columns is null
#outdf100_nullMand = outdf100.loc[outdf100.isnull().any(axis=1)] --for all cols
outdf100_nullMand = outdf100.loc[(outdf100["OrganizationUUID"].isnull()) |
                                (outdf100["OrganizationName"].isnull()) | (outdf100["OrganizationPurview"].isnull()) |
                                (outdf100["OrganizationWebsite"].isnull()) | (outdf100["OrganizationPhoneNumber"].isnull()) |
                                (outdf100["OrganizationContactName"].isnull()) | (outdf100["OrganizationContactEmail"].isnull()) |
                                (outdf100["DataMappingURL"].isnull())
                                 ]
#outdf100_nullMand = outdf100.loc[[False | (outdf100[varName].isnull()) for varName in requiredCols]]
if(len(outdf100_nullMand.index) > 0):
    outdf100_nullMand.to_csv('variables_mandatoryFieldMissing.csv')  # index=False,
#ToDO: purge these cells if there is any missing? #For now left to be inspected

print("Write out...")
# save to output
outdf100.to_csv(varCSV, index=False)

print("Done variables")