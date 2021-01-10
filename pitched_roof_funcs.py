# import FreeCAD
# import Part
# import draftgeoutils
# import DraftGeomUtils
# import DraftVecUtils
from extrude_pieces import distance

def intersection_point_of_two_edges_in_xy_plane(e1, e2):
	'''
	Note that the intersection point is for the infinitely long lines defined by the points,
	rather than the line segments between the points, and can produce an intersection point
	beyond the lengths of the line segments
	'''
	x1, y1, z1 = e1.Vertexes[0].Point
	x2, y2, z2 = e1.Vertexes[1].Point
	x3, y3, z3 = e2.Vertexes[0].Point
	x4, y4, z4 = e2.Vertexes[1].Point
	divisor = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
	x = ((x1 * y1 - y1 * x1) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / divisor
	y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / divisor

	return x, y


def mirror_point_corresponding_to_edge_in_xy(e, p):
	x1, y1 = p.x, p.y
	x2,y2, _ = e.firstVertex().Point
	x3,y3, _ = e.lastVertex().Point
	# if x3 == x2:
	# 	d = distance(e, p)
	# 	return 2 * d - x1, y1
	m = (y3 - y2) / (x3 - x2)
	c = (x3 * y2 - x2 * y3) / (x3 - x2)
	d = (x1 + (y1 - c) * m) / (1 + m ** 2)
	x4 = 2 * d - x1
	y4 = 2 * d * m - y1 + 2 * c
	return x4, y4

