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

// Base board specs
BASE_W = 60;
BASE_MARGIN = 3.5;
SCREW_DIST = 2; // Distance between screw holes on the base board

// Screw specs
M3_RADIUS = 1.5;
M3_CAP_HEIGHT = 2; // Screw cap height

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

module batteryHolderArm()
{
    difference()
    {
        translate([-ARM_THICKNESS, 0, -BASE_THICKNESS])
        {
            height = BATTERY_PACK_SIZE[2] + 
                BASE_THICKNESS + TOP_COVER_THICKNESS + TOP_EXTRA_SPACE + 
                TOP_ARM_THICKNESS; 

            cube([BATTERY_PACK_SIZE[0] + ARM_THICKNESS * 2, 
                BATTERY_PACK_SIZE[1],
                height]);

        }
        translate([0, -0.2, 0])
            cube(BATTERY_PACK_SIZE + [0, 0.4, 0]);
        
        translate([0, -0.2, BATTERY_PACK_SIZE[2] + TOP_ARM_THICKNESS])
            cube([BATTERY_PACK_SIZE[0], BATTERY_PACK_SIZE[1] + 0.4, TOP_EXTRA_SPACE]);
    }
}

module drawAll() 
{
    color([0.0, 1.0, 0.0]) 
    {
        batteryHolderArm();
    }
}


drawAll();