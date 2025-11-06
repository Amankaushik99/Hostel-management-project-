-- Hostel Management System Database Setup
-- Run: mysql -u root -p < database.sql

DROP DATABASE IF EXISTS student_hostel;
CREATE DATABASE student_hostel;
USE student_hostel;

-- Students table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    room_number VARCHAR(20) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    password VARCHAR(255) NOT NULL
);

-- Faculty table
CREATE TABLE faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    password VARCHAR(255) NOT NULL
);

-- Admin table
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Pass requests table
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
);

-- Attendance table
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    check_in_time DATETIME,
    check_out_time DATETIME,
    status VARCHAR(20) DEFAULT 'present',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    UNIQUE KEY unique_student_date (student_id, date)
);

-- Insert sample data
INSERT INTO students (student_id, name, room_number, phone, email, password) VALUES
('STU001', 'John Doe', 'A101', '9876543210', 'john@example.com', 'password123'),
('STU002', 'Jane Smith', 'A102', '9876543211', 'jane@example.com', 'password123'),
('STU003', 'Mike Johnson', 'B201', '9876543212', 'mike@example.com', 'password123');

INSERT INTO faculty (faculty_id, name, department, password) VALUES
('FAC001', 'Dr. Sarah Wilson', 'Computer Science', 'faculty123'),
('FAC002', 'Prof. Robert Brown', 'Mathematics', 'faculty123');

INSERT INTO admin (admin_id, name, email, password) VALUES
('aman', 'Aman Administrator', 'aman@hostel.com', '1234');
