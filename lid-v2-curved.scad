// Locked In V2 - Curved Sidewall Lid with Spline Groove
// Wave groove on bottom that matches base ridge

EXTERIOR_L = 199;
EXTERIOR_W = 112;
LID_H = 10;

// Wave params (slightly larger for clearance)
WAVE_AMPLITUDE = 3.2;
WAVE_PERIODS = 2;
WAVE_WIDTH = 8.4;
WAVE_OFFSET = 35;

$fn = 64;

module rounded_box(l, w, h, r=3) {
    hull() {
        for (x = [-l/2+r, l/2-r])
        for (y = [-w/2+r, w/2-r])
            translate([x, y, 0])
                cylinder(r=r, h=h);
    }
}

// Spline wave groove (cutter)
module wave_groove(length, width, amplitude, periods) {
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
    rounded_box(EXTERIOR_L, EXTERIOR_W, LID_H);
    
    // Wave grooves on bottom
    for (y_off = [-WAVE_OFFSET, WAVE_OFFSET]) {
        translate([0, y_off, WAVE_AMPLITUDE])
            wave_groove(EXTERIOR_L - 48, WAVE_WIDTH, WAVE_AMPLITUDE, WAVE_PERIODS);
    }
}
