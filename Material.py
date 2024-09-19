import Geometry3D
import numpy as np
import math
import json
from vispy import visuals, scene
from PIL import ImageColor
from vispy.color import color_array


class Material():
        
    def __init__(self, label):
        self.label = label
        self.parallelepiped : Geometry3D.ConvexPolyhedron
        self.name : str

        # to avoid calculation of excessive intersections
        # if point is not in self.hard_boundary it is certain, that it is not in material scope
        # [-x, x+, -y, y+, -z, z+]
        self.hard_boundary : list | None

        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)

    def is_point_in_hard_boundary(self, p):
        if self.hard_boundary is None:
            return True
        in_x = self.hard_boundary[0] <= p[0] <= self.hard_boundary[1]
        in_y = self.hard_boundary[2] <= p[1] <= self.hard_boundary[3]
        in_z = self.hard_boundary[4] <= p[2] <= self.hard_boundary[5]
        return in_x and in_y and in_z
    
    def is_seg_out_of_hard_boundary(self, p1, p2):
        if self.hard_boundary is None:
            return False
        # x axis
        out_x_low = self.hard_boundary[0] > p1[0] and self.hard_boundary[0] > p2[0]
        out_x_high = self.hard_boundary[1] < p1[0] and self.hard_boundary[1] < p2[0]
        # y axis
        out_y_low = self.hard_boundary[2] > p1[1] and self.hard_boundary[2] > p2[1]
        out_y_high = self.hard_boundary[3] < p1[1] and self.hard_boundary[3] < p2[1]
        # z axis
        out_z_low = self.hard_boundary[4] > p1[2] and self.hard_boundary[4] > p2[2]
        out_z_high = self.hard_boundary[5] < p1[2] and self.hard_boundary[5] < p2[2]
        is_out = out_x_low or out_x_high or out_y_low or out_y_high or out_z_low or out_z_high
        return is_out
        
    def fun_in(self, point):
        pass

    def fun_boundary(self, point):
        pass

    def fun_intersect(self, p1, p2, mat_in):
        if self.is_seg_out_of_hard_boundary(p1, p2):
            return None

        geo_p1 = Geometry3D.Point(p1)
        geo_p2 = Geometry3D.Point(p2)
        seg = Geometry3D.Segment(geo_p1, geo_p2)
        intersec = self.parallelepiped.intersection(seg)
        # print(self.name+" intersec", intersec)

        # there is not intersection (common line part) segment
        if intersec is None:
            return None
        intersec = mat_in.parallelepiped.intersection(intersec)
        # print(self.name+" intersec", intersec)
        if intersec is None:
            return None
        
        # there is intersection segment (common line part)
        elif isinstance(intersec, Geometry3D.Segment):
            # take the farthest intersection point
            inter_p1 = intersec.start_point
            inter_p2 = intersec.end_point
            dist1 = geo_p1.distance(inter_p1)
            dist2 = geo_p1.distance(inter_p2)

            if (inter_p1 == geo_p1 and inter_p2 == geo_p2) or (inter_p1 == geo_p2 and inter_p2 == geo_p1):
                return None

            if dist1 < dist2:
                if inter_p1 != geo_p1:
                    out_geo_p = inter_p1
                else:
                    out_geo_p = inter_p2
            else:
                out_geo_p = inter_p2
            # check if photon was nat in this tissue at the start
            # (it is important especially when there are more layers of materials)
            if out_geo_p == geo_p1:
                # photon was in this tissue at the beggining, so there was no boundary cross
                return None
            
        # there is only intersection point
        elif isinstance(intersec, Geometry3D.Point):
            # check if photon was nat in this tissue at the start
            if intersec == geo_p1:
                return None
            else:
                out_geo_p = intersec

        else:
            raise NotImplementedError()
        
        # Geometry3D Point to list
        out_p = [out_geo_p.x, out_geo_p.y, out_geo_p.z]
        return out_p

    def fun_plane_normal_vec(self, point):
        pass

    def fun_vispy_obj(self, parent):
        pass

    def make_dump(self):
        pass

    @staticmethod
    def load_dump(dump):
        pass

    # --- TOOLS ---

    @staticmethod
    def point_relative2static(point, propEnvShape):
        if isinstance(point, tuple):
            point = list(point)
        else:
            point = point.copy()
        for i in range(3):
            if isinstance(point[i], float):
                if propEnvShape is not None:
                    point[i] = round(point[i] * propEnvShape[i])
                else:
                    raise ValueError("To change relative float point into static int point, propEnvShape is needed.")
        return point
    

def load_dump(dump):
    cl = dump["class"]
    if cl == Cuboid.name:
        return Cuboid.load_dump(dump)
    if cl == Cylinder.name:
        return Cylinder.load_dump(dump)
    
def are_points_close(p1: Geometry3D.Point, p2: Geometry3D.Point):
    p1_list = [p1.x, p1.y, p1.z]
    p2_list = [p2.x, p2.y, p2.z]
    if False in [math.isclose(val1, val2) for val1, val2 in zip(p1_list, p2_list)]:
        return False
    else:
        return True

