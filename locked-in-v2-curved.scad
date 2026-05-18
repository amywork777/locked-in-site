// Locked In V2 - Curved Sidewall Attachment
// The lid has a curved underside that nests into a curved channel on the base

// Dimensions (mm)
EXTERIOR_L = 199;
EXTERIOR_W = 112;
BASE_H = 22;
LID_H = 10;
POCKET_L = 175;
POCKET_W = 88;
POCKET_D = 16;
WALL = 12;
CORNER_R = 3;

// Curved channel params
CURVE_R = 6;  // radius of the curved channel
CURVE_OFFSET = 30;  // offset from center

$fn = 64;

module rounded_box(l, w, h, r=3) {
    hull() {
        for (x = [-l/2+r, l/2-r])
        for (y = [-w/2+r, w/2-r])
            translate([x, y, 0])
                cylinder(r=r, h=h);
    }
}

module base_v2() {
    difference() {
        union() {
            // Main base body
            rounded_box(EXTERIOR_L, EXTERIOR_W, BASE_H);
            
            // Curved ridge running lengthwise on both sides
            for (y_off = [-CURVE_OFFSET, CURVE_OFFSET]) {
                translate([0, y_off, BASE_H])
                    rotate([0, 90, 0])
                        cylinder(r=CURVE_R, h=EXTERIOR_L-40, center=true);
            }
        }
        
        // Phone pocket
        translate([0, 0, BASE_H - POCKET_D])
            rounded_box(POCKET_L, POCKET_W, POCKET_D + 1, r=3.2);
    }
}

module lid_v2() {
    difference() {
        // Main lid body
        rounded_box(EXTERIOR_L, EXTERIOR_W, LID_H);
        
        // Curved grooves on bottom to match base ridges
        for (y_off = [-CURVE_OFFSET, CURVE_OFFSET]) {
            translate([0, y_off, 0])
                rotate([0, 90, 0])
                    cylinder(r=CURVE_R + 0.3, h=EXTERIOR_L-38, center=true);
        }
    }
}

// Export base
// base_v2();

// Export lid (uncomment to render)
lid_v2();
