// Locked In V2 - Curved Sidewall with Spline Profile
// Wave/spline ridge on sides that nests into matching groove in lid

EXTERIOR_L = 199;
EXTERIOR_W = 112;
BASE_H = 22;
POCKET_L = 175;
POCKET_W = 88;
POCKET_D = 16;

// Wave params
WAVE_AMPLITUDE = 3;   // height of wave
WAVE_PERIODS = 2;     // number of wave cycles
WAVE_WIDTH = 8;       // width of the wave channel
WAVE_OFFSET = 35;     // distance from center on Y axis

$fn = 64;

module rounded_box(l, w, h, r=3) {
    hull() {
        for (x = [-l/2+r, l/2-r])
        for (y = [-w/2+r, w/2-r])
            translate([x, y, 0])
                cylinder(r=r, h=h);
    }
}

// Spline wave ridge along X axis
module wave_ridge(length, width, amplitude, periods) {
    steps = 30;
    step_len = length / steps;
    
    for (i = [0:steps-1]) {
        x1 = -length/2 + i * step_len;
        x2 = -length/2 + (i + 1) * step_len;
        z1 = amplitude * sin(i / steps * periods * 360);
        z2 = amplitude * sin((i + 1) / steps * periods * 360);
        
        hull() {
            translate([x1, 0, z1])
                cylinder(r=width/2, h=0.1);
            translate([x2, 0, z2])
                cylinder(r=width/2, h=0.1);
        }
    }
}

difference() {
    union() {
        rounded_box(EXTERIOR_L, EXTERIOR_W, BASE_H);
        
        // Wave ridges on both sides
        for (y_off = [-WAVE_OFFSET, WAVE_OFFSET]) {
            translate([0, y_off, BASE_H + WAVE_AMPLITUDE])
                wave_ridge(EXTERIOR_L - 50, WAVE_WIDTH, WAVE_AMPLITUDE, WAVE_PERIODS);
        }
    }
    
    // Phone pocket
    translate([0, 0, BASE_H - POCKET_D])
        rounded_box(POCKET_L, POCKET_W, POCKET_D + 1, r=3.2);
}
