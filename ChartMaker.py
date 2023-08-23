from SumProjection import SumProjection
from Object3D import Object3D
from PropSetup import PropSetup
from ColorPointDF import ColorPointDF
from ByVispy import ByVispy
import matplotlib.pyplot as plt
import numpy as np
import os


class ChartMaker():
    def __init__(self):
        pass


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
    def show_all(propSetup: PropSetup, color_scheme="loop"):

        # SHOW RESULT ENV
        # ChartMaker.simple_show_object3d(propSetup.resultEnv)
        ChartMaker.show_resultEnv(propSetup.resultEnv, color_scheme)

        # SUM PROJECTIONS + MAKING .PNG IMAGES
        ChartMaker.sum_projections(propSetup.resultEnv, color_scheme)


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
    def sum_projections(resultEnv, color_scheme="loop"):
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
            proj.save_png(dir=dir, filename=name+".png", color_scheme=color_scheme)


    @staticmethod
    def show_resultEnv(resultEnv: Object3D, color_scheme="loop"):
        colorPointDF = ColorPointDF()
        df = colorPointDF.from_Object3d(resultEnv, color_scheme=color_scheme, drop_values=[0])
        vis = ByVispy()
        vis.show_ColorPointDF(df, title="Absorbed energy in volume", connect_lines=None)


    @staticmethod
    def simple_show_object3d(object3d: Object3D):
        vis = ByVispy()
        vis.show_body(object3d)



