import math

from tensealstat.algebra.abstract_algebra import AbstractAlgebra
from tensealstat.statistic.abstract_statistic import AbstractStatistic
from tensealstat.statistic.test_assertion import TestAssertion

class StudentTEqualVariance(AbstractStatistic):

    def encrypt_statistic(self, algebra:AbstractAlgebra, list_sample):
        if len(list_sample) != 2:  
            raise Exception("StudentTEqualVariance is a 2 sample procedure")
        sample_0 = list_sample[0]
        sample_1 = list_sample[1]

        size_sample_0 = algebra.size_vector(sample_0)
        size_sample_1 = algebra.size_vector(sample_1)

        mean_0 = algebra.mean(sample_0)
        mean_1 = algebra.mean(sample_1)
        variance = algebra.variance_pooled(sample_0, sample_1) * ((1 / size_sample_0) + (1 /size_sample_1))

        degrees_of_freedom = (size_sample_0 + size_sample_1 - 2)

        statistic_encoded = {}
        statistic_encoded['type_statistic'] = 'student_t_equal_variance'
        statistic_encoded['mean_difference'] = mean_0 - mean_1
        statistic_encoded['variance'] = variance
        statistic_encoded['degrees_of_freedom'] = degrees_of_freedom
        return statistic_encoded
    
    def decrypt_statistic(self, algebra:AbstractAlgebra, statistic_encoded):
        if not statistic_encoded['type_statistic'] == 'student_t_equal_variance':
            raise Exception('Incorrect statistic')
        mean_difference = algebra.decrypt_scalar(statistic_encoded['mean_difference'])
        variance = algebra.decrypt_scalar(statistic_encoded['variance'])
        degrees_of_freedom = statistic_encoded['degrees_of_freedom']
        t_statistic = mean_difference / math.sqrt(variance)
        return t_statistic, degrees_of_freedom