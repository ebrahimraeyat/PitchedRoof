__title__ = "PitchedRoof Workbench"
__author__ = "Roknabadi"
__url__ = "https://www.freecadweb.org"

import os

import FreeCADGui
import FreeCAD
import Part
import Draft
import Draft_rc
import ArchComponent

try:
    from PySide import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

import roof3d


def show_warning(message, title="PitchedRoof"):
    QtWidgets.QMessageBox.warning(
        FreeCADGui.getMainWindow(),
        title,
        message,
    )


def get_roof_from_base_selection():
    selection = FreeCADGui.Selection.getSelectionEx()
    if not selection:
        show_warning("Select one or more edges from the base sketch or wire of a roof.")
        return None, None

    sel = selection[0]
    base_obj = sel.Object
    edges_name = [name for name in sel.SubElementNames if "Edge" in name]

    if not edges_name:
        show_warning("Select one or more base edges before using this command.")
        return None, None

    roof = None
    for obj in FreeCAD.ActiveDocument.Objects:
        if hasattr(obj, "IfcType") and obj.IfcType == "Roof" and hasattr(obj, "Base") and obj.Base and obj.Base == base_obj:
            roof = obj
            break

    if roof is None:
        show_warning(
            "Select edges from the roof base sketch or wire, not from the roof solid itself."
        )
        return None, None

    return roof, edges_name


class Roof3D:
    '''the Pitched Roof command definition'''
    def GetResources(self):
        return {"Pixmap"  : "Arch_Roof",
                "MenuText": "Roof",
                "Accel"   : "R, F",
                "ToolTip" : "Creates a roof object from the selected wire."}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):
        sel = FreeCADGui.Selection.getSelectionEx()
        if sel:
            sel = sel[0]
            obj = sel.Object
            if obj.isDerivedFrom("Part::Part2DObjectPython"):
                base_obj = Draft.make_sketch(obj, autoconstraints=True, delete=True)
            elif obj.isDerivedFrom("Sketcher::SketchObject"):
                base_obj = obj
            FreeCADGui.Control.closeDialog()
            roof3d.make_roof(base_obj)
        else:
            FreeCAD.Console.PrintMessage("Please select a base object first" + "\n")
            FreeCADGui.Control.showDialog(ArchComponent.SelectionTaskPanel())
            FreeCAD.ArchObserver = ArchComponent.ArchSelectionObserver(nextCommand="pitched_roof_create_3d")
            FreeCADGui.Selection.addObserver(FreeCAD.ArchObserver)


class PitchedRoofSketch:


    def GetResources(self):

        return {'Pixmap'  : os.path.join(os.path.dirname(__file__), "resources", "icons", "Sketch.svg"),
                'MenuText': "Sketch",
                'ToolTip' : "Creates a new sketch in the current working plane",
                'Accel'   : 'S,K'}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):

        import FreeCADGui
        if hasattr(FreeCAD,"DraftWorkingPlane"):
            FreeCAD.DraftWorkingPlane.setup()
        if hasattr(FreeCADGui,"Snapper"):
            FreeCADGui.Snapper.setGrid()
        sk = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObject','Sketch')
        sk.MapMode = "Deactivated"
        p = FreeCAD.DraftWorkingPlane.getPlacement()
        p.Base = FreeCAD.DraftWorkingPlane.position
        sk.Placement = p
        FreeCADGui.ActiveDocument.setEdit(sk.Name)
        FreeCADGui.activateWorkbench('SketcherWorkbench')
        FreeCADGui.runCommand('Sketcher_CreatePolyline',0)


class GableEdges:


    def GetResources(self):

        return {'Pixmap'  : os.path.join(os.path.dirname(__file__), "resources", "icons", "Gable.svg"),
                'MenuText': "Gable",
                'ToolTip' : "Change the selected edges to gable",
                'Accel'   : 'g,e'}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):

        # import FreeCADGui
        # roof.ViewObject.Visibility = False
        # roof.Base.ViewObject.Visibility = True
        # FreeCADGui.ActiveDocument.ActiveView.viewTop()
        roof, edges_name = get_roof_from_base_selection()
        if roof is None:
            return
        edges_number = []

        angles = roof.Angles
        for name in edges_name:
            if "Edge" in name:
                n = int(name.lstrip("Edge"))
                edges_number.append(n)
                if angles[n - 1] == 90:
                    angles[n - 1] = int(roof.Angle.Value)
                else:
                    angles[n - 1] = 90
        roof.Angles = angles

        new_edges = set(roof.Gables).union(edges_number)
        roof.Gables = list(new_edges)
        FreeCAD.ActiveDocument.recompute()


class AngleEdges:

    def GetResources(self):

        return {'Pixmap'  : os.path.join(os.path.dirname(__file__), "resources", "icons", "Angle.svg"),
                'MenuText': "Angle",
                'ToolTip' : "Change the angle of selected edges",
                'Accel'   : 'a,e'}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):

        # import FreeCADGui
        # roof.ViewObject.Visibility = False
        # roof.Base.ViewObject.Visibility = True
        # FreeCADGui.ActiveDocument.ActiveView.viewTop()
        roof, edges_name = get_roof_from_base_selection()
        if roof is None:
            return

        angles = roof.Angles
        for name in edges_name:
            if "Edge" in name:
                n = int(name.lstrip("Edge"))
                if angles[n - 1] < 0:
                    angles[n - 1] = int(roof.Angle.Value)
                else:
                    angles[n - 1] = -int(roof.Angle.Value)
        roof.Angles = angles

        FreeCAD.ActiveDocument.recompute()




FreeCADGui.addCommand("pitched_roof_sketch", PitchedRoofSketch())
FreeCADGui.addCommand("pitched_roof_create_3d", Roof3D())
FreeCADGui.addCommand("pitched_roof_gable", GableEdges())
FreeCADGui.addCommand("pitched_roof_angle", AngleEdges())

# List of all pitched roof commands
PitchedRoofCommands = [
    "pitched_roof_sketch",
    "pitched_roof_create_3d",
    "pitched_roof_gable",
    "pitched_roof_angle",
]
