import numpy as np
from sklearn.linear_model import LinearRegression
import time
import random

# ==========================================
# PART 1: PREPARING THE TRAINING DATA
# ==========================================

print("--- Training the AI Model ---")

# We create dummy data to teach the model.
# Let's say:
# Distances 0cm to 50cm = Person is close -> DOOR OPEN (1)
# Distances 51cm to 100cm = Person is far -> DOOR CLOSE (0)

# Training Inputs (Distances in cm) represented as a column vector
X_train = np.array([
    [10], [20], [30], [40], [45],   # Close range
    [55], [60], [70], [80], [90]    # Far range
])

# Training Outputs (1 = Open, 0 = Close)
y_train = np.array([
    1, 1, 1, 1, 1,    # Labels for close range
    0, 0, 0, 0, 0     # Labels for far range
])

# ==========================================
# PART 2: BUILDING THE LINEAR MODEL
# ==========================================

# Initialize Linear Regression model
model = LinearRegression()

# Train the model (Fit the line to the data)
model.fit(X_train, y_train)

print("Model Trained Successfully!")
print(f"Intercept: {model.intercept_}")
print(f"Coefficient: {model.coef_}")
print("-----------------------------\n")

# ==========================================
# PART 3: THE AUTOMATION LOOP
# ==========================================

def get_sensor_distance():
    """
    In a real scenario, this would read from a sensor (like HC-SR04).
    Here, we simulate a person walking towards and away from the door.
    """
    # Simulating random movement between 10cm and 100cm
    return random.randint(10, 100)

def control_door():
    current_door_state = "CLOSED"
    
    print("--- System Active: Monitoring Distance ---")
    
    try:
        while True:
            # 1. Get Live Data
            real_distance = get_sensor_distance()
            
            # 2. Predict using the AI Model
            # We reshape input because model expects a 2D array
            prediction = model.predict([[real_distance]])
            
            # Linear regression returns continuous numbers (e.g., 0.8, 0.2, -0.1).
            # We apply a threshold of 0.5. 
            # If > 0.5, the model leans towards "Open". If < 0.5, it leans towards "Close".
            
            if prediction >= 0.5:
                action = "OPEN"
            else:
                action = "CLOSE"
            
            # 3. Actuate (Open or Close the door)
            if action != current_door_state:
                print(f"Distance: {real_distance}cm | Prediction Score: {prediction[0]:.2f} | Action: {action}ING DOOR...")
                current_door_state = action
                # 
            else:
                print(f"Distance: {real_distance}cm | Door remains {current_door_state}")

            # Slow down the loop for readability
            time.sleep(1.5)

    except KeyboardInterrupt:
        print("\nSystem deactivated.")

# Run the system
if __name__ == "__main__":
    control_door()