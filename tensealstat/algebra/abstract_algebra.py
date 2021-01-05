from abc import ABC

class AbstractAlgebra(ABC):

    # TODO hide a bit
    def element_at(self, vector, index):
        raise NotImplementedError()

    def size_vector(self, vector):
        raise NotImplementedError()

    def encrypt_vector(self, scalar):
        raise NotImplementedError()

    def encrypt_scalar(self, scalar):
        raise NotImplementedError()

    #@abstractmethod
    def encrypt_scalar_inv(self, scalar):
        raise NotImplementedError()

    #@abstractmethod
    def decrypt_scalar(self, scalar):
        raise NotImplementedError()

    #@abstractmethod
    def sqrt(self, x):
        raise NotImplementedError()

    def sqr(self, x):
        raise NotImplementedError()

    def mean(self, sample):
        raise NotImplementedError()
    
    def sum(self, sample):
        raise NotImplementedError()

    def count_all(self, list_sample):
        raise NotImplementedError()
    
    def sum_all(self, list_sample):
        raise NotImplementedError()

    def sum_sample(self, list_sample):
        raise NotImplementedError()

    def sum_measurement(self, list_sample):
        raise NotImplementedError()

    def sum_squared_all(self, list_sample):
        raise NotImplementedError()

    def mean_all(self, list_sample):
        raise NotImplementedError()

    def variance(self, sample):
        raise NotImplementedError()

    def variance_pooled(self, sample_0, sample_1):
        raise NotImplementedError()