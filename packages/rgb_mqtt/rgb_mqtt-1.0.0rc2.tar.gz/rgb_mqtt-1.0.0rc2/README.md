# dumb_led_mqtt

## Overview
`dumb_led_mqtt` is a Python package designed to control Dumb RGB LED strips using MQTT, making it easier to integrate lighting controls with the Home Assistant platform.
Currently specific to the GPIO pins of the Raspberry Pi but I intend to abstract that part of the code to make it work on any platform.

## Current requirements
* A raspberry PI, since the package directly refer to the GPIO pins for data transmission, and ensure you have the necessary permissions to access them (Root access) [How to set up the lights with the Raspberry Pi](https://blog.morill.es/2024/12/05/christmas/raspi/)
* Homeassistant instance
* An MQTT broker to facilitate communication between the Home Assistant and the Dumb RGB LED strips

## Local Installation (Options 1)
Use [Poetry](https://python-poetry.org/) to install the package:
```bash
poetry install
```

## PyPI Installation (Option 2) - Recommended

The `dumb_led_mqtt` package is also published on PyPI, allowing you to easily install it using pip. This enables seamless integration into projects without using Poetry.

```bash
pip install dumb_led_mqtt
```

## Usage
Here's a quick example on how to use `dumb_led_mqtt` in your project:

### env file
Multiple ways of doing this:
1. You can pass the env vars directly to the executable
  * example: `MQTT_BROKER=192.168.0.100 MQTT_PORT=1883 ... dumb-led-mqtt`
2. create an env file where the script is run, and it will automatically be loaded
3. Pass the path to your env file as an Environment variable: `Dumb RGB_ENV_PATH` and it will read from there. (Recommended)

```dotenv
MQTT_BROKER = "192.168.0.123"
MQTT_PORT = 1883
MQTT_USER = "your_user"
MQTT_PASS = "your_password"
MQTT_UID = "dumb-rgb-1"
```

#### Explanation of Environment Variables:
- MQTT_BROKER: This is the IP address of your MQTT broker. The broker is responsible for
  managing the communication between the different parts of your system.
- MQTT_PORT: The port on which the MQTT broker is running. The default MQTT port is 1883,
  but this might need to be changed if your setup uses a different configuration.
- MQTT_USER: The username required to authenticate with the MQTT broker.
- MQTT_PASS: The password for the given MQTT user. It's used alongside the username
- MQTT_UID: A unique identifier for this particular Dumb RGB LED controller instance. This is
  used so the broker and corresponding systems know where messages should be routed.

## Script arguments
```
usage: dumb-led-mqtt [-h] [-v]

Control the LED strip with MQTT and API

options:
  -h, --help       show this help message and exit
  -v, --verbosity  increase output verbosity, each v adds a verbosity level, (ex: -vvv)
```


## Running the script
if installed locally:
```bash
poetry run dumb_led_mqtt
```
if installed as package
```
dumb_led_mqtt
```

## Troubleshooting
Make sure to have configured all env vars properly.

If you encounter issues, check the MQTT broker connection and ensure the LED strip is properly connected.

You can debug using the `-v` option to increase verbosity and get more detailed logs.

If the problem persists, you can also check homeassistant logs.

You can open an issue, I will be happy to look into it.

## Contributing
Contributions are welcome! Please submit a pull request or file an issue for any enhancements.

## License
`dumb_led_mqtt` is licensed under the Apache License 2.0.

## Support
For issues or questions, please open an issue in this repository.
