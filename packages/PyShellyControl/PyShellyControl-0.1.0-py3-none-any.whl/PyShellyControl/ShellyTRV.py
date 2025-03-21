import json
import logging
from .ShellyDevice import ShellyDevice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShellyTRV(ShellyDevice):
    def setAutoTemperatureControl(self, enabled: bool, target_temp: int = None):
        """
        Enables or disables the automatic temperature control. Optionally, a target temperature can also be set.
        
        Args:
            enabled (bool): True to enable the automatic temperature control, False to disable it.
            target_temp (int, optional): The target temperature (4–31 degrees Celsius), if enabled.
        """
        params = {"target_t_enabled": 1 if enabled else 0}
        
        if target_temp is not None:
            if 4 <= target_temp <= 31:
                params["target_t"] = target_temp
            else:
                logging.error("Target temperature must be between 4 and 31 degrees Celsius.")
                return
        
        logging.info(f"Auto temperature control {'enabled' if enabled else 'disabled'} with target temperature: {target_temp}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/settings/thermostat/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("settings/thermostat/0", params)

    def setValvePosition(self, position: int):
        """
        Sets the valve position (0-100%).
        
        Args:
            position (int): The valve position in percentage (0-100%).
        """
        if 0 <= position <= 100:
            params = {"pos": position}
            logging.info(f"Valve position set to {position}%.")
            
            if self.useMQTT:
                topic = f"shellies/{self.deviceID}/thermostat/0"
                payload = json.dumps(params)
                self.sendMQTTCommand(topic, payload)
            else:
                return self.sendHTTPRequest("thermostat/0", params)
        else:
            logging.error("Valve position must be between 0 and 100 percent.")

    def setSchedule(self, enabled: bool):
        """
        Enables or disables the schedule.
        
        Args:
            enabled (bool): True to enable the schedule, False to disable it.
        """
        params = {"schedule": 1 if enabled else 0}
        
        logging.info(f"Schedule {'enabled' if enabled else 'disabled'}")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/settings/thermostat/0"
            payload = json.dumps(params)
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("settings/thermostat/0", params)

    def startBoost(self, minutes: int):
        """
        Starts the Boost function for a specified number of minutes.
        
        Args:
            minutes (int): The number of minutes for the Boost (e.g., 10 minutes).
        """
        if minutes > 0:
            params = {"boost_minutes": minutes}
            logging.info(f"Boost function started for {minutes} minutes.")
            
            if self.useMQTT:
                topic = f"shellies/{self.deviceID}/thermostat/0"
                payload = json.dumps(params)
                self.sendMQTTCommand(topic, payload)
            else:
                return self.sendHTTPRequest("thermostat/0", params)
        else:
            logging.error("Boost duration must be a positive number.")

    def calibrate(self):
        """
        Starts the calibration process of the Shelly TRV.
        """
        logging.info("Calibration of the Shelly TRV started.")
        
        if self.useMQTT:
            topic = f"shellies/{self.deviceID}/calibrate"
            payload = json.dumps({})
            self.sendMQTTCommand(topic, payload)
        else:
            return self.sendHTTPRequest("calibrate")
