import json
from Make import Make
from PropSetup import PropSetup

class Sim():

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
        for _ in range(self.config["number_of_photons"]):
            self.propagate_photon()
            

    def propagate_photon(self, start_point, ):
        raise NotImplementedError()
    




'''
if __name__ == '__main__':
    ap = argparse.ArgumentParser(fromfile_prefix_chars='@')
    ap.add_argument('-l', '--lol', help="nazwa pliku jsona do podziału", metavar='String', default=filename_in)
    ap.add_argument('-tr', '--train', help='nazwa pliku jsona wyjściowego - train', metavar='String', default=filename_out_train)
    ap.add_argument('-te', '--test', help='nazwa pliku jsona wyjściowego - test', metavar='String', default=filename_out_test)
    ap.add_argument('-r', '--ratio', help='stosunek zbioru testowego do całości', metavar=float, default=split_ratio)

    args = vars(ap.parse_args())

    arg_input = args['input']
    arg_train = args['train']
    arg_test = args['test']
    arg_ratio = args['ratio']
'''