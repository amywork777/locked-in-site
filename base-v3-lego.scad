// Locked In V3 - Lego Bump (studs on top, holes on bottom)
// Same geometry for both parts - stackable/interchangeable

EXTERIOR_L = 199;
EXTERIOR_W = 112;
BASE_H = 22;
POCKET_L = 175;
POCKET_W = 88;
POCKET_D = 16;

// Stud/hole params
STUD_R = 5;      // 10mm diameter studs
STUD_H = 4;      // 4mm tall
HOLE_R = 5.2;    // slightly larger for clearance
HOLE_D = 4.5;
INSET = 9;       // from corners - centered on 12mm wall

$fn = 64;

module rounded_box(l, w, h, r=3) {
    hull() {
        for (x = [-l/2+r, l/2-r])
        for (y = [-w/2+r, w/2-r])
            translate([x, y, 0])
                cylinder(r=r, h=h);
    }
}

// Positions for all 4 corners
positions = [
    [EXTERIOR_L/2 - INSET, EXTERIOR_W/2 - INSET],
    [EXTERIOR_L/2 - INSET, -EXTERIOR_W/2 + INSET],
    [-EXTERIOR_L/2 + INSET, EXTERIOR_W/2 - INSET],
    [-EXTERIOR_L/2 + INSET, -EXTERIOR_W/2 + INSET],
];

difference() {
    union() {
        // Main base body with pocket
        difference() {
            rounded_box(EXTERIOR_L, EXTERIOR_W, BASE_H);
            translate([0, 0, BASE_H - POCKET_D])
                rounded_box(POCKET_L, POCKET_W, POCKET_D + 1, r=3.2);
        }
        
        // Studs on TOP
        for (pos = positions) {
            translate([pos[0], pos[1], BASE_H])
                cylinder(r=STUD_R, h=STUD_H);
        }
    }
    
    // Holes on BOTTOM
    for (pos = positions) {
        translate([pos[0], pos[1], -0.5])
            cylinder(r=HOLE_R, h=HOLE_D + 0.5);
    }
}
