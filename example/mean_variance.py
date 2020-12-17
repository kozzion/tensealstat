import sys
import os
from time import time

import numpy as np
import tenseal as ts

sys.path.append(os.path.abspath('../../tensealstat'))

from tensealstat.tools_context import ToolsContext as tc
from tensealstat.tools_statistic import ToolsStatistic as tt

# m=1024 # enc 26 sec 
np.random.seed = 73
sample_size = 100 

sample_0 = np.random.normal(0, 1, sample_size)
sample_1 = np.random.normal(-2, 0.5, sample_size)

# parameters


# create TenSEALContext
context = tc.get_context_default()



t_start = time()
sample_0_encoded = ts.ckks_vector(context, sample_0.tolist())
sample_1_encoded = ts.ckks_vector(context, sample_1.tolist())
t_end = time()
print(f"Encryption of the training_set took {int(t_end - t_start)} seconds")


print('a')
print(np.mean(sample_0))
print(tt.mean(context, sample_0_encoded).decrypt()[0])
print(np.var(sample_0))
print(tt.variance(context, sample_0_encoded).decrypt()[0])

print('b')
print(np.mean(sample_1))
print(tt.mean(context, sample_1_encoded).decrypt()[0])
print(np.var(sample_1))
print(tt.variance(context, sample_1_encoded).decrypt()[0])
