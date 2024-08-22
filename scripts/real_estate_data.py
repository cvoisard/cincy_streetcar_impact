import requests
import pandas as pd
from pymongo import MongoClient
import json

from dotenv import load_dotenv
import os

load_dotenv()


json_path = os.getenv('JSON_PATH')

rentcast_api_key = os.getenv('RENTCAST_API_KEY')
rentcast_api_url = os.getenv('RENTCAST_API_URL')

mongo_url = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')
collection_name = os.getenv('COLLECTION_NAME_1')

client = MongoClient(mongo_url)
db = client[db_name]
collection = db[collection_name]
   
with open(json_path, 'r') as file:
    property_data = json.load(file)

for property_info in property_data:
    address = property_info.get('address')
    property_type = property_info.get('propertyType')
    bedrooms = property_info.get('bedrooms')
    bathrooms = property_info.get('bathrooms')
    square_footage = property_info.get('squareFootage')
    comp_count = property_info.get('compCount')

    payload = {
        'address': address,
        'propertyType': property_type,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'squareFootage': square_footage,
        'compCount': comp_count
    }

    headers = {
        'accept': 'application/json',
        'X-Api-Key': rentcast_api_key
    }

    response = requests.get(rentcast_api_url, headers=headers, params=payload)

    if response.status_code == 200:
        estimate_data = response.json()

        property_info['estimate'] = estimate_data
        collection.insert_one(property_info)
    else:
        print(f"Failed to get estimate for {address}. Status code: {response.status_code}, Response: {response.text}")
    
client.close()