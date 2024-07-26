import cv2
import face_recognition
import mysql.connector
import numpy as np
from datetime import datetime

# Connect to MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="sriram2002$shan",
    database="attendance_system"
)
cursor = db.cursor()

# Capture and store face encodings
def capture_face_encoding(employee_name, image_path):
    image = face_recognition.load_image_file(image_path)
    # Change this line in the capture_face_encoding function
    face_encoding = face_recognition.face_encodings(image)[0].tobytes()


    # Insert into the database
    cursor.execute("INSERT INTO employees (employee_name, face_encoding) VALUES (%s, %s)",
                   (employee_name, face_encoding))
    db.commit()

# Example usage
capture_face_encoding("surya", "surya_face.png")
