Final Project
ECE 4564 NetApps
Team 08

Carson Wittwer
Jason Nelson
MH Charles-Etuk

B O B - Bomb Operation roBot

Included In Folder:
			README
			gamepad.py (source code for controller input)
			arm_controller.py (source code for arm controls - tested and working file)
			arm_track_controller.py (source code for full controls - not tested but complete logic)
			BOB_BetaDemo.pptx (presentation for Beta demo, shows controller, arm, and track mappings)
			
Concept - 	Robotic Arm mounted to Tracked "Tank" Chassis that is connected/controlled
			via RasPi GPIO that is socket networked to another RasPi that is sending 
			commands via a Bluetooth XBox controller
			
Working - 	XBox controller inputs
			Arm Control

Non-Working-Tank Control

Parts - 	OWI-535 Robotic Arm Edge (modified) 
			(https://www.robotshop.com/en/owi-535-robotic-arm-edge.html)
			DFRobotShop Rover Chassis Kit
			https://www.robotshop.com/en/dfrobotshop-rover-chassis-kit.html
			Steelseeries Stratus XL Controller
			https://steelseries.com/gaming-controllers/stratus-xl-for-windows-and-android
			3X L293D Stepper Motor Driver (should have ordered 1 more)
			https://www.amazon.com/NDRTJM-MSTL2930-L293D-Stepper-Driver/dp/B008XCGLNM
			2X RasPi 3B+
			https://www.amazon.com/dp/B07BDR5PDW/ref=cm_sw_r_tw_dp_U_x_1zWcCbEF2J76H
			
Non-Working simple explanation: Did not have a 4th L293D and original motor controller
			was not working with this system. Should have ordered another L293D and would 
			have had all parts working. Also, blew up one of the L293D during testing.
			
Controller Implementation: Carson Wittwer Lead
			The Steelseries Stratus XL controller does not have any standard support for 
			Linux based systems, thus, we had to find another way around. EVDEV was used 
			to translate between Linux standard input and how the controller was to be 
			mapped. After using EVDEV to read in and learn the naming of all the different 
			buttons, joysticks, and triggers on the controller as well as the values that 
			are given when operated, we were able to map the controller's inputs to the 
			commands we wanted (see presentation images and excel spreadshit for details).
			Once those were found, we also needed a way to switch between controlling the 
			Arm and the Tracks. Using one of the buttons on the controller, we set up a 
			value that would read true or false depending on what mode we wanted to be in, 
			toggling every time the button was pressed. Once receiving the signal, we sent 
			a string over socket connection to the RasPi that was connected to the Arm/Tracks.
			This was done for simplicities sake, but encrypting the data over the network 
			should probably be implemented. The program reads the button presses and stick
			movement then print to console the button name when pressed/moved.

Arm Implementation: MH Charles-Etuk Lead, Carson Wittwer assist
			The Arm proved to be an exciting build. We first assembled the arm using the 
			provided instructions, getting it working with the out-of-the-box supplies and
			controller. After this, we set about modifying it. We knew that the out-of-the-box
			controller worked by completing the circuit for a given motor, whether that be 
			completing the circuit with the positive or negative voltage supply. This meant 
			the controller acted as a primitive 3 position switch. This solution would not 
			work for us, as using the RasPi GPIO this way is not the correct way to implement
			this. So, we removed the entire controller circuit, added in the L293D motor drivers
			to control each of the 5 motors (2 motors per chip), and used the GPIO to drive the 
			logic for the L293D. This implementation worked beautifully, where depending on which 
			GPIO pin was selected high, the motors would spin in a certain direction. We use the 
			RasPi 3.3V power to supply power to the chips logic circuits and the 5V power to 
			supply the motors. We received the commands from the controller RasPi via a socket 
			connection and mapped those to the specific functions controlling movement. During 
			testing, this implementation worked out to get a well-dialed in arm.

Track Implementation: Jason Nelson Lead
			After assembling the chassis, tracks, and gearbox, we set about wiring the 
			motors controls. We initially planned to use an Adafruit TB6612 Motor Driver chip,
			as this seemed to be sufficient for implementing and is frequently used on with
			this particular chassis. After much trial and error, we found that this chip proved 
			to be incompatible we our setup. We then set about testing the tracks with one of 
			L293D controller chups. After completing the wiring, logic, and code for this, the 
			tracks was moving, but very slowly if at all. We were getting extremely little voltage 
			and current to the motors, so we assumed our batterys were not able to provide 
			sufficient power. We chose to use a 6V, wall outlet, power supply to the motors. This
			proved to be a fatal error, as this supply destroyed one of our L293D chips. We believe
			this to be one of two problems, some accidently mixed up wiring or over powering the 
			chip. We believe that using the 5V power on the RasPi would have proved to be a better
			solution to powering the motors, as it was the best solution to powering all 5 of the 
			motors in the Arm. Outside of this, we believe our code would have worked to control 
			the tracks.
			