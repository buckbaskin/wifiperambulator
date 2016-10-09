from kalman_filter.sensor import SensorData
from kalman_filter.sensor.nonmetric_map import NonMetricMap

nmap = NonMetricMap()

sig1 = SensorData('a', -20)
sig2 = SensorData('a1', -40)
sig3 = SensorData('a2', -50)

sig4 = SensorData('b', -20)
sig5 = SensorData('b1', -45)
sig6 = SensorData('b2', -55)

nmap.update([sig1, sig2, sig3])

result = nmap.get_space([sig1, sig2, sig3])
print('result: %s' % (result,))
