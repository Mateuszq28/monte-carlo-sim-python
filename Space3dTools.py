import math

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

