# config/db.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.client = MongoClient(os.getenv('MONGODB_URI'))
            cls._instance.db = cls._instance.client[os.getenv('MONGODB_DB_NAME')]
        return cls._instance
    
    def get_db(self):
        return self.db