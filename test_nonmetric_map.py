import unittest
from kalman_filter.sensor import SensorData
from kalman_filter.sensor.nonmetric_map import NonMetricMap

class testNMM(unittest.TestCase):
    def setUp(self):
        self.sig1 = SensorData('a', -20)
        self.sig2 = SensorData('a1', -60)
        self.sig3 = SensorData('a2', -80)

        self.sig4 = SensorData('b', -20)
        self.sig5 = SensorData('b1', -65)
        self.sig6 = SensorData('b2', -85)

    def test_single_update(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])

        result = nmap.get_space([self.sig1, self.sig2, self.sig3])
        self.assertEqual(result[0], 'a')
    
    def test_double_update_first(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])
        nmap.update([self.sig4, self.sig5, self.sig6])

        result = nmap.get_space([self.sig1, self.sig2, self.sig3])
        self.assertEqual(result[0], 'a')

    def test_double_update_second(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])
        nmap.update([self.sig4, self.sig5, self.sig6])

        result = nmap.get_space([self.sig4, self.sig5, self.sig6])
        self.assertEqual(result[0], 'b')

    def test_single_partial_missing_a1(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])

        result = nmap.get_space([self.sig1, self.sig3])
        self.assertEqual(result[0], 'a')

    def test_single_partial_missing_a2(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])

        result = nmap.get_space([self.sig1, self.sig2])
        self.assertEqual(result[0], 'a')

    def test_single_partial_missing_a(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])

        result = nmap.get_space([self.sig2, self.sig3])
        self.assertEqual(result[0], 'a1')

    def test_double_partial_missing_a1(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])
        nmap.update([self.sig4, self.sig5, self.sig6])

        result = nmap.get_space([self.sig1, self.sig3])
        self.assertEqual(result[0], 'a')

    def test_double_partial_missing_a2(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])
        nmap.update([self.sig4, self.sig5, self.sig6])

        result = nmap.get_space([self.sig1, self.sig2])
        self.assertEqual(result[0], 'a')

    def test_double_partial_missing_a(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])
        nmap.update([self.sig4, self.sig5, self.sig6])

        result = nmap.get_space([self.sig2, self.sig3])
        self.assertEqual(result[0], 'a1')

    def test_double_partial_adding_b1(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])
        nmap.update([self.sig4, self.sig5, self.sig6])

        result = nmap.get_space([self.sig1, self.sig2, self.sig3, self.sig4])
        self.assertEqual(result[0], 'a')

    def test_double_partial_adding_b2(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])
        nmap.update([self.sig4, self.sig5, self.sig6])

        result = nmap.get_space([self.sig1, self.sig2, self.sig3, self.sig5])
        self.assertEqual(result[0], 'a')

    def test_double_partial_adding_b3(self):
        nmap = NonMetricMap()
        nmap.update([self.sig1, self.sig2, self.sig3])
        nmap.update([self.sig4, self.sig5, self.sig6])

        result = nmap.get_space([self.sig1, self.sig2, self.sig3, self.sig6])
        self.assertEqual(result[0], 'a')
