from Object3D import Object3D
import json
import numpy as np
import math
from MarchingCubes import *

class PropEnv(Object3D):
    def __init__(self, x=100, y=100, z=100, arr=None):
        super().__init__(x, y, z, arr)
        with open("config.json") as f:
            # get simulation config parameters
            config = json.load(f)
        self.tissue_properties = config["tissue_properties"]
    
    def get_label_from_float(self, xyz):
        xyz_int = self.round_xyz(xyz)
        label = self.body[xyz_int[0], xyz_int[1], xyz_int[2]]
        return label

    def get_properties(self, xyz):
        label = self.get_label_from_float(xyz)
        label_str = str(label)
        # Absorption Coefficient in 1/cm
        mu_a = self.tissue_properties[label_str]["mu_a"]
        # Scattering Coefficient in 1/cm
        mu_s = self.tissue_properties[label_str]["mu_s"]
        # Total attenuation coefficient in 1/cm
        mu_t = mu_a + mu_s
        return mu_a, mu_s, mu_t
    
    def get_refractive_index(self, xyz):
        label = self.get_label_from_float(xyz)
        label_str = str(label)
        # absolute refractive index
        n = self.tissue_properties[label_str]["n"]
        return n
    
    def env_boundary_check(self, xyz):
        xyz_int = self.round_xyz(xyz)
        env_boundary_exceeded = False
        for i in range(3):
            if xyz_int[i] > self.shape[i]:
                env_boundary_exceeded = True
                break
        return env_boundary_exceeded
    
    def boundary_check(self, xyz, xyz_next):
        label_in = self.get_label_from_float(xyz)

        # data type correctness
        if isinstance(xyz, np.ndarray):
            arr_xyz = xyz.copy()
        else:
            arr_xyz = np.array(xyz)
        if isinstance(xyz_next, np.ndarray):
            arr_xyz_next = xyz_next.copy()
        else:
            arr_xyz_next = np.array(xyz_next)

        vec = arr_xyz_next - arr_xyz
        dist = np.linalg.norm(vec)
        # photon steps from position xyz to xyz_next 
        linspace = np.linspace(0.0, dist, num=int(dist)+1)
        boundary_pos = xyz_next
        boundary_change = False
        for lin in linspace:
            t = lin/dist
            check_pos = arr_xyz + vec * t
            label_check = self.get_label_from_float(check_pos)
            if label_in != label_check:
                boundary_change = True
                boundary_pos = check_pos.tolist()
                break
        return boundary_pos, boundary_change
    
    def plane_boundary_normal_vec(self, last_pos, boundary_pos):
        boundary_pos_label = self.get_label_from_float(boundary_pos)
        # suggest cubes surrounding boundary point
        # max 8, less if some cube's points are not in env shape range
        marching_cubes_centroids = self.cubes_surrounding_point(boundary_pos)
        
        # centroids distances from last_pos
        marching_cubes_distances = []
        for cent in marching_cubes_centroids:
            marching_cubes_distances.append(math.dist(last_pos, cent))
        
        # sort centroids by distances
        sorted_indices = np.argsort(marching_cubes_distances)
        marching_cubes_distances = np.array(marching_cubes_distances)[sorted_indices]
        marching_cubes_centroids = np.array(marching_cubes_centroids)[sorted_indices]

        # iter through marching cubes, find plane stretched on triangles,
        # check if the ray crosses this plane, find its norm vector
        for cent, dist in list(zip(marching_cubes_centroids, marching_cubes_distances)):
            corners = marching_cube_corners_from_centroid(cent)
            # if corner has the same label, it's the part of the plane
            corner_full_binary_code = [self.get_label_from_float(co) == boundary_pos_label for co in corners]
            corner_full_decimal = sum([2**bit for bit, val in zip(range(7,-1,-1), corner_full_binary_code) if val == True])
            # all triangles corners in one list
            triangles = TriangleTable[corner_full_decimal].copy()
            # split into triangles
            triangles = [triangles[x:x+3] for x in range(0, len(triangles)-1, 3)]
            triangles_coordinates = [[triangle_corner_from_centroid(cent, corner_idx) for corner_idx in tri] for tri in triangles]
            













    def cubes_surrounding_point(self, point):
        """
        suggest cubes surrounding boundary point
        max 8, less if some cube's points are not in env shape range
        """
        point_int = self.round_xyz(point)
        marching_cubes_centroids = []
        # flags if corners are in env shape range
        flag_x_plus = point_int[0] + 1 <= self.shape[0]
        flag_x_minus = point_int[0] >= 1
        flag_y_plus = point_int[1] + 1 <= self.shape[1]
        flag_y_minus = point_int[1] >= 1
        flag_z_plus = point_int[2] + 1 <= self.shape[2]
        flag_z_minus = point_int[2] >= 1
        # add centroids of cubes
        if flag_x_plus:
            if flag_y_plus:
                if flag_z_plus:
                    centroid = [val + 0.5 for val in point_int]
                    marching_cubes_centroids.append(centroid.copy())
                
                if flag_z_minus:
                    centroid = point_int.copy()
                    centroid[0] += 0.5
                    centroid[1] += 0.5
                    centroid[2] -= 0.5
                    marching_cubes_centroids.append(centroid.copy())

            if flag_y_minus:
                if flag_z_plus:
                    centroid = point_int.copy()
                    centroid[0] += 0.5
                    centroid[1] -= 0.5
                    centroid[2] += 0.5
                    marching_cubes_centroids.append(centroid.copy())

                if flag_z_minus:
                    centroid = point_int.copy()
                    centroid[0] += 0.5
                    centroid[1] -= 0.5
                    centroid[2] -= 0.5
                    marching_cubes_centroids.append(centroid.copy())

        if flag_x_minus:
            if flag_y_plus:
                if flag_z_plus:
                    centroid = point_int.copy()
                    centroid[0] -= 0.5
                    centroid[1] += 0.5
                    centroid[2] += 0.5
                    marching_cubes_centroids.append(centroid.copy())
                    
                if flag_z_minus:
                    centroid = point_int.copy()
                    centroid[0] -= 0.5
                    centroid[1] += 0.5
                    centroid[2] -= 0.5
                    marching_cubes_centroids.append(centroid.copy())

            if flag_y_minus:
                if flag_z_plus:
                    centroid = point_int.copy()
                    centroid[0] -= 0.5
                    centroid[1] -= 0.5
                    centroid[2] += 0.5
                    marching_cubes_centroids.append(centroid.copy())

                if flag_z_minus:
                    centroid = [val - 0.5 for val in point_int]
                    marching_cubes_centroids.append(centroid.copy())

        return marching_cubes_centroids
    

    @staticmethod
    def load_json(path):
        with open(path, 'r') as f:
            d = json.load(f)
        arr = np.array(d["body"])
        return PropEnv(arr=arr)

    @staticmethod
    def round_xyz(xyz):
        xyz_int = [round(val) for val in xyz]
        return xyz_int
    
