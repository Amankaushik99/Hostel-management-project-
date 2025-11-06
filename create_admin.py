#!/usr/bin/env python3
"""
Create Admin User Script
Run this script to create an admin user for the system
"""

import pymysql
import getpass
from config import Config

def create_admin():
    """Create an admin user interactively"""
    
    print("🔐 Admin User Creation")
    print("=" * 30)
    
    # Get admin details from user input
    admin_id = input("Enter Admin ID: ").strip()
    if not admin_id:
        print("❌ Admin ID cannot be empty!")
        return False
    
    name = input("Enter Admin Name: ").strip()
    if not name:
        print("❌ Admin name cannot be empty!")
        return False
    
    email = input("Enter Admin Email: ").strip()
    
    # Get password securely
    password = getpass.getpass("Enter Admin Password: ")
    if len(password) < 6:
        print("❌ Password must be at least 6 characters!")
        return False
    
    confirm_password = getpass.getpass("Confirm Password: ")
    if password != confirm_password:
        print("❌ Passwords do not match!")
        return False
    
    try:
        # Connect to database
        conn = pymysql.connect(**Config.DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT admin_id FROM admin WHERE admin_id = %s", (admin_id,))
        if cursor.fetchone():
            print(f"❌ Admin with ID '{admin_id}' already exists!")
            conn.close()
            return False
        
        # Insert new admin
        cursor.execute("""
            INSERT INTO admin (admin_id, name, email, password)
            VALUES (%s, %s, %s, %s)
        """, (admin_id, name, email, password))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Admin user '{admin_id}' created successfully!")
        print(f"📧 Email: {email}")
        print("\n🚀 You can now login to the admin panel!")
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    create_admin()