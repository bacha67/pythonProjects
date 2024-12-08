import pyautogui
import time

try:
    print("Auto-clicker started. Press Ctrl+C to stop.")
    while True:
        pyautogui.click()  # Simulates a left mouse click
        time.sleep(5)  # Waits for 5 seconds
except KeyboardInterrupt:
    print("Auto-clicker stopped.")
