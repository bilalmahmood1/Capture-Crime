#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Crimemap Application
@author: bilal
"""
from db_helper import DBHelper
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
DB = DBHelper()

@app.route("/")
def home():
    try:
        print("Pulling data out of the db")
        data = DB.get_all_inputs()
    except Exception as e:
        print(e)
        data = None
    return render_template("home.html",
                           number_data = len(data),
                           data = data)

@app.route("/add", methods = ["POST"])
def add():
    try:
        print("Inserting data into db")
        data = request.form.get("user_input")
        DB.add_input(data)        
    except Exception as e:
        print(e)    
    return home()

@app.route("/clear")
def clear():
    try:
        print("Clearning db")
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()


if __name__ =="__main__":
    app.run(port = 5000, debug=True)