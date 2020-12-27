import math
import numpy as np
import tenseal as ts
import copy
from scipy.stats import t
from scipy.stats import f

#TODO everying should be jsonable or pickalble
#TODO make sure to handle the public and private keys better

class ToolsStatisticTest:

    #
    # Primitive section
    #
    @staticmethod
    def encode_scalar(context, scalar):
        return scalar

    @staticmethod
    def encode_scalar_inv(context, scalar):
        return 1/scalar

    @staticmethod
    def inv_0t2(context, x, d=7):
        return 1/x

    @staticmethod
    def sqrt(context, x):
        return math.sqrt(x)

    @staticmethod
    def sqr(context, x):
        return x * x

    @staticmethod
    def count_all(context, list_sample):
        count = 0 
        for sample in list_sample:
            count += len(sample)
        return count
    
    @staticmethod
    def sum(context, sample):
        return np.sum(sample)

    @staticmethod
    def sum_all(context, list_sample):
        all = 0
        for sample in list_sample:
            all += np.sum(sample)
        return all

    @staticmethod
    def sum_sample(context, list_sample):
        list_sum_sample = []
        for sample in list_sample:
            list_sum_sample.append(ToolsStatisticTest.sum(context, sample))
        return list_sum_sample


    @staticmethod
    def sum_measurement(context, list_sample):
        list_sum_measurement = []
        for index_measurement in range(len(list_sample[0])):
            list_sum_measurement.append(ToolsStatisticTest.encode_scalar(context, 0))
            for sample in list_sample:
                list_sum_measurement[index_measurement] += sample[index_measurement]
        return list_sum_measurement

    @staticmethod
    def sum_squared_all(context, list_sample):
        sum_squared_all = ToolsStatisticTest.encode_scalar(context, 0)
        for sample in list_sample:
            for measurement in sample:
                sum_squared_all += ToolsStatisticTest.sqr(context, measurement)
        return sum_squared_all

    @staticmethod
    def mean(context, sample):
        return np.mean(sample)


    @staticmethod
    def mean_all(context, list_sample):
        return ToolsStatisticTest.sum_all(context, list_sample) / ToolsStatisticTest.count_all(context, list_sample)

    @staticmethod
    def variance(context, sample):
        return np.var(sample)

    @staticmethod
    def variance_pooled(context, sample_0_encoded, sample_1_encoded):
        mean_0_encoded = ToolsStatisticTest.mean(context, sample_0_encoded) #TODO these means can be avoided
        mean_1_encoded = ToolsStatisticTest.mean(context, sample_1_encoded)
        variance_0_encoded = (sample_0_encoded - mean_0_encoded).dot(sample_0_encoded - mean_0_encoded)
        variance_1_encoded = (sample_1_encoded - mean_1_encoded).dot(sample_1_encoded - mean_1_encoded)
        scale = ts.ckks_vector(context, [1 / (sample_0_encoded.size() + sample_1_encoded.size() - 2)])
        return (variance_0_encoded + variance_1_encoded) * scale
        

