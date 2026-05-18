import streamlit as st
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["stallsync_db"]

st.set_page_config(page_title="StallSync Dashboard", layout="wide")
st.title("🏟️ StallSync: Vendor Operations")

# Sidebar for manual event triggers (to test the agent)
st.sidebar.header("Simulate Event")
if st.sidebar.button("Trigger: Match Delayed by 2 Hours"):
    st.sidebar.warning("Agent is calculating impact...")
    # In a full production app, this button would ping your Agent Builder endpoint.

st.subheader("Pending AI Actions")
proposals = list(db.proposals.find({"status": "pending"}))

if not proposals:
    st.info("No pending actions. Operations are normal.")
else:
    for p in proposals:
        with st.expander(f"Action Required for {p['stall_id']} 🚨"):
            st.write(f"**Reason:** {p['reason']}")
            st.json({"Proposed Restock": p['proposed_restock'], "New Pricing": p['proposed_pricing']})
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve Action", key=f"app_{p['_id']}"):
                    # Execute the MongoDB write
                    db.stalls.update_one(
                        {"stall_id": p['stall_id']},
                        {"$set": {"pricing": p['proposed_pricing']}}
                    )
                    db.proposals.update_one({"_id": p['_id']}, {"$set": {"status": "approved"}})
                    st.success("Action Approved! Database updated.")
                    st.rerun()
            with col2:
                if st.button("❌ Reject", key=f"rej_{p['_id']}"):
                    db.proposals.update_one({"_id": p['_id']}, {"$set": {"status": "rejected"}})
                    st.error("Action Rejected.")
                    st.rerun()