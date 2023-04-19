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


    def p3_to_normal_vec(self, p1:List[int], p2:List[int], p3:List[int]):
        """
        Gets three points that spread the plane and return a normal vector of this plane
        """
        p12 = np.array(p2) - np.array(p1)
        p13 = np.array(p3) - np.array(p1)
        vec = np.cross(p13, p12)
        normal_vec = vec/np.linalg.norm(vec)
        return normal_vec


    def plane_equation(self, plane_point, plane_normal_vec):
        D = -np.dot(plane_normal_vec, plane_point)
        eq = plane_normal_vec.copy()
        eq = np.append(eq, D)
        return eq


    def dist_p_to_plane(self, p, plane_equation):
        plane_norm_vec = plane_equation[0:3]
        D = plane_equation[3]
        dist = np.abs(np.dot(p, plane_norm_vec) + D)/np.linalg.norm(plane_norm_vec)
        return dist
    

    def dist_p_to_plane_by_norm_vec(self, p_out_plane, p_in_plane, plane_normal_vec):
        eq = self.plane_equation(p_in_plane, plane_normal_vec)
        dist = self.dist_p_to_plane(p_out_plane, eq)
        return dist
    

    def fromObj3D(self, object3D:Object3D, p1=(0,0,0), p2=None, p3=None, preset="max_cross_middle", reset_val=0, min_dist=math.sqrt(2)):
        b = object3D.body
        b_result = b.copy()
        if preset is not None:
            p1, p2, p3 = self.preset_decoder(p1, preset, b.shape)
        p1, p2, p3 = self.float2int_3points_decoder(p1, p2, p3, b.shape)
        normal_vec = self.p3_to_normal_vec(p1, p2, p3)
        plane_equation = self.plane_equation(p1, normal_vec)
        sh = b.shape
        for i in range(sh[0]):
            for j in range(sh[1]):
                for k in range(sh[2]):
                    particle = [i,j,k]
                    dist_from_plane = self.dist_p_to_plane(particle, plane_equation)
                    if dist_from_plane > min_dist:
                        b_result[i,j,k] = reset_val
        self.rebuild_from_array(b_result)
        self.set_plane_points(p1, p2, p3)
        return self


    def fromObj3D_to_projection(self, object3D:Object3D, p1=(0,0,0), p2=None, p3=None, preset="max_cross_middle", reset_val=0):
        b = object3D.body
        arr2d_result = np.array(b.shape[:2])
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
                z_idx = -(A*x_idx + B*y_idx + D)/C
                z_idx = int(round(z_idx, 0))
                if (0 <= z_idx <= sh[2]-1):
                    arr2d_result[x_idx, y_idx] = b[x_idx, y_idx, z_idx]
                else:
                    arr2d_result[x_idx, y_idx] = reset_val
        b_result = arr2d_result.reshape(sh[0],sh[1], 1)
        self.rebuild_from_array(b_result)
        self.set_plane_points(p1, p2, p3)
        projection = Projection(arr = b_result)
        projection.reset_val = reset_val
        return projection