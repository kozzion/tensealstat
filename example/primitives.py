import sys
import os
import math
from time import time

import numpy as np
import tenseal as ts

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc
from tensealstat.tools_statistic import ToolsStatistic as tt

sample_0 = [14.6, 17.3, 10.9, 12.8, 16.6, 12.2, 11.2, 15.4, 14.8, 16.2]

# create TenSEALContext
context = tc.get_context_default()

print('encode_scalar')
print(23)
print(tt.encode_scalar(context, 23).decrypt()[0])

print('')
print('encode_scalar and mult')
print(str(4*5))
print((tt.encode_scalar(context, 4) * tt.encode_scalar(context, 5)).decrypt()[0])

print('')
print('encode_scalar and add')
print(str(4+5))
print((tt.encode_scalar(context, 4) + tt.encode_scalar(context, 5)).decrypt()[0])

print('')
print('inv0x2')
list_value = []
#list_value.append(0.001) # problematic
list_value.append(0.1)
list_value.append(0.5) 
list_value.append(1.0)
list_value.append(1.5)
#list_value.append(1.99) # problematic
#list_value.append(2.0) # problematic
for value in list_value:
    print(1 / value)
    value_encoded = tt.encode_scalar(context, value)
    value_encoded_inverted = tt.inv_0t2(context, value_encoded)
    print(value_encoded_inverted.decrypt()[0])


print('')
print('sqrt_0x1')
list_value.append(0.1)# problematic
list_value.append(0.5) 
list_value.append(0.7)
list_value.append(0.99)
for value in list_value:
    print(math.sqrt(value))
    value_encoded = tt.encode_scalar(context, value)
    value_encoded_inverted = tt.sqrt_0t1(context, value_encoded)
    print(value_encoded_inverted.decrypt()[0])


print('')
print('abs_1t1')
for value in [-1, -0.5, 0, 0.5, 0.7, 1]:
    print(abs(value))
    value_encoded = tt.encode_scalar(context, value)
    value_encoded_inverted = tt.abs_0t1(context, value_encoded)
    print(value_encoded_inverted.decrypt()[0])


print('')
print('min_max_0t1')
for list_value in [[0.8, 0.1], [0.6, 0.5], [0.15, 0.3]]:
    print(str(min(list_value)) + ' ' + str(max(list_value)))
    value_encoded = tt.encode_scalar(context, value)
    value_min_encoded, value_max_encoded = tt.min_max_0t1(context, list_value[0], list_value[1], d=20)
    print(str(value_min_encoded.decrypt()[0]) + ' ' +  str(value_max_encoded.decrypt()[0]))




# print('b')
# print(np.mean(sample_1))
# print(tt.mean(context, sample_1_encoded).decrypt()[0])
# print(np.var(sample_1))
# print(tt.variance(context, sample_1_encoded).decrypt()[0])
