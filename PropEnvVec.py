from PropEnv import PropEnv
from Material import Material, load_dump
import json
import numpy as np
import math
from Space3dTools import Space3dTools

class PropEnvVec(PropEnv):
    def __init__(self, x=100, y=100, z=100):
        self.shape = [x, y, z]
        with open("config.json") as f:
            # get simulation config parameters
            config = json.load(f)
        self.tissue_properties = config["tissue_properties"]
        self.config = config
        # MATERIAL LABELS, AFFILIATION FUNCTIONS, BOUNDARY FUNCTIONS AND INTERSECTIONS ARE DESCRIBED IN MATERIAL STACK
        # EACH POSITION IN MATERIAL STACK IS ONE MATERIAL OBJECT OF CLASS MATERIAL
        # THE HIGHER INDEX, THE HIGHER PRIORITY
        self.material_stack : list[Material]
    

    def get_label_from_float(self, xyz):
        if self.config["flag_ignore_prop_env_labels"]:
            return self.config["global_label_if_ignore_prop_env_labels"]
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
    
    def boundary_check(self, xyz:list, xyz_next:list, label_in):
        if self.config["flag_ignore_prop_env_labels"]:
            boundary_pos = xyz_next.copy()
            boundary_change = False
            boundary_norm_vec = None
            label_out = None
            return boundary_pos, boundary_change, boundary_norm_vec, label_in, label_out, None

        debug = False
        if debug:
            print()
            print("xyz", xyz)
            print("xyz_next", xyz_next)
            print("label_in", label_in)

        if type(xyz) != list or type(xyz_next) != list:
            raise ValueError("xyz and xyz_next should be lists")
        
        mat_in = [mat for mat in self.material_stack if mat.label == label_in]
        if len(mat_in) == 1:
            mat_in = mat_in[0]
        else:
            mat_in = [mat for mat in mat_in if mat.fun_in(xyz)][-1]
        intersections = [[i, mat.fun_intersect(xyz, xyz_next, mat_in)] for mat, i in zip(self.material_stack, range(len(self.material_stack))) if mat.label != label_in]
        intersections = [inter for inter in intersections if inter[1] != None]
        if debug:
            print("intersections", intersections)

        if len(intersections) < 1:
            boundary_pos = xyz_next.copy()
            boundary_change = False
            boundary_norm_vec = None
            label_out = None
            return boundary_pos, boundary_change, boundary_norm_vec, label_in, label_out, None
        
        closest_idx, closest_inter = min(intersections[::-1], key = lambda x: math.dist(x[1], xyz))
        boundary_pos = closest_inter
        boundary_change = True
        if debug:
            print("closest_inter", closest_inter)
            print("self.material_stack[closest_idx].label", self.material_stack[closest_idx].label)
            print()
        boundary_norm_vec = self.material_stack[closest_idx].fun_plane_normal_vec(closest_inter)
        if boundary_norm_vec is None:
            boundary_norm_vec = mat_in.fun_plane_normal_vec(closest_inter)

        # boundary plane normal vector should be directerd outside (towards material in point xyz (xyz in))
        ray_vec_out = (np.array(xyz) - np.array(closest_inter)).tolist()
        alfa = Space3dTools.angle_between_vectors(ray_vec_out, boundary_norm_vec)
        # alfa should be in <0,90> deg
        if alfa > math.pi / 2:
            boundary_norm_vec = [-val for val in boundary_norm_vec] # type: ignore

        label_out = self.material_stack[closest_idx].label
        return boundary_pos, boundary_change, boundary_norm_vec, label_in, label_out, None
    




    def save_json(self, path, additional=True):
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
        propEnv = PropEnvVec()
        propEnv.shape = d["self.shape"]
        propEnv.material_stack = [load_dump(mat_dump) for mat_dump in d["material_dumps"]] # type: ignore
        return propEnv

    # it is the same like in inheritance parent class
    # @staticmethod
    # def round_xyz(xyz):
    #     xyz_int = [round(val) for val in xyz]
    #     return xyz_int
        
    
