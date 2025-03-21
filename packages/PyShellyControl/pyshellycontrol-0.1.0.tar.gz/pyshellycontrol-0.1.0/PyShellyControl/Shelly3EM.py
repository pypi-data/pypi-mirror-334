import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Shelly3EM(ShellyDevice):
    def getStatus(self):
        """
        Retrieves the status of the Shelly 3EM (via HTTP or MQTT).
        
        Returns:
            dict or None: The status response if successful, None if failed.
        """
        logging.info(f"Getting status of Shelly 3EM")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/rpc/Shelly.GetStatus"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("rpc/Shelly.GetStatus")

    def on(self, timer: int = None):
        """
        Turns on the relay of the Shelly 3EM, optionally with a timer (via HTTP or MQTT).

        Args:
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        """
        params = {"turn": "on"}
        if timer:
            params["timer"] = timer
        
        logging.info(f"Turning Shelly 3EM relay on, timer: {timer}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("relay/0", params)

    def off(self, timer: int = None):
        """
        Turns off the relay of the Shelly 3EM, optionally with a timer (via HTTP or MQTT).

        Args:
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        """
        params = {"turn": "off"}
        if timer:
            params["timer"] = timer
        
        logging.info(f"Turning Shelly 3EM relay off, timer: {timer}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("relay/0", params)

    def toggle(self):
        """
        Toggles the relay of the Shelly 3EM (via HTTP or MQTT).

        Returns:
            None
        """
        params = {"turn": "toggle"}
        
        logging.info(f"Toggling Shelly 3EM relay")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("relay/0", params)

    def readMeasurementData(self, channel: int):
        """
        Reads measurement data from the specified channel (0, 1, or 2).

        Args:
            channel (int): The channel from which to read measurement data (0, 1, or 2).

        Returns:
            dict or None: The measurement data if successful, None if failed.

        Raises:
            ValueError: If an invalid channel is provided (must be 0, 1, or 2).
        """
        if channel not in [0, 1, 2]:
            raise ValueError("Invalid channel. Allowed values are 0, 1, or 2.")
        
        logging.info(f"Getting measurement data from Shelly 3EM, channel {channel}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/emeter/{channel}/3em_data"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest(f"emeter/{channel}/3em_data")

    def downloadCSV(self, channel: int):
        """
        Downloads the .csv file from the specified channel (0, 1, or 2).

        Args:
            channel (int): The channel from which to download the .csv file (0, 1, or 2).

        Returns:
            dict or None: The .csv data if successful, None if failed.

        Raises:
            ValueError: If an invalid channel is provided (must be 0, 1, or 2).
        """
        if channel not in [0, 1, 2]:
            raise ValueError("Invalid channel. Allowed values are 0, 1, or 2.")
        
        logging.info(f"Downloading .csv file from Shelly 3EM, channel {channel}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/emeter/{channel}/3em_data.csv"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest(f"emeter/{channel}/3em_data.csv")
