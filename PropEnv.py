from Object3D import Object3D
import json
import numpy as np
import math
from MarchingCubes import MarchingCubes
from Space3dTools import Space3dTools

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
            if xyz_int[i] >= self.shape[i] or xyz_int[i] <= 0:
                env_boundary_exceeded = True
                break
        return env_boundary_exceeded
    
    def boundary_check(self, xyz:list, xyz_next:list):
        if type(xyz) != list or type(xyz_next) != list:
            raise ValueError("xyz and xyz_next should be lists")
        label_in = self.get_label_from_float(xyz)
        arr_xyz = np.array(xyz)
        arr_xyz_next = np.array(xyz_next)
        vec = arr_xyz_next - arr_xyz
        dist = np.linalg.norm(vec)
        # photon steps from position xyz to xyz_next 
        linspace = np.linspace(0.0, 1.0, num=int(dist)+1)

        # loop initiation values
        boundary_pos = xyz_next
        boundary_change = False
        boundary_norm_vec = None
        for t in linspace:
            check_pos = arr_xyz + vec * t
            if self.env_boundary_check(check_pos):
                # photon escaped from observed env (tissue)
                break
            label_check = self.get_label_from_float(check_pos)
            if label_in != label_check:
                proposed_norm_vec, proposed_boundary_pos = self.plane_boundary_normal_vec(xyz, check_pos.tolist())
                if proposed_norm_vec is not None:
                    boundary_change = True
                    boundary_pos = check_pos.tolist()
                    boundary_norm_vec = proposed_norm_vec
                    break
                else:
                    print("Photon was very close to the tissue boundary, but there was not intersection")
        return boundary_pos, boundary_change, boundary_norm_vec
    
    def plane_boundary_normal_vec(self, last_pos, boundary_pos):
        """
        Finds normal vector to the boundary tissue plane using
        Estimates the plane using Marching Cubes algorithm (8 marching cubes) in one local point (boundary_pos)
        """
        boundary_pos_label = self.get_label_from_float(boundary_pos)
        # suggest cubes surrounding boundary point
        # max 8, less if some cube's points are not in env shape range
        marching_cubes_centroids = self.cubes_surrounding_point(boundary_pos)
        
        # centroids distances from last_pos
        marching_cubes_distances = [math.dist(last_pos, cent) for cent in marching_cubes_centroids]
        
        # sort centroids by distances
        sorted_indices = np.argsort(marching_cubes_distances)
        marching_cubes_distances = np.array(marching_cubes_distances)[sorted_indices]
        marching_cubes_centroids = np.array(marching_cubes_centroids)[sorted_indices]

        # iter through marching cubes, find plane stretched on triangles,
        # check if the ray intersect this plane, find its norm vector and intersection point
        # loop initiation values
        return_norm_vec = None
        return_boundary_pos = boundary_pos.copy()
        for cent in marching_cubes_centroids:
            corners = MarchingCubes.marching_cube_corners_from_centroid(cent)
            # if corner has the same label, it's the part of the plane
            corner_full_binary_code = [self.get_label_from_float(co) == boundary_pos_label for co in corners]
            corner_full_decimal = sum([2**bit for bit, val in zip(range(7,-1,-1), corner_full_binary_code) if val == True])
            # all triangles corners in one list
            triangles = MarchingCubes.TriangleTable[corner_full_decimal].copy()
            # split into triangles
            triangles = [triangles[x:x+3] for x in range(0, len(triangles)-1, 3)]
            triangles_coordinates = [[MarchingCubes.triangle_corner_from_centroid(cent, corner_idx) for corner_idx in tri] for tri in triangles]
            # pp is list of three triangle corners
            triangles_planes = [Space3dTools.plane_equation(plane_point=pp[0], plane_normal_vec=Space3dTools.p3_to_normal_vec(pp[0], pp[1], pp[2])) for pp in triangles_coordinates]
            ray_intersect_planes = [Space3dTools.line_intersect_plane_point(pl_eq=tri_plane, l_p0=last_pos, l_p1=boundary_pos) for tri_plane in triangles_planes]
            # normal vec + intersection point, filter out None values
            normal_vec_and_intersect = [[plane_eq[:3], intersect] for plane_eq, intersect in zip(triangles_planes, ray_intersect_planes) if intersect is not None]
            # remove intersection points that are not in range of marching cube with centroid in cent 
            normal_vec_and_intersect_in_marching_cube = [[norm, p] for [norm, p] in normal_vec_and_intersect if (p[0] <= cent[0] + 0.5 and p[0] >= cent[0] - 0.5 and p[1] <= cent[1] + 0.5 and p[1] >= cent[1] - 0.5 and p[2] <= cent[2] + 0.5 and p[2] >= cent[2] - 0.5)]

            if len(normal_vec_and_intersect_in_marching_cube) == 0:
                continue
            else:
                return_norm_vec = normal_vec_and_intersect_in_marching_cube[0][0].copy()
                return_boundary_pos = normal_vec_and_intersect_in_marching_cube[0][1].copy()
                # to be sure, that norm ector is directed outwards boundary plane
                ray_vec_out = (np.array(last_pos) - np.array(boundary_pos)).tolist()
                alfa = Space3dTools.angle_between_vectors(ray_vec_out, return_norm_vec)
                # alfa should be in <0,90> deg
                if alfa > math.pi / 2:
                    return_norm_vec = (-np.array(return_norm_vec)).tolist()
                break
        return return_norm_vec, return_boundary_pos

            














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
    
