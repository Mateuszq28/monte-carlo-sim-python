from Object3D import Object3D
import numpy as np
import pandas as pd
import colorsys
from PIL import ImageColor
import json
from FeatureSampling import MyRandom

class ColorPointDF():

    threshold_const = 0.2
    threshold_quantile = 0.0
    use_threshold = "quantile"
    palette_1 = ['#C0392B', '#E74C3C', '#9B59B6', '#8E44AD', '#2980B9', '#3498DB', '#1ABC9C', '#16A085', '#27AE60', '#2ECC71', '#F1C40F', '#F39C12', '#E67E22', '#D35400', '#ECF0F1', '#BDC3C7', '#95A5A6', '#7F8C8D', '#34495E', '#2C3E50']
    palette_2 = ['green', 'yellow', 'orange', 'red', 'purple', 'blue', 'pink', '#339933', '#FF3366', '#CC0066', '#99FFCC', '#3366FF', '#0000CC']


    def __init__(self):
        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)
        # set default loop color list
        # self.loop_color_names = self.palette_2
        self.loop_color_names = self.create_palette(100)

    def create_palette(self, num_of_colors):
        hue = np.linspace(0.0, 1.0, num=num_of_colors, endpoint=True)
        rgb_color = [colorsys.hsv_to_rgb(h, 1.0, 1.0) for h in hue]
        rgb_color_255 = [[round(val * 255.0) for val in rgb] for rgb in rgb_color]
        hex_color = [self.rgb_to_hex(rgb) for rgb in rgb_color_255]
        return hex_color

    def rgb_to_hex(self, rgb):
        r, g, b = rgb
        return "#" + ('%02x%02x%02x' % (r, g, b)).upper()



    def process_df_by_color_scheme(self, df: pd.DataFrame, color_scheme, drop_values):

        # Drop values (for example 0.0)
        if drop_values is not None:
            df = df[~df["value"].isin(drop_values)]


        if color_scheme == "threshold":

            # choose threshold
            if self.use_threshold == "const":
                bins_per_1_cm = self.config["bins_per_1_cm"] # [N/cm]
                volume_per_bin = (1/bins_per_1_cm)**3
                threshold = self.threshold_const * volume_per_bin
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
                    
        elif color_scheme == "solid":

            other_uniq_vals = pd.unique(df['value']).tolist()

            # get solid colors dict from config
            solid_color_dict = dict()
            for key, value in self.config["tissue_properties"].items():
                solid_color_dict[key] = ImageColor.getrgb(value["print color"])
                solid_color_dict[float(key)] = ImageColor.getrgb(value["print color"])
                if key in other_uniq_vals:
                    other_uniq_vals.remove(key)

            # get loop colors dict for not specified labels in config
            color_names = self.loop_color_names.copy()
            colors_len = len(color_names)
            uniq_len = len(other_uniq_vals)
            if colors_len > uniq_len:
                color_names = color_names[0:uniq_len]
            else:
                # repeat colors
                for i in range(uniq_len - colors_len):
                    color_names.append(color_names[i % colors_len])

            # make dictionary for changing DF value fields into rgb colors
            colors_rgb = [ImageColor.getrgb(c) for c in color_names]
            trans_color = dict(zip(other_uniq_vals, colors_rgb))
            trans_color.update(solid_color_dict)

            # 2. set DF colors
            rgb = [trans_color[val] for val in df["value"].values]
            df.insert(len(df.columns), "R", [val[0] for val in rgb], True)
            df.insert(len(df.columns), "G", [val[1] for val in rgb], True)
            df.insert(len(df.columns), "B", [val[2] for val in rgb], True)
            # alpha channel
            # df['A'] = 255.0
            df.insert(len(df.columns), "A", [255 for _ in rgb], True)

        elif color_scheme == "photonwise":

            if "photon_id" not in df.columns:
                raise ValueError("df must have photon_id column")
            
            uniq_photon_id = pd.unique(df['photon_id'])
            rnd = MyRandom()
            colors = [[rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)] for _ in range(len(uniq_photon_id))]
            # id to color translator (dict)
            trans_color = dict(zip(uniq_photon_id, colors))
            # treanslate colors
            rgb = [trans_color[val] for val in df["photon_id"].values]
            # insert R, G, B columns
            df.insert(len(df.columns), "R", [val[0] for val in rgb], True)
            df.insert(len(df.columns), "G", [val[1] for val in rgb], True)
            df.insert(len(df.columns), "B", [val[2] for val in rgb], True)
            # alpha channel
            # df['A'] = 255.0
            df.insert(len(df.columns), "A", [255 for _ in rgb], True)


            





        return df







    # FUNCTIONS FROM OBJECTS TO COLOR SCHEME DF

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
    
    def from_resultRecords(self, resultRecords, color_scheme, drop_values=None, select_photon_id=None, photon_register=None, select_parent=True, select_child=True, border_limits=None):
        """
        :param border_limits: [x_min, x_max, y_min, y_max, z_min, z_max]
        """
        df = pd.DataFrame({'value': [val[4] for val in resultRecords], 'x_idx': [val[1] for val in resultRecords], 'y_idx': [val[2] for val in resultRecords], 'z_idx': [val[3] for val in resultRecords], 'photon_id': [val[0] for val in resultRecords]})
        # filter photon_id
        if select_photon_id is not None:
            if photon_register is not None:
                # parent
                if select_parent:
                    for select_id in select_photon_id.copy():
                        select_photon_id += self.all_parents_in_photon_register(photon_register, select_id)
                        select_photon_id = list(set(select_photon_id)) # unique vals
                # child
                if select_child:
                    for select_id in select_photon_id.copy():
                        select_photon_id += self.all_childs_in_photon_register(photon_register, select_id)
                        select_photon_id = list(set(select_photon_id)) # unique vals
            # filter - only ids that are in select_photon_id
            df = df[df["photon_id"].isin(select_photon_id)]
        # filter values in border limit
        if border_limits is not None:
            df = df[df["x_idx"] >= border_limits[0]]
            df = df[df["x_idx"] <= border_limits[1]-1]
            df = df[df["y_idx"] >= border_limits[2]]
            df = df[df["y_idx"] <= border_limits[3]-1]
            df = df[df["z_idx"] >= border_limits[4]]
            df = df[df["z_idx"] <= border_limits[5]-1]
        # color scheme process
        df = self.process_df_by_color_scheme(df, color_scheme, drop_values)
        return df
    



    # TOOLS

    def stack_color_scheme(self, cs_list: list[pd.DataFrame], ignore_index=True, drop_duplicates=True):
        cs_stack = pd.DataFrame()
        # columns that will be used as an unique key
        loc_cols = ["x_idx", "y_idx"]
        if "z_idx" in cs_list[0].columns:
            loc_cols.append("z_idx")
        # concatenate in loop
        for cs in cs_list:
            cs_stack = pd.concat([cs_stack, cs], ignore_index=ignore_index)
        # drop duplicates
        if drop_duplicates:
            cs_stack = cs_stack.drop_duplicates(subset=loc_cols, keep='last', ignore_index=ignore_index)
        return cs_stack
    

    def add_offset(self, df, offset):
        # choose columns to modify
        if len(offset) == 2:
            cols = ["x_idx", "y_idx"]
        else:
            cols = ["x_idx", "y_idx", "z_idx"]
        # add offset
        df[cols] += offset

    def all_parents_in_photon_register(self, photon_register, photon_id):
        parent_id = photon_register[photon_id]["parent"]
        if parent_id is None:
            return []
        else:
            return [parent_id] + self.all_parents_in_photon_register(photon_register, parent_id)
        
    def all_childs_in_photon_register(self, photon_register, photon_id):
        childs = photon_register[photon_id]["child"]
        if len(childs) > 0:
            bufor = []
            for one_child in childs:
                bufor += self.all_parents_in_photon_register(photon_register, one_child)
            return childs + bufor
        else:
            return []
        


        