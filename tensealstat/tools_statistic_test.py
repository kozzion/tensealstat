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
    def mean(context, sample):
        return np.mean(sample)


    @staticmethod
    def mean_all(context, list_sample):
        sum_all = ToolsStatisticTest.sum_all(context, list_sample)
        count_all =ToolsStatisticTest.count_all(context, list_sample)
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
        size = len(list_sample[0])
        for sample in list_sample:
            if len(sample) != size:
                raise Exception('Samples should be of equal size')

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
        #FTransform

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

        f_statistic = summed_variance / total_variance
        p_value = f.cdf(f_statistic, degrees_of_freedom_0, degrees_of_freedom_1)
        return f_statistic, p_value


  