from Object3D import Object3D
import json

class PropEnv(Object3D):
    def __init__(self, x=100, y=100, z=100, arr=None):
        super().__init__(x, y, z, arr)
    
    def get_label_from_float(self, xyz):
        xyz_int = self.round_xyz(xyz)
        label = self.body[xyz_int[0], xyz_int[1], xyz_int[2]]
        return label

    def get_properties(self, xyz):
        raise NotImplementedError()
    
    def get_refractive_index(self, xyz):
        raise NotImplementedError()
    
    def env_boundary_check(self, xyz):
        xyz_int = self.round_xyz(xyz)
        env_boundary_exceeded = False
        for i in range(3):
            if xyz_int[i] > self.shape[i]:
                env_boundary_exceeded = True
                break
        return env_boundary_exceeded

    @staticmethod
    def load_json(path):
        with open(path, 'w') as f:
            d = json.load(f)
        return PropEnv(arr=d["body"])

    @staticmethod
    def round_xyz(xyz):
        xyz_int = [round(val) for val in xyz]
        return xyz_int
    
