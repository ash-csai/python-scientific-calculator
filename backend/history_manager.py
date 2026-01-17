# history_manager.py

import sqlite3
from datetime import datetime

DB_FILE = "calculator_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT NOT NULL,
            result TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_history(expression, result):
    # Only store valid calculations (skip errors if you want)
    if str(result).startswith("ERROR"):
        return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO history(expression, result, timestamp)
        VALUES (?, ?, ?)
    ''', (expression, str(result), timestamp))
    conn.commit()
    conn.close()

def get_all_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, expression, result, timestamp FROM history ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows

def search_history(query):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, expression, result, timestamp FROM history WHERE expression LIKE ?", ('%'+query+'%',))
    rows = c.fetchall()
    conn.close()
    return rows

def clear_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM history")
    conn.commit()
    conn.close()

