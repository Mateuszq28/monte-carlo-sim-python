from Object3D import Object3D
import json
import numpy as np

class PropEnv(Object3D):
    def __init__(self, x=100, y=100, z=100, arr=None):
        super().__init__(x, y, z, arr)
        with open("config.json") as f:
            # get simulation config parameters
            config = json.load(f)
        self.tissue_properties = config["tissue_properties"]
    
    def get_label_from_float(self, xyz):
        xyz_int = self.round_xyz(xyz)
        label = self.body[xyz_int[0], xyz_int[1], xyz_int[2]]
        return label

    def get_properties(self, xyz):
        label = self.get_label_from_float(xyz)
        label_str = str(label)
        # Absorption Coefficient in 1/cm
        mu_a = self.tissue_properties[label_str]["mu_a"]
        # Scattering Coefficient in 1/cm
        mu_s = self.tissue_properties[label_str]["mu_s"]
        # Total attenuation coefficient in 1/cm
        mu_t = mu_a + mu_s
        return mu_a, mu_s, mu_t
    
    def get_refractive_index(self, xyz):
        label = self.get_label_from_float(xyz)
        label_str = str(label)
        # absolute refractive index
        n = self.tissue_properties[label_str]["n"]
        return n
    
    def env_boundary_check(self, xyz):
        xyz_int = self.round_xyz(xyz)
        env_boundary_exceeded = False
        for i in range(3):
            if xyz_int[i] > self.shape[i]:
                env_boundary_exceeded = True
                break
        return env_boundary_exceeded
    
    def boundary_check(self, xyz, xyz_next):
        label_in = self.get_label_from_float(xyz)
        round_xyz = np.array(self.round_xyz(xyz))
        round_xyz_next = np.array(self.round_xyz(xyz_next))
        vec = round_xyz_next - round_xyz
        dist = np.linalg.norm(vec)
        linspace = np.linspace(0.0, dist, num=int(dist)+1)
        boundary_pos = xyz_next
        boundary_change = False
        for lin in linspace:
            t = lin/dist
            check_pos = round_xyz + vec * t
            label_check = self.get_label_from_float(check_pos)
            if label_in != label_check:
                boundary_change = True
                boundary_pos = check_pos.tolist()
                break
        return boundary_pos, boundary_change

    @staticmethod
    def load_json(path):
        with open(path, 'r') as f:
            d = json.load(f)
        arr = np.array(d["body"])
        return PropEnv(arr=arr)

    @staticmethod
    def round_xyz(xyz):
        xyz_int = [round(val) for val in xyz]
        return xyz_int
    
