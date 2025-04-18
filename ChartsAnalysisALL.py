import pandas as pd
import glob2
import matplotlib.pyplot as plt
import datetime
import re
from datetime import datetime, timedelta

read_enc_val ="ISO-8859-1"
read_enc_val ="cp1252"
read_enc_val ="utf-8"

thelocalenames = ["kr", "za", "in", "global", "ng"]
thelocalenames = ["kr"]

x = datetime.now()

thelogdetails = ""
thelogdetails = "The run datetime is: " + str(x)

#Add the dates to the files - run once
def addsDatesToData(locale_name):   
    to_remove_front = "spotify " +locale_name+ " v2\\regional-" +locale_name+"-weekly-"
    to_remove_back = ".csv"

    len_front_remove = len(to_remove_front)
    len_back_remove = len(to_remove_back)

    print("len to remove front", len_front_remove)
    print("len to remove back", len_back_remove)

    for file in global_music_file_paths: 
        the_data_in_file = pd.read_csv(file)        
        
        the_dates = file[len_front_remove:]
        the_dates = the_dates[:-len_back_remove]

        split_dates = the_dates.split("-")

        start_date = split_dates[0] + "-" + split_dates[1] + "-" + split_dates[2]
        

        len_dates = the_data_in_file.shape[0]
        start_dates = len_dates * [start_date]

        date_columns = {"End Date": start_dates}   

        the_data_in_file["End Date"] = start_dates

        #write the data back to the File
        the_data_in_file.to_csv(file, index=False)
        
#remove dates in existing files
def removeExistingDates():
    for file in global_music_file_paths:
        
        the_data_in_file = pd.read_csv(file)

        the_data_in_file.drop(["Start Date", "End Date"], axis=1, inplace=True) 

        the_data_in_file.to_csv(file, index=False)

