from flask import Flask, jsonify, request, abort
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
from bson.objectid import ObjectId
import os
import time
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app, support_credentials=True)
     
# MongoDB connection
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri, server_api=ServerApi('1'))
db = client["DeeperSystemsTaskDB"]
users_collection = db["users"]

@app.route("/api/users", methods=["GET"])
def get_users():
    users = users_collection.find()
    return dumps(users), 200

@app.route("/api/users/<id>", methods=["GET"])
def get_user(id):
    user = users_collection.find_one({"_id": ObjectId(id)})
    if user:
        return dumps(user), 200
    else:
        abort(404, "User not found")

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    user_id = users_collection.insert_one(data).inserted_id
    return jsonify(str(user_id)), 201

@app.route("/api/users/<id>", methods=["PUT"])
def update_user(id):
    data = request.json
    # current_time = time.time()
    data["updated_ts"] = time.time()

    result = users_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count:
        return jsonify({"status": "User updated successfully"}), 200
    else:
        abort(404, "User not found")

@app.route("/api/users/<id>", methods=["DELETE"])
def delete_user(id):
    result = users_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"msg": "User deleted"}), 200
    else:
        abort(404, "User not found")

if __name__ == "__main__":
    app.run(debug=True)
