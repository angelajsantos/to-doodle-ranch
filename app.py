from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import random
import os
from datetime import datetime

# ── MongoDB ──────────────────────────────────────────────────────────────────
MONGODB_URI = os.environ.get(
    "MONGODB_URI",
    "mongodb+srv://angelajinsantos_db_user:Tempy0624@to-doodle-database.nbanyrx.mongodb.net/"
)
client = MongoClient(MONGODB_URI, tlsAllowInvalidCertificates=True)
db = client["training-grounds"]
collection = db["quests"]

# ── Pet roster (pixel art sprites from itch.io / opengameart) ────────────────
PETS = [
    {"name": "zuko",    "type": "dragon hatchling", "emoji": "🐉"},
    {"name": "biscuit", "type": "corgi pup",        "emoji": "🐕"},
    {"name": "mochi",   "type": "ghost bunny",      "emoji": "🐰"},
    {"name": "denki",   "type": "thunder cat",      "emoji": "🐱"},
    {"name": "slime",   "type": "slime",            "emoji": "🟢"},
    {"name": "oden",    "type": "cloud fox",        "emoji": "🦊"},
    {"name": "cinder",  "type": "lava toad",        "emoji": "🐸"},
    {"name": "stardust","type": "fairy moth",       "emoji": "🦋"},
]

app = Flask(__name__)

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/quests", methods=["GET"])
def get_quests():
    quests = []
    for q in collection.find().sort("created_at", -1):
        q["_id"] = str(q["_id"])
        quests.append(q)
    return jsonify(quests)


@app.route("/api/quests", methods=["POST"])
def create_quest():
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    pet = random.choice(PETS)
    quest = {
        "title":      data["title"],
        "description": data.get("description", ""),
        "status":     "training",          # training | graduated
        "pet":        pet,
        "created_at": datetime.utcnow().isoformat(),
        "completed_at": None,
        "xp":         random.randint(10, 100),
    }
    result = collection.insert_one(quest)
    quest["_id"] = str(result.inserted_id)
    return jsonify(quest), 201


@app.route("/api/quests/<quest_id>/complete", methods=["PATCH"])
def complete_quest(quest_id):
    try:
        oid = ObjectId(quest_id)
    except Exception:
        return jsonify({"error": "Invalid ID"}), 400

    result = collection.update_one(
        {"_id": oid},
        {"$set": {"status": "graduated", "completed_at": datetime.utcnow().isoformat()}}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Quest not found"}), 404
    return jsonify({"success": True})


@app.route("/api/quests/<quest_id>", methods=["DELETE"])
def delete_quest(quest_id):
    try:
        oid = ObjectId(quest_id)
    except Exception:
        return jsonify({"error": "Invalid ID"}), 400

    collection.delete_one({"_id": oid})
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
