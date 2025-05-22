import sqlite3
import functools
from datetime import datetime

### decorator to lof SQL queries

def log_queries(fun):
    def wrapper(*args,**kwargs):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"now {now} query log {args[0]}")
        return fun(*args,**kwargs)       
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
