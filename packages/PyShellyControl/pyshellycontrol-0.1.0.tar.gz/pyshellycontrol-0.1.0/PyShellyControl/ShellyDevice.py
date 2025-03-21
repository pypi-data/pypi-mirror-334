import requests
import paho.mqtt.client as mqtt
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyDevice:
    def __init__(self, deviceID, ip=None, mqttBroker=None, mqttPort=1883, username=None, password=None):
        """
        Initializes a ShellyDevice object with the given parameters.

        Args:
            deviceID (str): The unique identifier for the Shelly device.
            ip (str, optional): The IP address of the Shelly device (default is None).
            mqttBroker (str, optional): The address of the MQTT broker (default is None).
            mqttPort (int, optional): The port of the MQTT broker (default is 1883).
            username (str, optional): The username for HTTP authentication (default is None).
            password (str, optional): The password for HTTP authentication (default is None).

        Attributes:
            deviceID (str): The device ID of the Shelly device.
            ip (str, optional): The IP address of the Shelly device.
            mqttBroker (str, optional): The address of the MQTT broker.
            mqttPort (int): The port number of the MQTT broker.
            useMQTT (bool): A flag to indicate if MQTT is used (True if mqttBroker is provided).
            client (mqtt.Client, optional): The MQTT client instance.
            username (str, optional): The username for HTTP authentication.
            password (str, optional): The password for HTTP authentication.
        """
        self.deviceID = deviceID
        self.ip = ip
        self.mqttBroker = mqttBroker
        self.mqttPort = mqttPort
        self.useMQTT = mqttBroker is not None
        self.client = None
        self.username = username
        self.password = password

    def sendHTTPRequest(self, endpoint, params=None):
        """
        Sends an HTTP request to the Shelly device with optional authentication.

        Args:
            endpoint (str): The endpoint to send the request to (e.g., "status").
            params (dict, optional): Parameters to include in the request (default is None).

        Returns:
            dict or None: The response in JSON format if the request is successful, None if failed.
        
        Raises:
            ValueError: If IP address is not set when trying to send an HTTP request.
        """
        if not self.ip:
            raise ValueError("IP address is required for HTTP control")
        
        # Build URL with optional authentication
        if self.username and self.password:
            url = f"http://{self.username}:{self.password}@{self.ip}/{endpoint}"
        else:
            url = f"http://{self.ip}/{endpoint}"
        
        try:
            # Send the HTTP request with parameters if provided
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"HTTP request failed: {e}")
            return None

    def sendMQTTCommand(self, topic, payload):
        """
        Sends an MQTT message to the specified topic with optional authentication.

        Args:
            topic (str): The MQTT topic to publish the message to.
            payload (str): The message payload to send.

        Returns:
            None

        Raises:
            ValueError: If MQTT broker is not set when trying to send an MQTT message.
        """
        if not self.mqttBroker:
            raise ValueError("MQTT broker is required for MQTT control")
        
        # Initialize MQTT client if not done already
        if self.client is None:
            self.client = mqtt.Client()

            # Set MQTT username and password if provided
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)

            # Connect to the MQTT broker
            try:
                self.client.connect(self.mqttBroker, self.mqttPort, 60)
            except Exception as e:
                logging.error(f"MQTT connection failed: {e}")
                return
        
        # Send the MQTT message
        try:
            self.client.publish(topic, payload)
            logging.info(f"MQTT sent to {topic}: {payload}")
        except Exception as e:
            logging.error(f"MQTT message sending failed: {e}")

    def getStatus(self):
        """
        Gets the status of the Shelly device, either via HTTP or MQTT.

        Returns:
            dict or None: The status response if successful, None if failed.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/status"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Getting status via HTTP")
            return self.sendHTTPRequest("status")
        
    def getSettings(self):
        """
        Gets the settings of the Shelly device, either via HTTP or MQTT.

        Returns:
            dict or None: The settings response if successful, None if failed.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/settings"
            payload = json.dumps({"settings": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Getting settings via HTTP")
            return self.sendHTTPRequest("settings")
    
    def getActions(self):
        """
        Gets the actions available for the Shelly device, either via HTTP or MQTT.

        Returns:
            dict or None: The actions response if successful, None if failed.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/actions"
            payload = json.dumps({"actions": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Getting actions via HTTP")
            return self.sendHTTPRequest("settings/actions")
        
    def OTAUpdate(self):
        """
        Performs an OTA (Over-the-Air) update for the Shelly device, either via HTTP or MQTT.

        Returns:
            dict or None: The response from the OTA update request.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/ota"
            payload = json.dumps({"ota": "update"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Performing OTA update via HTTP")
            return self.sendHTTPRequest("ota?update=1")
        
    def reboot(self):
        """
        Reboots the Shelly device, either via HTTP or MQTT.

        Returns:
            dict or None: The response from the reboot request.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/reboot"
            payload = json.dumps({"reboot": "true"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Rebooting via HTTP")
            return self.sendHTTPRequest("reboot")
        
    def factoryReset(self):
        """
        Resets the Shelly device to factory settings, either via HTTP or MQTT.

        Returns:
            dict or None: The response from the factory reset request.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/reset"
            payload = json.dumps({"reset": "true"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Factory reset via HTTP")
            return self.sendHTTPRequest("reset")
