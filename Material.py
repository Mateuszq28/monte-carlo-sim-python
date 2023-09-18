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

        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)
        
    def fun_in(self, point):
        pass

    def fun_boundary(self, point):
        pass

    def fun_intersect(self, p1, p2):
        pass

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
    if cl == "Cuboid":
        return Cuboid.load_dump(dump)
    if cl == "Cylinder":
        return Cylinder.load_dump(dump)


# --- SHAPES ---

class Cuboid(Material):
        
    def __init__(self, label, start_p, end_p, propEnvShape=None):
        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)

        self.label = label
        self.start_p = start_p
        self.end_p = end_p
        self.propEnvShape = propEnvShape

        self.start_p_stat = self.point_relative2static(start_p, propEnvShape)
        self.end_p_stat = self.point_relative2static(end_p, propEnvShape)

        ver1 = [self.end_p_stat[0], self.start_p_stat[1], self.start_p_stat[2]]
        ver2 = [self.start_p_stat[0], self.end_p_stat[1], self.start_p_stat[2]]
        ver3 = [self.start_p_stat[0], self.start_p_stat[1], self.end_p_stat[2]]
        vec1 = np.array(ver1) - np.array(self.start_p_stat)
        vec2 = np.array(ver2) - np.array(self.start_p_stat)
        vec3 = np.array(ver3) - np.array(self.start_p_stat)
        vec1, vec2, vec3 = [Geometry3D.Vector(vec) for vec in [vec1, vec2, vec3]]
        self.geo_start_p = Geometry3D.Point(self.start_p_stat)
        self.cuboid = Geometry3D.geometry.Parallelepiped(base_point=self.geo_start_p, v1=vec1, v2=vec2, v3=vec3)

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
    
    def fun_intersect(self, p1, p2):
        geo_p1 = Geometry3D.Point(p1)
        geo_p2 = Geometry3D.Point(p2)
        seg = Geometry3D.Segment(geo_p1, geo_p2)
        intersec = self.cuboid.intersection(seg)
        if intersec is None:
            return None
        elif isinstance(intersec, Geometry3D.Segment):
            inter_p1 = intersec.start_point
            inter_p2 = intersec.end_point
            if inter_p1 == geo_p1 and inter_p2 == geo_p2:
                # whole segment is material, so there was no boundary cross
                return None
            dist1 = geo_p1.distance(inter_p1)
            dist2 = geo_p1.distance(inter_p2)
            if dist1 < dist2:
                out_geo_p = inter_p1
            else:
                out_geo_p = inter_p2
        elif isinstance(intersec, Geometry3D.Point):
            out_geo_p = intersec
        else:
            raise NotImplementedError()
        out_p = [out_geo_p.x, out_geo_p.y, out_geo_p.z]
        return out_p
    
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
        print(point)
        raise NotImplementedError()
    
    def fun_vispy_obj(self, parent):
        polygon = self.cuboid.convex_polygons[3]
        polygon_points = np.array([[p.x, p.y, p.z] for p in polygon.points])
        c = self.config["tissue_properties"][str(self.label)]["print color"]
        # c = ImageColor.getrgb(c)
        # color = [c[0], c[1], c[2], 255]
        # color = [val/255 for val in color]
        color = color_array.Color(c, alpha=1.0)
        scene.visuals.Mesh(vertices = polygon_points,
                           faces=None,
                           vertex_colors=None,
                           face_colors=None,
                           color=color,
                           vertex_values=None,
                           meshdata=None,
                           shading=None,
                           mode='triangle_fan',
                           parent = parent)
    
    def make_dump(self):
        d = dict()
        d["class"] = "Cuboid"
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
        
    def __init__(self, label, circle_center, radius, height_vector, propEnvShape=None):
        with open("config.json") as f:
            # get simulation config parameters
            self.config = json.load(f)

        self.label = label
        self.circle_center = circle_center
        self.radius = radius
        self.height_vector = height_vector
        self.propEnvShape = propEnvShape

        self.circle_center_stat = self.point_relative2static(self.circle_center, self.propEnvShape)
        self.geo_circle_center = Geometry3D.Point(self.circle_center_stat)
        self.geo_height_vector = Geometry3D.Vector(self.height_vector)
        self.cyl = Geometry3D.geometry.Cylinder(self.geo_circle_center, self.radius, self.geo_height_vector, n=10)
    
    def fun_intersect(self, p1, p2):
        geo_p1 = Geometry3D.Point(p1)
        geo_p2 = Geometry3D.Point(p2)
        seg = Geometry3D.Segment(geo_p1, geo_p2)
        intersec = self.cyl.intersection(seg)
        if intersec is None:
            return None
        elif isinstance(intersec, Geometry3D.Segment):
            inter_p1 = intersec.start_point
            inter_p2 = intersec.end_point
            dist1 = self.geo_circle_center.distance(inter_p1)
            dist2 = self.geo_circle_center.distance(inter_p2)
            if dist1 < dist2:
                out_geo_p = inter_p1
            else:
                out_geo_p = inter_p2
        elif isinstance(intersec, Geometry3D.Point):
            out_geo_p = intersec
        else:
            raise NotImplementedError()
        out_p = [out_geo_p.x, out_geo_p.y, out_geo_p.z]
        return out_p

    def fun_in(self, point):
        geo_p = Geometry3D.Point(point)
        return geo_p in self.cyl
    
    def fun_boundary(self, point):
        geo_p = Geometry3D.Point(point)
        polygons = self.cyl.convex_polygons
        ins = [(geo_p in pl) for pl in polygons]
        return True in ins
    
    def fun_plane_normal_vec(self, point):
        geo_p = Geometry3D.Point(point)
        polygons = self.cyl.convex_polygons
        ins = [(geo_p in pl) for pl in polygons]
        normals_in = [pl.plane.n for pl, in_flag in zip(polygons, ins) if in_flag]
        return normals_in[0]            
    
    def fun_vispy_obj(self, parent):
        polygons = self.cyl.convex_polygons
        
        top_bottom = [poly for poly in polygons if len(poly.points) != 4]
        top_bottom_center = [poly.center_point for poly in top_bottom]
        top_bottom_points = [[[p.x, p.y, p.z] for p in poly.points] for poly in top_bottom]
        top_bottom_points = [[[center.x, center.y, center.z]]+poly for poly, center in zip(top_bottom_points, top_bottom_center)]
        top_bottom_points = np.array(top_bottom_points)

        walls = [poly for poly in polygons if len(poly.points) == 4]
        walls = [[[p.x, p.y, p.z] for p in poly.points] for poly in walls]
        walls = np.array(walls)

        c = self.config["tissue_properties"][str(self.label)]["print color"]
        # c = ImageColor.getrgb(c)
        # color = [c[0], c[1], c[2], 255]
        # color = [val/255 for val in color]
        color = color_array.Color(c, alpha=1.0)

        vis_walls = None
        for wall in walls:
            scene.visuals.Mesh(vertices = wall,
                               faces=None,
                               vertex_colors=None,
                               face_colors=None,
                               color=color,
                               vertex_values=None,
                               meshdata=None,
                               shading=None,
                               mode='triangle_fan',
                               parent = parent)
        
        vis_top = None
        vis_top = scene.visuals.Mesh(vertices = top_bottom_points[0],
                                     faces=None,
                                     vertex_colors=None,
                                     face_colors=None,
                                     color=color,
                                     vertex_values=None,
                                     meshdata=None,
                                     shading=None,
                                     mode='triangle_fan',
                                     parent = parent)
        
        vis_bottom = None
        vis_bottom = scene.visuals.Mesh(vertices = top_bottom_points[1],
                                        faces=None,
                                        vertex_colors=None,
                                        face_colors=None,
                                        color=color,
                                        vertex_values=None,
                                        meshdata=None,
                                        shading=None,
                                        mode='triangle_fan',
                                        parent = parent)


        return (vis_top, vis_bottom, vis_walls)
    
    def make_dump(self):
        d = dict()
        d["class"] = "Cylinder"
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





