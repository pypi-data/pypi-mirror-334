import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyPlus1(ShellyDevice):
    def getStatus(self):
        """
        Retrieves the status of the Shelly device (via HTTP or MQTT).

        Returns:
            dict or None: The status response if successful, None if failed.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/0/status"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Getting status via HTTP")
            self.sendHTTPRequest("rpc/Shelly.GetStatus")

    def on(self, timer: int = None):
        """
        Turns on the relay, optionally with a timer (via HTTP or MQTT).

        Args:
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        """
        params = {"turn": "on"}
        if timer:
            params["timer"] = timer
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Turning relay on via HTTP")
            self.sendHTTPRequest("relay/0", params)

    def off(self, timer: int = None):
        """
        Turns off the relay, optionally with a timer (via HTTP or MQTT).

        Args:
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        """
        params = {"turn": "off"}
        if timer:
            params["timer"] = timer
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Turning relay off via HTTP")
            self.sendHTTPRequest("relay/0", params)

    def toggle(self):
        """
        Toggles the relay state (via HTTP or MQTT).

        Returns:
            None
        """
        params = {"turn": "toggle"}
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Toggling relay via HTTP")
            self.sendHTTPRequest("relay/0", params)
