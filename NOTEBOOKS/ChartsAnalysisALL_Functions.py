import pandas as pd
import glob2
import matplotlib.pyplot as plt
import datetime
import re
from datetime import datetime, timedelta
import yaml


#Add the dates to the files - run once
def addsDatesToData(locale_name,global_music_file_paths):   
    to_remove_front = "../" + "spotify " +locale_name+ " v2\\regional-" +locale_name+"-weekly-"
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
def removeExistingDates(global_music_file_paths):
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

def load_test_config(path_to_config):
    """
    Load a yaml file as the test config.
    """
    
    with open(path_to_config, 'r') as stream:
        
        parsed_yaml=yaml.safe_load(stream)
        
    return parsed_yaml