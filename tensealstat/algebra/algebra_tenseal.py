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

    def encrypt_vector(self, vector):
        return ts.ckks_vector(self.context, vector)

    def encrypt_scalar(self, scalar):
        return ts.ckks_vector(self.context, [scalar])

    def encrypt_scalar_inv(self, scalar):
        return ts.ckks_vector(self.context, [1 / scalar])

    def decrypt_scalar(self, scalar):
        return scalar.decrypt()[0]

    def sqr(self, scalar):
        return scalar * scalar
    
    def count_all(self, list_sample_encryptd):
        count = 0 
        for sample_encryptd in list_sample_encryptd:
            count += sample_encryptd.size()
        return count
    
    def sum(self, sample:ts.ckks_vector):
        return sample.sum()
        
    def sum_all(self, list_sample):
        sum = self.encrypt_scalar(0)
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
            list_sum_measurement.append(self.encrypt_scalar(0))
            for sample in list_sample:
                list_sum_measurement[index_measurement] += self.element_at(sample, index_measurement)
        return list_sum_measurement

    def sum_squared_all(self, list_sample):
        sum_squared_all = self.encrypt_scalar(0)
        for sample in list_sample:
            sum_squared_all += sample.dot(sample)
        return sum_squared_all
    
    def mean(self, sample):
        scale = self.encrypt_scalar_inv(sample.size())
        return self.sum(sample) * scale

    def mean_all(self, list_sample):
        scale = self.encrypt_scalar_inv(self.count_all(list_sample))
        return self.sum_all(list_sample) * scale

    def variance(self, sample):
        mean_encryptd = self.mean(sample)
        scale = self.encrypt_scalar_inv(sample.size() - 1)
        return (sample - mean_encryptd).dot(sample - mean_encryptd) * scale

    def variance_pooled(self, sample_0_encryptd, sample_1_encryptd):
        mean_0_encryptd = self.mean(sample_0_encryptd) #TODO these means can be avoided
        mean_1_encryptd = self.mean(sample_1_encryptd)
        variance_0_encryptd = (sample_0_encryptd - mean_0_encryptd).dot(sample_0_encryptd - mean_0_encryptd)
        variance_1_encryptd = (sample_1_encryptd - mean_1_encryptd).dot(sample_1_encryptd - mean_1_encryptd)
        scale = self.encrypt_scalar_inv(sample_0_encryptd.size() + sample_1_encryptd.size() - 2)
        return (variance_0_encryptd + variance_1_encryptd) * scale