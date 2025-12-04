from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

#Connect to Mongo Atlas Cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))
print(mongo_client.list_database_names())


# Access database
trust_bank_db = mongo_client["trust_bank_db"]

application_forms_collection = trust_bank_db["application_forms"]
users_collection = trust_bank_db["users"]