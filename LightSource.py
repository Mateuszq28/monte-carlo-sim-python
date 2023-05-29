from Object3D import Object3D
from Space3dTools import Space3dTools
from FeatureSampling import FeatureSampling
from Photon import Photon
import json
import numpy as np

class LightSourcePoint():

    def __init__(self, probaFun_phi, probaFun_theta, start_loc_shift_funs, photon_limit, loc_point, dir_vec=None, dir_phi=None, dir_theta=None):

        # dircetion vector in both cartesian and spherical
        if dir_vec is None:
            if dir_phi is not None and dir_theta is not None:
                x, y, z = Space3dTools.spherical2cartesian(1., dir_phi, dir_theta)
                dir_vec = [x, y, z]
            else:
                raise ValueError("Direction vector must be specified")
        else:
            _, dir_phi, dir_theta = Space3dTools.cartesian2spherical(dir_vec[0], dir_vec[1], dir_vec[2])

        # set object variables

        # localization vector
        self.loc_point = loc_point
        #self.direction vector
        self.dir_vec = dir_vec
        self.dir_phi = dir_phi
        self.dir_theta = dir_theta
        #self.probability function
        self.probaFun_phi = probaFun_phi
        self.probaFun_theta = probaFun_theta
        self.start_loc_shift_funs = start_loc_shift_funs
        # photons limit
        self.photon_limit = photon_limit
        self.photon_scattered = 0

    def emit(self):
        offset_vec = [fun() for fun in self.start_loc_shift_funs]
        emit_pos = np.array(self.loc_point) + np.array(offset_vec)
        offset_phi = self.probaFun_phi()
        offset_theta = self.probaFun_theta()
        emit_dir = Space3dTools.spherical2cartesian(1., self.dir_theta + offset_theta, self.dir_phi + offset_phi)
        self.photon_scattered += 1
        return Photon(emit_pos, emit_dir)


class LightSource(Object3D):

    def __init__(self, x=10, y=10, z=1, arr=None, light_source_label=-1):
        super().__init__(x, y, z, arr)
        self.light_source_label = light_source_label
        self.light_source_list = None
        self.body_type = None
        self.tropic = None
        self.source_type = None
        self.photon_limit = None
        self.photon_limits_list = None
        
    def initialize_source(self, body_type="from self body", body=None, tropic=None, source_type="straight", source_anchor="point", photon_limit=10, light_source_label=-1):
        # object variables
        self.body_type = body_type
        self.tropic = tropic
        self.source_type = source_type
        self.source_anchor = source_anchor
        self.photon_limit = photon_limit
        self.light_source_label = light_source_label

        # light rays tropic (direction vector)
        if tropic is None:
            tropic = [0,0,-1]

        # launch direction function - set proba direction function for each light point
        featureSampling = FeatureSampling()
        if source_type == "straight":
            probaFun_phi = featureSampling.photon_phi_constant
            probaFun_theta = featureSampling.photon_theta_constant
        elif source_type == "isotropic":
            probaFun_phi = featureSampling.photon_phi_isotropic
            probaFun_theta = featureSampling.photon_theta_isotropic
        elif source_type == "photon_fun":
            probaFun_phi = featureSampling.photon_phi
            probaFun_theta = featureSampling.photon_theta
        else:
            raise ValueError("source_type should be in {straight, isotropic, photon_fun}")
        
        # launch localization function - set proba function for shift start localization
        if source_anchor == "point":
            probaFun_loc_x = featureSampling.start_loc_shift_x_0
            probaFun_loc_y = featureSampling.start_loc_shift_y_0
            probaFun_loc_z = featureSampling.start_loc_shift_z_0
        else:
            raise ValueError("source_anchor should be in { point }")
        start_loc_shift_funs = [probaFun_loc_x, probaFun_loc_y, probaFun_loc_z]

        # mark localizations, where LightSourcePoints will be put
        # just set light_source_label in body

        if body_type == "from self body":
            pass
        elif body_type == "from body":
            if body is not None:
                self.rebuild_from_array(body)
            else:
                raise ValueError("body parameter is None")
        elif body_type == "rectangular":
            self.fill_cube(self.light_source_label, start_p=[0.,0.,0.], fill_rec=None, end_p=[1.,1.,1.])
        elif body_type == "point":
            self.fill_cube(self.light_source_label, start_p=[0,0,0], fill_rec=None, end_p=[1,1,1])

        # Get list of xyz coordinates of all light sources
        self.make3d_points_series()
        light_point_idx_in_series = self.composition["labels"].index(self.light_source_label)
        light_points_xyz = self.composition["points_series"][light_point_idx_in_series]

        # ditribute photon limits
        sources_count = len(light_points_xyz)
        distrib2every = photon_limit // sources_count
        distrib2first = sources_count - distrib2every * sources_count
        self.photon_limits_list = [distrib2every+1 for _ in range(distrib2first)] + [distrib2every for _ in range(sources_count-distrib2first)]

        # Make LightSourcePoint list
        self.light_source_list = [LightSourcePoint(probaFun_phi, probaFun_theta, start_loc_shift_funs, ph_lim, loc_point, dir_vec=tropic, dir_phi=None, dir_theta=None) for ph_lim, loc_point in list(zip(self.photon_limits_list, light_points_xyz))]


    def save_json(self, path, additional=True):
        d = {
            "body": self.body,
            "light_source_label": self.light_source_label,
            "light_source_list": self.light_source_list,
            "body_type": self.body_type,
            "tropic": self.tropic,
            "source_type": self.source_type,
            "source_anchor": self.source_anchor,
            "photon_limit": self.photon_limit,
            "photon_limits_list": self.photon_limits_list
        }
        if additional:
            d["self.height"] = self.height
            d["self.width"] = self.width
            d["self.depth"] = self.depth
            d["self.shape"] = self.shape
            d["composition"] = self.composition
        with open(path, 'w') as f:
            json.dump(d, f)


    @staticmethod
    def load_json(path):
        with open(path, 'w') as f:
            d = json.load(f)
        if d["photon_limit"] is None:
            d["photon_limit"] = sum(d["photon_limits_list"])
        lightSource = LightSource(arr=d["body"])
        if d["light_source_list"] is not None:
            lightSource.body = d["body"]
            lightSource.light_source_label = d["light_source_label"]
            lightSource.light_source_list = d["light_source_list"]
            lightSource.body_type = d["body_type"]
            lightSource.tropic = d["tropic"]
            lightSource.source_type = d["source_type"]
            lightSource.source_anchor=d["source_anchor"]
            lightSource.photon_limit = d["photon_limit"]
            lightSource.photon_limits_list = d["photon_limits_list"]
        else:
            lightSource.initialize_source(body_type="from self body", body=None, tropic=d["tropic"], source_type=d["source_type"], source_anchor=d["source_anchor"], photon_limit=d["photon_limit"], light_source_label=d["light_source_label"])
        return lightSource
    





        