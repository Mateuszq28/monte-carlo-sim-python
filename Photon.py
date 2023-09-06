from FeatureSampling import FeatureSampling

class Photon():

    featureSampling = FeatureSampling()
    fun_hop = featureSampling.photon_hop
    fun_theta = featureSampling.photon_theta
    fun_phi = featureSampling.photon_phi
    static_photon_id_counter = 0

    
    def __init__(self, emit_pos, emit_dir, weight=1.0):
        self.pos = emit_pos
        self.dir = emit_dir
        self.weight = weight
        self.id = Photon.static_photon_id_counter
        Photon.static_photon_id_counter += 1

    def print_me(self):
        print("self.pos", self.pos)
        print("self.dir", self.dir)
        print("self.weight", self.weight)
        print("self.id", self.id)


