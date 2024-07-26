from datetime import datetime
import RPi.GPIO as GPIO
import time
import mysql.connector
from display import display_text
from face_reco import mark_attendance 
from new_gps import gps_dis

current_datetime = datetime.now()
# Format the date and time as a string in 12-hour format
formatted_datetime = current_datetime.strftime("%I:%M:%S %p  %Y-%m-%d")

global db, cursor
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="sriram2002$shan",
    database="attendance_system"
)
cursor = db.cursor()

# GPIO setup function
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    
    # Define GPIO pins
    global PIN_22, PIN_24, PIN_23, PIN_25, PIN_27
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



def main():
    setup_gpio()
    try:
        while True:
            if GPIO.input(PIN_22) == GPIO.LOW:
                print("22 pin pressed - Back button pressed.")
            elif GPIO.input(PIN_24) == GPIO.LOW:
                attendance=mark_attendance(db,cursor)
                display_text(attendance)
            elif GPIO.input(PIN_23) == GPIO.LOW:
                gps_dis(db=db)
            elif GPIO.input(PIN_25) == GPIO.LOW:
                
            elif GPIO.input(PIN_27) == GPIO.LOW:
                run_student_system()
            time.sleep(0.1)
    except :
        display_text(formatted_datetime)
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main