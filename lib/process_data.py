import re
import os
import sys
import json
import datetime as dt

from lib.download_data import download_data_



def search_cat_data(data, downloads_path, current_date, norad_id):
    if not os.path.exists(downloads_path):
        os.mkdir(downloads_path)
    else:
        pass

    cat_file_name = f'{downloads_path}/{current_date} - SatCat'
    tle_file_name = f'{downloads_path}/{current_date} - TLE'
    download_data_(data, current_date,cat_file_name, tle_file_name)

    try:
        norad_id = norad_id.split("---",1)[1].replace(' ', '')
    except:
        pass
    for i in range(len(data['cat_data'])):
        if data['cat_data'][i]['NORAD_CAT_ID'] == norad_id:
                return data['cat_data'][i]
        else:
            pass

def search_tle_data(data, downloads_path, norad_id, current_date):
    cat_file_name = f'{downloads_path}/{current_date} - SatCat'
    tle_file_name = f'{downloads_path}/{current_date} - TLE'
    download_data_(data, current_date,cat_file_name, tle_file_name)

    for i in range(len(data['tle_data'])):
        if data['tle_data'][i]['NORAD_CAT_ID'] == norad_id:
            return data['tle_data'][i]
        else:
            pass



def generate_autocomplete_data(data):
    search_data = []
    for i in range(len(data['cat_data'])):
        sat_name = data['cat_data'][i]['SATNAME']
        norad_id = data['cat_data'][i]['NORAD_CAT_ID']

        item = f'{sat_name} --- {norad_id}'
        search_data.append(item)
    return search_data
