import sys
import os
from scipy import stats
import tenseal as ts

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc
from tensealstat.tools_statistic_test import ToolsStatisticTest as ttt
from tensealstat.tools_statistic import ToolsStatistic as tt

# This test follows Larsen Marc 4Th edition P779

# 1 done by the key holder
context = tc.get_context_default()

# 2 done by the data holders

sample_0 = [8, 11, 9, 16, 24]
sample_1 = [2, 1, 12, 11, 19]
sample_2 = [-2, 0, 6, 2 , 11]

sample_0_encoded = ts.ckks_vector(context, sample_0)
sample_1_encoded = ts.ckks_vector(context, sample_1)
sample_2_encoded = ts.ckks_vector(context, sample_2)

list_sample = []
list_sample.append(sample_0)
list_sample.append(sample_1)
list_sample.append(sample_2)

list_sample_encoded = []
list_sample_encoded.append(sample_0_encoded)
list_sample_encoded.append(sample_1_encoded)
list_sample_encoded.append(sample_2_encoded)

# 3 done by the agregator
# statistic_encoded = tt.encode_anova_repeated_measures(context, list_sample_encoded)

# # 4 done by the key holder
# f_statistic, p_value = tt.decode_anova_one_way(context, statistic_encoded)


# # p value should be between about 0.996 and 0.997
# print('via tensealstat')
# print('f_statistic: ' + str(f_statistic))
# print('p_value: ' + str(p_value))

statistic_encoded = ttt.encode_anova_repeated_measures(context, list_sample)
f_statistic_sample, f_statistic_measurement, p_value_sample, p_value_measurement = ttt.decode_anova_repeated_measures(context, statistic_encoded)
# Assert.IsTrue(0.995 < p_values.Item1);
# Assert.IsTrue(p_values.Item1 < 0.996);
# Assert.IsTrue(0.999 < p_values.Item2);
# Assert.IsTrue(p_values.Item2 < 1.000);
print('via tensealstat')
print('f_statistic sample:      ' + str(f_statistic_sample))
print('f_statistic measurement: ' + str(f_statistic_measurement))
print('p_value sample:          ' + str(p_value_sample))
print('p_value measurement:     ' + str(p_value_measurement))

#does not not exist in scipy
# f_statistic, p_value = stats.f_oneway(sample_0, sample_1, sample_2)
# print('')
# print('via scipy')
# print('f_statistic: ' + str(f_statistic))
# print('p_value: ' + str(1 - (p_value / 2)))
