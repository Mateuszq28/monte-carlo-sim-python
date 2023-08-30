from Object3D import Object3D
import numpy as np
from Print import Print
import os

class Projection(Object3D):
    def __init__(self, x=100, y=100, z=100, arr=None):
        super().__init__(x, y, z, arr)
        self.omit = [0, 0.0]
        self.reset_val = 0

    def x_high(self, object3D:Object3D):
        return self.throw(object3D, 0, -1)

    def x_low(self, object3D:Object3D):
        return self.throw(object3D, 0, 1)

    def y_high(self, object3D:Object3D):
        return self.throw(object3D, 1, -1)

    def y_low(self, object3D:Object3D):
        return self.throw(object3D, 1, 1)

    def z_high(self, object3D:Object3D):
        return self.throw(object3D, 2, -1)

    def z_low(self, object3D:Object3D):
        return self.throw(object3D, 2, 1)

    def throw(self, object3D:Object3D, axis, xray):
        """
        The function will take first value from object3D.body, which is different then values in self.omit, seen perpendicularly to axis.
        :param axis: observer's axis
        :param xray: If 1, observer is looking at the body from the start of the axis (axis[0]). If -1, observer is looking at the body from the end of the axis (axis[-1]).

        """
        b = object3D.body
        sh = b.shape
        ax_lvl_list = [0,1,2]
        ax_lvl_list.remove(axis)
        proj_ax_len = sh[axis]
        lvl_ax1_len = sh[ax_lvl_list[0]]
        lvl_ax2_len = sh[ax_lvl_list[1]]
        # array with flag if value was already sampled from body
        is_sampled = np.full((lvl_ax1_len, lvl_ax2_len), False)
        # array with values sampled from body (projected on the plane)
        samples = np.full((lvl_ax1_len, lvl_ax2_len), self.reset_val)
        if xray == 1:
            proj_ax_range = range(proj_ax_len)
        elif xray == -1:
            proj_ax_range = range(proj_ax_len-1, -1, -1)
        else:
            raise ValueError("xray value must be 1 or -1")
        for i in proj_ax_range:
            for j in range(lvl_ax1_len):
                for k in range(lvl_ax2_len):
                    if not is_sampled[j,k]:
                        if axis == 0:
                            b_val = b[i,j,k]
                        elif axis == 1:
                            b_val = b[j,i,k]
                        elif axis == 2:
                            b_val = b[j,k,i]
                        else:
                            b_val = None
                            ValueError("axis must be in {0,1,2}")
                        if b_val not in self.omit:
                            is_sampled[j,k] = True
                            samples[j,k] = b_val
        samples3d = samples.reshape(lvl_ax1_len,lvl_ax2_len,1)
        self.rebuild_from_array(samples3d)
        return self
    
    def save_png(self, dir=None, filename="projection.png", color_scheme="threshold", connect_lines=None):
        if dir is None:
            dir = os.path.join("slice_img", "projection_img")
        Print().z_high(self, dir, filename, color_scheme, connect_lines)

                    
        



