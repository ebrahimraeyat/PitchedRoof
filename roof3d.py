import FreeCAD
import Part
import ArchComponent
import Arch_rc

import polyskel
import extrude_pieces

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

		if not hasattr(obj, "face_compound"):
			obj.addProperty(
				"Part::PropertyPartShape",
				"face_compound",
				"Roof",
				)

	def onDocumentRestored(self, obj):
		super().onDocumentRestored(obj)
		self.setProperties(obj)

	def execute(self, obj):

		if hasattr(obj, "Base") and obj.Base:
			w = Part.Wire(obj.Base.Shape.Edges)
			f = Part.Face(w)
			base_obj = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython", "wire")
			base_obj.Shape = f
			base_obj.ViewObject.Proxy = 0
			projection_face_points, wire_edges = extrude_pieces.create_3D_roof(base_obj, obj.angle)

			faces = []
			for points in projection_face_points:
				n = len(points)
				points.append(points[0])
				edges = []
				for i in range(n):
					e = Part.makeLine(points[i], points[i + 1])
					edges.append(e)
				wire = Part.Wire(edges)
				face = Part.Face(wire)
				faces.append(face)
			obj.face_compound = Part.makeCompound(faces)
			shell = Part.Shell(faces)
			obj.Shape = shell.removeSplitter()
			obj.Base.ViewObject.Visibility = False
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




