# Direct test of QwiicButton without wrapper
import time
import qwiic_button

print("🔍 Initializing Qwiic Button...")
button = qwiic_button.QwiicButton(0x6F)  # or just qwiic_button.QwiicButton()

if button.begin():
    print("✅ Qwiic Button initialized!")
else:
    print("❌ Failed to initialize button")

print("🎯 Press button to test...")

try:
    while True:
        if button.is_button_pressed():
            print("🎉 Button Press Detected!")
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\n👋 Exit button test.")
