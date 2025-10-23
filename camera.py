import cv2
import time
import Hobot.GPIO as GPIO


led_pin = 13
button_pin = 31
cap = cv2.VideoCapture(0)

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.setup(button_pin, GPIO.IN)

    if not cap.isOpened():
        print("Error: Cannot open camera")
        exit()

    print("Ready")

    while True:
        if GPIO.input(button_pin) == GPIO.HIGH:
            print("Button pressed! Capturing...")

            #Turn LED on
            GPIO.output(led_pin, GPIO.HIGH)

            #Capture image
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image")
                GPIO.output(led_pin, GPIO.LOW)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Canny Edge Detection
            edges = cv2.Canny(gray, 100, 200)

            timestamp = int(time.time())
            orig_name = f"image_{timestamp}.jpg"
            edge_name = f"edges_{timestamp}.jpg"
            #save
            cv2.imwrite(orig_name, frame)
            cv2.imwrite(edge_name, edges)
            print(f"Saved: {orig_name}, {edge_name}")

            time.sleep(0.5)
            GPIO.output(led_pin, GPIO.LOW)

            while GPIO.input(button_pin) == GPIO.HIGH:
                time.sleep(0.1)

        time.sleep(0.1)

#clean
finally:
    print("Cleaning up...")
    cap.release()
    GPIO.cleanup()
    print("Done.")