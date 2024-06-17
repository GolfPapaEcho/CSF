import time
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
import sys
import psutil

# Setup GPIO
GPIO.setmode(GPIO.BCM)
HEATER_PIN = 17
GPIO.setup(HEATER_PIN, GPIO.OUT)

# Initialize the DS18B20 sensor
sensor = W1ThermSensor()

def read_temp():
    try:
        return sensor.get_temperature()
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

def is_solenoid_running():
    # Check if a process named "Solenoid.py" is running
    for proc in psutil.process_iter(['name', 'cmdline']):
        if 'Solenoid.py' in proc.info['cmdline']:
            return True
    return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: sudo python3 thermostat.py <setpoint_temperature>")
        sys.exit(1)

    try:
        setpoint_temp = float(sys.argv[1])
    except ValueError:
        print("Invalid setpoint temperature. Please provide a valid number.")
        sys.exit(1)

    try:
        while True:
            current_temp = read_temp()
            if current_temp is not None:
                print(f"Current temperature: {current_temp:.2f} °C")

                if current_temp <= setpoint_temp:
                    GPIO.output(HEATER_PIN, GPIO.HIGH)
                    print("Heater ON")
                else:
                    GPIO.output(HEATER_PIN, GPIO.LOW)
                    print("Heater OFF")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program interrupted. Checking for running Solenoid.py.")

    finally:
        if not is_solenoid_running():
            GPIO.cleanup()
            print("GPIO cleaned up.")
        else:
            print("Solenoid.py is running. Skipping GPIO cleanup.")
