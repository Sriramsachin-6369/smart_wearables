import cv2
import face_recognition
import numpy as np
import RPi.GPIO as GPIO
from datetime import datetime


day_order= '1'

# Face recognition for attendance
def mark_attendance(db,cursor):
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
                   
                    if employee_info and timetable_info and task_info :
                        print(f"Attendance registered for {employee_info[1]} (Employee ID: {employee_info[0]}) on day {day_order}.")


                        print(f"Timetable Info: {timetable_info}")
                    else:
                        print("Employee or timetable information not found.")
                    
                    task_info = cursor.fetchone()
                    if task_info is not None  :
                        print (f"today task: {task_info}")
                    else:
                        print("no task is scheduled")
                    cv2.destroyAllWindows()
                    video_capture.release()
                    db.close()
                    exit()
                return employee_info,timetable_info,task_info   

                   
                    



        # Display the frame
        cv2.imshow('Video', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q') or GPIO.input(22) == GPIO.LOW:
         break
            

    # Release the video capture object and close windows
    video_capture.release()
    cv2.destroyAllWindows()


