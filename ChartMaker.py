from SumProjection import SumProjection
from Object3D import Object3D
from PropSetup import PropSetup
from PropEnv import PropEnv
from ProjectionResultRecordsDF import ProjectionResultRecordsDF
from FeatureSampling import MyRandom
from ColorPointDF import ColorPointDF
from ByVispy import ByVispy
from Print import Print
from ArrowsDF import ArrowsDF
from ProjectionArrowsDF import ProjectionArrowsDF
import matplotlib.pyplot as plt
from matplotlib import cm, rc
import pandas as pd
# from IPython.display import display
import numpy as np
import os
import time
from Test import Test
from PlaneTriangles import PlaneTriangles


class ChartMaker():

    screen_px = [1920, 1080]
    inch = 15.6
    fig_size_px = [800, 800]

    dpi = np.linalg.norm(screen_px) / inch
    fig_size = np.array(fig_size_px) / dpi

    def __init__(self):
        pass


    @staticmethod
    def matplotlib_config():
        # bigger font on charts
        label_multiplier = 2.2
        font = {
            # 'family': 'monospace',
            # 'weight': 'bold',
            'size': 10 * label_multiplier
        }
        rc('font', **font)

        plt.rcParams['axes.titley'] = 1.0
        plt.rcParams['axes.titlepad'] = 15
        plt.rcParams['axes.linewidth'] = 0.8 * label_multiplier

        plt.rcParams['xtick.major.size'] = 3.5 * label_multiplier
        plt.rcParams['xtick.minor.size'] = 2 * label_multiplier
        plt.rcParams['xtick.major.width'] = 0.8 * label_multiplier
        plt.rcParams['xtick.minor.width'] = 0.6 * label_multiplier
        plt.rcParams['xtick.major.pad'] = 3.5 * label_multiplier
        plt.rcParams['xtick.minor.pad'] = 3.4 * label_multiplier

        plt.rcParams['ytick.major.size'] = 3.5 * label_multiplier
        plt.rcParams['ytick.minor.size'] = 2 * label_multiplier
        plt.rcParams['ytick.major.width'] = 0.8 * label_multiplier
        plt.rcParams['ytick.minor.width'] = 0.6 * label_multiplier
        plt.rcParams['ytick.major.pad'] = 3.5 * label_multiplier
        plt.rcParams['ytick.minor.pad'] = 3.4 * label_multiplier


    @staticmethod
    def show_all(propSetup: PropSetup, color_scheme="loop", do_connect_lines=False, color_points_by_root=False, color_arrows_by_root=False, do_triangled_planes=False, draw_planes_from_material_stack=False, use_triangled_planes_from_file=True):

        # MATPLOTLIB CHARTS CONFIG
        ChartMaker.matplotlib_config()

        # TEST DUPLICATES IN RECORDS
        turn_on_test = False
        if turn_on_test:
            propSetup.resultRecords.insert(0, [100, 0, 0, 0, 10.0]) # type: ignore
            propSetup.resultRecords.insert(0, [100, 0, 0, 0, 20.0]) # type: ignore
            propSetup.resultRecords.insert(0, [100, 0, 0, 0, 10.0]) # type: ignore
            propSetup.resultRecords.insert(0, [300, 0, 0, 0, 30.0]) # type: ignore
            propSetup.resultRecords.insert(0, [200, 0, 0, 0, 5.0]) # type: ignore

        
        # SHOW STATISTICS
        print()
        ChartMaker.show_statistics(propSetup)
        print()


        # PREPARE STANDARD ARROWS
        if do_connect_lines:
            standard_connect_lines = ChartMaker.prepare_standard_connect_lines(propSetup, color_by_root=color_arrows_by_root)
            standard_hide_points = False
            # Test.Test_ArrowsDF.check_arrow_dirs(standard_connect_lines)
        else:
            standard_connect_lines = None
            standard_hide_points = False


        # PREPARE TRIANGLED PLANES
        if True:
            if do_triangled_planes:
                if use_triangled_planes_from_file:
                    triangls_dict = PlaneTriangles.load_json(propSetup.result_folder)
                    # if file not exsists triangls_dict is None
                else:
                    triangls_dict = None
                if triangls_dict is None:
                    start_time = time.time()
                    triangls_dict = PlaneTriangles().from_propEnv(propSetup.propEnv)
                    end_time = time.time()
                    print()
                    print("Plane triangles calculation time:", end_time-start_time)
                    print()
                    PlaneTriangles.save_json(triangls_dict, propSetup.result_folder)
                else:
                    print()
                    print("Triangles successfully loaded from json file.")
                    print()
                ByVispy.triangled_planes_dict = triangls_dict


        # ASSIGN MATERIAL STACK TO ByVispy
        if draw_planes_from_material_stack:
            ByVispy.material_stack = propSetup.propEnv.material_stack # type: ignore




        # SHOW JUST BOUNDARY PLANES + LIGHT SOURCE
        ChartMaker.show_empty_simulation_preview_DF(propSetup = propSetup,
                                                    cs_light_source="solid")

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
        #                           color_scheme = color_scheme,
        #                           connect_lines = standard_connect_lines)
        # ChartMaker.simple_show_object3d_asVolume(propSetup.resultEnv, title="resultEnv as Volume")

        

        # SHOW RESULT RECORDS
        sl = list(range(10,20)) + list(range(30,40))
        sl = list(range(10,15))
        sl = None
        sl = [4, 48]
        sl = list(range(0,100))
        sl = [0,1]
        sl = [0, 16, 22, 38, 50, 68, 75, 78, 79, 91, 97, 98]
        sh = propSetup.propEnv.shape
        border_limits = None
        border_limits = [0, sh[0], 0, sh[1], 0, sh[2]]

        select_photon_id = [97, 98]
        very_close_photons = [0, 16, 22, 38, 50, 68, 75, 78, 79, 91, 97, 98]
        select_photon_id = very_close_photons
        select_photon_id = None
        select_photon_id = sl
        local_color_scheme = "loop"
        local_color_scheme = "photonwise"
        ChartMaker.show_resultRecords(resultRecords = propSetup.resultRecords,
                                      title = "Absorbed energy in volume - color_scheme = " + local_color_scheme,
                                      color_scheme = local_color_scheme,
                                      select_photon_id = select_photon_id,
                                      photon_register = propSetup.photon_register,
                                      select_parent = True,
                                      select_child = True,
                                      border_limits = border_limits,
                                      sum_same_idx = False,
                                      do_connect_lines = do_connect_lines,
                                      color_points_by_root = color_points_by_root,
                                      color_arrows_by_root = color_arrows_by_root)

        

        if sl is not None:
            take_group = 1
            sl = sl[:3]
            for i in range(len(sl)+1-take_group):
                select_photon_id = sl[i:i+take_group]
                local_color_scheme = "photonwise"
                ChartMaker.show_resultRecords(resultRecords = propSetup.resultRecords,
                                              title = "({}) one photon path - color_scheme = ".format(i) + local_color_scheme,
                                              color_scheme = local_color_scheme,
                                              select_photon_id = select_photon_id,
                                              photon_register = propSetup.photon_register,
                                              select_parent = True,
                                              select_child = True,
                                              border_limits = border_limits,
                                              sum_same_idx = False,
                                              do_connect_lines = do_connect_lines,
                                              color_points_by_root = color_points_by_root,
                                              color_arrows_by_root = color_arrows_by_root)
        




        # SUM PROJECTIONS + MAKING .PNG IMAGES
        # old
        # ChartMaker.sum_projections_show_body(resultEnv = propSetup.resultEnv,
        #                                      bins_per_cm = propSetup.config["bins_per_1_cm"])
        # new
        # local_color_scheme = color_scheme
        # local_color_scheme = "logarithmic"
        # ChartMaker.sum_projections(resultEnv = propSetup.resultEnv, # type: ignore
        #                            bins_per_cm = propSetup.config["bins_per_1_cm"], # type: ignore
        #                            color_scheme = local_color_scheme,
        #                            show = True,
        #                            connect_lines = standard_connect_lines,
        #                            hide_points = standard_hide_points)



        # [FROM RECORDS] PROJECTIONS + MAKING .PNG IMAGES
        # sh = propSetup.resultShape
        # local_color_scheme = color_scheme
        # local_color_scheme = "photonwise"
        # drop_values = [0, 0.0]
        # drop_values = None
        # local_reset_colors = local_color_scheme
        # local_reset_colors = None
        # local_reset_colors = "logarithmic"
        # ChartMaker.projections_from_resultRecords(resultRecords = propSetup.resultRecords,
        #                                           input_shape = sh,
        #                                           color_scheme = local_color_scheme,
        #                                           drop_values = drop_values,
        #                                           select_photon_id = None,
        #                                           photon_register = propSetup.photon_register,
        #                                           select_parent = True,
        #                                           select_child = True,
        #                                           border_limits = [0, sh[0], 0, sh[1], 0, sh[2]],
        #                                           png_dir = None,
        #                                           sum_same_idx = False,
        #                                           sum_axis = False,
        #                                           reset_png_colors = None,
        #                                           show = False,
        #                                           title_prefix = "",
        #                                           do_connect_lines = do_connect_lines,
        #                                           reset_colors = local_reset_colors,
        #                                           color_points_by_root = color_points_by_root,
        #                                           color_arrows_by_root = color_arrows_by_root)
        
        # if sl is not None:
        #     take_group = 1
        #     for i in range(len(sl)+1-take_group):
        #         select_photon_id = [sl[i]]
        #         select_photon_id = sl[i:i+take_group]
        #         local_color_scheme = "photonwise"
        #         ChartMaker.projections_from_resultRecords(resultRecords = propSetup.resultRecords,
        #                                                   input_shape = sh,
        #                                                   color_scheme = local_color_scheme,
        #                                                   drop_values = None,
        #                                                   select_photon_id = select_photon_id,
        #                                                   photon_register = propSetup.photon_register,
        #                                                   select_parent = True,
        #                                                   select_child = True,
        #                                                   border_limits = [0, sh[0], 0, sh[1], 0, sh[2]],
        #                                                   png_dir = os.path.join("slice_img", "single_photon_projection_img"),
        #                                                   sum_same_idx = False,
        #                                                   sum_axis = False,
        #                                                   reset_png_colors = None,
        #                                                   show = False,
        #                                                   title_prefix = "({}) ".format(i),
        #                                                   do_connect_lines = do_connect_lines,
        #                                                   reset_colors = local_reset_colors,
        #                                                   color_points_by_root = color_points_by_root,
        #                                                   color_arrows_by_root = color_arrows_by_root)
























    @staticmethod
    def show_simulation_preview(propSetup: PropSetup, color_scheme="loop"):
        simulation_preview = propSetup.make_preview()
        colorPointDF = ColorPointDF()
        df = colorPointDF.from_Object3d(simulation_preview, color_scheme=color_scheme, drop_values=[0])
        vis = ByVispy()
        vis.show_ColorPointDF(df, title="simulation preview - propagation env + light sources", connect_lines=None, draw_plane_triangles=False)


    @staticmethod
    def show_simulation_result_preview(propSetup: PropSetup, color_scheme="loop"):
        simulation_result_preview = propSetup.make_result_preview()
        colorPointDF = ColorPointDF()
        df = colorPointDF.from_Object3d(simulation_result_preview, color_scheme=color_scheme, drop_values=[0])
        vis = ByVispy()
        vis.show_ColorPointDF(df, title="simulation result preview - propagation env + absorbed energy in volume (photon weights)", connect_lines=None, draw_plane_triangles=False)


    @staticmethod
    def show_simulation_preview_DF(propSetup: PropSetup, cs_material="solid", cs_light_source="solid"):
        if PropSetup.flag_use_propenv_on_formulas:
            print("Skipped show_simulation_preview_DF - propEnv is on formulas")
        else:
            df, arrows_DF = propSetup.make_preview_DF(cs_material, cs_light_source)
            vis = ByVispy()
            vis.show_ColorPointDF(df, title="simulation preview - propagation env + light sources", connect_lines=None, draw_plane_triangles=False)


    @staticmethod
    def show_empty_simulation_preview_DF(propSetup: PropSetup, cs_light_source="solid"):
        if PropSetup.flag_use_propenv_on_formulas:
            draw_planes_from_material_stack = True
            draw_plane_triangles = False
        else:
            draw_planes_from_material_stack = False
            draw_plane_triangles = True
        df, arrows_DF = propSetup.make_empty_preview_DF(cs_light_source)
        vis = ByVispy()
        vis.show_ColorPointDF(df, title="boundary planes + light source", hide_points=False, connect_lines=arrows_DF, draw_plane_triangles=draw_plane_triangles, draw_planes_from_material_stack=draw_planes_from_material_stack)


    @staticmethod
    def show_simulation_result_preview_DF(propSetup: PropSetup, cs_material="solid", cs_photons="loop"):
        if propSetup.resultEnv is None:
            print("Skipped show_simulation_result_preview_DF - propSetup.resultEnv is None")
        elif PropSetup.flag_use_propenv_on_formulas:
            print("Skipped show_simulation_preview_DF - propEnv is on formulas")
        else:
            df = propSetup.make_result_preview_DF(cs_material, cs_photons)
            vis = ByVispy()
            vis.show_ColorPointDF(df, title="simulation result preview - propagation env + absorbed energy in volume (photon weights), photon color_scheme = " + cs_photons, connect_lines=None, draw_plane_triangles=False)


    @staticmethod
    def heatmap2d(arr: np.ndarray, bins_per_cm, title=None):
        # WARNING! if it's a sum along axis, remmember to divide by len(of this axis) (average)
        # do it before giving it to heatmap2d function
        # hint for debugging: search for this comment and go through function references
        if title is None:
            title = "absorbed fraction"
        extent=[0, arr.shape[1]/bins_per_cm, 0, arr.shape[0]/bins_per_cm]
        
        xlab = ""
        ylab = ""
        if "x_high" in title:
            xlab = "y [cm]"
            ylab = "z [cm]"
            title = "Współczynnik fluencji względnej (x_high)"
        if "y_high" in title:
            xlab = "x [cm]"
            ylab = "z [cm]"
            title = "Współczynnik fluencji względnej (y_high)"
        if "z_high" in title:
            xlab = "x [cm]"
            ylab = "y [cm]"
            title = "Współczynnik fluencji względnej (z_high)"
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)

        # in past here was arr/1000
        plt.imshow(arr, cmap='viridis', interpolation="none", extent=extent) # type: ignore

        cb = plt.colorbar(pad=0.010)
        cb.set_label(r'$ 1/cm^2 $')

        manager = plt.get_current_fig_manager()
        manager.window.showMaximized() # type: ignore

        plt.show()


    @staticmethod
    def heatmap2d_log10(arr: np.ndarray, bins_per_cm, title=None):
        # WARNING! if it's a sum along axis, remmember to divide by len(of this axis) (average)
        # do it before giving it to heatmap2d function
        # hint for debugging: search for this comment and go through function references
        if title is None:
            title = "absorbed fraction"

        # skip first tick on x axis
        # ax = plt.gca()
        # xticks = ax.xaxis.get_major_ticks()
        # xticks[0].label1.set_visible(False)

        # TICKS ON X, Y AXIS
        # arr = np.flip(arr, axis=0)
        extent=[0, arr.shape[1]/bins_per_cm, 0, arr.shape[0]/bins_per_cm]
        # origin='lower'

        xlab = ""
        ylab = ""
        if "x_high" in title:
            xlab = "y [cm]"
            ylab = "z [cm]"
            title = "Współczynnik fluencji względnej (x_high)"
        if "y_high" in title:
            xlab = "x [cm]"
            ylab = "z [cm]"
            title = "Współczynnik fluencji względnej (y_high)"
        if "z_high" in title:
            xlab = "x [cm]"
            ylab = "y [cm]"
            title = "Współczynnik fluencji względnej (z_high)"
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        # title = r'$\log_{10}arr$'
        plt.title(title)

        plt.imshow(arr, cmap='viridis', norm="log", interpolation="none", extent=extent) # type: ignore

        # cb = plt.colorbar(fraction=0.046, pad=0.04)
        cb = plt.colorbar(pad=0.010)
        # cb.set_label(r'$ \frac{1}{cm^2} $')
        cb.set_label(r'$ 1/cm^2 $')

        manager = plt.get_current_fig_manager()
        manager.window.showMaximized() # type: ignore
        # manager.canvas.toolbar.save_figure()

        plt.show()


    @staticmethod
    def plot2_heatmap2d(arr1: np.ndarray, arr2: np.ndarray, title1=None, title2=None):
        # WARNING! if it's a sum along axis, remmember to divide by len(of this axis) (average)
        # do it before giving it to heatmap2d function
        # hint for debugging: search for this comment and go through function references
        cmap = cm.get_cmap('viridis', 256)
        fig, axs = plt.subplots(1, 2, constrained_layout=True)
        arrs = [arr1, arr2]
        tits = [title1, title2]
        for ax, data, tit in zip(axs, arrs, tits):
            min_value = np.min(data)
            max_value = np.max(data)
            psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=min_value, vmax=max_value)
            fig.colorbar(psm, ax=ax)
            ax.set_title(tit)
        plt.show()


    @staticmethod
    def heatmap2d_(arr: np.ndarray, bins_per_cm):
        # WARNING! if it's a sum along axis, remmember to divide by len(of this axis) (average)
        # do it before giving it to heatmap2d function
        # hint for debugging: search for this comment and go through function references
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

        cb.set_label(r'$\mathregular{\frac{1}{cm^2}}$')

        ax.set_xlabel("cm")
        ax.set_ylabel("cm")


    @staticmethod
    def sum_projections_show_body(resultEnv, bins_per_cm):
        if resultEnv is None:
            print("Skipped sum_projections_show_body - resultEnv is None")
        else:
            # SumProjection functions have already have imlemented normalizing (scaling down) along the face axis (average)
            sump = SumProjection()
            funs = [sump.x_high, sump.x_low, sump.y_high, sump.y_low, sump.z_high, sump.z_low]
            projs_names = ["x_high", "x_low", "y_high", "y_low", "z_high", "z_low"]
            # used in loop
            dir = os.path.join("slice_img", "sum_projection_img")
            vis = ByVispy()
            for fun, name in zip(funs, projs_names):
                proj = fun(resultEnv)
                chart_name = "sum_projection_" + name
                vis.show_body(proj, title=chart_name)
                ChartMaker.heatmap2d(arr=proj.body[:,:,0]/len(proj.body[0,0,:]), bins_per_cm=bins_per_cm, title=chart_name)
                ChartMaker.heatmap2d_log10(arr=proj.body[:,:,0]/len(proj.body[0,0,:]), bins_per_cm=bins_per_cm, title=chart_name)
                proj.save_png(dir=dir, filename=chart_name+".png")


    @staticmethod
    def sum_projections(resultEnv: PropEnv, bins_per_cm, color_scheme="loop", show=True, connect_lines=None, hide_points=False):
        if resultEnv is None:
            print("Skipped sum_projections - resultEnv is None")
        else:
            # SumProjection functions have already have imlemented normalizing (scaling down) along the face axis (average)
            sump = SumProjection()
            padf = ProjectionArrowsDF()
            funs = [sump.x_high, sump.x_low, sump.y_high, sump.y_low, sump.z_high, sump.z_low]
            arrow_funs = [padf.x_high, padf.x_low, padf.y_high, padf.y_low, padf.z_high, padf.z_low]
            projs_names = ["x_high", "x_low", "y_high", "y_low", "z_high", "z_low"]
            take_idx = [0, 2, 4]
            # used in loop
            dir = os.path.join("slice_img", "sum_projection_img")
            for fun, line_fun, name, i in zip(funs, arrow_funs, projs_names, range(len(projs_names))):
                if i not in take_idx:
                    continue
                proj = fun(resultEnv)
                chart_name = "sum_projection_" + name
                # add arrows
                if connect_lines is not None:
                    flat_z_connect_lines, _, _ = line_fun(connect_lines, resultEnv.shape, set_z_as_flat_axis=True, set_z_idx_to_0=True)
                else:
                    flat_z_connect_lines = None
                if show:
                    # ChartMaker.show_resultEnv(resultEnv=proj, title=chart_name, color_scheme=color_scheme, connect_lines=flat_z_connect_lines, hide_points=hide_points, draw_plane_triangles=False)
                    ChartMaker.heatmap2d(arr=proj.body[:,:,0]/len(proj.body[0,0,:]), bins_per_cm=bins_per_cm, title=chart_name)
                    ChartMaker.heatmap2d_log10(arr=proj.body[:,:,0]/len(proj.body[0,0,:]), bins_per_cm=bins_per_cm, title=chart_name)
                proj.save_png(dir=dir, filename=chart_name+".png", color_scheme=color_scheme, connect_lines=flat_z_connect_lines, hide_points=hide_points)


    @staticmethod
    def projections_from_resultRecords(resultRecords, input_shape, color_scheme="photonwise", drop_values=None, select_photon_id=None, photon_register=None, select_parent=True, select_child=True, border_limits=None, png_dir=None, sum_same_idx=False, sum_axis=False, reset_png_colors=None, show=True, title_prefix="", do_connect_lines=False, reset_colors=None, color_points_by_root=False, color_arrows_by_root=False):
        if resultRecords is None:
            print("Skipped projections_from_resultRecords - resultRecords is None")
        else:
            cDF = ColorPointDF()
            df = cDF.from_resultRecords(resultRecords = resultRecords,
                                        color_scheme = color_scheme,
                                        drop_values = drop_values,
                                        select_photon_id = select_photon_id,
                                        photon_register = photon_register,
                                        select_parent = select_parent,
                                        select_child = select_child,
                                        border_limits = border_limits,
                                        sum_same_idx = sum_same_idx,
                                        sort = True,
                                        color_by_root=color_points_by_root)
            if do_connect_lines:
                df_arrows = cDF.from_resultRecords(resultRecords = resultRecords,
                                                color_scheme = "photonwise",
                                                drop_values = None,
                                                select_photon_id = select_photon_id,
                                                photon_register = photon_register,
                                                select_parent = select_parent,
                                                select_child = select_child,
                                                border_limits = None,
                                                sum_same_idx = False,
                                                sort = False,
                                                color_by_root=color_arrows_by_root)
                ADF = ArrowsDF()
                connect_lines = ADF.fromDF(df_arrows, photon_register=photon_register, add_start_arrows=True, color_by_root=color_arrows_by_root)
                hide_points = False
            else:
                connect_lines = None
                hide_points = False
            # ProjectionResultRecordsDF functions have already have imlemented normalizing (scaling down) along the face axis (average)
            pDF = ProjectionResultRecordsDF()
            funs = [pDF.x_high, pDF.x_low, pDF.y_high, pDF.y_low, pDF.z_high, pDF.z_low]
            projs_names = ["x_high", "x_low", "y_high", "y_low", "z_high", "z_low"]
            # used in loop
            if png_dir is None:
                dir = os.path.join("slice_img", "photonwise_projection_img")
            else:
                dir = png_dir
            vis = ByVispy()
            for proj_fun, name in zip(funs, projs_names):
                projDF, flat_ax, proj_connect_lines = proj_fun(df, input_shape, sum_axis=sum_axis, reset_colors=reset_colors, connect_lines=connect_lines)
                chart_name = title_prefix + "projections_from_resultRecords_" + name
                if show:
                    vis.show_ColorPointDF(projDF, title=chart_name, connect_lines=proj_connect_lines, hide_points=hide_points, draw_plane_triangles=False)
                flat_z_proj, image_shape, flat_z_connect_lines = pDF.set_z_as_flat_axis(projDF, flataxis=flat_ax, input_shape=input_shape, post_transform=True, transform_preset=name, reset_colors=reset_png_colors, connect_lines=proj_connect_lines)
                Print().projectionResultRecordsDF_to_png(flat_z_proj, image_shape=image_shape, dir=dir, filename=chart_name+".png", connect_lines=flat_z_connect_lines, hide_points=hide_points)


    @staticmethod
    def show_resultEnv(resultEnv: Object3D, title=None, color_scheme="loop", connect_lines=None, hide_points=False, draw_plane_triangles=True):
        if resultEnv is None:
            print("Skipped show_resultEnv - resultEnv is None")
        else:
            colorPointDF = ColorPointDF()
            df = colorPointDF.from_Object3d(resultEnv, color_scheme=color_scheme, drop_values=[0, 0.0])
            vis = ByVispy()
            if title is None:
                title="Absorbed energy in volume"
            vis.show_ColorPointDF(df, title=title, connect_lines=connect_lines, hide_points=hide_points, draw_plane_triangles=draw_plane_triangles)

    @staticmethod
    def show_resultRecords(resultRecords, title=None, color_scheme="photonwise", select_photon_id=None, photon_register=None, select_parent=True, select_child=True, border_limits=None, sum_same_idx=False, do_connect_lines=False, color_points_by_root=False, color_arrows_by_root=False):
        if resultRecords is None:
            print("Skipped show_resultRecords - resultRecords is None")
        else:
            colorPointDF = ColorPointDF()
            df = colorPointDF.from_resultRecords(resultRecords = resultRecords,
                                                color_scheme = color_scheme,
                                                drop_values = None,
                                                select_photon_id = select_photon_id,
                                                photon_register = photon_register,
                                                select_parent = select_parent,
                                                select_child = select_child,
                                                border_limits = border_limits,
                                                sum_same_idx = sum_same_idx,
                                                sort = True,
                                                color_by_root = color_points_by_root)
            if do_connect_lines:
                df_arrows = colorPointDF.from_resultRecords(resultRecords = resultRecords,
                                                            color_scheme = "photonwise",
                                                            drop_values = None,
                                                            select_photon_id = select_photon_id,
                                                            photon_register = photon_register,
                                                            select_parent = select_parent,
                                                            select_child = select_child,
                                                            border_limits = None,
                                                            sum_same_idx = False,
                                                            sort = False,
                                                            color_by_root = color_arrows_by_root)
                ADF = ArrowsDF()
                connect_lines = ADF.fromDF(df_arrows, photon_register=photon_register, add_start_arrows=True, color_by_root=color_arrows_by_root)
                hide_points = False
            else:
                connect_lines = None
                hide_points = False
            if title is None:
                title="Absorbed energy in volume"
            vis = ByVispy()
            vis.show_ColorPointDF(df, title=title, connect_lines=connect_lines, hide_points=hide_points, draw_plane_triangles=True)


    @staticmethod
    def simple_show_object3d(object3d: Object3D):
        vis = ByVispy()
        vis.show_body(object3d)

    @staticmethod
    def simple_show_object3d_asVolume(object3d: Object3D, title="object3d.body as Volume"):
        if object3d is None:
            print("Skipped simple_show_object3d_asVolume - object3d is None")
        else:
            vis = ByVispy()
            vis.show_body_asVolume(object3d, title=title)

    @staticmethod
    def prepare_standard_connect_lines(propSetup: PropSetup, color_by_root=False):
        if propSetup.resultRecords is None:
            raise ValueError("resultRecords can not be None to prepare connect_lines")
        else:
            CPDF = ColorPointDF()
            sh = propSetup.propEnv.shape
            border_limits = [0, sh[0], 0, sh[1], 0, sh[2]]
            df_arrows = CPDF.from_resultRecords(resultRecords = propSetup.resultRecords,
                                                color_scheme = "photonwise",
                                                drop_values = None,
                                                select_photon_id = None,
                                                photon_register = propSetup.photon_register,
                                                select_parent = True,
                                                select_child = True,
                                                border_limits = None,
                                                sum_same_idx = False,
                                                sort = False,
                                                color_by_root=False)
            ADF = ArrowsDF()
            standard_connect_lines = ADF.fromDF(df_arrows, photon_register=propSetup.photon_register, add_start_arrows=True, color_by_root=color_by_root, drop_excessive_columns=False)
            return standard_connect_lines
    
    @staticmethod
    def show_statistics(propSetup: PropSetup):
        print("number of generated random numbers IN SIM:", propSetup.generated_num)
        print("number of seperate random generator instances (MyRandom) IN SIM:", propSetup.random_seed_pool-propSetup.config["random_seed"]) # type: ignore
        print("len(photon_register)", len(propSetup.photon_register))
        if propSetup.config['flag_seve_result_records']: # type: ignore
            print("len(resultRecords)", len(propSetup.resultRecords)) # type: ignore
            ids = set([col[0] for col in propSetup.resultRecords]) # type: ignore
            print("photons recorded:", len(ids))
            print("max photon_id:", max(ids))
            print("min photon_id:", min(ids))


