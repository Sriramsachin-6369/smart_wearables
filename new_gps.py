
import serial
import pynmea2
from geopy.distance import geodesic
import math
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
import RPi.GPIO as GPIO
import time
import mysql.connector
import board
import busio
from PIL import Image, ImageDraw, ImageFont


def display_text(text,text2):
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((0, 0), text, fill="white")
    draw.text((0, 20), text2, fill="white")
    oled.display(image)
    time.sleep(2)

def read_gps_data(ser):
    newdata = ser.readline()
    n_data = newdata.decode('latin-1')
    if n_data[0:6] == '$GPRMC':
        newmsg = pynmea2.parse(n_data)
        return newmsg.latitude, newmsg.longitude
    return None

def calculate_distance(coord1, coord2):
    if coord1 is not None:
        distance = geodesic(coord1, coord2).kilometers
        return distance
    return None

def calculate_direction(coord1, coord2):
    if coord1 is not None:
        lat1, lon1 = coord1
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

def get_destination_coordinates(connection, location_name):
    cursor = connection.cursor()
    query = "SELECT latitude, longitude FROM destination_coordinates WHERE location_name = %s"
    cursor.execute(query, (location_name,))
    result = cursor.fetchone()
    cursor.close()
    return result if result else None


def update_navigation_info(gps, connection, location_name):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    destination_coords = get_destination_coordinates(connection, location_name)

    if destination_coords:
        print(f"Destination Coordinates for {location_name}: {destination_coords}")
        while True:
            coord1 = read_gps_data(gps)
            distance = calculate_distance(coord1, destination_coords)
            direction = calculate_direction(coord1, destination_coords)

            if coord1 is not None and distance is not None and direction is not None:
                print(f"Distance: {distance:.2f} km")
               
                
                print(f"Direction: {direction:.2f} degrees {'⬆️' if direction <= 45 or direction > 315 else '⬈' if 45 < direction <= 135 else '->' if 135 < direction <= 225 else '⬉' if 225 < direction <= 315 else '<-'}")
                display_text(f"Distance: {distance:.2f} km",f"Direction: {direction:.2f} degrees {'⬆️' if direction <= 45 or direction > 315 else '⬈' if 45 < direction <= 135 else '->' if 135 < direction <= 225 else '⬉' if 225 < direction <= 315 else '<-'}")
            time.sleep(1)
            if GPIO.input(22) == GPIO.LOW:
                print("exit")
                break
                
    else:
        print(f"Destination coordinates not found for {location_name}.")

def update_display():
    # Select button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Up button
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Down button
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
     
    # Initialize OLED
    
   

    # Initial data and index
    data = ["lab", "classroom", "playground", "library", "food court"]
    selected_index = 0
    


    try:
        while True:
            if GPIO.input(23) == GPIO.LOW:  # Up button pressed
                selected_index = (selected_index - 1) % len(data)
                
                display_text(data[selected_index]," ")
            elif GPIO.input(25) == GPIO.LOW:  # Down button pressed
                selected_index = (selected_index + 1) % len(data)
                display_text(data[selected_index]," ")
            elif GPIO.input(27) == GPIO.LOW:  # Select button pressed
                user_input = data[selected_index]
                print(f"Selected: {user_input}")
                display_text(f"Selected: {user_input}"," ")
                return user_input  # Return the selected data
            elif GPIO.input(22) == GPIO.LOW:
                print("exit")
                break
    except Exception as e:
        print(f"An error occurred: {e}")
      

def gps_dis(db):
    db_connection = db
    gps_port = "/dev/ttyAMA0"
    gps_baudrate = 9600
    gps_ser = serial.Serial(gps_port, baudrate=gps_baudrate, timeout=0.5)

    selected_location = update_display()
    update_navigation_info(gps_ser, db_connection, selected_location)
    return()

i2c_oled = i2c(port=1, address=0x3C)
oled = ssd1306(i2c_oled, width=128, height=32)
