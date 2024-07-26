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
