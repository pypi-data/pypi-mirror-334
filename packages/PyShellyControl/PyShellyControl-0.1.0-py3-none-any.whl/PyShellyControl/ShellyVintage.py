import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyVintage(ShellyDevice):
    def getStatus(self):
        """Fetches the status of the Shelly Vintage (via HTTP or MQTT)."""
        logging.info(f"Fetching status of the Shelly Vintage")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/rpc/Shelly.GetStatus"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("rpc/Shelly.GetStatus")

    def on(self, brightness: int = None, timer: int = None):
        """
        Turns on the light and optionally sets the brightness and a timer.
        
        Args:
            brightness (int, optional): The brightness of the light (0-100%).
            timer (int, optional): The timer value in seconds.
        """
        params = {"turn": "on"}
        
        if brightness is not None:
            if brightness < 0 or brightness > 100:
                logging.error("Brightness must be between 0 and 100.")
                return
            params["brightness"] = brightness
        
        if timer:
            params["timer"] = timer
        
        logging.info(f"Turning on light, Timer: {timer}, Brightness: {brightness}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("light/0", params)

    def off(self, timer: int = None):
        """
        Turns off the light, optionally with a timer.
        
        Args:
            timer (int, optional): The timer value in seconds.
        """
        params = {"turn": "off"}
        
        if timer:
            params["timer"] = timer
        
        logging.info(f"Turning off light, Timer: {timer}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("light/0", params)

    def toggle(self):
        """Toggles the light (on → off, off → on)."""
        params = {"turn": "toggle"}
        
        logging.info(f"Toggling light")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("light/0", params)

    def setBrightness(self, brightness: int):
        """
        Sets the brightness of the light (in %).
        
        Args:
            brightness (int): The brightness of the light (0-100%).
        """
        if brightness < 0 or brightness > 100:
            logging.error("Brightness must be between 0 and 100.")
            return
        
        params = {"brightness": brightness}
        
        logging.info(f"Setting brightness to {brightness}%")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("light/0", params)
