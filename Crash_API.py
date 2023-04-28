#Importing relevant libraries
import ckanapi
import calendar
import pandas as pd

#The main site
site = "https://data.wprdc.org"

#Defining the functiong to fetch complete data (This was given in the API documentation)
def get_resource_data(site,resource_id,count=50):
    ckan = ckanapi.RemoteCKAN(site)
    response = ckan.action.datastore_search(id=resource_id, limit=count)
    data = response['records']
    return data

#Fetching the data
crash_data_2018 = get_resource_data(site,resource_id="48f30bee-e404-4cf5-825b-b0da3c975e45",count=999999999) 

#Data cleaning

##Reading the data into df
df = pd.DataFrame(crash_data_2018)

## Removing unnecessary columns and null rows
cols_to_keep = ["_id","CRASH_COUNTY","CRASH_MONTH","DAY_OF_WEEK","FATAL_COUNT","FATAL_OR_MAJ_INJ","HOUR_OF_DAY","ICY_ROAD","INJURY","INJURY_COUNT","INJURY_OR_FATAL","MAJ_INJ_COUNT","MAJOR_INJURY","MIN_INJ_COUNT","MINOR_INJURY","MOD_INJ_COUNT","MODERATE_INJURY","TIME_OF_DAY","TOT_INJ_COUNT","WEATHER","WET_ROAD"]
df.drop(columns=[col for col in df.columns if col not in cols_to_keep], inplace=True)
df = df[~df['_id'].isin([5238,9157,9349])]
df.dropna(inplace=True)

##Reordering rows and columns
df = df.sort_index(axis=1)
df = df.sort_values('_id')
col = df.pop('_id')
df.insert(0, '_id', col)

##Extracting hour
df['HOUR_OF_DAY'] = df['TIME_OF_DAY'].astype(str).str.zfill(4).str[:2].astype(int)
df = df[df['TIME_OF_DAY'] != '9999']

##Coverting all the possible strings to int
def convert_to_int(x):
    if isinstance(x, int):
        return x
    elif isinstance(x, str) and x.isdigit():
        return int(x)
    elif x == '0n':
        return None
    else:
        return x
df = df.applymap(convert_to_int)

##Converting the month and day number to their names
month_map = {i: calendar.month_name[i] for i in range(1, 13)}
df['CRASH_MONTH'] = df['CRASH_MONTH'].apply(lambda x: month_map[x] if pd.notna(x) else x)

day_map = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday', 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
df['DAY_OF_WEEK'] = df['DAY_OF_WEEK'].map(day_map)

#Writing the clean data into an csv file
df.to_csv('Crashdata.csv', index=True)
