import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyPro2PM(ShellyDevice):
    def getStatus(self, channel: int = 0):
        """
        Retrieves the status of the Shelly Pro 2PM for the specified channel (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to check the status for (0 for channel 1, 1 for channel 2). Default is 0.

        Returns:
            dict or None: The status response if successful, None if failed.
        
        Raises:
            ValueError: If an invalid channel is provided (must be 0 or 1).
        """
        if channel not in [0, 1]:
            raise ValueError("Invalid channel. Allowed values are 0 (channel 1) or 1 (channel 2).")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/rpc/Shelly.GetStatus"
            payload = json.dumps({"status": "get", "id": channel})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Getting Shelly Pro 2PM status, channel {channel} via HTTP")
            return self.sendHTTPRequest(f"rpc/Shelly.GetStatus?id={channel}")

    def on(self, channel: int = 0, timer: int = None):
        """
        Turns the relay of the Shelly Pro 2PM for the specified channel on, optionally with a timer (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to turn on (0 for channel 1, 1 for channel 2). Default is 0.
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        
        Raises:
            ValueError: If an invalid channel is provided (must be 0 or 1).
        """
        if channel not in [0, 1]:
            raise ValueError("Invalid channel. Allowed values are 0 (channel 1) or 1 (channel 2).")
        
        params = {"turn": "on"}
        if timer:
            params["timer"] = timer

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Turning Shelly Pro 2PM relay, channel {channel}, on via HTTP with timer: {timer}")
            self.sendHTTPRequest(f"relay/{channel}", params)

    def off(self, channel: int = 0, timer: int = None):
        """
        Turns the relay of the Shelly Pro 2PM for the specified channel off, optionally with a timer (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to turn off (0 for channel 1, 1 for channel 2). Default is 0.
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        
        Raises:
            ValueError: If an invalid channel is provided (must be 0 or 1).
        """
        if channel not in [0, 1]:
            raise ValueError("Invalid channel. Allowed values are 0 (channel 1) or 1 (channel 2).")
        
        params = {"turn": "off"}
        if timer:
            params["timer"] = timer

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Turning Shelly Pro 2PM relay, channel {channel}, off via HTTP with timer: {timer}")
            self.sendHTTPRequest(f"relay/{channel}", params)

    def toggle(self, channel: int = 0):
        """
        Toggles the relay of the Shelly Pro 2PM for the specified channel (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to toggle (0 for channel 1, 1 for channel 2). Default is 0.

        Returns:
            None
        
        Raises:
            ValueError: If an invalid channel is provided (must be 0 or 1).
        """
        if channel not in [0, 1]:
            raise ValueError("Invalid channel. Allowed values are 0 (channel 1) or 1 (channel 2).")
        
        params = {"turn": "toggle"}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Toggling Shelly Pro 2PM relay, channel {channel}, via HTTP")
            self.sendHTTPRequest(f"relay/{channel}", params)
