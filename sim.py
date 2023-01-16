import json
import make_sim_env

class Sim():

    def __init__(self):
        with open("config.cfg") as f:
            # get simulation config parameters
            config = json.load(f)

            # make propagation environment
            if config['make_default_env']:
                prop_env_path = config['default_env_path']
                propEnv = make_sim_env.make_default_env()
            else:
                prop_env_path = config['non_default_env_path']
                propEnv = make_sim_env.load_env_json(prop_env_path)
                
            # make propagation environment
            if config['start_point'] is None:
                            half_depth = 
                            start_point = ()

        

            self.prop_env_filename = prop_env_path
            self.propEnv = propEnv




                            

    def start_sim(self):
        for i in self.config['photons_num']:
            self.propagate_photon()

    def propagate_photon(self, start_point, ):
        pass

    



        