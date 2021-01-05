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
from tensealstat.statistic.anova_one_way import AnovaOneWay



statistic_generator = AnovaOneWay()
#
# This test follows Larsen Marc 4Th edition P790
#
sample_0 = [69, 52, 71, 58, 59, 65]
sample_1 = [55, 60, 78, 58, 62, 66]
sample_2 = [66, 81, 70, 77, 57, 79]
sample_3 = [91, 72, 81, 67, 95, 84]
list_sample = [sample_0, sample_1, sample_2, sample_3]


# 1 done by the key holder
context = tc.get_context_default()
algebra_tenseal = AlgebraTenseal(context)

# 2 done by the data holders
list_sample_encrypted = [algebra_tenseal.encrypt_vector(sample) for sample in list_sample] 

# 3 done by the agregator
statistic_encrypted = statistic_generator.encrypt_statistic(algebra_tenseal, list_sample_encrypted)

# 4 done by the key holder
f_statistic, degrees_of_freedom_0, degrees_of_freedom_1 = statistic_generator.decrypt_statistic(algebra_tenseal, statistic_encrypted)
p_value = f.cdf(f_statistic, degrees_of_freedom_0, degrees_of_freedom_1)
# # p value should be between about 0.996 and 0.997
print('via tensealstat')
print('f_statistic: ' + str(f_statistic))
print('p_value: ' + str(p_value))

# Test version
algebra_numpy = AlgebraNumpy()

statistic_encrypted = AnovaOneWay.encrypt_statistic(algebra_numpy, list_sample)
f_statistic, degrees_of_freedom_0, degrees_of_freedom_1 = statistic_generator.decrypt_statistic(algebra_numpy, statistic_encrypted)
p_value = f.cdf(f_statistic, degrees_of_freedom_0, degrees_of_freedom_1)
print('')
print('via tensealstattest')
print('f_statistic: ' + str(f_statistic))
print('p_value: ' + str(p_value))

# Scipy version
f_statistic, p_value = stats.f_oneway(list_sample[0], list_sample[1], list_sample[2], list_sample[3])
print('')
print('via scipy')
print('f_statistic: ' + str(f_statistic))
print('p_value: ' + str(1 - p_value))
