from Object3D import Object3D
import numpy as np
import pandas as pd
from PIL import ImageColor

class ColorPointDF():

    threshold_const = 0.2
    threshold_quantile = 0.2
    use_threshold = "quantile"

    def __init__(self):
        pass

    @staticmethod
    def process_df_by_color_scheme(df: pd.DataFrame, color_scheme, drop_values):

        # Drop values (for example 0.0)
        if drop_values is not None:
            for drop_val in drop_values:
                df = df.loc[df["value"] == drop_val]


        if color_scheme == "threshold":

            # choose threshold
            if ColorPointDF.use_threshold == "const":
                threshold = ColorPointDF.threshold_const
            elif ColorPointDF.use_threshold == "quantile":
                threshold = df["value"].quantile(ColorPointDF.threshold_quantile)
            else:
                raise ValueError("wrong color_scheme value")
            
            # filter out values below threshold
            df = df.loc[df["value"] >= threshold]

            # set colors
            rgb = ImageColor.getrgb("white")
            df['R'] = rgb[0]
            df['G'] = rgb[1]
            df['B'] = rgb[2]



        return df









    @staticmethod
    def from_Object3d(object3d: Object3D, color_scheme, drop_values=None):
        X, Y, Z = np.indices(object3d.body.shape)
        df = pd.DataFrame({'value': object3d.body.flatten(), 'x_idx': X.flatten(), 'y_idx': Y.flatten(), 'z_idx': Z.flatten()})
        df = ColorPointDF.process_df_by_color_scheme(df, color_scheme, drop_values)
        return df

        