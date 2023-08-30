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
        # ChartMaker.show_simulation_preview_DF(propSetup = propSetup,
        #                                       cs_material="solid",
        #                                       cs_light_source="solid")

        # SHOW PHOTON WEIGHTS (RESULT ENV) + PROP ENV (MATERIAL LABELS)
        # ChartMaker.show_simulation_result_preview_DF(propSetup=propSetup,
        #                                              cs_material="solid",
        #                                              cs_photons=color_scheme)






        # SHOW RESULT ENV
        # ChartMaker.simple_show_object3d(propSetup.resultEnv)
        # ChartMaker.show_resultEnv(resultEnv = propSetup.resultEnv,
        #                           title = "Absorbed energy in volume - color_scheme = " + color_scheme,
        #                           color_scheme = color_scheme)

        





        # SHOW RESULT RECORDS
        sl = list(range(10,20)) + list(range(30,40))
        sl = None
        sl = list(range(10,15))
        sh = propSetup.propEnv.shape
        border_limits = None
        border_limits = [0, sh[0], 0, sh[1], 0, sh[2]]

        select_photon_id = None
        local_color_scheme = "loop"
        local_color_scheme = "photonwise"
        sum_same_idx = False
        ChartMaker.show_resultRecords(resultRecords = propSetup.resultRecords,
                                      title = "Absorbed energy in volume - color_scheme = " + local_color_scheme,
                                      color_scheme = local_color_scheme,
                                      select_photon_id = select_photon_id,
                                      photon_register = propSetup.photon_register,
                                      select_parent = True,
                                      select_child = True,
                                      border_limits = border_limits,
                                      sum_same_idx = sum_same_idx)

        
        if sl is not None:
            for s in sl[:1]:
                select_photon_id = [s]
                local_color_scheme = "photonwise"
                ChartMaker.show_resultRecords(resultRecords = propSetup.resultRecords,
                                              title = "one photon path - color_scheme = " + local_color_scheme,
                                              color_scheme = local_color_scheme,
                                              select_photon_id = select_photon_id,
                                              photon_register = propSetup.photon_register,
                                              select_parent = True,
                                              select_child = True,
                                              border_limits = border_limits)
        
                




        # SUM PROJECTIONS + MAKING .PNG IMAGES
        ChartMaker.sum_projections(resultEnv = propSetup.resultEnv,
                                   bins_per_cm = propSetup.config["bins_per_1_cm"],
                                   color_scheme = color_scheme)

        # [FROM RECORDS] PROJECTIONS + MAKING .PNG IMAGES
        sh = propSetup.resultEnv.shape
        local_color_scheme = "photonwise"
        ChartMaker.projections_from_resultRecords(resultRecords = propSetup.resultRecords,
                                                  input_shape = sh,
                                                  color_scheme = local_color_scheme,
                                                  drop_values = [0, 0.0],
                                                  select_photon_id = None,
                                                  photon_register = propSetup.photon_register,
                                                  select_parent = True,
                                                  select_child = True,
                                                  border_limits = [0, sh[0], 0, sh[1], 0, sh[2]])
        
        if sl is not None:
            for s in sl[:1]:
                select_photon_id = [s]
                local_color_scheme = "photonwise"
                ChartMaker.projections_from_resultRecords(resultRecords = propSetup.resultRecords,
                                                          input_shape = sh,
                                                          color_scheme = local_color_scheme,
                                                          drop_values = None,
                                                          select_photon_id = select_photon_id,
                                                          photon_register = propSetup.photon_register,
                                                          select_parent = True,
                                                          select_child = True,
                                                          border_limits = [0, sh[0], 0, sh[1], 0, sh[2]],
                                                          png_dir = os.path.join("slice_img", "single_photon_projection_img"))
























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
        vis.show_ColorPointDF(df, title="simulation result preview - propagation env + absorbed energy in volume (photon weights), photon color_scheme = " + cs_photons, connect_lines=None)


    @staticmethod
    def heatmap2d(arr: np.ndarray, bins_per_cm, title=None):
        if title is None:
            title = "absorbed fraction"
        plt.imshow(arr, cmap='viridis')
        plt.title(title)
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
            chart_name = "sum_projection_" + name
            vis.show_body(proj, title=chart_name)
            ChartMaker.heatmap2d(arr=proj.body[:,:,0], bins_per_cm=bins_per_cm, title=chart_name)
            proj.save_png(dir=dir, filename=chart_name+".png")


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
            chart_name = "sum_projection_" + name
            ChartMaker.show_resultEnv(resultEnv=proj, title=chart_name, color_scheme=color_scheme)
            ChartMaker.heatmap2d(arr=proj.body[:,:,0], bins_per_cm=bins_per_cm, title=chart_name)
            proj.save_png(dir=dir, filename=chart_name+".png", color_scheme=color_scheme)


    @staticmethod
    def projections_from_resultRecords(resultRecords, input_shape, color_scheme="photonwise", drop_values=None, select_photon_id=None, photon_register=None, select_parent=True, select_child=True, border_limits=None, png_dir=None):
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
        if png_dir is None:
            dir = os.path.join("slice_img", "photonwise_projection_img")
        else:
            dir = png_dir
        vis = ByVispy()
        for projDF, flat_ax, name in zip(projs, flat_axis, projs_names):
            chart_name = "projections_from_resultRecords_" + name
            vis.show_ColorPointDF(projDF, title=chart_name, connect_lines=None)
            flat_z_proj, image_shape = pDF.set_z_as_flat_axis(projDF, flataxis=flat_ax, input_shape=input_shape, post_transform=True, transform_preset=name)
            Print().projectionResultRecordsDF_to_png(flat_z_proj, image_shape=image_shape, dir=dir, filename=chart_name+".png")


    @staticmethod
    def show_resultEnv(resultEnv: Object3D, title=None, color_scheme="loop"):
        colorPointDF = ColorPointDF()
        df = colorPointDF.from_Object3d(resultEnv, color_scheme=color_scheme, drop_values=[0])
        vis = ByVispy()
        if title is None:
            title="Absorbed energy in volume"
        vis.show_ColorPointDF(df, title=title, connect_lines=None)

    @staticmethod
    def show_resultRecords(resultRecords, title=None, color_scheme="photonwise", select_photon_id=None, photon_register=None, select_parent=True, select_child=True, border_limits=None, sum_same_idx = False):
        colorPointDF = ColorPointDF()
        df = colorPointDF.from_resultRecords(resultRecords = resultRecords,
                                             color_scheme = color_scheme,
                                             drop_values = [0],
                                             select_photon_id = select_photon_id,
                                             photon_register = photon_register,
                                             select_parent = select_parent,
                                             select_child = select_child,
                                             border_limits = border_limits,
                                             sum_same_idx = sum_same_idx)
        vis = ByVispy()
        if title is None:
            title="Absorbed energy in volume"
        vis.show_ColorPointDF(df, title=title, connect_lines=None)


    @staticmethod
    def simple_show_object3d(object3d: Object3D):
        vis = ByVispy()
        vis.show_body(object3d)



