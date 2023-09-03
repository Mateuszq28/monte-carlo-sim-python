import numpy as np
from View import View
from Object3D import Object3D
from mpl_toolkits.mplot3d import Axes3D
# decorator used for overloading functions
# distinguish by num of arguments
import PIL
from PIL import ImageColor
import sys
from vispy import app, visuals, scene
import pandas as pd




class ByVispy(View):
    def __init__(self):
        super().__init__()

    def show_body(self, object3D: Object3D, title="", omit_labels=None):
        return self.show_body1(object3D, title, omit_labels=omit_labels)

    def show_body1(self, object3D:Object3D, title="", omit_labels=None):
        """
        Plot 3D interactive plot using Vispy of object3D.body
        :return: None
        """

        # make array to omit particles with this labels
        if omit_labels is None:
            omit_labels = View.omit_labels

        object3D.make3d_points_series()

        # data
        color_names = ['green', 'yellow', 'orange', 'red', 'purple', 'blue', 'pink', '#339933',
                       '#FF3366', '#CC0066', '#99FFCC', '#3366FF', '#0000CC']
        # loop initiation values
        counter = 0
        pos_list = []
        colrs_list = []
        for series, label in list(zip(object3D.composition["points_series"], object3D.composition["labels"])):
            if label not in omit_labels:
                pos_list.append(series)
                n = len(series)
                colors = np.ones((n, 4), dtype=np.float32)
                rgb = PIL.ImageColor.getrgb(color_names[counter % len(color_names)])
                rgb_norm = np.array(rgb) / 255.0
                for i in range(n):
                    colors[i,0:3] = rgb_norm
                    colors[i,3] = 1
                counter += 1
                colrs_list.append(colors)

        if len(pos_list) > 0:
            pos = np.concatenate(pos_list)
            colrs = np.concatenate(colrs_list)

            # build your visuals, that's all
            Scatter3D = scene.visuals.create_visual_node(visuals.MarkersVisual)

            # The real-things : plot using scene
            # build canvas
            canvas = scene.SceneCanvas(keys="interactive",  title=title, show=True)

            # Add a ViewBox to let the user zoom/rotate
            view = canvas.central_widget.add_view()
            view.camera = "turntable"
            view.camera.fov = 45
            view.camera.distance = 500

            # plot ! note the parent parameter
            p1 = Scatter3D(parent=view.scene)
            p1.set_gl_state("translucent", blend=True, depth_test=True)
            p1.set_data(
                pos, face_color=colrs, symbol="o", size=10, edge_width=0.5, edge_color="blue"
            )

            # Add a 3D axis to keep us oriented
            # Axes are x=red, y=green, z=blue
            axis_widget = scene.visuals.XYZAxis(parent=view.scene)
                # to enlarge it (scale by affine transformation)
            shape = sorted(object3D.shape)[1]
            s = visuals.transforms.STTransform(translate=(0, 0, 0), scale=(shape, shape, shape))
            affine = s.as_matrix()
            axis_widget.transform = affine

            # run
            if sys.flags.interactive != 1:
                app.run()

        else:
            print("Can not show empty object3D - " + title)


    def show_body2(self, object3D:Object3D, title="", omit_labels=None):
        """
        Plot 3D interactive plot using Vispy of object3D.body
        :return: None
        """

        # make array to omit particles with this labels
        if omit_labels is None:
            omit_labels = View.omit_labels

        object3D.make3d_points_series()

        # data

        # this commented line can be deleted - shows "air"/0 label
        # pos = object3D.composition["points_series"][0]

        pos_not_conc = [series for series, label in list(zip(object3D.composition["points_series"], object3D.composition["labels"])) if label not in omit_labels]

        if len(pos_not_conc) > 0:
            pos = np.concatenate(pos_not_conc)
            n = len(pos)
            # loop initiation value
            colors = np.ones((n, 4), dtype=np.float32)
            for i in range(n):
                colors[i] = (i / n, 1.0 - i / n, 0, 0.8)

            # build your visuals, that's all
            Scatter3D = scene.visuals.create_visual_node(visuals.MarkersVisual)

            # The real-things : plot using scene
            # build canvas
            canvas = scene.SceneCanvas(keys="interactive", title=title, show=True)

            # Add a ViewBox to let the user zoom/rotate
            view = canvas.central_widget.add_view()
            view.camera = "turntable"
            view.camera.fov = 45
            view.camera.distance = 500

            # plot ! note the parent parameter
            p1 = Scatter3D(parent=view.scene)
            p1.set_gl_state("translucent", blend=True, depth_test=True)
            p1.set_data(
                pos, face_color=colors, symbol="o", size=10, edge_width=0.5, edge_color="blue"
            )

            # Add a 3D axis to keep us oriented
            # Axes are x=red, y=green, z=blue
            axis_widget = scene.visuals.XYZAxis(parent=view.scene)
                # to enlarge it (scale by affine transformation)
            shape = sorted(object3D.shape)[1]
            s = visuals.transforms.STTransform(translate=(0, 0, 0), scale=(shape, shape, shape))
            affine = s.as_matrix()
            axis_widget.transform = affine

            # run
            if sys.flags.interactive != 1:
                app.run()

        else:
            print("Can not show empty object3D - " + title)


    def show_ColorPointDF(self, colorPointDF: pd.DataFrame, title="", connect_lines=None, hide_points=False):
        """
        Plot 3D interactive plot of points in colorPointDF data frame using Vispy
        :return: None
        """

        if len(colorPointDF) > 0:

            # data to visualize
            pos = colorPointDF[['x_idx', 'y_idx', 'z_idx']].to_numpy()
            colrs = colorPointDF[['R', 'G', 'B', 'A']].to_numpy() / 255.0


            # build your visuals, that's all
            Scatter3D = scene.visuals.create_visual_node(visuals.MarkersVisual)

            # The real-things : plot using scene
            # build canvas
            canvas = scene.SceneCanvas(keys="interactive",  title=title, show=True)

            # Add a ViewBox to let the user zoom/rotate
            view = canvas.central_widget.add_view()
            view.camera = "turntable"
            view.camera.fov = 45
            view.camera.distance = 500

            # plot ! note the parent parameter
            if not hide_points:
                p1 = Scatter3D(parent=view.scene)
                p1.set_gl_state("translucent", blend=True, depth_test=True)
                p1.set_data(pos, face_color=colrs, symbol="o", size=10, edge_width=0.5, edge_color="blue")

            # Add a 3D axis to keep us oriented
            # Axes are x=red, y=green, z=blue
            axis_widget = scene.visuals.XYZAxis(parent=view.scene)
                # to enlarge it (scale by affine transformation)
            shape = sorted(colorPointDF[['x_idx', 'y_idx', 'z_idx']].max().values)[1]
            s = visuals.transforms.STTransform(translate=(0, 0, 0), scale=(shape, shape, shape))
            affine = s.as_matrix()
            axis_widget.transform = affine

            if connect_lines is not None:
                # pos - line body
                arrow_pos = np.empty((len(connect_lines)*2, 3), dtype=int)
                arrow_pos[0::2] = connect_lines[["x_idx", "y_idx", "z_idx"]]
                arrow_pos[1::2] = connect_lines[["x_idx_2", "y_idx_2", "z_idx_2"]]
                # line color
                arrow_color = np.empty((arrow_pos.shape[0], 4), dtype=float)
                arrow_color[0::2] = connect_lines[["R", "G", "B", "A"]] / 255.0
                arrow_color[1::2] = arrow_color[0::2]
                # arrow_method = "agg"
                arrow_method = "gl"
                # arrows - just arrowheads
                arrows_vec_int = connect_lines[["x_idx", "y_idx", "z_idx", "x_idx_2", "y_idx_2", "z_idx_2"]].to_numpy()
                # move arrowheads backwards not to be overlapped by points balls
                dir_vec = arrows_vec_int[:, 3:6] - arrows_vec_int[:, 0:3]
                arrow_arrows = np.empty(arrows_vec_int.shape, dtype=float)
                arrow_arrows[:, 0:3] = arrows_vec_int[:, 0:3]
                # arrow_arrows[:, 3:6] = arrows_vec_int[:, 3:6] - 0.1 * dir_vec / np.linalg.norm(dir_vec, axis=1)[:, np.newaxis]
                arrow_arrows[:, 3:6] = arrows_vec_int[:, 3:6] - 0.5 * dir_vec # in the middle of the arrow body line
                arrow_types = ["stealth", "curved", "triangle_30", "triangle_60", "triangle_90", "angle_30", "angle_60", "angle_90", "inhibitor_round"] # len = 9
                # arrowhead color
                arrow_arrow_color = arrow_color[0::2]
                arrows = scene.visuals.Arrow(pos = arrow_pos,
                                             color = arrow_color,
                                             parent = view.scene,
                                             width = 1,
                                             connect = "segments",
                                             method = arrow_method,
                                             antialias = True,
                                             arrows = arrow_arrows,
                                             arrow_type = arrow_types[0],
                                             arrow_size = 5.0,
                                             arrow_color = arrow_arrow_color)

            # run
            if sys.flags.interactive != 1:
                app.run()

        else:
            print("Can not show empty colorPointDF - " + title)

     