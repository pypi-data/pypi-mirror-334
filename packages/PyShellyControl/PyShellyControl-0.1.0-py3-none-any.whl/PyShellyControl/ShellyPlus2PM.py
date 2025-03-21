import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyPlus2PM(ShellyDevice):
    def getStatus(self, channel: int = 0):
        """
        Retrieves the status of the relay or roller control, depending on the mode and channel.

        Args:
            channel (int, optional): The channel to query (0 for channel 1, 1 for channel 2). Default is 0.

        Raises:
            ValueError: If an invalid channel is specified (allowed values are 0 or 1).
        
        Returns:
            dict or None: The status response if successful, None if failed.
        """
        if channel not in [0, 1]:
            raise ValueError("Invalid channel. Allowed values are 0 (Channel 1) or 1 (Channel 2).")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/{channel}/status"
            payload = json.dumps({"status": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Getting status for channel {channel} via HTTP")
            return self.sendHTTPRequest(f"rpc/Switch.GetStatus?id={channel}")

    def on(self, channel: int = 0, timer: int = None):
        """
        Turns on the relay for the specified channel, optionally with a timer (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to turn on (0 for channel 1, 1 for channel 2). Default is 0.
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        """
        if channel not in [0, 1]:
            raise ValueError("Invalid channel. Allowed values are 0 (Channel 1) or 1 (Channel 2).")
        
        params = {"turn": "on"}
        if timer:
            params["timer"] = timer

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Turning relay on for channel {channel} via HTTP")
            self.sendHTTPRequest(f"relay/{channel}", params)

    def off(self, channel: int = 0, timer: int = None):
        """
        Turns off the relay for the specified channel, optionally with a timer (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to turn off (0 for channel 1, 1 for channel 2). Default is 0.
            timer (int, optional): The timer value in seconds (default is None).

        Returns:
            None
        """
        if channel not in [0, 1]:
            raise ValueError("Invalid channel. Allowed values are 0 (Channel 1) or 1 (Channel 2).")
        
        params = {"turn": "off"}
        if timer:
            params["timer"] = timer

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Turning relay off for channel {channel} via HTTP")
            self.sendHTTPRequest(f"relay/{channel}", params)

    def toggle(self, channel: int = 0):
        """
        Toggles the relay for the specified channel (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to toggle (0 for channel 1, 1 for channel 2). Default is 0.

        Returns:
            None
        """
        if channel not in [0, 1]:
            raise ValueError("Invalid channel. Allowed values are 0 (Channel 1) or 1 (Channel 2).")
        
        params = {"turn": "toggle"}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/relay/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Toggling relay for channel {channel} via HTTP")
            self.sendHTTPRequest(f"relay/{channel}", params)

    def coverOpen(self, channel: int = 0, timer: int = None):
        """
        Opens the roller shutter for the specified channel, optionally with a timer (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to control (0 for channel 1, 1 for channel 2). Default is 0.
            timer (int, optional): The duration of the opening in seconds (default is None).

        Returns:
            None
        """
        params = {"go": "open"}
        if timer:
            params["duration"] = timer

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/roller/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Opening roller shutter on channel {channel} via HTTP")
            self.sendHTTPRequest(f"roller/{channel}?go=open", params)

    def coverClose(self, channel: int = 0, timer: int = None):
        """
        Closes the roller shutter for the specified channel, optionally with a timer (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to control (0 for channel 1, 1 for channel 2). Default is 0.
            timer (int, optional): The duration of the closing in seconds (default is None).

        Returns:
            None
        """
        params = {"go": "close"}
        if timer:
            params["duration"] = timer

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/roller/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Closing roller shutter on channel {channel} via HTTP")
            self.sendHTTPRequest(f"roller/{channel}?go=close", params)

    def coverStop(self, channel: int = 0):
        """
        Stops the roller shutter for the specified channel (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to control (0 for channel 1, 1 for channel 2). Default is 0.

        Returns:
            None
        """
        params = {"go": "stop"}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/roller/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Stopping roller shutter on channel {channel} via HTTP")
            self.sendHTTPRequest(f"roller/{channel}?go=stop", params)

    def coverToPos(self, channel: int = 0, position: int = 0):
        """
        Sets the roller shutter position for the specified channel (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to control (0 for channel 1, 1 for channel 2). Default is 0.
            position (int, optional): The target position of the roller shutter (0 to 100). Default is 0.

        Returns:
            None
        """
        params = {"go": "to_pos", "roller_pos": position}

        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/roller/{channel}"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Setting roller shutter on channel {channel} to {position}% position via HTTP")
            self.sendHTTPRequest(f"roller/{channel}?go=to_pos&roller_pos={position}", params)

    def coverCalibrate(self, channel: int = 0):
        """
        Calibrates the roller shutter for the specified channel (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to calibrate (0 for channel 1, 1 for channel 2). Default is 0.

        Returns:
            None
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/roller/{channel}"
            payload = json.dumps({"go": "calibrate"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Calibrating roller shutter on channel {channel} via HTTP")
            self.sendHTTPRequest(f"rpc/Cover.Calibrate?id={channel}")

    def getCoverConfig(self, channel: int = 0):
        """
        Retrieves the configuration of the roller shutter for the specified channel (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to query (0 for channel 1, 1 for channel 2). Default is 0.

        Returns:
            dict or None: The configuration response if successful, None if failed.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/roller/{channel}/config"
            payload = json.dumps({"config": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Getting roller shutter configuration for channel {channel} via HTTP")
            return self.sendHTTPRequest(f"rpc/Cover.GetConfig?id={channel}")

    def getCoverState(self, channel: int = 0):
        """
        Retrieves the state of the roller shutter for the specified channel (via HTTP or MQTT).

        Args:
            channel (int, optional): The channel to query (0 for channel 1, 1 for channel 2). Default is 0.

        Returns:
            dict or None: The state response if successful, None if failed.
        """
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/roller/{channel}/status"
            payload = json.dumps({"state": "get"})
            self.sendMQTTCommand(topic, payload)
        else:
            logging.info(f"Getting roller shutter state for channel {channel} via HTTP")
            return self.sendHTTPRequest(f"rpc/Cover.GetStatus?id={channel}")
