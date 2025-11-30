import sqlite3
import hashlib
from werkzeug.security import generate_password_hash
import os

# Connect to the database
db_path = 'instance/users.db'
print(f"Database path: {os.path.abspath(db_path)}")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Update the admin password
        admin_email = 'admin@fashionfinds.com'
        new_password = 'admin'
        hashed_password = generate_password_hash(new_password, method="pbkdf2:sha256")
        
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, admin_email))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Password updated successfully for admin user with email: {admin_email}")
        else:
            print(f"No user found with email: {admin_email}")
            
        conn.close()
    except Exception as e:
        print(f"Error updating password: {e}")
else:
    print("Database file not found!")