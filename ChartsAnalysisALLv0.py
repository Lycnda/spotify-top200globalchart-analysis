import pandas as pd
import glob2
import matplotlib.pyplot as plt
import datetime
import re
from datetime import datetime, timedelta
import ChartsAnalysisALL_Functions


path_to_test_config1 = "configs/chartsanalysisparams.yml"
test_config1 = ChartsAnalysisALL_Functions.load_test_config(path_to_test_config1)
thelocalenames = test_config1["chartdetails"]["locales"]
read_enc_vals = test_config1["chartdetails"]["read_enc_val"]

# print(thelocalenames)
# ["kr", "za", "in", "global", "ng"]

print("STARTING THE RUN......................................................")

read_enc_val = read_enc_vals[0]

x = datetime.now()

thelogdetails = ""
thelogdetails = "The run datetime is: " + str(x)

for locale_name in thelocalenames:
    print("THE CURRENT CHART LOCALE RUNNING IS: ", str(locale_name))

    thelogdetails = thelogdetails + "THE CURRENT CHART LOCALE RUNNING IS: " + str(locale_name) + "\n"

    global_music_file_paths = glob2.glob('spotify ' + locale_name + ' v2/*.csv')

    thelogdetails = thelogdetails + " The number of files is: " + str(len(global_music_file_paths)) + "\n"
    print(len(global_music_file_paths))

    print(global_music_file_paths[:4])

    ChartsAnalysisALL_Functions.addsDatesToData(locale_name,global_music_file_paths)
    
    #### Add Dates to the Files
    
    #Combine the files and sort by dates
    all_files = []
    trouble_files = []
    for file in global_music_file_paths:
        the_data_in_file = pd.read_csv(file)
        
        if("URL" in list(the_data_in_file.columns)):
        
            the_data_in_file = the_data_in_file.drop(["URL"], axis=1)
        
        list_vals = sum(list(the_data_in_file.isnull().sum()))
        
        if(list_vals > 0):
            trouble_files.append(file)
        all_files.append(the_data_in_file)
        
    the_spotify_data = pd.concat(all_files) 
    # trouble_files_df = pd.concat(trouble_files)
    
    all_cols = list(the_spotify_data.columns)
    drop_cols = []
    
    for col in all_cols:
        if("Unnamed" in col or "artificial" in col):
            drop_cols.append(col)
            
    the_spotify_data.drop(drop_cols, axis=1, inplace = True)
    
    ### Error checking that all the Thursday dates are present
    date_list = the_spotify_data["End Date"].unique().tolist()
    # print(date_list)
    thelogdetails = thelogdetails + " The number of dates is: " + str(len(date_list)) + "\n"
    start_date = date_list[0]
    end_date = date_list[len(date_list)-1]
    
    # len(date_list)

    thelogdetails = thelogdetails + " The start dates is: " + str(start_date) + "." + " The end date is: " + str(end_date) + "\n"
    print("THE START AND END DATES ARE: ", start_date, end_date)

    result = ChartsAnalysisALL_Functions.check_thursdays_in_range(date_list, start_date, end_date)
    print("All Thursdays present:", result)
    thelogdetails = thelogdetails + " All Thursdays present: " + str(result) + "\n"
    
    ### Continue
    
    the_spotify_data["Week"] = the_spotify_data["End Date"].apply(lambda x : datetime.strptime(x, '%Y-%m-%d'))
    the_spotify_data["Year"] = the_spotify_data["Week"]
    
    the_spotify_data['Week'] = the_spotify_data['Week'].apply(lambda x : x.isocalendar()[1] )
    the_spotify_data['Year'] = the_spotify_data['Year'].apply(lambda x : x.isocalendar()[0] )
    
    # the_spotify_data["Start Date Dt"] = the_spotify_data["Start Date"].apply(lambda x : datetime.strptime(x, '%Y-%m-%d'))
    the_spotify_data["End Date Dt"] = the_spotify_data["End Date"].apply(lambda x : datetime.strptime(x, '%Y-%m-%d'))
    the_spotify_data['Seconds since Epoch'] = the_spotify_data['End Date Dt'].apply(lambda x : round(x.timestamp(), 0))


    the_spotify_data["End Date Aggregated"] = the_spotify_data["End Date"].apply(lambda x : ChartsAnalysisALL_Functions.changedaytotheFirst(x) )

    #find the number of artists on the track
    the_spotify_data.dropna(inplace=True)
    
    the_spotify_data["artist_names"] = the_spotify_data["artist_names"].apply(lambda x : x.encode("utf-8").decode("latin-1"))
    the_spotify_data["artist_names"] = the_spotify_data["artist_names"].apply(lambda x : re.sub(r'[^\x00-\x7F]+','', x))
    the_spotify_data["artist_names"] = the_spotify_data.apply(lambda x : x["artist_names"] + "Artist_NA" if(x["artist_names"] == "") else x["artist_names"], axis=1)
    
    the_spotify_data["track_name"] = the_spotify_data["track_name"].apply(lambda x : x.encode("utf-8").decode("latin-1"))
    the_spotify_data["track_name"] = the_spotify_data["track_name"].apply(lambda x : re.sub(r'[^\x00-\x7F]+','', x))
    the_spotify_data["track_name"] = the_spotify_data.apply(lambda x : x["artist_names"] + "_NA" if(x["track_name"] == "") else x["track_name"], axis=1)

    the_spotify_data['ArtistCount'] = the_spotify_data['track_name'].apply(lambda x : ChartsAnalysisALL_Functions.countNumberArtists(x))

    print(the_spotify_data.shape)
    
    the_spotify_data["main_artist"] = the_spotify_data.apply(lambda x : x["artist_names"].split(",")[0], axis=1)
    
    the_spotify_data = the_spotify_data.reset_index()
    the_spotify_data.drop(["index"], axis=1, inplace=True)
    
    print(the_spotify_data.shape)

    the_spotify_data = the_spotify_data[~the_spotify_data.index.duplicated()]
    the_spotify_data = the_spotify_data.groupby(["artist_names", "track_name"]).apply(lambda x : ChartsAnalysisALL_Functions.everInTopTen(x))
    
    # the_spotify_data.head()
    
    ### When did the track reach the Top 10 
    
    ### how long does a song last on the charts?
    
    # the_spotify_data["isTopTen"].value_counts()
    
    # the_spotify_data.isnull().sum()
    
    unique_artists = the_spotify_data["main_artist"].unique().tolist()
    num_artists = len(unique_artists)
    print("THE NUM OF ARTISTS: ", num_artists)
    thelogdetails = thelogdetails + " The number of artists in the data: " + str(num_artists) + "\n"

    the_spotify_data = the_spotify_data.drop(['artist_names', 'track_name'], axis=1)
    the_spotify_data =the_spotify_data.groupby(["main_artist"], as_index=False).apply(lambda x : ChartsAnalysisALL_Functions.getArtistAppearanceCount(x))
    the_spotify_data.drop(["level_2"], inplace=True, axis=1)
    

    the_spotify_data =the_spotify_data.groupby(["artist_names", "track_name"], as_index=False).apply(lambda x : ChartsAnalysisALL_Functions.getTrackAppearanceCount(x))
    # the_spotify_data = the_spotify_data.reset_index()
    the_spotify_data.drop(["level_0", "level_1"], inplace=True, axis=1)
    # print(the_spotify_data.columns)
    # stop
    
    # the_spotify_data.head()
    
    # the_spotify_data.to_csv("the_spotify_data_" + locale_name+ ".csv", index=False)
    
    the_spotify_data["rank"] = the_spotify_data["rank"].astype(int)
    the_spotify_data["streams"] = the_spotify_data["streams"].astype(int)
    the_spotify_data["ArtistCount"] = the_spotify_data["ArtistCount"].astype(int)
    
    the_spotify_data["isTopTen"] = the_spotify_data["isTopTen"].astype(int)
    # the_spotify_data["lenOnCharts"] = the_spotify_data["lenOnCharts"].astype(int)
    the_spotify_data["Year"] = the_spotify_data["Year"].astype(int)
    the_spotify_data["Week"] = the_spotify_data["Week"].astype(int)
    
    all_cols = list(the_spotify_data.columns)
    drop_cols = []
    
    for col in all_cols:
        if("Unnamed" in col or "artificial" in col):
            drop_cols.append(col)
            
    the_spotify_data.drop(drop_cols, axis=1, inplace = True)
    
    the_spotify_data["Artist and Track"] = the_spotify_data["artist_names"] + "; " + the_spotify_data["track_name"]
    
    ### Getting the list of Artists and Tracks
    all_files_grouped = the_spotify_data.groupby(["main_artist", "track_name"]).apply(lambda x: ChartsAnalysisALL_Functions.trackAppearance(x))
    
    # all_files_grouped["rank difference"].max()

    all_files_grouped["Position over Time"] = all_files_grouped.apply(lambda x : ChartsAnalysisALL_Functions.positionvertime(x), axis=1)

    ##### Add a Girl Group and Boy Group
    
    ggdf = pd.read_csv("Classification/ListofGirlGroups.csv", encoding='ANSI')
    bgdf = pd.read_csv("Classification/ListofBoyGroups.csv", on_bad_lines='skip', encoding='ANSI')
    mgdf = pd.read_csv("Classification/ListofMixedGroups.csv", on_bad_lines='skip', encoding='ANSI')

    all_files_grouped["IsGirlGroup"] = all_files_grouped["main_artist"].apply(lambda x : ChartsAnalysisALL_Functions.IsGG(ggdf, x))
    all_files_grouped["IsBoyGroup"] = all_files_grouped["main_artist"].apply(lambda x : ChartsAnalysisALL_Functions.IsGG(bgdf, x))
    all_files_grouped["IsMixedGroup"] = all_files_grouped["main_artist"].apply(lambda x : ChartsAnalysisALL_Functions.IsGG(mgdf, x))
    
    ggs = all_files_grouped[all_files_grouped["IsGirlGroup"]==True]["main_artist"].unique().tolist()
    bgs = all_files_grouped[all_files_grouped["IsBoyGroup"]==True]["main_artist"].unique().tolist()
    

    split_df = all_files_grouped['artist_names'].str.split(',', expand=True)

    all_files_grouped_df = pd.concat([all_files_grouped, split_df], axis=1).drop('artist_names', axis=1)

    all_files_grouped_df = all_files_grouped_df.fillna("")

    # Dictionary for renaming: {'old_name': 'new_name'}
    rename_mapping = {
        1: 'artist_1',
        2: 'artist_2',
        3: 'artist_3',
        4: 'artist_4',
        5: 'artist_5',
        6: 'artist_6',
        7: 'artist_7',
        8: 'artist_8',
        9: 'artist_9',
        10: 'artist_10',
    }

    # Rename the columns
    # Use inplace=True to modify the original DataFrame
    all_files_grouped_df.rename(columns=rename_mapping, inplace=True)


    print(all_files_grouped.columns)
    print("the output path......", "Classification/all_files_"+locale_name+"v1.csv")
    all_files_grouped_df.to_csv("Classification/all_files_"+locale_name+"v1.csv", index=False)
    thelogdetails = thelogdetails + " The output data written to this file: " + "Classification/all_files_"+locale_name+"v1.csv" + "\n"
    with open("Classification/Spotify_Logs.txt", "a") as f:
        f.write(thelogdetails)

    ### South African Artists

    all_files_grouped_df.shape
    
    all_files_grouped_df.columns
    
    print("DONE.")