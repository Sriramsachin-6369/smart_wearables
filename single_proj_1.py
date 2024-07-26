import cv2
import face_recognition
import mysql.connector
import numpy as np
from datetime import datetime
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Define GPIO pins
PIN_22 = 22
PIN_24 = 24
PIN_23 = 23
PIN_25 = 25
PIN_27 = 27

# Setup GPIO input pins
GPIO.setup(PIN_22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main_program():
    print("Main program logic goes here.")

try:
    while True:
        # Check if GPIO pins are pressed
        if GPIO.input(PIN_22) == GPIO.LOW:
            print("22 pin pressed - Back button pressed in main program")
            main_program()

        elif GPIO.input(PIN_24) == GPIO.LOW:
            print("24 pin pressed - Running face recognition for attendance")
            run_face_recognition()

        elif GPIO.input(PIN_23) == GPIO.LOW:
            print("23 pin pressed - Running NFC data transfer")
            run_nfc_data_transfer()

        elif GPIO.input(PIN_25) == GPIO.LOW:
            print("25 pin pressed - Running GPS system")
            run_gps_system()

        elif GPIO.input(PIN_27) == GPIO.LOW:
            print("27 pin pressed - Running student system")
            run_student_system()

        # Add a small delay to avoid rapid button presses
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()


# Connect to MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="sriram2002$shan",
    database="attendance_system"
)
cursor = db.cursor()
day_order= '1'

# Face recognition for attendance
def mark_attendance():
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture each frame
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Ensure the frame is in RGB format
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all face locations and face encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare with known faces in the database
            cursor.execute("SELECT employee_id, employee_name, face_encoding FROM employees")
            employees = cursor.fetchall()

            for employee_id, employee_name, stored_face_encoding in employees:
                stored_face_encoding = np.frombuffer(stored_face_encoding, dtype=np.float64)
                stored_face_encoding = np.reshape(stored_face_encoding, (128,))

                # Check if the face matches
                if face_recognition.compare_faces([stored_face_encoding], face_encoding)[0]:
                    # Mark attendance
                    check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("INSERT INTO attendance (employee_id, check_in_time) VALUES (%s, %s)",
                                   (employee_id, check_in_time))
                    db.commit()
                    
                    cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
                    employee_info = cursor.fetchone()

                    # Fetch timetable info from timetable table
                    cursor.execute("SELECT * FROM timetable WHERE employee_id = %s AND day_of_week = %s", (employee_id, day_order))
        
                    timetable_info = cursor.fetchone()
                   
                    if employee_info and timetable_info:
                        print(f"Attendance registered for {employee_info[1]} (Employee ID: {employee_info[0]}) on day {day_order}.")

                        print(f"Timetable Info: {timetable_info}")
                    else:
                        print("Employee or timetable information not found.")
                    cursor.execute("SELECT * FROM tasks WHERE employee_id = %s", (employee_id,))
                    task_info = cursor.fetchone()
                    if task_info is not None  :
                        print (f"today task: {task_info}")
                    else:
                        print("no task is scheduled")





                    cv2.destroyAllWindows()
                    video_capture.release()
                    db.close()
                    exit()



        # Display the frame
        cv2.imshow('Video', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close windows
    video_capture.release()
    cv2.destroyAllWindows()


# Example usage
mark_attendance()
import serial
import pynmea2
from geopy.distance import geodesic
import math
import time
import mysql.connector

class GPS:
    def __init__(self, port="/dev/ttyAMA0", baudrate=9600):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=0.5)
        self.dataout = pynmea2.NMEAStreamReader()
        self.coord1 = None

    def read_gps_data(self):
        newdata = self.ser.readline()
        n_data = newdata.decode('latin-1')
        if n_data[0:6] == '$GPRMC':
            newmsg = pynmea2.parse(n_data)
            self.coord1 = (newmsg.latitude, newmsg.longitude)

    def calculate_distance(self, coord2):
        if self.coord1 is not None:
            distance = geodesic(self.coord1, coord2).kilometers
            return distance
        return None

    def calculate_direction(self, coord2):
        if self.coord1 is not None:
            lat1, lon1 = self.coord1
            lat2, lon2 = coord2

            delta_lon = lon2 - lon1
            direction = math.atan2(math.sin(math.radians(delta_lon)) * math.cos(math.radians(lat2)),
                                   math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) -
                                   math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(
                                       math.radians(delta_lon)))

            direction = math.degrees(direction)
            direction = (direction + 360) % 360

            return direction
        return None


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="sriram2002$shan",
            database="attendance_system"
        )
        self.cursor = self.connection.cursor()

    def get_destination_coordinates(self, location_name):
        query = "SELECT latitude, longitude FROM destination_coordinates WHERE location_name = %s"
        self.cursor.execute(query, (location_name,))
        result = self.cursor.fetchone()
        return result if result else None


class NavigationSystem:
    def __init__(self, gps, database):
        self.gps = gps
        self.database = database

    def update_navigation_info(self, location_name):
        destination_coords = self.database.get_destination_coordinates(location_name)

        if destination_coords:
            print(f"Destination Coordinates for {location_name}: {destination_coords}")
            while True:
                self.gps.read_gps_data()
                distance = self.gps.calculate_distance(destination_coords)
                direction = self.gps.calculate_direction(destination_coords)

                if distance is not None and direction is not None:
                    print(f"Distance: {distance:.2f} km")
                    print(f"Direction: {direction:.2f} degrees {'⬆️' if direction <= 45 or direction > 315 else '⬈' if 45 < direction <= 135 else '->' if 135 < direction <= 225 else '⬉' if 225 < direction <= 315 else '<-'}")

                time.sleep(1)
        else:
            print(f"Destination coordinates not found for {location_name}.")

