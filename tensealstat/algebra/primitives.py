import tenseal as ts

class Primitives:


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
        

