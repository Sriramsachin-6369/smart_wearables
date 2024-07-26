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

            # Write data to the NFC card
            data_to_write = b"Hello, NFC!"
            pn532.ntag2xx_write_block(4, data_to_write)

            print("Data written to the card:", data_to_write)

            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        break
