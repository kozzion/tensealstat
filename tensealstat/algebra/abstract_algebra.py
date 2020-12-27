import math
import numpy as np
import copy
from abc import ABC
#TODO test is pickalble
#TODO make sure to handle the public and private keys better

class AbstractAlgebra(ABC):


    def size_vector(self, vector):
        return len(vector)

    def encode_scalar(self, scalar):
        return scalar

    def encode_scalar_inv(self, scalar):
        return 1/scalar

    def decode_scalar(self, scalar):
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
            list_sum_measurement.append(self.encode_scalar(0))
            for sample in list_sample:
                list_sum_measurement[index_measurement] += sample[index_measurement]
        return list_sum_measurement

    def sum_squared_all(self, list_sample):
        sum_squared_all = self.encode_scalar(0)
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

    def variance_pooled(self, sample_0_encoded, sample_1_encoded):
        mean_0_encoded = self.mean(sample_0_encoded) #TODO these means can be avoided
        mean_1_encoded = self.mean(sample_1_encoded)
        variance_0_encoded = (sample_0_encoded - mean_0_encoded).dot(sample_0_encoded - mean_0_encoded)
        variance_1_encoded = (sample_1_encoded - mean_1_encoded).dot(sample_1_encoded - mean_1_encoded)
        scale = ts.ckks_vector(self, [1 / (sample_0_encoded.size() + sample_1_encoded.size() - 2)])
        return (variance_0_encoded + variance_1_encoded) * scale