# --- SHAPES ---

class Cuboid(Material):
        
    name = "Cuboid"
        
    def __init__(self, label, start_p, end_p, propEnvShape=None):
        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)

        # require to make dict/json dump
        self.label = label
        self.start_p = start_p
        self.end_p = end_p
        self.propEnvShape = propEnvShape

        # float (proportion of propEnvShape) to int (static coordinates)
        self.start_p_stat = self.point_relative2static(start_p, propEnvShape)
        self.end_p_stat = self.point_relative2static(end_p, propEnvShape)

        self.hard_boundary = [self.start_p_stat[0], self.end_p_stat[0], self.start_p_stat[1], self.end_p_stat[1], self.start_p_stat[2], self.end_p_stat[2]]

        ver1 = [self.end_p_stat[0], self.start_p_stat[1], self.start_p_stat[2]]
        ver2 = [self.start_p_stat[0], self.end_p_stat[1], self.start_p_stat[2]]
        ver3 = [self.start_p_stat[0], self.start_p_stat[1], self.end_p_stat[2]]
        vec1 = [ver - ps for ver, ps in zip(ver1, self.start_p_stat)]
        vec2 = [ver - ps for ver, ps in zip(ver2, self.start_p_stat)]
        vec3 = [ver - ps for ver, ps in zip(ver3, self.start_p_stat)]
        vec1, vec2, vec3 = [Geometry3D.Vector(vec) for vec in [vec1, vec2, vec3]]
        self.geo_start_p = Geometry3D.Point(self.start_p_stat)
        # cuboid
        self.parallelepiped = Geometry3D.geometry.Parallelepiped(base_point=self.geo_start_p, v1=vec1, v2=vec2, v3=vec3)

    def fun_in(self, point):
        for i in range(3):
            if not (self.start_p_stat[i] <= point[i] <= self.end_p_stat[i]):
                return False
        return True
    
    def check_boundaries(self, point):
        return [math.isclose(self.start_p_stat[0], point[0]), math.isclose(self.end_p_stat[0], point[0]), math.isclose(self.start_p_stat[1], point[1]), math.isclose(self.end_p_stat[1], point[1]), math.isclose(self.start_p_stat[2], point[2]), math.isclose(self.end_p_stat[2], point[2])]
    
    def fun_boundary(self, point):
        return True in self.check_boundaries(point)
        # old
        # for i in range(3):
        #     at_start_ax = math.isclose(start_p[i], point[i])
        #     at_end_ax = math.isclose(end_p[i], point[i])
        #     if not (at_start_ax or at_end_ax):
        #         return False
        # return True
    
    def fun_plane_normal_vec(self, point):
        boundary_flags = self.check_boundaries(point)
        if boundary_flags[0]:
            return [-1, 0, 0]
        if boundary_flags[1]:
            return [1, 0, 0]
        if boundary_flags[2]:
            return [0, -1, 0]
        if boundary_flags[3]:
            return [0, 1, 0]
        if boundary_flags[4]:
            return [0, 0, -1]
        if boundary_flags[5]:
            return [0, 0, 1]
        # print(point)
        # raise NotImplementedError()
        return None
    
    def fun_vispy_obj(self, parent):
        c = self.config["tissue_properties"][str(self.label)]["print color"]
        # c = ImageColor.getrgb(c)
        # color = [c[0], c[1], c[2], 255]
        # color = [val/255 for val in color]
        color = color_array.Color(c, alpha=1.0)

        # top
        # 0-bottom, 1-back, 2-left, 3-top, 4-front, 5-right
        polygon = self.parallelepiped.convex_polygons[3]
        polygon_points = np.array([[p.x, p.y, p.z] for p in polygon.points])
        scene.visuals.Mesh(vertices = polygon_points, # type: ignore
                           faces=None,
                           vertex_colors=None,
                           face_colors=None,
                           color=color,
                           vertex_values=None,
                           meshdata=None,
                           shading=None,
                           mode='triangle_fan',
                           parent = parent)

        # # bottom
        # polygon = self.parallelepiped.convex_polygons[0]
        # polygon_points = np.array([[p.x, p.y, p.z] for p in polygon.points])
        # scene.visuals.Mesh(vertices = polygon_points,
        #                    faces=None,
        #                    vertex_colors=None,
        #                    face_colors=None,
        #                    color=color,
        #                    vertex_values=None,
        #                    meshdata=None,
        #                    shading=None,
        #                    mode='triangle_fan',
        #                    parent = parent)
    
    def make_dump(self):
        d = dict()
        d["class"] = Cuboid.name
        d["label"] = self.label
        d["start_p"] = self.start_p
        d["end_p"] = self.end_p
        d["propEnvShape"] = self.propEnvShape
        return d

    @staticmethod
    def load_dump(dump):
        label = dump["label"]
        start_p = dump["start_p"]
        end_p = dump["end_p"]
        propEnvShape = dump["propEnvShape"]
        cub = Cuboid(label=label, start_p=start_p, end_p=end_p, propEnvShape=propEnvShape)
        return cub 
    

