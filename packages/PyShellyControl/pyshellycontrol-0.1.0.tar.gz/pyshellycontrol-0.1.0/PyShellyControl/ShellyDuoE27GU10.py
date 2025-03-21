import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyDuoE27GU10(ShellyDevice):
    def getStatus(self):
        """Fetches the status of the Shelly Duo E27/GU10 (via HTTP or MQTT)."""
        logging.info(f"Fetching status of the Shelly Duo E27/GU10")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/rpc/Shelly.GetStatus"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("rpc/Shelly.GetStatus")

    def on(self, mode="color", timer: int = None, red: int = None, green: int = None, blue: int = None, gain: int = None):
        """
        Turns the light on in the specified mode (Color or White) and sets the colors or brightness.
        
        Args:
            mode (str): The mode ("color" or "white").
            timer (int, optional): The timer value in seconds.
            red (int, optional): The red color value (0-255), only in "color" mode.
            green (int, optional): The green color value (0-255), only in "color" mode.
            blue (int, optional): The blue color value (0-255), only in "color" mode.
            gain (int, optional): The brightness in "white" mode.
        """
        params = {"turn": "on"}
        
        if mode == "color":
            if red is not None and green is not None and blue is not None:
                params["red"] = red
                params["green"] = green
                params["blue"] = blue
            if gain is not None:
                params["gain"] = gain
        
        elif mode == "white" and gain is not None:
            params["gain"] = gain
        
        if timer:
            params["timer"] = timer
        
        logging.info(f"Light in {mode} mode on, Timer: {timer}, RGB: ({red}, {green}, {blue}), Gain: {gain}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/{mode}/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest(f"{mode}/0", params)

    def off(self, mode="color", timer: int = None):
        """
        Turns the light off in the specified mode (Color or White), optionally with a timer.
        
        Args:
            mode (str): The mode ("color" or "white").
            timer (int, optional): The timer value in seconds.
        """
        params = {"turn": "off"}
        if timer:
            params["timer"] = timer
        
        logging.info(f"Light in {mode} mode off, Timer: {timer}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/{mode}/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest(f"{mode}/0", params)

    def toggle(self, mode="color"):
        """
        Toggles the light in the specified mode (Color or White).
        
        Args:
            mode (str): The mode ("color" or "white").
        """
        params = {"turn": "toggle"}
        
        logging.info(f"Toggling light in {mode} mode")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/{mode}/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest(f"{mode}/0", params)

    def setBrightness(self, brightness: int):
        """
        Sets the brightness of the light in White Mode (0 to 100%).
        
        Args:
            brightness (int): The brightness percentage (0-100).
        """
        if brightness < 0 or brightness > 100:
            logging.error("Brightness must be between 0 and 100.")
            return
        
        params = {"brightness": brightness}
        
        logging.info(f"Setting brightness to {brightness}% in White Mode")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("light/0", params)

    def setRGB(self, red: int, green: int, blue: int):
        """
        Sets the RGB values of the light in Color Mode.
        
        Args:
            red (int): The red color value (0-255).
            green (int): The green color value (0-255).
            blue (int): The blue color value (0-255).
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            logging.error("RGB values must be between 0 and 255.")
            return
        
        params = {"turn": "on", "red": red, "green": green, "blue": blue}
        
        logging.info(f"Setting RGB to ({red}, {green}, {blue})")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/color/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("color/0", params)
