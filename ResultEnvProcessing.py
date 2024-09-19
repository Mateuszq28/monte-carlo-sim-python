from PropSetup import PropSetup
from PropEnv import PropEnv
import numpy as np

class ResultEnvProcessing():

    def __init__(self):
        pass

    @staticmethod
    def normalize_resultEnv(propSetup: PropSetup, n_photons, volume_per_bin, escaped_photons_weight, inplace=True, print_debug=False):
        """
        NORMALIZE resultEnv.body VALUES
        Values of resultEnv [photon weight/bin] are normalized by the appropriate volume_per_bin,
        n_photons and mu_a to yield Relative fluence rate [$\frac{1}{cm^2}$]=[1/cm^2]
        normalization in *mc321.c*:
        Fsph = Csph[ir]/Nphotons/shellvolume/mua;
        [1/cm2]
        """
        resultEnv = propSetup.resultEnv
        if inplace:
            body_pointer = resultEnv.body
        else:
            body_pointer = resultEnv.body.copy()
        sum_of_photon_weight_in_observed_area = n_photons * 1.0
        if print_debug:
            print("norm1 sum_of_photon_weight_in_observed_area:", sum_of_photon_weight_in_observed_area)
            print("n_photons:", n_photons)
            print("escaped_photons_weight:", escaped_photons_weight)
        get_mu_a_element_wise = np.vectorize(propSetup.propEnv.get_mu_a)
        arr_of_mu_a = get_mu_a_element_wise(propSetup.propEnv)
        div = arr_of_mu_a * sum_of_photon_weight_in_observed_area * volume_per_bin
        body_pointer = np.divide(resultEnv.body, div)
        if inplace:
            resultEnv.body = body_pointer
            return resultEnv
        else:
            return PropEnv(arr=body_pointer)
        
    @staticmethod
    def normalize_resultEnv_2(propSetup: PropSetup, volume_per_bin, escaped_photons_weight, inplace=True, print_debug=False):
        """
        variant with body sum instead of 
        NORMALIZE resultEnv.body VALUES
        Values of resultEnv [photon weight/bin] are normalized by the appropriate volume_per_bin, n_photons and mu_a to yield Relative fluence rate [$\frac{1}{cm^2}$]=[1/cm^2]
        normalization in *mc321.c*:
        Fsph = Csph[ir]/Nphotons/shellvolume/mua;
        [1/cm2]
        """
        resultEnv = propSetup.resultEnv
        if inplace:
            body_pointer = resultEnv.body
        else:
            body_pointer = resultEnv.body.copy()
        sum_of_photon_weight_in_observed_area = body_pointer.sum() + escaped_photons_weight
        if print_debug:
            print("norm2 sum_of_photon_weight_in_observed_area:", sum_of_photon_weight_in_observed_area)
        get_mu_a_element_wise = np.vectorize(propSetup.propEnv.get_mu_a)
        arr_of_mu_a = get_mu_a_element_wise(propSetup.propEnv)
        div = arr_of_mu_a * sum_of_photon_weight_in_observed_area * volume_per_bin
        body_pointer = np.divide(resultEnv.body, div)
        if inplace:
            resultEnv.body = body_pointer
            return resultEnv
        else:
            return PropEnv(arr=body_pointer)
        

    @staticmethod
    def normalize_resultRecords(propSetup: PropSetup, n_photons, volume_per_bin, escaped_photons_weight, inplace=True, print_debug=False):
        """
        NORMALIZE resultRecords VALUES COLUMN
        Values of resultRecords [photon weight/bin] are normalized by the appropriate volume_per_bin,
        n_photons and mu_a to yield Relative fluence rate [$\frac{1}{cm^2}$]=[1/cm^2]
        normalization in *mc321.c*:
        Fsph = Csph[ir]/Nphotons/shellvolume/mua;
        [1/cm2]
        """
        resultRecords = propSetup.resultRecords
        if not inplace:
            resultRecords = resultRecords.copy()
        sum_of_photon_weight_in_observed_area = n_photons * 1.0
        if print_debug:
            print("norm1 sum_of_photon_weight_in_observed_area:", sum_of_photon_weight_in_observed_area)
            print("n_photons:", n_photons)
            print("escaped_photons_weight:", escaped_photons_weight)
        resultRecords = [col[:4] + [col[4] / (sum_of_photon_weight_in_observed_area * volume_per_bin * propSetup.propEnv.get_mu_a(col[1:4]))] for col in resultRecords]
        return resultRecords
    

    @staticmethod
    def normalize_resultRecords_2(propSetup: PropSetup, volume_per_bin, escaped_photons_weight, borders, inplace=True, print_debug=False):
        """
        variant with values sum instead of 
        NORMALIZE resultRecords VALUES COLUMN
        Values of resultRecords [photon weight/bin] are normalized by the appropriate volume_per_bin and
        by the value n_photons to yield Relative fluence rate [$\frac{1}{cm^2}$]=[1/cm^2]
        normalization in *mc321.c*:
        Fsph = Csph[ir]/Nphotons/shellvolume/mua;
        [1/cm2]
        """
        resultRecords = propSetup.resultRecords
        if not inplace:
            resultRecords = resultRecords.copy()
        sum_of_photon_weight_in_observed_area = sum([col[4] for col in resultRecords if ResultEnvProcessing.is_in_borders(col, borders)]) + escaped_photons_weight
        if print_debug:
            print("norm2 sum_of_photon_weight_in_observed_area:", sum_of_photon_weight_in_observed_area)
        resultRecords = [col[:4] + [col[4] / (sum_of_photon_weight_in_observed_area * volume_per_bin * propSetup.propEnv.get_mu_a(col[1:4]))] for col in resultRecords]
        return resultRecords
    
    @staticmethod
    def is_in_borders(record, borders):
        xyz = record[1:4]
        x, y, z = PropEnv.round_xyz(xyz)
        x_in = x >= borders[0] and x <= borders[1]-1
        y_in = y >= borders[2] and y <= borders[3]-1
        z_in = z >= borders[4] and z <= borders[5]-1
        return x_in and y_in and z_in
        