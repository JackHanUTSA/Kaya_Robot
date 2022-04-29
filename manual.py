
from numpy import np


# T give general location matrix

T_Vel = np.array([[1,0,0],[0,1,0],[-1,0,0],[0,-1,0],[0,0,0]])
T1_Vel = T_Vel.T
#print('T1_Vel',T1_Vel)
T_Pose = np.array([[0,0,0],[0.1,0,0],[-0.1,0,0]])
T1_Pose = T_Pose.T
#print('T1_Pose',T1_Pose)
Target_Pose = np.array([[1,1,0]])
#Target_Pose = Target_Pose.T







#///////////////////////////////////////////////////////////////////////////////////
#Test routines
#///////////////////////////////////////////////////////////////////////////////////

#####################################
#           velocity tests
####################################

#move_robot_speed_trajectory_xyt(T1_Vel,speed_percentage,timer)

#test_move_speed_xyt_sync(speed_percentage,timer)  #>>funciona
#test_move_speed_sync(ALL_MOTORS,speed_percentage) #>>funciona

#####################################
#           position tests
####################################

#test_multi_turn_angles(motor_ID,speed_percentage,timer) #>>funciona
# move_multi_turn (motor_ID, T1_Pose[0,1],speed_percentage,timer) #>>funciona
#move_multi_turn_sync (motor_ID, 15000,speed_percentage,timer,True)  #>>funciona
#action(motor_ID)

#move_robot_position_xyt(T1_Pose[:,1],speed_percentage,timer)
#move_robot_position_trajectory_xyt(T1_Pose,speed_percentage,timer)        



def test_joint_angles(motor_ID):
    
    torque_disable(motor_ID) 
    mode = "Joint"
    Mode(motor_ID, mode)
    torque_enable(motor_ID) 
    angles = [0, 4095]
    move_motor_angles(motor_ID,angles,speed_percentage)
    return [0]


def test_multi_turn_angles(motor_ID,speed_percentage,timer):
    
    torque_disable(motor_ID) 
    mode = "Multi-turn"
    Mode(motor_ID, mode)
    torque_enable(motor_ID) 
    angles = [-15000,15000]
    move_motor_multi_turn_angles(motor_ID,angles,speed_percentage,timer)
    return[1]

def test_move_speed_sync(motor_ID,speed):
    
    torque_disable(motor_ID) 
    mode = "Wheel"
    Mode(motor_ID, mode)
    torque_enable(motor_ID) 


    for i in range(1):
        move_motor_speed(motor_ID,speed,"CW",True,timer)
        action(motor_ID)
        time.sleep(5)   
        move_motor_speed(motor_ID,speed,"CCW",True,timer)
        action(motor_ID)
        time.sleep(5)          
    stop_speed (motor_ID)  


def test_move_speed_xyt_sync(speed,timer) :

    for i in range(1):
        speed_x = speed
        speed_y = 0
        w_body = 0
        dir = np.array([speed_x,speed_y,w_body])
        move_robot_speed_xyt(dir,speed,timer)
        action(ALL_MOTORS)
        time.sleep(2)   
        
        speed_x = 0
        speed_y =speed
        w_body = 0     
        dir = np.array([speed_x,speed_y,w_body])
        move_robot_speed_xyt(dir,speed,timer)
        action(ALL_MOTORS)
        time.sleep(2)   
      
  
                   
    stop_speed (motor_ID)  

    return [1]


def test_move_robot_position_xyt(distance,speed):

    torque_disable(ALL_MOTORS) 
    mode = "Multi-turn"
    #mode = "Wheel"
    Mode(ALL_MOTORS, mode)
    torque_enable(ALL_MOTORS) 
    
    
    for i in range(1):
        #Create the movement distance
        distance_x = distance
        distance_y = 0
        angle_body = 0
        Pose = np.array([distance_x,distance_y,angle_body])

        move_robot_position_xyt(Pose,speed,True)
        action(ALL_MOTORS)
        #time.sleep(3)   
        
        distance_x = 0
        distance_y = distance
        angle_body = 0     
        Pose = np.array([distance_x,distance_y,angle_body])
        move_robot_position_xyt(Pose,speed,True)
        action(ALL_MOTORS)
        #time.sleep(3)   
      
  
                   
    stop_speed (motor_ID)  

    return [1]



