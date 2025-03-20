import RPi.GPIO as GPIO
import os
import threading
import time
import random

from rgb_mqtt.logger import log_client
# GPIO setup
PINS = {'R': os.getenv("DUMB_LED_RED_PIN", 17), 'G': os.getenv("DUMB_LED_GREEN_PIN", 22), 'B': os.getenv("DUMB_LED_BLUE_PIN", 24)}
GPIO.setmode(GPIO.BCM)
for pin in PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# PWM setup
FREQ = 1000  # 1kHz frequency to reduce flickering
pwm = {color: GPIO.PWM(pin, FREQ) for color, pin in PINS.items()}
for p in pwm.values():
    p.start(0)

# Track current color
current_color = {'R': 0, 'G': 0, 'B': 0}
loop_thread = None
loop_active = False

colors_options = {
    "all_leds": (255,255,255),
    "all_leds_state": False,
    "color_one": (255, 255, 0),
    "color_two": (0, 255, 255),
    "rate": 2,
    "loop_type": "fireplace"
}

def set_color(r, g, b):
    """Set the RGB color with values between 0-255."""
    current_color['R'] = r
    current_color['G'] = g
    current_color['B'] = b
    pwm['R'].ChangeDutyCycle(r * 100 / 255)
    pwm['G'].ChangeDutyCycle(g * 100 / 255)
    pwm['B'].ChangeDutyCycle(b * 100 / 255)

def manage_loop():
    """Handles the lighting loop based on the selected mode."""
    global loop_active
    try:
        while loop_active:
            if colors_options["loop_type"] == "alternate":
                for state in range(2):
                    set_color(*colors_options["color_one"] if state == 0 else colors_options["color_two"])
                    if not loop_active:
                       break
                    time.sleep(colors_options["rate"])
            elif colors_options["loop_type"] == "cycle":
                for _ in range(2):
                    set_color(*colors_options["color_one"])
                    if not loop_active:
                       break
                    time.sleep(colors_options["rate"] / 2)
                    set_color(*colors_options["color_two"])
                    if not loop_active:
                       break
                    time.sleep(colors_options["rate"] / 2)
            elif colors_options["loop_type"] == "fireplace":
                start_color = [random.randint(150, 255), random.randint(50, 100), random.randint(0, 50)]
                end_color = [random.randint(150, 255), random.randint(50, 100), random.randint(0, 50)]
                steps = int(colors_options["rate"] * 30)  # Smooth transition with ~30 steps per second
                for step in range(steps):
                    intermediate_color = [
                        int(start_color[i] + (end_color[i] - start_color[i]) * (step / steps))
                        for i in range(3)
                    ]
                    set_color(*intermediate_color)
                    if not loop_active:
                       break
                    time.sleep(1 / 30)  # 30 FPS smooth transition
                start_color = end_color  # Set new start for next transition
            elif colors_options["loop_type"] == "none":
                if colors_options["all_leds_state"]:
                    set_color(colors_options["all_leds"][0],colors_options["all_leds"][1],colors_options["all_leds"][2])
                else:
                    set_color(0,0,0)
                break
            else:
                break
    except Exception as e:
        log_client.error(f"[LEDS][%15s] Error in alternating colors: {e}", "manage_loop")

def start_loop():
    """Start a new loop thread."""
    global loop_thread, loop_active
    if loop_thread is not None and loop_thread.is_alive():
        stop_loop()
        loop_thread.join()
    loop_active = True
    loop_thread = threading.Thread(target=manage_loop)
    loop_thread.start()

def stop_loop():
    """Stop the running loop."""
    global loop_active
    loop_active = False
    if loop_thread is not None:
        loop_thread.join()

def set_cc_options(opt_object):
    """Update the loop configuration and restart the loop."""
    global colors_options
    stop_loop()
    colors_options.update(opt_object)
    start_loop()
