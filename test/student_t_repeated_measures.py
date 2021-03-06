import sys
import os
from scipy import stats
import tenseal as ts
import numpy as np
from scipy.stats import t

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc
from tensealstat.algebra.algebra_numpy import AlgebraNumpy
from tensealstat.algebra.algebra_tenseal import AlgebraTenseal
from tensealstat.statistic.student_t_repeated_measures import StudentTRepeatedMeasures


statistic_generator = StudentTRepeatedMeasures()
#
# This test follows Larsen Marc 4Th edition P790
#

# 1 done by the key holder
context = tc.get_context_default()
algebra_tenseal = AlgebraTenseal(context)
algebra_numpy = AlgebraNumpy()

# 2 done by the data holders
sample_0 = np.array([14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2])
sample_1 = np.array([13.8, 15.4, 11.3, 11.6, 16.4, 12.6, 11.8, 15.0, 14.4, 15.0])
list_sample = [sample_0, sample_1]
list_sample_encrypted = [algebra_tenseal.encrypt_vector(sample) for sample in list_sample] 

# 3 done by the agregator
statistic_encrypted = statistic_generator.encrypt_statistic(algebra_tenseal, list_sample_encrypted)

# 4 done by the key holder
t_statistic, degrees_of_freedom = statistic_generator.decrypt_statistic(algebra_tenseal, statistic_encrypted)
p_value = t.cdf(t_statistic, degrees_of_freedom)
# p value should be between about 0.94 and 0.95
print('via tensealstat')
print('t_statistic: ' + str(t_statistic))
print('p_value: ' + str(p_value))

# Test version
statistic_encrypted = statistic_generator.encrypt_statistic(algebra_numpy, list_sample)
t_statistic, degrees_of_freedom = statistic_generator.decrypt_statistic(algebra_numpy, statistic_encrypted)
p_value = t.cdf(t_statistic, degrees_of_freedom)
print('')
print('via tensealstattest')
print('t_statistic: ' + str(t_statistic))
print('p_value: ' + str(p_value))

# Scipy version
t_statistic, p_value = stats.ttest_rel(sample_0 ,sample_1)
print('')
print('via scipy')
print('t_statistic: ' + str(t_statistic))
print('p_value: ' + str(1 - (p_value / 2)))
