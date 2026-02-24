
import json
import os

# ---------------- BASE DB FILE ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "db", "upi_mandates.json"))

def load_data():
    """Load mandates from JSON file."""
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """Save mandates to JSON file."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ---------------- MCP TOOLS ----------------
def get_all_mandates():
    """Return all mandates with basic info."""
    data = load_data()
    return {
        "mandates": [
            {
                "mandate_id": m["mandate_id"],
                "mandate_name": m["mandate_name"],
                "status": m["status"]
            }
            for m in data
        ]
    }

def get_mandate_details(query: str):
    """Search mandates by name, ID, or phone number."""
    query = query.lower()
    matches = [
        m for m in load_data()
        if query in m["mandate_name"].lower()
        or query in m["mandate_id"].lower()
        or query in m["phone_no"]
    ]
    return {"matches": matches} if matches else {"matches": []}

def pause_mandate(query: str):
    """Set mandate status to 'paused'."""
    data = load_data()
    updated = []

    for m in data:
        if query.lower() in json.dumps(m).lower():
            m["status"] = "paused"
            updated.append(m)

    save_data(data)
    return {"success": bool(updated), "updated": updated}

def unpause_mandate(query: str):
    """Set mandate status back to 'active'."""
    data = load_data()
    updated = []

    for m in data:
        if query.lower() in json.dumps(m).lower():
            m["status"] = "active"
            updated.append(m)

    save_data(data)
    return {"success": bool(updated), "updated": updated}

def revoke_mandate(query: str):
    """Set mandate status to 'revoked' without deleting."""
    data = load_data()
    updated = []

    for m in data:
        if query.lower() in json.dumps(m).lower():
            m["status"] = "revoked"
            updated.append(m)

    save_data(data)
    return {"success": bool(updated), "updated": updated}

# ---------------- DEBUG ----------------
print("MCP SERVER DB PATH:", DB_FILE)

