import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["stallsync_db"]

stalls_collection = db["stalls"]
stalls_data = [
    {
        "stall_id": "STALL_001",
        "location": "MetLife Stadium - Gate A",
        "inventory": {"hot_dogs": 500, "water_bottles": 1200},
        "pricing": {"hot_dogs": 5.00, "water_bottles": 3.00},
        "foot_traffic_baseline": "high"
    },
    # Add more mock stalls as needed
]

stalls_collection.delete_many({})
stalls_collection.insert_many(stalls_data)
print("Database seeded successfully!")