def check_thursdays_in_range(date_list, start_date, end_date):
    # Convert start_date and end_date strings to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Initialize a set to store Thursdays in the range
    thursdays_in_range = set()
    
    # Iterate through the range of dates and add Thursdays to the set
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 3:  # Thursday
            thursdays_in_range.add(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    # Convert date_list to a set for efficient membership checking
    date_set = set(date_list)
    
    # Find missing Thursdays
    missing_thursdays = sorted(thursdays_in_range - date_set)
    print("thursdays_in_range: ", len(thursdays_in_range))
    print("date_set: ", len(date_set))
    
    if missing_thursdays:
        print("Missing Thursdays in the range:")
        print("len Missing thursdays in range: ", len(missing_thursdays))
        for thursday in missing_thursdays:
            print(thursday)
        return False
    else:
        print("All Thursdays are present in the range.")
        return True

#get the month when this happened
def changedaytotheFirst(x):
    x = x[:-2] + "01"
    
    return x

def countNumberArtists(x):
    len_all_featured_artists = 0
    num_artists = 0
    xvals = x.split("feat")
    len_xvals = len(xvals)
    
    if(len_xvals > 1):
        featured_artists = xvals[1:]
        featured_artists_str = ' '.join(featured_artists)
        all_featured_artists = featured_artists_str.split("& ")
        len_all_featured_artists = len(all_featured_artists)
        
    num_artists = 1 + len_all_featured_artists
    
    return num_artists
        
### Is Top Ten Status

def everInTopTen(x):
    position_vals = list(x["rank"])
    position_vals = list(set(position_vals))
    
#     print(position_vals)
    
    min_pos = min(position_vals)
    existence_val = 0
    
    if(min_pos <= 10):
        existence_val = 1
    
    x["isTopTen"] = [existence_val] * len(x)
    
    return x
    

### find new artists in that week
def getArtistAppearanceCount(x):

    x = x.sort_values(by='End Date', ascending=True)
    x = x.reset_index()
    # x.drop(["index"],axis=1,inplace=True)
    x = x.reset_index()
    
    x_cols = [w.replace('index', 'artistAppearanceCount') for w in x.columns]
    
    x.columns = x_cols
    
    return x        

#### Track Appearance Count
def getTrackAppearanceCount(x):

    x = x.sort_values(by=['End Date','track_name'], ascending=True)

    x = x.reset_index()
    # x.drop(["index"],axis=1,inplace=True)
    x = x.reset_index()
    
    x_cols = x.columns
    
    x_cols = [w.replace('index', 'trackAppearanceCount') for w in x_cols]
    
    x.columns = x_cols
    
    return x         
    
def trackAppearance(x):
    x = x.sort_values(by=["End Date"])

    x["rank"] = x["rank"].astype(int)
    
    x["rank difference"] = x["rank"].diff().fillna(0)
    x["rank difference"] = x["rank difference"].astype(int)
    
    return x
    
### Position over time

def positionvertime(x):
    posovertime = 0
    #new track
    if(x["rank difference"] == 0 and x["trackAppearanceCount"]==0):
        posovertime = 0
    #track stayed in the same position
    elif(x["rank difference"] == 0 and x["trackAppearanceCount"]!=0):
        posovertime = 50
    #track went up the chart
    elif(x["rank difference"] < 0):
        posovertime = 75
    #track fell down the chart
    else:
        posovertime = 100
    return posovertime



def IsGG(ggdf, y):
    ggs = [x.lower().strip() for x in ggdf["Artist"]]
    y = y.lower().strip()
    
    if y in ggs:
        return True
    else:
        return False

def IsBG(bgdf, y):
    bgs = [x.lower().strip() for x in bgdf["Artist"]]
    y = y.lower().strip()
    
    if y in bgs:
        return True
    else:
        return False




def newstuff(x):
#     x = x.reset_index()

    x = x.sort_values(by=['Seconds since Epoch'])
#     x.set_index(["Position"])
    print(x)
    
    return x

# 604800
def weekonweekposition(x):
    
#     print(x.values)
    
    pd.DataFrame({'email':x.index, 'list':x.values})

for locale_name in thelocalenames:

    thelogdetails = thelogdetails + "The chart locale is: " + str(locale_name) + "\n"

    global_music_file_paths = glob2.glob('spotify ' + locale_name + ' v2/*.csv')

    thelogdetails = thelogdetails + " The number of files is: " + str(len(global_music_file_paths)) + "\n"
    print(len(global_music_file_paths))

    print(global_music_file_paths[:4])

    addsDatesToData(locale_name)
    
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
    print(date_list)
    thelogdetails = thelogdetails + " The number of dates is: " + str(len(date_list)) + "\n"
    start_date = date_list[0]
    end_date = date_list[len(date_list)-1]
    
    len(date_list)

    thelogdetails = thelogdetails + " The start dates is: " + str(start_date) + "." + " The end date is: " + str(end_date) + "\n"
    print(start_date, end_date)

    result = check_thursdays_in_range(date_list, start_date, end_date)
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


    the_spotify_data["End Date Aggregated"] = the_spotify_data["End Date"].apply(lambda x : changedaytotheFirst(x) )

    #find the number of artists on the track
    the_spotify_data.dropna(inplace=True)
    
    the_spotify_data["artist_names"] = the_spotify_data["artist_names"].apply(lambda x : x.encode("utf-8").decode("latin-1"))
    the_spotify_data["artist_names"] = the_spotify_data["artist_names"].apply(lambda x : re.sub(r'[^\x00-\x7F]+','', x))
    the_spotify_data["artist_names"] = the_spotify_data.apply(lambda x : x["artist_names"] + "Artist_NA" if(x["artist_names"] == "") else x["artist_names"], axis=1)
    
    the_spotify_data["track_name"] = the_spotify_data["track_name"].apply(lambda x : x.encode("utf-8").decode("latin-1"))
    the_spotify_data["track_name"] = the_spotify_data["track_name"].apply(lambda x : re.sub(r'[^\x00-\x7F]+','', x))
    the_spotify_data["track_name"] = the_spotify_data.apply(lambda x : x["artist_names"] + "_NA" if(x["track_name"] == "") else x["track_name"], axis=1)

    the_spotify_data['ArtistCount'] = the_spotify_data['track_name'].apply(lambda x : countNumberArtists(x))

    print(the_spotify_data.shape)
    
    the_spotify_data["main_artist"] = the_spotify_data.apply(lambda x : x["artist_names"].split(",")[0], axis=1)
    
    the_spotify_data = the_spotify_data.reset_index()
    the_spotify_data.drop(["index"], axis=1, inplace=True)
    
    print(the_spotify_data.shape)

    the_spotify_data = the_spotify_data[~the_spotify_data.index.duplicated()]
    the_spotify_data = the_spotify_data.groupby(["artist_names", "track_name"]).apply(lambda x : everInTopTen(x))
    
    # the_spotify_data.head()
    
    ### When did the track reach the Top 10 
    
    ### how long does a song last on the charts?
    
    the_spotify_data["isTopTen"].value_counts()
    
    # the_spotify_data.isnull().sum()
    
    unique_artists = the_spotify_data["main_artist"].unique().tolist()
    num_artists = len(unique_artists)
    print(num_artists)
    thelogdetails = thelogdetails + " The number of artists in the data: " + str(num_artists) + "\n"

    the_spotify_data = the_spotify_data.drop(['artist_names', 'track_name'], axis=1)
    the_spotify_data =the_spotify_data.groupby(["main_artist"], as_index=False).apply(lambda x : getArtistAppearanceCount(x))
    the_spotify_data.drop(["level_2"], inplace=True, axis=1)
    

    the_spotify_data =the_spotify_data.groupby(["artist_names", "track_name"], as_index=False).apply(lambda x : getTrackAppearanceCount(x))
    # the_spotify_data = the_spotify_data.reset_index()
    the_spotify_data.drop(["level_0", "level_1"], inplace=True, axis=1)
    # print(the_spotify_data.columns)
    # stop
    
    # the_spotify_data.head()
    
    the_spotify_data.to_csv("the_spotify_data_" + locale_name+ ".csv")
    
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
    all_files_grouped = the_spotify_data.groupby(["main_artist", "track_name"]).apply(lambda x: trackAppearance(x))
    
    # all_files_grouped["rank difference"].max()

    all_files_grouped["Position over Time"] = all_files_grouped.apply(lambda x : positionvertime(x), axis=1)

    ##### Add a Girl Group and Boy Group
    
    ggdf = pd.read_csv("Classification/ListofGirlGroups.csv", encoding='ANSI')
    bgdf = pd.read_csv("Classification/ListofBoyGroups.csv", on_bad_lines='skip', encoding='ANSI')

    all_files_grouped["IsGirlGroup"] = all_files_grouped["main_artist"].apply(lambda x : IsGG(ggdf, x))
    all_files_grouped["IsBoyGroup"] = all_files_grouped["main_artist"].apply(lambda x : IsGG(bgdf, x))
    
    ggs = all_files_grouped[all_files_grouped["IsGirlGroup"]==True]["main_artist"].unique().tolist()
    bgs = all_files_grouped[all_files_grouped["IsBoyGroup"]==True]["main_artist"].unique().tolist()
    
    print(all_files_grouped.columns)
    all_files_grouped.to_csv("Classification/all_files_"+locale_name+"v1.csv", index=False)
    thelogdetails = thelogdetails + " The output data written to this file: " + "Classification/all_files_"+locale_name+"v1.csv" + "\n"
    with open("Classification/Spotify_Logs.txt", "a") as f:
        f.write(thelogdetails)

    ### South African Artists

    all_files_grouped.shape
    
    all_files_grouped.columns
    
    narrowing_df = all_files_grouped[['End Date', "rank difference"]]
    
    narrowing_df.reset_index(inplace=True)
    
    # narrowing_df.drop(["level_2"], axis=1, inplace=True)
    
    narrowing_df = narrowing_df[narrowing_df["rank difference"] == 0]
    
    print("DONE.")