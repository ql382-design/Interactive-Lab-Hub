import qwiic_button 
import time
import sys

print("🔍 Testing Qwiic Button using course code...")

my_button = qwiic_button.QwiicButton()

if not my_button.begin():
    print("❌ Button not detected!")
    sys.exit(1)

print("✅ Button initialized! Press to test...")

try:
    while True:
        if my_button.is_button_pressed():
            print("🎯 Button is PRESSED!")
        else:
            print("… waiting …")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n👋 Exit")
