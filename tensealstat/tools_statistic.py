import math
import tenseal as ts
import copy
from scipy.stats import t


#TODO everying should be jsonable or pickalble
#TODO make sure to handle the public and private keys better

class ToolsStatistic:


    #
    # Primitive section
    #
    @staticmethod
    def encode_scalar(context, scalar):
        return ts.ckks_vector(context, [scalar])

    # as in https://eprint.iacr.org/2019/417.pdf algoritm 1
    # Input: 0 < x < 2, d ∈ N
    # Output: an approximate value of 1/x (refer Lemma 1)
    @staticmethod
    def inv_0t2(context, x, d=7):
        enc_1 = ToolsStatistic.encode_scalar(context, 1.0)
        enc_2 = ToolsStatistic.encode_scalar(context, 2.0)
        a = enc_2 - x
        b = enc_1 - x
        try:
            for _ in range(d):
                b = b * b
                a = a * (enc_1 + b)
        except ValueError: #This might create a attack oppertunity for the crypto
            return a
        return a


    # as in https://eprint.iacr.org/2019/417.pdf algoritm 2
    # Input: 0 ≤ x ≤ 1, d ∈ N
    # Output: an approximate value of √x
    @staticmethod
    def sqrt_0t1(context, x, d=7):
        enc_025 = ToolsStatistic.encode_scalar(context, 0.25)
        enc_05 = ToolsStatistic.encode_scalar(context, 0.5)
        enc_1 = ToolsStatistic.encode_scalar(context, 1.0)
        enc_3 = ToolsStatistic.encode_scalar(context, 3.0)
        
        a = x
        b = x - enc_1
        try:
            for _ in range(d):
                a = a * (enc_1 - (b * enc_05))
                b = b * b * ((b - enc_3) * enc_025)
        except ValueError: #This might create a attack oppertunity for the crypto
            print('ValueError')
            return a
        return a

    @staticmethod
    def abs_0t1(context, x, d=7):
        return ToolsStatistic.sqrt_0t1(context, x * x, d)

    # as in https://eprint.iacr.org/2019/417.pdf algoritm 3
    #Input: a, b ∈ [0, 1), d ∈ N
    #Output: an approximate value of min(a, b) and max(a, b) (refer Theorem 1,2)
    @staticmethod
    def min_max_0t1(context, a, b, d=7):
        enc_05 = ToolsStatistic.encode_scalar(context, 0.5)
        x = (a + b) *enc_05
        y = (a - b) *enc_05
        z = ToolsStatistic.abs_0t1(context, y, d)
        return x - z, x + z

    @staticmethod
    def max_list_0t1(context, list_value_encoded, d=7):
        value_max_encoded = list_value_encoded[0]
        for i in range(1, list_value_encoded.size()):
            _, value_max_encoded = ToolsStatistic.min_max_0t1(context, value_max_encoded, list_value_encoded[i], d)            
        return value_max_encoded

    @staticmethod
    def min_list_0t1(context, list_value_encoded, d=7):
        value_min_encoded = list_value_encoded[0]
        for i in range(1, list_value_encoded.size()):
            value_min_encoded, _ = ToolsStatistic.min_max_0t1(context, value_min_encoded, list_value_encoded[i], d)            
        return value_min_encoded

    # full buble sort 
    @staticmethod
    def sort_list_buble_0t1(context, list_value_encoded, d=7):
        list_value_sorted_encoded = copy.copy(list_value_encoded)
        for i in range(list_value_sorted_encoded.size()):
            for j in range(list_value_sorted_encoded.size() - (i + 1)):
                min_encoded, max_encoded = ToolsStatistic.min_max_0t1(context, list_value_sorted_encoded[j], list_value_sorted_encoded[j + 1], d)
                list_value_sorted_encoded[j] = min_encoded
                list_value_sorted_encoded[j + 1] = max_encoded
        return list_value_sorted_encoded
        

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
        

#
# Test section
#
    
    @staticmethod
    def encode_student_t_independant_equal_variance(context, sample_0_encoded, sample_1_encoded):
        mean_0_encoded = ToolsStatistic.mean(context, sample_0_encoded)
        mean_1_encoded = ToolsStatistic.mean(context, sample_1_encoded)
        variance_encoded = ToolsStatistic.variance_pooled(context, sample_0_encoded, sample_1_encoded)
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



    @staticmethod
    def encode_student_t_repeated_measures(context, sample_0_encoded, sample_1_encoded):
        if sample_0_encoded.size() != sample_1_encoded.size():
            raise Exception('Samples should be of equal size')
        difference_encoded = sample_0_encoded - sample_1_encoded
        mean_difference_encoded = ToolsStatistic.mean(context, difference_encoded)
        variance_encoded = ToolsStatistic.variance(context, difference_encoded)
        variance_rescale = sample_0_encoded.size()
        degrees_of_freedom = sample_0_encoded.size() - 1
        
        #TODO these all need to get pickled properly or jsonsed or something so they can be moved over http
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
        t_statistic = mean_difference / (math.sqrt(variance) / math.sqrt(variance_rescale))
        p_value = t.cdf(t_statistic, degrees_of_freedom)
        return t_statistic, p_value



    #     # d / (sqt v / sqr n)
    # @staticmethod
    # def zstatistic(context, enc_data):
    #     enc_mean = ToolsStatistic.mean(context, enc_data)
    #     scale = ts.ckks_vector(context, [1 / (enc_data.size() - 1)])
    #     return (enc_data - enc_mean).dot(enc_data - enc_mean) * scale

