    
import math
from tensealstat.algebra.abstract_algebra import AbstractAlgebra
from scipy.stats import t

class StudentTEqualVariance(object):

    @staticmethod
    def encode_statistic(algebra:AbstractAlgebra, sample_0_encoded, sample_1_encoded):
        mean_0_encoded = algebra.mean(sample_0_encoded)
        mean_1_encoded = algebra.mean(sample_1_encoded)
        variance_encoded = algebra.variance_pooled(sample_0_encoded, sample_1_encoded)
        variance_rescale =  algebra.encod (1.0 / sample_0_encoded.size()) + (1.0 / sample_1_encoded.size())
        degrees_of_freedom = (sample_0_encoded.size() + sample_1_encoded.size() - 2)

        #TODO these all need to get pickled properly or jsonsed or something so they can be moved over http
        statistic_encoded = {}
        statistic_encoded['type_statistic'] = 'student_t_equal_variance'
        statistic_encoded['mean_difference_encoded'] = mean_0_encoded - mean_1_encoded
        statistic_encoded['variance_encoded'] = variance_encoded
        statistic_encoded['variance_rescale'] = variance_rescale
        statistic_encoded['degrees_of_freedom'] = degrees_of_freedom
        return statistic_encoded
    
    @staticmethod
    def decode_statistic(algebra:AbstractAlgebra, statistic_encoded):
        if not statistic_encoded['type_statistic'] == 'student_t_equal_variance':
            raise Exception('Incorrect statistic')
        mean_difference = statistic_encoded['mean_difference_encoded'].decrypt()[0]
        

        variance = statistic_encoded['variance_encoded'].decrypt()[0]
        variance_rescale = statistic_encoded['variance_rescale']
        degrees_of_freedom = statistic_encoded['degrees_of_freedom']
        t_statistic = mean_difference / (algebra.sqrt(variance) /algebra.sqrt(variance_rescale))
        p_value = t.cdf(t_statistic, degrees_of_freedom)
        return t_statistic, p_value