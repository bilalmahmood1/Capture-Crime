#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 05:48:06 2018

@author: bilal
"""


import pymysql
from db_config import username, password

class DBHelper:
    def connect(self, database = "crimemap"):        
        """Establishes connection to the database and returns the 
        connection object
        """
        connection = pymysql.connect(host = 'localhost',
                             user = username,
                             passwd = password,
                             db = database)
        
        return connection
    
    
    def get_all_inputs(self):
        """Fetches the description column from the crimes table"""
        connection = self.connect()
        try:
            query = "SELECT description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
            return data
            
        except Exception as e:
            print(e)
   
        finally:
            connection.close()
            
        
    def add_input(self, data):
        """Insert data into the description column of the crimes table"""
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (description) VALUES (%s);"
            with connection.cursor() as cursor:
                cursor.execute(query, data)
             
            connection.commit()
                
                
        except Exception as e:
            print(e)
   
        finally:
            connection.close()
     
        
    def clear_all(self):
        """Delete the crimes table"""
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            connection.commit()
                
                
        except Exception as e:
            print(e)
   
        finally:
            connection.close()
     
        
        