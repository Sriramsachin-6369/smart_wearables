import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Define the reset pin (or set to None if not used):
RESET_PIN = None

# Define the I2C bus and OLED object:
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=RESET_PIN)

# Clear the OLED display buffer:
oled.fill(0)
oled.show()

# Create blank image for drawing:
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load default font:
font = ImageFont.load_default()

# Draw some text:
draw.text((0, 0), "Hello, Pi Zero!", font=font, fill=255)

# Display image on the OLED:
oled.image(image)
oled.show()
##############################################################################################################
def display_text(text):
    # Clear the OLED display buffer:
    oled.fill(0)
    oled.show()

    # Create blank image for drawing:
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    # Load default font:
    font = ImageFont.load_default()

    # Draw some text:
    draw.text((0, 0), text, font=font, fill=255)

    # Display image on the OLED:
    oled.image(image)
    oled.show()