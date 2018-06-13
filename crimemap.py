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

test = False

if test:
    from db_config import MockDBHelper as DBHelper
else:
    from db_helper import DBHelper


DEFAULT_ADDRESS = 31.464930, 74.392414


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
    except Exception as e:
        print(e)
        data = None
    return render_template("home.html",
                           lat = address[0],
                           long =  address[1],
                           data = data)

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
    """ Uses IP address to estimate the address of the user"""
    return 31.464930, 74.392414

if __name__ =="__main__":
    app.run(port = 5000, debug=True)