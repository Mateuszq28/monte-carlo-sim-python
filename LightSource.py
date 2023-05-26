from Object3D import Object3D
from Space3dTools import Space3dTools
from FeatureSampling import FeatureSampling
import json

class LightSourcePoint():

    def __init__(self, probaFun_phi, probaFun_theta, photon_limit, loc_point, dir_vec=None, dir_phi=None, dir_theta=None):

        # dircetion vector in both cartesian and spherical
        if dir_vec is None:
            if dir_phi is not None and dir_theta is not None:
                x, y, z = Space3dTools.spherical2cartesian(1, dir_phi, dir_theta)
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
        # photons limit
        self.photon_limit = photon_limit
        self.photon_scattered = 0

class LightSource(Object3D):

    def __init__(self, x=10, y=10, z=1, arr=None, light_source_label=-1):
        super().__init__(x, y, z, arr)
        self.light_source_label = light_source_label
        self.light_source_list = None
        self.body_type = None
        self.tropic = None
        self.flag_isotropic = None
        self.photon_limit = None
        self.photon_limits_list = None
        
    def initialize_source(self, body_type="from self body", body=None, tropic=None, flag_isotropic=False, photon_limit=10, light_source_label=-1):
        # object variables
        self.body_type = body_type
        self.tropic = tropic
        self.flag_isotropic = flag_isotropic
        self.photon_limit = photon_limit
        self.light_source_label = light_source_label

        # light rays tropic (direction vector)
        if tropic is None:
            tropic = [0,0,-1]

        # set proba function for each light point
        featureSampling = FeatureSampling()
        if flag_isotropic:
            probaFun_phi = featureSampling.photon_phi_isotropic
            probaFun_theta = featureSampling.photon_theta_isotropic
        else:
            probaFun_phi = featureSampling.photon_phi
            probaFun_theta = featureSampling.photon_theta

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
        self.light_source_list = [LightSourcePoint(probaFun_phi, probaFun_theta, ph_lim, loc_point, dir_vec=tropic, dir_phi=None, dir_theta=None) for ph_lim, loc_point in list(zip(self.photon_limits_list, light_points_xyz))]


    def save_json(self, path, additional=True):
        d = {
            "body": self.body,
            "light_source_label": self.light_source_label,
            "light_source_list": self.light_source_list,
            "body_type": self.body_type,
            "tropic": self.tropic,
            "flag_isotropic": self.flag_isotropic,
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
            lightSource.flag_isotropic = d["flag_isotropic"]
            lightSource.photon_limit = d["photon_limit"]
            lightSource.photon_limits_list = d["photon_limits_list"]
        else:
            lightSource.initialize_source(body_type="from self body", body=None, tropic=d["tropic"], flag_isotropic=d["flag_isotropic"], photon_limit=d["photon_limit"], light_source_label=d["light_source_label"])
        return lightSource
    





        