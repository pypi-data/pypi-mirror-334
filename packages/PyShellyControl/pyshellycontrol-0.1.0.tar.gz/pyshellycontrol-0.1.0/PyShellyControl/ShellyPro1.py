import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyPro1(ShellyDevice):
    def getStatus(self):
        """
        Retrieves the status of the relay (via HTTP or MQTT).

        Returns:
            dict or None: The status response if successful, None if failed.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/rpc/Shelly.GetStatus"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Getting relay status via HTTP")
            return self.sendHTTPRequest("rpc/Shelly.GetStatus")

    def on(self, timer: int = None):
        """
        Turns the relay on, optionally with a timer (via HTTP or MQTT).

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
            logging.info(f"Turning relay on via HTTP with timer: {timer}")
            self.sendHTTPRequest("relay/0", params)

    def off(self, timer: int = None):
        """
        Turns the relay off, optionally with a timer (via HTTP or MQTT).

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
            logging.info(f"Turning relay off via HTTP with timer: {timer}")
            self.sendHTTPRequest("relay/0", params)

    def toggle(self):
        """
        Toggles the relay (via HTTP or MQTT).

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
