import sys
import os
from scipy import stats
import tenseal as ts
import numpy as np
from scipy.stats import chi2

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc

from tensealstat.algebra.algebra_numpy import AlgebraNumpy
from tensealstat.algebra.algebra_tenseal import AlgebraTenseal
from tensealstat.statistic.chi2_variance import Chi2Variance

variance_h0 = 0.01
statistic_generator = Chi2Variance(variance_h0)

'''
# https://www.itl.nist.gov/div898/handbook/eda/section3/eda3581.htm
'''
# 1 done by the key holder
context = tc.get_context_default()
algebra_tenseal = AlgebraTenseal(context)


# 2 done by the data holders
sample_0 = [ 1.006, 0.996, 0.998, 1.000, 0.992, 0.993, 1.002, 0.999, 0.994, 1.000 ]
sample_0.extend([ 0.998, 1.006, 1.000, 1.002, 0.997, 0.998, 0.996, 1.000, 1.006, 0.988 ])
sample_0.extend([ 0.991, 0.987, 0.997, 0.999, 0.995, 0.994, 1.000, 0.999, 0.996, 0.996 ])
sample_0.extend([ 1.005, 1.002, 0.994, 1.000, 0.995, 0.994, 0.998, 0.996, 1.002, 0.996 ])
sample_0.extend([ 0.998, 0.998, 0.982, 0.990, 1.002, 0.984, 0.996, 0.993, 0.980, 0.996 ])
sample_0.extend([ 1.009, 1.013, 1.009, 0.997, 0.988, 1.002, 0.995, 0.998, 0.981, 0.996 ])
sample_0.extend([ 0.990, 1.004, 0.996, 1.001, 0.998, 1.000, 1.018, 1.010, 0.996, 1.002 ])
sample_0.extend([ 0.998, 1.000, 1.006, 1.000, 1.002, 0.996, 0.998, 0.996, 1.002, 1.006 ])
sample_0.extend([ 1.002, 0.998, 0.996, 0.995, 0.996, 1.004, 1.004, 0.998, 0.999, 0.991 ])
sample_0.extend([ 0.991, 0.995, 0.984, 0.994, 0.997, 0.997, 0.991, 0.998, 1.004, 0.997 ])
list_sample = [sample_0]
list_sample_encrypted = [algebra_tenseal.encrypt_vector(sample) for sample in list_sample] 


# 3 done by the agregator
statistic_encrypted = statistic_generator.encrypt_statistic(algebra_tenseal, list_sample_encrypted)

# 4 done by the key holder
chi2_statistic, degrees_of_freedom_0 = statistic_generator.decrypt_statistic(algebra_tenseal, statistic_encrypted)
p_value = chi2.cdf(chi2_statistic, degrees_of_freedom_0)

# Assert.IsTrue(chi2_statistic ~= 0.3903)
# Assert.IsTrue(p_value ~= 0.0)
print('via tensealstat')
print('chi2_statistic:      ' + str(chi2_statistic))
print('p_value:             ' + str(p_value))



algebra_numpy = AlgebraNumpy()
statistic_encrypted = statistic_generator.encrypt_statistic(algebra_numpy, list_sample)
chi2_statistic, degrees_of_freedom_0 = statistic_generator.decrypt_statistic(algebra_numpy, statistic_encrypted)
p_value = chi2.cdf(chi2_statistic, degrees_of_freedom_0)

# Assert.IsTrue(chi2_statistic ~= 0.3903)
# Assert.IsTrue(p_value ~= 0.0)
print('via tensealstat')
print('chi2_statistic:      ' + str(chi2_statistic))
print('p_value:             ' + str(p_value))