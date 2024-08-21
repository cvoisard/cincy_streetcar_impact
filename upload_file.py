import pandas as pd
from pymongo import MongoClient

from dotenv import load_dotenv
import os

load_dotenv()

csv_name = os.getenv('CSV_PATH')

df = pd.read_csv(csv_name)

mongo_url = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')
collection_name = os.getenv('COLLECTION_NAME_2')

client = MongoClient(mongo_url)
db = client[db_name]
collection = db[collection_name]

data = df.to_dict(orient='records')
collection.insert_many(data)

print("data imported successfully")
