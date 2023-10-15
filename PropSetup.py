from LightSource import LightSource
from PropEnv import PropEnv
from PropEnvVec import PropEnvVec
from Object3D import Object3D
import json
import numpy as np
import os
from ByVispy import ByVispy
from ColorPointDF import ColorPointDF
from ArrowsDF import ArrowsDF

class PropSetup:

    # it is overwritten in sim
    flag_use_propenv_on_formulas = False

    def __init__(self, propEnv: PropEnv, lightSource: LightSource, offset):
        self.propEnv = propEnv
        self.lightSource = lightSource
        self.offset = offset
        self.env_path = None
        self.light_source_path = None
        self.escaped_photons_weight = 0.0
        self.resultEnv = None
        self.resultRecords = None
        self.resultShape = None
        self.photon_register = dict()
        self.config = None
        self.result_folder = ""
        self.random_seed_pool = 0
        self.generated_num = 0

    def make_preview(self):
        """
        Make object3D that contain material labels + marked light sources locations
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
        Make object3D that contain material labels + result photon weights in tissue
        self.propEnv.body + self.resultEnv.body
        """
        if self.resultEnv is not None:
            arr = self.resultEnv.body + self.propEnv.body
            result_preview = PropEnv(arr=arr)
            return result_preview
        else:
            raise ValueError("self.resultEnv can not be None")
        

    def make_preview_DF(self, cs_material="solid", cs_light_source="solid"):
        """
        Make ColorPointDF that contain material labels + marked light sources locations
        self.propEnv.body + self.lightSource.body
        """
        cdf = ColorPointDF()
        df_material = cdf.from_Object3d(self.propEnv, color_scheme=cs_material, drop_values=[0])
        df_light_source = cdf.from_Object3d(self.lightSource, color_scheme=cs_light_source, drop_values=[0])
        cdf.add_offset(df_light_source, offset=self.offset)
        arrows_DF = ArrowsDF().from_lightSource(self.lightSource, df_light_source, offset=self.offset, arrow_length=20.0)
        # df_material['A'] = 20
        preview_DF = cdf.stack_color_scheme([df_material, df_light_source])
        return preview_DF, arrows_DF


    def make_result_preview_DF(self, cs_material="solid", cs_photons="loop"):
        """
        Make ColorPointDF that contain material labels + result photon weights in tissue
        self.propEnv.body + self.resultEnv.body
        """
        cdf = ColorPointDF()
        df_material = cdf.from_Object3d(self.propEnv, color_scheme=cs_material, drop_values=[0])
        # df_material['A'] = 20
        df_photons = cdf.from_Object3d(self.resultEnv, color_scheme=cs_photons, drop_values=[0])
        result_preview_DF = cdf.stack_color_scheme([df_material, df_photons])
        return result_preview_DF


    def save2result_env_and_records(self, xyz, weight, photon_id, round=True):
        self.save2resultEnv(xyz, weight)
        self.save2resultRecords(xyz, weight, photon_id, round)

    def save2resultEnv(self, xyz, weight):
        if self.config is not None:
            if self.config["flag_save_result_env"]:
                if self.resultEnv is None:
                    sh = self.propEnv.shape
                    arr = np.full(shape=sh, fill_value=0.0, dtype=np.float64)
                    self.resultEnv = PropEnv(arr=arr)
                    self.resultShape = self.propEnv.shape.copy()
                xyz_int = PropEnv.round_xyz(xyz)
                self.resultEnv.body[xyz_int[0], xyz_int[1], xyz_int[2]] += weight
        else:
            raise ValueError("self.config is needed")
        
    def save2resultRecords(self, xyz, weight, photon_id, round=True):
        if self.config is not None:
            if self.config["flag_seve_result_records"]:
                # check if create resultRecords container
                if self.resultRecords is None:
                    self.resultRecords = []
                    self.resultShape = self.propEnv.shape.copy()
                # float int conversion
                if round:
                    xyz_save = PropEnv.round_xyz(xyz)
                else:
                    xyz_save = xyz.copy()
                # data type cohesion
                if isinstance(xyz_save, np.ndarray):
                    xyz_save = xyz_save.tolist()
                # save
                record = [photon_id] + xyz_save + [weight]
                self.resultRecords.append(record)
        else:
            raise ValueError("self.config is needed")

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

    def load_result_json(self, folder):
        # path
        path_resultEnv = os.path.join(folder, "resultEnv.json")
        path_resultRecords = os.path.join(folder, "resultRecords.json")
        # load from files
        with open(path_resultEnv, "r") as f:
            d_resultEnv = json.load(f)
        with open(path_resultRecords, "r") as f:
            d_resultRecords = json.load(f)
        # change resultEnv to PropEnv object if needed and assign to variables
        re = d_resultEnv["resultEnv"]
        if re is None:
            self.resultEnv = None
        else:
            self.resultEnv = PropEnv(arr=np.array(re))
        self.resultRecords = d_resultRecords["resultRecords"]


    @staticmethod
    def auto_offset(env_shape, lightSource_shape):
        # middle x axis
        offset_x = (env_shape[0] - lightSource_shape[0]) // 2
        # middle y axis
        offset_y = (env_shape[1] - lightSource_shape[1]) // 2
        # max top z axis
        offset_z = env_shape[2] - lightSource_shape[2] - 0
        return [offset_x, offset_y, offset_z]

    @staticmethod
    def from_components(env_path, light_source_path, offset=None):
        if PropSetup.flag_use_propenv_on_formulas:
            propEnv = PropEnvVec.load_json(env_path)
        else:
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