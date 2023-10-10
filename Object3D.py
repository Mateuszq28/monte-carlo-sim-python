import numpy as np
import json
from FeatureSampling import MyRandom


class Object3D():

    myRandom = MyRandom()

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
        self.reset_val = 0
        if arr is None:
            self.initialize_body_from_xyz(x, y, z)
        else:
           self.initialize_body_from_array(arr)

        self.bodyThumb = None
        self.composition = dict()
        # self.analize_materials()


    def initialize_body_from_xyz(self, x, y, z):
        self.body = np.full(shape=[x, y, z], fill_value=self.reset_val, dtype=int)
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
        Then counts number of their occurrences and saves to self.composition["labels_count"].
        :return: None
        """
        self.composition = dict()
        self.composition["labels"] = np.unique(self.body).tolist()
        # loop initiation value
        self.composition["labels_count"] = []
        for label in self.composition["labels"]:
            self.composition["labels_count"].append(np.count_nonzero(self.body == label))


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
        self.composition["points_series"] = [] # loop initiation value
        for i in range(len(self.composition["labels"])):
            self.composition["points_series"].append(np.zeros(shape=(self.composition["labels_count"][i], 3)))
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
        self.composition["points_series"] = [ps.tolist() for ps in self.composition["points_series"]]


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
        # loop initiation values
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
            "body": self.body.tolist()            
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
        with open(path, 'r') as f:
            d = json.load(f)
        arr = np.array(d["body"])
        return Object3D(arr=arr)
    

    def float_shape_to_int(self, float_point):
        int_point = []
        for i in range(3):
            if isinstance(float_point[i], float):
                int_point.append(int(float_point[i] * self.shape[i]))
            elif isinstance(float_point[i], int) or isinstance(float_point[i], np.int32):
                int_point.append(float_point[i])
            else:
                print(type(float_point[i]))
                raise ValueError("float_point should be int or float")
        return int_point
                

    def fill_cube(self, fill, start_p, fill_rec=None, end_p=None, random_fill=False):
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
            start_pi = self.float_shape_to_int(start_p)
            fill_reci = self.float_shape_to_int(fill_rec)
            end_p = np.array(start_pi) + np.array(fill_reci)

        # if points are fractions of dimensions, count positions
        start_pi = self.float_shape_to_int(start_p)
        end_pi = self.float_shape_to_int(end_p)

        # block for input correctness
        for dimIdx in range(3):
            if end_pi[dimIdx] < start_pi[dimIdx]:
                raise Exception("end_p can't be smaller than startP")
            # if endP is not in Cube, we cut it to Cube's borders
            if end_pi[dimIdx] > self.shape[dimIdx]:
                end_pi[dimIdx] = self.shape[dimIdx]

        # Random generator
        rnd = Object3D.myRandom

        # fill in loop
        for i in range(start_pi[0], end_pi[0]):
            for j in range(start_pi[1], end_pi[1]):
                for k in range(start_pi[2], end_pi[2]):
                    if random_fill:
                        fill = rnd.uniform_half_open(0.0, 1.0)
                    self.body[i, j, k] = fill

        self.analize_materials()
        
