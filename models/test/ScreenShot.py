import pyautogui
import time
def take_screenshot(file_path):
    try:
        # Capture the screenshot
        screenshot = pyautogui.screenshot()
        
        # Save the screenshot to the specified file path
        screenshot.save(file_path)
        print("Screenshot saved successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
time.sleep(5)
take_screenshot("screenshot.png")
