import json
from Make import Make
from PropSetup import PropSetup
from Photon import Photon

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
        mu_s, mu_a = self.propSetup.propEnv.get_properties(pos_x, pos_y, pos_z)

        

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
 