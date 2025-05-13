CREATE DATABASE IF NOT EXISTS JMS;
USE JMS;

-- Create Cells Table first (since Inmates references it)
CREATE TABLE cells (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cell_number VARCHAR(20) UNIQUE NOT NULL,
    capacity INT NOT NULL,
    current_occupancy INT DEFAULT 0
);

-- Create Users Table (Admin & Jailer)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'jailer') NOT NULL,
    last_notification_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Inmates Table (references cells)
CREATE TABLE inmates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    crime VARCHAR(255) NOT NULL,
    sentence_duration VARCHAR(50) NOT NULL,
    admission_date DATE NOT NULL,
    release_date DATE,
    status ENUM('Active', 'Released') DEFAULT 'Active',
    cell_id INT,
    FOREIGN KEY (cell_id) REFERENCES cells(id)
);

-- Create Visitors Table (references inmates)
CREATE TABLE visitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inmate_id INT NOT NULL,
    visitor_name VARCHAR(100) NOT NULL,
    relation VARCHAR(100) NOT NULL,
    visit_date DATE NOT NULL,
    FOREIGN KEY (inmate_id) REFERENCES inmates(id)
);

-- Create Punishments Table (references inmates)
CREATE TABLE punishments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inmate_id INT NOT NULL,
    punishment_detail TEXT NOT NULL,
    date_given DATE NOT NULL,
    FOREIGN KEY (inmate_id) REFERENCES inmates(id)
);

-- Create Transfers Table (references inmates)
CREATE TABLE transfers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inmate_id INT NOT NULL,
    from_cell VARCHAR(50) NOT NULL,
    to_cell VARCHAR(50) NOT NULL,
    transfer_date DATE NOT NULL,
    FOREIGN KEY (inmate_id) REFERENCES inmates(id)
);

-- Create Notifications Table (standalone)
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Visit Requests Table (standalone)
CREATE TABLE visit_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    visitor_name VARCHAR(100) NOT NULL,
    inmate_name VARCHAR(100) NOT NULL,
    date_requested DATE NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending'
);

-- Create Alerts Table (references inmates)
CREATE TABLE alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inmate_id INT,
    alert_type ENUM('Release', 'Medical', 'Security') NOT NULL,
    alert_date DATE,
    message TEXT,
    status ENUM('Active', 'Resolved') DEFAULT 'Active',
    FOREIGN KEY (inmate_id) REFERENCES inmates(id)
);
