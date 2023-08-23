from Object3D import Object3D
import numpy as np
import pandas as pd
from PIL import ImageColor
import json

class ColorPointDF():

    threshold_const = 0.2
    threshold_quantile = 0.2
    use_threshold = "quantile"
    loop_color_names = ['green', 'yellow', 'orange', 'red', 'purple', 'blue', 'pink', '#339933', '#FF3366', '#CC0066', '#99FFCC', '#3366FF', '#0000CC']


    def __init__(self):
        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)

    def process_df_by_color_scheme(self, df: pd.DataFrame, color_scheme, drop_values):

        # Drop values (for example 0.0)
        if drop_values is not None:
            for drop_val in drop_values:
                df = df.loc[df["value"] != drop_val]


        if color_scheme == "threshold":

            # choose threshold
            if self.use_threshold == "const":
                threshold = self.threshold_const * self.volume_per_bin
            elif self.use_threshold == "quantile":
                threshold = df["value"].quantile(self.threshold_quantile)
            else:
                raise ValueError("wrong color_scheme value")
            
            # filter out values below threshold
            df = df.loc[df["value"] >= threshold]

            # set DF colors
            rgb = ImageColor.getrgb("white")
            df['R'] = rgb[0]
            df['G'] = rgb[1]
            df['B'] = rgb[2]
            # alpha channel
            df['A'] = 255

        elif color_scheme == "loop":

            # 1. Preparing dict for translating vals in DF into rgb color
            color_names = self.loop_color_names.copy()
            uniq_vals = pd.unique(df['value'])
            colors_len = len(color_names)
            uniq_len = len(uniq_vals)
            if colors_len > uniq_len:
                color_names = color_names[0:uniq_len]
            else:
                # repeat colors
                for i in range(uniq_len - colors_len):
                    color_names.append(color_names[i % colors_len])

            # make dictionary for changing DF value fields into rgb colors
            colors_rgb = [ImageColor.getrgb(c) for c in color_names]
            trans_color = dict(zip(uniq_vals, colors_rgb))

            # 2. set DF colors
            rgb = [trans_color[val] for val in df["value"].values]
            df.insert(len(df.columns), "R", [val[0] for val in rgb], True)
            df.insert(len(df.columns), "G", [val[1] for val in rgb], True)
            df.insert(len(df.columns), "B", [val[2] for val in rgb], True)
            # alpha channel
            # df['A'] = 255.0
            df.insert(len(df.columns), "A", [255 for _ in rgb], True)
                    










        return df









    def from_Object3d(self, object3d: Object3D, color_scheme, drop_values=None):
        X, Y, Z = np.indices(object3d.body.shape)
        df = pd.DataFrame({'value': object3d.body.flatten(), 'x_idx': X.flatten(), 'y_idx': Y.flatten(), 'z_idx': Z.flatten()})
        df = self.process_df_by_color_scheme(df, color_scheme, drop_values)
        return df
    

    def from_arr2d(self, arr2d, color_scheme, drop_values=None):
        X, Y = np.indices(arr2d.shape)
        df = pd.DataFrame({'value': arr2d.flatten(), 'x_idx': X.flatten(), 'y_idx': Y.flatten()})
        df = self.process_df_by_color_scheme(df, color_scheme, drop_values)
        return df

        