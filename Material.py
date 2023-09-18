class Material():
    def __init__(self, label, fun_in, fun_boundary, fun_intersect, fun_plane_normal_vec):
        self.label = label
        self.fun_in = fun_in
        self.fun_boundary = fun_boundary
        self.fun_intersect = fun_intersect
        self.fun_plane_normal_vec = fun_plane_normal_vec