import math
import numpy as np
import tenseal as ts
from tensealstat.algebra.abstract_algebra import AbstractAlgebra

#TODO test is pickalble
#TODO make sure to handle the public and private keys better

class AlgebraTenseal(AbstractAlgebra):


    """docstring for AlgebraNumpy."""
    def __init__(self, context):
        super(AlgebraTenseal, self).__init__()
        self.context = context

    # TODO Hacky tensor indexing
    def element_at(self, vector, index):
        array_select = np.zeros(vector.size())
        array_select[index] = 1
        return vector * ts.ckks_vector(self.context, array_select)

    # less hacky
    def size_vector(self, vector):
        return vector.size()

    def encode_scalar(self, scalar):
        return ts.ckks_vector(self.context, [scalar])

    def encode_scalar_inv(self, scalar):
        return ts.ckks_vector(self.context, [1 / scalar])

    def decode_scalar(self, scalar):
        return scalar.decrypt()[0]

    def sqr(self, scalar):
        return scalar * scalar
    
    def count_all(self, list_sample_encoded):
        count = 0 
        for sample_encoded in list_sample_encoded:
            count += sample_encoded.size()
        return count
    
    def sum(self, sample_encoded):
        ones_encoded = ts.ckks_vector(self.context, [1] * sample_encoded.size())
        return sample_encoded.dot(ones_encoded)
        
    def sum_all(self, list_sample):
        sum = self.encode_scalar(0)
        for sample in list_sample:
            sum += self.sum(sample)
        return sum

    def sum_sample(self, list_sample):
        list_sum_sample = []
        for sample in list_sample:
            list_sum_sample.append(self.sum(sample))
        return list_sum_sample

    def sum_measurement(self, list_sample):
        list_sum_measurement = []
        for index_measurement in range(self.size_vector(list_sample[0])):
            list_sum_measurement.append(self.encode_scalar(0))
            for sample in list_sample:
                list_sum_measurement[index_measurement] += self.element_at(sample, index_measurement)
        return list_sum_measurement

    def sum_squared_all(self, list_sample):
        sum_squared_all = self.encode_scalar(0)
        for sample in list_sample:
            sum_squared_all += sample.dot(sample)
        return sum_squared_all
    
    def mean(self, sample):
        scale = self.encode_scalar_inv(sample.size())
        return self.sum(sample) * scale

    def mean_all(self, list_sample):
        scale = self.encode_scalar_inv(self.count_all(list_sample))
        return self.sum_all(list_sample) * scale

    def variance(self, sample):
        mean_encoded = self.mean(sample)
        scale = self.encode_scalar_inv(sample.size() - 1)
        return (sample - mean_encoded).dot(sample - mean_encoded) * scale

    def variance_pooled(self, sample_0_encoded, sample_1_encoded):
        mean_0_encoded = self.mean(sample_0_encoded) #TODO these means can be avoided
        mean_1_encoded = self.mean(sample_1_encoded)
        variance_0_encoded = (sample_0_encoded - mean_0_encoded).dot(sample_0_encoded - mean_0_encoded)
        variance_1_encoded = (sample_1_encoded - mean_1_encoded).dot(sample_1_encoded - mean_1_encoded)
        scale = self.encode_scalar_inv(sample_0_encoded.size() + sample_1_encoded.size() - 2)
        return (variance_0_encoded + variance_1_encoded) * scale