import pandas as pd
import numpy as np

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
        df[["x_idx_2", "y_idx_2", "z_idx_2", "photon_id_2"]] = df.iloc[move_idx][["x_idx", "y_idx", "z_idx", "photon_id"]].to_numpy()
        # drop last row (it's photon_idx_2 is hookeded up to the first row)
        df = df.iloc[:-1]
        # delete arrows, that are not connected to the same photon
        df = df[df["photon_id"] == df["photon_id_2"]]
        if add_start_arrows:
            if photon_register is not None:
                sa = self.start_points_arrows(df, photon_register)
                df = pd.concat([df, sa], ignore_index=True)
            else:
                raise ValueError("To add start point arrows photon_register is needed")
        if color_by_root:
            self.color_by_root_photon(df, photon_register)
        # delete arrows with 0 length
        df = df[df[["x_idx", "y_idx", "z_idx"]].to_numpy() != df[["x_idx_2", "y_idx_2", "z_idx_2"]].to_numpy()]
        df.drop_duplicates(subset=["x_idx", "y_idx", "z_idx", "x_idx_2", "y_idx_2", "z_idx_2", "R", "G", "B", "A"], keep="first", inplace=True)
        if drop_excessive_columns:
            df = df[["x_idx", "y_idx", "z_idx", "x_idx_2", "y_idx_2", "z_idx_2", "R", "G", "B", "A"]]
        return df


    def start_points_arrows(self, first_arrow_records: pd.DataFrame, photon_register):
        start_arrows = first_arrow_records.copy()
        start_arrows.drop_duplicates(subset="photon_id", keep="first", inplace=True)
        start_arrows[["x_idx_2", "y_idx_2", "z_idx_2"]] = start_arrows[["x_idx", "y_idx", "z_idx"]]
        start_pos = np.array([np.array( photon_register[id]["start_pos"]) for id in start_arrows["photon_id"]])
        start_arrows[["x_idx", "y_idx", "z_idx"]] = start_pos
        return start_arrows
    
    def color_by_root_photon(self, df, photon_register):
        photon_ids = list(set(df["photon_id"].to_list()))
        dic = self.find_root_photon_ids(photon_ids, photon_register)
        # add to df
        column_root = [dic[pid] for pid in df["photon_id"]]
        root_colors = [self.find_colors_by_photon_id(df, pid) for pid in df["photon_id"]]
        df["root_photon_id"] = column_root
        df[["R", "G", "B", "A"]] = root_colors


    def find_root_photon_ids(self, photon_ids: list, photon_register):
        root_paths = [self.find_root_path_photon_id(pid, photon_register, finded=[]) for pid in photon_ids]
        # filter out photon id, that are not in colorDF (not in space to draw)
        root_paths_filtered = [[pid for pid in rp if pid in photon_ids] for rp in root_paths]
        # take oldest
        # root path of every photon has at least one photon_id (itself) 
        root_photons = [rp[-1] for rp in root_paths_filtered]
        dic = dict(zip(photon_ids, root_photons))
        return dic

    def find_root_path_photon_id(self, photon_id, photon_register, finded: list):
        finded += [photon_id]
        parent_id = photon_register[photon_id]["parent"]
        if parent_id is not None:
            return self.find_root_path_photon_id(parent_id, photon_register, finded)
        else:
            return finded
        
    def find_colors_by_photon_id(self, df: pd.DataFrame, photon_id):
        colors = df[df["photon_id"] == photon_id][["R", "G", "B", "A"]].iloc[0].to_numpy()
        return colors
    

    @staticmethod
    def make_sparse(df, put_num):
        scale = put_num+1
        df[["x_idx", "y_idx", "z_idx", "x_idx_2", "y_idx_2", "z_idx_2"]] = df[["x_idx", "y_idx", "z_idx", "x_idx_2", "y_idx_2", "z_idx_2"]] * scale
        return df



