import json
import os
import numpy as np
import math
import time
from Make import Make
from PropSetup import PropSetup
from MarchingCubes import MarchingCubes
from Photon import Photon
from Space3dTools import Space3dTools
from FeatureSampling import FeatureSampling, MyRandom
from tqdm import tqdm


class Sim():

    propSetup: PropSetup
    result_folder = "resultRecords"
    ONE_MINUS_COSZERO = 1.0E-12

    def __init__(self, load_last_dump=False):
        if load_last_dump:
            self.load_last_dump()
        else:
            with open("config.json") as f:
                # get simulation config parameters
                self.config = json.load(f)
            PropSetup.flag_use_propenv_on_formulas = self.config["flag_use_propenv_on_formulas"]
            Make.flag_use_propenv_on_formulas = self.config["flag_use_propenv_on_formulas"]
            self.boundary_check_calculation_time = 0
            self.splitted_photons_to_run = []

            # np.random.seed(self.config["random_seed"])
            MyRandom.random_seed_pool = self.config["random_seed"]
            # myRandom is defined in object, not in class, because sim is a object which uses many random numbers
            # (seperate random states across Sim instances are prefered)
            self.myRandom = MyRandom()

            # interface to class, that makes Object3D instances, fills it and saves them to files
            make = Make(self.config)
            # interface to random functions
            # featureSampling is defined in object, not in class, because sim is a object which uses many random numbers
            # (seperate random states across Sim instances are prefered)
            self.featureSampling = FeatureSampling()

            # default paths
            self.default_env_path = "envs/DefaultEnv.json"
            self.default_light_surce_path = "lightSources/DefaultLightSource.json"
            self.default_prop_setup_path = "propSetups/DefaultPropSetup.json"
            make.pass_default_paths(self.default_env_path, self.default_light_surce_path, self.default_prop_setup_path)

            # make default settings files from scratch
            if self.config["flag_make_default_env"]:
                make.default_env_file(self.default_env_path)
            if self.config["flag_make_default_light_source"]:
                make.default_light_source_file(self.default_light_surce_path)
            if self.config["flag_make_default_prop_setup_file"]:
                make.default_prop_setup_file(self.default_prop_setup_path)

            # set paths
            if self.config["flag_use_default_env"]:
                self.chosen_env_path = self.default_env_path
            else:
                self.chosen_env_path = self.config["alternative_env_path"]
            if self.config["flag_use_default_light_surce"]:
                self.chosen_light_source_path = self.default_light_surce_path
            else:
                self.chosen_light_source_path = self.config["alternative_light_source_path"]
            if self.config["flag_use_default_prop_setup"]:
                self.chosen_prop_setup_path = self.default_prop_setup_path
            else:
                self.chosen_prop_setup_path = self.config["alternative_prop_setup_path"]

            # make propagation setup (environment + light source)
            if self.config["flag_make_prop_setup_from_componentes"]:
                self.propSetup = PropSetup.from_components(self.chosen_env_path, self.chosen_light_source_path)
            else:
                self.propSetup = PropSetup.from_file(self.chosen_prop_setup_path)
            
            # link config to PropSetup
            self.propSetup.config = self.config
            # link output folder
            self.propSetup.result_folder = Sim.result_folder


    def load_last_dump(self):
        path_sim_dump = os.path.join(Sim.result_folder, "sim_dump.json")
        with open(path_sim_dump, 'r') as f:
            d = json.load(f)
        
        self.config = d["config"]
        self.splitted_photons_to_run = []

        # default paths
        self.default_env_path = d["default_env_path"]
        self.default_light_surce_path = d["default_light_surce_path"]
        self.default_prop_setup_path = d["default_prop_setup_path"]

        # set paths
        self.chosen_env_path = d["chosen_env_path"]
        self.chosen_light_source_path = d["chosen_light_source_path"]
        self.chosen_prop_setup_path = d["chosen_prop_setup_path"]

        MyRandom.generated_num = d["generated_num"]
        MyRandom.random_seed_pool = d["random_seed_pool"]
        # block off code from __init__
        PropSetup.flag_use_propenv_on_formulas = self.config["flag_use_propenv_on_formulas"]
        Make.flag_use_propenv_on_formulas = self.config["flag_use_propenv_on_formulas"]
        self.myRandom = MyRandom()
        make = Make(self.config)
        self.featureSampling = FeatureSampling()
        make.pass_default_paths(self.default_env_path, self.default_light_surce_path, self.default_prop_setup_path)
        self.propSetup = PropSetup.from_file(self.chosen_prop_setup_path)
        self.propSetup.config = self.config
        self.propSetup.result_folder = Sim.result_folder

        # values from propSetup obtained during the simulation
        self.propSetup.escaped_photons_weight = d["escaped_photons_weight"]
        self.propSetup.resultShape = d["resultShape"]
        self.propSetup.photon_register = d["photon_register"]
        self.propSetup.generated_num = d["generated_num"]
        self.propSetup.random_seed_pool = d["random_seed_pool"]

        # load resultEnv and resultRecords
        folder = Sim.result_folder
        self.propSetup.load_result_json(folder)

        self.simulation_calculation_time = d["simulation_calculation_time"]
        self.boundary_check_calculation_time = d["boundary_check_calculation_time"]


    def dump_sim_json(self):
        d = {
            # default paths
            "default_env_path": self.default_env_path,
            "default_light_surce_path": self.default_light_surce_path,
            "default_prop_setup_path": self.default_prop_setup_path,

            # set paths
            "chosen_env_path": self.chosen_env_path,
            "chosen_light_source_path": self.chosen_light_source_path,
            "chosen_prop_setup_path": self.chosen_prop_setup_path,

            # values from propSetup obtained during the simulation
            "escaped_photons_weight": self.propSetup.escaped_photons_weight,
            "resultShape": self.propSetup.resultShape,
            "random_seed_pool": self.propSetup.random_seed_pool,
            "generated_num": self.propSetup.generated_num,

            "simulation_calculation_time": self.simulation_calculation_time,
            "boundary_check_calculation_time": self.boundary_check_calculation_time,

            "config": self.config,
            "photon_register": self.propSetup.photon_register
        }
        path_sim_dump = os.path.join(Sim.result_folder, "sim_dump.json")
        with open(path_sim_dump, "w") as f:
            json.dump(d, f)
        

    def start_sim(self):
        start_time = time.time()
        photon_limits_list = self.propSetup.lightSource.photon_limits_list
        ls = self.propSetup.lightSource.light_source_list
        if photon_limits_list is not None:
            for i in range(len(photon_limits_list)):
                print("lightSource {i} progress:")
                for _ in tqdm(range(photon_limits_list[i])):
                    if ls is not None:
                        # local coordiantes
                        photon = ls[i].emit()
                        # global coordinates
                        photon.pos = (np.array(photon.pos) + self.propSetup.offset).tolist()
                        # set start pos material label
                        photon.mat_label = self.propSetup.propEnv.get_label_from_float(photon.pos)
                        # register start position in photon_register
                        self.propSetup.photon_register[str(photon.id)] = {"start_pos": self.condition_round(photon.pos),
                                                                          "parent": None,
                                                                          "child": []
                                                                         }
                        # propagate
                        # print("normal")
                        self.propagate_photon(photon)

                        # propagate photons from split list (refraction, reflection)
                        while len(self.splitted_photons_to_run) > 0:
                            # print("splitted")
                            # take values from stack
                            refraction_photon = self.splitted_photons_to_run.pop(0)
                            rest_dist_refraction = self.splitted_photons_to_run.pop(0)
                            # propagate
                            self.split_photon_actions(photon=refraction_photon, distance=rest_dist_refraction)
                            
                    else:
                        raise ValueError("ls is None")
        else:
            raise ValueError("photon_limits_list is None")
        end_time = time.time()
        self.simulation_calculation_time = end_time-start_time
        # save results
        self.propSetup.random_seed_pool = MyRandom.random_seed_pool
        self.propSetup.generated_num = MyRandom.generated_num
        self.propSetup.save_result_json(Sim.result_folder)
        self.dump_sim_json()
        return self.propSetup


    def propagate_photon(self, photon: Photon):
        while photon.weight > 0:
            _, _, mu_t = self.propSetup.propEnv.get_properties_from_label(photon.mat_label)
            # move photon to new position
            self.hop(photon, mu_t)
            # do the rest, get termination flag
            flag_break = self.after_hop(photon)
            if flag_break:
                break


    def split_photon_actions(self, photon, distance):
        self.try_move(photon, distance)
        flag_terminate = self.after_hop(photon)
        if not flag_terminate:
            self.propagate_photon(photon)
            

    def after_hop(self, photon: Photon):
        """
        Second part of propagation.
        Returns flag if terminate.
        """
        # photon.weight is set to 0 when photon escape env
        if photon.weight == 0:
            return True
        # absorb light in medium
        mu_a, mu_s, mu_t = self.propSetup.propEnv.get_properties_from_label(photon.mat_label)
        self.drop(photon, mu_a, mu_s, mu_t)
        self.spin(photon)
        flag_terminate = self.terminate(photon)
        if flag_terminate:
            return True
        return False

            
    def hop(self, photon: Photon, mu_t):
        distance = Photon.fun_hop(mu_t=mu_t)
        self.try_move(photon, distance)


    def try_move(self, photon:Photon, distance):
        # photon.print_me()
        # print(distance)
        min_step = self.config["min_step_when_boundary_cross"]
        loop_iter = 0
        while distance > 0 and photon.weight > 0:
            if loop_iter >= 5:
                # print(photon.id)
                # mu_a, mu_s, mu_t = self.propSetup.propEnv.get_properties_from_label(photon.mat_label)
                # self.drop(photon, mu_a, mu_s, mu_t)
                # if self.terminate(photon):
                #     break
                # self.just_move(photon, step=min_step)
                break
            loop_iter += 1

            # photon.print_me()
            # print(distance)

            step = [distance * ax for ax in photon.dir]
            next_pos = (np.array(photon.pos) + np.array(step)).tolist()

            # check if there was change of a material
            start_time = time.time()
            boundary_pos, boundary_change, boundary_norm_vec, label_in, label_out, forced_label_change = self.propSetup.propEnv.boundary_check(photon.pos, next_pos, photon.mat_label)
            if forced_label_change is not None:
                photon.mat_label = forced_label_change
            # print("nowy label_out fotonu otrzymany w sim!", label_out)
            # print("nowy boundary_pos fotonu otrzymany w sim!", boundary_pos)
            end_time = time.time()
            self.boundary_check_calculation_time += (end_time-start_time)
            # check if photon is in env shape range
            if boundary_change:
                # photon interact with the tissue earlier
                env_boundary_exceeded = False
            else:
                env_boundary_exceeded = self.propSetup.propEnv.env_boundary_check(next_pos)

            if not env_boundary_exceeded:
                if boundary_change:
                    # save photon position with no absorb weight
                    self.propSetup.save2resultRecords(xyz=boundary_pos, weight=0.0, photon_id=photon.id, round=self.config["flag_result_records_pos_int"])

                    incident_vec = (np.array(boundary_pos) - np.array(photon.pos)).tolist()
                    reflect_vec = Space3dTools.reflect_vector(incident_vec, boundary_norm_vec)

                    # Total internal reflection
                    R = 0.0 # init value
                    neg_incident_vec = Space3dTools.negative_vector(incident_vec)
                    alpha = Space3dTools.angle_between_vectors(neg_incident_vec, boundary_norm_vec)
                    refraction_vec = None
                        # refractive indices
                    n1 = self.propSetup.propEnv.get_refractive_index_from_label(label_in)
                    n2 = self.propSetup.propEnv.get_refractive_index_from_label(label_out)
                    if n2 < n1:
                        critical_alpha = math.asin(n2 / n1)
                        if alpha > critical_alpha:
                            # internal reflectance
                            R = 1.0

                    # if R was not set
                    # (if there was not total internal reflection)
                    if R == 0.0:
                        refraction_vec = Space3dTools.refraction_vec(incident_vec, boundary_norm_vec, n1, n2)
                        neg_normal_vec = Space3dTools.negative_vector(boundary_norm_vec)
                        beta = Space3dTools.angle_between_vectors(refraction_vec, neg_normal_vec)
                        # print("n1:", n1)
                        # print("n2:", n2)
                        R = Space3dTools.internal_reflectance(alpha, beta)

                    traveled_dist = math.dist(photon.pos, boundary_pos)
                    rest_dist_reflection = distance - traveled_dist - min_step
                    # for refraction we need to change hop, because material has changed
                    if rest_dist_reflection > 0:
                        _, _, mu_t = self.propSetup.propEnv.get_properties_from_label(label_in)
                        F = Photon.hop_distribution(mu_t=mu_t, hop=rest_dist_reflection)
                        _, _, mu_t = self.propSetup.propEnv.get_properties_from_label(label_out)
                        rest_dist_refraction = photon.fun_hop(mu_t=mu_t, F=F)
                    else:
                        rest_dist_refraction = 0

                    if R == 0.0:
                        # ONLY REFRACTION (OLD RAY)
                        # penetration ray - refraction
                        # photon.weight *= (1.0-R)
                        photon.pos = boundary_pos
                        photon.dir = refraction_vec
                        photon.mat_label = label_out
                        self.just_move(photon, min_step)
                        # SET DISTANCE VALUE TO AVOID RECURENTION
                        # self.try_move(photon, rest_dist_refraction)
                        distance = rest_dist_refraction

                    if 0.0 < R < 1.0:

                        if self.config["use_proba_instead_of_splitting"]:
                            # DECIDE BASED ON PROBABLITY WHICH RAY TO PROPAGATE
                            # (REFRACTION RAY OR REFLECTION RAY)
                            rnd_uniform = self.featureSampling.proba_split()
                            if rnd_uniform < R:
                                flag_reflect = False
                            else:
                                flag_reflect = True
                            
                            if flag_reflect:
                                # ONLY REFLECTION (OLD RAY)
                                # photon weight is not changed
                                photon.pos = boundary_pos
                                photon.dir = reflect_vec
                                photon.mat_label = label_in
                                self.just_move(photon, min_step)
                                # SET DISTANCE VALUE TO AVOID RECURENTION
                                # self.try_move(photon, rest_dist_reflection)
                                distance = rest_dist_reflection
                            else:
                                # ONLY REFRACTION (OLD RAY)
                                # penetration ray - refraction
                                # photon weight is not changed
                                photon.pos = boundary_pos
                                photon.dir = refraction_vec
                                photon.mat_label = label_out
                                self.just_move(photon, min_step)
                                # SET DISTANCE VALUE TO AVOID RECURENTION
                                # self.try_move(photon, rest_dist_refraction)
                                distance = rest_dist_refraction

                        else:
                            # RAY IS SPLIT INTO REFRACTION RAY AND REFLECTION (OLD) RAY
                            # penetration ray - refraction
                            # new photon to track
                            refraction_photon = Photon(boundary_pos.copy(), refraction_vec, weight=photon.weight*(1.0-R))
                            refraction_photon.mat_label = label_out
                            self.propSetup.photon_register[str(refraction_photon.id)] = {"start_pos": self.condition_round(refraction_photon.pos),
                                                                                    "parent": photon.id,
                                                                                    "child": []
                                                                                    }
                            self.propSetup.photon_register[str(photon.id)]["child"].append(refraction_photon.id)
                            self.just_move(refraction_photon, min_step)
                            # --block of new photon propagation
                            if self.config["recurention_if_split"]:
                                self.split_photon_actions(photon=refraction_photon, distance=rest_dist_refraction)
                            else:
                                self.splitted_photons_to_run.append(refraction_photon)
                                self.splitted_photons_to_run.append(rest_dist_refraction)
                            # --end block of new photon propagation
                            # update old photon (reflection one)
                            photon.weight *= R
                            photon.pos = boundary_pos
                            photon.dir = reflect_vec
                            photon.mat_label = label_in
                            self.just_move(photon, min_step)
                            # SET DISTANCE VALUE TO AVOID RECURENTION
                            # self.try_move(photon, rest_dist_reflection)
                            distance = rest_dist_reflection

                    if R == 1.0:
                        # ONLY REFLECTION (OLD RAY)
                        # photon.weight *= R
                        photon.pos = boundary_pos
                        photon.dir = reflect_vec
                        photon.mat_label = label_in
                        self.just_move(photon, min_step)
                        # SET DISTANCE VALUE TO AVOID RECURENTION
                        # self.try_move(photon, rest_dist_reflection)
                        distance = rest_dist_reflection
                
                else:
                    # photon just moved in the same tissue
                    photon.pos = next_pos
                    # REST DISTANCE, LOOP CONDITION
                    distance = 0
            else:
                # ignore the further path of the photon - photon escape from tissue
                self.propSetup.save2resultRecords(xyz=next_pos, weight=photon.weight, photon_id=photon.id, round=self.config["flag_result_records_pos_int"])
                photon.pos = next_pos
                self.propSetup.escaped_photons_weight += photon.weight
                # stop tracking
                # with a weight of zero, the algorithm will finish tracking (loop condition)
                photon.weight = 0.0
                # REST DISTANCE, LOOP CONDITION
                distance = 0


    def just_move(self, photon: Photon, step):
        vec = np.array(photon.dir) * step
        photon.pos = [p+s for p, s in zip(photon.pos, vec)]


    def drop(self, photon:Photon, mu_a, mu_s, mu_t):
        w_drop = photon.weight * (mu_a / mu_t)
        self.propSetup.save2result_env_and_records(xyz=photon.pos, weight=w_drop, photon_id=photon.id, round=self.config["flag_result_records_pos_int"])
        photon.weight = photon.weight * (mu_s / mu_t)


    def sign(self, x):
        if x >= 0:
            return 1
        else:
            return -1


    def spin_mc321(self, photon: Photon):
        ux, uy, uz = Space3dTools.cart_vec_norm(photon.dir[0], photon.dir[1], photon.dir[2])
        costheta, sintheta, cosphi, sinphi = photon.fun_get_spin()
        # --- New trajectory. ---
        if (1 - abs(uz) <= self.ONE_MINUS_COSZERO): # close to perpendicular.
            uxx = sintheta * cosphi
            uyy = sintheta * sinphi
            # SIGN() is faster than division.
            uzz = costheta * self.sign(uz)
        else: # usually use this option
            temp = math.sqrt(1.0 - uz * uz)
            uxx = sintheta * (ux * uz * cosphi - uy * sinphi) / temp + ux * costheta
            uyy = sintheta * (uy * uz * cosphi + ux * sinphi) / temp + uy * costheta
            uzz = -sintheta * cosphi * temp + uz * costheta
        return [uxx, uyy, uzz]


    def spin(self, photon: Photon):
        # =======================================================================================
        # OLD METHOD
        # =======================================================================================
        # # print("photon.dir before spin", photon.dir)
        # theta = Photon.featureSampling.photon_theta()
        # phi = Photon.featureSampling.photon_phi()
        # ux, uy, uz = Space3dTools.cart_vec_norm(photon.dir[0], photon.dir[1], photon.dir[2])

        # do_method_from_book = True

        # # from Chapter 5 5.3.5
        # # Monte Carlo Modeling of Light Transport in Tissue (Steady State and Time of Flight)
        # if do_method_from_book:
        #     if np.isclose(ux, 0) and np.isclose(uy, 0):
        #         uxx = math.sin(theta) * math.cos(phi)
        #         uyy = math.sin(theta) * math.sin(phi)
        #         if uz > 0:
        #             uzz = math.cos(theta)
        #         else:
        #             uzz = -math.cos(theta)
        #     else:
        #         temp = math.sqrt(1 - uz**2)
        #         uxx = math.sin(theta) * (ux * uz * math.cos(phi) - uy * math.sin(phi)) / temp + ux * math.cos(theta)
        #         uyy = math.sin(theta) * (uy * uz * math.cos(phi) + ux * math.sin(phi)) / temp + uy * math.cos(theta)
        #         uzz = -math.sin(theta) * math.cos(phi) * temp + uz * math.cos(theta)

        # # (my simple idea) why not that?
        # else:
        #     _, old_phi, old_theta = Space3dTools.cartesian2spherical(ux, uy, uz)
        #     new_phi = old_phi + phi
        #     new_theta = old_theta + theta
        #     uxx, uyy, uzz = Space3dTools.spherical2cartesian(R=1., theta=new_theta, phi=new_phi)
        # =======================================================================================

        # NEW METHOD
        [uxx, uyy, uzz] = self.spin_mc321(photon)

        # update dir vec
        photon.dir = [uxx, uyy, uzz]
        # print("photon.dir after spin", photon.dir)


    def terminate(self, photon:Photon):
        """
        Roulette Method
        from Chapter 5 5.3.6
        Monte Carlo Modeling of Light Transport in Tissue (Steady State and Time of Flight)
        """
        threshold = self.config["photon_weight_threshold"]
        chance = self.config["photon_chance"]
        rnd = self.myRandom.uniform_half_open(0.0, 1.0)
        flag_terminate = False
        if photon.weight < threshold:
            if rnd < chance:
                new_weight = photon.weight / chance
                self.propSetup.escaped_photons_weight -= (new_weight - photon.weight)
                photon.weight = new_weight
            else:
                self.propSetup.escaped_photons_weight += photon.weight
                flag_terminate = True
        return flag_terminate
    
    def condition_round(self, xyz):
        xyz = xyz.copy()
        if self.config["flag_result_records_pos_int"]:
            xyz = [round(val) for val in xyz]
        return xyz




        

    


    