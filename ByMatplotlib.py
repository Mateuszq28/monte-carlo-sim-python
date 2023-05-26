from View import View
from Object3D import Object3D
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ByMatplotlib(View):
    def __init__(self):
        super().__init__()

    def show_body(self, object3D: Object3D, title="", omit_labels=None):
        return self.show_body1(object3D, title=title, omit_labels=omit_labels)
    
    def show_body_surface(self, object3D: Object3D, title="", omit_labels=None):
        return self.show_body_surface1(object3D, title=title, omit_labels=omit_labels)

    # NEEDS_REFACTOR
    def show_body_surface1(self, object3D:Object3D, title="", omit_labels=None):
        """
        Plot 3D interactive plot using Matplotlib of object3D.body
        :return: None
        """

        # make array to omit particles with this labels
        if omit_labels is None:
            omit_labels = View.omit_labels

        object3D.make3d_points_series()
        fig = plt.figure(num=title)
        ax = fig.add_subplot(111, projection='3d')
        # colors
        color_bufor = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        color_idx = 0
        color_idx_limit = len(color_bufor)
        for series, label in list(zip(object3D.composition["points_series"], object3D.composition["labels"])):
            if label not in omit_labels:
                x_series = series[:, 0]
                y_series = series[:, 1]
                z_series = series[:, 2]
                ax.scatter(x_series, y_series, z_series, c=color_bufor[color_idx], alpha=1)
                # ax.plot_surface(x_series, y_series, z_series, c=color_bufor[color_idx], alpha=1)
                color_idx = (color_idx+1) % color_idx_limit
        plt.show()

    def show_body1(self, object3D:Object3D, title="", omit_labels=None):
        """
        Plot 3D interactive plot using Matplotlib of object3D.body
        :return: None
        """

        # make array to omit particles with this labels
        if omit_labels is None:
            omit_labels = View.omit_labels

        object3D.make3d_points_series()
        fig = plt.figure(num=title)
        ax = fig.add_subplot(111, projection='3d')
        # colors
        color_bufor = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        color_idx = 0
        color_idx_limit = len(color_bufor)
        for series, label in list(zip(object3D.composition["points_series"], object3D.composition["labels"])):
            if label not in omit_labels:
                x_series = series[:, 0]
                y_series = series[:, 1]
                z_series = series[:, 2]
                ax.scatter(x_series, y_series, z_series, c=color_bufor[color_idx], alpha=1)
                color_idx = (color_idx+1) % color_idx_limit
        plt.show()