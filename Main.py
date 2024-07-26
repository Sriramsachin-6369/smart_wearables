import RPi.GPIO as GPIO
import time
import mysql.connector

ClassA = ["Alice Johnson", "Bob Smith", "Claire Davis", "David Brown", "Emily Taylor", "Frank Wilson", "Grace Miller", "Henry Anderson", "Iris Harris", "Jack Turner"]
ClassB = ["Kelly Thompson", "Liam Garcia", "Megan Martinez", "Noah Taylor", "Olivia Rodriguez", "Peter Lee", "Quinn White", "Rachel Scott", "Samuel Thomas", "Taylor Hall"]
ClassC = ["Emma Johnson", "Liam Smith", "Olivia Davis", "Noah Brown", "Ava Taylor", "Ethan Wilson", "Sophia Miller", "Jackson Anderson", "Isabella Harris", "Aiden Turner", "Grace Thompson", "Lucas Garcia", "Ella Martinez"]
ClassE = ["Logan Taylor", "Mia Rodriguez", "Oliver Lee", "Amelia White", "Caleb Scott", "Abigail Thomas", "Benjamin Hall"]
ClassX = ["Charlotte Baker", "Mason Lewis", "Harper Moore", "Aiden Evans", "Scarlett Hayes", "Elijah Mitchell", "Zoey Carter"]
ClassY = ["Carter Turner", "Addison Peterson", "William Adams", "Avery Walker", "Evelyn King", "Samuel Richardson", "Lily Cook", "James Foster", "Penelope Bennett", "Lucas Gray", "Aria Cooper", "Dylan Phillips", "Chloe Reed"]
ClassW = ["Sebastian Thompson", "Penelope Cooper", "Samuel Hayes", "Aurora Evans", "Lincoln Foster", "Nora Turner", "Dominic Scott", "Isla Miller", "Jaxon Davis", "Lila Mitchell", "Levi Wilson", "Madeline Reed", "Hunter King"]
ClassZ = ["Ava Garcia", "Benjamin Brooks", "Sadie Foster", "Owen Phillips", "Ivy Harris", "Wyatt Taylor", "Scarlett Walker", "Eliana Smith", "Grayson Robinson", "Hazel Adams", "Oliver Carter", "Ruby King", "Caleb Wright", "Piper Miller"]


# Configure GPIO pins
GPIO.setmode(GPIO.BCM)
STOP_PIN = 22  # GPIO pin 22 for stopping the program
PRESENT_PIN =25 
ABSENT_PIN =27
GPIO.setup(STOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PRESENT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ABSENT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

db_host = "127.0.0.1"
db_user = "root"
db_password = "sriram2002$shan"
db_name = "attendance_system"

# Connect to the MySQL server
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = connection.cursor()

def get_timetable(user_id, day_order):
    # Fetch timetable from MySQL using user_id and day_order
    cursor.execute("SELECT * FROM timetable WHERE employee_id = %s AND day_of_week = %s", (user_id, day_order))
    timetable_data = cursor.fetchall()
    return timetable_data
def get_class_students(class_name):
    # Return the student array based on the class name
    return globals().get(class_name, [])
    
def display_students(class_students):
    print(f"\nClass Students:")
    for student in class_students:
        print(student)

def take_attendance(class_students, class_name, attendance_array):
    print(f"\n{class_name} Students:")
    for student in class_students:
        print(student)

    for i, student_info in enumerate(attendance_array):
        student = student_info[0]
        if GPIO.input(PRESENT_PIN) == GPIO.LOW:
            x=1
        elif GPIO.input(ABSENT_PIN) == GPIO.LOW:
            x=0

        try:
            x = int(x)
            if x == 1:
                attendance_array[i][1] = 'Present'
                print(f"{student} marked as Present.")
            elif x == 0:
                attendance_array[i][1] = 'Absent'
                print(f"{student} marked as Absent.")
            else:
                print("Invalid input. Please enter 1 for present or 0 for absent.")
        except ValueError:
            print("Invalid input. Please enter 1 for present or 0 for absent.")

def wait_for_nfc_confirmation():
    print("Waiting for NFC confirmation...")
    while GPIO.input(NFC_CONFIRM_PIN) == GPIO.HIGH:
        time.sleep(0.1)
    print("NFC confirmation received!")

def update_attendance_in_db(employee_id, class_name, attendance_array):
    for student_info in attendance_array:
        student_name = student_info[0]
        attendance_status = student_info[1]

        # Update attendance in the MySQL server
        query = f"INSERT INTO attendance (employee_id, class_name, present, absent) VALUES (%s, %s, %s, %s)"
        values = (employee_id, class_name, 1 if attendance_status == 'Present' else 0, 1 if attendance_status == 'Absent' else 0)
        cursor.execute(query, values)
        connection.commit()
def main():
    user_id = 1  # Replace with the actual user id
    day_order = 1  # Replace with the actual day order

    try:
        timetable_data = get_timetable(user_id, day_order)

        if not timetable_data:
            print("Timetable data not found.")
            return

        for class_number in range(min(6, len(timetable_data))):
            class_info = timetable_data[class_number]

            # Make sure the indices are within the bounds of the list
            if day_order + 1 < len(class_info):
                class_name = class_info[day_order + 1]  # +1 to skip the user_id column
                print(class_name)
                class_students = get_class_students(class_name)
                start_time = class_info[1]
                end_time = class_info[2]

                if not class_students:
                    print(f"Class {class_name} students not found.")
                    continue

                # Display students for the current class
                display_students(class_students)

                # Take attendance for the current class
                attendance_array = [[student, 'Absent'] for student in class_students]
                take_attendance(class_students, class_name, attendance_array)

                # Wait for NFC confirmation
                wait_for_nfc_confirmation()

                # Update attendance in the database
                update_attendance_in_db(user_id, class_name, attendance_array)

                # Clear attendance_array for the next class
                attendance_array = []

                # Optional: Wait for the next class or end the loop based on time conditions
                # You can use start_time and end_time for time-based conditions

                # Check GPIO pin 22 to see if the program should stop
                if GPIO.input(STOP_PIN) == GPIO.LOW:
                    print("Program stopped by GPIO pin 22.")
                    break
            else:
                print("Invalid index for class_info")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        GPIO.cleanup()
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
