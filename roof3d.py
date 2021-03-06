import FreeCAD
import Part
import ArchComponent
import Arch_rc

import extrude_pieces


def adjust_list_len (lst, n, val):
	if len(lst) > n:
		new_lst = lst[:n]
	else:
		new_lst = lst + [val for i in range(n - len(lst))]
	return new_lst


class Roof3d(ArchComponent.Component):

	def __init__(self, obj):
		super().__init__(obj)
		self.set_properties(obj)
		obj.IfcType = "Roof"
		obj.Proxy = self

	def set_properties(self, obj):
		self.Type = "Roof3d"

		if not hasattr(obj, "angle"):
			obj.addProperty(
				"App::PropertyAngle",
				"angle",
				"Roof",
				)

		if not hasattr(obj, "angles"):
			obj.addProperty(
				"App::PropertyIntegerList",
				"angles",
				"Edges",
				)

		if not hasattr(obj, "face_compound"):
			obj.addProperty(
				"Part::PropertyPartShape",
				"face_compound",
				"Roof",
				)

		if not hasattr(obj, "edegs_height"):
			obj.addProperty(
				"App::PropertyFloatList",
				"edegs_height",
				"Edges",
				)

		if not hasattr(obj, "gables"):
			obj.addProperty(
				"App::PropertyIntegerList",
				"gables",
				"Edges",
				)

		if not hasattr(obj, "n"):
			obj.addProperty(
				"App::PropertyInteger",
				"n",
				"Edges",
				)

	def onDocumentRestored(self, obj):
		super().onDocumentRestored(obj)
		self.setProperties(obj)

	def execute(self, obj):

		if hasattr(obj, "Base") and obj.Base:
			edges = obj.Base.Shape.Edges
			obj.n = len(edges)
			w = Part.Wire(edges)
			f = Part.Face(w)
			base_obj = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython", "wire")
			base_obj.Shape = f
			base_obj.ViewObject.Proxy = 0
			projection_face_points, wire_edges = extrude_pieces.create_3D_roof(base_obj, obj.angle, [], obj.angles)

			edegs_height = obj.edegs_height
			obj.edegs_height = adjust_list_len(edegs_height, obj.n, 0)

			edges_angle = obj.angles
			obj.angles = adjust_list_len(edges_angle, obj.n, int(obj.angle.Value))

			faces = []
			if len(set(obj.edegs_height)) > 1:
				bb = w.BoundBox
				xmin, xmax, ymin, ymax = bb.XMin, bb.XMax, bb.YMin, bb.YMax
				p1 = (xmin, ymin, 0)
				p2 = (xmax, ymin, 0)
				p3 = (xmax, ymax, 0)
				p4 = (xmin, ymax, 0)
				e1 = Part.makeLine(p1, p2)
				e2 = Part.makeLine(p2, p3)
				e3 = Part.makeLine(p3, p4)
				e4 = Part.makeLine(p4, p1)
				wire = Part.Wire([e1, e2, e3, e4])
				cut_face = Part.Face(wire)
			for j, points in enumerate(projection_face_points):
				n = len(points)
				points.append(points[0])
				edges = []
				for i in range(n):
					e = Part.makeLine(points[i], points[i + 1])
					edges.append(e)
				wire = Part.Wire(edges)
				face = Part.Face(wire)
				if len(set(obj.edegs_height)) > 1:
					h = obj.edegs_height[j]
					if h > 0:
						f = cut_face.copy()
						f.Placement.Base.z = h
						sh = extrude_pieces.split(face, [f])
						for cutted_face in sh:
							if cutted_face.BoundBox.ZMax > h + 1:
								face = cutted_face
								break

				faces.append(face)

			obj.face_compound = Part.makeCompound(faces)
			shell = Part.Shell(faces)
			obj.Shape = shell.removeSplitter()
			# obj.Base.ViewObject.Visibility = False
			# obj.Base.ViewObject.LineColor = (1.00,0.00,0.00)
			obj.Base.ViewObject.LineWidth = .5

			FreeCAD.ActiveDocument.removeObject(base_obj.Name)
		else:
			return


class ViewProviderRoof3d(ArchComponent.ViewProviderComponent):
	'''A View Provider for the Roof object'''
	def __init__(self, vobj):
		super().__init__(vobj)
		vobj.Transparency = 50
		vobj.LineWidth = 1.00

	def getIcon(self):
		return ":/icons/Arch_Roof_Tree.svg"

	def attach(self, vobj):
		self.Object = vobj.Object
		return


def make_roof(baseobj=None, angle=25, name="Roof"):

	if not FreeCAD.ActiveDocument:
		FreeCAD.Console.PrintError("No active document. Aborting\n")
		return
	obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name)
	obj.Label = name
	Roof3d(obj)
	if FreeCAD.GuiUp:
		ViewProviderRoof3d(obj.ViewObject)
	if baseobj:
		obj.Base = baseobj
	obj.angle = angle
	FreeCAD.ActiveDocument.recompute()
	return obj




