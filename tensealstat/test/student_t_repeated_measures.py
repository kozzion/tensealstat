import math
from scipy.stats import t

from tensealstat.algebra.abstract_algebra import AbstractAlgebra

class StudentTRepeatedMeasures(object):

    @staticmethod
    def encode_statistic(algebra:AbstractAlgebra, sample_0, sample_1):
        if algebra.size_vector(sample_0) != algebra.size_vector(sample_1):
            raise Exception('Samples should be of equal size')
        difference = sample_0 - sample_1
        mean_difference = algebra.mean(difference)
        variance = algebra.variance(difference)
        variance_rescale = algebra.size_vector(sample_0)
        degrees_of_freedom = algebra.size_vector(sample_0) - 1
        
        #TODO these all need to get pickled properly or jsonsed or something so they can be moved over http
        statistic_encoded = {}
        statistic_encoded['type_statistic'] = 'student_t_repeated_measures'
        statistic_encoded['mean_difference'] = mean_difference
        statistic_encoded['variance'] = variance   
        statistic_encoded['variance_rescale'] = variance_rescale
        statistic_encoded['degrees_of_freedom'] = degrees_of_freedom
        return statistic_encoded
    
    @staticmethod
    def decode_statistic(algebra:AbstractAlgebra, statistic_encoded):
        if not statistic_encoded['type_statistic'] == 'student_t_repeated_measures':
            raise Exception('Incorrect statistic')
    
        mean_difference = algebra.decode_scalar(statistic_encoded['mean_difference'])
        variance = algebra.decode_scalar(statistic_encoded['variance'])
        variance_rescale = statistic_encoded['variance_rescale']
        degrees_of_freedom = statistic_encoded['degrees_of_freedom']

        t_statistic = mean_difference / (math.sqrt(variance) / math.sqrt(variance_rescale))
        p_value = t.cdf(t_statistic, degrees_of_freedom)
        return t_statistic, p_value