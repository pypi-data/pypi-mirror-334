import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyUni(ShellyDevice):
    def getStatus(self):
        """
        Retrieves the status of the Shelly Uni (via HTTP or MQTT).
        
        Returns:
            dict or None: The status response if successful, None if failed.
        """
        logging.info(f"Getting status of Shelly Uni")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/rpc/Shelly.GetStatus"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("rpc/Shelly.GetStatus")

    def on(self, timer: int = None):
        """
        Turns on the relay of the Shelly Uni, optionally with a timer (in seconds) (via HTTP or MQTT).
        
        Args:
            timer (int, optional): The timer value in seconds (default is None).
        
        Returns:
            None
        """
        params = {"turn": "on"}
        if timer:
            params["timer"] = timer
        
        logging.info(f"Turning Shelly Uni relay on, timer: {timer}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("relay/0", params)

    def off(self, timer: int = None):
        """
        Turns off the relay of the Shelly Uni, optionally with a timer (in seconds) (via HTTP or MQTT).
        
        Args:
            timer (int, optional): The timer value in seconds (default is None).
        
        Returns:
            None
        """
        params = {"turn": "off"}
        if timer:
            params["timer"] = timer
        
        logging.info(f"Turning Shelly Uni relay off, timer: {timer}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("relay/0", params)

    def toggle(self):
        """
        Toggles the relay of the Shelly Uni (via HTTP or MQTT).
        
        Returns:
            None
        """
        params = {"turn": "toggle"}
        
        logging.info(f"Toggling Shelly Uni relay")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("relay/0", params)
