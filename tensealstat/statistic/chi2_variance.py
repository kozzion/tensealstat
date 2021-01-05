import math

from tensealstat.algebra.abstract_algebra import AbstractAlgebra
from tensealstat.statistic.abstract_statistic import AbstractStatistic
from tensealstat.statistic.test_assertion import TestAssertion

class Chi2Variance(AbstractStatistic):

    """docstring for Chi2Variance."""
    def __init__(self, variance_h0):
        super(Chi2Variance, self).__init__()
        self.variance_h0 = variance_h0

    def encrypt_statistic(self, algebra:AbstractAlgebra, list_sample):
        if len(list_sample) != 1:  
            raise Exception("Chi2Variance is a 1 sample procedure")
        sample_0 = list_sample[0]
        size_sample_0 = algebra.size_vector(sample_0)

        variance = algebra.variance(sample_0)
        degrees_of_freedom = size_sample_0 - 1
        chi2_statistic =  variance * (degrees_of_freedom / self.variance_h0)

        statistic_encrypted = {}
        statistic_encrypted['type_statistic'] = 'chi2_variance'
        statistic_encrypted['chi2_statistic'] = chi2_statistic
        statistic_encrypted['degrees_of_freedom'] = degrees_of_freedom
        return statistic_encrypted
    
    def decrypt_statistic(self, algebra:AbstractAlgebra, statistic_encrypted):
        if not statistic_encrypted['type_statistic'] == 'chi2_variance':
            raise Exception('Incorrect statistic')

        chi2_statistic = algebra.decrypt_scalar(statistic_encrypted['chi2_statistic'])
        degrees_of_freedom = statistic_encrypted['degrees_of_freedom']
        return chi2_statistic, degrees_of_freedom