# utils/db_handler.py
import sqlite3
import csv

def log_trade_db(trade_details, mode):
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    
    # Create table if not exists
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS trades_{mode} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            price REAL,
            signal TEXT,
            quantity INTEGER
        )
    ''')
    
    # Insert trade details
    c.execute(f'''
        INSERT INTO trades_{mode} (symbol, price, signal, quantity)
        VALUES (?, ?, ?, ?)
    ''', (trade_details['symbol'], trade_details['price'], trade_details['signal'], trade_details['quantity']))
    
    conn.commit()
    conn.close()
