CREATE DATABASE IF NOT EXISTS study_sync;
USE study_sync;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS contact_messages;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS time_slots;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'lecturer', 'admin') NOT NULL DEFAULT 'student',
    phone VARCHAR(30) DEFAULT NULL,
    bio TEXT DEFAULT NULL,
    department VARCHAR(100) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    lecturer_id INT NOT NULL,
    category VARCHAR(80) NOT NULL DEFAULT 'General',
    location VARCHAR(120) NOT NULL DEFAULT 'Online',
    duration_minutes INT NOT NULL DEFAULT 60,
    status ENUM('active', 'archived') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_class_lecturer FOREIGN KEY (lecturer_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE time_slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    max_capacity INT NOT NULL DEFAULT 10,
    status ENUM('open', 'full', 'cancelled') NOT NULL DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_slot_class FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    slot_id INT NOT NULL,
    status ENUM('confirmed', 'cancelled') NOT NULL DEFAULT 'confirmed',
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_booking_student FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_booking_slot FOREIGN KEY (slot_id) REFERENCES time_slots(id) ON DELETE CASCADE,
    CONSTRAINT unique_student_slot UNIQUE (student_id, slot_id)
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL UNIQUE,
    marked_by INT NOT NULL,
    status ENUM('present', 'absent', 'late') NOT NULL DEFAULT 'present',
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_attendance_booking FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    CONSTRAINT fk_attendance_marker FOREIGN KEY (marked_by) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    is_read TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notification_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Placeholder hashes — run: python scripts/seed_users.py
INSERT INTO users (name, email, password_hash, role, department) VALUES
('Dr. Sarah Chen', 'lecturer@studysync.app', 'REPLACE_WITH_LECTURER_HASH', 'lecturer', 'Computer Science'),
('Platform Admin', 'admin@studysync.app', 'REPLACE_WITH_ADMIN_HASH', 'admin', 'Operations');

INSERT INTO classes (title, description, lecturer_id, category, location, duration_minutes) VALUES
('Data Structures Masterclass', 'Deep dive into trees, graphs, and algorithmic efficiency.', 1, 'Computer Science', 'Room 204', 90),
('Academic Writing Workshop', 'Structure essays and research papers with confidence.', 1, 'Writing', 'Library Hall B', 60),
('Python for Beginners', 'Hands-on introduction to Python programming fundamentals.', 1, 'Programming', 'Lab 3', 120);

INSERT INTO time_slots (class_id, start_time, end_time, max_capacity) VALUES
(1, '2026-07-08 10:00:00', '2026-07-08 11:30:00', 20),
(1, '2026-07-15 10:00:00', '2026-07-15 11:30:00', 20),
(2, '2026-07-09 14:00:00', '2026-07-09 15:00:00', 15),
(3, '2026-07-10 09:00:00', '2026-07-10 11:00:00', 25),
(3, '2026-07-17 09:00:00', '2026-07-17 11:00:00', 25);
