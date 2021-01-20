import os
import re
import sys
import json
import time
import progressbar
import numpy as np
import datetime as dt


def clean_data(data, cat_file_name, tle_file_name):
    tle_data = []
    tmp_dict = {}

    if not os.path.exists(f'{tle_file_name}.txt'):
        pass
    else:
        print('[*] Reading satellite TLE data...')
        with open(f'{tle_file_name}.txt', 'r') as read_file:
            for line in read_file:
                if line[0] == '1':
                    norad_id = line.split()[1]
                    norad_id = re.sub('\D', '', norad_id)

                    tmp_dict['NORAD_CAT_ID'] = norad_id
                    tmp_dict['TLE_1'] = line.replace('\n', '')

                elif line[0] == '2':
                    tmp_dict['TLE_2'] = line.replace('\n', '')
                    tle_data.append(tmp_dict)
                    tmp_dict = {}

                else:
                    break

        print('[*] Cleaning satellite catalog data...')

        with open(f'{cat_file_name}.txt', 'r') as read_file:
            cat_data = json.load(read_file)


        print('[*] Writing new files...')
        with open(f'{tle_file_name}.json', 'w') as write_file:
            json.dump(tle_data, write_file, indent=2)

        with open(f'{cat_file_name}.json', 'w') as write_file:
            json.dump(cat_data, write_file, indent=2)

        os.remove(f'{cat_file_name}.txt')
        os.remove(f'{tle_file_name}.txt')


        with open(f'{tle_file_name}.json', 'r') as read_file:
            tle_data = json.load(read_file)

        with open(f'{cat_file_name}.json', 'r') as read_file:
            cat_data = json.load(read_file)

        data['tle_data'] = tle_data
        data['cat_data'] = cat_data

def check_expiry_date(file_name):
    file_name = f'{file_name}.json'
    if os.path.exists(file_name):
        data_file = os.stat(file_name)
        data_file_age = (time.time() - data_file.st_mtime)
        #86400 seconds == 24hours
        if data_file_age <= 86400:
            return False, None
        else:
            from lib.login import space_track_login
            login_session = space_track_login()
            return True, login_session
    else:
        from lib.login import space_track_login
        login_session = space_track_login()
        return True, login_session

def tle_data_download(login_session, tle_file_name):
        current_date = dt.date.today()
        d1 = current_date.strftime("%d-%m-%Y")

        login_session = check_expiry_date(tle_file_name)[1]

        if check_expiry_date(tle_file_name)[0] == True:
            print('[*] Downloading TLE data...')

            url = "https://www.space-track.org/basicspacedata/query/class/tle/EPOCH/{}%2000:00:00" \
                  "--{}%2000:00:00/orderby/TLE_LINE1/format/tle".format(current_date - dt.timedelta(days=1), current_date)

            response = login_session.get(url, timeout=5, stream=True)
            file_size = int(response.headers.get('Content-Length', None))
            bars_num = np.ceil(file_size / 1024)



            bar = progressbar.ProgressBar(maxval=bars_num).start()
            with open(f'{tle_file_name}.txt', 'wb') as f:
                for i, chunk in enumerate(response.iter_content(1024)):
                    f.write(chunk)
                    bar.update(i+1)
        else:
            pass

def cat_data_download(data, login_session, cat_file_name, tle_file_name):
    login_session = check_expiry_date(cat_file_name)[1]

    if check_expiry_date(cat_file_name)[0] == True:
        url = 'https://www.space-track.org/basicspacedata/query/class/satcat/orderby/NORAD_CAT_ID%20asc/metadata/false/format/json'
        print('[*] Downloading satellite catalog data...')

        response = login_session.get(url, timeout=5, stream=True)
        file_size = int(response.headers.get('Content-Length', None))
        bars_num = np.ceil(file_size / 1024)



        bar = progressbar.ProgressBar(maxval=bars_num).start()
        with open(f'{cat_file_name}.txt', 'wb') as f:
            for i, chunk in enumerate(response.iter_content(1024)):
                f.write(chunk)
                bar.update(i+1)

        clean_data(data, cat_file_name, tle_file_name)
    else:
        pass

def download_data_(data, current_date, cat_file_name, tle_file_name):
    if (not os.path.exists(f'{cat_file_name}.json') and
            not os.path.exists(f'{tle_file_name}.json')):

        current_date_ = current_date.strftime("%d-%m-%Y")
        login_session = check_expiry_date(tle_file_name)[1]
        tle_data_download(login_session, tle_file_name)
        cat_data_download(data, login_session, cat_file_name, tle_file_name)

    else:
        if not data:
            with open(f'{tle_file_name}.json', 'r') as read_file:
                tle_data = json.load(read_file)

            with open(f'{cat_file_name}.json', 'r') as read_file:
                cat_data = json.load(read_file)

            data['tle_data'] = tle_data
            data['cat_data'] = cat_data
        else:
            pass
