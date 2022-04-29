# Kaya Code Reconstruct 


> This construct come from **v-12 module** `Kaya_robot_Control_v12.py`

˝
## Quick shortcut guide for **VScode**

**For Mac**
- fold innermost uncollapsed region: ⌘ + ⌥ + [

**For Windows/Linux**

- fold innermost uncollapsed region: ⌃ + ⇧ + [


### Initialization 

- Communication check
- vision check
- robot IMU check
- battery check
- system status : ready

### System

- system status: `system_status == 1` means ready
- system report: `system_report()` print all initialization parameters

### Configuration

At here we define/initial several things

- mode
- motor_ID
- speed_percentage
- timer
- user_command
- $(x,y,\theta)$



### Motors

This section contain all driver for the motor and the available, all the functions focus on driving each motor as individual 
- initial platform
	- ping
	- reboot
	- action
	- torque_enable
	- torque_disable
- position mode
- speed mode


### Robot 

Drive the robot to go as a unified body. All motors/wheels work together.
In this module should given the input parameters and the robot dynamic model the output should be the send to the motors 

- robot status: standby/busy/shtopped/need charge
- robot initial: reset all sensors, motors, get the position/location($x,y,\omega$)  form `vision`
- robot target: given location($x,y,\omega$) call motor control command
- robot info: given `robot_info()` and give the current location($x,y,\omega$) 
- robot stop: given `robot_stop()` and output shutdown all motors
- robot home: given `robot_home()` and output back to the initial position



- set speed `set_speed`
- stop `stop_speed`
- move the body `move_motor_speed` : direction = 'CCW' / 'CW'
- move the body `move_motor_speed2` : direction = '+' / '-'


### Controller 

Move the robot to specific location, before you load this module you need to load the `robot` and `vision` module to make it work 

- SPEED CONTROL
	- move robot to desire location with speed control : `move_robot_speed_xyt`
	- move robot to a set of way points : `move_robot_speed_trajectory_xyt`
- POSITION CONTROL
	- move robot to desired location with position control: `move_robot_target_real_xyt`
	- move robot to position : `move_robot_position_real_xyt`
	- move robot to target with trajectory : `move_robot_trajectory_real_xyt` 

- MULTI-CONTROL
	- ==move robot with input $x,y,\omega$==
	- move a robot with given trajectory in chart: `move_robot_position_trajectory_xyt`


### Manual 

You need to import motors and controller to make this work properly. This package give the basic test for given system. You can physically exam the robot to determine if it is running properly.\
 
In this module, we provide several functions to test the wheels and encoders' functionalities, and move to desire target(this is open loop control!)

- test joint angles: `test_joint_angles`
- test multi turn angles: `test_multi_turn_angles` make more turns with given speed
- test move speed sync: `test_move_speed_sync` move all wheels 
- move to location($x,y,\omega$) in speed mode: `test_move_speed_xyt_sync`
- move to location($x,y,\omega$) in position mode: `test_move_robot_position_xyt`
- create a trajectory($x,y,\omega$): `create_trajectory`	


### Main 

- serial port test
- 




