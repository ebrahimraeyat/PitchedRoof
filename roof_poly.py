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
	if not edges or len(sinks) != 2:
		return False
	for e in edges:
		p1, p2 = sinks
		p1 = FreeCAD.Vector(p1.x, p1.y, 0)
		p2 = FreeCAD.Vector(p2.x, p2.y, 0)
		p3 = e.firstVertex().Point
		p4 = e.lastVertex().Point

		if (DraftVecUtils.equals(p1, p3) and DraftVecUtils.equals(p2, p4)) or \
			(DraftVecUtils.equals(p2, p3) and DraftVecUtils.equals(p1, p4)):
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
			print("find gable!")
			mid_point = gable_e.CenterOfMass
			arc.source.x = mid_point.x
			arc.source.y = mid_point.y
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



