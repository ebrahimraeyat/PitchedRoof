## FreeCAD PitchedRoof Workbench

Create adaptive pitched roofs from a closed sketch or wire in [FreeCAD](https://freecad.org).

This workbench is useful when you want roof faces to rebuild automatically after the base shape changes. It focuses on quickly generating roof surfaces for common architectural workflows and lets you adjust individual roof edges after creation.

![roof](https://user-images.githubusercontent.com/8196112/101233149-c1a4dc00-36cb-11eb-9ecc-c083891afae3.gif)

## Features

- Create a roof from a closed 2D sketch or wire
- Recompute the roof when the base sketch changes
- Mark selected edges as gables
- Flip selected edges to the opposite roof angle
- Edit roof properties from the FreeCAD property editor

## Commands

The workbench provides four commands:

1. **Sketch** - creates a new sketch on the current working plane
2. **Roof** - creates a pitched roof from the selected sketch or wire
3. **Gable** - converts selected roof edges to gable edges
4. **Angle** - flips the selected roof edges to the opposite slope

## Requirements

- FreeCAD
- Python package: `euclid3`

## Installation

### Windows

1. Close FreeCAD.
2. Open your FreeCAD Mod folder:
	- usually `%APPDATA%\FreeCAD\Mod`
3. Clone or extract this repository into that folder so you get:
	- `%APPDATA%\FreeCAD\Mod\PitchedRoof`
4. Install the Python dependency `euclid3` using the Python that ships with FreeCAD.

Example PowerShell command:

```powershell
& "C:\Program Files\FreeCAD 1.0\bin\python.exe" -m pip install euclid3
```

If your FreeCAD is installed elsewhere, change the path accordingly.

### Linux

#### Debian / Ubuntu

```bash
sudo apt install freecad-python3 git
python3 -m pip install --user euclid3
mkdir -p "$HOME/.local/share/FreeCAD/Mod"
cd "$HOME/.local/share/FreeCAD/Mod"
git clone https://github.com/ebrahimraeyat/PitchedRoof.git
```

For older FreeCAD installations, the Mod folder may be:

```bash
$HOME/.FreeCAD/Mod
```

### Verify installation

1. Start FreeCAD.
2. Switch to the **PitchedRoof** workbench.
3. Confirm the toolbar shows the four commands: **Sketch**, **Roof**, **Gable**, and **Angle**.

## Quick start

1. Switch to the **PitchedRoof** workbench.
2. Create a closed base shape with **Sketch**, or select an existing closed sketch/wire.
3. Click **Roof**.
4. Select the created roof object and change its properties such as `Angle`, `Angles`, `Edges Height`, or `Gables`.
5. Edit the base sketch later if needed and recompute the document.

## Step-by-step tutorials

### 1) Sketch tool

Use this when you want to create a new roof outline from scratch.

Steps:

1. Activate the **PitchedRoof** workbench.
2. Click **Sketch**.
3. Draw a **closed** polyline in Sketcher.
4. Close the sketch and finish editing.

Tip: the tool works best with a valid closed outline.

### 2) Roof tool

Use this to generate the roof surface.

Steps:

1. Select a closed sketch or a 2D wire.
2. Click **Roof**.
3. A new roof object is created.
4. Select the roof object and adjust properties in the property editor.

Important:

- The base shape must be closed.
- Open lines or invalid profiles cannot produce a valid roof.

### 3) Gable tool

Use this to convert specific roof sides into gables.

Steps:

1. Select the **base sketch/wire edges** that correspond to the roof edges you want to modify.
2. Click **Gable**.
3. Recompute if needed.
4. The selected edges are toggled to gable behavior.

Tip: you can apply this to one edge or several edges in the same operation.

### 4) Angle tool

Use this to invert the slope direction of selected edges.

Steps:

1. Select one or more edges from the roof base sketch/wire.
2. Click **Angle**.
3. The edge angle is flipped to the opposite sign.
4. Recompute if needed.

This is useful for more complex roof forms where some edges should slope inward or outward differently.

## Editing roof properties

After creating a roof, the main properties are:

- `Angle` - default roof angle
- `Angles` - per-edge angles
- `Edges Height` - per-edge height offsets
- `Gables` - list of edges treated as gables
- `Edge Count` - number of base edges

## Troubleshooting

- If the roof is not created, make sure the base profile is closed.
- If the result looks wrong, verify that the sketch does not contain overlapping or accidental extra geometry.
- After editing the sketch, recompute the document.
- If FreeCAD does not show the workbench, confirm the folder name is exactly `PitchedRoof` inside the Mod directory.

## Discussion

Forum thread to discuss this workbench can be found in the [FreeCAD Subforums](https://forum.freecadweb.org/viewtopic.php?f=23&t=51382).

## Contribute

Pull requests are welcome. Please feel free to discuss ideas on the forum thread or in the issue tracker.