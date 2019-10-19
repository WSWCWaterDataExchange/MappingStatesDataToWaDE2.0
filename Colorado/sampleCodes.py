

%% timeit
for ix in range(len(df100.index)):
    #print(ix)
    df100.loc[ix, 'SiteUUID'] = "_".join(["UTDWRE",str(df100.loc[ix, 'RECORD_ID'])])
df100['SiteUUID']

%% timeit
siteuuidSer = []
for index, row in df100.iterrows():
    #print(ix)
    siteuuidSer.append("_".join(["UTDWRE", str(row['RECORD_ID'])]))
    # df100.loc[ix, 'SiteUUID'] = "_".join(["UTDWRE",str(df100.loc[ix, 'RECORD_ID'])])
df100['SiteUUID'] = siteuuidSer
df100['SiteUUID']

%% timeit
df100['SiteUUID'] = df100.apply(lambda row: "_".join(["UTDWRE", str(row['RECORD_ID'])]), axis=1)
df100['SiteUUID']

%% timeit
df100['SiteUUID'] = "_".join(["UTDWRE", str(df100['RECORD_ID'])])
df100['SiteUUID']

%% timeit
df100['SiteUUID'] = "_".join(["UTDWRE", str(df100['RECORD_ID'].values)])
df100['SiteUUID']

