from abc import ABC
from tensealstat.algebra.abstract_algebra import AbstractAlgebra

class AbstractStatistic(ABC):
    
    def list_test_assertion_asumption(self):
        raise NotImplementedError()

    def list_test_assertion_0_hypothesys(self):
        raise NotImplementedError()

    def encrypt_statistic(self, algebra:AbstractAlgebra, statistic_encrypted):
        raise NotImplementedError()

    def decrypt_statistic(self, algebra:AbstractAlgebra, statistic_encrypted):
        raise NotImplementedError()