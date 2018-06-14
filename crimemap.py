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
import bleach
import dateparser
import datetime
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
def home(messages = None):
    try:
        address = get_approx_address()
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
                           categories = CATEGORIES,
                           error_message = messages
                           )

@app.route("/submit_issue", methods = ["POST"])
def add_issue():
        
    ## Validating category
    category = request.form.get("category")
    if category not in CATEGORIES:
        messages = "Please select from the category."
        return home(messages)
    

    user_date = request.form.get("date")
    date = validate_date(user_date)
    
    if date == None:
        messages = "Please enter correct date (year/month/day). "
        return home(messages)
    
                                    
    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:
        messages = "Please enter location by clicking on the map."
        return home(messages)
        
    
    ## Sanitizing the description
    description = sanitize_text(request.form.get("description"))

    try:    
        DB.add_issue(category, date, latitude, longitude, description)
    except Exception as e:
        print(e)

    return home()

@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()


def validate_date(user_date):
    """validate user entered date"""
    date = dateparser.parse(user_date)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None
     
def sanitize_text(text):
    """Sanitize free text to prevent against XSS attacks"""
    return bleach.clean(text)

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