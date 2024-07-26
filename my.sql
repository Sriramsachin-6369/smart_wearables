CREATE DATABASE attendance_system;

USE attendance_system;
DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_name VARCHAR(255) NOT NULL,
    face_encoding BLOB NOT NULL
);

DROP TABLE IF EXISTS attendance;
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    check_in_time DATETIME,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
ALTER TABLE attendance
ADD CONSTRAINT attendance_ibfk_1
FOREIGN KEY (employee_id)
REFERENCES employees(employee_id);
SELECT * FROM attendance;
SELECT * FROM employees;
TRUNCATE TABLE attendance;


-- Table to store tasks
CREATE TABLE Task (
    TaskID INT PRIMARY KEY,
    TaskName VARCHAR(100),
    TaskDescription TEXT
);

-- Table to store the timetable for each employee
DROP TABLE IF EXISTS timetable;
CREATE TABLE timetable (
    employee_id INT NOT NULL,
    day_of_week INT NOT NULL,
    hour_10 VARCHAR(255),
    hour_11 VARCHAR(255),
    hour_12 VARCHAR(255),
    hour_13 VARCHAR(255),
    hour_14 VARCHAR(255),
    hour_15 VARCHAR(255),
    hour_16 VARCHAR(255),
	FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);


-- Table to store task assignments
CREATE TABLE TaskAssignment (
    AssignmentID INT PRIMARY KEY,
    employee_id INT,
    TaskID INT,
    AssignmentDate DATE,  
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (TaskID) REFERENCES Task(TaskID)
);

CREATE TABLE tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    task_description VARCHAR(255),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);




-- Insert sample data into the Task table
INSERT INTO taskS (employee_id, task_description)
VALUES
(1 , 'Project A Develop new software'),
( 2 , 'Meeting Team meeting at 10 AM'),
( 3 , 'Report Generate monthly sales report');

-- Insert sample data into the Timetable table
INSERT INTO timetable (employee_id, day_of_week, hour_10, hour_11, hour_12, hour_13, hour_14, hour_15)
VALUES
(1, 1,'ClassA', 'ClassB', 'ClassC', NULL, 'ClassE', NULL),
(2, 1,'ClassX', 'ClassY', NULL, NULL, NULL, 'ClassW' ),
(3, 1,'ClassB','ClassY',NULL,NULL,'CLassW','classA'),
(4, 1,'ClassC','CLassZ','ClassY',NULL,'CLassA',NULL),
(2, 2,'ClassA', 'ClassB', 'ClassC', NULL, 'ClassE', NULL),
(3, 2,'ClassX', 'ClassY', NULL, NULL, NULL, 'ClassW' ),
(4, 2,'ClassB','ClassY',NULL,NULL,'CLassW','classA'),
(1, 2,'ClassC','CLassZ','ClassY',NULL,'CLassA',NULL),
(2, 3,'ClassB','ClassY',NULL,NULL,'CLassW','classA'),
(3, 3,'ClassC','CLassZ','ClassY',NULL,'CLassA',NULL),
(4, 3,'ClassA', 'ClassB', 'ClassC', NULL, 'ClassE', NULL),
(1, 3,'ClassX', 'ClassY', NULL, NULL, NULL, 'ClassW' ),
(2, 4,'ClassC','CLassZ','ClassY',NULL,'CLassA',NULL),
(3, 4,'ClassA', 'ClassB', 'ClassC', NULL, 'ClassE', NULL),
(4, 4,'ClassX', 'ClassY', NULL, NULL, NULL, 'ClassW' ),
(1, 4,'ClassB','ClassY',NULL,NULL,'CLassW','classA');

SELECT * FROM timetable;
CREATE TABLE destination_coordinates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL
);
-- Example data insertion
 INSERT INTO destination_coordinates (location_name, latitude, longitude) VALUES
('libary', 10.937410835578897, 76.95917052864316),
('lab', 10.937470509311206, 76.9594246088394),
('foodcort',10.937710117542789, 76.9598415892788),
('playground',10.9369597108818, 76.95761399349702),
('classroom',10.937724461718988, 76.95910714567128);
SELECT * FROM destination_coordinates;
ALTER TABLE tasks 
    MODIFY COLUMN employee_id INT NOT NULL,
    ADD FOREIGN KEY (employee_id) REFERENCES employees(employee_id);

CREATE TABLE IF NOT EXISTS student_Attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    student_name VARCHAR(255) NOT NULL,
    status ENUM('Present', 'Absent') NOT NULL,
    attendance_date DATE NOT NULL
);
SELECT * FROM student_Attendance;