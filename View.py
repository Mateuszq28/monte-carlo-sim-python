from Object3D import Object3D

class View():
    def __init__(self):
        pass
        
    def show_body(self, object3D:Object3D, title=""):
        pass

    def show_body_surface(self, object3D:Object3D, title=""):
        pass

    def show_stride(self, object3D:Object3D, stride, title=""):
        if stride is not None:
            new_env = object3D.stride(stride)
            self.show_body(new_env, title=title)