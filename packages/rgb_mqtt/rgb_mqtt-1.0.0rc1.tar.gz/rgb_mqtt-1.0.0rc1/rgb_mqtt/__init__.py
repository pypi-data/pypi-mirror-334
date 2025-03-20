import os

import time
from dotenv import load_dotenv

if os.name == 'nt':
    os.system('color')

load_dotenv(os.getenv("DUMB_RGB_ENV_PATH", ".env"))

from rgb_mqtt.args import init_args
init_args()

from rgb_mqtt.logger import init_logger
init_logger()

from rgb_mqtt.mqtt import init_mqtt
init_mqtt()

def main():
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()