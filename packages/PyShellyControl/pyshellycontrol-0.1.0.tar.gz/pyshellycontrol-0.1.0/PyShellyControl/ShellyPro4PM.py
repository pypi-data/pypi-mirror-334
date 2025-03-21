import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyPro4PM(ShellyDevice):
    def getStatus(self, channel: int = 0):
        """
        Retrieves the status of the Shelly Pro 4PM for the specified channel (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to check the status for (0 for channel 1, 1 for channel 2, 2 for channel 3, 3 for channel 4). Default is 0.

        Returns:
            dict or None: The status response if successful, None if failed.
        
        Raises:
            ValueError: If an invalid channel is provided (must be 0, 1, 2, or 3).
        """
        if channel not in [0, 1, 2, 3]:
            raise ValueError("Invalid channel. Allowed values are 0 (channel 1), 1 (channel 2), 2 (channel 3), or 3 (channel 4).")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/rpc/Shelly.GetStatus"
            payload = json.dumps({"status": "get", "id": channel})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Getting Shelly Pro 4PM status, channel {channel} via HTTP")
            return self.sendHTTPRequest(f"rpc/Shelly.GetStatus?id={channel}")

    def on(self, channel: int = 0, timer: int = None):
        """
        Turns the relay of the Shelly Pro 4PM for the specified channel on, optionally with a timer (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to turn on (0 for channel 1, 1 for channel 2, 2 for channel 3, 3 for channel 4). Default is 0.
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        
        Raises:
            ValueError: If an invalid channel is provided (must be 0, 1, 2, or 3).
        """
        if channel not in [0, 1, 2, 3]:
            raise ValueError("Invalid channel. Allowed values are 0 (channel 1), 1 (channel 2), 2 (channel 3), or 3 (channel 4).")
        
        params = {"turn": "on"}
        if timer:
            params["timer"] = timer

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Turning Shelly Pro 4PM relay, channel {channel}, on via HTTP with timer: {timer}")
            self.sendHTTPRequest(f"relay/{channel}", params)

    def off(self, channel: int = 0, timer: int = None):
        """
        Turns the relay of the Shelly Pro 4PM for the specified channel off, optionally with a timer (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to turn off (0 for channel 1, 1 for channel 2, 2 for channel 3, 3 for channel 4). Default is 0.
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        
        Raises:
            ValueError: If an invalid channel is provided (must be 0, 1, 2, or 3).
        """
        if channel not in [0, 1, 2, 3]:
            raise ValueError("Invalid channel. Allowed values are 0 (channel 1), 1 (channel 2), 2 (channel 3), or 3 (channel 4).")
        
        params = {"turn": "off"}
        if timer:
            params["timer"] = timer

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Turning Shelly Pro 4PM relay, channel {channel}, off via HTTP with timer: {timer}")
            self.sendHTTPRequest(f"relay/{channel}", params)

    def toggle(self, channel: int = 0):
        """
        Toggles the relay of the Shelly Pro 4PM for the specified channel (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to toggle (0 for channel 1, 1 for channel 2, 2 for channel 3, 3 for channel 4). Default is 0.

        Returns:
            None
        
        Raises:
            ValueError: If an invalid channel is provided (must be 0, 1, 2, or 3).
        """
        if channel not in [0, 1, 2, 3]:
            raise ValueError("Invalid channel. Allowed values are 0 (channel 1), 1 (channel 2), 2 (channel 3), or 3 (channel 4).")
        
        params = {"turn": "toggle"}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Toggling Shelly Pro 4PM relay, channel {channel}, via HTTP")
            self.sendHTTPRequest(f"relay/{channel}", params)

    def setDisplayBrightness(self, brightness: int):
        """
        Sets the display brightness of the Shelly Pro 4PM (0 to 100).

        Args:
            brightness (int): The brightness level to set (between 0 and 100).

        Returns:
            None

        Raises:
            ValueError: If an invalid brightness value is provided (must be between 0 and 100).
        """
        if brightness < 0 or brightness > 100:
            raise ValueError("Invalid brightness. The value must be between 0 and 100.")
        
        params = {"idle_brightness": brightness}
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/rpc/Ui.SetConfig"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Setting Shelly Pro 4PM display brightness to {brightness}%")
            self.sendHTTPRequest("rpc/Ui.SetConfig", params)
