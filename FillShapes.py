from PropEnv import PropEnv

class FillShapes():

    def __init__(self):
        pass

    @staticmethod
    def fill_vein(propEnv: PropEnv, z_pos, r=0.15, vein_thickness=0.05):
        x_pos = propEnv.shape[0] // 2
        radius = r * propEnv.shape[1]
        for x_idx in range(propEnv.shape[0]):
            for z_idx in range(propEnv.shape[2]):
                eq = (x_pos - x_idx)**2 + (z_pos - z_idx)**2
                if eq <= (radius - vein_thickness)**2:
                    propEnv.body[x_idx, :, z_idx] = 10
                elif eq <= radius**2:
                    propEnv.body[x_idx, :, z_idx] = 9

