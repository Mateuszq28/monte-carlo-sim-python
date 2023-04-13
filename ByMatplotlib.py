from View import View
from Object3D import Object3D
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ByMatplotlib(View):
    def __init__(self):
        super().__init__()

    def show_body(self, object3D: Object3D):
        return self.show_body1(object3D)
    
    def show_body_surface(self, object3D: Object3D):
        return self.show_body_surface1(object3D)

    # NEEDS_REFACTOR
    def show_body_surface1(self, object3D:Object3D):
        """
        Plot 3D interactive plot using Matplotlib of object3D.body
        :return: None
        """
        object3D.make3d_points_series()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # colors
        color_bufor = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        color_idx = 0
        color_idx_limit = len(color_bufor)
        for series in object3D.composition["points_series"]:
            x_series = series[:, 0]
            y_series = series[:, 1]
            z_series = series[:, 2]
            ax.scatter(x_series, y_series, z_series, c=color_bufor[color_idx], alpha=1)
            # ax.plot_surface(x_series, y_series, z_series, c=color_bufor[color_idx], alpha=1)
            color_idx = (color_idx+1) % color_idx_limit
        plt.show()

    def show_body1(self, object3D:Object3D):
        """
        Plot 3D interactive plot using Matplotlib of object3D.body
        :return: None
        """
        object3D.make3d_points_series()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # colors
        color_bufor = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        color_idx = 0
        color_idx_limit = len(color_bufor)
        for series in object3D.composition["points_series"]:
            x_series = series[:, 0]
            y_series = series[:, 1]
            z_series = series[:, 2]
            ax.scatter(x_series, y_series, z_series, c=color_bufor[color_idx], alpha=1)
            color_idx = (color_idx+1) % color_idx_limit
        plt.show()