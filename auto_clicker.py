import pyautogui
import time

print("Auto-clicker started. Press Ctrl+C to stop.")
try:
    while True:
        x, y = pyautogui.position()  # Get the current mouse position
        print(f"Clicking at {x}, {y}")
        pyautogui.click()  # Perform the click
        time.sleep(4)  # Wait for 5 seconds
except KeyboardInterrupt:
    print("Auto-clicker stopped.")

