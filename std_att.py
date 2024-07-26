import RPi.GPIO as GPIO

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
