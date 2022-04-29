# Controller Module

# this module need the vision, robot and robot_model module


def move_robot_speed_xyt(dir_n, speed_control,timer_speed):
# dir_n is a column vector with the NORMALIZED direction velocities in x,y and body:  dir = [x,y,w]

    print('move_robot_speed_xyt: timer = ', timer_speed, ' direction =',dir)
    
    '''
    torque_disable(ALL_MOTORS) 
    mode = "Wheel"
    Mode(ALL_MOTORS, mode)
    torque_enable(ALL_MOTORS) 
    '''
    
    print(dir_n)

    
    # USe kinematic model of Kaya Robot for getting the wheels angular velocities
    ohmegas = 1/r *np.dot(kaya_inv_kine,dir_n)
    print('ohmegas',ohmegas)

    #calculate  the normalized speed
    #speed = math.trunc(speed_control/100.0*MAX_MOVE_SPEED)
    speed = speed_control
    print ( 'speed_control', speed_control)
    print ( 'speed', speed) 
    

    speed_wh1 = int(speed * ohmegas[0] )
    speed_wh2 = int(speed * ohmegas[1] )
    speed_wh3 = int(speed * ohmegas[2] )

    print('speed_wh1 = ',speed_wh1)
    print('speed_wh2 = ',speed_wh2)
    print('speed_wh3 = ',speed_wh3)

    sync = True  #all motors should move at the same time
    timer_motor = 0 # this avoids the individual motors to wait the timer    
    move_motor_speed2 (1, speed_wh1,sync,timer_motor)    #wheel 1     
    move_motor_speed2 (2, speed_wh2,sync,timer_motor)   #wheel 2   
    move_motor_speed2 (3, speed_wh3,sync,timer_motor)    #wheel 3
        

    action(ALL_MOTORS)
    
    # requested timer for movement
    # timer = 0 do not stop the motor
    if timer_speed != 0.0:
        time.sleep(timer_speed)     
        #stop_speed (ALL_MOTORS)  
        
        
    return [1]


def move_robot_speed_trajectory_xyt(dir_array,speed,timer_speed):
    print('move_robot_speed_trajectory_xyt:  direction = \n',dir_array)

    torque_disable(ALL_MOTORS) 
    mode = "Wheel"
    Mode(ALL_MOTORS, mode)
    torque_enable(ALL_MOTORS) 
    
    for idx in range(dir_array.shape[1]):
            #get the  direction from the array
        vel_x = dir_array[0, idx]
        vel_y = dir_array[1, idx]
        w_body = dir_array[2, idx]
        
        #Get the direction vector
        dir = np.array([vel_x,vel_y,w_body])        
        move_robot_speed_xyt(dir,speed,timer_speed)   

    stop_speed (ALL_MOTORS) 
         
    return [1]






def move_robot_target_real_xyt():
#This is the position control routine called every 100 mSec!!!


    error_x = target_position[0]- robot_position[0]
    error_y = target_position[1]- robot_position[1]
    error_T = target_position[2]- robot_position[2]
    error_T = 0

    #print('error_x: ', error_x)
    #print('error_y: ', error_y)
 

    distance_to_target = sqrt(error_x**2 + error_y**2)

    control_speed = distance_to_target
    #print('control_speed:', control_speed)
    
    #Calculate the direction vector
    dir = np.array([error_x,error_y,error_T]) 
    #print('direction vector = ',dir)   

    #normalize the direction vector
    dir = dir / MAX_CAMERA_DISTANCE  
    #print('Normalized direction vector = ',dir)   
    

    control_velocity = int(control_speed * proportional_gain)

    #print('proportional_gain: ', proportional_gain)
    #print('Control velocity: ', control_velocity)

            
    #if (distance_to_target < 30 and (robot_position[0] < 100) and (robot_position[1] < 100) and (target_position[0] == 0) and (target_position[1] == 0)): 
    if ( (robot_position[0] < 100) and (robot_position[1] < 100) and (target_position[0] == 0) and (target_position[1] == 0)): 

        stop_speed (ALL_MOTORS)
        error_x = 0
        error_y = 0
        error_T = 0
        control_velocity = 0

        print(' ****************  At the Target  ****************') 

    elif distance_to_target > 100:
        stop_speed (ALL_MOTORS)
        error_x = 0
        error_y = 0
        error_T = 0
        control_velocity = 0

        print(' ****************  Out of range  ****************')     
    else:


        #Call the movement routine    
        move_robot_speed_xyt(dir,control_velocity,0)  
        #move_robot_speed_xyt(dir,15,0)  #move at 15% speed  without stopping


    #Update monitoring of variables
    DataBank.set_words(1,[target_position[0]])
    DataBank.set_words(2,[target_position[1]])
    DataBank.set_words(3,[target_position[2]])
    DataBank.set_words(4,[robot_position[0]])
    DataBank.set_words(5,[robot_position[1]])
    DataBank.set_words(6,[robot_position[2]])

    DataBank.set_words(7,[control_velocity])
    #DataBank.set_words(8,[proportional_gain])
    
    DataBank.set_words(9,[error_x])
    DataBank.set_words(10,[error_y])



