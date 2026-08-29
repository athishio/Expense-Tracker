from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

def get_db():
    uri = os.environ.get("MONGODB_URI")
    if not uri:
        return None, "MONGODB_URI environment variable is not set"
    try:
        from pymongo import MongoClient
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        try:
            db = client.get_default_database()
        except Exception:
            db = client["expense_tracker"]
        if db is None:
            db = client["expense_tracker"]
        return db, None
    except Exception as e:
        return None, str(e)

def save_to_file(new_expense):
    db, err = get_db()
    if db is not None:
        try:
            db.expenses.insert_one(dict(new_expense))
            return
        except Exception as e:
            print(f"MongoDB write error: {e}")

    filename = "expenses.json"
    expenses_list = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                expenses_list = json.load(f)
            except Exception:
                expenses_list = []
    expenses_list.append(new_expense)
    with open(filename, "w") as f:
        json.dump(expenses_list, f, indent=4)

def load_from_file():
    db, err = get_db()
    if db is not None:
        try:
            return list(db.expenses.find({}, {"_id": 0}))
        except Exception as e:
            print(f"MongoDB read error: {e}")

    filename = "expenses.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    print("Received Data:", data)
    save_to_file(data)
    return jsonify({"status": "success", "message": "Saved!"})

@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    data = load_from_file()
    return jsonify(data)

@app.route('/api/status', methods=['GET'])
def api_status():
    uri = os.environ.get("MONGODB_URI")
    if not uri:
        return jsonify({
            "mongodb_configured": False,
            "message": "MONGODB_URI environment variable is NOT set in Vercel."
        })
    try:
        from pymongo import MongoClient
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db, _ = get_db()
        count = db.expenses.count_documents({})
        return jsonify({
            "mongodb_configured": True,
            "mongodb_connected": True,
            "total_expenses_in_db": count,
            "message": "MongoDB is successfully connected and working!"
        })
    except Exception as e:
        return jsonify({
            "mongodb_configured": True,
            "mongodb_connected": False,
            "error": str(e),
            "hint": "Check: 1. Is the password correct? 2. Are special characters in password URL-encoded? 3. Is Network Access set to 0.0.0.0/0?"
        })

if __name__ == '__main__':
    app.run(debug=True)
