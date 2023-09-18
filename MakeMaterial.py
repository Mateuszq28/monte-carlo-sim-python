from Material import Material
import numpy as np
import Geometry3D
import math

class MakeMaterial():
    def __init__(self):
        pass

    # --- MAKE COMPLICATED MATERIALS ---

    # --- MAKE RAW SHAPES ---
    
    def cuboid(self, label, start_p, end_p, propEnvShape=None):
        start_p = self.point_relative2static(start_p, propEnvShape)
        end_p = self.point_relative2static(end_p, propEnvShape)

        ver1 = [end_p[0], start_p[1], start_p[2]]
        ver2 = [start_p[0], end_p[1], start_p[2]]
        ver3 = [start_p[0], start_p[1], end_p[2]]
        vec1 = np.array(ver1) - np.array(start_p)
        vec2 = np.array(ver2) - np.array(start_p)
        vec3 = np.array(ver3) - np.array(start_p)
        vec1, vec2, vec3 = [Geometry3D.Vector(vec) for vec in [vec1, vec2, vec3]]
        geo_start_p = Geometry3D.Point(start_p)
        cuboid = Geometry3D.geometry.Parallelepiped(base_point=geo_start_p, v1=vec1, v2=vec2, v3=vec3)

        def fun_in(point):
            for i in range(3):
                if not (start_p[i] <= point[i] <= end_p[i]):
                    return False
            return True
        
        def check_boundaries(point):
            return [math.isclose(start_p[0], point[0]), math.isclose(end_p[0], point[0]), math.isclose(start_p[1], point[1]), math.isclose(end_p[1], point[1]), math.isclose(start_p[2], point[2]), math.isclose(end_p[2], point[2])]
        
        def fun_boundary(point):
            return True in check_boundaries(point)
            # old
            # for i in range(3):
            #     at_start_ax = math.isclose(start_p[i], point[i])
            #     at_end_ax = math.isclose(end_p[i], point[i])
            #     if not (at_start_ax or at_end_ax):
            #         return False
            # return True
        
        def fun_intersect(p1, p2):
            geo_p1 = Geometry3D.Point(p1)
            geo_p2 = Geometry3D.Point(p2)
            seg = Geometry3D.Segment(geo_p1, geo_p2)
            intersec = cuboid.intersection(seg)
            if intersec is None:
                return None
            elif isinstance(intersec, Geometry3D.Segment):
                inter_p1 = intersec.start_point
                inter_p2 = intersec.end_point
                dist1 = geo_start_p.distance(inter_p1)
                dist2 = geo_start_p.distance(inter_p2)
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
        
        def fun_plane_normal_vec(point):
            boundary_flags = check_boundaries(point)
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
 
        material = Material(label=label, fun_in=fun_in, fun_boundary=fun_boundary, fun_intersect=fun_intersect, fun_plane_normal_vec=fun_plane_normal_vec)
        return material



    # --- TOOLS ---

    def point_relative2static(self, point, propEnvShape):
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
    



# makeMaterials = MakeMaterial()
# cuboid = makeMaterials.cuboid(label=0, start_p=(0,0,0), end_p=(5,5,5), propEnvShape=None)

# p_to_check = [(2,2,2), (2,5,2), (5,5,5), (7,7,7), (0,0,7)]
# p_to_check = [Geometry3D.Point(p) for p in p_to_check]
# p_to_check_names = ["point_in", "point_boundary", "point_vert", "point_out", "point_out2"]

# for p, name in zip(p_to_check, p_to_check_names):
#     # not working
#     # dist = cuboid.distance(p)
#     # print(name, dist)

#     p_segm_start = Geometry3D.Point(10,10,10)
#     seg = Geometry3D.Segment(p_segm_start, p)
#     intersect = cuboid.intersection(seg)
#     print(name, intersect)

#     # not working
#     # dist = cuboid.distance(seg)
#     # print(name, dist)

                



