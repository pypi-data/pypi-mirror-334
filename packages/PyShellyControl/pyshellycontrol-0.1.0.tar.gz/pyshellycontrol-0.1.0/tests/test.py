import unittest
from PyShellyControl import ShellyDevice

class TestShellyDevice(unittest.TestCase):
    def test_device_on(self):
        device = ShellyDevice("192.168.0.166")
        response = device.turn_on()
        self.assertTrue(response)
        
if __name__ == "__main__":
    unittest.main()
