import sys
import os
from scipy import stats
import tenseal as ts
import numpy as np

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc
from tensealstat.algebra.algebra_numpy import AlgebraNumpy
from tensealstat.algebra.algebra_tenseal import AlgebraTenseal
from tensealstat.test.anova_one_way import AnovaOneWay

#
# This test follows Larsen Marc 4Th edition P790
#

# 1 done by the key holder
context = tc.get_context_default()
algebra_tenseal = AlgebraTenseal(context)
algebra_numpy = AlgebraNumpy()

# 2 done by the data holders
sample_0 = [69, 52, 71, 58, 59, 65]
sample_1 = [55, 60, 78, 58, 62, 66]
sample_2 = [66, 81, 70, 77, 57, 79]
sample_3 = [91, 72, 81, 67, 95, 84]

sample_0_encoded = ts.ckks_vector(context, sample_0)
sample_1_encoded = ts.ckks_vector(context, sample_1)
sample_2_encoded = ts.ckks_vector(context, sample_2)
sample_3_encoded = ts.ckks_vector(context, sample_3)

list_sample = []
list_sample.append(sample_0)
list_sample.append(sample_1)
list_sample.append(sample_2)
list_sample.append(sample_3)

list_sample_encoded = []
list_sample_encoded.append(sample_0_encoded)
list_sample_encoded.append(sample_1_encoded)
list_sample_encoded.append(sample_2_encoded)
list_sample_encoded.append(sample_3_encoded)

# 3 done by the agregator
statistic_encoded = AnovaOneWay.encode_statistic(algebra_tenseal, list_sample_encoded)

# 4 done by the key holder
f_statistic, p_value = AnovaOneWay.decode_statistic(algebra_tenseal, statistic_encoded)

# # p value should be between about 0.996 and 0.997
print('via tensealstat')
print('f_statistic: ' + str(f_statistic))
print('p_value: ' + str(p_value))

# Test version
statistic_encoded = AnovaOneWay.encode_statistic(algebra_numpy, list_sample)
f_statistic, p_value = AnovaOneWay.decode_statistic(algebra_numpy, statistic_encoded)
print('')
print('via tensealstattest')
print('f_statistic: ' + str(f_statistic))
print('p_value: ' + str(p_value))

# Scipy version
f_statistic, p_value = stats.f_oneway(sample_0, sample_1, sample_2, sample_3)
print('')
print('via scipy')
print('f_statistic: ' + str(f_statistic))
print('p_value: ' + str(1 - p_value))
