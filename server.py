from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Connect to MongoDB if MONGODB_URI is provided in environment, otherwise use local JSON file
MONGODB_URI = os.environ.get("MONGODB_URI")
db = None
if MONGODB_URI:
    try:
        from pymongo import MongoClient
        client = MongoClient(MONGODB_URI)
        # Use default database from URI, or fall back to 'expense_tracker' database
        try:
            db = client.get_default_database()
        except Exception:
            db = client["expense_tracker"]
        if db is None:
            db = client["expense_tracker"]
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        db = None

def save_to_file(new_expense):
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

if __name__ == '__main__':
    app.run(debug=True)