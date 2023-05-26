from Object3D import Object3D
from Space3dTools import Space3dTools
from FeatureSampling import FeatureSampling

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
        
    def initialize_source(self, body_type="from self body", body=None, tropic=None, flag_isotropic=False, photon_limit=10):

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
        photon_limits = [distrib2every+1 for _ in range(distrib2first)] + [distrib2every for _ in range(sources_count-distrib2first)]

        # Make LightSourcePoint list
        self.light_source_list = [LightSourcePoint(probaFun_phi, probaFun_theta, ph_lim, loc_point, dir_vec=tropic, dir_phi=None, dir_theta=None) for ph_lim, loc_point in list(zip(photon_limits, light_points_xyz))]







        