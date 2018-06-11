#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initializes MYSQL database. 
Creates crimemap database and creates crimes table in it!
@author: bilal
"""

import pymysql
from db_config import username, password

connection = pymysql.connect(host = 'localhost',
                             user=username,
                             passwd=password)
try:
    with connection.cursor() as cursor:
        sql = """CREATE DATABASE IF NOT EXISTS crimemap"""
        cursor.execute(sql)
        sql = """
                 CREATE TABLE IF NOT EXISTS crimemap.crimes
                 (
                         id int NOT NULL AUTO_INCREMENT,
                         latitude FLOAT(10,6),
                         longitude FLOAT(10,6),
                         date DATETIME,
                         category VARCHAR(50),
                         description VARCHAR(1000),
                         updated_at TIMESTAMP,
                         PRIMARY KEY(id)
                 )
                """
        cursor.execute(sql)
    
    connection.commit()

except Exception as e:
    print(e) 
finally:
    connection.close()
        
        