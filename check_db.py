import sqlite3
import os

# Check if database exists
db_path = 'instance/users.db'
print(f"Database path: {os.path.abspath(db_path)}")
print(f"Database exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in database:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check users table structure
        cursor.execute("PRAGMA table_info(users);")
        columns = cursor.fetchall()
        print("\nUsers table structure:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Check users data
        cursor.execute("SELECT id, custom_id, name, email, password, role FROM users;")
        users = cursor.fetchall()
        print("\nUsers in database:")
        for user in users:
            print(f"  - ID: {user[0]}, Custom ID: {user[1]}, Name: {user[2]}, Email: {user[3]}, Password: {user[4][:20]}..., Role: {user[5]}")
            
        conn.close()
    except Exception as e:
        print(f"Error accessing database: {e}")
else:
    print("Database file not found!")