import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyRGBW2(ShellyDevice):
    # Color mode (RGBW)

    def getStatus(self):
        """
        Retrieves the status of the light in color mode (via HTTP or MQTT).

        Returns:
            dict or None: The status response if successful, None if failed.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/color/0/status"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Getting light status in color mode via HTTP")
            return self.sendHTTPRequest("color/0?status")

    def on(self, timer: int = None, red: int = None, green: int = None, blue: int = None, white: int = None, gain: int = None):
        """
        Turns on the light and optionally sets the colors, intensity, and timer (via HTTP or MQTT).

        Args:
            timer (int, optional): The timer value in seconds (default is None).
            red (int, optional): The red color intensity (0-255).
            green (int, optional): The green color intensity (0-255).
            blue (int, optional): The blue color intensity (0-255).
            white (int, optional): The white color intensity (0-255).
            gain (int, optional): The intensity gain (0-100). Default is None.

        Returns:
            None
        """
        params = {"turn": "on"}

        if timer:
            params["timer"] = timer
        if red is not None:
            params["red"] = red
        if green is not None:
            params["green"] = green
        if blue is not None:
            params["blue"] = blue
        if white is not None:
            params["white"] = white
        if gain is not None:
            params["gain"] = gain

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/color/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Turning on light in color mode via HTTP")
            self.sendHTTPRequest("color/0", params)

    def off(self, timer: int = None):
        """
        Turns off the light in color mode, optionally with a timer (via HTTP or MQTT).

        Args:
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        """
        params = {"turn": "off"}
        if timer:
            params["timer"] = timer

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/color/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Turning off light in color mode via HTTP")
            self.sendHTTPRequest("color/0", params)

    def toggle(self):
        """
        Toggles the light in color mode (via HTTP or MQTT).

        Returns:
            None
        """
        params = {"turn": "toggle"}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/color/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Toggling light in color mode via HTTP")
            self.sendHTTPRequest("color/0", params)

    def setRGB(self, red: int, green: int, blue: int, white: int = 0):
        """
        Sets the RGBW colors of the light (via HTTP or MQTT).

        Args:
            red (int): The red color intensity (0-255).
            green (int): The green color intensity (0-255).
            blue (int): The blue color intensity (0-255).
            white (int, optional): The white color intensity (0-255). Default is 0.

        Returns:
            None
        """
        params = {"turn": "on", "red": red, "green": green, "blue": blue, "white": white}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/color/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Setting RGBW colors (R:{red}, G:{green}, B:{blue}, W:{white}) via HTTP")
            self.sendHTTPRequest("color/0", params)

    def setWhiteOnly(self, white: int):
        """
        Sets the light to white (only with the white color, without RGB) (via HTTP or MQTT).

        Args:
            white (int): The white color intensity (0-255).

        Returns:
            None
        """
        params = {"turn": "on", "white": white}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/color/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Setting white color only (White: {white}) via HTTP")
            self.sendHTTPRequest("color/0", params)

    def setIntensity(self, gain: int):
        """
        Sets the intensity of the light (via HTTP or MQTT).

        Args:
            gain (int): The intensity gain (0-100).

        Returns:
            None
        """
        params = {"turn": "on", "gain": gain}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/color/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Setting intensity (Gain: {gain}) via HTTP")
            self.sendHTTPRequest("color/0", params)

    # White mode (White)

    def onWhite(self, timer: int = None, brightness: int = None):
        """
        Turns on the white light, optionally with brightness and timer (via HTTP or MQTT).

        Args:
            timer (int, optional): The timer value in seconds (default is None).
            brightness (int, optional): The brightness level (0-100). Default is None.

        Returns:
            None
        """
        params = {"turn": "on"}

        if timer:
            params["timer"] = timer
        if brightness is not None:
            params["brightness"] = brightness

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/white/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Turning on white light via HTTP")
            self.sendHTTPRequest("white/0", params)

    def offWhite(self, timer: int = None):
        """
        Turns off the white light, optionally with a timer (via HTTP or MQTT).

        Args:
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        """
        params = {"turn": "off"}
        if timer:
            params["timer"] = timer

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/white/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Turning off white light via HTTP")
            self.sendHTTPRequest("white/0", params)

    def toggleWhite(self):
        """
        Toggles the white light (via HTTP or MQTT).

        Returns:
            None
        """
        params = {"turn": "toggle"}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/white/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Toggling white light via HTTP")
            self.sendHTTPRequest("white/0", params)

    def setWhiteBrightness(self, brightness: int):
        """
        Sets the brightness of the white light (via HTTP or MQTT).

        Args:
            brightness (int): The brightness level (0-100).

        Returns:
            None
        """
        params = {"brightness": brightness}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/white/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Setting white light brightness (Brightness: {brightness}) via HTTP")
            self.sendHTTPRequest(f"white/0?brightness={brightness}", params)
