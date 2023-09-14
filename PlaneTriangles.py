from PropEnv import PropEnv
from MarchingCubes import MarchingCubes
import numpy as np
import json
import os

class PlaneTriangles():

    traingles_planes_json_filename = "propEnvTrianglesPlanes.json"

    def __init__(self):
        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)

    def from_propEnv(self, propEnv: PropEnv):
        """
        Makes list of triangles of all planes (triangled planes).
        """
        triangls_dict = dict() # key = label
        # labels (unique values) in propEnv
        labels = np.unique(propEnv.body)
        # centroid coordinates
        cent_x_linspace = np.linspace(0.5, propEnv.shape[0]-1-0.5, num=propEnv.shape[0]-1)
        cent_y_linspace = np.linspace(0.5, propEnv.shape[1]-1-0.5, num=propEnv.shape[1]-1)
        cent_z_linspace = np.linspace(0.5, propEnv.shape[2]-1-0.5, num=propEnv.shape[2]-1)
        for label in labels:
            triangls_dict[str(label)] = {"print color": self.config["tissue_properties"][str(label)]["print color"],
                                    "traingles": []}
            for cent_x in cent_x_linspace:
                for cent_y in cent_y_linspace:
                    for cent_z in cent_z_linspace:
                        cent = [cent_x, cent_y, cent_z]
                        corners = MarchingCubes.marching_cube_corners_from_centroid(cent)
                        # if corner has the same label, it's the part of the plane
                        corner_full_binary_code = [propEnv.get_label_from_float(co) == label for co in corners]
                        corner_full_decimal = sum([2**bit for bit, val in zip(range(7,-1,-1), corner_full_binary_code) if val == True])
                        # all triangles corners in one list
                        triangles = MarchingCubes.TriangleTable[corner_full_decimal].copy()
                        if len(triangles) > 2:
                            # split into triangles
                            triangles = [triangles[x:x+3] for x in range(0, len(triangles)-1, 3)]
                            triangles_coordinates = [[MarchingCubes.triangle_corner_from_centroid(cent, corner_idx) for corner_idx in tri] for tri in triangles]
                            # add to dict
                            triangls_dict[str(label)]["traingles"] += triangles_coordinates
        return triangls_dict

    def from_propEnv_vectorized(self, propEnv: PropEnv):
        """
        Makes list of triangles of all planes (triangled planes).
        """
        triangls_dict = dict() # key = label
        # labels (unique values) in propEnv
        labels = np.unique(propEnv.body)
        for label in labels:
            triangls_dict[str(label)] = {"print color": self.config["tissue_properties"][str(label)]["print color"], "traingles": []}
            # centroid coordinates
            sh = [s-1 for s in propEnv.shape]
            x, y, z = np.indices(sh)
            x = x.flatten().reshape(-1,1) + 0.5
            y = y.flatten().reshape(-1,1) + 0.5
            z = z.flatten().reshape(-1,1) + 0.5
            cents = np.hstack([x, y, z])
            corners = [MarchingCubes.marching_cube_corners_from_centroid(row) for row in cents]
            # if corner has the same label, it's the part of the plane
            corner_full_binary_code = [[propEnv.get_label_from_float(co) == label for co in row] for row in corners]
            corner_full_decimal = [sum([2**bit for bit, val in zip(range(7,-1,-1), row) if val == True]) for row in corner_full_binary_code]
            # all triangles corners in one list
            triangles = [MarchingCubes.TriangleTable[row].copy() for row in corner_full_decimal]

            # split into triangles
            triangles = [[row[x:x+3] for x in range(0, len(row)-1, 3)] for row in triangles]
            triangles_coordinates = [[[MarchingCubes.triangle_corner_from_centroid(cent, corner_idx) for corner_idx in tri] for tri in row if len(tri) > 2] for row, cent in zip(triangles, cents) if len(row) > 0]
            triangles_coordinates = [item for sublist in triangles_coordinates for item in sublist]

            # add to dict
            triangls_dict[str(label)]["traingles"] = triangles_coordinates
        return triangls_dict
  

    
    @staticmethod
    def save_json(triangls_dict, folder):
        path = os.path.join(folder, PlaneTriangles.traingles_planes_json_filename)
        with open(path, 'w') as f:
            json.dump(triangls_dict, f)

    @staticmethod
    def load_json(folder):
        path = os.path.join(folder, PlaneTriangles.traingles_planes_json_filename)
        if os.path.isfile(path):
            with open(path, 'r') as f:
                d = json.load(f)
        else:
            d = None
        return d