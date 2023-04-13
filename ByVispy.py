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




class ByVispy(View):
    def __init__(self):
        super().__init__()

    def show_body(self, object3D: Object3D, title=""):
        return self.show_body1(object3D, title)

    def show_body1(self, object3D:Object3D, title=""):
        """
        Plot 3D interactive plot using Vispy of object3D.body
        :return: None
        """
        object3D.make3d_points_series()

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

        # data
        color_names = ['green', 'yellow', 'orange', 'red', 'purple', 'blue', 'pink', '#339933',
                       '#FF3366', '#CC0066', '#99FFCC', '#3366FF', '#0000CC']
        counter = 0
        pos_list = []
        colrs_list = []
        for series in object3D.composition["points_series"]:
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

        pos = np.concatenate(pos_list)
        colrs = np.concatenate(colrs_list)

        # plot ! note the parent parameter
        p1 = Scatter3D(parent=view.scene)
        p1.set_gl_state("translucent", blend=True, depth_test=True)
        p1.set_data(
            pos, face_color=colrs, symbol="o", size=10, edge_width=0.5, edge_color="blue"
        )

        # run
        if sys.flags.interactive != 1:
            app.run()

    def show_body2(self, object3D:Object3D, title=""):
        """
        Plot 3D interactive plot using Vispy of object3D.body
        :return: None
        """
        object3D.make3d_points_series()

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

        # data
        pos = object3D.composition["points_series"][0]
        n = len(pos)
        colors = np.ones((n, 4), dtype=np.float32)
        for i in range(n):
            colors[i] = (i / n, 1.0 - i / n, 0, 0.8)

        # plot ! note the parent parameter
        p1 = Scatter3D(parent=view.scene)
        p1.set_gl_state("translucent", blend=True, depth_test=True)
        p1.set_data(
            pos, face_color=colors, symbol="o", size=10, edge_width=0.5, edge_color="blue"
        )

        # run
        if sys.flags.interactive != 1:
            app.run()

     