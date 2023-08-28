from SumProjection import SumProjection
from Object3D import Object3D
from PropSetup import PropSetup
from PropEnv import PropEnv
from ProjectionResultRecordsDF import ProjectionResultRecordsDF
from ColorPointDF import ColorPointDF
from ByVispy import ByVispy
from Print import Print
import matplotlib.pyplot as plt
import numpy as np
import os


class ChartMaker():
    def __init__(self):
        pass


    @staticmethod
    def show_all(propSetup: PropSetup, color_scheme="loop"):

        # MAKE AND SHOW OBJECT THAT CONTAIN MATERIAL LABELS + MARKED LIGHT SOURCES LOCATIONS
        # ChartMaker.show_simulation_preview_DF(propSetup, cs_material="solid", cs_light_source="solid")

        # SHOW PHOTON WEIGHTS (RESULT ENV) + PROP ENV (MATERIAL LABELS)
        # ChartMaker.show_simulation_result_preview_DF(propSetup, cs_material="solid", cs_photons="loop")

        # SHOW RESULT ENV
        # ChartMaker.simple_show_object3d(propSetup.resultEnv)
        # ChartMaker.show_resultEnv(propSetup.resultEnv, color_scheme)

        # SUM PROJECTIONS + MAKING .PNG IMAGES
        # ChartMaker.sum_projections(propSetup.resultEnv, propSetup.config["bins_per_1_cm"], color_scheme)

        # [FROM RECORDS] PROJECTIONS + MAKING .PNG IMAGES
        sh = propSetup.resultEnv.shape
        ChartMaker.projections_from_resultRecords(resultRecords = propSetup.resultRecords,
                                                  input_shape = sh,
                                                  color_scheme = "photonwise",
                                                  drop_values = None,
                                                  select_photon_id = None,
                                                  photon_register = propSetup.photon_register,
                                                  select_parent = True,
                                                  select_child = True,
                                                  border_limits = [0, sh[0], 0, sh[1], 0, sh[2]])

        # SHOW RESULT RECORDS
        sl = list(range(10,20)) + list(range(30,40))
        sl = None
        sl = list(range(10,15))
        sh = propSetup.propEnv.shape
        border_limits = [0, sh[0], 0, sh[1], 0, sh[2]]
        border_limits = None

        select_photon_id = None
        ChartMaker.show_resultRecords(resultRecords = propSetup.resultRecords,
                                      color_scheme = "photonwise",
                                      select_photon_id = select_photon_id,
                                      photon_register = propSetup.photon_register,
                                      select_parent = True,
                                      select_child = True,
                                      border_limits = border_limits)

        if sl is not None:
            for s in sl:
                select_photon_id = [s]
                ChartMaker.show_resultRecords(resultRecords = propSetup.resultRecords,
                                              color_scheme = "photonwise",
                                              select_photon_id = select_photon_id,
                                              photon_register = propSetup.photon_register,
                                              select_parent = True,
                                              select_child = True,
                                              border_limits = border_limits)
























    @staticmethod
    def show_simulation_preview(propSetup: PropSetup, color_scheme="loop"):
        simulation_preview = propSetup.make_preview()
        colorPointDF = ColorPointDF()
        df = colorPointDF.from_Object3d(simulation_preview, color_scheme=color_scheme, drop_values=[0])
        vis = ByVispy()
        vis.show_ColorPointDF(df, title="simulation preview - propagation env + light sources", connect_lines=None)


    @staticmethod
    def show_simulation_result_preview(propSetup: PropSetup, color_scheme="loop"):
        simulation_result_preview = propSetup.make_result_preview()
        colorPointDF = ColorPointDF()
        df = colorPointDF.from_Object3d(simulation_result_preview, color_scheme=color_scheme, drop_values=[0])
        vis = ByVispy()
        vis.show_ColorPointDF(df, title="simulation result preview - propagation env + absorbed energy in volume (photon weights)", connect_lines=None)


    @staticmethod
    def show_simulation_preview_DF(propSetup: PropSetup, cs_material="solid", cs_light_source="solid"):
        df = propSetup.make_preview_DF(cs_material, cs_light_source)
        vis = ByVispy()
        vis.show_ColorPointDF(df, title="simulation preview - propagation env + light sources", connect_lines=None)


    @staticmethod
    def show_simulation_result_preview_DF(propSetup: PropSetup, cs_material="solid", cs_photons="loop"):
        df = propSetup.make_result_preview_DF(cs_material, cs_photons)
        vis = ByVispy()
        vis.show_ColorPointDF(df, title="simulation result preview - propagation env + absorbed energy in volume (photon weights)", connect_lines=None)


    @staticmethod
    def heatmap2d(arr: np.ndarray, bins_per_cm):
        plt.imshow(arr, cmap='viridis')
        plt.title("absorbed fraction")
        cb = plt.colorbar()
        cb.set_label(r'$\mathregular{\frac{1}{cm^3}}$')
        # plt.xlabel = r'$\mathregular{x \frac{1}{bins_per_cm} cm}$'.replace("bins_per_cm", str(bins_per_cm))
        # plt.ylabel = r'$\mathregular{x \frac{1}{bins_per_cm} cm}$'.replace("bins_per_cm", str(bins_per_cm))
        plt.show()


    @staticmethod
    def heatmap2d_(arr: np.ndarray, bins_per_cm):
        fig, ax = plt.subplots(1,1)

        # img = ax.imshow(arr, extent=[-1,1,-1,1])
        img = ax.imshow(arr)

        x_label_list = ax.get_xticks() / bins_per_cm
        y_label_list = ax.get_yticks() / bins_per_cm

        print(ax.get_xticks())
        print(ax.get_yticks())

        # ax.set_xticks([-0.75,-0.25,0.25,0.75])
        # ax.set_yticks([-0.75,-0.25,0.25,0.75])

        ax.set_xticklabels(x_label_list)
        ax.set_yticklabels(y_label_list)

        cb = fig.colorbar(img)

        cb.set_label(r'$\mathregular{\frac{1}{cm^3}}$')

        ax.set_xlabel("cm")
        ax.set_ylabel("cm")


    @staticmethod
    def sum_projections_show_body(resultEnv, bins_per_cm):
        sump = SumProjection()
        x_high = sump.x_high(resultEnv)
        x_low = sump.x_low(resultEnv)
        y_high = sump.y_high(resultEnv)
        y_low = sump.y_low(resultEnv)
        z_high = sump.z_high(resultEnv)
        z_low = sump.z_low(resultEnv)
        projs = [x_high, x_low, y_high, y_low, z_high, z_low]
        projs_names = ["x_high", "x_low", "y_high", "y_low", "z_high", "z_low"]
        # used in loop
        dir = os.path.join("slice_img", "sum_projection_img")
        vis = ByVispy()
        for proj, name in zip(projs, projs_names):
            vis.show_body(proj)
            ChartMaker.heatmap2d(proj.body[:,:,0], bins_per_cm)
            proj.save_png(dir=dir, filename=name+".png")


    @staticmethod
    def sum_projections(resultEnv: PropEnv, bins_per_cm, color_scheme="loop"):
        sump = SumProjection()
        x_high = sump.x_high(resultEnv)
        x_low = sump.x_low(resultEnv)
        y_high = sump.y_high(resultEnv)
        y_low = sump.y_low(resultEnv)
        z_high = sump.z_high(resultEnv)
        z_low = sump.z_low(resultEnv)
        projs = [x_high, x_low, y_high, y_low, z_high, z_low]
        projs_names = ["x_high", "x_low", "y_high", "y_low", "z_high", "z_low"]
        # used in loop
        dir = os.path.join("slice_img", "sum_projection_img")
        vis = ByVispy()
        for proj, name in zip(projs, projs_names):
            ChartMaker.show_resultEnv(proj, color_scheme)
            ChartMaker.heatmap2d(proj.body[:,:,0], bins_per_cm)
            proj.save_png(dir=dir, filename=name+".png", color_scheme=color_scheme)


    @staticmethod
    def projections_from_resultRecords(resultRecords, input_shape, color_scheme="photonwise", drop_values=None, select_photon_id=None, photon_register=None, select_parent=True, select_child=True, border_limits=None):
        cDF = ColorPointDF()
        df = cDF.from_resultRecords(resultRecords = resultRecords,
                                    color_scheme = color_scheme,
                                    drop_values = drop_values,
                                    select_photon_id = select_photon_id,
                                    photon_register = photon_register,
                                    select_parent = select_parent,
                                    select_child = select_child,
                                    border_limits = border_limits)
        pDF = ProjectionResultRecordsDF()
        x_high, x_high_flat_axis = pDF.x_high(df, input_shape)
        x_low, x_low_flat_axis = pDF.x_low(df, input_shape)
        y_high, y_high_flat_axis = pDF.y_high(df, input_shape)
        y_low, y_low_flat_axis = pDF.y_low(df, input_shape)
        z_high, z_high_flat_axis = pDF.z_high(df, input_shape)
        z_low, z_low_flat_axis = pDF.z_low(df, input_shape)
        projs = [x_high, x_low, y_high, y_low, z_high, z_low]
        flat_axis = [x_high_flat_axis, x_low_flat_axis, y_high_flat_axis, y_low_flat_axis, z_high_flat_axis, z_low_flat_axis]
        projs_names = ["x_high", "x_low", "y_high", "y_low", "z_high", "z_low"]
        # used in loop
        dir = os.path.join("slice_img", "photonwise_projection_img")
        vis = ByVispy()
        for proj, flat_ax, name in zip(projs, flat_axis, projs_names):
            vis.show_ColorPointDF(proj, title="Absorbed energy in volume", connect_lines=None)
            flat_z_proj = pDF.set_z_as_flat_axis(proj, flat_ax)
            image_shape = input_shape.copy().remove(flat_ax)
            Print().projectionResultRecordsDF_to_png(flat_z_proj, image_shape, dir=dir, filename=name+".png")


    @staticmethod
    def show_resultEnv(resultEnv: Object3D, color_scheme="loop"):
        colorPointDF = ColorPointDF()
        df = colorPointDF.from_Object3d(resultEnv, color_scheme=color_scheme, drop_values=[0])
        vis = ByVispy()
        vis.show_ColorPointDF(df, title="Absorbed energy in volume", connect_lines=None)

    @staticmethod
    def show_resultRecords(resultRecords, color_scheme="photonwise", select_photon_id=None, photon_register=None, select_parent=True, select_child=True, border_limits=None):
        colorPointDF = ColorPointDF()
        df = colorPointDF.from_resultRecords(resultRecords = resultRecords,
                                             color_scheme = color_scheme,
                                             drop_values = [0],
                                             select_photon_id = select_photon_id,
                                             photon_register = photon_register,
                                             select_parent = select_parent,
                                             select_child = select_child,
                                             border_limits = border_limits)
        vis = ByVispy()
        vis.show_ColorPointDF(df, title="Absorbed energy in volume", connect_lines=None)


    @staticmethod
    def simple_show_object3d(object3d: Object3D):
        vis = ByVispy()
        vis.show_body(object3d)



