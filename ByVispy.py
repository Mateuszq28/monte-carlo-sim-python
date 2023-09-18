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
from vispy.color import color_array
import pandas as pd




class ByVispy(View):

    triangled_planes_dict = dict()
    material_stack = []

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


    def show_ColorPointDF(self, colorPointDF: pd.DataFrame, title="", connect_lines=None, hide_points=False, draw_plane_triangles=False, draw_planes_from_material_stack=True):
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

            # camera rotating point
            max_idx = colorPointDF[['x_idx', 'y_idx', 'z_idx']].max().to_numpy()
            min_idx = colorPointDF[['x_idx', 'y_idx', 'z_idx']].min().to_numpy()
            mid = (min_idx + max_idx) / 2
            view.camera.center = mid

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
                arrow_pos = np.empty((len(connect_lines)*2, 3), dtype=float)
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
                
            # manually added border plane (rectangle)
            flag_draw_plane = False
            if flag_draw_plane:
                draw_plane = scene.visuals.Plane(width = 1.0,
                                                 height = 1.0,
                                                 direction = '+z',
                                                 color = color_array.Color('white', alpha=1.0),
                                                 edge_color = None,
                                                 parent = view.scene)
                s = visuals.transforms.STTransform(translate=(25.0, 25.0, 49.5), scale=(50.5, 50.5, 1))
                affine = s.as_matrix()
                draw_plane.transform = affine
                
                # draw_plane = scene.visuals.Volume(vol,
                #                                   parent=view.scene,
                #                                   raycasting_mode='plane',
                #                                   method='mip',
                #                                   plane_thickness=3.0,
                #                                   plane_position=(128, 60, 64),
                #                                   plane_normal=(1, 0, 0))
                
                # draw_plane = scene.visuals.Rectangle(center = np.array([50/2-1, 50/2-1, 49.5]),
                #                                      color = color_array.Color('blue'),
                #                                      border_color = color_array.Color('red'),
                #                                      border_width = 1,
                #                                      height = 50,
                #                                      width = 50,
                #                                      radius = 0,
                #                                      parent = view.scene)

            # mark some positions (for debugging)
            put_markers = False
            if put_markers:
                pos_to_mark = [[18.084844079411813, 9.089343247806013, 27.583690503396138]]
                pos_to_mark = np.array(pos_to_mark)
                markers = scene.visuals.Markers(pos = pos_to_mark,
                                                size= 3.0,
                                                # edge_width = 2,
                                                face_color = color_array.Color('red', alpha=1.0),
                                                symbol = "diamond",
                                                scaling =True,
                                                antialias = True,
                                                parent = view.scene)
                

            if draw_plane_triangles:
                str_omit = [str(l) for l in self.omit_labels]
                for label, dic in ByVispy.triangled_planes_dict.items():
                    if label not in str_omit:
                        color = dic["print color"]
                        position = np.array(dic["traingles"]).reshape(-1,3)
                        scene.visuals.Mesh(vertices=position,
                                           faces=None,
                                           vertex_colors=None,
                                           face_colors=None,
                                           color=color_array.Color(color, alpha=1.0),
                                           vertex_values=None,
                                           meshdata=None,
                                           shading=None,
                                           mode='triangles',
                                           parent = view.scene)
                        
            if draw_planes_from_material_stack:
                if len(self.material_stack) > 0:
                    for mat in self.material_stack:
                        mat.fun_vispy_obj(parent = view.scene)
                                                          
                                                          
            # run
            if sys.flags.interactive != 1:
                app.run()

        else:
            print("Can not show empty colorPointDF - " + title)

    def show_body_asVolume(self, object3D: Object3D, title=""):
        # data to visualize
        # input x,y,z
        # output z,y,x
        vol = np.swapaxes(object3D.body, 0, 2)


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

        # camera rotating point
        mid = [val/2 for val in object3D.shape]
        view.camera.center = mid


        # Add a 3D axis to keep us oriented
        # Axes are x=red, y=green, z=blue
        axis_widget = scene.visuals.XYZAxis(parent=view.scene)
            # to enlarge it (scale by affine transformation)
        shape = sorted(object3D.shape)[1]
        s = visuals.transforms.STTransform(translate=(0, 0, 0), scale=(shape, shape, shape))
        affine = s.as_matrix()
        axis_widget.transform = affine

        
        scene.visuals.Volume(vol, parent = view.scene)
                                                        
                                                        
        # run
        if sys.flags.interactive != 1:
            app.run()

     