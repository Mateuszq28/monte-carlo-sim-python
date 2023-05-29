from Object3D import Object3D
import json

class PropEnv(Object3D):
    def __init__(self, x=100, y=100, z=100, arr=None):
        super().__init__(x, y, z, arr)

    def get_properties(self, x, y, z):
        raise NotImplementedError()

    @staticmethod
    def load_json(path):
        with open(path, 'w') as f:
            d = json.load(f)
        return PropEnv(arr=d["body"])
