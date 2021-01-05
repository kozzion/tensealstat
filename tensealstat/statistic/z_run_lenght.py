import math

from tensealstat.algebra.abstract_algebra import AbstractAlgebra
from tensealstat.statistic.abstract_statistic import AbstractStatistic
from tensealstat.statistic.test_assertion import TestAssertion

class ZRunLenght(AbstractStatistic):

    def encrypt_statistic(self, algebra:AbstractAlgebra, list_sample):
        if len(list_sample) != 1:  
            raise Exception("ZRunLenght is a one sample procedure")
        sample_0 = list_sample[0]
        sample_0_size = algebra.size_vector(sample_0)
        if sample_0_size < 2:  
            raise Exception("ZRunLenght requires at least 2 measurements")

        statistic = 1
        sign = sample_0[0] < sample_0[1]
        for index in range(1, sample_0_size):
            new_sign = sample_0[index - 1] < sample_0[index]
            if(sign != new_sign):
                statistic += 1
                sign = new_sign

        expected_value = ((2.0 * sample_0.Count) - 1.0) / 3.0
        variance = ((16.0 * sample_0.Count) - 29.0) / 90.0
        z_statistic = (statistic - expected_value) / math.sqrt(variance)

        statistic_encrypted = {}
        statistic_encrypted['type_statistic'] = 'z_run_lenght'
        statistic_encrypted['z_statistic'] = z_statistic
        return statistic_encrypted

    def decrypt_statistic(self, algebra:AbstractAlgebra, statistic_encoded):
        if not statistic_encoded['type_statistic'] == 'z_run_lenght':
            raise Exception('Incorrect statistic')
        z_statistic = algebra.decrypt_scalar(statistic_encoded['z_statistic'])
   
        return z_statistic