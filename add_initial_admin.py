import sqlite3
from werkzeug.security import generate_password_hash
import os

# Connect to the database
db_path = 'instance/users.db'
print(f"Database path: {os.path.abspath(db_path)}")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the admin user already exists
        admin_email = 'admin_A0001@fashionfinds.com'
        cursor.execute("SELECT id FROM users WHERE email = ?", (admin_email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"Admin user with email {admin_email} already exists.")
        else:
            # Create the initial admin user
            admin_password = 'FF_A0001'
            hashed_password = generate_password_hash(admin_password, method="pbkdf2:sha256")
            
            # Insert the new admin user
            cursor.execute("""
                INSERT INTO users (custom_id, name, phone, email, password, address, state, city, pincode, role, approved) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'A0001',           # custom_id
                'Initial Admin',   # name
                '9999999999',      # phone
                admin_email,       # email
                hashed_password,   # password
                'Admin Address',   # address
                'Admin State',     # state
                'Admin City',      # city
                '123456',          # pincode
                'admin',           # role
                1                  # approved
            ))
            
            conn.commit()
            print(f"Initial admin user created successfully with email: {admin_email} and password: {admin_password}")
            
        conn.close()
    except Exception as e:
        print(f"Error creating admin user: {e}")
else:
    print("Database file not found!")