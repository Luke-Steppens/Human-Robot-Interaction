import serial
import time

import serial
import time

"""
Arduino control
- python sends mv (movement) number (-2 to +2) over serial
- arduino reads mv
- servos tilt the plate
- ball moves to assigned corner
"""

class ArduinoController:
    def __init__(self, port: str, baud: int = 115200):
        self.ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2)

    def send_cmd(self, cmd: int):
        # cmd should be 2, 1, -1, or -2
        self.ser.write(f"{cmd}\n".encode("utf-8"))

    def close(self):
        self.ser.close()

