from Object3D import Object3D
import numpy as np
import PIL
from PIL import ImageColor, Image
import os
import math

class Slice(Object3D):
    def __init__(self):
        self.p1 = None
        self.p2 = None
        self.p3 = None


    def points_dist(self, p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)


    def farthest_from_p(self, p, arr_shape):
        c0 = [0,0,0]
        c1 = [0,0,arr_shape[2]]
        c2 = [0,arr_shape[1],0]
        c3 = [0,arr_shape[1],arr_shape[2]]
        c4 = [arr_shape[0],0,0]
        c5 = [arr_shape[0],0,arr_shape[2]]
        c6 = [arr_shape[0],arr_shape[1],0]
        c7 = [arr_shape[0],arr_shape[1],arr_shape[2]]
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
        p1 = p.copy()
        if preset in ['xy', 'yx']:
            p1 = [0, 0, p1[2]]
            p2 = [1, 0, p1[2]]
            p3 = [0, 1, p1[2]]
        elif preset in ['xz', 'zx']:
            p1 = [0, p1[1], 0]
            p2 = [1, p1[1], 0]
            p3 = [0, p1[1], 1]
        elif preset in ['yz', 'zy']:
            p1 = [p1[0], 0, 0]
            p2 = [p1[0], 1, 0]
            p3 = [p1[0], 0, 1]
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


    def float2int_point_decoder(self, p1, p2, p3, arr_shape):
        p_arr = [p1, p2, p3]
        int_p_arr = []
        for i in range(3):
            if isinstance(p_arr[i], float):
                x = round(p_arr[i] * arr_shape[i], 0)
                int_p_arr.append(x)
            else:
                int_p_arr.append(p_arr[i])
        return int_p_arr


    def p3_to_normal_vec(self, p1, p2, p3):
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
        eq.append(D)
        return eq


    def dist_p_to_plane(self, p, plane_equation):
        plane_norm_vec = plane_equation[0:3]
        D = plane_equation[3]
        dist = np.abs(np.dot(p, plane_norm_vec) + D)/np.linalg.norm(plane_norm_vec)
        return dist


    def fromObj3D(self, object3D:Object3D, p1=(0,0,0), p2=None, p3=None, preset="max_cross_middle"):
        b = object3D.body
        if preset is not None:
            p1, p2, p3 = self.preset_decoder(p1, preset, b.shape)
        p1, p2, p3 = self.float2int_point_decoder(p1, p2, p3, b.shape)
        normal_vec = self.p3_to_normal_vec(p1, p2, p3)
        sh = b.shape
        for i in range(sh[0]):
            for j in range(sh[1]):
                for k in range(sh[2]):
                    particle = [i,j,k]
                    plane_equation = self.plane_equation(p1, normal_vec)
                    dist_from_plane = self.dist_p_to_plane(particle, plane_equation)


    
    
















'''


    # NEEDS_REFACTOR
    def slice_arr3p(arr, p1=(0,0,0), p2=None, p3=None, clip_idx=False):
        if p3 is None:
            p3 = (arr.shape[0]-1, arr.shape[1]-1, arr.shape[2]-1)
        if p2 is None:
            p2 = (p1[0], (p1[1]+p3[1])//2, p3[2])

        normal_vec = p3_to_normal_vec(p1, p2, p3)
        n = normal_vec

        depth_cords = np.arange(p1[0], p3[0]+1)
        height_cords = np.arange(p1[1], p3[1]+1)
        if clip_idx:
            depth_cords = np.clip(depth_cords, a_min=0, a_max=(arr.shape[0]-1))
            height_cords = np.clip(height_cords, a_min=0, a_max=(arr.shape[1]-1))
        z_vals = np.zeros((len(depth_cords),len(height_cords)))

        # sampling
        for i in range(len(depth_cords)):
            for j in range(len(height_cords)):
                x = depth_cords[i]
                y = height_cords[j]

                ''''''
                z = (-(n[0]*(x-p1[0]) + n[1]*(y-p1[1]))/n[2]) + p1[2] # doesn't work (but it should...)
                z = (-(n[1]*(x-p1[1]) + n[2]*(y-p1[2]))/n[0]) + p1[0] # doesn't work
                z = (-(n[1]*(x-p1[1]) + n[0]*(y-p1[0]))/n[2]) + p1[2] # doesn't work
                z = (-(n[2]*(x-p1[2]) + n[0]*(y-p1[0]))/n[1]) + p1[1] # works
                z = (-(n[2]*(x-p1[2]) + n[1]*(y-p1[1]))/n[0]) + p1[0] # doesn't work
                ''''''
                z = (-(n[0]*(x-p1[0]) + n[2]*(y-p1[2]))/n[1]) + p1[1] # works

                z_vals[i,j] = z
        width_cords = np.around(z_vals).astype(int)
        if clip_idx:
            width_cords = np.clip(width_cords, a_min=0, a_max=(arr.shape[2]-1))

        # NEEDS_REFACTOR
        print_debug = False
        if print_debug:
            print(depth_cords)
            print(height_cords)
            print(width_cords)
            print(p1)
            print(p2)
            print(p3)
            print(p3_to_normal_vec(p1,p2,p3))
            for val in width_cords.reshape(-1):
                if val > 99:
                    #print(val)
                    pass

        out_arr = np.zeros((len(depth_cords),len(height_cords)))
        for i in range(out_arr.shape[0]):
            for j in range(out_arr.shape[1]):
                out_arr[i,j] = arr[depth_cords[i], height_cords[j], width_cords[i,j]]
        return out_arr.astype(int)


'''