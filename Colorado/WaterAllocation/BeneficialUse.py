#!/usr/bin/env python
import pandas as pd
from sodapy import Socrata
import os

workingDir="C:/Tseganeh/0WaDE/"
os.chdir(workingDir)

fileInput="DWR_Water_Right_-_Net_Amounts.csv"
BenUseCSV="BeneficialUse.csv"

#from https://dev.socrata.com/foundry/data.colorado.gov/a8zw-bjth
# client = Socrata("data.colorado.gov", None)
# top100 = client.get("a8zw-bjth", limit=100)
# df = pd.DataFrame.from_records(top100)
#or read csv
df = pd.read_csv(fileInput)
df100 = df.head(100)

"""
Comment from Adel 
we get unique water source based on combination of ID, name, and source type, water quailty indicator
"""

#WaDE columns

primKey=''

columns=['BeneficialUseCategoryID', 'BeneficialUseCategory', 'PrimaryUseCategory', 'USGSCategoryNameCV', 'NAICSCodeNameCV']

dtypesx = []

#assumes dtypes inferred from CO file
outdf100=pd.DataFrame(columns=columns)

benUseDict = {
    "0":"STORAGE",
    "1":"IRRIGATION",
    "2":"MUNICIPAL",
    "3":"COMMERCIAL",
    "4":"INDUSTRIAL",
    "5":"RECREATION",
    "6":"FISHERY",
    "7":"FIRE",
    "8":"DOMESTIC",
    "9":"STOCK",
    "A":"AUGMENTATION",
    "B":"EXPORT FROM BASIN",
    "C":"CUMULATIVE ACCRETION TO RIVER",
    "D":"CUMULATIVE DEPLETION FROM RIVER",
    "E":"EVAPORATIVE",
    "F":"FEDERAL RESERVED",
    "G":"GEOTHERMAL",
    "H":"HOUSEHOLD USE ONLY",
    "K":"SNOW MAKING",
    "M":"MINIMUM STREAMFLOW",
    "N":"NET EFFECT ON RIVER",
    "P":"POWER GENERATION",
    "Q":"OTHER",
    "R":"RECHARGE",
    "S":"EXPORT FROM STATE",
    "T":"TRANSMOUNTAIN EXPORT",
    "W":"WILDLIFE",
    "X":"ALL BENEFICIAL USES"
}

#existing corresponding fields
#outdf100.WaterSourceNativeID = df100.WDID
#benUseList= df100['Decreed Uses']
#print (benUseList)
outdf100.BeneficialUseCategoryID = df100['Decreed Uses']
# find no-loop approach
for ix in range(len(outdf100.index)):
    benUseListStr = outdf100.loc[ix, 'BeneficialUseCategoryID']
    outdf100.BeneficialUseCategory[ix] = ",".join(benUseDict[inx] for inx in list(str(benUseListStr)))         #map(lambda x: x, benUseListStr))


#outdf100.PrimaryUseCategory
#outdf100.USGSCategoryNameCV
#outdf100.NAICSCodeNameCV

#outdf100.rename_axis(indxx)

outdf100.to_csv(BenUseCSV)     #index=False,


"""" 
dtype = ['str', 'str', 'str', 'str', 'int', 'float', 'float', 'int', 'float']
df = pd.concat([pd.Series(name=col, dtype=dt) for col, dt in zip(columns, dtype)], axis=1)
df.info()

dtypes = numpy.dtype([
          ('a', str),
          ('b', int),
          ('c', float),
          ('d', numpy.datetime64),
          ])
data = numpy.empty(0, dtype=dtypes)
df = pandas.DataFrame(data)

def df_empty(columns, dtypes, index=None):
    assert len(columns)==len(dtypes)
    df = pd.DataFrame(index=index)
    for c,d in zip(columns, dtypes):
        df[c] = pd.Series(dtype=d)
    return df

df = df_empty(['a', 'b'], dtypes=[np.int64, np.int64])
print(list(df.dtypes)) # int64, int64


from https://dev.socrata.com/foundry/data.colorado.gov/a8zw-bjth

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.colorado.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.colorado.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("a8zw-bjth", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
"""