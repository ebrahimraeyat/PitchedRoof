import FreeCAD
import FreeCADGui
import polyskel
import Part
import DraftVecUtils


def get_skeleton_of_roof(sketch=None):
	if not sketch:
		sketch = FreeCADGui.Selection.getSelection()[0]
	es = sketch.Shape.Wires[0].Edges
	es = Part.__sortEdges__(es)

	poly = []
	for e in es:
		v1 = e.firstVertex()
		poly.append((v1.X, v1.Y))

	skeleton = polyskel.skeletonize(poly, [])
	return skeleton

def get_gable_edges(sketch, angles):
	gable_edges = []
	edges = sketch.Shape.Edges
	for e, angle in zip(edges, angles):
		if angle == 90:
			gable_edges.append(e)

	return gable_edges

def get_negative_edges(sketch, angles):
	negative_edges = []
	edges = sketch.Shape.Edges
	for e, angle in zip(edges, angles):
		if angle < 0:
			negative_edges.append(e)

	return negative_edges

def is_sinks_points_in_edges(sinks, edges=None):
	if not edges:
		return False
	for e in edges:
		p1 = e.firstVertex().Point
		p2 = e.lastVertex().Point
		common_points = []
		for p in sinks:
			p = FreeCAD.Vector(p.x, p.y, 0)
			if DraftVecUtils.equals(p, p1) or DraftVecUtils.equals(p, p2):
				common_points.append(p)
		if len(common_points) == 2:
			return e

	return False


def get_skeleton_lines_of_roof(sketch=None, angles=None):

	skeleton = get_skeleton_of_roof(sketch)
	lines = []
	h = sketch.Placement.Base.z
	gable_edges = get_gable_edges(sketch, angles)
	negative_edges = get_negative_edges(sketch, angles)
	outer_points_edges = []
	for arc in skeleton:
		gable_e = is_sinks_points_in_edges(arc.sinks, gable_edges)
		if gable_e:
			mid_point = gable_e.CenterOfMass
			arc.source.x = mid_point.x
			arc.source.y = mid_point.y
			if len(arc.sinks) == 2:
				continue
		negative_edge = is_sinks_points_in_edges(arc.sinks, negative_edges)
		if negative_edge:
			p = FreeCAD.Vector(arc.source.x, arc.source.y, 0)
			outer_points_edges.append([arc.source.x, arc.source.y, negative_edge])
		for sink in arc.sinks:
			if arc.source.x == sink.x and arc.source.y == sink.y:
				continue
			line = Part.makeLine((arc.source.x, arc.source.y, h), 
							(sink.x, sink.y, h))
			lines.append(line)
	return lines, outer_points_edges


if __name__ == '__main__':
	get_skeleton_of_roof()



