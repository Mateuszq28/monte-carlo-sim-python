import pandas as pd
from ProjectionResultRecordsDF import ProjectionResultRecordsDF

class ProjectionArrowsDF():

    def __init__(self):
        pass

    def x_high(self, connect_lines: pd.DataFrame, input_shape, set_z_as_flat_axis=True):
        PRR = ProjectionResultRecordsDF()
        empty_df = pd.DataFrame({"x_idx": [0], "y_idx": [0], "z_idx": [0]})
        _, flat_axis, proj_connect_lines = PRR.throw(empty_df, input_shape, 0, -1, sum_axis=False, sort=False, reset_colors=None, connect_lines=connect_lines)
        if set_z_as_flat_axis:
            flat_z_connect_lines, image_shape = self.set_z_as_flat_axis(proj_connect_lines, flat_axis, input_shape, post_transform=True, transform_preset="x_high")
            out1 = flat_z_connect_lines
            out2 = flat_axis
            out3 = image_shape
        else:
            out1 = proj_connect_lines
            out2 = flat_axis
            out3 = None
        return out1, out2, out3

    def x_low(self, connect_lines: pd.DataFrame, input_shape, set_z_as_flat_axis=True):
        PRR = ProjectionResultRecordsDF()
        empty_df = pd.DataFrame({"x_idx": [0], "y_idx": [0], "z_idx": [0]})
        _, flat_axis, proj_connect_lines = PRR.throw(empty_df, input_shape, 0, 1, sum_axis=False, sort=False, reset_colors=None, connect_lines=connect_lines)
        if set_z_as_flat_axis:
            flat_z_connect_lines, image_shape = self.set_z_as_flat_axis(proj_connect_lines, flat_axis, input_shape, post_transform=True, transform_preset="x_low")
            out1 = flat_z_connect_lines
            out2 = flat_axis
            out3 = image_shape
        else:
            out1 = proj_connect_lines
            out2 = flat_axis
            out3 = None
        return out1, out2, out3

    def y_high(self, connect_lines: pd.DataFrame, input_shape, set_z_as_flat_axis=True):
        PRR = ProjectionResultRecordsDF()
        empty_df = pd.DataFrame({"x_idx": [0], "y_idx": [0], "z_idx": [0]})
        _, flat_axis, proj_connect_lines = PRR.throw(empty_df, input_shape, 1, -1, sum_axis=False, sort=False, reset_colors=None, connect_lines=connect_lines)
        if set_z_as_flat_axis:
            flat_z_connect_lines, image_shape = self.set_z_as_flat_axis(proj_connect_lines, flat_axis, input_shape, post_transform=True, transform_preset="y_high")
            out1 = flat_z_connect_lines
            out2 = flat_axis
            out3 = image_shape
        else:
            out1 = proj_connect_lines
            out2 = flat_axis
            out3 = None
        return out1, out2, out3

    def y_low(self, connect_lines: pd.DataFrame, input_shape, set_z_as_flat_axis=True):
        PRR = ProjectionResultRecordsDF()
        empty_df = pd.DataFrame({"x_idx": [0], "y_idx": [0], "z_idx": [0]})
        _, flat_axis, proj_connect_lines = PRR.throw(empty_df, input_shape, 1, 1, sum_axis=False, sort=False, reset_colors=None, connect_lines=connect_lines)
        if set_z_as_flat_axis:
            flat_z_connect_lines, image_shape = self.set_z_as_flat_axis(proj_connect_lines, flat_axis, input_shape, post_transform=True, transform_preset="y_low")
            out1 = flat_z_connect_lines
            out2 = flat_axis
            out3 = image_shape
        else:
            out1 = proj_connect_lines
            out2 = flat_axis
            out3 = None
        return out1, out2, out3

    def z_high(self, connect_lines: pd.DataFrame, input_shape, set_z_as_flat_axis=True):
        PRR = ProjectionResultRecordsDF()
        empty_df = pd.DataFrame({"x_idx": [0], "y_idx": [0], "z_idx": [0]})
        _, flat_axis, proj_connect_lines = PRR.throw(empty_df, input_shape, 2, -1, sum_axis=False, sort=False, reset_colors=None, connect_lines=connect_lines)
        if set_z_as_flat_axis:
            flat_z_connect_lines, image_shape = self.set_z_as_flat_axis(proj_connect_lines, flat_axis, input_shape, post_transform=True, transform_preset="z_high")
            out1 = flat_z_connect_lines
            out2 = flat_axis
            out3 = image_shape
        else:
            out1 = proj_connect_lines
            out2 = flat_axis
            out3 = None
        return out1, out2, out3

    def z_low(self, connect_lines: pd.DataFrame, input_shape, set_z_as_flat_axis=True):
        PRR = ProjectionResultRecordsDF()
        empty_df = pd.DataFrame({"x_idx": [0], "y_idx": [0], "z_idx": [0]})
        _, flat_axis, proj_connect_lines = PRR.throw(empty_df, input_shape, 2, 1, sum_axis=False, sort=False, reset_colors=None, connect_lines=connect_lines)
        if set_z_as_flat_axis:
            flat_z_connect_lines, image_shape = self.set_z_as_flat_axis(proj_connect_lines, flat_axis, input_shape, post_transform=True, transform_preset="z_low")
            out1 = flat_z_connect_lines
            out2 = flat_axis
            out3 = image_shape
        else:
            out1 = proj_connect_lines
            out2 = flat_axis
            out3 = None
        return out1, out2, out3
    
    def set_z_as_flat_axis(self, connect_lines, flataxis, input_shape, post_transform=True, transform_preset=None):
        PRR = ProjectionResultRecordsDF()
        empty_df = pd.DataFrame({"x_idx": [0], "y_idx": [0], "z_idx": [0]})
        _, image_shape, flat_z_connect_lines = PRR.set_z_as_flat_axis(empty_df, flataxis, input_shape, post_transform=post_transform, transform_preset=transform_preset, sort=False, reset_colors=None, connect_lines=connect_lines)
        return flat_z_connect_lines, image_shape