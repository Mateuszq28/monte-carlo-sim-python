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


# --- SHAPES ---

class Cuboid(Material):
        
    def __init__(self, label, start_p, end_p, propEnvShape=None):
        self.label = label

        self.start_p = self.point_relative2static(start_p, propEnvShape)
        self.end_p = self.point_relative2static(end_p, propEnvShape)

        ver1 = [end_p[0], start_p[1], start_p[2]]
        ver2 = [start_p[0], end_p[1], start_p[2]]
        ver3 = [start_p[0], start_p[1], end_p[2]]
        vec1 = np.array(ver1) - np.array(start_p)
        vec2 = np.array(ver2) - np.array(start_p)
        vec3 = np.array(ver3) - np.array(start_p)
        vec1, vec2, vec3 = [Geometry3D.Vector(vec) for vec in [vec1, vec2, vec3]]
        self.geo_start_p = Geometry3D.Point(start_p)
        self.cuboid = Geometry3D.geometry.Parallelepiped(base_point=self.geo_start_p, v1=vec1, v2=vec2, v3=vec3)

    def fun_in(self, point):
        for i in range(3):
            if not (self.start_p[i] <= point[i] <= self.end_p[i]):
                return False
        return True
    
    def check_boundaries(self, point):
        return [math.isclose(self.start_p[0], point[0]), math.isclose(self.end_p[0], point[0]), math.isclose(self.start_p[1], point[1]), math.isclose(self.end_p[1], point[1]), math.isclose(self.start_p[2], point[2]), math.isclose(self.end_p[2], point[2])]
    
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
            dist1 = self.geo_start_p.distance(inter_p1)
            dist2 = self.geo_start_p.distance(inter_p2)
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
        if boundary_flags[3]:
            return [0, 0, 1]
        raise NotImplementedError()
    
    def fun_vispy_obj(self, parent):
        c = self.config["tissue_properties"][str(self.label)]["print color"]
        # c = ImageColor.getrgb(c)
        # color = [c[0], c[1], c[2], 255]
        # color = [val/255 for val in color]
        color = color_array.Color(c, alpha=1.0),
        box = visuals.box.BoxVisual(width = self.end_p[0] - self.start_p[0],
                                    height = self.end_p[0] - self.start_p[0],
                                    depth = self.end_p[0] - self.start_p[0],
                                    width_segments = 1,
                                    height_segments = 1,
                                    depth_segments = 1,
                                    planes = None,
                                    vertex_colors = None,
                                    face_colors = None,
                                    color = color,
                                    edge_color=None,
                                    parent = parent)
        return box
    

class Cylinder(Material):
        
    def __init__(self, label, circle_center, radius, height_vector, propEnvShape=None):
        self.label = label
        circle_center = self.point_relative2static(circle_center, propEnvShape)
        self.geo_circle_center = Geometry3D.Point(circle_center)
        geo_height_vector = Geometry3D.Vector(height_vector)
        self.cyl = Geometry3D.geometry.Cylinder(self.geo_circle_center, radius, geo_height_vector, n=10)
    
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

        walls = [poly for poly in polygons if len(poly.points) == 4]
        walls = [[[p.x, p.y, p.z] for p in poly.points] for poly in walls]

        c = self.config["tissue_properties"][str(self.label)]["print color"]
        # c = ImageColor.getrgb(c)
        # color = [c[0], c[1], c[2], 255]
        # color = [val/255 for val in color]
        color = color_array.Color(c, alpha=1.0),

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





