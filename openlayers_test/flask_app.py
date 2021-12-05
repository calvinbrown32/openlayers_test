"""
This goal of this script is to both test Openlayers features, but also to learn and apply JavaScript
skills in conjunction with Python, Flask.

Other skills that I hope to incorporate in this Web app: React, JQuery,

Resources - Python and JavaScript
https://flask.palletsprojects.com/en/2.0.x/patterns/jquery/
https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
https://towardsdatascience.com/talking-to-python-from-javascript-flask-and-the-fetch-api-e0ef3573c451
https://www.jitsejan.com/python-and-javascript-in-flask



TO DO:

"""





import os
import pandas as pd
import geopandas as gpd
import numpy as np
from flask import Flask, request,json, render_template, redirect, url_for, request, send_from_directory, flash, session
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from werkzeug.utils import secure_filename
import datetime as dt
from datetime import datetime
import shutil
import json

# # Geojson Endpoint for NYC Open Data - 311 2010 - Present

ENDPOINT = "https://data.cityofnewyork.us/resource/erm2-nwe9.geojson"
QUERY_SYMBOL = '?'
COMMUNITY_BOARD = 'community_board'
CB = "03 MANHATTAN"
base_url = ENDPOINT + QUERY_SYMBOL + COMMUNITY_BOARD + '=' + CB

# Create secondary query to test date function.
# Documentation here: https://dev.socrata.com/foundry/data.cityofnewyork.us/erm2-nwe9

ENDPOINT = "https://data.cityofnewyork.us/resource/erm2-nwe9.geojson"
QUERY_SYMBOL = '?'
WHERE = "$where="
date = "2021-09-01T00:00:00.000"
date_operator = " > "
date_query = f"created_date{date_operator}'{date}'"
base_url = ENDPOINT + QUERY_SYMBOL + WHERE + date_query

# Current Time in floating timestamp data type, which is what Socrata uses.
now = datetime.now()
dt_2 = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4]

# Blank Space in url works with Socrata, but not geopandas, so replacing space with html hexadecimal space.
base_url = base_url.replace(' ','%20')

# Read in geojson data from socrata url created above
cb3_complaints_geo = gpd.read_file(base_url)

# Total bounds is returning null array. This is probably because there are null values in geometry column.
# Follow Steps 1 and 2 to correct:

# 1 Create new geodataframe of rows with null geometry so that data is not lost
complaints_null_geo = cb3_complaints_geo[cb3_complaints_geo['geometry'].isna()]

# 2 Remove all rows with null geometry from original geodataframe
cb3_complaints_geo = cb3_complaints_geo[cb3_complaints_geo['geometry'].notna()]

bounds = cb3_complaints_geo.total_bounds
a = np.mean(bounds[0:3:2]).round(3)
b = np.mean(bounds[1:4:2]).round(3)
data_centroid = [a,b]
print(data_centroid)

cb3_complaints = cb3_complaints_geo.to_json()

cb3_complaints

type(cb3_complaints)

# ==============================================================
# from os.path import join, dirname, realpath

project_root = os.path.dirname(__file__)
print(project_root)
template_path = os.path.join(project_root, 'app/templates')


server = flask.Flask(__name__)

# Setup Upload Folder
cwd = os.getcwd()
UPLOAD_FOLDER = os.path.join(cwd, 'uploads')
print(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'csv'}

#Configure Server / Flask Object
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
server.config['UPLOAD_EXTENSIONS'] = ['.csv']
server.config['SECRET_KEY'] = '6WX9PIg8zdrQHqwwDVOS_Q'


@server.route('/')
def render_index():
    """index.html"""
    return render_template('map_example.html', cb3_complaints=cb3_complaints, data_centroid=data_centroid, author = 'Calvin')



@server.route('/map_example_1.html')
def render_contact():
    """contact.html"""
    return render_template('map_example_1.html.html', author = 'Calvin')

if __name__ == '__main__':
    server.run(debug=True)
