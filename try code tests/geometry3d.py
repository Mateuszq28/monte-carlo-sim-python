import Geometry3D


cuboid = Geometry3D.Parallelepiped(base_point=Geometry3D.Point(0,0,0),
                                   v1=Geometry3D.Vector(5,0,0),
                                   v2=Geometry3D.Vector(0,5,0),
                                   v3=Geometry3D.Vector(0,0,5))

p_to_check = [(2,2,2), (2,5,2), (5,5,5), (7,7,7), (0,0,7)]
p_to_check = [Geometry3D.Point(p) for p in p_to_check]
p_to_check_names = ["point_in", "point_boundary", "point_vert", "point_out", "point_out2"]

for p, name in zip(p_to_check, p_to_check_names):
    # not working
    # dist = cuboid.distance(p)
    # print(name, dist)

    p_segm_start = Geometry3D.Point(-10,-10,-10)
    seg = Geometry3D.Segment(p_segm_start, p)
    intersect = cuboid.intersection(seg)
    print(name, intersect)

    # not working
    # dist = cuboid.distance(seg)
    # print(name, dist)
                




# box = Geometry3D.Parallelepiped(Geometry3D.Point(0,0,0), Geometry3D.Vector(1,0,0), Geometry3D.Vector(0,1,0), Geometry3D.Vector(0,0,1))
# polygons = box.convex_polygons
# print()
# print(polygons)
# print()
# planes = [pol.plane.n for pol in polygons]
# print(planes)
# print()

# p_list = [Geometry3D.Point(0,0,0), Geometry3D.Point(0,0,1), Geometry3D.Point(0,1,0), Geometry3D.Point(0,1,1)]
# polygon2 = Geometry3D.ConvexPolygon(pts=p_list)
# print(polygon2.plane.n)
# print()


# polygon2.center_point