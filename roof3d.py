import FreeCAD
import Part
import ArchComponent
import Arch_rc

import extrude_pieces


PROPERTY_DEFINITIONS = (
	{
		"name": "Angle",
		"legacy_name": "angle",
		"type": "App::PropertyAngle",
		"group": "Roof",
	},
	{
		"name": "Angles",
		"legacy_name": "angles",
		"type": "App::PropertyIntegerList",
		"group": "Edges",
	},
	{
		"name": "FaceCompound",
		"legacy_name": "face_compound",
		"type": "Part::PropertyPartShape",
		"group": "Roof",
	},
	{
		"name": "EdgesHeight",
		"legacy_name": "edegs_height",
		"type": "App::PropertyFloatList",
		"group": "Edges",
	},
	{
		"name": "Gables",
		"legacy_name": "gables",
		"type": "App::PropertyIntegerList",
		"group": "Edges",
	},
	{
		"name": "EdgeCount",
		"legacy_name": "n",
		"type": "App::PropertyInteger",
		"group": "Edges",
	},
)


def adjust_list_len (lst, n, val):
	if len(lst) > n:
		new_lst = lst[:n]
	else:
		new_lst = lst + [val for i in range(n - len(lst))]
	return new_lst


def has_property(obj, name):
	return name in getattr(obj, "PropertiesList", [])


def copy_property_value(obj, source_name, target_name):
	if has_property(obj, source_name) and has_property(obj, target_name):
		setattr(obj, target_name, getattr(obj, source_name))


class Roof3d(ArchComponent.Component):

	def __init__(self, obj):
		super().__init__(obj)
		self.set_properties(obj)
		obj.IfcType = "Roof"
		obj.Proxy = self

	def set_properties(self, obj):
		self.Type = "Roof3d"

		for prop in PROPERTY_DEFINITIONS:
			created = False
			if not has_property(obj, prop["name"]):
				obj.addProperty(
					prop["type"],
					prop["name"],
					prop["group"],
					)
				created = True

			legacy_name = prop["legacy_name"]
			if has_property(obj, legacy_name):
				if created:
					copy_property_value(obj, legacy_name, prop["name"])
				obj.setEditorMode(legacy_name, 2)

		self.sync_legacy_properties(obj)

	def sync_legacy_properties(self, obj):
		for prop in PROPERTY_DEFINITIONS:
			legacy_name = prop["legacy_name"]
			if has_property(obj, legacy_name):
				copy_property_value(obj, prop["name"], legacy_name)

	def onDocumentRestored(self, obj):
		super().onDocumentRestored(obj)
		self.setProperties(obj)

	def execute(self, obj):

		if hasattr(obj, "Base") and obj.Base:
			edges = obj.Base.Shape.Edges
			obj.EdgeCount = len(edges)
			w = Part.Wire(edges)
			f = Part.Face(w)
			base_obj = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython", "wire")
			base_obj.Shape = f
			base_obj.ViewObject.Proxy = 0
			projection_face_points, wire_edges = extrude_pieces.create_3D_roof(base_obj, obj.Angle, [], obj.Angles)

			edges_height = obj.EdgesHeight
			obj.EdgesHeight = adjust_list_len(edges_height, obj.EdgeCount, 0)

			edges_angle = obj.Angles
			obj.Angles = adjust_list_len(edges_angle, obj.EdgeCount, int(obj.Angle.Value))

			faces = []
			if len(set(obj.EdgesHeight)) > 1:
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
				if len(set(obj.EdgesHeight)) > 1:
					h = obj.EdgesHeight[j]
					if h > 0:
						f = cut_face.copy()
						f.Placement.Base.z = h
						sh = extrude_pieces.split(face, [f])
						for cutted_face in sh:
							if cutted_face.BoundBox.ZMax > h + 1:
								face = cutted_face
								break

				faces.append(face)

			obj.FaceCompound = Part.makeCompound(faces)
			shell = Part.Shell(faces)
			obj.Shape = shell.removeSplitter()
			self.sync_legacy_properties(obj)
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
	obj.Angle = angle
	FreeCAD.ActiveDocument.recompute()
	return obj




