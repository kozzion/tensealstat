import math

from tensealstat.algebra.abstract_algebra import AbstractAlgebra
from tensealstat.statistic.abstract_statistic import AbstractStatistic
from tensealstat.statistic.test_assertion import TestAssertion

class AnovaRepeatedMeasures(AbstractStatistic):

    def encrypt_statistic(self, algebra:AbstractAlgebra, list_sample):
        count_sample = len(list_sample)
        count_measurement = algebra.size_vector(list_sample[0])
        for sample in list_sample:
            if algebra.size_vector(sample) != count_measurement:
                raise Exception('Samples should be of equal size')

        count_total = count_sample * count_measurement
        total_mean = algebra.mean_all(list_sample)
        sum_squared_all = algebra.sum_squared_all(list_sample)
        list_sum_sample = algebra.sum_sample(list_sample)
        list_sum_measurement = algebra.sum_measurement(list_sample)

        # compute C
        c = algebra.sqr(total_mean * algebra.encrypt_scalar(count_total))
        c *= algebra.encrypt_scalar_inv(count_total)

        sstot = sum_squared_all - c

        ssb = 0
        for sum_measurement in list_sum_measurement:
            ssb += algebra.sqr(sum_measurement) 
        ssb *= 1 / count_sample
        ssb -= c

        sstr = 0
        for sum_sample in list_sum_sample:
            sstr += algebra.sqr(sum_sample)
        sstr *= 1 / count_measurement
        sstr -= c




        sse = sstot - ssb - sstr
        #sstot = 767
        #ssb = 437
        #sstr = 260
        #c = 1126

        #sstot = 581
        #ssb = 495
        #sstr = 56.3
        #c = 6793


        degrees_of_freedom_0_sample      = (count_sample - 1.0)
        degrees_of_freedom_0_measurement = (count_measurement - 1.0)
        degrees_of_freedom_1             = degrees_of_freedom_0_sample * degrees_of_freedom_0_measurement

        total_variance = sse * (1 / degrees_of_freedom_1)
        summed_variance_sample =  sstr * algebra.encrypt_scalar_inv(degrees_of_freedom_0_sample)
        summed_variance_measurement = ssb * algebra.encrypt_scalar_inv(degrees_of_freedom_0_measurement)

        
        #TODO these all need to get pickled properly or jsonsed or something so they can be moved over http
        statistic_encrypted = {}
        statistic_encrypted['type_statistic'] = 'anova_repeated_measures'
        statistic_encrypted['degrees_of_freedom_0_sample'] = degrees_of_freedom_0_sample
        statistic_encrypted['degrees_of_freedom_0_measurement'] = degrees_of_freedom_0_measurement
        statistic_encrypted['degrees_of_freedom_1'] = degrees_of_freedom_1
        statistic_encrypted['summed_variance_sample'] = summed_variance_sample
        statistic_encrypted['summed_variance_measurement'] = summed_variance_measurement
        statistic_encrypted['total_variance'] = total_variance
        return statistic_encrypted
    
    def decrypt_statistic(self, algebra:AbstractAlgebra, statistic_encrypted):
        if not statistic_encrypted['type_statistic'] == 'anova_repeated_measures':
            raise Exception('Incorrect statistic')

        degrees_of_freedom_0_sample = statistic_encrypted['degrees_of_freedom_0_sample']
        degrees_of_freedom_0_measurement = statistic_encrypted['degrees_of_freedom_0_measurement']
        degrees_of_freedom_1 = statistic_encrypted['degrees_of_freedom_1']
        summed_variance_sample = statistic_encrypted['summed_variance_sample'] 
        summed_variance_measurement = statistic_encrypted['summed_variance_measurement'] 
        total_variance = statistic_encrypted['total_variance'] 

        #F-transform

        f_statistic_sample = summed_variance_sample / total_variance
        f_statistic_measurement = summed_variance_measurement / total_variance

        return f_statistic_sample, f_statistic_measurement, degrees_of_freedom_0_sample, degrees_of_freedom_0_measurement, degrees_of_freedom_1