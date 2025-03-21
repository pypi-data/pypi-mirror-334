# ShellyControl

ShellyControl is a Python library for controlling and managing Shelly smart devices via HTTP and MQTT protocols. It provides an easy-to-use interface to interact with Shelly devices, retrieve their status, configure settings, and perform actions such as OTA updates and reboots.

## Features
- Supports communication with Shelly devices via HTTP and MQTT
- Retrieve device status, settings, and actions
- Perform OTA updates and reboots
- Factory reset Shelly devices
- MQTT authentication support
- Easily extensible for different Shelly models

## Installation

To install ShellyControl, you need Python 3.7 or later. Install the required dependencies using pip:

```sh
pip install requests paho-mqtt
```

Alternatively, if you have a `requirements.txt` file, install the dependencies with:

```sh
pip install -r requirements.txt
```

## Usage

### Importing the Library

```python
from shellycontrol import ShellyDevice
```

### Creating a Shelly Device Instance

You can initialize a Shelly device using either HTTP or MQTT:

#### Using HTTP:
```python
device = ShellyDevice(deviceID="shelly1", ip="192.168.1.100")
```

#### Using MQTT:
```python
device = ShellyDevice(deviceID="shelly1", mqttBroker="mqtt.example.com", mqttPort=1883, username="user", password="pass")
```

### Retrieve Device Status
```python
status = device.getStatus()
print(status)
```

### Retrieve Device Settings
```python
settings = device.getSettings()
print(settings)
```

### Retrieve Device Actions
```python
actions = device.getActions()
print(actions)
```

### Perform OTA Update
```python
device.OTAUpdate()
```

### Reboot Device
```python
device.reboot()
```

### Factory Reset
```python
device.factoryReset()
```

## Available Classes and Methods

### `ShellyDevice` Class
#### Constructor
```python
ShellyDevice(deviceID, ip=None, mqttBroker=None, mqttPort=1883, username=None, password=None)
```
- `deviceID` (str): Unique identifier of the Shelly device.
- `ip` (str, optional): IP address of the device (if using HTTP).
- `mqttBroker` (str, optional): MQTT broker address (if using MQTT).
- `mqttPort` (int, optional): MQTT broker port (default is 1883).
- `username` (str, optional): Username for authentication.
- `password` (str, optional): Password for authentication.

#### Methods
```python
def sendHTTPRequest(endpoint, params=None)
```
- Sends an HTTP request to the Shelly device.
- `endpoint` (str): API endpoint (e.g., "status").
- `params` (dict, optional): Request parameters.
- Returns: JSON response if successful, else None.

```python
def sendMQTTCommand(topic, payload)
```
- Sends an MQTT message.
- `topic` (str): MQTT topic.
- `payload` (str): Message payload.

```python
def getStatus()
```
- Retrieves device status.
- Returns: JSON response with device status.

```python
def getSettings()
```
- Retrieves device settings.
- Returns: JSON response with device settings.

```python
def getActions()
```
- Retrieves available device actions.
- Returns: JSON response with device actions.

```python
def OTAUpdate()
```
- Performs an over-the-air (OTA) update.

```python
def reboot()
```
- Reboots the device.

```python
def factoryReset()
```
- Resets the device to factory settings.

## Supported Shelly Devices
ShellyControl is designed to work with multiple Shelly devices, including:
- Shelly 3EM
- Shelly Dimmer 2
- Shelly Duo E27/GU10
- Shelly Plug
- Shelly Plus 1/1PM/2PM
- Shelly Pro 1/1PM/2/2PM/3/4PM
- Shelly RGBW2
- Shelly TRV
- Shelly Uni
- Shelly Vintage

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## License
This project is licensed under the MIT License.