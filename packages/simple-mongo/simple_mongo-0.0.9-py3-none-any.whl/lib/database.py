from pymongo import MongoClient
from dotenv import load_dotenv
from pydantic import BaseModel
import os
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
    def find_one(cls, collection_name, query):
        """
        Finds a single document in the collection
        """
        return cls.collection(collection_name).find_one(query)
    
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