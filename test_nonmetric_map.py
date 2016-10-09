import unittest
from kalman_filter.sensor import SensorData
from kalman_filter.sensor.nonmetric_map import NonMetricMap

class testNMM(unittest.TestCase):
    def setUp(self):
        self.sig1 = SensorData('a', -20)
        self.sig2 = SensorData('a1', -40)
        self.sig3 = SensorData('a2', -50)

        self.sig4 = SensorData('b', -20)
        self.sig5 = SensorData('b1', -45)
        self.sig6 = SensorData('b2', -55)

    def test_single_update(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])

        result = nmap.get_space([self.sig1, self.sig2, self.sig3])
        self.assertEqual(result[0], 'a')
