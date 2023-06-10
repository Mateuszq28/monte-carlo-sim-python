import math
import numpy as np

class Space3dTools():
    def __init__(self):
        pass

    @staticmethod
    def spherical2cartesian(R, theta, phi):
        x = R * math.sin(theta) * math.cos(phi)
        y = R * math.sin(theta) * math.sin(phi)
        z = R * math.cos(theta)
        return x, y, z
    
    @staticmethod
    def cartesian2spherical(x, y, z):
        R = math.sqrt(x**2 + y**2 + z**2)
        r = math.sqrt(x**2 + y**2)
        if R != 0:
            theta = math.acos(z/R)
            if r != 0:
                phi = math.acos(x/r)
            else:
                phi = 0
        else:
            theta = 0
            phi = 0
        return R, phi, theta
    
    @staticmethod
    def cart_vec_norm(x, y, z):
        R = math.sqrt(x**2 + y**2 + z**2)
        xn = x/R
        yn = y/R
        zn = z/R
        return xn, yn, zn
    
    @staticmethod
    def reflect_vector(incident_vec, normal_vec):
        # https://en.wikipedia.org/wiki/Specular_reflection
        id = np.array(incident_vec)
        id = id / np.linalg.norm(id)
        n = np.array(normal_vec)
        n = n / np.linalg.norm(n)
        reflected = id - 2*n * np.dot(n,id)
        return reflected.tolist()
    
    @staticmethod
    def negative_vector(vec):
        return [-val for val in vec]
    
    @staticmethod
    def angle_between_vectors(vec1, vec2):
        a = np.array(vec1)
        b = np.array(vec2)
        alfa = math.acos(np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        return alfa
    
    @staticmethod
    def refraction_vec(incident_vec, normal_vec, n1, n2):
        # https://en.wikipedia.org/wiki/Snell%27s_law
        # https://stackoverflow.com/questions/29758545/how-to-find-refraction-vector-from-incoming-vector-and-surface-normal
        l = np.array(incident_vec)
        l = l / np.linalg.norm(l)
        n = np.array(normal_vec)
        n = n / np.linalg.norm(n)
        r = n1/n2
        c = -np.dot(n,l)
        refraction = r*l + (r*c - math.sqrt(1 - r**2 * (1 - c**2))) * n
        return refraction.tolist()
    
    @staticmethod
    def internal_reflectance(theta1, theta2):
        # from Chapter 5 5.3.3.2, formula 5.36
        # Monte Carlo Modeling of Light Transport in Tissue (Steady State and Time of Flight)
        t1 = theta1
        t2 = theta2
        temp1 = (math.sin(t1)*math.cos(t2) - math.cos(t1)*math.sin(t2))**2/2
        temp2 = (math.cos(t1)*math.cos(t2) + math.sin(t1)*math.sin(t2))**2 + (math.cos(t1)*math.cos(t2) - math.sin(t1)*math.sin(t2))**2
        temp3 = (math.sin(t1)*math.cos(t2) + math.cos(t1)*math.sin(t2))**2
        temp4 = (math.cos(t1)*math.cos(t2) + math.sin(t1)*math.sin(t2))**2
        R = temp1 * temp2 / (temp3 * temp4)
        return R
    








    @staticmethod
    def p3_to_normal_vec(p1, p2, p3):
        """
        Gets three points that spread the plane and return a normal vector of this plane
        """
        p12 = np.array(p2) - np.array(p1)
        p13 = np.array(p3) - np.array(p1)
        vec = np.cross(p12, p13)
        normal_vec = vec/np.linalg.norm(vec)
        return normal_vec.tolist()

    @staticmethod
    def plane_equation(plane_point, plane_normal_vec):
        D = -np.dot(plane_normal_vec, plane_point)
        eq = plane_normal_vec.copy()
        eq.append(D)
        return eq
    
    @staticmethod
    def dist_p_to_plane_VEC(p_vec, plane_equation):
        # works on vectors
        plane_norm_vec = plane_equation[0:3]
        D = plane_equation[3]
        dist_vec = np.abs(np.dot(p_vec, plane_norm_vec) + D)/np.linalg.norm(plane_norm_vec)
        return dist_vec

    @staticmethod
    def dist_p_to_plane(p, plane_equation):
        plane_norm_vec = plane_equation[0:3]
        D = plane_equation[3]
        dist = np.abs(np.dot(p, plane_norm_vec) + D)/np.linalg.norm(plane_norm_vec)
        return dist
    
    @staticmethod
    def dist_p_to_plane_by_norm_vec(p_out_plane, p_in_plane, plane_normal_vec):
        eq = Space3dTools.plane_equation(p_in_plane, plane_normal_vec)
        dist = Space3dTools.dist_p_to_plane(p_out_plane, eq)
        return dist