import FreeCADGui
import polyskel
import Part


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
	lines = []
	h = sketch.Placement.Base.z
	for arc in skeleton:
		for sink in arc.sinks:
			if arc.source.x == sink.x and arc.source.y == sink.y:
				continue
			line = Part.makeLine((arc.source.x, arc.source.y, h), 
							(sink.x, sink.y, h))
			lines.append(line)
	return lines


if __name__ == '__main__':
	get_skeleton_of_roof()



