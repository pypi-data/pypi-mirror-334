from pymongo import MongoClient
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from .aggregator import Aggregator
class MongoDB:
    
    def __init__(self):
        load_dotenv()
        self._client = MongoClient(os.getenv('MONGODB_URL'))

    def __new__(cls, *args, **kwargs):
        return super(MongoDB, cls).__new__(cls)

    @property
    def db(self):
        """
        Returns the database object
        """
        return self._client[os.getenv('MONGODB_NAME')]
    
    @classmethod
    def collection(cls, collection_name):
        """
        Returns the collection object
        """
        return cls().db[collection_name]
    
    @classmethod
    def create(cls, collection_name, data : dict | BaseModel):
        """
        Creates a new document in the collection
        """

        if isinstance(data, BaseModel):
            data = data.model_dump()

        return cls.collection(collection_name).insert_one(data)
    
    @classmethod
    def update(cls, collection_name, query, data):
        """
        Updates a document in the collection
        """
        return cls.collection(collection_name).update_one(query, {'$set': data})
    
    @classmethod
    def update_by_id(cls, collection_name, _id, data):
        """
        Updates a document by id
        """
        return cls.collection(collection_name).update_one({'_id': _id}, {'$set': data})
    
    @classmethod
    def delete(cls, collection_name, query):
        """
        Deletes a document in the collection
        """
        return cls.collection(collection_name).delete_one(query)
    
    @classmethod
    def all(cls, collection_name):
        """
        Returns all documents in the collection
        """
        return cls.collection(collection_name).find()

    @classmethod
    def find_one(cls, collection_name : str, query : dict):
        """
        Finds a single document in the collection
        """
        return cls.collection(collection_name).find_one(query)
    
    @classmethod
    def begin_aggregate(cls, collection_name: str):
        
        return Aggregator(cls, collection_name)
    
    @classmethod
    def aggregate(cls, collection_name, pipeline):
        """
        Aggregates the collection
        """
        return cls.collection(collection_name).aggregate(pipeline)
    
    @classmethod
    def paginate(cls, collection_name, query, page, limit):
        """
        Paginates the collection
        """
        return cls.collection(collection_name).find(query).skip((page-1)*limit).limit(limit)