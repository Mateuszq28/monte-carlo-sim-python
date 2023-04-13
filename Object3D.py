import numpy as np
import json


class Object3D():


    def __init__(self, x=100, y=100, z=100, arr=None):
        """
        Initializes the cuboid self.body (numpy ndarray) that limits
        the object in counter-clockwise cartesian system
        (pol. układ kartezjański prawoskrętny).
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
        :param arr: ready to use body array
        """
        if arr is None:
            self.initialize_body_from_xyz(x, y, z)
        else:
           self.initialize_body_from_array(arr)

        self.bodyThumb = None
        self.composition = dict()
        self.analize_materials()


    def initialize_body_from_xyz(self, x, y, z):
        self.body = np.zeros(shape=[x, y, z], dtype=int)
        self.depth = x
        self.width = y
        self.height = z
        self.shape = [x, y, z]


    def initialize_body_from_array(self, arr):
        self.body = arr
        self.depth = arr.shape[0]
        self.width = arr.shape[1]
        self.height = arr.shape[2]
        self.shape = [self.depth, self.width, self.height]


    def rebuild_from_array(self, arr):
        del self.body
        del self.bodyThumb
        del self.composition
        self.initialize_body_from_array(arr)
        self.bodyThumb = None
        self.composition = dict()
        self.analize_materials()


    def analize_materials(self):
        """
        Save unique values found in self.body to self.composition["labels"].
        Then counts num of their occurrences and saves to self.composition["labels_num"].
        :return: None
        """
        self.composition = dict()
        self.composition["labels"] = np.unique(self.body).tolist()
        self.composition["labels_num"] = []
        for label in self.composition["labels"]:
            self.composition["labels_num"].append(np.count_nonzero(self.body == label))


    def make3d_points_series(self):
        """
        Makes separate data series for each label in self.body.
        Values are in [x, y, z] coordinates in self.body.
        Saves it in self.composition["points_series"].
        Also gives unique ID number to every point in series.
        :return: None
        """
        self.analize_materials()
        # list of np.array [point number, xyz]
        self.composition["points_series"] = []
        for i in range(len(self.composition["labels"])):
            self.composition["points_series"].append(np.zeros(shape=(self.composition["labels_num"][i], 3)))
        # counter to change values in arrays - list of free ID's
        array_id_counter = [0 for _ in range(len(self.composition["points_series"]))]
        for i in range(self.depth):
            for j in range(self.width):
                for k in range(self.height):
                    idx2append = self.composition["labels"].index(self.body[i, j, k])
                    # give the point the smallest possible unused ID
                    point_id_in_series = array_id_counter[idx2append]
                    self.composition["points_series"][idx2append][point_id_in_series, 0:3] = np.array([i, j, k])
                    # this ID is now used, so increment the table of free ID's
                    array_id_counter[idx2append] += 1


    def stride(self, stride=(1, 1, 1), overwrite_thumb=True):
        """
        Downsample the self.body and return a new one (new_body).
        Works similar to stride in tensorflow stride on Neural Networks.
        :param stride: sampling step
        :param overwrite_thumb: whether to save return object to self.bodyThumb
        :return: new_body (an Object3D object with downsampled body)
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
                    new_arr[new_x_idx, new_y_idx, new_z_idx] = self.body[i, j, k]
                    new_z_idx += 1
                new_z_idx = 0
                new_y_idx += 1
            new_y_idx = 0
            new_x_idx += 1
        new_body = Object3D(arr=new_arr)
        if overwrite_thumb:
            self.bodyThumb = new_body
        return new_body
    

    def save_json(self, path, additional=True):
        d = {
            "body": self.body            
        }
        if additional:
            d["self.height"] = self.height
            d["self.width"] = self.width
            d["self.depth"] = self.depth
            d["self.shape"] = self.shape
            d["composition"] = self.composition

        with open(path, 'w') as f:
            json.dump(d, f)


    @staticmethod
    def load_json(path):
        with open(path, 'w') as f:
            d = json.load(f)
        return Object3D(arr=d["body"])


    def fill_cube(self, fill, start_p, fill_rec=None, end_p=None):
        """
        Fills subCube in main body using number in fill variable.
        Works inplace on self.body ndarray
        If points contain floats, it will take a fraction of Env dimension.
        :param fill: int number to fill subCube
        :param start_p: start fill corner (np.array or list)
        :param fill_rec: np.array(shape=3) depth, width and height to fill started from start_p
        :param end_p: end fill corner (np.array or list), doesn't include this point
        :return: None
        """
        if not ((fill_rec is None) ^ (end_p is None)):
            raise Exception("You have to choose fillRec xor end_p")
        elif end_p is None:
            end_p = start_p + fill_rec

        # if points are fractions of dimensions, count positions
        for point in [start_p, end_p]:
            for i in range(3):
                if isinstance(point[i], float):
                    point[i] = int(point[i] * self.shape[i])

        # block for input correctness
        for dimIdx in range(3):
            if end_p[dimIdx] < start_p[dimIdx]:
                raise Exception("end_p can't be smaller than startP")
            # if endP is not in Cube, we cut it to Cube's borders
            if end_p[dimIdx] > self.shape[dimIdx]:
                end_p[dimIdx] = self.shape[dimIdx]

        # fill in loop
        for i in range(start_p[0], end_p[0]):
            for j in range(start_p[1], end_p[1]):
                for k in range(start_p[2], end_p[2]):
                    self.body[i, j, k] = fill
        
