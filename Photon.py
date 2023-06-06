from FeatureSampling import FeatureSampling

class Photon():

    featureSampling = FeatureSampling()
    fun_hop = featureSampling.photon_hop
    fun_theta = featureSampling.photon_theta
    fun_phi = featureSampling.photon_phi

    
    def __init__(self, emit_pos, emit_dir, weight=1.):
        self.pos = emit_pos
        self.dir = emit_dir
        self.weight = weight


