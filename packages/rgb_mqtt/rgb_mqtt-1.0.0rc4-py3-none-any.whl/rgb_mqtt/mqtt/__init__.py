import os
import json
import paho.mqtt.client as mqtt
import yaml
import pprint
import logging
from pathlib import Path

from rgb_mqtt.logger import log_client
from rgb_mqtt.leds import set_color, start_loop, stop_loop, set_cc_options, loop_active
from rgb_mqtt.utils import colr_str_to_tuple, colr_tuple_to_st



mqtt_client = None
device_config = None  # Declare a global variable for the device configuration

# MQTT settings
MQTT_BROKER = os.getenv("MQTT_BROKER")
if not MQTT_BROKER:
    raise ValueError("Missing MQTT_BROKER env var")
MQTT_PORT = os.getenv("MQTT_PORT")
if not MQTT_PORT:
    raise ValueError("Missing MQTT_PORT env var")
try:
    MQTT_PORT = int(MQTT_PORT)
except ValueError:
    raise ValueError("MQTT_PORT must be an integer")
MQTT_USER = os.getenv("MQTT_USER")
if not MQTT_USER:
    raise ValueError("Missing MQTT_USER env var")
MQTT_PASS = os.getenv("MQTT_PASS")
if not MQTT_PASS:
    raise ValueError("Missing MQTT_PASS env var")

MQTT_UID = os.getenv("MQTT_UID") or "dumb-rgb-mqtt"
MQTT_TOPIC_STATUS = os.getenv("MQTT_TOPIC_STATUS") or f"homeassistant/device/{MQTT_UID}/config"


def publish_all_led(all_led_state):
    try:
        led_status = all_led_state["state"]
        topic = device_config.get("cmps").get(f"all_leds").get("state_topic")
        rgb_topic = device_config.get("cmps").get(f"all_leds").get("rgb_stat_t")
        mqtt_client.publish(f"{topic}", led_status.encode('utf-8'), retain=True)
        if "color" in all_led_state:
            led_status = colr_tuple_to_st(all_led_state["color"])
            mqtt_client.publish(f"{rgb_topic}", led_status.encode('utf-8'), retain=True)
            log_client.debug(f"[MQTT][%15s] Status: {all_led_state}", "publish_all_led")
        else:
            log_client.debug(f"[MQTT][%15s] Status: {all_led_state['state']}", "publish_all_led")
    except Exception as e:
        log_client.error(f"[MQTT][%15s] Error publishing LED status: {e}", "publish_all_led")


def on_connect(client, userdata, flags, rc):
    log_client.info(f"[MQTT][%15s] Connected to broker", "on_connect")
    # Loop through LEDs and subscribe to their command topics
    for _, led_config in device_config['cmps'].items():
        for topic_type in ["command_topic", "rgb_cmd_t"]:
            topic = led_config.get(topic_type, False)
            if topic:
                client.subscribe(topic)
                log_client.info(f"[MQTT][%15s] Subscribed to {topic}", "on_connect")
            # rgb_command_topic = led_config['rgb_cmd_t']
            # client.subscribe(rgb_command_topic)
            # log_client.info(f"[MQTT][%15s] Subscribed to {rgb_command_topic}", "on_connect")

    # Publish initial status
    client.publish(MQTT_TOPIC_STATUS, json.dumps(device_config), retain=True)


