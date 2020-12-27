import sys
import os
from scipy import stats
import tenseal as ts
import numpy as np

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc

from tensealstat.algebra.algebra_numpy import AlgebraNumpy
from tensealstat.algebra.algebra_tenseal import AlgebraTenseal
from tensealstat.test.anova_repeated_measures import AnovaRepeatedMeasures


# 1 done by the key holder
context = tc.get_context_high()
algebra_tenseal = AlgebraTenseal(context)
algebra_numpy = AlgebraNumpy()

# http://www.itl.nist.gov/div898/handbook/eda/section3/eda35a.htm
sample_0 = [ 1.006, 0.996, 0.998, 1.000, 0.992, 0.993, 1.002, 0.999, 0.994, 1.000 ]
sample_1 = [ 0.998, 1.006, 1.000, 1.002, 0.997, 0.998, 0.996, 1.000, 1.006, 0.988 ]
sample_2 = [ 0.991, 0.987, 0.997, 0.999, 0.995, 0.994, 1.000, 0.999, 0.996, 0.996 ]
sample_3 = [ 1.005, 1.002, 0.994, 1.000, 0.995, 0.994, 0.998, 0.996, 1.002, 0.996 ]
sample_4 = [ 0.998, 0.998, 0.982, 0.990, 1.002, 0.984, 0.996, 0.993, 0.980, 0.996 ]
sample_5 = [ 1.009, 1.013, 1.009, 0.997, 0.988, 1.002, 0.995, 0.998, 0.981, 0.996 ]
sample_6 = [ 0.990, 1.004, 0.996, 1.001, 0.998, 1.000, 1.018, 1.010, 0.996, 1.002 ]
sample_7 = [ 0.998, 1.000, 1.006, 1.000, 1.002, 0.996, 0.998, 0.996, 1.002, 1.006 ]
sample_8 = [ 1.002, 0.998, 0.996, 0.995, 0.996, 1.004, 1.004, 0.998, 0.999, 0.991 ]
sample_9 = [ 0.991, 0.995, 0.984, 0.994, 0.997, 0.997, 0.991, 0.998, 1.004, 0.997 ]
            double[][] samples = new double[][] { sample_0, sample_1, sample_2, sample_3, sample_4, sample_5, sample_6, sample_7, sample_8, sample_9 ]
            double p_value = TestLevene.TestStatic(samples);
# Assert.IsTrue(0.98 < p_value);
# Assert.IsTrue(p_value < 0.99);