# This code was originally provided by JC Williams but was modified with Copilot to run the servo motor via activation of the high/low trigger relay.

# This is an example code for using a Capacitive Soil Moisture probe with the ECE 1000 Raspberry Pi Pico Kit
# For any questions regarding this script, please email: jawilliams46@tntech.edu

# For this script, we utilize the Raspberry Pi Pico Kit that you are given along with the capacitive soil moisture probe which should be connected as follows:
# V_cc to the 3.3 Volt or 5 Volt pin on the Pico Breadboard
# GND to the GND pin on the Pico Breadboard
# AOUT to the GPIO 26 pin on the Pico Breadboard (This is one of the ADC pins)
# How does this code work? Well, first we declare our libraries, then we delare what is hooked up to the Raspberry Pi Pico and to which pins they are connected, and finally we then ask the Pi Pico to show us the values of the probe as a percentage (FOREVER) .... (while True:)
from machine import ADC, Pin
import utime

# Soil moisture sensor setup
soil_probe = ADC(Pin(26))
max_moisture = 27574
min_moisture = 57100

# Relay setup
relay = Pin(13, Pin.OUT)

# Before we can show the moisture as a percentage, need to first get the minimum moisture value (when the probe is not in water) and the maximum moisture value (when the probe is in water)
def get_moisture_percentage(moisture_level):
    point_1_x = min_moisture
    point_2_x = max_moisture
    point_1_y = 0
    point_2_y = 100
    m = ((point_2_y - point_1_y) / (point_2_x - point_1_x))
    return int((m * moisture_level) - (m * min_moisture) + point_1_y)

while True:
    moisture_level = soil_probe.read_u16()
    moisture_level_percentage = get_moisture_percentage(moisture_level)
    print(moisture_level_percentage)
    
    if moisture_level_percentage < 55:
        relay.value(1)  # Turn on the relay (high trigger)
        utime.sleep(2)  # Keep it on for 2 seconds
        relay.value(0)  # Turn off the relay (low trigger)
    
    utime.sleep(10)
