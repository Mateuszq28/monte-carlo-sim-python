from PropEnv import PropEnv
from LightSource import LightSource
from PropSetup import PropSetup
from FillShapes import FillShapes
import json
from MakeMaterial import MakeMaterial
import numpy as np
import time


class Make():
        
    # it is overwritten in sim
    flag_use_propenv_on_formulas = False

    def __init__(self, config):
        self.default_env_path = None
        self.default_light_surce_path = None
        self.default_prop_setup_path = None
        self.config = config


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
        start_time = time.time()
        env_idx = 1
        if Make.flag_use_propenv_on_formulas:
            makeMat = MakeMaterial(self.config)
            env_fun_list = [
                makeMat.default_env,
                makeMat.env_master_thesis_1layers,
                makeMat.env_master_thesis_2layers,
                makeMat.env_master_thesis_3layers,
                makeMat.env_master_thesis_multilayers

            ]
            propEnv = env_fun_list[env_idx]()
        else:
            env_fun_list = [
                self.default_env_on_points,
                self.env_master_thesis_1layers_table,
                self.env_master_thesis_2layers_table,
                self.env_master_thesis_3layers_table,
                self.env_master_thesis_multilayers_table
            ]
            propEnv = env_fun_list[env_idx]()
        end_time = time.time()
        print("making default env calculation time:", end_time-start_time)
        return propEnv


    def default_env_on_points(self):
        propEnv = PropEnv(x=50, y=50, z=100)
        propEnv.fill_cube(fill=1, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 1.0]) # air
        propEnv.fill_cube(fill=2, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 0.75]) # water
        propEnv.fill_cube(fill=4, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 0.65]) # dermis
        FillShapes.fill_vein(propEnv, z_pos=0.25)
        return propEnv
    

    def env_master_thesis_1layers_table(self):
        bins_per_1_cm = self.config["bins_per_1_cm"]
        # size od propEnv [x,y,z] in cm
        size_cm = [1.5,1.5,2]
        size_bins = [int(round(s_cm * bins_per_1_cm)) for s_cm in size_cm]
        propEnv = PropEnv(x=size_bins[0], y=size_bins[1], z=size_bins[2])
        propEnv.fill_cube(fill=4, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 1.0]) # dermis
        return propEnv
    

    def env_master_thesis_2layers_table(self):
        bins_per_1_cm = self.config["bins_per_1_cm"]
        # size od propEnv [x,y,z] in cm
        size_cm = [1.5,1.5,2]
        size_bins = [int(round(s_cm * bins_per_1_cm)) for s_cm in size_cm]
        propEnv = PropEnv(x=size_bins[0], y=size_bins[1], z=size_bins[2])
        propEnv.fill_cube(fill=3, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 1.0]) # epidermis
        propEnv.fill_cube(fill=4, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 0.5]) # dermis
        return propEnv
    

    def env_master_thesis_3layers_table(self):
        bins_per_1_cm = self.config["bins_per_1_cm"]
        # size od propEnv [x,y,z] in cm
        size_cm = [1.5,1.5,2]
        size_bins = [int(round(s_cm * bins_per_1_cm)) for s_cm in size_cm]
        propEnv = PropEnv(x=size_bins[0], y=size_bins[1], z=size_bins[2])
        propEnv.fill_cube(fill=3, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 1.0]) # epidermis
        propEnv.fill_cube(fill=4, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 0.66]) # dermis
        propEnv.fill_cube(fill=5, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 0.33]) # dermis
        return propEnv
    

    def env_master_thesis_multilayers_table(self):
        bins_per_1_cm = self.config["bins_per_1_cm"]
        # layer_names = ["air", "salt water (sweat)", "epidermis", "dermis", "vein", "blood", "vein", "dermis", "fatty subcutaneous tissue"]
        # layer_idx = [1, 2, 3, 4, 7, 8, 7, 4, 5]
        layer_size_cm = [0.01, 0.01, 0.01, 0.22, 0.05, 0.07, 0.05, 0.08, 0.3]
        sum_z = sum(layer_size_cm)
        upper_boundary = [float(sum(layer_size_cm[i:])/sum_z) for i in range(len(layer_size_cm))]
        # size od propEnv [x,y,z] in cm
        size_cm = [sum_z/2, sum_z/2, sum_z]
        size_bins = [int(round(s_cm * bins_per_1_cm)) for s_cm in size_cm]
        propEnv = PropEnv(x=size_bins[0], y=size_bins[1], z=size_bins[2])
        # cubes
        propEnv.fill_cube(fill=1, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 1.0]) # air
        propEnv.fill_cube(fill=2, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, upper_boundary[1]]) # salt water (sweat)
        propEnv.fill_cube(fill=3, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, upper_boundary[2]]) # epidermis
        propEnv.fill_cube(fill=4, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, upper_boundary[3]]) # dermis
        propEnv.fill_cube(fill=5, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, upper_boundary[-1]]) # fatty subcutaneous tissue
        # vein
        z_pos = float((upper_boundary[4] + upper_boundary[6])/2)
        # radius r is relative to y, not z
        r = ((layer_size_cm[4]+layer_size_cm[5]+layer_size_cm[6])/2) / size_cm[1]
        # same with vein_thickness
        vein_thickness = layer_size_cm[4]/size_cm[1]
        FillShapes.fill_vein(propEnv, z_pos=z_pos, r=r, vein_thickness=vein_thickness)
        return propEnv
    

    def default_light_source(self):
        lightSource = LightSource(x=1, y=1, z=1)
        lightSource.initialize_source(photon_limit=10000) # ID_EDIT_1
        return lightSource


    def default_prop_setup(self):
        env_path = self.default_env_path
        light_source_path = self.default_light_surce_path
        offset = [150, 150, 570]
        offset = None
        propSetup = PropSetup.from_components(env_path, light_source_path, offset=offset)
        return propSetup














