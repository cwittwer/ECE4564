import pymongo
import pycurl
from datetime import datetime 
from functools import wraps
from flask import request, Response
import json


class AuthDB:
		
	def __init__(self):
	
		self._client = pymongo.MongoClient("mongodb://localhost:27017/")
		self._db = self._client.user_database
		self._collection = self._db.users

	def ADD_USER(self, message):
		user = message['username']
		password = message['password']
		
		search_data = {'username' : user, 'password': password}
		try:
			count_users = self._collection.find(search_data).count()
			if count_users > 0: 
				response = 'Error: Unable to add. User already exists'
				return response
			else:
				user_data = {'user': user , 'password' : password}
				x = self._collection.insert_one(user_data).inserted_id
				response = 'OK: Successfully inserted. User: ' + str(x)
				return response
		except:
			user_data = {'user': user , 'password' : password}
			x = self._collection.insert_one(user_data)
			response = 'OK: Successfully inserted, User: ' + str(x.inserted_id)
			return response

	def DROP_DB(self):
		self._client.drop_database(self._db)



