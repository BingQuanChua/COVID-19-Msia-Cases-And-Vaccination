import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
import vincent as v
v.core.initialize_notebook()

def get_coordinates(address):    
    try:
        geolocator = Nominatim(user_agent="http")
        location = geolocator.geocode(address)
        return [location[-1][0], location[-1][1]]
    except:
        print(f'Oops! No coordinates found for: {address}')
        return [None, None]
def change_col_dt(df):
    new_df = df.T.copy()
    new_df.index =  pd.to_datetime(new_df.index)
    return new_df.T.copy()

def import_data_JHU():
    # url to the data 'Novel Coronavirus (COVID-19) Cases', provided by JHU CSSE
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

    # confirmed cases and deaths worldwide for each country
    cases = pd.read_csv(url + 'time_series_covid19_confirmed_global.csv')
    deaths = pd.read_csv(url + 'time_series_covid19_deaths_global.csv')

    # we sum over Province/State for countries (US = Alabama, Alaska,..)
    cases = cases.groupby('Country/Region', axis=0).sum()
    deaths = deaths.groupby('Country/Region', axis=0).sum()
    #group Italy and San Marino:
    cases.loc['Italy'] = cases.loc['Italy'] + cases.loc['San Marino']
    cases.drop(['San Marino'],inplace=True)
    cases.rename(index={'United Kingdom': 'UK'}, inplace=True)
    deaths.loc['Italy'] = deaths.loc['Italy'] + deaths.loc['San Marino']
    deaths.drop(['San Marino'],inplace=True)
    deaths.rename(index={'United Kingdom': 'UK'}, inplace=True)

    # Some cleaning of the data:
    last_day = cases.columns[-1]
    cases.sort_values( [last_day], ascending=False,
                       axis=0, inplace=True)      # ordering by total number of latest point
    deaths = deaths.reindex(index=cases.index)    # same ordering as cases

    cases.index.name = None                       # delete the name of the index
    deaths.index.name = None

    # delete the following rows from the data
    to_del = ['Diamond Princess', 'MS Zaandam', 'Holy See', 'Western Sahara']
    cases = cases.drop(to_del)
    deaths = deaths.drop(to_del)

    new_df = deaths.iloc[:,2:].T.copy()
    new_df.index =  pd.to_datetime(new_df.index)
    deaths = new_df.T.copy()

    new_df = cases.iloc[:,2:].T.copy()
    new_df.index =  pd.to_datetime(new_df.index)
    cases = new_df.T.copy()

    cases.to_csv('data/cases.csv')
    deaths.to_csv('data/deaths.csv')
    return True


def create_data_plots_map():
    json_files = {}
    dic={}
    for name in cases.index:
        coord = get_coordinates(name)
        dic[name] = coord
        df = cases_pT_new.T[name].to_frame(name='cases')
        df['deaths*10'] = deaths_pT_new.T[name]*10
        line = v.Line(df.rolling(7, center=True, min_periods=1).mean())
        line.axis_titles(x='Date', y='per 100k inhabitants')
        line.legend(name)
        line.width = 350
        line.height = 150
        json_files[name] = str(line.to_json())
    df = pd.DataFrame(dic,index=['lat', 'long']).T
    df2 = pd.DataFrame(json_files,index=['json']).T
    df['json'] = df2
    coord = df.copy()
    coord.to_csv('data/coord.csv')
    return True







