from Sim import Sim
from ByVispy import ByVispy
from Test import Test
from PropSetup import PropSetup
from ResultEnvProcessing import ResultEnvProcessing
from SumProjection import SumProjection
from ChartMaker import ChartMaker
from tabulate import tabulate
import time
import os


class RunAll():
    def __init__(self):
        pass


    @staticmethod
    def normalize_process(propSetup: PropSetup):
        # NORMALIZATION OF resultEnv
        # normalize output [photon weight / bin] -> absorbed fraction [1/cm^3]
        photon_limits_list = propSetup.lightSource.photon_limits_list
        photon_num = sum(photon_limits_list)
        bins_per_1_cm = propSetup.config["bins_per_1_cm"] # [N/cm]
        volume_per_bin = (1/bins_per_1_cm)**3

        if propSetup.config["flag_save_result_env"]:
            # TEST TO DELETE (inplace = False)
            Test.Test_ResultEnvProcessing.are_2_variants_equal_resultEnv(propSetup.resultEnv, photon_num, volume_per_bin, propSetup.escaped_photons_weight)
            # END OF TEST

            ResultEnvProcessing.normalize_resultEnv(propSetup.resultEnv, photon_num, volume_per_bin, propSetup.escaped_photons_weight, inplace=True)
            # HERE NORMALIZATION ON propSetup.resultEnv INPLACE IS DONE
            # NORMALIZATION OF resultRecords

        if propSetup.config["flag_seve_result_records"]:
            # TEST TO DELETE (inplace = False)
            sh = propSetup.resultShape
            borders = [0, sh[0], 0, sh[1], 0, sh[2]]
            Test.Test_ResultEnvProcessing.are_2_variants_equal_resultRecords(propSetup.resultRecords, photon_num, volume_per_bin, borders, propSetup.escaped_photons_weight)
            # END OF TEST

            ResultEnvProcessing.normalize_resultRecords(propSetup.resultRecords, photon_num, volume_per_bin, propSetup.escaped_photons_weight, inplace=True, print_debug=False)
            # HERE NORMALIZATION ON propSetup.resultRecords INPLACE IS DONE


    @staticmethod
    def run():
        """
        MAIN PHOTON SIMULATION
        """
        # if true, just load last saved results 
        LOAD_INSTEAD_OF_SIM = True
        LOAD_INSTEAD_OF_SIM = False

        # used in every printing and charts
        color_scheme_list = ["threshold", "loop", "solid", "photonwise", "random", "rainbow", "min-max", "median", "trans-normal", "logarithmic", "heatmap min-max", "heatmap median", "heatmap trans-normal", "heatmap logarithmic"]
        do_connect_lines_list = [True, False]
        do_connect_lines_list = [True]
        do_connect_lines_list = [False]

        # SIMULATION
        sim = Sim(load_last_dump=LOAD_INSTEAD_OF_SIM)
        if LOAD_INSTEAD_OF_SIM:
            result_propSetup = sim.propSetup
            print("simulation dump loaded")
        else:
            result_propSetup = sim.start_sim()
            print("simulation calculation time:", sim.simulation_calculation_time)
        
        # return
    
        # NORMALIZATION
        RunAll.normalize_process(result_propSetup)

        # SHOW CHARTS + MAKE .PNG IMAGES
        take_cs = color_scheme_list
        take_cs.remove("photonwise")
        take_cs = ["min-max", "heatmap min-max", "heatmap trans-normal"]
        take_cs = ["heatmap trans-normal"]
        print()
        for do_cl in do_connect_lines_list:
            for i in range(len(take_cs)):
                color_scheme = take_cs[i]
                print("({}) Run ChartMaker.show_all, color_scheme = {}".format(i, color_scheme))
                ChartMaker.show_all(result_propSetup, color_scheme, do_cl, color_points_by_root=True, color_arrows_by_root=True, do_triangled_planes=False, draw_planes_from_material_stack=True)


if __name__ == '__main__':
    RunAll.run()