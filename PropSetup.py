from LightSource import LightSource
from PropEnv import PropEnv
from Object3D import Object3D
import json
import numpy as np

class PropSetup:
    def __init__(self, propEnv: PropEnv, lightSource: LightSource, offset):
        self.propEnv = propEnv
        self.lightSource = lightSource
        self.offset = offset
        self.preview = None
        self.env_path = None
        self.light_source_path = None
        self.resultEnv = None
        self.resultRecords = None

    def makePreview(self):
        arr3d = self.propEnv.body.copy()
        ox, oy, oz = self.offset
        sh = self.lightSource.shape
        arr3d[ox:ox+sh[0], oy:oy+sh[1], oz:oz+sh[2]] = self.lightSource
        self.preview = Object3D(arr=arr3d)

    def save2result_env(self, xyz, weight):
        if self.resultEnv is None:
            sh = self.propEnv.shape
            arr = np.full(shape=sh, fill_value=0.)
            self.resultEnv = PropEnv(arr=arr)
        xyz_int = self.resultEnv.round_xyz(xyz)
        self.resultEnv.body[xyz[0], xyz[1], xyz[2]] += weight
        
    def save2resultRecords(self, xyz, weight, round=True):
        if self.resultRecords is None:
            self.resultRecords = []
        if round:
            xyz_save = PropEnv.round_xyz(xyz)
        else:
            xyz_save = xyz.copy()
        if isinstance(xyz_save,np.ndarray):
            xyz_save = xyz_save.tolist()
        record = xyz_save + [weight]
        self.resultRecords.append(record)

    @staticmethod
    def auto_offset(env_shape, lightSource_shape):
        # middle x axis
        offset_x = (env_shape[0] - lightSource_shape[0]) // 2
        # middle y axis
        offset_y = (env_shape[1] - lightSource_shape[1]) // 2
        # max top z axis
        offset_z = env_shape[2] - lightSource_shape[2] - 1
        return [offset_x, offset_y, offset_z]

    @staticmethod
    def from_components(env_path, light_source_path, offset=None):
        propEnv = PropEnv.load_json(env_path)
        lightSource = LightSource.load_json(light_source_path)
        if offset is None:
            offset = PropSetup.auto_offset(propEnv.shape, lightSource.shape)
        propSetup = PropSetup(propEnv, lightSource, offset)
        propSetup.env_path = env_path
        propSetup.light_source_path = light_source_path
        return propSetup

    def save_json(self, path):
        d = {
            "env_path": self.env_path,
            "light_source_path": self.light_source_path,
            "offset": self.offset
        }
        with open(path, 'w') as f:
            json.dump(d, f)

    @staticmethod
    def load_json(path):
        with open(path, 'w') as f:
            d = json.load(f)
        propSetup = PropSetup.from_components(d["env_path"], d["light_source_path"], d["offset"])
        return propSetup

    @staticmethod
    def from_file(prop_setup_path):
        return PropSetup.load_json(prop_setup_path)