if __name__ == "__main__":
    # Replace with your database connection details
    db_instance = Database()
    gps_instance = GPS()
    navigation_system = NavigationSystem(gps_instance, db_instance)

    # Example: Ask the user for a location and update navigation info
    user_input = input("Enter the location (e.g., classroom, lab, library): ")
    navigation_system.update_navigation_info(user_input)
    classA = ["Alice Johnson", "Bob Smith", "Claire Davis", "David Brown", "Emily Taylor", "Frank Wilson", "Grace Miller", "Henry Anderson", "Iris Harris", "Jack Turner"]
classB = ["Kelly Thompson", "Liam Garcia", "Megan Martinez", "Noah Taylor", "Olivia Rodriguez", "Peter Lee", "Quinn White", "Rachel Scott", "Samuel Thomas", "Taylor Hall"]
classC = ["Emma Johnson", "Liam Smith", "Olivia Davis", "Noah Brown", "Ava Taylor", "Ethan Wilson", "Sophia Miller", "Jackson Anderson", "Isabella Harris", "Aiden Turner", "Grace Thompson", "Lucas Garcia", "Ella Martinez"]
classE = ["Logan Taylor", "Mia Rodriguez", "Oliver Lee", "Amelia White", "Caleb Scott", "Abigail Thomas", "Benjamin Hall"]
classX = ["Charlotte Baker", "Mason Lewis", "Harper Moore", "Aiden Evans", "Scarlett Hayes", "Elijah Mitchell", "Zoey Carter"]
classY = ["Carter Turner", "Addison Peterson", "William Adams", "Avery Walker", "Evelyn King", "Samuel Richardson", "Lily Cook", "James Foster", "Penelope Bennett", "Lucas Gray", "Aria Cooper", "Dylan Phillips", "Chloe Reed"]
classW = ["Sebastian Thompson", "Penelope Cooper", "Samuel Hayes", "Aurora Evans", "Lincoln Foster", "Nora Turner", "Dominic Scott", "Isla Miller", "Jaxon Davis", "Lila Mitchell", "Levi Wilson", "Madeline Reed", "Hunter King"]
classZ = ["Ava Garcia", "Benjamin Brooks", "Sadie Foster", "Owen Phillips", "Ivy Harris", "Wyatt Taylor", "Scarlett Walker", "Eliana Smith", "Grayson Robinson", "Hazel Adams", "Oliver Carter", "Ruby King", "Caleb Wright", "Piper Miller"]

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)  # Assuming GPIO 23 for marking 'Present'
GPIO.setup(24, GPIO.IN)  # Assuming GPIO 24 for marking 'Absent'

def take_attendance(class_students):
    attendance_array = [[student, 'Absent'] for student in class_students]

    try:
        print(f"\n{class_name} Students:")
        for student in class_students:
            print(student)

        for i, student_info in enumerate(attendance_array):
            student = student_info[0]
            print(f"Is {student} present? Press GPIO 23 for Yes, GPIO 24 for No.")

            while True:
                 if GPIO.input(23):
                    attendance_array[i][1] = 'Present'
                    print(f"{student} marked as Present.")
                    break
                
                 elif GPIO.input(24):
                    attendance_array[i][1] = 'Absent'
                    print(f"{student} marked as Absent.")
                    break

    except KeyboardInterrupt:
        print(f"Attendance tracking for {class_name} stopped.")
        GPIO.cleanup()

try:
    class_name = input("Enter the class name (A, B, C, E, X, Y, W, Z): ").upper()

    if class_name in {'A', 'B', 'C', 'E', 'X', 'Y', 'W', 'Z'}:
        class_students = globals()[f"class{class_name}"]
        take_attendance(class_students)
    else:
        print("Invalid class name. Please enter A, B, C, E, X, Y, W, Z.")

except KeyboardInterrupt:
    print("Program stopped.")
finally:
    GPIO.cleanup()

import time
import board
from adafruit_pn532.i2c import PN532_I2C

# Initialize I2C communication with the PN532 module
i2c = board.I2C()  # uses board.SCL and board.SDA
pn532 = PN532_I2C(i2c, debug=False)

print("Waiting for an NFC card...")

while True:
    try:
        uid = pn532.read_passive_target(timeout=0.5)
        if uid is not None:
            print("Found NFC card with UID:", [hex(i) for i in uid])

            # Data to write to the NFC card
            data_to_write = b"Hello, NFC!"

            # Pad the data to make it a multiple of 4 bytes
            data_to_write = data_to_write.ljust((len(data_to_write) + 3) // 4 * 4, b'\0')

            # Split the data into chunks of 4 bytes
            for i in range(0, len(data_to_write), 4):
                chunk = data_to_write[i:i+4]
                block_number = (i // 4) + 4  # Starting from block 4
                pn532.ntag2xx_write_block(block_number, chunk)
                print("Wrote data to block", block_number, ":", chunk)

            # Read data from the NFC card
            read_data = b""
            for block_number in range(4, 8):  # Reading blocks 4 to 7
                block_data = pn532.ntag2xx_read_block(block_number)
                if block_data is not None:
                    read_data += block_data
                    print("Read data from block", block_number, ":", block_data)
                else:
                    print("Failed to read data from block", block_number)

            if read_data:
                print("Read data from the card:", read_data.decode("utf-8"))

            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        break
