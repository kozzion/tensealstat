import math

from tensealstat.algebra.abstract_algebra import AbstractAlgebra
from tensealstat.statistic.abstract_statistic import AbstractStatistic
from tensealstat.statistic.test_assertion import TestAssertion

class StudentTRepeatedMeasures(object):


    def encrypt_statistic(self, algebra:AbstractAlgebra, list_sample):
        if len(list_sample) != 2:  
            raise Exception("StudentTRepeatedMeasures is a 2 sample procedure")
        sample_0 = list_sample[0]
        sample_1 = list_sample[1]

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
    
    def decrypt_statistic(self, algebra:AbstractAlgebra, statistic_encoded):
        if not statistic_encoded['type_statistic'] == 'student_t_repeated_measures':
            raise Exception('Incorrect statistic')
    
        mean_difference = algebra.decode_scalar(statistic_encoded['mean_difference'])
        variance = algebra.decode_scalar(statistic_encoded['variance'])
        variance_rescale = statistic_encoded['variance_rescale']
        degrees_of_freedom = statistic_encoded['degrees_of_freedom']

        t_statistic = mean_difference / (math.sqrt(variance) / math.sqrt(variance_rescale))
        
        return t_statistic, degrees_of_freedom