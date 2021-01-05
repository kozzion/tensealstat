import math

from tensealstat.algebra.abstract_algebra import AbstractAlgebra
from tensealstat.statistic.abstract_statistic import AbstractStatistic
from tensealstat.statistic.test_assertion import TestAssertion

class AnovaOneWay(AbstractStatistic):

    def encrypt_statistic(self, algebra:AbstractAlgebra, list_sample):
        count_sample = len(list_sample)
        count_total = algebra.count_all(list_sample)
        mean_total = algebra.mean_all(list_sample)
        
        list_sample_mean = []
        for sample in list_sample:
            list_sample_mean.append(algebra.mean(sample))
    
        sstr = 0
        for sample, mean_sample in zip(list_sample, list_sample_mean):
            sstr += algebra.size_vector(sample) * algebra.sqr(mean_sample - mean_total)
        
        sse = 0
        for sample, sample_mean in zip(list_sample, list_sample_mean):
            sse += (sample - sample_mean).dot(sample - sample_mean)

        degrees_of_freedom_0 = (count_sample - 1.0)
        degrees_of_freedom_1 = (count_total - count_sample)
        summed_variance = sstr  * algebra.encrypt_scalar_inv(degrees_of_freedom_0)
        total_variance = sse * algebra.encrypt_scalar_inv(degrees_of_freedom_1)


        #TODO these all need to get pickled properly or jsonsed or something so they can be moved over http
        statistic_encrypted = {}
        statistic_encrypted['type_statistic'] = 'anova_one_way'
        statistic_encrypted['degrees_of_freedom_0'] = degrees_of_freedom_0
        statistic_encrypted['degrees_of_freedom_1'] = degrees_of_freedom_1
        statistic_encrypted['summed_variance'] = summed_variance
        statistic_encrypted['total_variance'] = total_variance
        return statistic_encrypted
    
    def decrypt_statistic(self, algebra, statistic_encrypted):
        if not statistic_encrypted['type_statistic'] == 'anova_one_way':
            raise Exception('Incorrect statistic')

        degrees_of_freedom_0 = statistic_encrypted['degrees_of_freedom_0']
        degrees_of_freedom_1 = statistic_encrypted['degrees_of_freedom_1']
        summed_variance = algebra.decrypt_scalar(statistic_encrypted['summed_variance'])
        total_variance = algebra.decrypt_scalar(statistic_encrypted['total_variance'])

        #F-transform
        f_statistic = summed_variance / total_variance
        return f_statistic, degrees_of_freedom_0, degrees_of_freedom_1
