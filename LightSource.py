from Object3D import Object3D

class LightSourcePoint():

    def __init__(self, loc_point, dir_vec, dir_phi, dir_theta, probaFun_phi, probaFun_theta, photon_limit, emit_freq=1):

        # localization vector
        self.loc_point = loc_point
        #self.direction vector
        self.dir_vec = dir_vec
        #self.probability function
        self.probaFun = probaFun
        # emit frequency - how many photons release, the rest will be omited
        self.emit_freq = emit_freq
        # photons limit
        self.photon_limit = photon_limit

class LightSource(Object3D):

    def __init__(self, x=10, y=10, z=1, arr=None, label=-1):
        super().__init__(x, y, z, arr)
        self.light_label = label
        
    
    def initialize_source(self, body_type, body, flag_individual_tropic, tropic, flag_isotropic):

        # mark localizations, where LightSourcePoints will be put 
        if body_type == "rectangular":
            self.fill_cube(self.light_label, start_p=[0.,0.,0.], fill_rec=None, end_p=[1.,1.,1.])

        