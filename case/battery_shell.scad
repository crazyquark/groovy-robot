/*
The base of the robot which will encase the battery pack
and hold the RPi
*/

include <PiHole.scad>
include <camera.scad>

// Battery pack specs
BATTERY_PACK_SIZE = [64, 59, 31]; // W x L x H
ARM_THICKNESS = 6; 
BASE_THICKNESS = 1.1;
TOP_COVER_THICKNESS = 3; // This is for the screw
TOP_ARM_THICKNESS = 5;   // This is for the battery pack
TOP_EXTRA_SPACE = 15;
ARM_WIDTH = 10;

// Base board specs
BASE_W = 60;
BASE_MARGIN = 3.5;
SCREW_DIST = 2.1; // Distance between screw holes on the base board

// Screw specs
M3_RADIUS = 1.6; // +0.1 for 3D printing shrinkage
M3_CAP_HEIGHT = 2; // Screw cap height

PI_SCREW_DIST = 48.5;
PI_WIDITH = piBoardDim("3B")[1];
PI_HOLE_LOC_1 = piHoleLocations("3B")[0][0];
PI_HOLE_LOC_2 = piHoleLocations("3B")[2][1];
echo("Pi hole loc 1:", PI_HOLE_LOC_1);
echo("Pi hole loc 2:", PI_HOLE_LOC_2);

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

    boardAlign = BATTERY_PACK_SIZE[1] - PI_WIDITH;
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

module drawAll() 
{
    color([0.0, 1.0, 0.0]) 
    {
        rotate([90, 0, 0])
            batteryHolderArm();
    }
}


drawAll();
//piBoard("3B");