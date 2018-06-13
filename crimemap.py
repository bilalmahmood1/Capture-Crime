#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Crimemap Application
@author: bilal
"""

from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
import json
import requests
from API_KEYS import IPINFO_KEY,MAPS_KEY_1,MAPS_KEY_2,MAPS_KEY_3

test = False

if test:
    from db_config import MockDBHelper as DBHelper
else:
    from db_helper import DBHelper


DEFAULT_ADDRESS = 31.464930, 74.392414
CATEGORIES = sorted(["Corruption","Injustice","Traffic","Theft","Deception","Crime","Violence"])
CATEGORIES.append("Other") 

              
app = Flask(__name__)
DB = DBHelper()

@app.route("/")
def home():
    
    try:
        address = get_approx_address()
    except Exception as e:
        print(e)
        address = DEFAULT_ADDRESS
    try:
        data = DB.get_all_issues()
        data = json.dumps(data)
        count = DB.count_issues()
    except Exception as e:
        print(e)
        data = None
    return render_template("home.html",
                           MAPS_KEY = MAPS_KEY_1 + MAPS_KEY_2 + MAPS_KEY_3,
                           lat = address[0],
                           long =  address[1],
                           data = data,
                           count = count,
                           categories = CATEGORIES
                           )

@app.route("/submit_issue", methods = ["POST"])
def add_issue():
    try:
        
        category = request.form.get("category")
        date = request.form.get("date")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        description = request.form.get("description")
        DB.add_issue(category, date, latitude, longitude, description)

    except Exception as e:
        print(e)

    return redirect(url_for('home'))

@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return redirect(url_for('home'))




def get_approx_address():
    """Access latitude and longitude information using the client's IP"""
    ip = get_ip_address()
    return get_lat_long(ip)
def get_ip_address():
    """Returns IP address of the client"""
    try:
        ip = request.remote_addr
    except Exception as e:
        print(e)
        ip = None
        
    finally:
        return ip

def get_lat_long(ip):
    """Get latitude and longitude from the ip address using ipinfo API"""
    URL = "http://ipinfo.io/{}/json?token={}"
    try:
        response = requests.get(URL.format(ip,IPINFO_KEY))
        location = [float(i) for i in response.json()['loc'].split(",")]
        latitude = location[0]
        longitude = location[1]
        
    except Exception as e:
        print(e)
        latitude, longitude = DEFAULT_ADDRESS
        
    finally:
        return latitude, longitude
    
    
if __name__ =="__main__":
    app.run(port = 5000, debug=True)