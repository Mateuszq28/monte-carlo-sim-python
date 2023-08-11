from PropEnv import PropEnv

class ResultEnvProcessing():

    def __init__(self):
        pass

    @staticmethod
    def normalize_resultEnv(resultEnv: PropEnv, n_photons, volume_per_bin, escaped_photons_weight, inplace=True):
        """
        NORMALIZE resultEnv.body VALUES
        Values of resultEnv [photon weight/bin] are normalized by the appropriate volume_per_bin and
        by the value n_photons to yield the absorbed fraction [1/cm^3]
        """
        if inplace:
            body_pointer = resultEnv.body
        else:
            body_pointer = resultEnv.body.copy()
        sum_of_photon_weight_in_observed_area = n_photons * 1.0 - escaped_photons_weight
        body_pointer = resultEnv.body / (sum_of_photon_weight_in_observed_area * volume_per_bin)
        if inplace:
            return resultEnv
        else:
            return PropEnv(arr=body_pointer)