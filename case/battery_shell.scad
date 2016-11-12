/*
The base of the robot which will encase the battery pack
and hold the RPi
*/

include <PiHole.scad>

// Battery pack specs
BATTERY_PACK_SIZE = [63, 59, 31]; // W x L x H
ARM_THICKNESS = 3.5; 
BASE_THICKNESS = 1.1;
TOP_COVER_THICKNESS = 1.5; // This is for the screw
TOP_ARM_THICKNESS = 5;   // This is for the battery pack
TOP_EXTRA_SPACE = 15;
ARM_WIDTH = 10;

// Base board specs
BASE_W = 60;
BASE_MARGIN = 3.5;
SCREW_DIST = 2.1; // Distance between screw holes on the base board

// Screw specs
M3_RADIUS = 1.5;
M3_CAP_HEIGHT = 2; // Screw cap height

PI_SCREW_DIST = 48.5;
PI_WIDITH = piBoardDim("3B")[1];
PI_HOLE_LOC_1 = piHoleLocations("3B")[0][0];
PI_HOLE_LOC_2 = piHoleLocations("3B")[2][1];
echo("Pi hole loc 1:", PI_HOLE_LOC_1);
echo("Pi hole loc 2:", PI_HOLE_LOC_2);

// Camera
PI_CAM_WIDTH = 30; // case dimensions
PI_CAM_LENGTH = 28;
PI_CAM_HEIGHT = 8;

$fn = 20;
epsilon = 0.02;

module piSupport()
{
    piBoard("3B");
}

module camFork()
{
    union()
    {
        cube([SHELL_THICKNESS * 3, SHELL_THICKNESS * 2, SHELL_THICKNESS]);
        translate([SHELL_THICKNESS * 3, 0, 0])
            cube([SHELL_THICKNESS * 1.3, SHELL_THICKNESS * 2, BASE_HEIGHT * 1.7]);
    }
}

module batteryPack()
{
    cube(BATTERY_PACK_SIZE);    
}

module drill(pos, size, z)
{
     translate([pos, SCREW_DIST * 2, z])
        #cylinder(r = M3_RADIUS, size, center = true);
}

module batteryHolderArm()
{
    middle = BATTERY_PACK_SIZE[0] / 2;

    boardAlign = (ARM_THICKNESS + BATTERY_PACK_SIZE[1] - PI_WIDITH) / 2;
    echo("Board align:", boardAlign);

    hole1 = PI_HOLE_LOC_1 + boardAlign;
    echo("Screw 1 pos:", hole1);

    hole2 = PI_HOLE_LOC_2 + boardAlign;
    echo("Screw 1 pos:", hole2);
    
    height = BATTERY_PACK_SIZE[2] + 
        BASE_THICKNESS + TOP_COVER_THICKNESS + TOP_EXTRA_SPACE + 
        TOP_ARM_THICKNESS; 
    echo("Total height:", height);

    difference()
    {
        translate([-ARM_THICKNESS, 0, -BASE_THICKNESS])
        {

            cube([BATTERY_PACK_SIZE[0] + ARM_THICKNESS * 2, 
                ARM_WIDTH,
                height]);

        }
        translate([0, -0.2, 0])
            cube(BATTERY_PACK_SIZE + [0, 0.4, 0]);
        
        translate([0, -0.2, BATTERY_PACK_SIZE[2] + TOP_ARM_THICKNESS])
            cube([BATTERY_PACK_SIZE[0], BATTERY_PACK_SIZE[1] + 0.4, TOP_EXTRA_SPACE]);
        
        holeDist = SCREW_DIST + M3_RADIUS * 2;

        drill(middle, BATTERY_PACK_SIZE[1] / 4, 0);

        drill(middle - holeDist * 5, BATTERY_PACK_SIZE[1] / 4, 0);                
        drill(middle + holeDist * 5, BATTERY_PACK_SIZE[1] / 4, 0);

        drill(middle - holeDist * 3, BATTERY_PACK_SIZE[1] / 4, 0);                
        drill(middle + holeDist * 3, BATTERY_PACK_SIZE[1] / 4, 0);  

        drill(hole1,  BATTERY_PACK_SIZE[1] / 4, height);
        drill(hole2,  BATTERY_PACK_SIZE[1] / 4, height);
    }
}

module cameraHolder()
{
    holderLen = 15;
    shellThickness = 1.5;

    union()
    {
        import("camera_front.stl");
        difference()
        {
            translate([PI_CAM_WIDTH / 2, PI_CAM_LENGTH + holderLen / 2, PI_CAM_HEIGHT / 2 - 0.1])
                cube([PI_CAM_HEIGHT, holderLen, PI_CAM_HEIGHT], center = true);
            translate([PI_CAM_WIDTH / 2, PI_CAM_LENGTH + holderLen / 2, PI_CAM_HEIGHT / 2 + 3])        
                cube([PI_CAM_HEIGHT + 1, holderLen - 1.5, PI_CAM_HEIGHT - 0.5], center = true);
            
            translate([PI_CAM_WIDTH / 2, PI_CAM_LENGTH + 15, shellThickness + 4])
                rotate([90, 0, 0])
                    cylinder(r = shellThickness, h = 10, center = true);            
        }
    }
}

module drawAll() 
{
    color([0.0, 1.0, 0.0]) 
    {
        rotate([90, 0, 0])
            batteryHolderArm();
        //cameraHolder();
    }
}


drawAll();
//piBoard("3B");