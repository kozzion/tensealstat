    
import math
from scipy.stats import f

class AnovaOneWay(object):

    @staticmethod
    def encode_statistic(algebra, list_sample):
        count_sample = len(list_sample)
        count_total = algebra.count_all(list_sample)
        mean_total = algebra.mean_all(list_sample)
        
        list_sample_mean = []
        for sample in list_sample:
            list_sample_mean.append(algebra.mean(sample))
    
        sstr = algebra.encode_scalar(0.0)
        for sample, mean_sample in zip(list_sample, list_sample_mean):
            sstr += algebra.size_vector(sample) * algebra.sqr(mean_sample - mean_total)
        
        sse = algebra.encode_scalar(0.0)
        for sample, sample_mean in zip(list_sample, list_sample_mean):
            sse += (sample - sample_mean).dot(sample - sample_mean)

        degrees_of_freedom_0 = (count_sample - 1.0)
        degrees_of_freedom_1 = (count_total - count_sample)
        summed_variance = sstr  * algebra.encode_scalar_inv(degrees_of_freedom_0)
        total_variance = sse * algebra.encode_scalar_inv(degrees_of_freedom_1)


        #TODO these all need to get pickled properly or jsonsed or something so they can be moved over http
        statistic_encoded = {}
        statistic_encoded['type_statistic'] = 'anova_one_way'
        statistic_encoded['degrees_of_freedom_0'] = degrees_of_freedom_0
        statistic_encoded['degrees_of_freedom_1'] = degrees_of_freedom_1
        statistic_encoded['summed_variance'] = summed_variance
        statistic_encoded['total_variance'] = total_variance
        return statistic_encoded
    
    @staticmethod
    def decode_statistic(algebra, statistic_encoded):
        if not statistic_encoded['type_statistic'] == 'anova_one_way':
            raise Exception('Incorrect statistic')

        degrees_of_freedom_0 = statistic_encoded['degrees_of_freedom_0']
        degrees_of_freedom_1 = statistic_encoded['degrees_of_freedom_1']
        summed_variance = algebra.decode_scalar(statistic_encoded['summed_variance'])
        total_variance = algebra.decode_scalar(statistic_encoded['total_variance'])

        #F-transform
        f_statistic = summed_variance / total_variance
        p_value = f.cdf(f_statistic, degrees_of_freedom_0, degrees_of_freedom_1)
        return f_statistic, p_value
