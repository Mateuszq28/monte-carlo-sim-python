from Object3D import Object3D
import numpy as np
import pandas as pd
import colorsys
from PIL import ImageColor
import json
import math
from FeatureSampling import MyRandom
from scipy.stats import norm
from matplotlib import cm
import matplotlib.pyplot as plt

class ColorPointDF():

    threshold_const = 0.2
    threshold_quantile = 0.0
    use_threshold = "quantile"
    palette_1 = ['#C0392B', '#E74C3C', '#9B59B6', '#8E44AD', '#2980B9', '#3498DB', '#1ABC9C', '#16A085', '#27AE60', '#2ECC71', '#F1C40F', '#F39C12', '#E67E22', '#D35400', '#ECF0F1', '#BDC3C7', '#95A5A6', '#7F8C8D', '#34495E', '#2C3E50']
    palette_2 = ['green', 'yellow', 'orange', 'red', 'purple', 'blue', 'pink', '#339933', '#FF3366', '#CC0066', '#99FFCC', '#3366FF', '#0000CC']
    old_color_dict = None


    def __init__(self):
        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)
        # set default loop color list
        # self.loop_color_names = self.palette_2
        self.loop_color_names = self.create_palette(30)

    def create_palette(self, num_of_colors):
        # choose to how many parts split hsv color wheel (color space)
        hue_max_fragments = 15
        saturation_max_fragments = 5
        value_max_fragments = 5
        # check if num_of_colors not exceeds the limit
        num_of_colors_limit = hue_max_fragments * saturation_max_fragments * value_max_fragments
        if num_of_colors > num_of_colors_limit:
            raise ValueError("num_of_colors must be <= {}".format(num_of_colors_limit))
        # tune up split up nums
        # first take all hue, then all value, then all saturation
        if num_of_colors > hue_max_fragments:
            hue_num_of_colors = hue_max_fragments
            value_num_of_colors = math.ceil(num_of_colors / hue_num_of_colors)
            if value_num_of_colors > value_max_fragments:
                value_num_of_colors = value_max_fragments
                saturation_num_of_colors = math.ceil(num_of_colors / (hue_num_of_colors * value_num_of_colors))
            else:
                saturation_num_of_colors = 1
        else:
            hue_num_of_colors = num_of_colors
            value_num_of_colors = 1
            saturation_num_of_colors = 1
        # split hsv
        hue = np.linspace(0.0, 1.0, num=hue_num_of_colors, endpoint=True)
        saturation = np.linspace(1.0, 0.5, num=saturation_num_of_colors, endpoint=True) # reversed to take first 1.0
        value = np.linspace(1.0, 0.5, num=value_num_of_colors, endpoint=True) # reversed to take first 1.0
        # hsv to rgb <0.0, 1.0>
        rgb_color = []
        for h in hue:
            for s in saturation:
                for v in value:
                    rgb_color.append(colorsys.hsv_to_rgb(h, s, v))
        # to rgb <0, 255>
        rgb_color_255 = [[round(val * 255.0) for val in rgb] for rgb in rgb_color]
        # to hex string code
        hex_color = [self.rgb_to_hex(rgb) for rgb in rgb_color_255]
        return hex_color[:num_of_colors]

    def rgb_to_hex(self, rgb):
        r, g, b = rgb
        return "#" + ('%02x%02x%02x' % (r, g, b)).upper()



    # MAIN COLOR SCHEME PROCESS FUNCTION

    def process_df_by_color_scheme(self, df: pd.DataFrame, color_scheme, drop_values, try_use_old_color_dict=True):

        # Drop values (for example 0.0)
        if drop_values is not None:
            df = df[~df["value"].isin(drop_values)]


        if color_scheme == "threshold":
            df = self.cs_threshold(df)
        elif color_scheme == "loop":
            df = self.cs_loop(df)
        elif color_scheme == "solid":
            df = self.cs_solid(df)
        elif color_scheme == "photonwise":
            df = self.cs_photonwise(df, try_use_old_color_dict=try_use_old_color_dict)
        elif color_scheme == "random":
            df = self.cs_random(df)
        elif color_scheme == "rainbow":
            df = self.cs_rainbow(df)

        elif color_scheme == "min-max":
            df = self.cs_minmax(df)
        elif color_scheme == "median":
            df = self.cs_median(df)
        elif color_scheme == "trans-normal":
            df = self.cs_transnormal(df)
        elif color_scheme == "logarithmic":
            df = self.cs_logarithmic(df)

        elif color_scheme == "heatmap min-max":
            df = self.cs_minmax(df)
            df = self.cs_rgb2heatmap(df)
        elif color_scheme == "heatmap median":
            df = self.cs_median(df)
            df = self.cs_rgb2heatmap(df)
        elif color_scheme == "heatmap trans-normal":
            df = self.cs_transnormal(df)
            df = self.cs_rgb2heatmap(df)
        elif color_scheme == "heatmap logarithmic":
            df = self.cs_logarithmic(df)
            df = self.cs_rgb2heatmap(df)


        return df



    # COLOR SCHEMES FUNCTIONS

    def cs_threshold(self, df):
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
        return df



    def cs_loop(self, df):
        df = df.copy()
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


    def cs_solid(self, df):
        df = df.copy()
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
        return df


    def cs_photonwise(self, df, try_use_old_color_dict):
        df = df.copy()
        if "photon_id" not in df.columns:
            raise ValueError("df must have photon_id column")
        uniq_photon_id = pd.unique(df['photon_id'])
        rnd = MyRandom()
        colors = [[rnd.randint(0, 255+1), rnd.randint(0, 255+1), rnd.randint(0, 255+1)] for _ in range(len(uniq_photon_id))]
        # id to color translator (dict)
        trans_color = dict(zip(uniq_photon_id, colors))
        ColorPointDF.old_color_dict = trans_color
        if try_use_old_color_dict and ColorPointDF.old_color_dict is not None:
            old_trans_color = ColorPointDF.old_color_dict
            trans_color.update(old_trans_color)
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


    def cs_random(self, df):
        df = df.copy()
        rnd = MyRandom()
        rgb = rnd.randint(0, 255+1, size=(len(df), 3))
        # insert R, G, B columns
        df.insert(len(df.columns), "R", [val[0] for val in rgb], True)
        df.insert(len(df.columns), "G", [val[1] for val in rgb], True)
        df.insert(len(df.columns), "B", [val[2] for val in rgb], True)
        # alpha channel
        df.insert(len(df.columns), "A", [255 for _ in range(len(df))], True)
        return df


    def cs_rainbow(self, df):
        df = df.copy()
        n = len(df)
        rgb = [(i / n, 1.0 - i / n, 0.0, 0.8) for i in range(n)]
        rgb = [[val*255.0 for val in rgb_tup] for rgb_tup in rgb]
        # insert R, G, B columns
        df.insert(len(df.columns), "R", [val[0] for val in rgb], True)
        df.insert(len(df.columns), "G", [val[1] for val in rgb], True)
        df.insert(len(df.columns), "B", [val[2] for val in rgb], True)
        # alpha channel
        df.insert(len(df.columns), "A", [val[3] for val in rgb], True)
        return df


    def cs_minmax(self, df):
        df = df.copy()
        max = df["value"].max()
        min = df["value"].min()
        gray = 255 * ((df["value"].to_numpy() - min) / (max - min))
        # insert R, G, B columns
        df.insert(len(df.columns), "R", [val for val in gray], True)
        df.insert(len(df.columns), "G", [val for val in gray], True)
        df.insert(len(df.columns), "B", [val for val in gray], True)
        # alpha channel
        df.insert(len(df.columns), "A", [255 for _ in gray], True)
        return df


    def cs_median(self, df):
        df = df.copy()
        me = df["value"].median()
        gray = 255 * (df["value"].to_numpy() / me)
        gray = np.clip(gray, a_min=0, a_max=255)
        # insert R, G, B columns
        df.insert(len(df.columns), "R", [val for val in gray], True)
        df.insert(len(df.columns), "G", [val for val in gray], True)
        df.insert(len(df.columns), "B", [val for val in gray], True)
        # alpha channel
        df.insert(len(df.columns), "A", [255 for _ in gray], True)
        return df


    def cs_transnormal(self, df):
        df = df.copy()
        min_color = 15
        hist, bin_edges = np.histogram(df["value"].to_numpy(), bins=256-min_color, density=False)
        cumsum = np.cumsum(hist)
        cumsum_under = np.hstack((np.array([0]), cumsum))[:-1]
        # cumulative sum in the middle of the bins
        middle_cumsum = cumsum_under + 0.5 * hist
        # number of all samples
        n = sum(hist)
        # proportion
        p = middle_cumsum / n # cdf
        # Percent point function (inverse of cdf — percentiles)
        ppf = norm.ppf(p, loc=0, scale=1)
        # min max normalization
        # gry color for each bin
        min = ppf.min()
        max = ppf.max()
        gray = (255-min_color) * ((ppf - min) / (max - min)) + min_color
        # set colors
        values = df["value"].to_numpy()
        color = df["value"].to_numpy()
        for i in range(len(hist)):
            # <= value <=
            # can be closed both side, because it will be overwritten
            # must be closed, because lat val in bin_edges is included
            mask = (bin_edges[i] <= values) * (values <= bin_edges[i+1])
            color[mask] = gray[i]
        # insert R, G, B columns
        df.insert(len(df.columns), "R", [val for val in color], True)
        df.insert(len(df.columns), "G", [val for val in color], True)
        df.insert(len(df.columns), "B", [val for val in color], True)
        # alpha channel
        df.insert(len(df.columns), "A", [255 for _ in color], True)
        return df


    def cs_logarithmic(self, df):
        df = df.copy()
        vals = df["value"].to_numpy()
        max = vals.max()
        # decibels (max is 0, other are negative)
        dec_vals = 20 * np.log10( vals / max )
        #   other logarithms to achieve greater dynamic (difference between max and min)
        #   dec_vals = np.log2( vals / max )
        # dec_vals = np.emath.logn(n=1.05, x= vals / max )
        # min max normalization
        min = dec_vals.min() # negative
        max = dec_vals.max() # 0
        min_color = 15
        gray = (255-min_color) * ((dec_vals - min) / (max - min)) + min_color
        # insert R, G, B columns
        df.insert(len(df.columns), "R", [val for val in gray], True)
        df.insert(len(df.columns), "G", [val for val in gray], True)
        df.insert(len(df.columns), "B", [val for val in gray], True)
        # alpha channel
        df.insert(len(df.columns), "A", [255 for _ in gray], True)
        return df


    def cs_rgb2heatmap(self, df):
        df = df.copy()
        # interesting colormaps from OpenCV
        # - COLORMAP_AUTUMN - red. orange, yellow
        # - COLORMAP_JET - blue, green, red
        # - COLORMAP_HOT - black, red, orange, yellow, white
        # interesting colormaps from matplotlib
        # - autumn - red. orange, yellow
        # - jet - blue, green, red
        # - hot - black, red, orange, yellow, white
        # - YlOrRd - yellow, orange, red
        # - inferno - purple, yellow
        name = "inferno"
        gray = df['R'].to_numpy() / 255
        rgb = cm.get_cmap(plt.get_cmap(name))(gray) * 255
        # update values
        df = df.drop(["R", "G", "B", "A"], axis='columns', inplace=False)
        # insert R, G, B columns
        df.insert(len(df.columns), "R", [val[0] for val in rgb], True)
        df.insert(len(df.columns), "G", [val[1] for val in rgb], True)
        df.insert(len(df.columns), "B", [val[2] for val in rgb], True)
        # alpha channel
        df.insert(len(df.columns), "A", [val[3] for val in rgb], True)
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
    

    def from_resultRecords(self, resultRecords, color_scheme, drop_values=None, select_photon_id=None, photon_register=None, select_parent=True, select_child=True, border_limits=None, sum_same_idx=False, sort=True, color_by_root=False):
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
            df = df[df["x_idx"].round() >= border_limits[0]]
            df = df[df["x_idx"].round() <= border_limits[1]-1]
            df = df[df["y_idx"].round() >= border_limits[2]]
            df = df[df["y_idx"].round() <= border_limits[3]-1]
            df = df[df["z_idx"].round() >= border_limits[4]]
            df = df[df["z_idx"].round() <= border_limits[5]-1]
        # sum values (photon weights) on the same localization idx and delete duplicates
        if sum_same_idx:
            self.sum_same_idx(df)
        # sort output to have same colors like in propEnv processing
        if sort:
            df.sort_values(["x_idx", "y_idx", "z_idx"], ignore_index=True, inplace=True)
        # color scheme process
        df = self.process_df_by_color_scheme(df, color_scheme, drop_values)
        # to photon children (reflect and refraction) have the same color
        if color_by_root:
            self.color_by_root_photon(df, photon_register)
        return df
    

    def reset_colors(self, df: pd.DataFrame, color_scheme, drop_values=None):
        df.drop(["R", "G", "B", "A"], axis='columns', inplace=True)
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
        

    @staticmethod
    def color_by_root_photon(df, photon_register=None):
        if "root_photon_id" not in df.columns:
            if photon_register is not None:
                photon_ids = list(set(df["photon_id"].to_list()))
                dic = ColorPointDF.find_root_photon_ids(photon_ids, photon_register)
                # add to df
                column_root = [dic[pid] for pid in df["photon_id"]]
                df["root_photon_id"] = column_root
            else:
                raise ValueError("To add root_photon_id to df photon_register is needed")
        root_colors = [ColorPointDF.find_colors_by_photon_id(df, pid) for pid in df["root_photon_id"]]
        df[["R", "G", "B", "A"]] = root_colors


    @staticmethod
    def find_root_photon_ids(photon_ids: list, photon_register):
        root_paths = [ColorPointDF.find_root_path_photon_id(pid, photon_register, finded=[]) for pid in photon_ids]
        # filter out photon id, that are not in colorDF (not in space to draw)
        root_paths_filtered = [[pid for pid in rp if pid in photon_ids] for rp in root_paths]
        # take oldest
        # root path of every photon has at least one photon_id (itself) 
        root_photons = [rp[-1] for rp in root_paths_filtered]
        dic = dict(zip(photon_ids, root_photons))
        return dic


    @staticmethod
    def find_root_path_photon_id(photon_id, photon_register, finded: list):
        finded += [photon_id]
        parent_id = photon_register[photon_id]["parent"]
        if parent_id is not None:
            return ColorPointDF.find_root_path_photon_id(parent_id, photon_register, finded)
        else:
            return finded
        

    @staticmethod
    def find_colors_by_photon_id(df: pd.DataFrame, photon_id):
        colors = df[df["photon_id"] == photon_id][["R", "G", "B", "A"]].iloc[0].to_numpy()
        return colors
        

    @staticmethod
    def sum_same_idx(df: pd.DataFrame, subset=None):
        df[["x_idx", "y_idx", "z_idx"]] = df[["x_idx", "y_idx", "z_idx"]].round().astype(int)
        if subset is None:
            subset = ["x_idx", "y_idx", "z_idx"]
        sums = df.groupby(by=subset, as_index=False, sort=False, dropna=False)["value"].sum()
        # drop duplicates to achieve the same lenth as finded_idx (groupby)
        df.drop_duplicates(subset=subset, inplace=True, ignore_index=True, keep="first")
        df["value"] = sums["value"]
        if "photon_id" in df.columns:
            df.drop("photon_id", axis="columns", inplace=True)

        
    @staticmethod
    def make_sparse(df, put_num):
        scale = put_num+1
        df[["x_idx", "y_idx", "z_idx"]] = df[["x_idx", "y_idx", "z_idx"]] * scale
        return df
    
    
        