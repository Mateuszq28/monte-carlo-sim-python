from PropEnv import PropEnv
from Material import Material, load_dump
import json
import numpy as np
import math

class PropEnvOnMathFormulas(PropEnv):
    def __init__(self, x=100, y=100, z=100):
        self.shape = [x, y, z]
        with open("config.json") as f:
            # get simulation config parameters
            config = json.load(f)
        self.tissue_properties = config["tissue_properties"]
        # MATERIAL LABELS, AFFILIATION FUNCTIONS, BOUNDARY FUNCTIONS AND INTERSECTIONS ARE DESCRIBED IN MATERIAL STACK
        # EACH POSITION IN MATERIAL STACK IS ONE MATERIAL OBJECT OF CLASS MATERIAL
        # THE HIGHER INDEX, THE HIGHER PRIORITY
        self.material_stack : list[Material]
    

    def get_label_from_float(self, xyz):
        last_in_label = [material.label for material in self.material_stack if material.fun_in(xyz)][-1]
        return last_in_label

    # it is the same like in inheritance parent class
    # def get_properties(self, xyz):
    #     label = self.get_label_from_float(xyz)
    #     label_str = str(label)
    #     # Absorption Coefficient in 1/cm
    #     mu_a = self.tissue_properties[label_str]["mu_a"]
    #     # Scattering Coefficient in 1/cm
    #     mu_s = self.tissue_properties[label_str]["mu_s"]
    #     # Total attenuation coefficient in 1/cm
    #     mu_t = mu_a + mu_s
    #     return mu_a, mu_s, mu_t
    
    # it is the same like in inheritance parent class
    # def get_refractive_index(self, xyz):
    #     label = self.get_label_from_float(xyz)
    #     label_str = str(label)
    #     # absolute refractive index
    #     n = self.tissue_properties[label_str]["n"]
    #     return n
    
    # it is the same like in inheritance parent class
    # def env_boundary_check(self, xyz):
    #     xyz_int = PropEnv.round_xyz(xyz)
    #     env_boundary_exceeded = False
    #     for i in range(3):
    #         if xyz_int[i] > self.shape[i]-1 or xyz_int[i] < 0:
    #             env_boundary_exceeded = True
    #             break
    #     return env_boundary_exceeded
    
    def boundary_check(self, xyz:list, xyz_next:list):
        if type(xyz) != list or type(xyz_next) != list:
            raise ValueError("xyz and xyz_next should be lists")
        
        label_in = self.get_label_from_float(xyz)
        intersections = [[i, mat.fun_intersect(xyz, xyz_next)] for mat, i in zip(self.material_stack, range(len(self.material_stack))) if mat.label != label_in]

        if len(intersections) < 1:
            boundary_pos = xyz_next.copy()
            boundary_change = False
            boundary_norm_vec = None
            return boundary_pos, boundary_change, boundary_norm_vec
        
        closest_idx, closest_inter = min(intersections, key = lambda x: math.dist(x[1], xyz))
        boundary_pos = closest_inter
        boundary_change = True
        boundary_norm_vec = self.material_stack[closest_idx].fun_plane_normal_vec()
        return boundary_pos, boundary_change, boundary_norm_vec




    def save_json(self, path):
        material_dumps = [mat.make_dump() for mat in self.material_stack]
        d = dict()
        d["self.shape"] = self.shape
        d["material_dumps"] = material_dumps
        with open(path, 'w') as f:
            json.dump(d, f)

    @staticmethod
    def load_json(path):
        with open(path, 'r') as f:
            d = json.load(f)
        propEnv = PropEnvOnMathFormulas()
        propEnv.shape = d["self.shape"]
        propEnv.material_stack = [load_dump(mat_dump) for mat_dump in d["material_dumps"]]
        return propEnv

    # it is the same like in inheritance parent class
    # @staticmethod
    # def round_xyz(xyz):
    #     xyz_int = [round(val) for val in xyz]
    #     return xyz_int
        
    
