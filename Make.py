from PropEnv import PropEnv
from LightSource import LightSource
from PropSetup import PropSetup
from FillShapes import FillShapes
import json


class Make():

    def __init__(self):
        self.default_env_path = None
        self.default_light_surce_path = None
        self.default_prop_setup_path = None


    def pass_default_paths(self, default_env_path, default_light_surce_path, default_prop_setup_path):
        self.default_env_path = default_env_path
        self.default_light_surce_path = default_light_surce_path
        self.default_prop_setup_path = default_prop_setup_path


    def default_env_file(self, path):
        propEnv = self.default_env()
        propEnv.save_json(path)


    def default_light_source_file(self, path):
        lightSource = self.default_light_source()
        lightSource.save_json(path)


    def default_prop_setup_file(self, path):
        propSetup = self.default_prop_setup()
        propSetup.save_json(path)


    def default_env(self):
        propEnv = PropEnv(x=50, y=50, z=100)
        propEnv.fill_cube(fill=1, start_p=[0, 0, 0], end_p=[1.0, 1.0, 1.0]) # air
        propEnv.fill_cube(fill=2, start_p=[1.0, 1.0, 0.70], end_p=[1.0, 1.0, 0.75]) # water
        propEnv.fill_cube(fill=2, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 0.70]) # skin
        FillShapes.fill_vein(propEnv, z_pos=0.35)
        return propEnv


    def default_light_source(self):
        lightSource = LightSource(x=1, y=1, z=1)
        lightSource.initialize_source(photon_limit=100)
        return lightSource


    def default_prop_setup(self):
        env_path = self.default_env_path
        light_source_path = self.default_light_surce_path
        offset = [150, 150, 570]
        offset = None
        propSetup = PropSetup.from_components(env_path, light_source_path, offset=offset)
        return propSetup














