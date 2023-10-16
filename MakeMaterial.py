from Material import Material, Cuboid, Cylinder
from PropEnvVec import PropEnvVec


class MakeMaterial():
    def __init__(self, config):
        self.config = config

    # --- MAKE COMPLEX MATERIALS ---

    def default_env(self):
        propEnv = PropEnvVec(x=50, y=50, z=100)
        air = Cuboid(label=1, start_p=[0.0, 0.0, 0.75], end_p=[1.0, 1.0, 1.0], propEnvShape=propEnv.shape)
        water = Cuboid(label=2, start_p=[0.0, 0.0, 0.65], end_p=[1.0, 1.0, 0.75], propEnvShape=propEnv.shape)
        skin = Cuboid(label=4, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 0.65], propEnvShape=propEnv.shape)
        propEnv.material_stack = [air, water, skin]
        self.vein(propEnv, z_pos=0.25)
        return propEnv

    def vein(self, propEnv: PropEnvVec, z_pos, r=0.25, vein_thickness=0.10):
        x_pos_idx = propEnv.shape[0] // 2
        z_pos_idx = int(z_pos * propEnv.shape[2])
        radius = r * propEnv.shape[1]
        vein_thick = vein_thickness * propEnv.shape[1]
        vein_hard_boundary = [x_pos_idx-radius, x_pos_idx+radius, 0, propEnv.shape[1], z_pos_idx-radius, z_pos_idx+radius]
        vein_cyl = Cylinder(label=7, circle_center=[x_pos_idx, 0, z_pos_idx], radius=radius, height_vector=[0, propEnv.shape[1], 0], propEnvShape=propEnv.shape, hard_boundary=vein_hard_boundary)
        blood_hard_boundary = [x_pos_idx-(radius-vein_thick), x_pos_idx+(radius-vein_thick), 0, propEnv.shape[1], z_pos_idx-(radius-vein_thick), z_pos_idx+(radius-vein_thick)]
        blood_cyl = Cylinder(label=8, circle_center=[x_pos_idx, 0, z_pos_idx], radius=radius-vein_thick, height_vector=[0, propEnv.shape[1], 0], propEnvShape=propEnv.shape, hard_boundary=blood_hard_boundary)
        propEnv.material_stack += [vein_cyl, blood_cyl]
    
    def env_master_thesis_1layers(self):
        bins_per_1_cm = self.config["bins_per_1_cm"]
        # size od propEnv [x,y,z] in cm
        size_cm = [1.5,1.5,2]
        size_bins = [int(round(s_cm * bins_per_1_cm)) for s_cm in size_cm]
        propEnv = PropEnvVec(x=size_bins[0], y=size_bins[1], z=size_bins[2])
        dermis = Cuboid(label=4, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 1.0], propEnvShape=propEnv.shape)
        propEnv.material_stack = [dermis]
        return propEnv
    
    def env_master_thesis_2layers(self):
        bins_per_1_cm = self.config["bins_per_1_cm"]
        # size od propEnv [x,y,z] in cm
        size_cm = [1.5,1.5,2]
        size_bins = [int(round(s_cm * bins_per_1_cm)) for s_cm in size_cm]
        propEnv = PropEnvVec(x=size_bins[0], y=size_bins[1], z=size_bins[2])
        epidermis = Cuboid(label=3, start_p=[0.0, 0.0, 0.75], end_p=[1.0, 1.0, 1.0], propEnvShape=propEnv.shape)
        dermis = Cuboid(label=4, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 0.75], propEnvShape=propEnv.shape)
        propEnv.material_stack = [epidermis, dermis]
        return propEnv

    def env_master_thesis_3layers(self):
        bins_per_1_cm = self.config["bins_per_1_cm"]
        # size od propEnv [x,y,z] in cm
        size_cm = [1.5,1.5,2]
        size_bins = [int(round(s_cm * bins_per_1_cm)) for s_cm in size_cm]
        propEnv = PropEnvVec(x=size_bins[0], y=size_bins[1], z=size_bins[2])
        epidermis = Cuboid(label=3, start_p=[0.0, 0.0, 0.666], end_p=[1.0, 1.0, 1.0], propEnvShape=propEnv.shape)
        dermis = Cuboid(label=4, start_p=[0.0, 0.0, 0.333], end_p=[1.0, 1.0, 0.666], propEnvShape=propEnv.shape)
        fat = Cuboid(label=5, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, 0.333], propEnvShape=propEnv.shape)
        propEnv.material_stack = [epidermis, dermis, fat]
        return propEnv
    
    def env_master_thesis_multilayers(self):
        bins_per_1_cm = self.config["bins_per_1_cm"]
        # layer_names = ["air", "salt water (sweat)", "epidermis", "dermis", "vein", "blood", "vein", "dermis", "fatty subcutaneous tissue"]
        # layer_idx = [1, 2, 3, 4, 7, 8, 7, 4, 5]
        layer_size_cm = [0.01, 0.01, 0.01, 0.22, 0.05, 0.07, 0.05, 0.08, 0.3]
        sum_z = sum(layer_size_cm)
        upper_boundary = [float(sum(layer_size_cm[i:])/sum_z) for i in range(len(layer_size_cm))]
        # size od propEnv [x,y,z] in cm
        size_cm = [sum_z/2, sum_z/2, sum_z]
        size_bins = [int(round(s_cm * bins_per_1_cm)) for s_cm in size_cm]
        propEnv = PropEnvVec(x=size_bins[0], y=size_bins[1], z=size_bins[2])
        # cubes
        air = Cuboid(label=1, start_p=[0.0, 0.0, upper_boundary[1]], end_p=[1.0, 1.0, 1.0], propEnvShape=propEnv.shape)
        water = Cuboid(label=2, start_p=[0.0, 0.0, upper_boundary[2]], end_p=[1.0, 1.0, upper_boundary[1]], propEnvShape=propEnv.shape)
        epidermis = Cuboid(label=3, start_p=[0.0, 0.0, upper_boundary[3]], end_p=[1.0, 1.0, upper_boundary[2]], propEnvShape=propEnv.shape)
        dermis = Cuboid(label=4, start_p=[0.0, 0.0, upper_boundary[8]], end_p=[1.0, 1.0, upper_boundary[3]], propEnvShape=propEnv.shape)
        fat = Cuboid(label=5, start_p=[0.0, 0.0, 0.0], end_p=[1.0, 1.0, upper_boundary[8]], propEnvShape=propEnv.shape)
        # add to env
        propEnv.material_stack = [air, water, epidermis, dermis, fat]
        # vein
        z_pos = float((upper_boundary[4] + upper_boundary[6])/2)
        # radius r is relative to y, not z
        r = ((layer_size_cm[4]+layer_size_cm[5]+layer_size_cm[6])/2) / size_cm[1]
        # same with vein_thickness
        vein_thickness = layer_size_cm[4]/size_cm[1]
        self.vein(propEnv, z_pos=z_pos, r=r, vein_thickness=vein_thickness)
        return propEnv



