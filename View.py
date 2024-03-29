from Object3D import Object3D

class View():
    
    omit_labels = [0, 0.0]

    def __init__(self):
        pass
        
    def show_body(self, object3D:Object3D, title="", omit_labels=None):
        pass

    def show_body_surface(self, object3D:Object3D, title="", omit_labels=None):
        pass

    def show_stride(self, object3D:Object3D, stride, title="", omit_labels=None):
        new_env = object3D.stride(stride)
        self.show_body(new_env, title=title, omit_labels=omit_labels)