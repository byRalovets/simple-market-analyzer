import json
import redis
import pandas as pd

from const.database import Database
from const.dataset import Dataset

print("script started")
redis_client = redis.Redis(host=Database.REDIS_HOST,
                           port=Database.REDIS_PORT,
                           db=Database.REDIS_DB,
                           password="trading_platform",
                           charset=Database.REDIS_CHARSET,
                           decode_responses=True)
print("redis connected")

result = redis_client.hgetall(Database.REDIS_HASH_NAME)
data = list(result.values())
print("data extracted")

json_values = []

for element in data:
    json_object = json.loads(element)
    json_values.append(json_object)

df = pd.DataFrame(json_values)
print("dataset created")

csv_data = df.to_csv(Dataset.PATH, index=False)
print(f"dataset saved to {Dataset.PATH}")
