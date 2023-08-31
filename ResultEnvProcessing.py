from PropEnv import PropEnv

class ResultEnvProcessing():

    def __init__(self):
        pass

    @staticmethod
    def normalize_resultEnv(resultEnv: PropEnv, n_photons, volume_per_bin, escaped_photons_weight, inplace=True, print_debug=False):
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
        if print_debug:
            print("norm1 sum_of_photon_weight_in_observed_area:", sum_of_photon_weight_in_observed_area)
            print("n_photons:", n_photons)
            print("escaped_photons_weight:", escaped_photons_weight)
        body_pointer = resultEnv.body / (sum_of_photon_weight_in_observed_area * volume_per_bin)
        if inplace:
            return resultEnv
        else:
            return PropEnv(arr=body_pointer)
        
    @staticmethod
    def normalize_resultEnv_2(resultEnv: PropEnv, volume_per_bin, inplace=True, print_debug=False):
        """
        variant with body sum instead of 
        NORMALIZE resultEnv.body VALUES
        Values of resultEnv [photon weight/bin] are normalized by the appropriate volume_per_bin and
        by the value n_photons to yield the absorbed fraction [1/cm^3]
        """
        if inplace:
            body_pointer = resultEnv.body
        else:
            body_pointer = resultEnv.body.copy()
        sum_of_photon_weight_in_observed_area = body_pointer.sum()
        if print_debug:
            print("norm2 sum_of_photon_weight_in_observed_area:", sum_of_photon_weight_in_observed_area)
        body_pointer = resultEnv.body / (sum_of_photon_weight_in_observed_area * volume_per_bin)
        if inplace:
            return resultEnv
        else:
            return PropEnv(arr=body_pointer)
        

    @staticmethod
    def normalize_resultRecords(resultRecords, n_photons, volume_per_bin, escaped_photons_weight, inplace=True, print_debug=False):
        """
        NORMALIZE resultRecords VALUES COLUMN
        Values of resultRecords [photon weight/bin] are normalized by the appropriate volume_per_bin and
        by the value n_photons to yield the absorbed fraction [1/cm^3]
        """
        if inplace:
            resultRecords_pointer = resultRecords
        else:
            resultRecords_pointer = resultRecords.copy()
        sum_of_photon_weight_in_observed_area = n_photons * 1.0 - escaped_photons_weight
        if print_debug:
            print("norm1 sum_of_photon_weight_in_observed_area:", sum_of_photon_weight_in_observed_area)
            print("n_photons:", n_photons)
            print("escaped_photons_weight:", escaped_photons_weight)
        resultRecords_pointer = [col[:4] + [col[4] / (sum_of_photon_weight_in_observed_area * volume_per_bin)] for col in resultRecords_pointer]
        return resultRecords_pointer
    

    @staticmethod
    def normalize_resultRecords_2(resultRecords, volume_per_bin, borders, inplace=True, print_debug=False):
        """
        variant with values sum instead of 
        NORMALIZE resultRecords VALUES COLUMN
        Values of resultRecords [photon weight/bin] are normalized by the appropriate volume_per_bin and
        by the value n_photons to yield the absorbed fraction [1/cm^3]
        """
        if inplace:
            resultRecords_pointer = resultRecords
        else:
            resultRecords_pointer = resultRecords.copy()
        sum_of_photon_weight_in_observed_area = sum([col[4] for col in resultRecords_pointer if ResultEnvProcessing.is_in_borders(col, borders)])
        if print_debug:
            print("norm2 sum_of_photon_weight_in_observed_area:", sum_of_photon_weight_in_observed_area)
        resultRecords_pointer = [col[:4] + [col[4] / (sum_of_photon_weight_in_observed_area * volume_per_bin)] for col in resultRecords_pointer]
        return resultRecords_pointer
    
    @staticmethod
    def is_in_borders(record, borders):
        x, y, z = record[1:4]
        x_in = x >= borders[0] and x <= borders[1]-1
        y_in = y >= borders[2] and y <= borders[3]-1
        z_in = z >= borders[4] and z <= borders[5]-1
        return x_in and y_in and z_in
        