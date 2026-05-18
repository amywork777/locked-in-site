#!/usr/bin/env python3
"""
Create alternate attachment geometry variants for Locked In phone box.
V2: Curved sidewall
V3: Lego bump (studs on base, holes in lid)
"""

import trimesh
import numpy as np

# Dimensions from original design (mm)
EXTERIOR_L = 199
EXTERIOR_W = 112  
TOTAL_H = 32
BASE_H = 22
LID_H = 10
POCKET_L = 175
POCKET_W = 88
POCKET_D = 16
WALL = 12
CORNER_R = 3.0

def rounded_box(length, width, height, radius=3.0):
    """Create a box with rounded vertical edges."""
    # Start with basic box
    box = trimesh.creation.box([length, width, height])
    # Move so bottom is at z=0
    box.apply_translation([0, 0, height/2])
    return box

def create_base_v2():
    """Base with curved ridge on top for nesting lid."""
    # Main base body
    base = rounded_box(EXTERIOR_L, EXTERIOR_W, BASE_H)
    
    # Phone pocket (subtract from top)
    pocket = rounded_box(POCKET_L, POCKET_W, POCKET_D + 1)
    pocket.apply_translation([0, 0, BASE_H - POCKET_D])
    
    base = trimesh.boolean.difference([base, pocket], engine='blender')
    
    # Add curved ridge along the top rim (wave profile)
    # Create a cylinder segment that curves along the length
    ridge_r = 4  # radius of curve
    ridge = trimesh.creation.cylinder(radius=ridge_r, height=EXTERIOR_W - 20)
    ridge.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1,0,0]))
    ridge.apply_translation([0, 0, BASE_H - ridge_r/2])
    
    base = trimesh.boolean.union([base, ridge], engine='blender')
    
    return base

def create_lid_v2():
    """Lid with curved groove on bottom to match base ridge."""
    # Main lid body
    lid = rounded_box(EXTERIOR_L, EXTERIOR_W, LID_H)
    
    # Curved groove on bottom
    groove_r = 4.2  # slightly larger than ridge for clearance
    groove = trimesh.creation.cylinder(radius=groove_r, height=EXTERIOR_W - 18)
    groove.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1,0,0]))
    groove.apply_translation([0, 0, groove_r/2])
    
    lid = trimesh.boolean.difference([lid, groove], engine='blender')
    
    return lid

def create_base_v3():
    """Base with lego-style studs on rim."""
    # Main base body
    base = rounded_box(EXTERIOR_L, EXTERIOR_W, BASE_H)
    
    # Phone pocket
    pocket = rounded_box(POCKET_L, POCKET_W, POCKET_D + 1)
    pocket.apply_translation([0, 0, BASE_H - POCKET_D])
    
    base = trimesh.boolean.difference([base, pocket], engine='blender')
    
    # Add 4 studs in corners (like lego)
    stud_r = 5  # 10mm diameter studs
    stud_h = 3  # 3mm tall
    stud_inset = 15  # from corners
    
    positions = [
        (EXTERIOR_L/2 - stud_inset, EXTERIOR_W/2 - stud_inset),
        (EXTERIOR_L/2 - stud_inset, -EXTERIOR_W/2 + stud_inset),
        (-EXTERIOR_L/2 + stud_inset, EXTERIOR_W/2 - stud_inset),
        (-EXTERIOR_L/2 + stud_inset, -EXTERIOR_W/2 + stud_inset),
    ]
    
    for x, y in positions:
        stud = trimesh.creation.cylinder(radius=stud_r, height=stud_h)
        stud.apply_translation([x, y, BASE_H + stud_h/2])
        base = trimesh.boolean.union([base, stud], engine='blender')
    
    return base

def create_lid_v3():
    """Lid with holes to receive studs."""
    # Main lid body
    lid = rounded_box(EXTERIOR_L, EXTERIOR_W, LID_H)
    
    # Holes for studs
    hole_r = 5.2  # slightly larger for clearance
    hole_d = 3.5  # deeper than stud for tolerance
    stud_inset = 15
    
    positions = [
        (EXTERIOR_L/2 - stud_inset, EXTERIOR_W/2 - stud_inset),
        (EXTERIOR_L/2 - stud_inset, -EXTERIOR_W/2 + stud_inset),
        (-EXTERIOR_L/2 + stud_inset, EXTERIOR_W/2 - stud_inset),
        (-EXTERIOR_L/2 + stud_inset, -EXTERIOR_W/2 + stud_inset),
    ]
    
    for x, y in positions:
        hole = trimesh.creation.cylinder(radius=hole_r, height=hole_d + 1)
        hole.apply_translation([x, y, hole_d/2])
        lid = trimesh.boolean.difference([lid, hole], engine='blender')
    
    return lid

if __name__ == "__main__":
    print("Creating V2 (curved sidewall)...")
    try:
        base_v2 = create_base_v2()
        base_v2.export('locked-in-base-v2-curved.stl')
        print("  Base V2 exported")
        
        lid_v2 = create_lid_v2()
        lid_v2.export('locked-in-lid-v2-curved.stl')
        print("  Lid V2 exported")
    except Exception as e:
        print(f"  V2 failed: {e}")
    
    print("Creating V3 (lego bump)...")
    try:
        base_v3 = create_base_v3()
        base_v3.export('locked-in-base-v3-lego.stl')
        print("  Base V3 exported")
        
        lid_v3 = create_lid_v3()
        lid_v3.export('locked-in-lid-v3-lego.stl')
        print("  Lid V3 exported")
    except Exception as e:
        print(f"  V3 failed: {e}")
    
    print("Done!")
