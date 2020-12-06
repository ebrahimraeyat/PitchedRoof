__title__ = "PitchedRoof Workbench"
__author__ = "Roknabadi"
__url__ = "https://www.freecadweb.org"


import FreeCADGui
import FreeCAD
import Part
import Draft
import Draft_rc
import ArchComponent

import roof3d


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


FreeCADGui.addCommand("pitched_roof_create_3d", Roof3D())

# List of all pitched roof commands
PitchedRoofCommands = [
    "pitched_roof_create_3d",
]
