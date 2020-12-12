import FreeCADGui
import polyskel
import Part


def get_skeleton_of_roof(sketch=None):
	if not sketch:
		sketch = FreeCADGui.Selection.getSelection()[0]
	x_plus = sketch.Shape.BoundBox.XMin
	y_plus = sketch.Shape.BoundBox.YMin
	es = sketch.Shape.Wires[0].Edges
	es = Part.__sortEdges__(es)

	poly = []
	for e in es:
		v1 = e.firstVertex()
		poly.append((v1.X - x_plus, v1.Y - y_plus))

	skeleton = polyskel.skeletonize(poly, [])
	lines = []
	h = sketch.Placement.Base.z
	for arc in skeleton:
		for sink in arc.sinks:
			if arc.source.x == sink.x and arc.source.y == sink.y:
				continue
			line = Part.makeLine((arc.source.x + x_plus, arc.source.y + y_plus, h), 
							(sink.x + x_plus, sink.y + y_plus, h))
			lines.append(line)
	return lines


if __name__ == '__main__':
	get_skeleton_of_roof()



