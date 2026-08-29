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

## Deployment Note

The repository includes a `vercel.json` configuration for deploying to Vercel. However, because Vercel's serverless functions use an ephemeral filesystem between invocations, data written to the local `expenses.json` file will not persist reliably across requests or redeployments on the live deployment.

For reliable production use, the local JSON file storage should be migrated to a lightweight hosted database (e.g., PostgreSQL, Supabase, or MongoDB) before advertising persistent storage.
