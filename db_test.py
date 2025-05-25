from pymongo import MongoClient
import os

# MongoDB Atlas connection string
uri = os.getenv("MONGODB_URI")

# create Client
client = MongoClient(uri)

# print DB List 
print(client.list_database_names())
