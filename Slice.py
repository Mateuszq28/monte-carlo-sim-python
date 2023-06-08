from Object3D import Object3D
import numpy as np
import PIL
from PIL import ImageColor, Image
import os
import math
from typing import List, Tuple
from Projection import Projection


class Slice(Object3D):
    def __init__(self, x=100, y=100, z=100, arr=None):
        super().__init__(x, y, z, arr)
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.omit = [0]
        self.reset_val = 0

    
    def set_plane_points(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3


    def points_dist(self, p1, p2):
        # dist = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
        dist = np.linalg.norm(np.array(p2) - np.array(p1))
        return dist


    def farthest_from_p(self, p, arr_shape):
        arr_max_idx = [x-1 for x in arr_shape]
        c0 = [0,0,0]
        c1 = [0,0,arr_max_idx[2]]
        c2 = [0,arr_max_idx[1],0]
        c3 = [0,arr_max_idx[1],arr_max_idx[2]]
        c4 = [arr_max_idx[0],0,0]
        c5 = [arr_max_idx[0],0,arr_max_idx[2]]
        c6 = [arr_max_idx[0],arr_max_idx[1],0]
        c7 = [arr_max_idx[0],arr_max_idx[1],arr_max_idx[2]]
        farthest = c0
        farthest_dist = self.points_dist(p, c0)
        corners = [c1, c2, c3, c4, c5, c6, c7]
        for c in corners:
            d = self.points_dist(p, c)
            if d > farthest_dist:
                farthest = c
                farthest_dist = d
        return farthest


    def preset_decoder(self, p, preset, arr_shape):
        p1 = self.float2int_point_decoder(p, arr_shape)
        if preset in ['xy', 'yx']:
            p1 = [0., 0., p1[2]]
            p2 = [1., 0., p1[2]]
            p3 = [0., 1., p1[2]]
        elif preset in ['xz', 'zx']:
            p1 = [0., p1[1], 0.]
            p2 = [1., p1[1], 0.]
            p3 = [0., p1[1], 1.]
        elif preset in ['yz', 'zy']:
            p1 = [p1[0], 0., 0.]
            p2 = [p1[0], 1., 0.]
            p3 = [p1[0], 0., 1.]
        elif preset in ['xy-middle', 'yx-middle']:
            p1 = [0., 0., 0.5]
            p2 = [1., 0., 0.5]
            p3 = [0., 1., 0.5]
        elif preset in ['xz-middle', 'zx-middle']:
            p1 = [0., 0.5, 0.]
            p2 = [1., 0.5, 0.]
            p3 = [0., 0.5, 1.]
        elif preset in ['yz-middle', 'zy-middle']:
            p1 = [0.5, 0., 0.]
            p2 = [0.5, 1., 0.]
            p3 = [0.5, 0., 1.]
        elif preset == "max_cross_middle":
            p3 = self.farthest_from_p(p1, arr_shape)
            middle = int(round((p1[2]+p3[2])/2, 0))
            p2 = [p3[0], p1[1], middle]
        elif preset == "max_cross_up":
            p3 = self.farthest_from_p(p1, arr_shape)
            p2 = [p3[0], p1[1], p3[2]]
        elif preset == "max_cross_down":
            p3 = self.farthest_from_p(p1, arr_shape)
            p2 = [p3[0], p1[1], p1[2]]
        else:
            raise ValueError('Preset not recognized')
        return p1, p2, p3


    def float2int_3points_decoder(self, p1, p2, p3, arr_shape):
        p_arr = [p1, p2, p3]
        int_p_arr = []
        for i in range(3):
            int_p = self.float2int_point_decoder(p_arr[i], arr_shape)
            int_p_arr.append(int_p)
        return int_p_arr
    

    def float2int_point_decoder(self, p, arr_shape):
        arr_max_idx = [x-1 for x in arr_shape]
        int_arr = []
        for i in range(3):
            if isinstance(p[i], float):
                x = int(round(p[i] * arr_max_idx[i], 0))
                int_arr.append(x)
            elif isinstance(p[i], int):
                int_arr.append(p[i])
            else:
                raise TypeError("p should be int or float type")
        return int_arr


    def p3_to_normal_vec(self, p1:list[int], p2:list[int], p3:list[int]):
        """
        Gets three points that spread the plane and return a normal vector of this plane
        """
        p12 = np.array(p2) - np.array(p1)
        p13 = np.array(p3) - np.array(p1)
        vec = np.cross(p12, p13)
        normal_vec = vec/np.linalg.norm(vec)
        return normal_vec


    def plane_equation(self, plane_point, plane_normal_vec):
        D = -np.dot(plane_normal_vec, plane_point)
        eq = plane_normal_vec.copy()
        eq = np.append(eq, D)
        return eq
    
    def dist_p_to_plane_VEC(self, p_vec, plane_equation):
        # works on vectors
        plane_norm_vec = plane_equation[0:3]
        D = plane_equation[3]
        dist_vec = np.abs(np.dot(p_vec, plane_norm_vec) + D)/np.linalg.norm(plane_norm_vec)
        return dist_vec


    def dist_p_to_plane(self, p, plane_equation):
        plane_norm_vec = plane_equation[0:3]
        D = plane_equation[3]
        dist = np.abs(np.dot(p, plane_norm_vec) + D)/np.linalg.norm(plane_norm_vec)
        return dist
    

    def dist_p_to_plane_by_norm_vec(self, p_out_plane, p_in_plane, plane_normal_vec):
        eq = self.plane_equation(p_in_plane, plane_normal_vec)
        dist = self.dist_p_to_plane(p_out_plane, eq)
        return dist
    
    def find_first_non_omit_z_idx(self, arr3d, x_idx, y_idx, plane_equation):
        A = plane_equation[0]
        B = plane_equation[1]
        C = plane_equation[2]
        D = plane_equation[3]
        z_column = arr3d[x_idx, y_idx]
        z_idx = None
        for i in range(len(z_column)):
            if A*x_idx + B*y_idx + C*i + D == 0:
                if z_column[i] not in self.omit:
                    z_idx = i
                    break
        return z_idx

    def fromObj3D_1(self, object3D:Object3D, p1=(0,0,0), p2=None, p3=None, preset="max_cross_middle", reset_val=0, min_dist=math.sqrt(2)/2):
        # slower vesion
        b = object3D.body
        b_result = b.copy()
        if preset is not None:
            p1, p2, p3 = self.preset_decoder(p1, preset, b.shape)
        p1, p2, p3 = self.float2int_3points_decoder(p1, p2, p3, b.shape)
        normal_vec = self.p3_to_normal_vec(p1, p2, p3)
        plane_equation = self.plane_equation(p1, normal_vec)
        sh = b.shape
        # --- this block is the difference between other fromObj3D functions ---
        for i in range(sh[0]):
            for j in range(sh[1]):
                for k in range(sh[2]):
                    particle = [i,j,k]
                    dist_from_plane = self.dist_p_to_plane(particle, plane_equation)
                    if dist_from_plane > min_dist:
                        b_result[i,j,k] = reset_val
        # ---
        self.rebuild_from_array(b_result)
        self.set_plane_points(p1, p2, p3)
        return self
    
    def fromObj3D_2(self, object3D:Object3D, p1=(0,0,0), p2=None, p3=None, preset="max_cross_middle", reset_val=0, min_dist=math.sqrt(2)/2):
        b = object3D.body
        b_result = b.copy()
        if preset is not None:
            p1, p2, p3 = self.preset_decoder(p1, preset, b.shape)
        p1, p2, p3 = self.float2int_3points_decoder(p1, p2, p3, b.shape)
        normal_vec = self.p3_to_normal_vec(p1, p2, p3)
        plane_equation = self.plane_equation(p1, normal_vec)
        sh = b.shape
        # --- this block is the difference between other fromObj3D functions ---
        reset_flag = np.array([self.dist_p_to_plane([i,j,k], plane_equation) > min_dist for i in range(sh[0]) for j in range(sh[1]) for k in range(sh[2])]).reshape(sh)
        b_result[reset_flag] = reset_val
        # ---
        self.rebuild_from_array(b_result)
        self.set_plane_points(p1, p2, p3)
        return self
    
    def fromObj3D_3(self, object3D:Object3D, p1=(0,0,0), p2=None, p3=None, preset="max_cross_middle", reset_val=0, min_dist=math.sqrt(2)/2):
        b = object3D.body
        b_result = b.copy()
        if preset is not None:
            p1, p2, p3 = self.preset_decoder(p1, preset, b.shape)
        p1, p2, p3 = self.float2int_3points_decoder(p1, p2, p3, b.shape)
        normal_vec = self.p3_to_normal_vec(p1, p2, p3)
        plane_equation = self.plane_equation(p1, normal_vec)
        sh = b.shape
        # --- this block is the difference between other fromObj3D functions ---
        check_reset_flag_fun = lambda i,j,k: self.dist_p_to_plane([i,j,k], plane_equation) > min_dist
        X, Y, Z = np.indices(b.shape)
        reset_flag_mtx = np.array(list(map(check_reset_flag_fun, X.flatten(), Y.flatten(), Z.flatten()))).reshape(sh)
        b_result[reset_flag_mtx] = reset_val
        # ---
        self.rebuild_from_array(b_result)
        self.set_plane_points(p1, p2, p3)
        return self
    
    def fromObj3D(self, object3D:Object3D, p1=(0,0,0), p2=None, p3=None, preset="max_cross_middle", reset_val=0, min_dist=math.sqrt(2)/2):
        b = object3D.body
        b_result = b.copy()
        if preset is not None:
            p1, p2, p3 = self.preset_decoder(p1, preset, b.shape)
        p1, p2, p3 = self.float2int_3points_decoder(p1, p2, p3, b.shape)
        normal_vec = self.p3_to_normal_vec(p1, p2, p3)
        plane_equation = self.plane_equation(p1, normal_vec)
        sh = b.shape
        # --- this block is the difference between other fromObj3D functions ---
        X, Y, Z = np.indices(b.shape)
        p_vec = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()])
        reset_flag_mtx = self.dist_p_to_plane_VEC(p_vec, plane_equation).reshape(sh) > min_dist
        b_result[reset_flag_mtx] = reset_val
        # ---
        self.rebuild_from_array(b_result)
        self.set_plane_points(p1, p2, p3)
        return self
    
    def fromObj3D_5(self, object3D:Object3D, p1=(0,0,0), p2=None, p3=None, preset="max_cross_middle", reset_val=0, min_dist=math.sqrt(2)/2):
        b = object3D.body
        b_result = b.copy()
        if preset is not None:
            p1, p2, p3 = self.preset_decoder(p1, preset, b.shape)
        p1, p2, p3 = self.float2int_3points_decoder(p1, p2, p3, b.shape)
        normal_vec = self.p3_to_normal_vec(p1, p2, p3)
        plane_equation = self.plane_equation(p1, normal_vec)
        sh = b.shape
        # --- this block is the difference between other fromObj3D functions ---
        check_reset_flag_fun = lambda i,j,k: self.dist_p_to_plane([i,j,k], plane_equation) > min_dist
        def mapper(X, Y, Z):
            return np.array(list(map(check_reset_flag_fun, X.flatten(), Y.flatten(), Z.flatten()))).reshape(sh)
        reset_flag_mtx = np.fromfunction(mapper, sh, dtype=int)
        b_result[reset_flag_mtx] = reset_val
        # ---
        self.rebuild_from_array(b_result)
        self.set_plane_points(p1, p2, p3)
        return self


    def fromObj3D_to_projection(self, object3D:Object3D, p1=(0,0,0), p2=None, p3=None, preset="max_cross_middle", reset_val=None):
        if reset_val is None:
            reset_val = self.reset_val
        b = object3D.body
        arr2d_result = np.zeros(b.shape[:2])
        if preset is not None:
            p1, p2, p3 = self.preset_decoder(p1, preset, b.shape)
        p1, p2, p3 = self.float2int_3points_decoder(p1, p2, p3, b.shape)
        normal_vec = self.p3_to_normal_vec(p1, p2, p3)
        plane_equation = self.plane_equation(p1, normal_vec)
        A = plane_equation[0]
        B = plane_equation[1]
        C = plane_equation[2]
        D = plane_equation[3]
        sh = b.shape
        for x_idx in range(sh[0]):
            for y_idx in range(sh[1]):

                if C != 0:
                    z_idx = -(A*x_idx + B*y_idx + D)/C
                else:
                    # xz/yz plane is perpendicular to xz plane
                    # here z_idx can become None
                    z_idx = self.find_first_non_omit_z_idx(b, x_idx, y_idx, plane_equation)
                    
                if z_idx is not None:
                    z_idx = int(round(z_idx, 0))
                    if (0 <= z_idx <= sh[2]-1):
                        arr2d_result[x_idx, y_idx] = b[x_idx, y_idx, z_idx]
                    else:
                        arr2d_result[x_idx, y_idx] = reset_val
                else:
                    arr2d_result[x_idx, y_idx] = reset_val
        if C == 0:
            print("C in plane equation is zero, used first finded z_idx.")
        b_result = arr2d_result.reshape(sh[0],sh[1], 1)
        self.rebuild_from_array(b_result)
        self.set_plane_points(p1, p2, p3)
        projection = Projection(arr = b_result)
        projection.reset_val = reset_val
        return projection
    

    def fromObj3D_byPlaneEq(self, object3D:Object3D, p1=(0,0,0), p2=None, p3=None, preset="max_cross_middle", reset_val=None):
        # faster method, but not accurate
        # especially in plane xz/yz it will be just projection on xy plane - 1d line
        if reset_val is None:
            reset_val = self.reset_val
        b = object3D.body
        arr3d_result = np.zeros(b.shape)
        if preset is not None:
            p1, p2, p3 = self.preset_decoder(p1, preset, b.shape)
        p1, p2, p3 = self.float2int_3points_decoder(p1, p2, p3, b.shape)
        normal_vec = self.p3_to_normal_vec(p1, p2, p3)
        plane_equation = self.plane_equation(p1, normal_vec)
        A = plane_equation[0]
        B = plane_equation[1]
        C = plane_equation[2]
        D = plane_equation[3]
        sh = b.shape
        for x_idx in range(sh[0]):
            for y_idx in range(sh[1]):

                if C != 0:
                    z_idx = -(A*x_idx + B*y_idx + D)/C
                else:
                    # xz/yz plane is perpendicular to xz plane
                    # here z_idx can become None
                    z_idx = self.find_first_non_omit_z_idx(b, x_idx, y_idx, plane_equation)
                    
                if z_idx is not None:
                    z_idx = int(round(z_idx, 0))
                    if (0 <= z_idx <= sh[2]-1):
                        arr3d_result[x_idx, y_idx, z_idx] = b[x_idx, y_idx, z_idx]
                    else:
                        arr3d_result[x_idx, y_idx, z_idx] = reset_val
                else:
                    arr3d_result[x_idx, y_idx, z_idx] = reset_val
        if C == 0:
            print("C in plane equation is zero, used first finded z_idx.")
        self.rebuild_from_array(arr3d_result)
        self.set_plane_points(p1, p2, p3)
        return self