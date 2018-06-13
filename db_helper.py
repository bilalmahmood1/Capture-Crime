#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 05:48:06 2018

@author: bilal
"""

import pymysql
from db_config import username, password
import datetime


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
    
    def add_issue(self, category, date, latitude, longitude, description):
        """Add the data user entered into the DB"""
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (category, date, latitude, longitude, description) VALUES (%s,%s,%s,%s,%s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (category, date, latitude, longitude, description))     
            connection.commit()
        except Exception as e:
            print(e)
        
        finally:
            connection.close()

	
    def count_issues(self):
        """Returns total number of issues registered so far"""
        
        connection = self.connect()
        total_count = None
        try:
            
            query = "SELECT COUNT(*) FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)     
                total_count = cursor.fetchone()[0]
                    
            return total_count
        except Exception as e:
            print(e)
            return total_count
        finally:
            connection.close()

    
    def get_all_issues(self):
        """Fetches the issues from the crimes table"""
        connection = self.connect()
        try:
            query = "SELECT latitude, longitude, date, category, description FROM crimes;"
            data = []
            with connection.cursor() as cursor:
                cursor.execute(query)
                for issue in cursor:
                    named_issue = {
                        'latitude': issue[0],
                        'longitude': issue[1],
                        'date': datetime.datetime.strftime(issue[2], '%Y-%m-%d'),
                        'category': issue[3],
                        'description': issue[4]
                    }
                    data.append(named_issue)
            return data
            
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
     
        
        