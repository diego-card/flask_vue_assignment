import json
from dataclasses import dataclass, asdict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    active: bool
    created_ts: float

def parse_roles(data):
    roles = []
    if data.get("is_user_admin"):
        roles.append("admin")
    if data.get("is_user_manager"):
        roles.append("manager")
    if data.get("is_user_tester"):
        roles.append("tester")
    return roles

def load_json_and_import(json_file):
    with open(json_file) as file:
        data = json.load(file)
    
    users = []
    for user_data in data["users"]:
        user = User(
            username=user_data["user"],
            password=user_data["password"],
            roles=parse_roles(user_data),
            preferences=UserPreferences(timezone=user_data["user_timezone"]),
            active=user_data["is_user_active"],
            created_ts=time.mktime(datetime.strptime(user_data["created_at"], "%Y-%m-%dT%H:%M:%SZ").timetuple())
        )
        users.append(asdict(user))
    
    return users

def insert_users_to_mongo(users):
    client = MongoClient(mongo_uri, server_api=ServerApi('1'))
    db = client["DeeperSystemsTaskDB"]
    users_collection = db["users"]
    
    users_collection.insert_many(users)
    print(f"Inserted {len(users)} users into the MongoDB 'users' collection.")

if __name__ == "__main__":
    users = load_json_and_import("data.json")
    insert_users_to_mongo(users)