def move_robot_position_real_xyt(pose):
#This is the position control routine called every 100 mSec!!!


    error_x = pose[0]- robot_position[0]
    error_y = pose[1]- robot_position[1]
    error_T = pose[2]- robot_position[2]
    error_T = 0

    #print('error_x: ', error_x)
    #print('error_y: ', error_y)
 

    distance_to_target = sqrt(error_x**2 + error_y**2)

    control_speed = distance_to_target
    #print('control_speed:', control_speed)
    
    #Calculate the direction vector
    dir = np.array([error_x,error_y,error_T]) 
    #print('direction vector = ',dir)   

    #normalize the direction vector
    dir = dir / MAX_CAMERA_DISTANCE  
    #print('Normalized direction vector = ',dir)   
    

    control_velocity = int(control_speed * proportional_gain)

    #print('proportional_gain: ', proportional_gain)
    #print('Control velocity: ', control_velocity)

            
    if ( distance_to_target < 10.0): 
        print(' ****************  At the Way Point  ****************') 
        arrived = True
    else:
        arrived = False    

    if distance_to_target > 100:
        stop_speed (ALL_MOTORS)
        error_x = 0
        error_y = 0
        error_T = 0
        control_velocity = 0

        print(' ****************  Out of range  ****************')     
    else:


        #Call the movement routine    
        move_robot_speed_xyt(dir,control_velocity,0)  
        #move_robot_speed_xyt(dir,15,0)  #move at 15% speed  without stopping


    #Update monitoring of variables
    DataBank.set_words(1,[pose[0]])
    DataBank.set_words(2,[pose[1]])
    DataBank.set_words(3,[pose[2]])
    DataBank.set_words(4,[robot_position[0]])
    DataBank.set_words(5,[robot_position[1]])
    DataBank.set_words(6,[robot_position[2]])

    DataBank.set_words(7,[control_velocity])
    #DataBank.set_words(8,[proportional_gain])
    
    DataBank.set_words(9,[error_x])
    DataBank.set_words(10,[error_y])

    return (arrived)


def move_robot_trajectory_real_xyt(dir_array):
    print('move_robot_trajectory_real_xyt:  direction = \n',dir_array)

    torque_disable(ALL_MOTORS) 
    mode = "Wheel"
    Mode(ALL_MOTORS, mode)
    torque_enable(ALL_MOTORS) 
    
    

    for idx in range(dir_array.shape[1]):
            #get the  direction from the array
        pos_x = dir_array[0, idx]
        pos_y = dir_array[1, idx]
        w_body = dir_array[2, idx]
        

        #Get the direction vector
        dir = np.array([pos_x,pos_y,w_body]) 

        pose_reached = False
        while pose_reached == False:
            robot_position, target_position = get_global_coordinates()
            pose_reached = move_robot_position_real_xyt(dir)   

    stop_speed (ALL_MOTORS)      
    return [1]

    

def move_robot_position_xyt(Pose,speed,timer_global):
# This function requires Mode = Multi-turn
# Pose is column vector with the  direction angles in x,y and body:  dir = [x,y,angle]

    print('move_robot_angle_xyt: ')
    print('Pose =',Pose)
    
    '''
    torque_disable(ALL_MOTORS) 
    mode = "Multi-turn"
    Mode(ALL_MOTORS, mode)
    torque_enable(ALL_MOTORS) 
    '''
        
    
    # kinematic model of Kaya Robot
    
    angles = 1/r * np.dot(kaya_inv_kine,Pose)
    
    
    #print("angles [rad]",angles)
    angle_wh1 = angles[0] 
    angle_wh2 = angles[1] 
    angle_wh3 = angles[2] 
    #scaling to Kaya robot Dynamixel MX-12 motors
    angle_wh1 = int(angle_wh1 * 180.0/pi/360*MAX_ANGLE)
    angle_wh2 = int(angle_wh2 * 180.0/pi/360*MAX_ANGLE)
    angle_wh3 = int(angle_wh3 * 180.0/pi/360*MAX_ANGLE)
    print("angles int",angle_wh1,angle_wh2,angle_wh3)

    sync = 1  #all the motors should move at the same time
    timer_motor = 0  # don't let each motor to wait the movement finish
    #wheel 1
    move_multi_turn_sync (1, angle_wh1,speed,timer_motor,sync)   
        
    #wheel 2
    move_multi_turn_sync (2, angle_wh2,speed,timer_motor,sync)   

    #wheel 3
    move_multi_turn_sync (3, angle_wh3,speed,timer_motor,sync)   
     
    action(ALL_MOTORS)    


    #wait for the angle to be reached
    if timer_global == 0:
            return[1]
    elif timer_global == -1:
    
        angle_reached = False
        while not angle_reached:
            #print("angle_reached = ", angle_reached)
            m1_done = read_moving_command(1)
            m2_done = read_moving_command(2)
            m3_done = read_moving_command(3)
            if (m1_done and m2_done and m3_done):
                angle_reached = True
                print("angle_reached = ", angle_reached)
                
    else:    
        time.sleep(timer_global)  
            
            
    return [1]


def move_robot_position_trajectory_xyt(T_Pose,speed,timer_trajectory):
#T_Pose is a vector of 3 x No_of_points

    ''' 
    torque_disable(ALL_MOTORS) 
    mode = "Multi-turn"
    #mode = "Wheel"
    Mode(ALL_MOTORS, mode)
    torque_enable(ALL_MOTORS) 
    '''  
    
    for idx in range(T_Pose.shape[1]):
        #get the  angle
        x = T_Pose[0, idx]
        y = T_Pose[1, idx]
        angle_body = T_Pose[2, idx]
        Pose = np.array([x,y,angle_body])
        timer = -1
        move_robot_position_xyt(Pose,speed,timer_trajectory)
        #time.sleep(4)
        
 
        
                
  

    return [1]