def on_message(client, userdata, msg):
    global loop_active
    try:
        payload = msg.payload.decode('utf-8')
        log_client.info(f"[MQTT][%15s] topic  : \"{msg.topic}\"", "on_message")
        log_client.info(f"[MQTT][%15s] payload: \"{msg.payload}\"", "on_message")
        if msg.topic == f"cmnd/{MQTT_UID}/all_leds/cycle_color":
            if payload == "OFF":
                set_cc_options(False)
            else:
                set_cc_options({"loop_type": "cycle"}) 
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/cycle_color", payload, retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/fireplace", "OFF".encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/state", "OFF".encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/alternate", "OFF".encode('utf-8'), retain=True)
        if msg.topic == f"cmnd/{MQTT_UID}/all_leds/fireplace":
            if payload == "OFF":
                set_cc_options(False)
            else:
                set_cc_options({"loop_type": "fireplace"}) 
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/fireplace", payload, retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/cycle_color", "OFF".encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/state", "OFF".encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/alternate", "OFF".encode('utf-8'), retain=True)
        elif msg.topic == f"cmnd/{MQTT_UID}/all_leds/alternate":
            if payload == "OFF":
                set_cc_options(False)
            else:
                set_cc_options({"loop_type": "alternate"})
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/alternate", payload)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/fireplace", "OFF".encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/state", "OFF".encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/cycle_color", "OFF".encode('utf-8'), retain=True)
        elif msg.topic == f"cmnd/{MQTT_UID}/all_leds/color_one/rgb":
            color_one = colr_str_to_tuple(payload)
            set_cc_options({"color_one": color_one})
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/color_one/rgb", payload.encode('utf-8'), retain=True)
        elif msg.topic == f"cmnd/{MQTT_UID}/all_leds/color_one":
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/color_one", "ON".encode('utf-8'), retain=True)
        elif msg.topic == f"cmnd/{MQTT_UID}/all_leds/color_two/rgb":
            color_two = colr_str_to_tuple(payload)
            set_cc_options({"color_two": color_two})
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/color_two/rgb", payload.encode('utf-8'), retain=True)
        elif msg.topic == f"cmnd/{MQTT_UID}/all_leds/color_two":
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/color_two", "ON".encode('utf-8'), retain=True)
        elif msg.topic == f"cmnd/{MQTT_UID}/all_leds/rate":
            rate = payload
            set_cc_options({"rate": float(rate)})
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/rate", payload, retain=True)
        elif msg.topic == f"cmnd/{MQTT_UID}/all_leds/transition":
            transition = False if payload == "ON" else True
            set_cc_options({"transition": transition})
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/transition", payload)
        elif msg.topic == f"cmnd/{MQTT_UID}/all_leds/rgb":
                # publish_led(led_index)
            color = colr_str_to_tuple(payload)
            set_cc_options({"all_leds": color, "all_leds_state": True, "loop_type": "none"})
            set_color(color[0], color[1], color[2])
            publish_all_led({"state": "ON", "color": colr_str_to_tuple(payload) })
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/fireplace", "OFF".encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/alternate", "OFF".encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/cycle_color", "OFF".encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/state", "ON".encode('utf-8'), retain=True)
        elif msg.topic == f"cmnd/{MQTT_UID}/all_leds/state":
            if payload == "OFF":
                set_cc_options({"all_leds_state": False, "loop_type": "none"})
            else:
                set_cc_options({"all_leds_state": True, "loop_type": "none"}) 
            publish_all_led({"state": payload })
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/state", payload.encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/fireplace", "OFF".encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/alternate", "OFF".encode('utf-8'), retain=True)
            mqtt_client.publish(f"stat/{MQTT_UID}/all_leds/cycle_color", "OFF".encode('utf-8'), retain=True)
    except Exception as e:
        log_client.error(f"[MQTT][%15s] Error processing message: {e}", "on_message")
        log_client.debug(f"[MQTT][%15s] Message payload : {msg.payload}", "on_message")
        log_client.debug(f"[MQTT][%15s] Message topic : {msg.topic}", "on_message")

def gen_leds_conf():
    # led_config = {}
    # Iterate over each component configuration in the device configuration
    # and update string values by replacing 'MQTT_UID' with its actual value.
    for _, component_values in device_config["cmps"].items():
        for key, value in component_values.items():
            if isinstance(value, str):
                component_values[key] = value.replace("MQTT_UID", MQTT_UID)

    # device_config["cmps"].update(led_config)
    # log_client.info("[MQTT][%15s] `LED configuration generated` :", "gen_leds_conf")
    if log_client.getEffectiveLevel() == logging.INFO:
        pprint.pprint(device_config, indent=2)


def init_mqtt():
    global mqtt_client, device_config  # Declare global to modify the external variables

    # Load device configuration once during initialization
    path = Path(os.path.dirname(__file__)) / "../device_config.yaml"
    with open(path, 'r') as file:
        device_config = yaml.safe_load(file)
        # Replace placeholder MQTT_UID, and generate as many "Lights" as there are leds in HA
        gen_leds_conf()
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    # for i in range(NUM_LEDS):
    #     publish_led(i)
