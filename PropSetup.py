from LightSource import LightSource
from PropEnv import PropEnv
from Object3D import Object3D
import json
import numpy as np
import os
from ByVispy import ByVispy

class PropSetup:

    def __init__(self, propEnv: PropEnv, lightSource: LightSource, offset):
        self.propEnv = propEnv
        self.lightSource = lightSource
        self.offset = offset
        self.env_path = None
        self.light_source_path = None
        self.escaped_photons_weight = 0.0
        self.resultEnv = None
        self.resultRecords = None
        self.config = None

    def make_preview(self):
        """
        Make object that contain material labels + marked light sources locations
        self.propEnv.body + self.lightSource.body
        """
        arr3d = self.propEnv.body.copy()
        ox, oy, oz = self.offset
        sh = self.lightSource.shape
        arr3d[ox:ox+sh[0], oy:oy+sh[1], oz:oz+sh[2]] = self.lightSource.body
        preview = Object3D(arr=arr3d)
        return preview

    def make_result_preview(self):
        """
        Make object that contain material labels + result photon weights in tissue
        self.propEnv.body + self.resultEnv.body
        """
        if self.resultEnv is not None:
            arr = self.resultEnv.body + self.propEnv.body
            result_preview = PropEnv(arr=arr)
            return result_preview
        else:
            raise ValueError("self.resultEnv can not be None")

    def save2result_env_and_records(self, xyz, weight, photon_id, round=True):
        self.save2resultEnv(xyz, weight)
        self.save2resultRecords(xyz, weight, photon_id, round)

    def save2resultEnv(self, xyz, weight):
        if self.resultEnv is None:
            sh = self.propEnv.shape
            arr = np.full(shape=sh, fill_value=0.)
            self.resultEnv = PropEnv(arr=arr)
        xyz_int = self.resultEnv.round_xyz(xyz)
        self.resultEnv.body[xyz_int[0], xyz_int[1], xyz_int[2]] += weight
        
    def save2resultRecords(self, xyz, weight, photon_id, round=True):
        if self.resultRecords is None:
            self.resultRecords = []
        if round:
            xyz_save = PropEnv.round_xyz(xyz)
        else:
            xyz_save = xyz.copy()
        if isinstance(xyz_save,np.ndarray):
            xyz_save = xyz_save.tolist()
        record = [photon_id] + xyz_save + [weight]
        self.resultRecords.append(record)

    def save_result_json(self, folder):
        if self.resultEnv is not None:
            re = self.resultEnv.body.tolist()
        else:
            re = None
        d_resultEnv = {"resultEnv": re}
        d_resultRecords = {"resultRecords": self.resultRecords}
        path_resultEnv = os.path.join(folder, "resultEnv.json")
        path_resultRecords = os.path.join(folder, "resultRecords.json")
        with open(path_resultEnv, "w") as f:
            json.dump(d_resultEnv, f)
        with open(path_resultRecords, "w") as f:
            json.dump(d_resultRecords, f)


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
        with open(path, 'r') as f:
            d = json.load(f)
        propSetup = PropSetup.from_components(d["env_path"], d["light_source_path"], d["offset"])
        return propSetup

    @staticmethod
    def from_file(prop_setup_path):
        return PropSetup.load_json(prop_setup_path)