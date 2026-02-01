from flask import Flask, render_template, request, jsonify
import json
import os
app = Flask(__name__)
def save_to_file(new_expense):
    filename = "expenses.json"
    expenses_list = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                expenses_list = json.load(f)
            except:
                expenses_list = []
    expenses_list.append(new_expense)
    with open(filename, "w") as f:
        json.dump(expenses_list, f, indent=4)
def load_from_file():
    filename = "expenses.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except:
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
    return jsonify({"status": "success", "message": "Saved!"}
@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    data = load_from_file()
    return jsonify(data)
if __name__ == '__main__':
    app.run(debug=True)