import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyDimmer2(ShellyDevice):
    def getStatus(self):
        """
        Retrieves the status of the light (via HTTP or MQTT).

        Returns:
            dict or None: The status response if successful, None if failed.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0/status"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Getting light status via HTTP")
            return self.sendHTTPRequest("light/0?status")

    def on(self, timer: int = None, brightness: int = None):
        """
        Turns on the light and optionally sets the brightness and timer (via HTTP or MQTT).

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
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Turning light on via HTTP")
            self.sendHTTPRequest("light/0", params)

    def off(self, timer: int = None):
        """
        Turns off the light, optionally with a timer (via HTTP or MQTT).

        Args:
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        """
        params = {"turn": "off"}
        if timer:
            params["timer"] = timer

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Turning light off via HTTP")
            self.sendHTTPRequest("light/0", params)

    def toggle(self):
        """
        Toggles the light (via HTTP or MQTT).

        Returns:
            None
        """
        params = {"turn": "toggle"}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Toggling light via HTTP")
            self.sendHTTPRequest("light/0", params)

    def setBrightness(self, brightness: int):
        """
        Sets the brightness of the light to the specified value (via HTTP or MQTT).

        Args:
            brightness (int): The brightness level (0-100).

        Returns:
            None
        """
        params = {"brightness": brightness}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Setting brightness to {brightness}% via HTTP")
            self.sendHTTPRequest(f"light/0?brightness={brightness}", params)

    def increaseBrightness(self, step: int = 10):
        """
        Increases the brightness by the specified step (via HTTP or MQTT).

        Args:
            step (int, optional): The increment step for brightness (default is 10).

        Returns:
            None
        """
        params = {"dim": "up", "step": step}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Increasing brightness by {step}% via HTTP")
            self.sendHTTPRequest(f"light/0?dim=up&step={step}", params)

    def decreaseBrightness(self, step: int = 10):
        """
        Decreases the brightness by the specified step (via HTTP or MQTT).

        Args:
            step (int, optional): The decrement step for brightness (default is 10).

        Returns:
            None
        """
        params = {"dim": "down", "step": step}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Decreasing brightness by {step}% via HTTP")
            self.sendHTTPRequest(f"light/0?dim=down&step={step}", params)

    def stopDimming(self):
        """
        Stops dimming the light (via HTTP or MQTT).

        Returns:
            None
        """
        params = {"dim": "stop"}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/light/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info("Stopping dimming via HTTP")
            self.sendHTTPRequest("light/0?dim=stop", params)
