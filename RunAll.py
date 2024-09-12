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
        # normalize output [photon weight / bin] -> Relative fluence rate [1/cm^2]
        photon_limits_list = propSetup.lightSource.photon_limits_list
        photon_num = sum(photon_limits_list)
        bins_per_1_cm = propSetup.config["bins_per_1_cm"] # [N/cm]
        volume_per_bin = (1/bins_per_1_cm)**3

        if propSetup.config["flag_save_result_env"]:
            # TEST TO DELETE (inplace = False)
            Test.Test_ResultEnvProcessing.are_2_variants_equal_resultEnv(propSetup, photon_num, volume_per_bin, propSetup.escaped_photons_weight)
            # END OF TEST

            propSetup.resultEnv = ResultEnvProcessing.normalize_resultEnv(propSetup, photon_num, volume_per_bin, propSetup.escaped_photons_weight, inplace=True)
            # HERE NORMALIZATION ON propSetup.resultEnv INPLACE IS DONE
            # NORMALIZATION OF resultRecords

        if propSetup.config["flag_seve_result_records"]:
            # TEST TO DELETE (inplace = False)
            sh = propSetup.resultShape
            borders = [0, sh[0], 0, sh[1], 0, sh[2]]
            Test.Test_ResultEnvProcessing.are_2_variants_equal_resultRecords(propSetup, photon_num, volume_per_bin, borders, propSetup.escaped_photons_weight)
            # END OF TEST

            propSetup.resultRecords = ResultEnvProcessing.normalize_resultRecords(propSetup, photon_num, volume_per_bin, propSetup.escaped_photons_weight, inplace=True, print_debug=False)
            # HERE NORMALIZATION ON propSetup.resultRecords INPLACE IS DONE

        return propSetup


    @staticmethod
    def run():
        """
        MAIN PHOTON SIMULATION
        """
        # check list
        # - LOAD_INSTEAD_OF_SIM
        # - USE_TRIANGLED_PLANES_FROM_FILE
        # - ["heatmap trans-normal", "heatmap min-max"]
        # - do_connect_lines_list = [False]
        # - photon limit in make
        # - make env
        # - save result records
        # - flag_use_propenv_on_formulas

        # if true, just load last saved results
        LOAD_INSTEAD_OF_SIM = True
        LOAD_INSTEAD_OF_SIM = False



        # if False, new traingled planes to show in ByVispy will be calculated using data from propEnv.body array
        USE_TRIANGLED_PLANES_FROM_FILE = False
        USE_TRIANGLED_PLANES_FROM_FILE = True



        # SIMULATION
        sim = Sim(load_last_dump=LOAD_INSTEAD_OF_SIM)
        if LOAD_INSTEAD_OF_SIM:
            result_propSetup = sim.propSetup
            print("simulation dump loaded")
        else:
            result_propSetup = sim.start_sim()
            print("simulation calculation time:", sim.simulation_calculation_time)
            print("boundary check calculation time:", sim.boundary_check_calculation_time)
        


        # return
    


        # NORMALIZATION
        result_propSetup = RunAll.normalize_process(result_propSetup)



        # used in every print .png and charts
        color_scheme_list = ["threshold", "loop", "solid", "photonwise", "random", "rainbow", "min-max", "median", "trans-normal", "logarithmic", "heatmap min-max", "heatmap median", "heatmap trans-normal", "heatmap logarithmic"]
        take_cs = color_scheme_list
        take_cs.remove("photonwise")
        take_cs = ["min-max", "heatmap min-max", "heatmap trans-normal"]
        take_cs = ["photonwise"]
        take_cs = ["heatmap trans-normal", "heatmap min-max"]
        take_cs = ["heatmap logarithmic"]

        do_connect_lines_list = [True]
        do_connect_lines_list = [True, False]
        do_connect_lines_list = [False]



        # SHOW CHARTS + MAKE .PNG IMAGES
        print()
        for cl_loop in do_connect_lines_list:
            for i in range(len(take_cs)):
                cs_loop = take_cs[i]
                print("({}) Run ChartMaker.show_all, color_scheme = {}".format(i, cs_loop))
                ChartMaker.show_all(result_propSetup,
                                    cs_loop,
                                    cl_loop,
                                    color_points_by_root = False,
                                    color_arrows_by_root = False,
                                    do_triangled_planes = False,
                                    draw_planes_from_material_stack = True,
                                    use_triangled_planes_from_file = USE_TRIANGLED_PLANES_FROM_FILE)


if __name__ == '__main__':
    RunAll.run()