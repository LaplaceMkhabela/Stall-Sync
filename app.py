import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = MongoClient(os.getenv("MONGO_URI"))
db = client["stallsync_db"]

# Endpoint for the Agent to read current stock
@app.route('/api/inventory/<stall_id>', methods=['GET'])
def get_inventory(stall_id):
    stall = db.stalls.find_one({"stall_id": stall_id}, {"_id": 0})
    return jsonify(stall) if stall else jsonify({"error": "Stall not found"}), 404

# Endpoint for the Agent to PROPOSE a change (Human-in-the-loop)
@app.route('/api/propose_action', methods=['POST'])
def propose_action():
    data = request.json
    # Store the proposed action in a separate collection for human review
    proposal = {
        "stall_id": data.get("stall_id"),
        "reason": data.get("reason"),
        "proposed_restock": data.get("restock_amounts"),
        "proposed_pricing": data.get("new_pricing"),
        "status": "pending"
    }
    db.proposals.insert_one(proposal)
    return jsonify({"message": "Action proposed and awaiting human approval."}), 201

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')