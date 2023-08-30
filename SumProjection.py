from Object3D import Object3D
from Projection import Projection
from Space3dTools import Space3dTools
import numpy as np

class SumProjection():
    def __init__(self):
        pass

    def x_high(self, object3D:Object3D):
        ax = 0
        sh = object3D.body.shape
        proj_arr2d = np.sum(object3D.body, axis=ax)
        # transformations
        proj_arr2d = self.rotate_left(proj_arr2d)
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)

    def x_low(self, object3D:Object3D):
        ax = 0
        sh = object3D.body.shape
        proj_arr2d = np.sum(object3D.body, axis=ax)
        # transformations
        proj_arr2d = self.rotate_left(proj_arr2d)
        proj_arr2d = self.inverese_vertical(proj_arr2d)
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)

    def y_high(self, object3D:Object3D):
        ax = 1
        sh = object3D.body.shape
        proj_arr2d = np.sum(object3D.body, axis=ax)
        # transformations
        proj_arr2d = self.rotate_left(proj_arr2d)
        proj_arr2d = self.inverese_vertical(proj_arr2d)
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)

    def y_low(self, object3D:Object3D):
        ax = 1
        sh = object3D.body.shape
        proj_arr2d = np.sum(object3D.body, axis=ax)
        # transformations
        proj_arr2d = self.rotate_left(proj_arr2d)
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)

    def z_high(self, object3D:Object3D):
        ax = 2
        sh = object3D.body.shape
        proj_arr2d = np.sum(object3D.body, axis=ax)
        # no need for transformations
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)

    def z_low(self, object3D:Object3D):
        ax = 2
        sh = object3D.body.shape
        proj_arr2d = np.sum(object3D.body, axis=ax)
        # transformations
        proj_arr2d = self.inverese_horizontal(proj_arr2d)
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)
    


    # TRANSFORMATIONS

    def rotate_left(self, arr2d: np.ndarray):
        arr2d = self.flip_axis(arr2d, ax1=0, ax2=1)
        arr2d = self.inverese_horizontal(arr2d)
        return arr2d

    def rotate_right(self, arr2d: np.ndarray):
        arr2d = self.flip_axis(arr2d, ax1=0, ax2=1)
        arr2d = self.inverese_vertical(arr2d)
        return arr2d

    def inverese_vertical(self, arr2d: np.ndarray):
        arr2d = np.flip(arr2d, axis=1)
        return arr2d

    def inverese_horizontal(self, arr2d: np.ndarray):
        arr2d = np.flip(arr2d, axis=0)
        return arr2d

    def flip_axis(self, arr2d: np.ndarray, ax1, ax2):
        arr2d = np.swapaxes(arr2d, axis1=ax1, axis2=ax2)
        return arr2d
        