from PropEnv import PropEnv

class FillShapes():

    def __init__(self):
        pass

    @staticmethod
    def fill_vein(propEnv: PropEnv, z_pos, r=0.25, vein_thickness=0.10):
        x_pos_idx = propEnv.shape[0] // 2
        z_pos_idx = z_pos * propEnv.shape[2]
        radius = r * propEnv.shape[1]
        vein_thick = vein_thickness * propEnv.shape[1]
        for x_idx in range(propEnv.shape[0]):
            for z_idx in range(propEnv.shape[2]):
                eq = (x_pos_idx - x_idx)**2 + (z_pos_idx - z_idx)**2
                if eq <= (radius - vein_thick)**2:
                    propEnv.body[x_idx, :, z_idx] = 10
                elif eq <= radius**2:
                    propEnv.body[x_idx, :, z_idx] = 9

