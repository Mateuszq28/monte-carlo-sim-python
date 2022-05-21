import json
import make_sim_env

class Sim():

    def __init__(self):
        with open("config.cfg") as f:
            # get simulation config parameters
            config = json.load(f)

            # make propagation environment
            if config['make_default_env']:
                config['env_in_filename']
                propEnv = self.make_default_env()
            else:
                prop_env_filename = config['make_default_env']
                propEnv = make_sim_env.load_json()

                if config['env_filename']:
                
            if config['start_point'] is None:
                            half_depth = 
                            start_point = ()
                            

    def start_sim(self):
        for i in self.config['photons_num']:
            self.propagate_photon()

    def propagate_photon(self, start_point, ):
        pass

    def make_default_env(self):
        propEnv = make_sim_env.PropEnv()
        propEnv.fill_cube(1, [0, 0, 0], end_p=[1.0, 1.0, 0.25])
        return propEnv