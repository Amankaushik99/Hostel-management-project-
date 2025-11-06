#!/usr/bin/env python3
"""
Database Setup Script - Fix the leave_type column issue
"""

import pymysql
from config import Config

# Database Configuration from environment variables
DB_CONFIG = {
    'host': Config.DB_CONFIG['host'],
    'port': Config.DB_CONFIG['port'],
    'user': Config.DB_CONFIG['user'],
    'password': Config.DB_CONFIG['password'],
    'charset': Config.DB_CONFIG['charset']
}

def setup_database():
    try:
        print("🔧 Setting up database...")
        
        # Connect to MySQL server (without database)
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Drop and create database
        print("📋 Creating database...")
        cursor.execute(f"DROP DATABASE IF EXISTS {Config.DB_CONFIG['database']}")
        cursor.execute(f"CREATE DATABASE {Config.DB_CONFIG['database']}")
        cursor.execute(f"USE {Config.DB_CONFIG['database']}")
        
        # Create students table
        print("👥 Creating students table...")
        cursor.execute("""
            CREATE TABLE students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                room_number VARCHAR(20) NOT NULL,
                phone VARCHAR(15),
                email VARCHAR(100),
                password VARCHAR(255) NOT NULL
            )
        """)
        
        # Create faculty table
        print("👨‍🏫 Creating faculty table...")
        cursor.execute("""
            CREATE TABLE faculty (
                id INT AUTO_INCREMENT PRIMARY KEY,
                faculty_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                password VARCHAR(255) NOT NULL
            )
        """)
        
        # Create pass_requests table with leave_type column
        print("📝 Creating pass_requests table...")
        cursor.execute("""
            CREATE TABLE pass_requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(50) NOT NULL,
                leave_type VARCHAR(50) NOT NULL DEFAULT 'other',
                reason TEXT NOT NULL,
                from_date DATE NOT NULL,
                to_date DATE NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                approved_by VARCHAR(50),
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)
        
        # Create admin table
        print("👑 Creating admin table...")
        cursor.execute("""
            CREATE TABLE admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                admin_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                password VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create attendance table
        print("📊 Creating attendance table...")
        cursor.execute("""
            CREATE TABLE attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(50) NOT NULL,
                date DATE NOT NULL,
                check_in_time DATETIME,
                check_out_time DATETIME,
                status VARCHAR(20) DEFAULT 'present',
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                UNIQUE KEY unique_student_date (student_id, date)
            )
        """)
        
        # Insert sample students
        print("👤 Adding sample students...")
        students_data = [
            ('STU001', 'John Doe', 'A101', '9876543210', 'john@example.com', 'password123'),
            ('STU002', 'Jane Smith', 'A102', '9876543211', 'jane@example.com', 'password123'),
            ('STU003', 'Mike Johnson', 'B201', '9876543212', 'mike@example.com', 'password123')
        ]
        
        for student in students_data:
            cursor.execute("""
                INSERT INTO students (student_id, name, room_number, phone, email, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, student)
        
        # Insert sample faculty
        print("👨‍🏫 Adding sample faculty...")
        faculty_data = [
            ('FAC001', 'Dr. Sarah Wilson', 'Computer Science', 'faculty123'),
            ('FAC002', 'Prof. Robert Brown', 'Mathematics', 'faculty123')
        ]
        
        for faculty in faculty_data:
            cursor.execute("""
                INSERT INTO faculty (faculty_id, name, department, password)
                VALUES (%s, %s, %s, %s)
            """, faculty)
        
        # Insert default admin
        print("👑 Adding default admin...")
        cursor.execute("""
            INSERT INTO admin (admin_id, name, email, password)
            VALUES (%s, %s, %s, %s)
        """, ('aman', 'Aman Administrator', 'aman@hostel.com', '1234'))
        
        # Commit all changes
        conn.commit()
        
        # Verify the table structure
        print("🔍 Verifying table structure...")
        cursor.execute("DESCRIBE pass_requests")
        columns = cursor.fetchall()
        
        print("\n📊 pass_requests table structure:")
        for column in columns:
            print(f"   {column[0]} - {column[1]}")
        
        # Check if leave_type column exists
        leave_type_exists = any(col[0] == 'leave_type' for col in columns)
        
        if leave_type_exists:
            print("\n✅ SUCCESS: leave_type column exists!")
        else:
            print("\n❌ ERROR: leave_type column missing!")
        
        conn.close()
        
        print("\n🎉 Database setup completed successfully!")
        print("\n📋 Sample Login Credentials:")
        print("Students: STU001/password123, STU002/password123, STU003/password123")
        print("Faculty: FAC001/faculty123, FAC002/faculty123")
        print("Admin: aman/1234")
        print("\n🚀 You can now run: python app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

if __name__ == '__main__':
    setup_database()