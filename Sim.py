import json
import numpy as np
import math
from Make import Make
from PropSetup import PropSetup
from Photon import Photon
from Space3dTools import Space3dTools
from FeatureSampling import FeatureSampling
import random


class Sim():

    propSetup: PropSetup

    def __init__(self):
        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)

        # interface to class, that makes Object3D instances, fills it and saves them to files
        make = Make()
        # interface to random functions
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


    def start_sim(self):
        photon_limits_list = self.propSetup.lightSource.photon_limits_list
        if photon_limits_list is not None:
            for i in range(len(photon_limits_list)):
                for j in range(photon_limits_list[i]):
                    ls = self.propSetup.lightSource.light_source_list
                    if ls is not None:
                        photon = ls[i].emit()
                        self.propagate_photon(photon)
                    else:
                        raise ValueError("ls is None")
        else:
            raise ValueError("photon_limits_list is None")


    def propagate_photon(self, photon: Photon):
        while photon.weight > 0:
            mu_a, mu_s, mu_t = self.propSetup.propEnv.get_properties(photon.pos)
            # move photon to new position
            self.hop(photon, mu_t)
            # absorb light in medium
            self.drop(photon, mu_a, mu_s, mu_t)
            self.spin(photon)
            flag_terminate = self.terminate(photon)
            if flag_terminate:
                break

            
    def hop(self, photon: Photon, mu_t):
        distance = photon.fun_hop(mu_t=mu_t)
        self.try_move(photon, distance)


    def try_move(self, photon:Photon, distance):
        step = [distance * ax for ax in photon.dir]
        next_pos = (np.array(photon.pos) + np.array(step)).tolist()

        # check if there was change of a material
        boundary_pos, boundary_change, boundary_norm_vec = self.propSetup.propEnv.boundary_check(photon.pos, next_pos)
        # check if photon is in env shape range
        if boundary_change:
            env_boundary_exceeded = False
        else:
            env_boundary_exceeded = self.propSetup.propEnv.env_boundary_check(next_pos)

        if not env_boundary_exceeded:
            if boundary_change:
                # save photon position with no absorb weight
                self.propSetup.save2resultRecords(xyz=boundary_pos, weight=0.)

                incident_vec = (np.array(boundary_pos) - np.array(photon.pos)).tolist()
                reflect_vec = Space3dTools.reflect_vector(incident_vec, boundary_norm_vec)

                # Total internal reflection
                R = 0
                neg_incident_vec = Space3dTools.negative_vector(incident_vec)
                alpha = Space3dTools.angle_between_vectors(neg_incident_vec, boundary_norm_vec)
                refraction_vec = None
                    # refractive indices
                n1 = self.propSetup.propEnv.get_refractive_index(xyz=photon.pos)
                n2 = self.propSetup.propEnv.get_refractive_index(xyz=boundary_pos)
                if n2 > n1:
                    critical_alpha = math.asin(n2 / n1)
                    if alpha > critical_alpha:
                        # internal reflectance
                        R = 1.

                if n2 <= n1 or R == 0:
                    refraction_vec = Space3dTools.refraction_vec(incident_vec, boundary_norm_vec, n1, n2)
                    neg_normal_vec = Space3dTools.negative_vector(boundary_norm_vec)
                    beta = Space3dTools.angle_between_vectors(refraction_vec, neg_normal_vec)
                    R = Space3dTools.internal_reflectance(alpha, beta)

                if R < 1.:
                    traveled_dist = math.dist(photon.pos, boundary_pos)
                    rest_dist = distance - traveled_dist
                    # penetration ray - refraction
                    # new photon to track
                    refraction_photon = Photon(boundary_pos, refraction_vec, weight=photon.weight*(1-R))
                    self.try_move(refraction_photon, rest_dist)
                    self.propagate_photon(refraction_photon)
                    # update old photon
                    photon.pos = boundary_pos
                    photon.weight *= R
                    photon.dir = reflect_vec
                    self.try_move(photon, rest_dist)
            
            else:
                photon.pos = next_pos
        # else ignore - photon escape


    def drop(self, photon:Photon, mu_a, mu_s, mu_t):
        w_drop = photon.weight * (mu_a / mu_t)
        self.propSetup.save2result_env(photon.pos, w_drop)
        self.propSetup.save2resultRecords(xyz=photon.pos, weight=w_drop)
        photon.weight = photon.weight * (mu_s / mu_t)


    def spin(self, photon):
        theta = self.featureSampling.photon_theta()
        phi = self.featureSampling.photon_phi()
        ux, uy, uz = Space3dTools.cart_vec_norm(photon.dir[0], photon.dir[1], photon.dir[2])

        do_method_from_book = False

        # from Chapter 5 5.3.5
        # Monte Carlo Modeling of Light Transport in Tissue (Steady State and Time of Flight)
        if do_method_from_book:
            if np.isclose(ux, 0) and np.isclose(uy, 0):
                uxx = math.sin(theta) * math.cos(phi)
                uyy = math.sin(theta) * math.sin(phi)
                if uz > 0:
                    uzz = math.cos(theta)
                else:
                    uzz = -math.cos(theta)
            else:
                temp = math.sqrt(1 - uz**2)
                uxx = math.sin(theta) * (ux * uz * math.cos(phi) - uy * math.sin(phi)) / temp + ux * math.cos(theta)
                uyy = math.sin(theta) * (uy * uz * math.cos(phi) + ux * math.sin(phi)) / temp + uy * math.cos(theta)
                uzz = -math.sin(theta) * math.cos(phi) * temp + uz * math.cos(theta)

        # (my simple idea) why not that?
        else:
            _, old_phi, old_theta = Space3dTools.cartesian2spherical(ux, uy, uz)
            new_phi = old_phi + phi
            new_theta = old_theta + theta
            uxx, uyy, uzz = Space3dTools.spherical2cartesian(R=1., theta=new_theta, phi=new_phi)

        # update dir vec
        photon.dir = [uxx, uyy, uzz]


    def terminate(self, photon:Photon):
        """
        Roulette Method
        from Chapter 5 5.3.6
        Monte Carlo Modeling of Light Transport in Tissue (Steady State and Time of Flight)
        """
        threshold = self.config["photon_weight_threshold"]
        chance = self.config["photon_chance"]
        rnd = random.random()
        flag_terminate = False
        if photon.weight < threshold:
            if rnd <= chance:
                photon.weight = photon.weight / chance
            else:
                flag_terminate = True
        return flag_terminate




        

    


    