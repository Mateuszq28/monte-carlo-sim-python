from FeatureSampling import FeatureSampling

class Photon():

    fun_hop = FeatureSampling.photon_hop
    fun_theta = FeatureSampling.photon_theta
    fun_phi = FeatureSampling.photon_phi

    
    def __init__(self, emit_pos, emit_dir):
        self.pos = emit_pos
        self.dir = emit_dir

