from pyModbusTCP.server import ModbusServer
from pyModbusTCP.server import DataBank
from pyModbusTCP.client import ModbusClient



# Define the Modbus client/server objects here
client = ModbusClient(host = "192.168.0.242",port =  12345)   # Drone Server (Camera info video streaming)
server = ModbusServer("192.168.0.251",12345, no_block = True) # Rover Server 



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


