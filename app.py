#Author: JaniniRami
import os
import time
import json
import datetime as dt
from flask import Flask
from flask import render_template, url_for, request, Response, jsonify, redirect, make_response

from lib.process_data import search_cat_data, search_tle_data, generate_autocomplete_data


data = {}
downloads_path = 'data'
current_date = dt.date.today()
expire_date = dt.datetime.now()
expire_date = expire_date + dt.timedelta(hours=5)


app = Flask(__name__)


######################################################################
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
######################################################################

@app.route('/')
def frstLoad():
    return render_template('first_load.html')

@app.route('/home', methods=['GET', 'POST'])
def index():
    search_cat_data(data, downloads_path, current_date, 0)
    search_bar = request.form.get('satellite_info')
    norad_id = request.args.get('satellite_info', None)

    if norad_id == None:
        return render_template('index.html', form = search_bar, cat_data = {'ERROR' : True, 'COMMENT' : ''})
    else:
        cat_data = search_cat_data(data, downloads_path, current_date, norad_id)
        if cat_data == None:
            cat_data = {'ERROR' : True, 'COMMENT' : 'Name or ID cannot be found.'}
        else:
            pass
        return render_template('index.html', cat_data = cat_data)


@app.route('/autocomplete')
def autocomplete():
    autocomplete_data = generate_autocomplete_data(data)
    return Response(json.dumps(autocomplete_data), mimetype='application/json')

@app.route('/map')
def map():
    norad_id = request.args.get('id', None)
    tle_data = search_tle_data(data, downloads_path, norad_id, current_date)
    sat_name = search_cat_data(data, downloads_path, current_date, norad_id)['SATNAME']
    print(sat_name)
    print(tle_data)
    if tle_data == None:
        return render_template('errors/404.html', error_comment = 'The satellite have decayed or is not available.')
    else:
        return render_template('map.html', tle1 = tle_data['TLE_1'], tle2 = tle_data['TLE_2'], norad_id = norad_id, sat_name = sat_name)


@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
