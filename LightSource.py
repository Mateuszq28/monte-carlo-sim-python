from Object3D import Object3D

class LightSourcePoint():

    def __init__(self, loc_point, dir_vec, probaFun, photon_limit, emit_freq=1):

        # localization vector
        self.loc_point = loc_point
        #self.direction vector
        self.dir_vec = dir_vec
        #self.probability function
        self.probaFun = probaFun
        # emit frequency - how many photons release, the rest will be ommited
        self.emit_freq = emit_freq
        # photons limit
        self.photon_limit = photon_limit

class LightSource(Object3D):
    
    def __init__(self, label=-1):
        super()
        self.light_label = label

    
    def initialize_source(self, body_type, body, flag_individual_tropic, tropic, flag_isotropic):
        if body_type == "rectangular":
            self.fill_cube(self.light_label, start_p=[], fill_rec=None, end_p=None)