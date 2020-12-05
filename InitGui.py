__title__ = "PitchedRoof Workbench"
__author__ = "Roknabadi"
__url__ = "https://www.freecadweb.org"


from pathlib import Path
import FreeCADGui
import pitched_roof_gui

wb_icon_path = str(
    Path(pitched_roof_gui.__file__).parent.absolute() / "resources" / "icons" / "pitched_roof.png"
)


class PitchedRoofWorkbench(FreeCADGui.Workbench):
    global wb_icon_path
    MenuText = "PitchedRoof"
    ToolTip = "Create Building PitchedRoof"
    Icon = wb_icon_path

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        import pitched_roof_gui
        from pathlib import Path

        self.metalroof_commands = pitched_roof_gui.PitchedRoofCommands
        self.appendToolbar("PitchedRoofCommands", self.metalroof_commands)


    def Activated(self):
        """This function is executed when the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("PitchedRoofCommands", self.metalroof_commands)

    def GetClassName(self):
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(PitchedRoofWorkbench())
