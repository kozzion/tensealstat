import math
from tensealstat.algebra.abstract_algebra import AbstractAlgebra
from tensealstat.test.test_assertion import TestAssertion

class Levene(object):

    @staticmethod
    def list_test_assertion_asumption():
        return [
            TestAssertion.MeasurementsIndependant, 
            TestAssertion.SamplesDrawnFromNormalDistribution]

    @staticmethod
    def list_test_assertion_0_hypothesys():
        return [
            TestAssertion.SamplesHaveEqualVariances]

    # TODO equal to one way anova?
    # TODO check against
    # TODO implement 3 mean variants
    # http://www.itl.nist.gov/div898/handbook/eda/section3/eda35a.htm

    @staticmethod
    def encode_statistic(algebra:AbstractAlgebra, list_sample):

        total_count = algebra.count_all(list_sample)
        total_mean = algebra.mean_all(list_sample)
        
        list_mean_sample = algebra.mean_sample(list_sample)

        summed_varriance = algebra.encode_scalar(0)       
        for sample, mean_sample in zip(list_sample, list_mean_sample):
            summed_varriance += algebra.encode_scalar(algebra.size_vector(sample)) * algebra.sqr(mean_sample - total_mean);
    
        total_variance = algebra.encode_scalar(0)
        for sample, mean_sample in zip(list_sample, list_mean_sample):
            total_variance += (sample - mean_sample).dot(sample - mean_sample)

        degrees_of_freedom_0 = len(list_sample) - 1
        degrees_of_freedom_1 = total_count - len(list_sample)


        f_statistic = (degrees_of_freedom_1 * summed_varriance) / (degrees_of_freedom_0 * total_variance);
        p_value = f.cdf(f_statistic, degrees_of_freedom_0, degrees_of_freedom_1)
        return f_statistic, p_value