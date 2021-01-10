from typing import List, Tuple, Iterable
import FreeCAD
import FreeCADGui
import Draft
import Part
import draftgeoutils
import DraftVecUtils
import math
from math import sqrt
import roof_poly
from GeneralFuseResult import GeneralFuseResult
from pitched_roof_funcs import mirror_point_corresponding_to_edge_in_xy


def find_wire_edges_common_with_group_object(wire, faces):
	'''
	This function gives a faces list and a wire. then find
	which edge of wire is common with which face"
	'''
	
	slice_and_correspond_edge = []
	edges = Part.__sortEdges__(wire.Shape.Edges)
	for e_w in edges:
		p1 = e_w.firstVertex().Point
		p2 = e_w.lastVertex().Point
		for face in faces:
			if face.isInside(p1, .1, True) and face.isInside(p2, .1, True):
				slice_and_correspond_edge.append((e_w, face))
				break

	return slice_and_correspond_edge
 
def distance(edge, point):

	dist_vec = draftgeoutils.geometry.findDistance(point, edge)
	if dist_vec:
		dist = sqrt(dist_vec.x ** 2 + dist_vec.y ** 2)
		return dist
	return False


def split(base_shape, tool_shapes, tolerance = 0.0):
    """slice(base_shape, tool_shapes, tolerance = 0.0): functional part of
    Slice feature. Splits base_shape into pieces based on intersections with tool_shapes.
	"""

    shapes = [base_shape] + [Part.Compound([tool_shape]) for tool_shape in tool_shapes] # hack: putting tools into compounds will prevent contamination of result with pieces of tools
    if len(shapes) < 2:
        raise ValueError("No slicing objects supplied!")
    pieces, map = shapes[0].generalFuse(shapes[1:], tolerance)
    gr = GeneralFuseResult(shapes, (pieces,map))
    gr.splitAggregates(gr.piecesFromSource(shapes[0]))
    result = gr.piecesFromSource(shapes[0])
    sh = result[0] if len(result) == 1 else Part.Compound(result)

    shps = sh.childShapes()
    return shps

def unique_points_of_edges_list(
	edges: List
	) -> Iterable[Tuple]:

	points = set()
	for e in edges:
		p1 = e.firstVertex().Point
		p2 = e.lastVertex().Point
		points.add(tuple(p1))
		points.add(tuple(p2))
	return list(points)

def create_3D_roof(
		wire=None,
		angle=25,
		edges=[],
		angles=None,
		):
	if not wire:
		wire = FreeCADGui.Selection.getSelectionEx()[0].Object
	base_level = wire.Placement.Base.z
	if not edges:
		edges, outer_points_edges = roof_poly.get_skeleton_lines_of_roof(wire, angles)
	faces = split(wire.Shape, edges)

	slice_and_correspond_edge = find_wire_edges_common_with_group_object(wire, faces)
	projection_face_points = []
	for edge, face in slice_and_correspond_edge:
		edges = Part.__sortEdges__(face.Edges)
		sort_points = []
		for e in edges:
			p1 = e.firstVertex().Point
			sort_points.append(p1)
		new_points = []
		for point in sort_points:
			x, y = point.x, point.y
			dist = distance(edge, point)
			if not dist or dist < .1:
				h = 0
			else:
				h = dist * math.tan(angle * math.pi / 180)
			for out_point in outer_points_edges:
				x1, y1, e = out_point
				p2 = FreeCAD.Vector(x1, y1, 0)
				if DraftVecUtils.equals(point, p2):
					x, y = mirror_point_corresponding_to_edge_in_xy(
						e, point
						)
			p = (x, y, h + base_level)
			new_points.append(p)
		projection_face_points.append(new_points)
	wire_edges = [i[1] for i in slice_and_correspond_edge]
	return projection_face_points, wire_edges

if __name__ == '__main__':
	projection_face_points, _, _ = create_3D_roof()
	for points in projection_face_points[0]:
		w = Draft.makeWire(points, closed=True, face=True)
		w.ViewObject.ShapeColor = (0.14,0.07,0.85)
		w.ViewObject.Transparency = 40

