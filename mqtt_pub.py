import cv2
import paho.mqtt.client as mqtt
import base64
import time

# MQTT Configuration
broker = 'localhost'
topic = 'camera/frame'

# Connect to MQTT broker
client = mqtt.Client()
client.connect(broker, 1883, 60)

# Open camera
cap = cv2.VideoCapture(0)

# Make sure the resolution is reasonable
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Starting camera stream to MQTT...")

try:
    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
            
        # Resize for performance (optional, adjust as needed)
        frame = cv2.resize(frame, (320, 240))
        
        # Convert to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        
        # Convert to base64 with proper data URI format
        jpg_as_text = "data:image/jpeg;base64," + base64.b64encode(buffer).decode()
        
        # Publish to MQTT
        client.publish(topic, jpg_as_text)
        
        # Limit rate to reduce network load
        time.sleep(0.5)
        
except KeyboardInterrupt:
    print("Stopping camera stream")
finally:
    # Release resources
    cap.release()
    client.disconnect()
    print("Camera stream stopped")