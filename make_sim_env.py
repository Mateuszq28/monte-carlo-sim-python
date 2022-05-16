import argparse
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# decorator used for overloading functions
# distinguish by num of arguments


class PropEnv:

    def __init__(self, x=100, y=100, z=100, arr=None):
        """
        Initializes the cuboid self.Env (numpy ndarray) that limits
        the environment in counter-clockwise cartesian system
        (pol. układ kartezjański prawoskrętny)
           ^ z=height
           |
           |
           .----------> y=width
          /
         /
        + x=depth
        :param x: self.depth
        :param y: self.width
        :param z: self.height
        """
        if arr is None:
            self.Env = np.zeros(shape=[x, y, z], dtype=int)
            self.depth = x
            self.width = y
            self.height = z
            self.shape = [x, y, z]
        else:
            self.Env = arr
            self.depth = arr.shape[0]
            self.width = arr.shape[1]
            self.height = arr.shape[2]
            self.shape = [x, y, z]
        self.EnvThumb = None
        self.composition = None
        self.analize_materials()

    def analize_materials(self):
        """
        Save unique values found in self.Env to self.composition["labels"]
        then counts num of their occurrences and saves to self.composition["labels_num"]
        :return: None
        """
        self.composition = dict()
        self.composition["labels"] = np.unique(self.Env).tolist()
        self.composition["labels_num"] = []
        for label in self.composition["labels"]:
            self.composition["labels_num"].append(np.count_nonzero(self.Env == label))

    def make3d_points_series(self):
        """
        Makes separate data series for each label in self.Enf
        Values are [x, y, z] coordinates in self.Env
        Saves it in self.composition["points_series"]
        :return:
        """
        self.analize_materials()
        # list of np.array [point number, xyz]
        self.composition["points_series"] = []
        for i in range(len(self.composition["labels"])):
            self.composition["points_series"].append(np.zeros(shape=(self.composition["labels_num"][i], 3)))
        # counter to change values in arrays
        array_id_counter = [0 for _ in range(len(self.composition["points_series"]))]
        for i in range(self.depth):
            for j in range(self.width):
                for k in range(self.height):
                    idx2append = self.composition["labels"].index(self.Env[i, j, k])
                    point_id_in_series = array_id_counter[idx2append]
                    self.composition["points_series"][idx2append][point_id_in_series, 0:3] = np.array([i, j, k])
                    array_id_counter[idx2append] += 1

    def stride(self, stride=(1, 1, 1), overwrite_thumb=True):
        """
        Downsample the Env and return a new one (new_env)
        Works similar to stride in tensorflow stride on Neural Networks
        :param stride: sampling step
        :param overwrite_thumb: whether to save return object to self.EnvThumb
        :return: new_env (a PropEnv object with downsampled Env)
        """
        if isinstance(stride, int):
            stride = (stride, stride, stride)
        range_x = range(0, self.depth, stride[0])
        range_y = range(0, self.width, stride[1])
        range_z = range(0, self.height, stride[2])
        new_arr = np.zeros([len(range_x), len(range_y), len(range_z)])
        new_x_idx = 0
        new_y_idx = 0
        new_z_idx = 0
        for i in range_x:
            for j in range_y:
                for k in range_z:
                    new_arr[new_x_idx, new_y_idx, new_z_idx] = self.Env[i, j, k]
                    new_z_idx += 1
                new_z_idx = 0
                new_y_idx += 1
            new_y_idx = 0
            new_x_idx += 1
        new_env = PropEnv(arr=new_arr)
        if overwrite_thumb:
            self.EnvThumb = new_env
        return new_env

    def vizualize(self):
        """
        Plot 3D interactive plot using Matplotlib of self.Env
        :return: None
        """
        self.make3d_points_series()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # colors
        color_bufor = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        color_idx = 0
        color_idx_limit = len(color_bufor)+1
        for series in self.composition["points_series"]:
            x_series = series[:, 0]
            y_series = series[:, 1]
            z_series = series[:, 2]
            ax.scatter(x_series, y_series, z_series, c=color_bufor[color_idx], alpha=1)
            color_idx = (color_idx+1) % color_idx_limit
        plt.show()

    def vizualize_params(self, stride):
        if stride is not None:
            new_env = self.stride(stride)
            new_env.vizualize()



    def fill_cube(self, fill, start_p, fill_rec=None, end_p=None):
        """
        Fills subCube in main env Cube using number in fill variable
        Works inplace on self.Env ndarray
        if points contain floats, it will take a fraction of Env dimension
        :param fill: int number to fill subCube
        :param start_p: start fill corner (np.array or list)
        :param fill_rec: np.array(shape=3) depth, width and height to fill started from start_p
        :param end_p: end fill corner (np.array or list), doesn't include this point
        :return: None
        """
        if not ((fill_rec is None) ^ (end_p is None)):
            raise Exception("You have to choose fillRec or end_p")
        elif end_p is None:
            end_p = start_p + fill_rec

        # if points are fractions of dimensions, count positions
        for point in [start_p, end_p]:
            for c in point:
                for i in range(3):
                    if isinstance(point[i], float):
                        point[i] = int(point[i] * self.shape[i])

        # block for input correctness
        for dimIdx in range(len(end_p)): # it is constant range(3)
            if end_p[dimIdx] < start_p[dimIdx]:
                raise Exception("end_p can't be smaller than startP")
            # if endP is not in Cube, we cut it to Cube's borders
            if end_p[dimIdx] > self.shape[dimIdx]:
                end_p[dimIdx] = self.shape[dimIdx]

        # fill in loop
        for i in range(start_p[0], end_p[0]):
            for j in range(start_p[1], end_p[1]):
                for k in range(start_p[2], end_p[2]):
                    self.Env[i, j, k] = fill



'''
if __name__ == '__main__':

    filename_in = "kaggle_masks_coco.json"
    filename_out_train = "kaggle_masks_coco_train.json"
    filename_out_test = "kaggle_masks_coco_test.json"
    split_ratio = 0.25

    ap = argparse.ArgumentParser(fromfile_prefix_chars='@')
    ap.add_argument('-l', '--lol', help="nazwa pliku jsona do podziału", metavar='String', default=filename_in)
    ap.add_argument('-tr', '--train', help='nazwa pliku jsona wyjściowego - train', metavar='String', default=filename_out_train)
    ap.add_argument('-te', '--test', help='nazwa pliku jsona wyjściowego - test', metavar='String', default=filename_out_test)
    ap.add_argument('-r', '--ratio', help='stosunek zbioru testowego do całości', metavar=float, default=split_ratio)

    args = vars(ap.parse_args())

    arg_input = args['input']
    arg_train = args['train']
    arg_test = args['test']
    arg_ratio = args['ratio']
'''

