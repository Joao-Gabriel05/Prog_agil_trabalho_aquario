import pymongo
from bson import json_util

class Mongo:
    def __init__(self, string_conexao:str, db_name:str, collection_name:str):
        self.client = pymongo.MongoClient(string_conexao)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_document(self, document):
        result = self.collection.insert_one(document)
        result = self.read_document_one({"_id":result.inserted_id})
        return result

    def read_document_all(self,query={}):
        if query:
            return self.collection.find(query)
        result = list(self.collection.find())
        for item in result:
            item["_id"] = str(item["_id"])
        return result
    
    def read_document_one(self, query):
        result = self.collection.find_one(query)
        result["_id"] = str(result["_id"])
        return result

    def update_document(self, query, update_data):
        self.collection.update_one(query, {'$set': update_data})
        result = self.read_document_one(query)
        return result

    def delete_document(self, query):
        self.collection.delete_one(query)

    def existe(self, query):
        if list(self.read_document_all(query)):
            return True
        else:
            return False