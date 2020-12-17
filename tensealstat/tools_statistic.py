import math
import tenseal as ts

from scipy.stats import t


#TODO everying should be jsonable or pickalble
#TODO make sure to handle the public and private keys better

class ToolsStatistic:

    @staticmethod
    def sum(context, sample_encoded):
        ones_encoded = ts.ckks_vector(context, [1] * sample_encoded.size())
        return sample_encoded.dot(ones_encoded)
    
    @staticmethod
    def mean(context, sample_encoded):
        scale = ts.ckks_vector(context, [1 / sample_encoded.size()])
        return ToolsStatistic.sum(context, sample_encoded) * scale

    @staticmethod
    def variance(context, sample_encoded):
        mean_encoded = ToolsStatistic.mean(context, sample_encoded)
        scale = ts.ckks_vector(context, [1 / (sample_encoded.size() - 1)])
        return (sample_encoded - mean_encoded).dot(sample_encoded - mean_encoded) * scale

    @staticmethod
    def variance_pooled(context, sample_0_encoded, sample_1_encoded):
        mean_0_encoded = ToolsStatistic.mean(context, sample_0_encoded) #TODO these means can be avoided
        mean_1_encoded = ToolsStatistic.mean(context, sample_1_encoded)
        variance_0_encoded = (sample_0_encoded - mean_0_encoded).dot(sample_0_encoded - mean_0_encoded)
        variance_1_encoded = (sample_1_encoded - mean_1_encoded).dot(sample_1_encoded - mean_1_encoded)
        scale = ts.ckks_vector(context, [1 / (sample_0_encoded.size() + sample_1_encoded.size() - 2)])
        return (variance_0_encoded + variance_1_encoded) * scale
        


    
    @staticmethod
    def encode_student_t_independant_equal_variance(context, sample_0_encoded, sample_1_encoded):
        mean_0_encoded = ToolsStatistic.mean(context, sample_0_encoded)
        mean_1_encoded = ToolsStatistic.mean(context, sample_1_encoded)
        variance_encoded = ToolsStatistic.variance_pooled(context, sample_0_encoded, sample_1_encoded)
        variance_rescale =  (1.0 / sample_0_encoded.size()) + (1.0 / sample_1_encoded.size())
        degrees_of_freedom = (sample_0_encoded.size() + sample_1_encoded.size() - 2)
        #TODO these all need to get pickled properly or jsonsed or something
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
        return p_value, t_statistic



    @staticmethod
    def encode_student_t_repeated_measures(context, sample_0_encoded, sample_1_encoded):
        if sample_0_encoded.size() != sample_1_encoded.size():
            raise Exception('Samples should be of equal size')
        difference_encoded = sample_0_encoded - sample_1_encoded
        mean_difference_encoded = ToolsStatistic.mean(context, difference_encoded)
        variance_encoded = ToolsStatistic.variance(context, difference_encoded)
        variance_rescale = sample_0_encoded.size()
        degrees_of_freedom = sample_0_encoded.size() - 1
        
        #TODO these all need to get pickled properly or jsonsed or something
        statistic_encoded = {}
        statistic_encoded['type_statistic'] = 'student_t_repeated_measures'
        statistic_encoded['mean_difference_encoded'] = mean_difference_encoded
        statistic_encoded['variance_encoded'] = variance_encoded   
        statistic_encoded['variance_rescale'] = variance_rescale
        statistic_encoded['degrees_of_freedom'] = degrees_of_freedom
        return statistic_encoded
    
    @staticmethod
    def decode_student_t_repeated_measures(context, statistic_encoded):
        if not statistic_encoded['type_statistic'] == 'student_t_repeated_measures':
            raise Exception('Incorrect statistic')
        mean_difference = statistic_encoded['mean_difference_encoded'].decrypt()[0]
        variance = statistic_encoded['variance_encoded'].decrypt()[0]
        variance_rescale = statistic_encoded['variance_rescale']
        degrees_of_freedom = statistic_encoded['degrees_of_freedom']
        print(mean_difference)
        print(variance)
        print(variance_rescale)
        t_statistic = mean_difference / (math.sqrt(variance) / math.sqrt(variance_rescale))
        p_value = t.cdf(t_statistic, degrees_of_freedom)
        return p_value, t_statistic



    #     # d / (sqt v / sqr n)
    # @staticmethod
    # def zstatistic(context, enc_data):
    #     enc_mean = ToolsStatistic.mean(context, enc_data)
    #     scale = ts.ckks_vector(context, [1 / (enc_data.size() - 1)])
    #     return (enc_data - enc_mean).dot(enc_data - enc_mean) * scale

