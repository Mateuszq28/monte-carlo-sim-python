from Material import Material, Cuboid, Cylinder
from PropEnvOnMathFormulas import PropEnvOnMathFormulas


class MakeMaterial():
    def __init__(self):
        pass

    # --- MAKE COMPLEX MATERIALS ---

    def default_env(self):
        propEnv = PropEnvOnMathFormulas(x=50, y=50, z=100)
        air = Cuboid(label=1, start_p=[0.0, 0.0, 0.75], end_p=[1.0, 1.0, 1.0], propEnvShape=propEnv.shape)
        water = Cuboid(label=2, start_p=[0.0, 0.0, 0.65], end_p=[1.0, 1.0, 0.75], propEnvShape=propEnv.shape)
        skin = Cuboid(label=8, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 0.65], propEnvShape=propEnv.shape)
        propEnv.material_stack = [air, water, skin]
        self.vein(propEnv, z_pos=0.25)
        return propEnv

    def vein(self, propEnv: PropEnvOnMathFormulas, z_pos, r=0.25, vein_thickness=0.10):
        x_pos_idx = propEnv.shape[0] // 2
        z_pos_idx = int(z_pos * propEnv.shape[2])
        radius = r * propEnv.shape[1]
        vein_thick = vein_thickness * propEnv.shape[1]
        vein_hard_boundary = [x_pos_idx-radius, x_pos_idx+radius, 0, propEnv.shape[1], z_pos_idx-radius, z_pos_idx+radius]
        vein_cyl = Cylinder(label=9, circle_center=[x_pos_idx, 0, z_pos_idx], radius=radius, height_vector=[0, propEnv.shape[1], 0], propEnvShape=propEnv.shape, hard_boundary=vein_hard_boundary)
        blood_hard_boundary = [x_pos_idx-(radius-vein_thick), x_pos_idx+(radius-vein_thick), 0, propEnv.shape[1], z_pos_idx-(radius-vein_thick), z_pos_idx+(radius-vein_thick)]
        blood_cyl = Cylinder(label=10, circle_center=[x_pos_idx, 0, z_pos_idx], radius=radius-vein_thick, height_vector=[0, propEnv.shape[1], 0], propEnvShape=propEnv.shape, hard_boundary=blood_hard_boundary)
        propEnv.material_stack += [vein_cyl, blood_cyl]