class Cylinder(Material):
        
    name = "Cylinder"

    def __init__(self, label, circle_center, radius, height_vector, propEnvShape=None, hard_boundary=None):
        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)

        self.hard_boundary = hard_boundary

        # require to make dict/json dump
        self.label = label
        self.circle_center = circle_center
        self.radius = radius
        self.height_vector = height_vector
        self.propEnvShape = propEnvShape

        # float (proportion of propEnvShape) to int (static coordinates)
        self.circle_center_stat = self.point_relative2static(self.circle_center, self.propEnvShape)
        self.geo_circle_center = Geometry3D.Point(self.circle_center_stat)
        self.geo_height_vector = Geometry3D.Vector(self.height_vector)
        self.parallelepiped = Geometry3D.geometry.Cylinder(self.geo_circle_center, self.radius, self.geo_height_vector, n=10)


    def fun_in(self, point):
        if not self.is_point_in_hard_boundary(point):
            return False
        geo_p = Geometry3D.Point(point)
        return geo_p in self.parallelepiped
    
    def fun_boundary(self, point):
        geo_p = Geometry3D.Point(point)
        polygons = self.parallelepiped.convex_polygons
        ins = [(geo_p in pl) for pl in polygons]
        return True in ins
    
    def fun_plane_normal_vec(self, point):
        geo_p = Geometry3D.Point(point)
        polygons = self.parallelepiped.convex_polygons
        ins = [(geo_p in pl) for pl in polygons]
        normals_in = [pl.plane.n for pl, in_flag in zip(polygons, ins) if in_flag]
        # print("cyl normals_in", normals_in)
        if len(normals_in) > 0:
            normal_p = [normals_in[0][0], normals_in[0][1], normals_in[0][2]]
            return normal_p
        else:
            # print(point)
            return None
    
    def fun_vispy_obj(self, parent):
        polygons = self.parallelepiped.convex_polygons
        
        top_bottom = [poly for poly in polygons if len(poly.points) != 4]
        top_bottom_center = [poly.center_point for poly in top_bottom]
        top_bottom_points = [[[p.x, p.y, p.z] for p in poly.points] for poly in top_bottom]
        # add center point, to draw traingles in fan mode
        top_bottom_points = [[[center.x, center.y, center.z]]+poly for poly, center in zip(top_bottom_points, top_bottom_center)]
        # repeat second point to close polygon fan
        top_bottom_points[0].append(top_bottom_points[0][1])
        top_bottom_points[1].append(top_bottom_points[1][1])
        top_bottom_points = np.array(top_bottom_points)

        walls = [poly for poly in polygons if len(poly.points) == 4]
        walls = [[[p.x, p.y, p.z] for p in poly.points] for poly in walls]
        walls = np.array(walls)

        c = self.config["tissue_properties"][str(self.label)]["print color"]
        # c = ImageColor.getrgb(c)
        # color = [c[0], c[1], c[2], 255]
        # color = [val/255 for val in color]
        color = color_array.Color(c, alpha=1.0)

        for wall in walls:
            scene.visuals.Mesh(vertices = wall, # type: ignore
                               faces=None,
                               vertex_colors=None,
                               face_colors=None,
                               color=color,
                               vertex_values=None,
                               meshdata=None,
                               shading=None,
                               mode='triangle_fan',
                               parent = parent)
        
        # scene.visuals.Mesh(vertices = top_bottom_points[0],
        #                    faces=None,
        #                    vertex_colors=None,
        #                    face_colors=None,
        #                    color=color,
        #                    vertex_values=None,
        #                    meshdata=None,
        #                    shading=None,
        #                    mode='triangle_fan',
        #                    parent = parent)
        
        # scene.visuals.Mesh(vertices = top_bottom_points[1],
        #                    faces=None,
        #                    vertex_colors=None,
        #                    face_colors=None,
        #                    color=color,
        #                    vertex_values=None,
        #                    meshdata=None,
        #                    shading=None,
        #                    mode='triangle_fan',
        #                    parent = parent)
    
    def make_dump(self):
        d = dict()
        d["class"] = Cylinder.name
        d["label"] = self.label
        d["circle_center"] = self.circle_center
        d["radius"] = self.radius
        d["height_vector"] = self.height_vector
        d["propEnvShape"] = self.propEnvShape
        return d

    @staticmethod
    def load_dump(dump):
        label = dump["label"]
        circle_center = dump["circle_center"]
        radius = dump["radius"]
        height_vector = dump["height_vector"]
        propEnvShape = dump["propEnvShape"]
        cyl = Cylinder(label=label, circle_center=circle_center, radius=radius, height_vector=height_vector, propEnvShape=propEnvShape)
        return cyl 





