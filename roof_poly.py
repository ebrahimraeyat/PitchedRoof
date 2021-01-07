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

def get_gable_edges(sketch, gables):
	gable_edges = []
	dges = sketch.Shape.Edges
	if gables:
		for e, g in zip(edges, gables):
			if g:
				gable_edges.append(e)
	# gable_edges_xy_coordinate = []
	# for e in gable_edges:
	# 	p1 = e.firstVertex().Point
	# 	p2 = e.lastVertex().Point
	# 	gable_edges_xy_coordinate.append([(p1.x, p1.y), (p2.x, p2.y)])

	return gable_edges

def is_sinks_points_in_gables(sinks, gable_edges=None):
	if not gable_edges or len(sinks) != 2:
		return False
	for e in gable_edges:
		p1, p2 = sinks
		p1 = FreeCAD.Vector(p1.x, p1.y, 0)
		p2 = FreeCAD.Vector(p2.x, p2.y, 0)
		p3 = e.firstVertex().Point
		p4 = e.lastVertex().Point

		if (DraftVecUtils.equals(p1, p3) and DraftVecUtils.equals(p2, p4)) or \
			(DraftVecUtils.equals(p2, p3) and DraftVecUtils.equals(p1, p4)):
			return e
	return False


def get_skeleton_lines_of_roof(sketch=None, gable_edges=None):

	skeleton = get_skeleton_of_roof(sketch)
	lines = []
	h = sketch.Placement.Base.z
	for arc in skeleton:
		e = is_sinks_points_in_gables(arc.sinks, gable_edges)
		if e:
			mid_point = e.CenterOfMass
			arc.source.x = mid_point.x
			arc.source.y = mid_point.y

		for sink in arc.sinks:
			if arc.source.x == sink.x and arc.source.y == sink.y:
				continue
			line = Part.makeLine((arc.source.x, arc.source.y, h), 
							(sink.x, sink.y, h))
			lines.append(line)
	return lines


if __name__ == '__main__':
	get_skeleton_of_roof()



