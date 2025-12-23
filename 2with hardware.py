import serial
import time
import numpy as np
from sklearn.linear_model import LinearRegression

# ==========================================
# CONFIGURATION
# ==========================================
COM_PORT = 'COM8'  # <--- CHANGE THIS to your Arduino Port
BAUD_RATE = 115200 # Must match Arduino code

# ==========================================
# PART 1: TRAIN THE MODEL (Same as before)
# ==========================================
print("--- Training the AI Model ---")

# Data: Distance (cm) -> Action (1=Open, 0=Close)
# Distances 0-50cm: Open (1)
# Distances 51-100cm: Close (0)
X_train = np.array([[10], [20], [30], [40], [45], [55], [60], [70], [80], [90]])
y_train = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])

model = LinearRegression()
model.fit(X_train, y_train)
print("Model Trained. Ready for Sensor Data.")

# ==========================================
# PART 2: CONNECT TO ARDUINO
# ==========================================
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Wait 2 seconds for Arduino connection to stabilize
    print(f"Connected to Arduino on {COM_PORT}")
except Exception as e:
    print(f"Error: Could not connect to {COM_PORT}. Check your cable and port name.")
    exit()

# ==========================================
# PART 3: REAL-TIME AI LOOP
# ==========================================

def process_sensor_data():
    current_door_state = "CLOSED"
    
    # Flush input buffer to ensure we aren't reading old data
    ser.reset_input_buffer()

    print("--- System Running: Waiting for Movement ---")

    try:
        while True:
            # We check if there is data waiting in the USB pipe
            if ser.in_waiting > 0:
                
                # Read the line from Arduino, decode bytes to string, strip whitespace
                try:
                    line = ser.readline().decode('utf-8').strip()
                    
                    # Convert string input to float
                    real_distance = float(line)
                    
                    # --- AI PREDICTION ---
                    prediction = model.predict([[real_distance]])
                    
                    if prediction >= 0.5:
                        desired_action = "OPEN"
                    else:
                        desired_action = "CLOSE"
                    
                    # Only print if state changes or for debugging every few cycles
                    # Using carriage return \r to update the line in place for "sinkage" feel
                    print(f"Dist: {real_distance}cm | AI Score: {prediction[0]:.2f} | Door: {desired_action}   ", end='\r')
                    
                    # LOGIC TO ACTUALLY TRIGGER DOOR
                    if desired_action != current_door_state:
                        # In a real system, you would send a signal back to Arduino here
                        # ser.write(b'1') if OPEN, ser.write(b'0') if CLOSE
                        current_door_state = desired_action
                        
                except ValueError:
                    # Sometimes serial data gets corrupted (e.g., partial bytes), ignore it
                    pass
                    
    except KeyboardInterrupt:
        print("\nConnection Closed.")
        ser.close()

if __name__ == "__main__":
    process_sensor_data()