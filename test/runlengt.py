import sys
import os
from scipy import stats
import tenseal as ts
import numpy as np
from scipy.stats import norm

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc
from tensealstat.algebra.abstract_algebra import AbstractAlgebra
from tensealstat.algebra.algebra_numpy import AlgebraNumpy
from tensealstat.algebra.algebra_tenseal import AlgebraTenseal
from tensealstat.statistic.abstract_statistic import AbstractStatistic
from tensealstat.statistic.z_run_lenght import ZRunLenght


statistic_generator = ZRunLenght()


algebra = AlgebraNumpy()
#          
# Test follows Larsen Marx 4Th edition P837
#
sample_0 = [61,53,58,51,52,34,45,52,46,52,37,39,50,38,55,59,57,64,73,46,48,47,40,35,40]
list_sample = [sample_0]
statistic_encrypted = statistic_generator.encrypt_statistic(algebra, list_sample)
z_statistic = statistic_generator.decrypt_statistic(algebra, statistic_encrypted)
p_value = 1 - norm.cdf(0.0, 1.0, z_statistic)
print(p_value)
print(p_value)
# Assert.IsTrue(p_value < 0.21)
# Assert.IsTrue(0.20 < p_value)