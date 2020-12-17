import tenseal as ts


class ToolsContext:

    @staticmethod
    def get_context_default():
        poly_mod_degree = 16384
        coeff_mod_bit_sizes = [60, 40, 40, 40, 40, 40, 60] # for better accuracy
        context = ts.context(ts.SCHEME_TYPE.CKKS, poly_mod_degree, -1, coeff_mod_bit_sizes)
        context.global_scale = 2 ** 40
        context.generate_galois_keys()
        return context

    @staticmethod
    def get_context_poor():
        poly_mod_degree = 8192
        coeff_mod_bit_sizes = [40, 21, 21, 21, 21, 21, 21, 40]
        context = ts.context(ts.SCHEME_TYPE.CKKS, poly_mod_degree, -1, coeff_mod_bit_sizes)
        context.global_scale = 2 ** 21
        context.generate_galois_keys()
        return context
