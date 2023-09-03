import pandas as pd
import numpy as np

class ArrowsDF():

    def __init__(self):
        pass

    def fromDF(self, df: pd.DataFrame, photon_register=None, add_start_arrows=True, color_by_root=False):
        df = df.copy()
        if "photon_id" not in df:
            raise ValueError("df must have photon_id column")
        df.sort_values(by=['photon_id'], inplace=True)
        move_idx = [(i+1) % len(df) for i in range(len(df))]
        df[["x_idx_2", "y_idx_2", "z_idx_2", "photon_id_2"]] = df.iloc[move_idx][["x_idx", "y_idx", "z_idx", "photon_id"]].to_numpy()
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
        return df


    def start_points_arrows(self, first_arrow_records: pd.DataFrame, photon_register):
        start_arrows = first_arrow_records.copy()
        start_arrows.drop_duplicates(subset="photon_id", keep="first", inplace=True)
        start_arrows[["x_idx_2", "y_idx_2", "z_idx_2"]] = start_arrows[["x_idx", "y_idx", "z_idx"]]
        start_pos = np.array([np.array( photon_register[id]["start_pos"], dtype=int) for id in start_arrows["photon_id"]])
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



