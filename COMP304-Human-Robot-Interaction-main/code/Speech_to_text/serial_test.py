from arduino_control import ArduinoController
import time

arduino = ArduinoController("COM4")  #  always check com on arduino first!!!!!

arduino.send_position(1)
time.sleep(2)

arduino.send_position(2)
time.sleep(2)

arduino.send_position(3)
time.sleep(2)

arduino.close()
