import math

from tensealstat.algebra.abstract_algebra import AbstractAlgebra
from tensealstat.statistic.abstract_statistic import AbstractStatistic
from tensealstat.statistic.test_assertion import TestAssertion

class StudentTUnequalVariance(AbstractStatistic):

    def encrypt_statistic(self, algebra:AbstractAlgebra, list_sample):
        if len(list_sample) != 2:  
            raise Exception("StudentTUnequalVariance is a 2 sample procedure")
        sample_0 = list_sample[0]
        sample_1 = list_sample[1]

        mean_0 = algebra.mean(sample_0)
        mean_1 = algebra.mean(sample_1)

        variance_0 = algebra.variance(sample_0)
        variance_1 = algebra.variance(sample_1)

        size_sample_0 = algebra.size_vector(sample_0)
        size_sample_1 = algebra.size_vector(sample_1)

        variance_scaled_0 = variance_0 * (1 / size_sample_0)
        variance_scaled_1 = variance_1 * (1 / size_sample_1)
 
        variance = variance_scaled_0 + variance_scaled_1

        #Welch–Satterthwaite equation:
        size_sample_0_pow = 1 / (size_sample_0 * size_sample_0 * (size_sample_0 - 1))
        size_sample_1_pow = 1 / (size_sample_1 * size_sample_1 * (size_sample_1 - 1))
        variance_0_pow = variance_0 * variance_0
        variance_0_pow = variance_0_pow * variance_0_pow
        variance_1_pow = variance_1 * variance_1 * variance_1 * variance_1
        degrees_of_freedom_scale = (variance_0_pow * size_sample_0_pow) + (variance_1_pow * size_sample_1_pow)

        statistic_encrypted = {}
        statistic_encrypted['type_statistic'] = 'student_t_unequal_variance'
        statistic_encrypted['mean_difference'] = mean_0 - mean_1
        statistic_encrypted['variance'] = variance
        statistic_encrypted['degrees_of_freedom_scale'] = degrees_of_freedom_scale
        return statistic_encrypted
    
    def decrypt_statistic(self, algebra:AbstractAlgebra, statistic_encrypted):
        if not statistic_encrypted['type_statistic'] == 'student_t_unequal_variance':
            raise Exception('Incorrect statistic')
        mean_difference = algebra.decrypt_scalar(statistic_encrypted['mean_difference'])
        variance = algebra.decrypt_scalar(statistic_encrypted['variance'])
        degrees_of_freedom_scale = algebra.decrypt_scalar(statistic_encrypted['degrees_of_freedom_scale'])

        degrees_of_freedom = (variance * variance) / degrees_of_freedom_scale
        t_statistic = mean_difference / math.sqrt(variance)

        return t_statistic, degrees_of_freedom