#
# Test section
#

    #
    # student_t_equal varriance
    #

    
    @staticmethod
    def encode_student_t_independant_equal_variance(context, sample_0_encoded, sample_1_encoded):
        mean_0_encoded = ToolsStatisticTest.mean(context, sample_0_encoded)
        mean_1_encoded = ToolsStatisticTest.mean(context, sample_1_encoded)
        variance_encoded = ToolsStatisticTest.variance_pooled(context, sample_0_encoded, sample_1_encoded)
        variance_rescale =  (1.0 / sample_0_encoded.size()) + (1.0 / sample_1_encoded.size())
        degrees_of_freedom = (sample_0_encoded.size() + sample_1_encoded.size() - 2)

        #TODO these all need to get pickled properly or jsonsed or something so they can be moved over http
        statistic_encoded = {}
        statistic_encoded['type_statistic'] = 'student_t_independant_equal_variance'
        statistic_encoded['mean_difference_encoded'] = mean_0_encoded - mean_1_encoded
        statistic_encoded['variance_encoded'] = variance_encoded
        statistic_encoded['variance_rescale'] = variance_rescale
        statistic_encoded['degrees_of_freedom'] = degrees_of_freedom
        return statistic_encoded
    
    @staticmethod
    def decode_student_t_independant_equal_variance(context, statistic_encoded):
        if not statistic_encoded['type_statistic'] == 'student_t_independant_equal_variance':
            raise Exception('Incorrect statistic')
        mean_difference = statistic_encoded['mean_difference_encoded'].decrypt()[0]
        variance = statistic_encoded['variance_encoded'].decrypt()[0]
        variance_rescale = statistic_encoded['variance_rescale']
        degrees_of_freedom = statistic_encoded['degrees_of_freedom']
        t_statistic = mean_difference / (math.sqrt(variance) / math.sqrt(variance_rescale))
        p_value = t.cdf(t_statistic, degrees_of_freedom)
        return t_statistic, p_value

    #
    # student_t_repeated_measures
    #

    @staticmethod
    def encode_student_t_repeated_measures(context, sample_0, sample_1):
        if len(sample_0) != len(sample_1):
            raise Exception('Samples should be of equal size')
        difference = sample_0 - sample_1
        mean_difference = ToolsStatisticTest.mean(context, difference)
        variance = ToolsStatisticTest.variance(context, difference)
        variance_rescale = len(sample_0)
        degrees_of_freedom = len(sample_0) - 1
        
        #TODO these all need to get pickled properly or jsonsed or something so they can be moved over http
        statistic_encoded = {}
        statistic_encoded['type_statistic'] = 'student_t_repeated_measures'
        statistic_encoded['mean_difference'] = mean_difference
        statistic_encoded['variance'] = variance   
        statistic_encoded['variance_rescale'] = variance_rescale
        statistic_encoded['degrees_of_freedom'] = degrees_of_freedom
        return statistic_encoded
    
    @staticmethod
    def decode_student_t_repeated_measures(context, statistic_encoded):
        if not statistic_encoded['type_statistic'] == 'student_t_repeated_measures':
            raise Exception('Incorrect statistic')
        
        mean_difference = statistic_encoded['mean_difference']
        variance = statistic_encoded['variance']
        variance_rescale = statistic_encoded['variance_rescale']
        degrees_of_freedom = statistic_encoded['degrees_of_freedom']

        t_statistic = mean_difference / (math.sqrt(variance) / math.sqrt(variance_rescale))
        p_value = t.cdf(t_statistic, degrees_of_freedom)
        return t_statistic, p_value

    @staticmethod
    def encode_anova_one_way(context, list_sample):
        count_sample = len(list_sample)
        count_total = ToolsStatisticTest.count_all(context, list_sample)
        mean_total = ToolsStatisticTest.mean_all(context, list_sample)
        
        list_sample_mean = []
        for sample in list_sample:
            list_sample_mean.append(ToolsStatisticTest.mean(context, sample))
    
        sstr = 0.0
        for sample, mean_sample in zip(list_sample, list_sample_mean):
            sstr += len(sample) * ToolsStatisticTest.sqr(context, mean_sample - mean_total)
        
        sse = 0.0
        for sample, sample_mean in zip(list_sample, list_sample_mean):
            for measurement in sample:
                sse += ToolsStatisticTest.sqr(context, measurement - sample_mean)

        degrees_of_freedom_0 = (count_sample - 1.0)
        degrees_of_freedom_1 = (count_total - count_sample)
        summed_variance = sstr / degrees_of_freedom_0
        total_variance = sse / degrees_of_freedom_1


        #TODO these all need to get pickled properly or jsonsed or something so they can be moved over http
        statistic_encoded = {}
        statistic_encoded['type_statistic'] = 'anova_one_way'
        statistic_encoded['degrees_of_freedom_0'] = degrees_of_freedom_0
        statistic_encoded['degrees_of_freedom_1'] = degrees_of_freedom_1
        statistic_encoded['summed_variance'] = summed_variance
        statistic_encoded['total_variance'] = total_variance
        return statistic_encoded
    
    @staticmethod
    def decode_anova_one_way(context, statistic_encoded):
        if not statistic_encoded['type_statistic'] == 'anova_one_way':
            raise Exception('Incorrect statistic')

        degrees_of_freedom_0 = statistic_encoded['degrees_of_freedom_0']
        degrees_of_freedom_1 = statistic_encoded['degrees_of_freedom_1']
        summed_variance = statistic_encoded['summed_variance'] 
        total_variance = statistic_encoded['total_variance'] 

        #F-transform

        f_statistic = summed_variance / total_variance
        p_value = f.cdf(f_statistic, degrees_of_freedom_0, degrees_of_freedom_1)
        return f_statistic, p_value


  

  
    @staticmethod
    def encode_anova_repeated_measures(context, list_sample):
        count_sample = len(list_sample)
        count_measurement = len(list_sample[0])
        for sample in list_sample:
            if len(sample) != count_measurement:
                raise Exception('Samples should be of equal size')

        count_total = count_sample * count_measurement
        total_mean = ToolsStatisticTest.mean_all(context, list_sample)
        sum_squared_all = ToolsStatisticTest.sum_squared_all(context, list_sample)
        list_sum_sample = ToolsStatisticTest.sum_sample(context, list_sample)
        list_sum_measurement = ToolsStatisticTest.sum_measurement(context, list_sample)

        # compute C
        c = ToolsStatisticTest.sqr(context, total_mean * ToolsStatisticTest.encode_scalar(context, count_total))
        c *= ToolsStatisticTest.encode_scalar_inv(context, count_total)

        sstot = sum_squared_all - c

        ssb = 0
        for sum_measurement in list_sum_measurement:
            ssb += ToolsStatisticTest.sqr(context, sum_measurement) 
        ssb *= ToolsStatisticTest.encode_scalar_inv(context, count_sample)
        ssb -= c

        sstr = 0.0
        for sum_sample in list_sum_sample:
            sstr += ToolsStatisticTest.sqr(context, sum_sample)
        sstr *= ToolsStatisticTest.encode_scalar_inv(context, count_measurement)
        sstr -= c

        sse = sstot - ssb - sstr

        degrees_of_freedom_0_sample      = (count_sample - 1.0)
        degrees_of_freedom_0_measurement = (count_measurement - 1.0)
        degrees_of_freedom_1             = degrees_of_freedom_0_sample * degrees_of_freedom_0_measurement;

        total_variance = sse * ToolsStatisticTest.encode_scalar_inv(context, degrees_of_freedom_1)
        summed_variance_sample =  sstr * ToolsStatisticTest.encode_scalar_inv(context, degrees_of_freedom_0_sample)
        summed_variance_measurement = ssb * ToolsStatisticTest.encode_scalar_inv(context, degrees_of_freedom_0_measurement)

        
        #TODO these all need to get pickled properly or jsonsed or something so they can be moved over http
        statistic_encoded = {}
        statistic_encoded['type_statistic'] = 'anova_repeated_measures'
        statistic_encoded['degrees_of_freedom_0_sample'] = degrees_of_freedom_0_sample
        statistic_encoded['degrees_of_freedom_0_measurement'] = degrees_of_freedom_0_measurement
        statistic_encoded['degrees_of_freedom_1'] = degrees_of_freedom_1
        statistic_encoded['summed_variance_sample'] = summed_variance_sample
        statistic_encoded['summed_variance_measurement'] = summed_variance_measurement
        statistic_encoded['total_variance'] = total_variance
        return statistic_encoded
    
    @staticmethod
    def decode_anova_repeated_measures(context, statistic_encoded):
        if not statistic_encoded['type_statistic'] == 'anova_repeated_measures':
            raise Exception('Incorrect statistic')

        degrees_of_freedom_0_sample = statistic_encoded['degrees_of_freedom_0_sample']
        degrees_of_freedom_0_measurement = statistic_encoded['degrees_of_freedom_0_measurement']
        degrees_of_freedom_1 = statistic_encoded['degrees_of_freedom_1']
        summed_variance_sample = statistic_encoded['summed_variance_sample'] 
        summed_variance_measurement = statistic_encoded['summed_variance_measurement'] 
        total_variance = statistic_encoded['total_variance'] 

        #F-transform

        f_statistic_sample = summed_variance_sample / total_variance
        f_statistic_measurement = summed_variance_measurement / total_variance
        p_value_sample = f.cdf(f_statistic_sample, degrees_of_freedom_0_sample, degrees_of_freedom_1)
        p_value_measurement = f.cdf(f_statistic_measurement, degrees_of_freedom_0_measurement, degrees_of_freedom_1)
        return f_statistic_sample, f_statistic_measurement, p_value_sample, p_value_measurement