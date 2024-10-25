import pandas as pd

dfglobal = pd.read_csv("Classification/all_files_globalv1.csv")
dfza = pd.read_csv("Classification/all_files_ZAv1.csv")
dfskr = pd.read_csv("Classification/all_files_skrv1.csv")

dfskr=dfskr.drop_duplicates()

artistsbystreams = dfskr.groupby(["main_artist"])["streams"].sum()
artistsbystreamssorted = pd.DataFrame(artistsbystreams.sort_values(ascending=False))
artistsbystreamssorted=artistsbystreamssorted.reset_index()
artistsbystreamssorted.head(15)

groupname=["bts", "blackpink"]
groups = [["v", "jimin", "jin", 'jung kook', 'agust d', 'j-hope', 'rm'], ["jennie", 'jisoo', 'lisa', 'ros']]
dfskr['lower_main_artist'] = dfskr['main_artist'].apply(lambda x :x.lower())
idx = 1

rslt_df = dfskr[dfskr['lower_main_artist'].isin(groups[idx])]
rslt_df['main_artist'].unique().tolist()

rslt_df = rslt_df[rslt_df['main_artist'] != 'LiSA']

### Number of songs

rslt_df[["main_artist","track_name"]].drop_duplicates()

numsongsdf = pd.DataFrame(rslt_df.groupby(["main_artist","track_name"])["track_name"].count())
numsongsdf.columns = ["appearances"]
numsongsdf = numsongsdf.reset_index()
numsongscount = pd.DataFrame(numsongsdf.groupby(["main_artist"])["track_name"].count())
numsongscount.columns = ["num_songs"]
numsongscountdf = numsongscount.reset_index()

### Number of appearances

numappearancescount = pd.DataFrame(numsongsdf.groupby(["main_artist"])["appearances"].sum())
numappearancescountdf = numappearancescount.reset_index()

### Streams per artist
numstreamsdf = pd.DataFrame(rslt_df.groupby(["main_artist"])["streams"].sum())
numstreamsdf.columns = ["streams_sum"]
numstreamsdf = numstreamsdf.reset_index()

### Years on the chart

yrsonchartdf = pd.DataFrame(rslt_df.groupby(["main_artist"])["Year"].nunique())
yrsonchartdf.columns = ["yrsonchart"]
yrsonchartdf = yrsonchartdf.reset_index()

### Collaborators

def getcollaborators(x):
    collabs = x.split(",")[1:]
    
    if(len(collabs) == 0):
        collabs = ""
    
    return collabs

rslt_df["num_artists"] = rslt_df["artist_names"].apply(lambda x : len(x.split(",")))
rslt_df["num_collaborators"] = rslt_df["num_artists"].apply(lambda x : x-1)
rslt_df["collabs_artists"] = rslt_df["artist_names"].apply(lambda x : getcollaborators(x))
collabscountdf = rslt_df[["main_artist", "track_name", "num_collaborators"]].drop_duplicates()
collabscountdf = pd.DataFrame(collabscountdf.groupby(["main_artist"])["num_collaborators"].sum()).reset_index()

### FINAL DATAFRAME

numappandsongs = numappearancescountdf.merge(numsongscountdf, left_on=["main_artist"], right_on=["main_artist"], how="inner")
numappstreamssongs = numstreamsdf.merge(numappandsongs, left_on=["main_artist"], right_on=["main_artist"], how="inner")
numappstreamssongsyrs = numappstreamssongs.merge(yrsonchartdf, left_on=["main_artist"], right_on=["main_artist"], how="inner")
numappstreamssongsyrscollabs = numappstreamssongsyrs.merge(collabscountdf, left_on=["main_artist"], right_on=["main_artist"], how="inner")
numappstreamssongsyrs.to_csv("Classification/numappstreamssongsyrs" + groupname[idx] + ".csv", index=False)