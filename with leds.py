import serial
import time
import numpy as np
from sklearn.linear_model import LinearRegression

# ==========================================
# CONFIGURATION
# ==========================================
COM_PORT = 'COM8'   # <--- CHECK YOUR PORT (e.g., COM3, COM5, /dev/ttyUSB0)
BAUD_RATE = 115200  # Matches Arduino

# ==========================================
# TRAIN MODEL
# ==========================================
print("--- Training AI Model ---")
X_train = np.array([[10], [20], [30], [40], [45], [55], [60], [70], [80], [90]])
y_train = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
model = LinearRegression()
model.fit(X_train, y_train)
print("Model Ready.")

# ==========================================
# CONNECT
# ==========================================
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Allow connection to stabilize
    print(f"Connected to {COM_PORT}")
except Exception as e:
    print("Error: Check your COM Port setting in the code.")
    exit()

# ==========================================
# MAIN LOOP
# ==========================================
def run_system():
    # Helper to track state to avoid spamming the console
    last_action = "" 

    print("--- System Running ---")
    
    try:
        while True:
            if ser.in_waiting > 0:
                try:
                    # 1. READ DISTANCE FROM ARDUINO
                    line = ser.readline().decode('utf-8').strip()
                    
                    if not line: continue 
                    
                    real_distance = float(line)
                    
                    # 2. AI PREDICTION
                    prediction = model.predict([[real_distance]])
                    
                    # 3. DECISION & FEEDBACK LOOP
                    if prediction >= 0.5:
                        action = "OPEN"
                        # Send 'O' to Arduino (Turn Green LED ON)
                        ser.write(b'O')
                    else:
                        action = "CLOSE"
                        # Send 'C' to Arduino (Turn Red LED ON)
                        ser.write(b'C')

                    # 4. DISPLAY OUTPUT (Only update if distance changes slightly or logic runs)
                    # Using \r overwrites the line for a clean "dashboard" look
                    print(f"Distance: {real_distance:05.1f} cm | AI Confidence: {prediction[0]:.2f} | Door: {action}   ", end='\r')
                    
                except ValueError:
                    pass
    except KeyboardInterrupt:
        print("\nStopping system...")
        ser.close()

if __name__ == "__main__":
    run_system()