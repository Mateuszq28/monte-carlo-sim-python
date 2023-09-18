from PropEnv import PropEnv
from Material import Material
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












        label_in = self.get_label_from_float(xyz)
        arr_xyz = np.array(xyz)
        arr_xyz_next = np.array(xyz_next)
        vec = arr_xyz_next - arr_xyz
        dist = np.linalg.norm(vec)
        # photon steps from position xyz to xyz_next 
        linspace = np.linspace(0.0, 1.0, num=int(dist*2+2), endpoint=True)
        
        check_pos = vec.reshape(1,-1) * linspace.reshape(-1,1) + arr_xyz
        funs_in = [material.fun_in for material in self.material_stack]
        # is in flag array
        # each row is different material, in columns are flags "if in material" per point from linspace 
        in_flags = np.array([np.apply_along_axis(f, axis=1, arr=check_pos) for f in funs_in])
        are_all_in = np.all(in_flags, axis=1)
        are_all_out = np.all(in_flags == False, axis=1)
        change_in_material = ~np.logical_or(are_all_in, are_all_out)
        idx_mat_with_change = [i for i, flag_change in zip(range(len(change_in_material)), change_in_material) if flag_change]

        if len(idx_mat_with_change) < 1:
            boundary_pos = xyz_next.copy()
            boundary_change = False
            boundary_norm_vec = None
            return boundary_pos, boundary_change, boundary_norm_vec
        
        mat_idx = idx_mat_with_change[-1]
        




        # loop initiation values
        boundary_pos = xyz_next.copy()
        boundary_change = False
        boundary_norm_vec = None
        for t in linspace:
            check_pos = arr_xyz + vec * t
            if self.env_boundary_check(check_pos):
                # photon escaped from observed env (tissue)
                break
            label_check = self.get_label_from_float(check_pos)
            if label_in != label_check:
                proposed_norm_vec, proposed_boundary_pos = self.plane_boundary_normal_vec(xyz, check_pos.tolist(), debug=debug_flag)
                if proposed_norm_vec is not None:
                    # boundary_pos = check_pos.tolist()
                    boundary_pos = proposed_boundary_pos
                    boundary_change = True
                    boundary_norm_vec = proposed_norm_vec
                    if tuple(xyz) in self.very_close_photons:
                        print("Intersection done by photon from very_close_photons set!")
                        print("debug xyz in", xyz)
                        print()
                        self.very_close_photons.remove(tuple(xyz))
                    break
                else:
                    print("Photon was very close to the tissue boundary, but there was not intersection")
                    print("debug xyz in", xyz)
                    print("debug label_in", label_in)
                    print("debug check_pos", check_pos)
                    print("debug label_check", label_check)
                    print("debug xyz_next", xyz_next)
                    print("\n")
                    self.very_close_photons.add(tuple(xyz))
        return boundary_pos, boundary_change, boundary_norm_vec
    
    def plane_boundary_normal_vec(self, last_pos, boundary_pos, debug=False):
        """
        Finds normal vector to the boundary tissue plane using.
        Estimates the plane using Marching Cubes algorithm (8 marching cubes) in one local point (boundary_pos).
        """
        boundary_pos_label = self.get_label_from_float(boundary_pos)
        # suggest cubes surrounding boundary point
        # max 8, less if some cube's points are not in env shape range
        marching_cubes_centroids = self.cubes_surrounding_point(boundary_pos)
        
        # centroids distances from last_pos
        marching_cubes_distances = [math.dist(last_pos, cent) for cent in marching_cubes_centroids]
        if debug:
            print("marching_cubes_centroids", marching_cubes_centroids)
        
        # sort centroids by distances
        sorted_indices = np.argsort(marching_cubes_distances)
        marching_cubes_distances = np.array(marching_cubes_distances)[sorted_indices]
        marching_cubes_centroids = np.array(marching_cubes_centroids)[sorted_indices]
        if debug:
            print("sorted marching_cubes_centroids", marching_cubes_centroids)

        # - iter through marching cubes, find plane stretched on triangles,
        # - check if the ray intersect this plane, find its norm vector and intersection point
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
            cmv = MarchingCubes.cmv # marching cube corner +/- value from centroid
            om = MarchingCubes.om # out env margin (for example -0.17 is rounded to 0, so margin should be 0.5)
            normal_vec_and_intersect_in_marching_cube = self.filter_normal_vec_and_intersect(normal_vec_and_intersect, cent, cmv, om)
            # check if intersection wasn't somewhere between +cmv and +0.5
            if MarchingCubes.cmv < 0.5:
                cmv = 0.5
                control_list = self.filter_normal_vec_and_intersect(normal_vec_and_intersect, cent, cmv, om)
                if len(control_list) != len(normal_vec_and_intersect_in_marching_cube):
                    print("WARNING! Photon slipped in between marching cubes!")

            if debug:
                print("corners", corners)
                print("corner_full_binary_code", corner_full_binary_code)
                print("corner_full_decimal", corner_full_decimal)
                print("triangles", triangles)
                print("triangles_coordinates", triangles_coordinates)
                print("triangles_planes", triangles_planes)
                print("ray_intersect_planes", ray_intersect_planes)
                print("normal_vec_and_intersect", normal_vec_and_intersect)
                print("normal_vec_and_intersect_in_marching_cube", normal_vec_and_intersect_in_marching_cube)

            if len(normal_vec_and_intersect_in_marching_cube) == 0:
                continue
            else:
                return_norm_vec = normal_vec_and_intersect_in_marching_cube[0][0].copy()
                return_boundary_pos = normal_vec_and_intersect_in_marching_cube[0][1].copy()
                # to be sure, that norm vector is directed outwards boundary plane
                ray_vec_out = (np.array(last_pos) - np.array(return_boundary_pos)).tolist()
                alfa = Space3dTools.angle_between_vectors(ray_vec_out, return_norm_vec)
                # alfa should be in <0,90> deg
                if alfa > math.pi / 2:
                    return_norm_vec = (-np.array(return_norm_vec)).tolist()
                    alfa = Space3dTools.angle_between_vectors(ray_vec_out, return_norm_vec)

                if debug:
                    print("return_norm_vec", return_norm_vec)
                    print("return_boundary_pos", return_boundary_pos)
                    print("ray_vec_out", ray_vec_out)
                    print("alfa [deg]", alfa * 180 / math.pi)

                break
        return return_norm_vec, return_boundary_pos

            
    def filter_normal_vec_and_intersect(self, normal_vec_and_intersect, cent, cmv, om):
        out = []
        xc, yc, zc = cent[0], cent[1], cent[2]
        for norm, p in normal_vec_and_intersect:
            # flags is in centroid
            x_in_c = xc-cmv <= p[0] <= xc+cmv
            y_in_c = yc-cmv <= p[1] <= yc+cmv
            z_in_c = zc-cmv <= p[2] <= zc+cmv
            # flag is in env margin
            x_in_m = (0-om <= p[0] < 0) or (self.shape[0]-1 < p[0] <= self.shape[0]-1 + om)
            y_in_m = (0-om <= p[1] < 0) or (self.shape[1]-1 < p[1] <= self.shape[1]-1 + om)
            z_in_m = (0-om <= p[2] < 0) or (self.shape[2]-1 < p[2] <= self.shape[2]-1 + om)
            # flag to leave it in list
            is_ok = (x_in_c or x_in_m) and (y_in_c or y_in_m) and (z_in_c or z_in_m)
            if is_ok:
                out.append([norm, p])
        return out
        
        











    def cubes_surrounding_point(self, point):
        """
        suggest cubes surrounding boundary point
        max 8, less if some cube's points are not in env shape range
        """
        cmv = MarchingCubes.cmv
        point_int = self.round_xyz(point)
        # point_int = point
        marching_cubes_centroids = []
        # flags if corners are in env shape range
        flag_x_plus = point_int[0] + 1 <= self.shape[0] - 1
        flag_x_minus = point_int[0] - 1 >= 0
        flag_y_plus = point_int[1] + 1 <= self.shape[1] - 1
        flag_y_minus = point_int[1] -1 >= 0
        flag_z_plus = point_int[2] + 1 <= self.shape[2] - 1
        flag_z_minus = point_int[2] -1 >= 0
        # add centroids of cubes
        if flag_x_plus:
            if flag_y_plus:
                if flag_z_plus:
                    centroid = [val + cmv for val in point_int]
                    marching_cubes_centroids.append(centroid.copy())
                
                if flag_z_minus:
                    centroid = point_int.copy()
                    centroid[0] += cmv
                    centroid[1] += cmv
                    centroid[2] -= cmv
                    marching_cubes_centroids.append(centroid.copy())

            if flag_y_minus:
                if flag_z_plus:
                    centroid = point_int.copy()
                    centroid[0] += cmv
                    centroid[1] -= cmv
                    centroid[2] += cmv
                    marching_cubes_centroids.append(centroid.copy())

                if flag_z_minus:
                    centroid = point_int.copy()
                    centroid[0] += cmv
                    centroid[1] -= cmv
                    centroid[2] -= cmv
                    marching_cubes_centroids.append(centroid.copy())

        if flag_x_minus:
            if flag_y_plus:
                if flag_z_plus:
                    centroid = point_int.copy()
                    centroid[0] -= cmv
                    centroid[1] += cmv
                    centroid[2] += cmv
                    marching_cubes_centroids.append(centroid.copy())
                    
                if flag_z_minus:
                    centroid = point_int.copy()
                    centroid[0] -= cmv
                    centroid[1] += cmv
                    centroid[2] -= cmv
                    marching_cubes_centroids.append(centroid.copy())

            if flag_y_minus:
                if flag_z_plus:
                    centroid = point_int.copy()
                    centroid[0] -= cmv
                    centroid[1] -= cmv
                    centroid[2] += cmv
                    marching_cubes_centroids.append(centroid.copy())

                if flag_z_minus:
                    centroid = [val - cmv for val in point_int]
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
    
    @staticmethod
    def are_lists_with_same_vals(l1, l2):
        le1 = len(l1)
        le2 = len(l2)
        if le1 != le2:
            return False
        for i in range(le1):
            if l1[i] != l2[i]:
                return False
        return True
        
    
