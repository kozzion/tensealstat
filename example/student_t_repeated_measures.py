import sys
import os
import numpy as np
import tenseal as ts
from scipy import stats

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc
from tensealstat.tools_statistic import ToolsStatistic as tt
from tensealstat.tools_statistic_test import ToolsStatisticTest as ttt

# This test follows Larsen Marc 4Th edition P790

# 1 done by the key holder
context = tc.get_context_default()

# 2 done by the data holders
sample_0 = np.array([14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2])
sample_1 = np.array([13.8, 15.4, 11.3, 11.6, 16.4, 12.6, 11.8, 15.0, 14.4, 15.0])

sample_0_encoded = ts.ckks_vector(context, sample_0.tolist())
sample_1_encoded = ts.ckks_vector(context, sample_1.tolist())

# 3 done by the agregator
statistic_encoded = tt.encode_student_t_repeated_measures(context, sample_0_encoded, sample_1_encoded)

# 4 done by the key holder
t_statistic, p_value = tt.decode_student_t_repeated_measures(context, statistic_encoded)

# p value should be between about 0.94 and 0.95
print('via tensealstat')
print('t_statistic: ' + str(t_statistic))
print('p_value: ' + str(p_value))

# Test version
statistic_encoded = ttt.encode_student_t_repeated_measures(context, sample_0, sample_1)
t_statistic, p_value = ttt.decode_student_t_repeated_measures(context, statistic_encoded)
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
