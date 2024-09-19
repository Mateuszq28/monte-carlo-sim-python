import pandas as pd
import numpy as np
from ColorPointDF import ColorPointDF
from LightSource import LightSource

class ArrowsDF():

    def __init__(self):
        pass

    def fromDF(self, df: pd.DataFrame, photon_register=None, add_start_arrows=True, color_by_root=False, drop_excessive_columns=True):
        df = df.copy()
        if "photon_id" not in df:
            raise ValueError("df must have photon_id column")
        # Do not sort like this! It will also change order within the same photon_id
        # df.sort_values(by=['photon_id'], inplace=True)
        # right way to do that:
        df.reset_index()
        df["sort_idx"] = df.index
        df.sort_values(by=['photon_id', "sort_idx"], inplace=True)
        # make pairs
        move_idx = [(i+1) % len(df) for i in range(len(df))]
        df[["x_idx_2", "y_idx_2", "z_idx_2"]] = df.iloc[move_idx][["x_idx", "y_idx", "z_idx"]].to_numpy()
        df["photon_id_2"] = df.iloc[move_idx]["photon_id"].to_numpy()
        # change last row (it's photon_idx_2 is hookeded up to the first row)
        df.loc[df.index[[-1]], "photon_id_2"] = df.loc[df.index[-1], ["photon_id"]].to_numpy()
        df.loc[df.index[[-1]], ["x_idx_2", "y_idx_2", "z_idx_2"]] = df.loc[df.index[-1], ["x_idx", "y_idx", "z_idx"]].to_numpy()
        # save single occurences
        single_flag = ~df.duplicated(subset="photon_id", keep=False)
        df.loc[single_flag, "photon_id_2"] = df["photon_id"][single_flag]
        df.loc[single_flag, "x_idx_2"] = df["x_idx"][single_flag]
        df.loc[single_flag, "y_idx_2"] = df["y_idx"][single_flag]
        df.loc[single_flag, "z_idx_2"] = df["z_idx"][single_flag]
        # delete arrows, that are not connected to the same photon
        df = df[df["photon_id"] == df["photon_id_2"]]
        if add_start_arrows:
            if photon_register is not None:
                sa = self.start_points_arrows(df, photon_register)
                df = pd.concat([df, sa], ignore_index=True)
            else:
                raise ValueError("To add start point arrows photon_register is needed")
        if color_by_root:
            ColorPointDF.color_by_root_photon(df, photon_register)
        # delete arrows with 0 length
        df = df[df[["x_idx", "y_idx", "z_idx"]].to_numpy() != df[["x_idx_2", "y_idx_2", "z_idx_2"]].to_numpy()]
        df.drop_duplicates(subset=["x_idx", "y_idx", "z_idx", "x_idx_2", "y_idx_2", "z_idx_2", "R", "G", "B", "A"], keep="first", inplace=True)
        if drop_excessive_columns:
            df = df[["x_idx", "y_idx", "z_idx", "x_idx_2", "y_idx_2", "z_idx_2", "R", "G", "B", "A"]]
        return df
    

    def from_lightSource(self, lightSource: LightSource, lightSource_DF, offset, arrow_length):
        df = pd.DataFrame()
        loc = np.array([ls.loc_point for ls in lightSource.light_source_list]) + np.array(offset) # type: ignore
        dir = np.array([ls.dir_vec for ls in lightSource.light_source_list]) # type: ignore
        next_loc = loc + dir * arrow_length
        df[["x_idx", "y_idx", "z_idx"]] = loc
        df[["x_idx_2", "y_idx_2", "z_idx_2"]] = next_loc
        df.sort_values(["x_idx", "y_idx", "z_idx"], inplace=True)
        lightSource_DF = lightSource_DF.sort_values(["x_idx", "y_idx", "z_idx"], inplace=False)
        lightSource_DF[["x_idx_2", "y_idx_2", "z_idx_2"]] = df[["x_idx_2", "y_idx_2", "z_idx_2"]]
        return lightSource_DF


    def start_points_arrows(self, first_arrow_records: pd.DataFrame, photon_register):
        start_arrows = first_arrow_records.copy()
        start_arrows.drop_duplicates(subset="photon_id", keep="first", inplace=True)
        start_arrows[["x_idx_2", "y_idx_2", "z_idx_2"]] = start_arrows[["x_idx", "y_idx", "z_idx"]]
        start_pos = np.array([np.array( photon_register[str(id)]["start_pos"]) for id in start_arrows["photon_id"]])
        start_arrows[["x_idx", "y_idx", "z_idx"]] = start_pos
        return start_arrows
    

    @staticmethod
    def make_sparse(df, put_num):
        scale = put_num+1
        df[["x_idx", "y_idx", "z_idx", "x_idx_2", "y_idx_2", "z_idx_2"]] = df[["x_idx", "y_idx", "z_idx", "x_idx_2", "y_idx_2", "z_idx_2"]] * scale
        return df



