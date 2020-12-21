import sys
import os
from scipy import stats
import tenseal as ts

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc
from tensealstat.tools_statistic import ToolsStatistic as tt
from tensealstat.tools_statistic_test import ToolsStatisticTest as ttt

# This test follows Larsen Marc 4Th edition P790

# 1 done by the key holder
context = tc.get_context_default()

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


 
# # 3 done by the agregator
statistic_encoded = tt.encode_anova_one_way(context, list_sample_encoded)

# # 4 done by the key holder
f_statistic, p_value = tt.decode_anova_one_way(context, statistic_encoded)


# # p value should be between about 0.996 and 0.997
print('via tensealstat')
print('f_statistic: ' + str(f_statistic))
print('p_value: ' + str(p_value))


# Test version
statistic_encoded = ttt.encode_anova_one_way(context, list_sample)
f_statistic, p_value = ttt.decode_anova_one_way(context, statistic_encoded)
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
