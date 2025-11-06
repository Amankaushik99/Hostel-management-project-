#!/usr/bin/env python3
"""
Remove Sample Data Script
Run this script to remove sample/demo data before production deployment
"""

import pymysql
from config import Config

def remove_sample_data():
    """Remove all sample data from the database"""
    
    print("🧹 Removing Sample Data")
    print("=" * 30)
    
    # Confirm action
    confirm = input("⚠️  This will remove ALL sample data. Continue? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("❌ Operation cancelled.")
        return False
    
    try:
        # Connect to database
        conn = pymysql.connect(**Config.DB_CONFIG)
        cursor = conn.cursor()
        
        # Remove sample data (keep structure)
        print("🗑️  Removing sample students...")
        cursor.execute("DELETE FROM students WHERE student_id LIKE 'STU%'")
        students_removed = cursor.rowcount
        
        print("🗑️  Removing sample faculty...")
        cursor.execute("DELETE FROM faculty WHERE faculty_id LIKE 'FAC%'")
        faculty_removed = cursor.rowcount
        
        print("🗑️  Removing related attendance records...")
        cursor.execute("DELETE FROM attendance")
        attendance_removed = cursor.rowcount
        
        print("🗑️  Removing related pass requests...")
        cursor.execute("DELETE FROM pass_requests")
        requests_removed = cursor.rowcount
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("\n✅ Sample data removal completed!")
        print(f"📊 Removed: {students_removed} students, {faculty_removed} faculty")
        print(f"📊 Removed: {attendance_removed} attendance records, {requests_removed} pass requests")
        print("\n🚀 Database is now ready for production!")
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    remove_sample_data()