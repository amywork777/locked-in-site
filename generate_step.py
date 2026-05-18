#!/usr/bin/env python3
"""Generate STEP files for Locked In variants using FreeCAD"""

import sys
sys.path.insert(0, '/usr/lib/freecad/lib')

import FreeCAD
import Part
import math

# Dimensions (mm)
EXTERIOR_L = 199
EXTERIOR_W = 112
BASE_H = 22
LID_H = 10
POCKET_L = 175
POCKET_W = 88
POCKET_D = 16

def rounded_box(l, w, h, r=3):
    """Create a box with rounded vertical edges"""
    box = Part.makeBox(l, w, h, FreeCAD.Vector(-l/2, -w/2, 0))
    try:
        vertical_edges = []
        for i, edge in enumerate(box.Edges):
            if abs(edge.Vertexes[0].X - edge.Vertexes[1].X) < 0.01 and abs(edge.Vertexes[0].Y - edge.Vertexes[1].Y) < 0.01:
                vertical_edges.append(box.Edges[i])
        if vertical_edges and r > 0:
            box = box.makeFillet(r, vertical_edges)
    except:
        pass
    return box

def create_base_v2():
    """Base with wave spline ridges"""
    base = rounded_box(EXTERIOR_L, EXTERIOR_W, BASE_H)
    pocket = rounded_box(POCKET_L, POCKET_W, POCKET_D + 1, r=3.2)
    pocket.translate(FreeCAD.Vector(0, 0, BASE_H - POCKET_D))
    base = base.cut(pocket)
    
    # Wave parameters
    WAVE_AMP = 3
    WAVE_PERIODS = 2
    WAVE_WIDTH = 8
    WAVE_OFFSET = 35
    WAVE_LEN = EXTERIOR_L - 50
    steps = 30
    
    for y_off in [-WAVE_OFFSET, WAVE_OFFSET]:
        # Build wave ridge as series of cylinders
        for i in range(steps):
            x1 = -WAVE_LEN/2 + i * (WAVE_LEN/steps)
            x2 = -WAVE_LEN/2 + (i+1) * (WAVE_LEN/steps)
            z1 = BASE_H + WAVE_AMP + WAVE_AMP * math.sin(i/steps * WAVE_PERIODS * 2 * math.pi)
            z2 = BASE_H + WAVE_AMP + WAVE_AMP * math.sin((i+1)/steps * WAVE_PERIODS * 2 * math.pi)
            
            cyl1 = Part.makeSphere(WAVE_WIDTH/2, FreeCAD.Vector(x1, y_off, z1))
            cyl2 = Part.makeSphere(WAVE_WIDTH/2, FreeCAD.Vector(x2, y_off, z2))
            base = base.fuse(cyl1).fuse(cyl2)
    
    return base

def create_lid_v2():
    """Lid with wave spline grooves"""
    lid = rounded_box(EXTERIOR_L, EXTERIOR_W, LID_H)
    
    WAVE_AMP = 3.2
    WAVE_PERIODS = 2
    WAVE_WIDTH = 8.4
    WAVE_OFFSET = 35
    WAVE_LEN = EXTERIOR_L - 48
    steps = 30
    
    for y_off in [-WAVE_OFFSET, WAVE_OFFSET]:
        for i in range(steps):
            x1 = -WAVE_LEN/2 + i * (WAVE_LEN/steps)
            x2 = -WAVE_LEN/2 + (i+1) * (WAVE_LEN/steps)
            z1 = WAVE_AMP + WAVE_AMP * math.sin(i/steps * WAVE_PERIODS * 2 * math.pi)
            z2 = WAVE_AMP + WAVE_AMP * math.sin((i+1)/steps * WAVE_PERIODS * 2 * math.pi)
            
            cyl1 = Part.makeSphere(WAVE_WIDTH/2, FreeCAD.Vector(x1, y_off, z1))
            cyl2 = Part.makeSphere(WAVE_WIDTH/2, FreeCAD.Vector(x2, y_off, z2))
            lid = lid.cut(cyl1).cut(cyl2)
    
    return lid

def create_base_v3():
    """Base with studs on top AND holes on bottom"""
    base = rounded_box(EXTERIOR_L, EXTERIOR_W, BASE_H)
    pocket = rounded_box(POCKET_L, POCKET_W, POCKET_D + 1, r=3.2)
    pocket.translate(FreeCAD.Vector(0, 0, BASE_H - POCKET_D))
    base = base.cut(pocket)
    
    STUD_R = 5
    STUD_H = 4
    HOLE_R = 5.2
    HOLE_D = 4.5
    INSET = 18
    
    positions = [
        (EXTERIOR_L/2 - INSET, EXTERIOR_W/2 - INSET),
        (EXTERIOR_L/2 - INSET, -EXTERIOR_W/2 + INSET),
        (-EXTERIOR_L/2 + INSET, EXTERIOR_W/2 - INSET),
        (-EXTERIOR_L/2 + INSET, -EXTERIOR_W/2 + INSET),
    ]
    
    # Add studs on top
    for x, y in positions:
        stud = Part.makeCylinder(STUD_R, STUD_H)
        stud.translate(FreeCAD.Vector(x, y, BASE_H))
        base = base.fuse(stud)
    
    # Cut holes on bottom
    for x, y in positions:
        hole = Part.makeCylinder(HOLE_R, HOLE_D + 1)
        hole.translate(FreeCAD.Vector(x, y, -0.5))
        base = base.cut(hole)
    
    return base

def create_lid_v3():
    """Lid with studs on top AND holes on bottom (same as base)"""
    lid = rounded_box(EXTERIOR_L, EXTERIOR_W, LID_H)
    
    STUD_R = 5
    STUD_H = 4
    HOLE_R = 5.2
    HOLE_D = 4.5
    INSET = 18
    
    positions = [
        (EXTERIOR_L/2 - INSET, EXTERIOR_W/2 - INSET),
        (EXTERIOR_L/2 - INSET, -EXTERIOR_W/2 + INSET),
        (-EXTERIOR_L/2 + INSET, EXTERIOR_W/2 - INSET),
        (-EXTERIOR_L/2 + INSET, -EXTERIOR_W/2 + INSET),
    ]
    
    # Add studs on top
    for x, y in positions:
        stud = Part.makeCylinder(STUD_R, STUD_H)
        stud.translate(FreeCAD.Vector(x, y, LID_H))
        lid = lid.fuse(stud)
    
    # Cut holes on bottom
    for x, y in positions:
        hole = Part.makeCylinder(HOLE_R, HOLE_D + 1)
        hole.translate(FreeCAD.Vector(x, y, -0.5))
        lid = lid.cut(hole)
    
    return lid

if __name__ == "__main__":
    print("Creating V2 curved (wave spline)...")
    base_v2 = create_base_v2()
    base_v2.exportStep("locked-in-base-v2-curved.step")
    print("  Base V2 exported")
    
    lid_v2 = create_lid_v2()
    lid_v2.exportStep("locked-in-lid-v2-curved.step")
    print("  Lid V2 exported")
    
    print("Creating V3 lego (studs+holes both sides)...")
    base_v3 = create_base_v3()
    base_v3.exportStep("locked-in-base-v3-lego.step")
    print("  Base V3 exported")
    
    lid_v3 = create_lid_v3()
    lid_v3.exportStep("locked-in-lid-v3-lego.step")
    print("  Lid V3 exported")
    
    print("Done!")
