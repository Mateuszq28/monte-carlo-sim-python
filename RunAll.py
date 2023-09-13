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

        # TEST TO DELETE (inplace = False)
        Test.Test_ResultEnvProcessing.are_2_variants_equal_resultEnv(propSetup.resultEnv, photon_num, volume_per_bin, propSetup.escaped_photons_weight)
        # END OF TEST

        ResultEnvProcessing.normalize_resultEnv(propSetup.resultEnv, photon_num, volume_per_bin, propSetup.escaped_photons_weight, inplace=True)
        # HERE NORMALIZATION ON propSetup.resultEnv INPLACE IS DONE
        # NORMALIZATION OF resultRecords

        # TEST TO DELETE (inplace = False)
        sh = propSetup.resultEnv.shape
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

        # used in every printing and charts
        color_scheme = "threshold"
        color_scheme = "loop"
        color_scheme = "random"
        color_scheme = "rainbow"
        color_scheme = "solid"
        color_scheme = "min-max"
        color_scheme = "median"
        color_scheme = "trans-normal"
        color_scheme = "logarithmic"
        color_scheme = "heatmap trans-normal"
        do_connect_lines = True
        do_connect_lines = False

        sim = Sim()
        vis = ByVispy()

        # SIMULATION
        start_time = time.time()
        sim.start_sim()
        end_time = time.time()
        print("simulation calculation time:", end_time-start_time)
        
        # return
    
        # NORMALIZATION
        RunAll.normalize_process(sim.propSetup)

        # SHOW CHARTS + MAKE .PNG IMAGES
        ChartMaker.show_all(sim.propSetup, color_scheme, do_connect_lines, color_points_by_root=True, color_arrows_by_root=True, do_triangled_planes=True)



if __name__ == '__main__':
    RunAll.run()