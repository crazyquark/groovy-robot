board_width=25.5;
board_height=23;
board_thick=4.75;
cable_width=18;
cable_thick=1;
side_cover=7.5;
camera_hole_width=10;
camera_hole_height=5.5;
screw_hole_r=2.65;
padding=2.5;
d=0.001;
mount_offset=2*padding+board_width;
mount_thickness=8;

module camHolder()
{
	//camera holder
	difference(){
		cube([board_thick+2*padding, board_width+2*padding, board_height+2*padding]);
		//main compartment
		translate([padding, padding, padding]) cube([board_thick, board_width, board_height+padding+d]);
		//front camera slot
		translate([board_thick+padding-d, padding+side_cover, padding+camera_hole_height]) cube([padding+2*d, camera_hole_width, board_height+padding-camera_hole_height+d]);
		//hole for cable in the bottom
		translate([padding+2,padding+(board_width-cable_width)/2,0]) cube([cable_thick, cable_width+2*d, padding+2*d]);
	}
}

module camMount()
{
	//mount
	difference(){
		//body of mount
		union(){
			translate([0, mount_offset, board_height/2+padding]) rotate([90,0,0]) cylinder(r=board_height/2+padding, h=mount_thickness, $fn=100);
		translate([-board_height/2-padding,mount_offset-mount_thickness,0]) cube([board_height/2+padding,mount_thickness-d,board_height/2+padding]);
		}
		//remove circle sticking out front
		translate([d,0,0]) cube([50, board_width+2*padding+d, board_height+2*padding+d]);
		//add a hole for the M5 nut
		translate([-screw_hole_r-5,mount_offset, board_height/2+padding]) rotate([90,0,0]) cylinder(r=screw_hole_r, h=mount_thickness+2*d, $fn=100);
	}
}

camHolder();

