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
        proj_arr2d = np.sum(object3D.body, axis=ax) / sh[ax]
        # FLIP TO ^Y ->X
        # no need to flip
        # no need to change axis
        # FLIP TO \/X ->Y
        proj_arr2d = Space3dTools.change_axis2print_mode(proj_arr2d)
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)

    def x_low(self, object3D:Object3D):
        ax = 0
        sh = object3D.body.shape
        proj_arr2d = np.sum(object3D.body, axis=ax) / sh[ax]
        # FLIP TO ^Y ->X
        proj_arr2d = np.flip(proj_arr2d, axis=0)
        # no need to change axis
        # FLIP TO \/X ->Y
        proj_arr2d = Space3dTools.change_axis2print_mode(proj_arr2d)
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)

    def y_high(self, object3D:Object3D):
        ax = 1
        sh = object3D.body.shape
        proj_arr2d = np.sum(object3D.body, axis=ax) / sh[ax]
        # FLIP TO ^Y ->X
        proj_arr2d = np.flip(proj_arr2d, axis=0)
        # no need to change axis
        # FLIP TO \/X ->Y
        proj_arr2d = Space3dTools.change_axis2print_mode(proj_arr2d)
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)

    def y_low(self, object3D:Object3D):
        ax = 1
        sh = object3D.body.shape
        proj_arr2d = np.sum(object3D.body, axis=ax) / sh[ax]
        # FLIP TO ^Y ->X
        # no need to flip
        # no need to change axis
        # FLIP TO \/X ->Y
        proj_arr2d = Space3dTools.change_axis2print_mode(proj_arr2d)
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)

    def z_high(self, object3D:Object3D):
        ax = 2
        sh = object3D.body.shape
        proj_arr2d = np.sum(object3D.body, axis=ax) / sh[ax]
        # FLIP TO ^Y ->X
        # no need to flip
        # no need to change axis
        # FLIP TO \/X ->Y
        proj_arr2d = Space3dTools.change_axis2print_mode(proj_arr2d)
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)

    def z_low(self, object3D:Object3D):
        ax = 2
        sh = object3D.body.shape
        proj_arr2d = np.sum(object3D.body, axis=ax) / sh[ax]
        # FLIP TO ^Y ->X
        proj_arr2d = np.flip(proj_arr2d, axis=0)
        # no need to change axis
        # FLIP TO \/X ->Y
        proj_arr2d = Space3dTools.change_axis2print_mode(proj_arr2d)
        # reshape to 3d object plane (floor)
        sh2 = proj_arr2d.shape
        proj_arr3d = proj_arr2d.reshape(sh2[0], sh2[1], 1)
        return Projection(arr=proj_arr3d)
        