def create_trajectory(x,y,theta,points):


    Path = np.zeros([3,len(x)])

    T = np.empty([3,points*len(x)],dtype = float)
    xxx = []
    yyy = []
    ttt = []

    print("xxx values are:\n",xxx)
    print("\n")
    print("yyy values are:\n", yyy)
    print("\n")



    print("x values are:\n",x)
    print("\n")
    print("y values are:\n", y)
    print("\n")
    for idx in range (len(x)):
        Path[0,idx] =  x[idx] 
        Path[1,idx] = y[idx] 
        Path[2,idx] = theta[idx] 
    print("PAth:\n")       
    print(Path)
    #plt.scatter(x,y)


    for idx in range (len(x)-1):
        xx = np.linspace(Path[0,idx],Path[0,idx+1],points)

        m = (Path[1,idx+1]-Path[1,idx])/(Path[0,idx+1]-Path[0,idx])
        b = Path[1,idx+1] - m * Path[0,idx+1]
        yy = m *xx + b

        tt = np.linspace(Path[2,idx],Path[2,idx+1],points)
        print("(xx, yy, tt) = ",xx, yy,tt)


        xxx.append(xx)
        x4 = np.stack(xxx, axis = 0)
        x5 = np.concatenate(x4,axis = 0)
        
        yyy.append(yy)
        y4 = np.stack(yyy, axis = 0)
        y5 = np.concatenate(y4,axis = 0)


        ttt.append(tt)
        t4 = np.stack(ttt, axis = 0)
        t5 = np.concatenate(t4,axis = 0)
        
        
        #plt.plot(xx,yy)
    print("x5 values are:\n",x5)
    print("\n")
    print("y5values are:\n", y5)
    print("\n")
    print("t5values are:\n", t5)
    print("\n")
    #plt.plot(x5,y5)
        
    T = np.array([x5,y5,t5],dtype = float)    
    print("T values:\n")
    print(T)
        
    #plt.plot(T[0,:],T[1,:])


    return (T)

#///////////////////////////////////////////////////////////////////////////////////


def read_modbus_commands():

    if emergency_stop :#EMERGENCY STOP

        stop_speed (ALL_MOTORS)
        torque_disable(ALL_MOTORS) 


    if reset_robot: #Init Robot in Wheel mode
        
        print("Rebooting motors")
        reboot_motors()
        torque_disable(ALL_MOTORS) 
        mode = "Wheel"
        Mode(ALL_MOTORS, mode)
        torque_enable(ALL_MOTORS) 
        set_speed(ALL_MOTORS,0)
    
  


    '''
    if enable_open_loop_trajectory_control: #move_robot_speed_trajectory_xyt  by time
    
        timer = 2
        speed_percentage = 15
        move_robot_speed_trajectory_xyt(T1_Vel,speed_percentage,timer)
    '''


        
    if enable_trajectory_control2:
        x_points = np.array([10,20,30,40,50,60])
        y_points = np.array([10,20,30,40,50,60])
        theta_points = np.array([0,0,0,0,0,0,0])
        points = 10
    
        T = create_trajectory(x_points,y_points,theta_points,points)
        timer = 0.1
        move_robot_position_trajectory_xyt(T, speed_percentage,timer)
        

        
    return (1)




def get_global_coordinates():

#Tag35H11_0  is the origin of the (x,y) coordinate system
#Tag35H11_1  is the x Axis. I use it to scale the coordinates
#Tag35H11_2  is the y Axis. I use it to scale the coordinates
#Tag35H11_3  is the UGV position
#Tag35H11_4  is the Target position

#REGISTERS DEFINITIONS
    
    X_O = 2
    Y_O = 3
    T_O = 4


    X_X = X_O + 4
    Y_X = Y_O + 4
    T_X = T_O + 4

    X_Y = X_O + 8
    Y_Y = Y_O + 8
    T_Y = T_O + 8

    X_R = X_O + 12
    Y_R = Y_O + 12
    T_R = T_O + 12

    X_T = X_O + 16
    Y_T = Y_O + 16
    T_T = T_O + 16


    registers = client.read_holding_registers(0, 25)
    #print(registers)
    num_tags = registers[0]
    if num_tags ==0:
        print('No tags found..')
        
    else :
        if registers[X_O-1]  == 1 :
            print('Tag_0 found')
        if registers[X_X-1]  == 2 :
            print('Tag_1 found')
        if registers[X_Y-1]  == 3 :
            print('Tag_2 found')
        if registers[X_R-1] == 4 :
            print('Tag_3 found')
        if registers[X_T-1]  == 5 :
            print('Tag_4 found')


    origin[0:3] = [registers[X_O],registers[Y_O],registers[T_O]]
    x_axis[0:3] = [registers[X_X],registers[Y_X],registers[T_X]]
    y_axis[0:3] = [registers[X_Y],registers[Y_Y],registers[T_Y]]

    frame [0:3] = [origin,x_axis,y_axis]
    robot_position[0:3] = [registers[X_R],registers[Y_R],registers[T_R]]
    target_position[0:3] = [registers[X_T],registers[Y_T],registers[T_T]]


    print('\nframe =', frame)
    print('\nrobot_position =', robot_position)
    print('\ntarget_position =', target_position)

    #time.sleep(0.5)


    return  robot_position, target_position
