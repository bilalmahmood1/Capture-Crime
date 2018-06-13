#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Credentials to talk with the DB, along with the mo-ck database that is 
used to emulalte the db interaction while devolping the crime app
@author: bilal
"""

username ='root'
password ='root'

class MockDBHelper:
	def connect(self, database="crimemap"):
		pass
	def get_all_inputs(self):
		return ['A','B','C']
	def add_input(self, data):
		pass
	def clear_all(self):
		pass
	def add_issue(category, date, latitude, longitude, description):
		pass

