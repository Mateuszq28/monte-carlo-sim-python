from Object3D import Object3D
import json

class PropEnv(Object3D):
    def __init__(self, x=100, y=100, z=100, arr=None):
        super().__init__(x, y, z, arr)

    def get_properties(self, x, y, z):
        raise NotImplementedError()
    
    def get_label_from_float(self, xf=None, yf=None, zf=None, xyz=None):
        if xyz is not None:
             xf = xyz[0]
             yf = xyz[1]
             zf = xyz[2]

        if xf is not None and xf is not None and zf is not None:
            int_x = int(xf)
            int_y = int(yf)
            int_z = int(zf)
            label = self.body[int_x, int_y, int_z]
        else:
            raise ValueError("too many None values")
        return label
    
    def env_boundary_check(self, pos):
        env_boundary_exceeded = False
        for i in range(3):
            if pos[i] > self.shape[i]:
                env_boundary_exceeded = True
                break
        return env_boundary_exceeded

    @staticmethod
    def load_json(path):
        with open(path, 'w') as f:
            d = json.load(f)
        return PropEnv(arr=d["body"])
    
