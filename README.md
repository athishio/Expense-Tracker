# Expense-Tracker-Flask

A lightweight web application for tracking personal expenses, built with Python (Flask) and vanilla JavaScript.

## Overview

This is a minimal expense tracker designed for simplicity:
- **Backend:** A Flask application (`server.py`) that serves the UI and provides two API endpoints:
  - `POST /add_expense`: Appends a new expense entry to a local `expenses.json` file.
  - `GET /get_expenses`: Reads and returns the list of expenses from `expenses.json`.
- **Frontend:** A single-page interface (`templates/index.html`) built with vanilla HTML/CSS/JS to submit new expenses and view logged entries.

## Running Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the server:**
   ```bash
   python server.py
   ```
3. Open `http://localhost:5000` in your browser.

## Persistent Storage (MongoDB Atlas)

To persist expenses in production (e.g. on Vercel), the app connects to **MongoDB Atlas** when the `MONGODB_URI` environment variable is present:

1. Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/atlas).
2. Create a database user and allow network access from anywhere (`0.0.0.0/0`).
3. Copy your connection string (`mongodb+srv://<username>:<password>@cluster0.../expense_tracker?retryWrites=true&w=majority`).
4. Set `MONGODB_URI` in your Vercel Project Settings under **Settings > Environment Variables**.

*If `MONGODB_URI` is not set (e.g. during offline local development), the server automatically falls back to storing entries in `expenses.json`.*
