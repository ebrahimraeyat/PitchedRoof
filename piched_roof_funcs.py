

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
