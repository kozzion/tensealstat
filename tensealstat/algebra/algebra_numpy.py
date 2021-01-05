import math
import numpy as np
from tensealstat.algebra.abstract_algebra import AbstractAlgebra


#TODO test is pickalble
#TODO make sure to handle the public and private keys better

class AlgebraNumpy(AbstractAlgebra):

    """docstring for AlgebraNumpy."""
    def __init__(self):
        super(AlgebraNumpy, self).__init__()

    def size_vector(self, vector):
        return len(vector)

    def encrypt_list(self, list):
        return np.array(list)

    def encrypt_scalar(self, scalar):
        return scalar

    def encrypt_scalar_inv(self, scalar):
        return 1/scalar

    def decrypt_scalar(self, scalar):
        return scalar


    def sqrt(self, x):
        return math.sqrt(x)

    def sqr(self, x):
        return x * x

    def count_all(self, list_sample):
        count = 0 
        for sample in list_sample:
            count += len(sample)
        return count
    
    def sum(self, sample):
        return np.sum(sample)

    def sum_all(self, list_sample):
        all = 0
        for sample in list_sample:
            all += np.sum(sample)
        return all

    def sum_sample(self, list_sample):
        list_sum_sample = []
        for sample in list_sample:
            list_sum_sample.append(self.sum(sample))
        return list_sum_sample

    def sum_measurement(self, list_sample):
        list_sum_measurement = []
        for index_measurement in range(len(list_sample[0])):
            list_sum_measurement.append(self.encrypt_scalar(0))
            for sample in list_sample:
                list_sum_measurement[index_measurement] += sample[index_measurement]
        return list_sum_measurement

    def sum_squared_all(self, list_sample):
        sum_squared_all = self.encrypt_scalar(0)
        for sample in list_sample:
            for measurement in sample:
                sum_squared_all += self.sqr(measurement)
        return sum_squared_all

    def mean(self, sample):
        return np.mean(sample)

    def mean_all(self, list_sample):
        return self.sum_all(list_sample) / self.count_all(list_sample)

    def variance(self, sample):
        mean = self.mean(sample)
        return (sample - mean).dot(sample - mean) / (len(sample) - 1)
        #return np.var(sample) #BAD!!!

    def variance_pooled(self, sample_0, sample_1):
        mean_0 = self.mean(sample_0) #TODO these means can be avoided
        mean_1 = self.mean(sample_1)
        variance_0 = (sample_0 - mean_0).dot(sample_0 - mean_0)
        variance_1 = (sample_1 - mean_1).dot(sample_1 - mean_1)
        scale = 1 / (len(sample_0) + len(sample_1) - 2)
        return (variance_0 + variance_1) * scale
