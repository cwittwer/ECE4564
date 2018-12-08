import pymongo
from datetime import datetime 
import json

class mongo:
		
	def __init__(self):
	
		self._client = pymongo.MongoClient("mongodb://localhost:27017/")
		self._db = self._client.book_database
		self._collection = self._db.books
		
	def ADD(self, message):
		name = message['Name']
		author = message['Author']
		
		search_data = { 'Name' : name, 'Author': author}
		try:
			count_books = self._collection.find_one(search_data).count()
			if count_books > 0: 
				response = 'Error: Unable to add. Book already exists'
				return response
			else:
				book_data = {'stock': 0 , 'Name' : name, 'Author': author}
				x = self._collection.insert_one(book_data).inserted_id
				response = 'OK: Successfully inserted. Book ID ' + str(x)
				return response
		except:
			book_data = {'stock': 0 , 'Name' : name, 'Author': author}
			x = self._collection.insert_one(book_data)
			response = 'OK: Successfully inserted. Book ID ' + str(x.inserted_id)
			return response
		
	def BUY(self, message):
		name = message['Name']
		author = message['Author']
		count = message['Count']
		
		search_data = { 'Name' : name, 'Author': author}
		count_books = self._collection.find_one(search_data)
		if count_books != None: 
			while(count):
				self._collection.update_one(search_data, { '$inc': { 'stock' : 1}})
				count = count - 1
			book_return_count = self._collection.find_one(search_data , {'Name' : 0 , 'Author' : 0 })
			response = 'Ok:' + str(search_data) + 'Stock: ' + str(book_return_count['stock'])
			return response
		else:
			#error handle
			response = 'Error: Book does not exist'
			return response
			
	def SELL(self, message):
		name = message['Name']
		author = message['Author']
		count = message['Count']
		
		search_data = { 'Name' : name, 'Author': author}
		count_books = self._collection.find(search_data).count()
		if count_books > 0:#decrement count or delete
			book_value = self._collection.find_one(search_data)
			if book_value['stock'] < count:
				response = 'Error: Stock is not enough'
				return response
			else:
				while(count):
					self._collection.update_one(search_data, { '$inc': { 'stock' : -1}})
					count = count - 1
				book_return_count = self._collection.find_one(search_data , {'Name' : 0 , 'Author' : 0 })
				response = 'Ok:' + str(search_data) + 'Stock: ' + str(book_return_count['stock'])
				return response
		else:
			response = 'Error: Unable to sell. Book does not exist.'
			return response		
			
	def DELETE(self, message):
		name = message['Name']
		author = message['Author']
		
		search_data = { 'Name' : name, 'Author': author}
		count_books = self._collection.find_one(search_data)
		if count_books != None:
			self._collection.delete_one(search_data)
			response = 'Ok: successfully deleted'
			return response
		else:
			response = 'Error: Unable to delete. Book does not exist.'
			return response	
			
	def COUNT(self, name, author):		
		search_data = { 'Name' : name, 'Author': author}
		count_books = self._collection.find_one(search_data)
		if count_books == None:
			response = 'Error: No books in stock'
			return response
		else:
			response = 'Ok: ' + str(count_books['stock']) + ' books in stock.'
			return response
			
	def LIST(self):
                x = []
                book_list = list(self._collection.find())
                count_books = self._collection.count()
                mess = [('OK. Got books information')]
                for i in book_list:
                        x.append(i)
                response = {'Msg' : mess, 'Books' : 'does not work'}
                return response
		
	def COUNT_INT(self):		
		count_books = self._collection.count()
		if count_books == 0:
			return 0
		else:
			return count_books
			
	def DROP_DB(self):
		self._client.drop_database(self._db)
		
	def EXISTS(self):
		try:
			col_list = self._client.list_collection_names()
			if 'books' in col_list:
				return True
			else:
				return False
		except:
			return False
