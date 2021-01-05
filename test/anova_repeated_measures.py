import sys
import os
from scipy import stats
import tenseal as ts
import numpy as np
from scipy.stats import f

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc

from tensealstat.algebra.algebra_numpy import AlgebraNumpy
from tensealstat.algebra.algebra_tenseal import AlgebraTenseal
from tensealstat.statistic.anova_repeated_measures import AnovaRepeatedMeasures

statistic_generator = AnovaRepeatedMeasures()
'''
This test follows Larsen Marc 4Th edition P779
'''
# 1 done by the key holder
context = tc.get_context_default()
algebra_tenseal = AlgebraTenseal(context)


# 2 done by the data holders
sample_0 = [8, 11, 9, 16, 24]
sample_1 = [2, 1, 12, 11, 19]
sample_2 = [-2, 0, 6, 2 , 11]
list_sample = [sample_0, sample_1, sample_2]
list_sample_encrypted = [algebra_tenseal.encrypt_vector(sample) for sample in list_sample] 

# 3 done by the agregator
statistic_encrypted = statistic_generator.encrypt_statistic(algebra_tenseal, list_sample_encrypted)

# 4 done by the key holder
f_statistic_sample, f_statistic_measurement, degrees_of_freedom_0_sample, degrees_of_freedom_0_measurement, degrees_of_freedom_1 = statistic_generator.decode_statistic(algebra_tenseal, statistic_encrypted)
p_value_sample = f.cdf(f_statistic_sample, degrees_of_freedom_0_sample, degrees_of_freedom_1)
p_value_measurement = f.cdf(f_statistic_measurement, degrees_of_freedom_0_measurement, degrees_of_freedom_1)
# Assert.IsTrue(0.998 < p_values.Item1)
# Assert.IsTrue(p_values.Item1<  0.999)
# Assert.IsTrue(0.998 < p_values.Item2)
# Assert.IsTrue(p_values.Item2 <0.999)
print('via tensealstat')
print('f_statistic sample:      ' + str(f_statistic_sample))
print('f_statistic measurement: ' + str(f_statistic_measurement))
print('p_value sample:          ' + str(p_value_sample))
print('p_value measurement:     ' + str(p_value_measurement))


algebra_numpy = AlgebraNumpy()
statistic_encrypted = statistic_generator.encrypt_statistic(algebra_numpy, list_sample)
f_statistic_sample, f_statistic_measurement, degrees_of_freedom_0_sample, degrees_of_freedom_0_measurement, degrees_of_freedom_1 = statistic_generator.decode_statistic(algebra_numpy, statistic_encrypted)
p_value_sample = f.cdf(f_statistic_sample, degrees_of_freedom_0_sample, degrees_of_freedom_1)
p_value_measurement = f.cdf(f_statistic_measurement, degrees_of_freedom_0_measurement, degrees_of_freedom_1)
# Assert.IsTrue(0.998 < p_values.Item1)
# Assert.IsTrue(p_values.Item1<  0.999)
# Assert.IsTrue(0.998 < p_values.Item2)
# Assert.IsTrue(p_values.Item2 <0.999)
print('via tensealstat')
print('f_statistic sample:      ' + str(f_statistic_sample))
print('f_statistic measurement: ' + str(f_statistic_measurement))
print('p_value sample:          ' + str(p_value_sample))
print('p_value measurement:     ' + str(p_value_measurement))

#Test does not not exist in scipy

# Larsen Marx 4Th editiopn P781
sample_0 = [13.8, 12.9, 25.9, 18.0, 15.2]
sample_1 = [11.7, 16.7, 29.8, 23.1, 20.2]
sample_2 = [14.0, 15.5, 27.8, 23.0, 19.0]
sample_3 = [12.6, 13.8, 25.0, 16.9, 13.7]
list_sample = [sample_0, sample_1, sample_2]
list_sample_encrypted = [algebra_tenseal.encrypt_vector(sample) for sample in list_sample] 

statistic_encrypted = statistic_generator.encrypt_statistic(algebra_numpy, list_sample)
f_statistic_sample, f_statistic_measurement, degrees_of_freedom_0_sample, degrees_of_freedom_0_measurement, degrees_of_freedom_1 = statistic_generator.decode_statistic(algebra_numpy, statistic_encrypted)
p_value_sample = f.cdf(f_statistic_sample, degrees_of_freedom_0_sample, degrees_of_freedom_1)
p_value_measurement = f.cdf(f_statistic_measurement, degrees_of_freedom_0_measurement, degrees_of_freedom_1)
# Assert.IsTrue(0.995 < p_values.Item1);
# Assert.IsTrue(p_values.Item1 < 0.996);
# Assert.IsTrue(0.999 < p_values.Item2);
# Assert.IsTrue(p_values.Item2 < 1.000);
print('via tensealstat')
print('f_statistic sample:      ' + str(f_statistic_sample))
print('f_statistic measurement: ' + str(f_statistic_measurement))
print('p_value sample:          ' + str(p_value_sample))
print('p_value measurement:     ' + str(p_value_measurement))