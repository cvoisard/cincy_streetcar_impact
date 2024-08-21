import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

csv_path = os.getenv('CSV_PATH')
json_path = os.getenv('JSON_PATH')

columns_to_include = os.getenv('COLUMNS_TO_INCLUDE').split(',')

df = pd.read_csv(csv_path)

df.columns = df.columns.str.strip()

available_columns = [col for col in columns_to_include if col in df.columns]

df_filtered = df[available_columns]

json_str = df_filtered.to_json(orient='records', lines=True)
json_lines = json_str.strip().splitlines()
formatted_json = '[\n' + ',\n'.join(json_lines)+ '\n]'

with open(json_path, 'w') as json_file:
    json_file.write(formatted_json)
