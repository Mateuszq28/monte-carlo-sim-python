import json
import numpy as np
import math
from Make import Make
from PropSetup import PropSetup
from Photon import Photon
from Space3dTools import Space3dTools


class Sim():

    propSetup: PropSetup

    def __init__(self):
        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)

        # interface to class, that makes Object3D instances, fills it and saves them to files
        make = Make()

        # default paths
        self.default_env_path = "envs/DefaultEnv.json"
        self.default_light_surce_path = "lightSources/DefaultLightSource.json"
        self.default_prop_setup_path = "propSetups/DefaultPropSetup.json"

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
        pos_x, pos_y, pos_z = photon.pos

        while photon.weight > 0:
            mu_a, mu_s = self.propSetup.propEnv.get_properties(pos_x, pos_y, pos_z)
            mu_t = mu_a + mu_s
            ux, uy, uz = self.hop(photon, mu_t)
            

            albedo = mu_s / (mu_s + mu_a);
            rs = (n-1.0)*(n-1.0)/(n+1.0)/(n+1.0);	/* specular reflection */
            crit_angle = sqrt(1.0-1.0/n/n);			/* cos of critical angle */
            bins_per_mfp = 1e4/microns_per_bin/(mu_a+mu_s);
            

                launch ();
                while (weight > 0) {
                    move ();
                    absorb ();
                    scatter ();
                }
            
    def hop(self, photon: Photon, mu_t):
        distance = photon.fun_hop(mu_t=mu_t)
        self.try_move(photon, distance)


    def try_move(self, photon:Photon, distance):
        step = [distance * ax for ax in photon.dir]
        next_pos = np.array(photon.pos) + np.array(step)

        # check if there was change of a material
        boundary_pos, boundary_change, n1, n2 = self.propSetup.propEnv.boundary_check(photon.pos, next_pos)
        # check if photon is in env range
        if boundary_change:
            env_boundary_exceeded = False
        else:
            env_boundary_exceeded = self.propSetup.propEnv.env_boundary_check(next_pos)

        if not env_boundary_exceeded:
            if boundary_change:
                label_in = self.propSetup.propEnv.get_label_from_float(photon.pos)
                plane_boundary_normal_vec = self.propSetup.propEnv.plane_normal_vec(boundary_pos, label_in)
                incident_vec = np.array(boundary_pos) - np.array(photon.pos)
                reflect_vec = Space3dTools.reflect_vector(incident_vec, plane_boundary_normal_vec)

                # Total internal reflection
                R = 0
                neg_incident_vec = Space3dTools.negative_vector(incident_vec)
                alpha = Space3dTools.angle_between_vectors(neg_incident_vec, plane_boundary_normal_vec)
                refraction_vec = None
                if n2 > n1:
                    critical_alpha = math.asin(n2 / n1)
                    if alpha > critical_alpha:
                        # internal reflectance
                        R = 1.

                if n2 <= n1 or R == 0:
                    refraction_vec = Space3dTools.refraction_vec(incident_vec, plane_boundary_normal_vec, n1, n2)
                    neg_normal_vec = Space3dTools.negative_vector(plane_boundary_normal_vec)
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

    


    