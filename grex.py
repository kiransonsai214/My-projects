import serial
import time

# === Configure your port and baud rate ===
# Replace 'COM3' with your Arduino port
# On Linux/Mac, it may look like '/dev/ttyACM0' or '/dev/ttyUSB0'

def intake():
    arduino = serial.Serial(port='COM8', baudrate=9600, timeout=1)

    time.sleep(2)  # wait for Arduino to initialize

    print("Reading values from Arduino...\n")

    try:
        time.sleep(10)
        line = arduino.readline().decode('utf-8').strip()

    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print("Error:", e)

       
    return line

intake()  