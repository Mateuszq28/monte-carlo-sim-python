from Sim import Sim
from ByVispy import ByVispy
from Test import Test
from PropSetup import PropSetup
from ResultEnvProcessing import ResultEnvProcessing
from SumProjection import SumProjection
from ChartMaker import ChartMaker
import time
import os


class RunAll():
    def __init__(self):
        pass


    @staticmethod
    def normalize_process(propSetup: PropSetup):
        # normalize output [photon weight / bin] -> absorbed fraction [1/cm^3]
        photon_limits_list = propSetup.lightSource.photon_limits_list
        photon_num = sum(photon_limits_list)
        bins_per_1_cm = propSetup.config["bins_per_1_cm"] # [N/cm]
        volume_per_bin = (1/bins_per_1_cm)**3
        # TEST TO DELETE (inplace = False)
        Test.Test_ResultEnvProcessing.are_2_variants_equal(propSetup.resultEnv, photon_num, volume_per_bin, propSetup.escaped_photons_weight)
        # END OF TEST
        ResultEnvProcessing.normalize_resultEnv(propSetup.resultEnv, photon_num, volume_per_bin, propSetup.escaped_photons_weight, inplace=True)
        # HERE NORMALIZATION INPLACE IS DONE


    @staticmethod
    def run():
        """
        MAIN PHOTON SIMULATION
        """

        # used in every printing and charts
        color_scheme = "threshold"
        color_scheme = "loop"

        sim = Sim()
        vis = ByVispy()

        # SIMULATION
        start_time = time.time()
        sim.start_sim()
        end_time = time.time()
        print("simulation calculation time:", end_time-start_time)

        # NORMALIZATION
        RunAll.normalize_process(sim.propSetup)

        # SHOW CHARTS + MAKE .PNG IMAGES
        ChartMaker.show_all(sim.propSetup, color_scheme)



if __name__ == '__main__':
    RunAll.run()