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
from tensealstat.statistic.student_t_equal_variance import StudentTEqualVariance


statistic_generator = StudentTEqualVariance()
#
# This test follows https://en.wikipedia.org/w/index.php?title=Welch%27s_t-test&oldid=994214781#Examples
# Example 1
#

# 1 done by the key holder
context = tc.get_context_default()
algebra_tenseal = AlgebraTenseal(context)
algebra_numpy = AlgebraNumpy()

# 2 done by the data holders
sample_0 = np.array([27.5, 21.0, 19.0, 23.6, 17.0, 17.9, 16.9, 20.1, 21.9, 22.6, 23.1, 19.6, 19.0, 21.7, 21.4])
sample_1 = np.array([27.1, 22.0, 20.8, 23.4, 23.4, 23.5, 25.8, 22.0, 24.8, 20.2, 21.9, 22.1, 22.9, 20.5, 24.4])

list_sample = [sample_0, sample_1]
list_sample_encrypted = [algebra_tenseal.encrypt_vector(sample) for sample in list_sample] 

# 3 done by the agregator
statistic_encrypted = statistic_generator.encrypt_statistic(algebra_tenseal, list_sample_encrypted)

# # 4 done by the key holder
t_statistic, degrees_of_freedom = statistic_generator.decrypt_statistic(algebra_tenseal, statistic_encrypted)
p_value = t.cdf(t_statistic, degrees_of_freedom)
# Assert.IsTrue(chi2_statistic ~= -2.46)
# Assert.IsTrue(p_value ~= 0.010)
print('')
print('via tensealstattest')
print('t_statistic: ' + str(t_statistic))
print('p_value: ' + str(p_value))

# Test version
statistic_encrypted = statistic_generator.encrypt_statistic(algebra_numpy, list_sample)
t_statistic, degrees_of_freedom = statistic_generator.decrypt_statistic(algebra_numpy, statistic_encrypted)
p_value = t.cdf(t_statistic, degrees_of_freedom)
# Assert.IsTrue(chi2_statistic ~= -2.46)
# Assert.IsTrue(p_value ~= 0.010)
print('')
print('via tensealstat')
print('t_statistic: ' + str(t_statistic))
print('p_value: ' + str(p_value))

t_statistic, p_value = stats.ttest_ind(sample_0, sample_1, equal_var=True)
print('')
print('via scipy')
print('t_statistic: ' + str(t_statistic))
print('p_value: ' + str(p_value / 2))