import sys
import os
import math
from time import time

import numpy as np
import tenseal as ts

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc
from tensealstat.algebra.algebra_tenseal import AlgebraTenseal
from tensealstat.algebra.algebra_numpy import AlgebraNumpy

sample_0 = [14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2]

sample_1 = [14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2, 
            14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2, 
            14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2,
            14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2, 
            14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2,
            14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2, 
            14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2,
            14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2]

# create TenSEALContext
context = tc.get_context_default()
algebra_tenseal = AlgebraTenseal(context)
algebra_numpy = AlgebraNumpy()



print('mean')
print(algebra_numpy.mean(sample_0))
print(algebra_tenseal.decrypt_scalar(algebra_tenseal.mean(algebra_tenseal.encrypt_vector(sample_0))))

print('')
print('varriance')
print(algebra_numpy.variance(sample_0))
print(algebra_tenseal.decrypt_scalar(algebra_tenseal.variance(algebra_tenseal.encrypt_vector(sample_0))))

print('')
print('varriance')
print(algebra_numpy.variance(sample_1))
print(algebra_tenseal.decrypt_scalar(algebra_tenseal.variance(algebra_tenseal.encrypt_vector(sample_1))))
