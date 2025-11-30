import sqlite3
import os

# Connect to the database
db_path = 'instance/users.db'
print(f"Database path: {os.path.abspath(db_path)}")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check the admin user
        admin_email = 'admin_A0001@fashionfinds.com'
        cursor.execute("SELECT id, custom_id, name, email, role FROM users WHERE email = ?", (admin_email,))
        rows = cursor.fetchall()
        print('Admin user details:')
        for row in rows:
            print(f'  - ID: {row[0]}, Custom ID: {row[1]}, Name: {row[2]}, Email: {row[3]}, Role: {row[4]}')
        
        conn.close()
    except Exception as e:
        print(f"Error accessing database: {e}")
else:
    print("Database file not found!")