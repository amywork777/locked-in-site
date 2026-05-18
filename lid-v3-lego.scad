// Locked In V3 - Lego Bump Lid (studs on top, holes on bottom)
// Same geometry as base - stackable/interchangeable

EXTERIOR_L = 199;
EXTERIOR_W = 112;
LID_H = 10;

// Stud/hole params
STUD_R = 5;
STUD_H = 4;
HOLE_R = 5.2;
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

positions = [
    [EXTERIOR_L/2 - INSET, EXTERIOR_W/2 - INSET],
    [EXTERIOR_L/2 - INSET, -EXTERIOR_W/2 + INSET],
    [-EXTERIOR_L/2 + INSET, EXTERIOR_W/2 - INSET],
    [-EXTERIOR_L/2 + INSET, -EXTERIOR_W/2 + INSET],
];

difference() {
    union() {
        rounded_box(EXTERIOR_L, EXTERIOR_W, LID_H);
        
        // Studs on TOP
        for (pos = positions) {
            translate([pos[0], pos[1], LID_H])
                cylinder(r=STUD_R, h=STUD_H);
        }
    }
    
    // Holes on BOTTOM
    for (pos = positions) {
        translate([pos[0], pos[1], -0.5])
            cylinder(r=HOLE_R, h=HOLE_D + 0.5);
    }
}
